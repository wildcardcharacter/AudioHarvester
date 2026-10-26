"""GitHub release checker and Debian package updater for AudioHarvester."""

import json
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

GITHUB_REPO = "wildcardcharacter/AudioHarvester"
RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases/latest"
LATEST_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def version_key(version):
    """Compare dotted numeric versions without depending on extra packages."""
    try:
        return tuple(int(part) for part in version.strip().lstrip("vV").split("."))
    except (AttributeError, TypeError, ValueError):
        raise ValueError(f"Ungültige Versionsnummer: {version}")


def installed_deb_version():
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${Status}\n${Version}", "audioharvester"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    lines = result.stdout.splitlines()
    if result.returncode or len(lines) < 2 or lines[0] != "install ok installed":
        return None
    return lines[1].split(":")[-1]


class ReleaseCheckWorker(QThread):
    succeeded = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def run(self):
        request = urllib.request.Request(
            LATEST_API_URL,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "AudioHarvester"},
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                release = json.loads(response.read(2_000_000).decode("utf-8"))
            version = str(release.get("tag_name", "")).strip().removeprefix("v").removeprefix("V")
            version_key(version)
            asset_name = f"audioharvester_{version}_all.deb"
            asset = next((item for item in release.get("assets", []) if item.get("name") == asset_name), None)
            asset_url = asset.get("browser_download_url", "") if asset else ""
            if asset_url and not asset_url.startswith("https://"):
                raise RuntimeError("Das Release enthält eine ungültige Download-Adresse.")
            self.succeeded.emit({
                "version": version,
                "notes": str(release.get("body", "")).strip(),
                "url": asset_url,
                "asset_name": asset_name,
                "release_url": RELEASES_URL,
            })
        except urllib.error.HTTPError as error:
            self.failed.emit("Auf GitHub wurde noch kein Release gefunden." if error.code == 404 else f"GitHub meldet HTTP {error.code}.")
        except Exception as error:
            self.failed.emit(str(error))


class PackageInstallWorker(QThread):
    progress = pyqtSignal(str)
    succeeded = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, release):
        super().__init__()
        self.release = release

    def run(self):
        package = Path.home() / ".cache" / "audioharvester" / "updates" / self.release["asset_name"]
        try:
            package.parent.mkdir(parents=True, exist_ok=True)
            request = urllib.request.Request(self.release["url"], headers={"User-Agent": "AudioHarvester"})
            self.progress.emit("Updatepaket wird heruntergeladen …")
            with urllib.request.urlopen(request, timeout=30) as response, package.open("wb") as output:
                shutil.copyfileobj(response, output)
            if package.stat().st_size < 1024:
                raise RuntimeError("Das heruntergeladene Debian-Paket ist unerwartet klein.")
            self.progress.emit("Update wird installiert …")
            result = subprocess.run(
                ["pkexec", "apt-get", "install", "-y", str(package)],
                capture_output=True, text=True, timeout=900, check=False,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip().splitlines()
                raise RuntimeError(detail[-1] if detail else f"Installationsfehler ({result.returncode})")
            self.succeeded.emit()
        except Exception as error:
            package.unlink(missing_ok=True)
            self.failed.emit(str(error))
