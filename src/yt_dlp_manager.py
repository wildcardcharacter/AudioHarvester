"""Locate and manage the yt-dlp executable used by AudioHarvester."""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


def find_yt_dlp():
    home = Path.home()
    candidates = [
        home / ".local/bin/yt-dlp",
        home / ".local/share/pipx/venvs/yt-dlp/bin/yt-dlp",
        home / ".local/pipx/venvs/yt-dlp/bin/yt-dlp",
        Path("/usr/local/bin/yt-dlp"), Path("/usr/bin/yt-dlp"),
    ]
    executable = next((str(path) for path in candidates if path.is_file()), None)
    executable = executable or shutil.which("yt-dlp")
    if executable:
        return [executable]
    if importlib.util.find_spec("yt_dlp") is not None:
        return [sys.executable, "-m", "yt_dlp"]
    return None


def get_yt_dlp_version():
    command = find_yt_dlp()
    if not command:
        return None
    try:
        result = subprocess.run(command + ["--version"], capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def get_yt_dlp_update_command():
    command = find_yt_dlp()
    if not command:
        return None
    executable = Path(command[0]).resolve()
    if executable.name == "yt-dlp" and "pipx" in str(executable):
        pipx = shutil.which("pipx")
        return [pipx, "upgrade", "yt-dlp"] if pipx else None
    if executable.name == "yt-dlp" and str(executable).startswith(("/usr/bin/", "/bin/")):
        return ["pkexec", "apt-get", "install", "--only-upgrade", "-y", "yt-dlp"]
    if executable.name == "yt-dlp":
        return command + ["-U"]
    return None
