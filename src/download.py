import re
import shutil
import subprocess
from pathlib import Path

from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)


class DownloadWorker(QThread):
    log_message = pyqtSignal(str)
    progress_changed = pyqtSignal(int)
    finished_download = pyqtSignal(int)
    status_changed = pyqtSignal(str)

    def __init__(self, url, audio_format, quality, output_dir, thumbnail, playlist_mode):
        super().__init__()

        self.url = url
        self.audio_format = audio_format
        self.quality = quality
        self.output_dir = output_dir
        self.thumbnail = thumbnail
        self.playlist_mode = playlist_mode

    def run(self):
        download_dir = Path(self.output_dir)
        download_dir.mkdir(parents=True, exist_ok=True)

        yt_dlp_local = Path.home() / ".local" / "bin" / "yt-dlp"

        if yt_dlp_local.is_file():
            yt_dlp = str(yt_dlp_local)
        else:
            yt_dlp = shutil.which("yt-dlp")

        if not yt_dlp:
            self.log_message.emit("❌ yt-dlp wurde nicht gefunden.")
            self.finished_download.emit(1)
            return

        cmd = [
            yt_dlp,
            "-x",
            "--newline",
            "-o",
            str(download_dir / "%(title)s.%(ext)s")
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
        else:
            cmd.append("--no-playlist")

        cmd.append(self.url)

        self.video_title = self.url

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        for line in self.process.stdout:
            line = line.strip()

            if line:
                self.log_message.emit(line)

            if "[download] Destination:" in line:
                filename = line.split("Destination:", 1)[1].strip()
                self.video_title = Path(filename).stem

            if "[ExtractAudio]" in line:
                self.status_changed.emit("🔄 Konvertiere Audio...")

            if "[EmbedThumbnail]" in line:
                self.status_changed.emit("🖼️ Bette Coverbild ein...")

            if "[Metadata]" in line:
                self.status_changed.emit("📝 Schreibe Metadaten...")

            match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", line)

            if match:
                percent = int(float(match.group(1)))
                self.progress_changed.emit(percent)

        self.process.wait()
        self.finished_download.emit(self.process.returncode)

    def stop(self):
        if hasattr(self, "process") and self.process:
            self.process.terminate()