# Standardbibliothek
import re
import sys
import subprocess
import shutil
from pathlib import Path
from version import VERSION
from about import show_info_dialog
from changelog import show_changelog_dialog

PROJECT_DIR = Path(__file__).resolve().parent.parent
ICON_FILE = PROJECT_DIR / "icons" / "audioharvester.png"

# Drittanbieter
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtWidgets import (
    QGroupBox,
    QListWidget,
    QMessageBox,
    QFileDialog,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
    QProgressBar,
    QCheckBox,
    QDialog,
  )
# Eigene Module
from settings import load_settings, save_settings

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

        yt_dlp = Path.home() / ".local" / "bin" / "yt-dlp"

        if not yt_dlp.exists():
            yt_dlp = shutil.which("yt-dlp")

        if not yt_dlp:
            self.log_message.emit("❌ yt-dlp wurde nicht gefunden.")
            self.finished_download.emit(1)
            return

        cmd = [
            str(yt_dlp),
            "-x",
            "--newline",
            "-o",
            str(download_dir / "%(title)s.%(ext)s")
        ]

        if self.audio_format == "MP3":
            cmd += ["--audio-format", "mp3"]
            if self.quality != "Original":
                bitrate = self.quality.split()[0]
                cmd += ["--postprocessor-args", f"-b:a {bitrate}k"]
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


class AudioHarvester(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(
            QIcon(
                str(
                    Path(__file__).resolve().parent.parent
                    / "icons"
                    / "audioharvester.png"
                )
            )
        )
        self.download_cancelled = False

        settings = load_settings()

        self.setWindowTitle(f"AudioHarvester v{VERSION}")

        self.resize(650, 450)

        layout = QVBoxLayout()
        download_group = QGroupBox("Download")
        download_layout = QVBoxLayout()
        download_layout.setSpacing(8)

        download_group.setLayout(download_layout)

        layout.addWidget(download_group)
        self.settings = load_settings()

        options_group = QGroupBox("Optionen")
        options_layout = QVBoxLayout()
        options_layout.setSpacing(8)

        options_group.setLayout(options_layout)

        layout.addWidget(options_group)

        folder_group = QGroupBox("Zielordner")
        folder_layout = QVBoxLayout()
        folder_layout.setSpacing(8)


        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)

        actions_group = QGroupBox("Aktionen")
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)

        actions_group.setLayout(actions_layout)

        layout.addWidget(actions_group)

        download_layout.addWidget(QLabel("YouTube URL"))

        url_layout = QHBoxLayout()

        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)

        self.clear_url_button = QPushButton("✖")
        self.clear_url_button.clicked.connect(self.clear_url)
        url_layout.addWidget(self.clear_url_button)

        self.clear_url_button.setToolTip(
            "Leert das URL-Feld"
        )

        download_layout.addLayout(url_layout)

        download_layout.addWidget(QLabel("Format"))
        self.format_box = QComboBox()
        self.format_box.addItems(["MP3", "Opus", "M4A"])

        saved_format = self.settings.get("format", "MP3")
        index = self.format_box.findText(saved_format)

        if index >= 0:
            self.format_box.setCurrentIndex(index)

        download_layout.addWidget(self.format_box)

        download_layout.addWidget(QLabel("Qualität"))
        self.quality_box = QComboBox()
        self.quality_box.addItems([
            "128 kbps",
            "192 kbps",
            "320 kbps",
            "Original"])
        saved_quality = self.settings.get(
            "quality",
            "320 kbps")
        index = self.quality_box.findText(saved_quality)

        if index >= 0:
            self.quality_box.setCurrentIndex(index)

        download_layout.addWidget(self.quality_box)

        self.thumbnail_checkbox = QCheckBox(
        "Coverbild einbetten"
        )

        self.thumbnail_checkbox.setChecked(
        self.settings.get(
        "download_thumbnail",
            False
            )
        )

        options_layout.addWidget(self.thumbnail_checkbox)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        actions_layout.addWidget(self.progress)

        self.status_label = QLabel("Bereit")
        actions_layout.addWidget(self.status_label)

        self.output_dir = self.settings.get("output_dir",
         str(Path.home() / "Musik" / "AudioHarvester")
)
        self.output_label = QLabel(f"Zielordner: {self.output_dir}")
        folder_layout.addWidget(self.output_label)

        self.choose_folder_button = QPushButton("Zielordner auswählen")
        self.choose_folder_button.clicked.connect(self.choose_output_folder)
        folder_layout.addWidget(self.choose_folder_button)

        button_layout = QHBoxLayout()

        self.download_button = QPushButton("⬇ Download starten")
        self.download_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_button)

        self.download_button.setToolTip(
            "Startet den Download der eingegebenen URL"
        )

        self.cancel_button = QPushButton("⏸ Abbrechen")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)

        button_layout.addWidget(self.cancel_button)

        self.cancel_button.setToolTip(
            "Bricht den laufenden Download ab"
        )

        self.folder_button = QPushButton("📂 Ordner öffnen")
        self.folder_button.clicked.connect(self.open_download_folder)
        button_layout.addWidget(self.folder_button)

        self.folder_button.setToolTip(
            "Öffnet den aktuellen Zielordner"
        )

        self.info_button = QPushButton("ℹ Info")
        self.info_button.clicked.connect(
        lambda: show_info_dialog(self)
)
        button_layout.addWidget(self.info_button)

        self.info_button.setToolTip(
            "Zeigt Informationen über AudioHarvester"
        )

        self.changelog_button = QPushButton ("📋 Changelog")
        self.changelog_button.clicked.connect(
            lambda: show_changelog_dialog(self)
        )
        button_layout.addWidget(self.changelog_button)

        self.changelog_button.setToolTip(
            "Zeigt die Änderungen der aktuellen Versionen"
        )

        self.legal_button = QPushButton ("⚖ Rechtliches")
        self.legal_button.clicked.connect(self.show_legal)
        button_layout.addWidget(self.legal_button)

        actions_layout.addLayout(button_layout)

        self.legal_button.setToolTip(
            "Zeigt rechtliche Hinweise"
        )

        history_group = QGroupBox("Letzte Downloads")
        history_layout = QVBoxLayout()
        history_layout.setSpacing(8)
        
        history_group.setLayout(history_layout)

        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)

        self.history_list.itemDoubleClicked.connect(
            self.load_history_item
)
        for item in self.settings.get("history", []):
            self.history_list.addItem(item)

        self.clear_history_button = QPushButton("Historie löschen")
        self.clear_history_button.clicked.connect(self.clear_history)
        history_layout.addWidget(self.clear_history_button)

        self.clear_history_button.setToolTip(
            "Löscht die Download-Historie"
        )

        layout.addWidget(history_group)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def save_current_settings(self):
        self.settings["output_dir"] = self.output_dir
        self.settings["download_thumbnail"] = self.thumbnail_checkbox.isChecked()
        self.settings["format"] = self.format_box.currentText()
        self.settings["quality"] = self.quality_box.currentText()
        save_settings(self.settings)

    def start_download(self):
        self.log.clear()
        url = self.url_input.text().strip()

        self.download_cancelled = False

        self.save_current_settings()

        if not url:
            self.log.append("Bitte eine URL eingeben.")
            return
        
        playlist_mode = "video"
        is_playlist = "list=" in url or "playlist" in url

        if is_playlist:
            msg = QMessageBox(self)

            msg.setWindowTitle("Playlist erkannt")

            msg.setText(
                "Diese URL gehört zu einer Playlist.\n\n"
                "Möchtest du die gesamte Playlist herunterladen\n"
                "oder nur den aktuell ausgewählten Titel?"
            )

            playlist_button = msg.addButton(
                "Gesamte Playlist",
                QMessageBox.ButtonRole.AcceptRole
            )

            msg.addButton(
                "Nur diesen Titel",
                QMessageBox.ButtonRole.RejectRole
            )

            msg.exec()

            if msg.clickedButton() == playlist_button:
                playlist_mode = "playlist"
                self.log.append("Playlist-Modus: Ganze Playlist")
            else:
                playlist_mode = "video"
                self.log.append("Playlist-Modus: Nur dieses Audio")

        self.progress.setValue(0)
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        audio_format = self.format_box.currentText()
        quality = self.quality_box.currentText()

        self.log.append("Starte Download...")
        self.log.append(f"Format: {audio_format}")
        self.log.append(f"Qualität: {quality}")

        self.worker = DownloadWorker(
            url, 
            audio_format, 
            quality,
            self.output_dir,
            self.thumbnail_checkbox.isChecked(),
            playlist_mode
        )

        self.worker.log_message.connect(self.log.append)
        self.worker.progress_changed.connect(self.progress.setValue)
        self.worker.status_changed.connect(self.status_label.setText)
        self.worker.finished_download.connect(self.download_finished)

        self.status_label.setText("⬇️ Download läuft...")
        
        self.worker.start()

    def cancel_download(self):
        self.download_cancelled = True

        if hasattr(self, "worker"):
            self.worker.stop()

        self.cancel_button.setEnabled(False)
        self.download_button.setEnabled(True)

        self.status_label.setText("⏹️ Download abgebrochen")
        self.log.append("Download wurde abgebrochen.")

    def download_finished(self, code):
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

        if self.download_cancelled:
            self.status_label.setText("⏹️ Download abgebrochen")

            QTimer.singleShot(
                5000,
                lambda: self.status_label.setText("Bereit")
)
            return

        if code == 0:
            self.progress.setValue(100)

            QTimer.singleShot(
                1000,
                lambda: self.status_label.setText("✅ Download erfolgreich")
            )

            QTimer.singleShot(
                6000,
                lambda: self.status_label.setText("Bereit")
            )

            self.log.append("Download erfolgreich.")

            self.url_input.clear()

            title = getattr(self.worker, "video_title", self.url_input.text().strip())

            self.history_list.insertItem(0, title)

            history = self.settings.get("history", [])
            history.insert(0, title)

            self.settings["history"] = history[:20]
            save_settings(self.settings)

        else:
            self.status_label.setText("❌ Fehler beim Download")
            self.log.append("Fehler beim Download.")

    def clear_history(self):
        msg = QMessageBox(self)

        msg.setWindowTitle("Historie löschen")
        msg.setText(
            "Möchtest du die Download-Historie wirklich löschen?"
        )

        ja_button = msg.addButton(
            "Ja",
            QMessageBox.ButtonRole.AcceptRole
        )

        nein_button = msg.addButton(
            "Nein",
            QMessageBox.ButtonRole.RejectRole
        )

        msg.exec()

        if msg.clickedButton() != ja_button:
            return

        self.history_list.clear()

        self.settings["history"] = []

        save_settings(self.settings)

        self.status_label.setText(
        "🗑️ Historie gelöscht"
    )
        QTimer.singleShot(
            6000,
            lambda: self.status_label.setText("Bereit")
        )

    def clear_url(self):
        self.url_input.clear()
        self.status_label.setText("URL-Feld geleert")

    def load_history_item(self, item):
        self.url_input.setText(item.text())

        self.status_label.setText(
            "Eintrag aus Historie übernommen"
        )

    def show_legal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Rechtlicher Hinweis")
        dialog.resize(600, 450)

        layout = QVBoxLayout()

        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        title_label = QLabel("<h2>Rechtlicher Hinweis</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        text_label = QLabel(
            "AudioHarvester ist ein Werkzeug zum Herunterladen von Audioinhalten.<br><br>"
            "<b>Bitte beachten Sie:</b><br><br>"
            "• Privatkopien können für den persönlichen Gebrauch zulässig sein.<br><br>"
            "• Downloads sollten nur von rechtmäßigen Quellen erfolgen.<br><br>"
            "• Das Umgehen technischer Schutzmaßnahmen ist nicht erlaubt.<br><br>"
            "• YouTube-Nutzungsbedingungen können Downloads untersagen.<br><br>"
            "• Inhalte dürfen nicht ohne Erlaubnis verbreitet oder kommerziell genutzt werden.<br><br>"
            "<b>Jeder Nutzer ist selbst verantwortlich, geltende Gesetze und Nutzungsbedingungen einzuhalten.</b>"
        )

        text_label.setWordWrap(True)
        text_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(text_label)

        layout.addSpacing(20)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def open_download_folder(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        subprocess.Popen(["xdg-open", self.output_dir])

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
             "Zielordner auswählen",
            self.output_dir
    )
        if folder:
            self.output_dir = folder
            self.output_label.setText(
                f"Zielordner: {self.output_dir}"
            )
            self.settings["output_dir"] = self.output_dir
            save_settings(self.settings)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioHarvester()
    window.show()
    sys.exit(app.exec())
