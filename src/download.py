import re
import json
import subprocess
import sys
from pathlib import Path

from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)
from yt_dlp_manager import find_yt_dlp


class PlaylistInfoWorker(QThread):
    succeeded = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, url, language="Deutsch"):
        super().__init__()
        self.url = url
        self.language = language

    def run(self):
        command = find_yt_dlp()
        if not command:
            self.failed.emit("yt-dlp wurde nicht gefunden." if self.language != "English" else "yt-dlp was not found.")
            return
        try:
            result = subprocess.run(command + ["--flat-playlist", "--dump-single-json", "--no-warnings", self.url], capture_output=True, text=True, timeout=120, check=False)
            if result.returncode:
                detail = (result.stderr or "").strip().splitlines()
                self.failed.emit(detail[-1] if detail else ("Playlist konnte nicht geladen werden." if self.language != "English" else "Could not load the playlist."))
                return
            data = json.loads(result.stdout)
            entries = []
            for index, entry in enumerate(data.get("entries") or [], start=1):
                if entry and entry.get("id"):
                    entries.append({"index": index, "id": str(entry["id"]), "title": str(entry.get("title") or entry["id"])})
            if not entries:
                self.failed.emit("Die Playlist enthält keine auswählbaren Titel." if self.language != "English" else "The playlist has no selectable tracks.")
                return
            self.succeeded.emit(entries)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            self.failed.emit(str(error))


class DownloadWorker(QThread):
    log_message = pyqtSignal(str)
    progress_changed = pyqtSignal(int)
    finished_download = pyqtSignal(int)
    status_changed = pyqtSignal(str)

    def __init__(self, url, audio_format, quality, output_dir, thumbnail, playlist_mode, filename_template="%(title)s", language="Deutsch", playlist_items=None):
        super().__init__()

        self.url = url
        self.audio_format = audio_format
        self.quality = quality
        self.output_dir = output_dir
        self.thumbnail = thumbnail
        self.playlist_mode = playlist_mode
        self.filename_template = filename_template
        self.language = language
        self.playlist_items = playlist_items

    def run(self):
        download_dir = Path(self.output_dir)
        download_dir.mkdir(parents=True, exist_ok=True)

        # Desktop launchers often provide a smaller PATH than a terminal. Check
        # the usual per-user install locations explicitly before giving up.
        yt_dlp = find_yt_dlp()

        if not yt_dlp:
            self.log_message.emit(
                "❌ yt-dlp was not found. Install it with: pipx install yt-dlp"
                if self.language == "English"
                else "❌ yt-dlp wurde nicht gefunden. Installation: pipx install yt-dlp"
            )
            self.finished_download.emit(1)
            return

        cmd = [
            *yt_dlp,
            "-x",
            "--newline",
            "-o",
            str(download_dir / f"{self.filename_template}.%(ext)s")
        ]

        if self.audio_format == "MP3":
            cmd += ["--audio-format", "mp3"]

            if self.quality != "Original":
                bitrate = self.quality.split()[0]
                cmd += [
                    "--postprocessor-args",
                    f"-b:a {bitrate}k"
                ]

        elif self.audio_format == "Opus":
            cmd += ["--audio-format", "opus"]

        elif self.audio_format == "M4A":
            cmd += ["--audio-format", "m4a"]

        if self.thumbnail:
            cmd += [
                "--convert-thumbnails",
                "jpg",
                "--embed-thumbnail",
                "--add-metadata"
            ]

        if self.playlist_mode == "playlist":
            cmd.append("--yes-playlist")
            if self.playlist_items:
                cmd += ["--playlist-items", ",".join(str(item) for item in self.playlist_items)]
        else:
            cmd.append("--no-playlist")

        cmd.append(self.url)

        self.video_title = self.url

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except OSError as error:
            message = (
                f"❌ yt-dlp could not be started: {error}"
                if self.language == "English"
                else f"❌ yt-dlp konnte nicht gestartet werden: {error}"
            )
            self.log_message.emit(message)
            self.finished_download.emit(1)
            return

        for line in self.process.stdout:
            line = line.strip()

            if line:
                self.log_message.emit(line)

            if "[download] Destination:" in line:
                filename = line.split("Destination:", 1)[1].strip()
                self.video_title = Path(filename).stem

            if "[ExtractAudio]" in line:
                self.status_changed.emit("🔄 Converting audio..." if self.language == "English" else "🔄 Konvertiere Audio...")

            if "[EmbedThumbnail]" in line:
                self.status_changed.emit("🖼️ Embedding cover art..." if self.language == "English" else "🖼️ Bette Coverbild ein...")

            if "[Metadata]" in line:
                self.status_changed.emit("📝 Writing metadata..." if self.language == "English" else "📝 Schreibe Metadaten...")

            match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", line)

            if match:
                percent = int(float(match.group(1)))
                self.progress_changed.emit(percent)

        self.process.wait()
        self.finished_download.emit(self.process.returncode)

    def stop(self):
        if hasattr(self, "process") and self.process:
            self.process.terminate()
