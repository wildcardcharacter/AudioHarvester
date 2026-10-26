# Standardbibliothek
import sys
import subprocess
from pathlib import Path
from version import VERSION
from about import show_info_dialog
from changelog import show_changelog_dialog
from download import DownloadWorker
from legal import show_legal_dialog

PROJECT_DIR = Path(__file__).resolve().parent.parent
ICON_FILE = PROJECT_DIR / "assets" / "icons" / "audioharvester.png"

# Drittanbieter
from PyQt6.QtGui import QIcon, QActionGroup, QDesktopServices
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer, QUrl
from PyQt6.QtWidgets import (
    QGroupBox,
    QListWidget,
    QListWidgetItem,
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
    QTextBrowser,
    QScrollArea,
    QToolButton,
    QMenu,
  )
# Eigene Module
from settings import load_settings, save_settings
from updater import (
    PackageInstallWorker, ReleaseCheckWorker, installed_deb_version, version_key,
)

QUEUE_URL_ROLE = int(Qt.ItemDataRole.UserRole)
QUEUE_STATUS_ROLE = QUEUE_URL_ROLE + 1


class AudioHarvester(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(
            QIcon(
                str(
                    Path(__file__).resolve().parent.parent
                    / "assets"
                    / "icons"
                    / "audioharvester.png"
                )
            )
        )
        self.download_cancelled = False

        settings = load_settings()

        self.setWindowTitle(f"AudioHarvester v{VERSION}")

        # Fenstergröße an den Bildschirm anpassen; bei wenig Platz bleibt der
        # Inhalt über Scrollleisten erreichbar.
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry() if screen else None
        if available:
            max_width = max(1, available.width() - 40)
            max_height = max(1, available.height() - 80)
        else:
            max_width, max_height = 1200, 900
        self.setMinimumSize(min(760, max_width), min(500, max_height))
        width = min(settings.get("window_width", 900), max_width)
        height = min(settings.get("window_height", 600), max_height)
        self.resize(max(self.minimumWidth(), width), max(self.minimumHeight(), height))

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 10, 12, 12)
        layout.setSpacing(10)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.update_button = QPushButton("⬆ Updates prüfen")
        self.update_button.clicked.connect(self.check_for_updates)
        top_bar.addWidget(self.update_button)
        self.settings_button = QToolButton()
        self.settings_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        top_bar.addWidget(self.settings_button)
        self.more_button = QToolButton()
        self.more_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.more_menu = QMenu(self.more_button)
        self.changelog_action = self.more_menu.addAction("Changelog")
        self.changelog_action.triggered.connect(lambda: show_changelog_dialog(self, self.language))
        self.legal_action = self.more_menu.addAction("Rechtliches")
        self.legal_action.triggered.connect(lambda: show_legal_dialog(self, self.language))
        self.info_action = self.more_menu.addAction("Info")
        self.info_action.triggered.connect(lambda: show_info_dialog(self, self.language))
        self.more_button.setMenu(self.more_menu)
        top_bar.addWidget(self.more_button)
        layout.addLayout(top_bar)

        download_group = QGroupBox("Download")
        download_layout = QVBoxLayout()
        download_layout.setContentsMargins(10, 10, 10, 10)
        download_layout.setSpacing(6)

        download_group.setLayout(download_layout)

        self.settings = load_settings()
        self.language = self.settings.get("language", "Deutsch")
        self.selected_format = self.settings.get("format", "MP3")
        self.selected_quality = self.settings.get("quality", "320 kbps")
        self.embed_cover = self.settings.get("download_thumbnail", False)
        self.current_queue_item = None
        self.create_settings_menu()

        folder_group = QGroupBox("Zielordner")
        folder_layout = QVBoxLayout()
        folder_layout.setContentsMargins(10, 10, 10, 10)
        folder_layout.setSpacing(6)


        folder_group.setLayout(folder_layout)

        actions_group = QGroupBox("Aktionen")
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(10, 10, 10, 10)
        actions_layout.setSpacing(6)

        actions_group.setLayout(actions_layout)


        download_layout.addWidget(QLabel("YouTube URL(s) – mehrere Links zeilenweise"))

        url_layout = QHBoxLayout()

        self.url_input = QTextEdit()
        self.url_input.setMinimumHeight(48)
        self.url_input.setMaximumHeight(58)
        url_layout.addWidget(self.url_input)

        self.clear_url_button = QPushButton("✖")
        self.clear_url_button.clicked.connect(self.clear_url)
        url_layout.addWidget(self.clear_url_button)

        self.clear_url_button.setToolTip(
            "Leert das URL-Feld"
        )

        download_layout.addLayout(url_layout)

        queue_buttons = QHBoxLayout()
        self.add_queue_button = QPushButton("Zur Warteschlange hinzufügen")
        self.add_queue_button.clicked.connect(self.add_to_queue)
        queue_buttons.addWidget(self.add_queue_button)
        self.start_queue_button = QPushButton("Warteschlange starten")
        self.start_queue_button.clicked.connect(self.start_download)
        queue_buttons.addWidget(self.start_queue_button)
        download_layout.addLayout(queue_buttons)
        self.queue_list = QListWidget()
        download_layout.addWidget(self.queue_list)
        queue_controls = QHBoxLayout()
        self.remove_queue_button = QPushButton("Auswahl entfernen")
        self.remove_queue_button.clicked.connect(self.remove_queue_item)
        queue_controls.addWidget(self.remove_queue_button)
        self.clear_queue_button = QPushButton("Warteschlange leeren")
        self.clear_queue_button.clicked.connect(self.clear_queue)
        queue_controls.addWidget(self.clear_queue_button)
        self.retry_failed_button = QPushButton("Fehlgeschlagene erneut versuchen")
        self.retry_failed_button.clicked.connect(self.retry_failed_downloads)
        self.retry_failed_button.setEnabled(False)
        queue_controls.addWidget(self.retry_failed_button)
        download_layout.addLayout(queue_controls)
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Dateiname"))
        self.filename_template = QLineEdit(self.settings.get("filename_template", "%(title)s"))
        self.filename_template.setToolTip("yt-dlp Vorlage, z. B. %(artist)s - %(title)s")
        template_layout.addWidget(self.filename_template)
        download_layout.addLayout(template_layout)

        self.current_download_label = QLabel("Kein Download aktiv")
        self.current_download_label.setWordWrap(True)
        actions_layout.addWidget(self.current_download_label)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        actions_layout.addWidget(self.progress)

        self.status_label = QLabel("Bereit")
        actions_layout.addWidget(self.status_label)

        self.output_dir = self.settings.get("output_dir",
         str(Path.home() / "Musik" / "AudioHarvester")
)
        self.output_label = QLabel(f"Zielordner: {self.output_dir}")
        self.output_label.setWordWrap(True)
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
        folder_layout.addWidget(self.folder_button)

        self.folder_button.setToolTip(
            "Öffnet den aktuellen Zielordner"
        )

        actions_layout.addLayout(button_layout)
        history_group = QGroupBox("Letzte Downloads")
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(10, 10, 10, 10)
        history_layout.setSpacing(6)
        
        history_group.setLayout(history_layout)

        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(72)
        self.history_list.setMaximumHeight(126)
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

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log_toggle = QPushButton()
        self.log_toggle.setCheckable(True)
        self.log_toggle.setChecked(False)
        self.log_toggle.setMinimumHeight(32)
        self.log_toggle.toggled.connect(self.toggle_log)
        workspace = QHBoxLayout()
        workspace.setSpacing(10)
        left_column = QVBoxLayout()
        left_column.setSpacing(10)
        left_column.addWidget(download_group, 1)
        right_column = QVBoxLayout()
        right_column.setSpacing(10)
        right_column.addWidget(actions_group)
        right_column.addWidget(folder_group)
        right_column.addWidget(history_group, 1)
        workspace.addLayout(left_column, 3)
        workspace.addLayout(right_column, 2)
        layout.addLayout(workspace, 1)
        layout.addWidget(self.log_toggle)
        self.log.hide()
        layout.addWidget(self.log)

        content = QWidget()
        content.setLayout(layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content)
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(scroll_area)
        self.apply_language()

    def tr(self, german, english):
        return english if self.language == "English" else german

    def queue_status_label(self, status):
        labels = {
            "waiting": ("⏳ Wartet", "⏳ Waiting"),
            "running": ("⬇ Läuft", "⬇ In progress"),
            "success": ("✅ Erfolgreich", "✅ Complete"),
            "failed": ("❌ Fehlgeschlagen", "❌ Failed"),
        }
        german, english = labels[status]
        return self.tr(german, english)

    def set_queue_item_status(self, item, status):
        item.setData(QUEUE_STATUS_ROLE, status)
        url = item.data(QUEUE_URL_ROLE)
        item.setText(f"{self.queue_status_label(status)} — {url}")
        self.retry_failed_button.setEnabled(self.has_failed_downloads())

    def has_failed_downloads(self):
        return any(
            self.queue_list.item(index).data(QUEUE_STATUS_ROLE) == "failed"
            for index in range(self.queue_list.count())
        )

    def next_waiting_item(self):
        for index in range(self.queue_list.count()):
            item = self.queue_list.item(index)
            if item.data(QUEUE_STATUS_ROLE) == "waiting":
                return item
        return None

    def refresh_queue_labels(self):
        for index in range(self.queue_list.count()):
            item = self.queue_list.item(index)
            status = item.data(QUEUE_STATUS_ROLE)
            if status:
                self.set_queue_item_status(item, status)

    def toggle_log(self, expanded):
        self.log.setVisible(expanded)
        self.log_toggle.setText(
            self.tr("Protokoll ausblenden ▴", "Hide log ▴") if expanded
            else self.tr("Protokoll anzeigen ▾", "Show log ▾")
        )

    def change_language(self, language):
        self.language = language
        self.settings["language"] = language
        save_settings(self.settings)
        self.apply_language()

    def create_settings_menu(self):
        self.settings_menu = QMenu(self.settings_button)
        self.settings_button.setMenu(self.settings_menu)

        self.language_menu = self.settings_menu.addMenu("Sprache")
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)
        self.language_actions = {}
        for language in ("Deutsch", "English"):
            action = self.language_menu.addAction(language)
            action.setCheckable(True)
            action.setChecked(language == self.language)
            self.language_group.addAction(action)
            action.triggered.connect(lambda checked, value=language: self.change_language(value) if checked else None)
            self.language_actions[language] = action

        self.format_menu = self.settings_menu.addMenu("Format")
        self.format_group = QActionGroup(self)
        self.format_group.setExclusive(True)
        self.format_actions = {}
        for audio_format in ("MP3", "Opus", "M4A"):
            action = self.format_menu.addAction(audio_format)
            action.setCheckable(True)
            action.setChecked(audio_format == self.selected_format)
            self.format_group.addAction(action)
            action.triggered.connect(lambda checked, value=audio_format: self.set_audio_format(value) if checked else None)
            self.format_actions[audio_format] = action

        self.quality_menu = self.settings_menu.addMenu("Qualität")
        self.quality_group = QActionGroup(self)
        self.quality_group.setExclusive(True)
        self.quality_actions = {}
        for quality in ("128 kbps", "192 kbps", "320 kbps", "Original"):
            action = self.quality_menu.addAction(quality)
            action.setCheckable(True)
            action.setChecked(quality == self.selected_quality)
            self.quality_group.addAction(action)
            action.triggered.connect(lambda checked, value=quality: self.set_audio_quality(value) if checked else None)
            self.quality_actions[quality] = action

        self.cover_action = self.settings_menu.addAction("Coverbild einbetten")
        self.cover_action.setCheckable(True)
        self.cover_action.setChecked(self.embed_cover)
        self.cover_action.triggered.connect(self.set_cover_embedding)
        self.update_settings_menu_language()
        self.update_button.setText(self.tr("⬆ Updates prüfen", "⬆ Check for updates"))

    def set_audio_format(self, audio_format):
        self.selected_format = audio_format
        self.settings["format"] = audio_format
        save_settings(self.settings)

    def set_audio_quality(self, quality):
        self.selected_quality = quality
        self.settings["quality"] = quality
        save_settings(self.settings)

    def set_cover_embedding(self, enabled):
        self.embed_cover = enabled
        self.settings["download_thumbnail"] = enabled
        save_settings(self.settings)

    def update_settings_menu_language(self):
        self.settings_button.setText(self.tr("⚙ Einstellungen ▾", "⚙ Settings ▾"))
        self.language_menu.setTitle(self.tr("Sprache", "Language"))
        self.format_menu.setTitle(self.tr("Format", "Format"))
        self.quality_menu.setTitle(self.tr("Qualität", "Quality"))
        self.cover_action.setText(self.tr("Coverbild einbetten", "Embed cover art"))

    def check_for_updates(self):
        self.update_button.setEnabled(False)
        self.update_button.setText(self.tr("Prüfe Updates …", "Checking for updates …"))
        self.release_worker = ReleaseCheckWorker()
        self.release_worker.succeeded.connect(self.update_check_succeeded)
        self.release_worker.failed.connect(self.update_check_failed)
        self.release_worker.finished.connect(self.reset_update_button)
        self.release_worker.start()

    def reset_update_button(self):
        self.update_button.setEnabled(True)
        self.update_button.setText(self.tr("⬆ Updates prüfen", "⬆ Check for updates"))

    def update_check_failed(self, error):
        QMessageBox.warning(
            self, self.tr("Updateprüfung fehlgeschlagen", "Update check failed"), error
        )

    def update_check_succeeded(self, release):
        current_version = installed_deb_version() or VERSION
        try:
            has_update = version_key(release["version"]) > version_key(current_version)
        except ValueError as error:
            self.update_check_failed(str(error))
            return

        if not has_update:
            QMessageBox.information(
                self, self.tr("AudioHarvester ist aktuell", "AudioHarvester is up to date"),
                self.tr(
                    f"Du verwendest bereits AudioHarvester {current_version}.",
                    f"You are already using AudioHarvester {current_version}.",
                ),
            )
            return

        package_installed = installed_deb_version() is not None
        action = self.show_update_dialog(
            release, current_version, package_installed and bool(release["url"])
        )
        if action == "install":
            self.install_update(release)
        elif action == "open":
            QDesktopServices.openUrl(QUrl(release["release_url"]))

    def show_update_dialog(self, release, current_version, can_install):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Update verfügbar", "Update available"))
        dialog.setMinimumSize(560, 430)
        dialog.resize(640, 500)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(12)

        heading = QLabel(self.tr("Eine neue Version ist verfügbar", "A new version is available"))
        heading.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(heading)

        versions = QLabel(
            f"<b>{self.tr('Installiert', 'Installed')}</b>  {current_version}"
            f"<br><b>{self.tr('Verfügbar', 'Available')}</b>  {release['version']}"
        )
        versions.setTextFormat(Qt.TextFormat.RichText)
        versions.setStyleSheet("padding: 10px 12px; background: palette(alternate-base); border-radius: 6px;")
        layout.addWidget(versions)

        notes_heading = QLabel(self.tr("Versionshinweise", "Release notes"))
        notes_heading.setStyleSheet("font-weight: 600; margin-top: 4px;")
        layout.addWidget(notes_heading)

        notes = QTextBrowser()
        notes.setOpenExternalLinks(True)
        notes.setPlaceholderText(self.tr("Keine Versionshinweise verfügbar.", "No release notes available."))
        notes.setMarkdown(release["notes"] or self.tr("Keine Versionshinweise verfügbar.", "No release notes available."))
        notes.setStyleSheet("border: 1px solid palette(mid); border-radius: 6px; padding: 8px;")
        layout.addWidget(notes, 1)

        buttons = QHBoxLayout()
        buttons.addStretch()
        later_button = QPushButton(self.tr("Später", "Later"))
        later_button.clicked.connect(dialog.reject)
        buttons.addWidget(later_button)
        action_text = self.tr("Update installieren", "Install update") if can_install else self.tr("Release-Seite öffnen", "Open release page")
        action_button = QPushButton(action_text)
        action_button.setDefault(True)
        action_button.clicked.connect(dialog.accept)
        buttons.addWidget(action_button)
        layout.addLayout(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return "install" if can_install else "open"

    def install_update(self, release):
        self.update_button.setEnabled(False)
        self.update_install_worker = PackageInstallWorker(release)
        self.update_install_worker.progress.connect(self.status_label.setText)
        self.update_install_worker.failed.connect(self.update_install_failed)
        self.update_install_worker.succeeded.connect(self.update_install_succeeded)
        self.update_install_worker.finished.connect(self.reset_update_button)
        self.update_install_worker.start()

    def update_install_failed(self, error):
        QMessageBox.critical(
            self, self.tr("Update fehlgeschlagen", "Update failed"), error
        )

    def update_install_succeeded(self):
        answer = QMessageBox.question(
            self, self.tr("Update installiert", "Update installed"),
            self.tr(
                "AudioHarvester wurde aktualisiert. Jetzt neu starten?",
                "AudioHarvester was updated. Restart now?",
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            executable = Path("/usr/bin/audioharvester")
            if executable.exists():
                subprocess.Popen([str(executable)], start_new_session=True)
                self.close()
            else:
                QMessageBox.information(
                    self, self.tr("Neustart erforderlich", "Restart required"),
                    self.tr("Bitte starte AudioHarvester über das Anwendungsmenü neu.", "Please restart AudioHarvester from the applications menu."),
                )

    def apply_language(self):
        translations = {
            "Optionen": "Options", "Zielordner": "Output folder", "Aktionen": "Actions",
            "YouTube URL(s) – mehrere Links zeilenweise": "YouTube URL(s) – enter one link per line",
            "Leert das URL-Feld": "Clear the URL field", "Zur Warteschlange hinzufügen": "Add to queue",
            "Warteschlange starten": "Start queue", "Auswahl entfernen": "Remove selected",
            "Warteschlange leeren": "Clear queue", "Dateiname": "Filename template",
            "Fehlgeschlagene erneut versuchen": "Retry failed downloads",
            "yt-dlp Vorlage, z. B. %(artist)s - %(title)s": "yt-dlp template, e.g. %(artist)s - %(title)s",
            "Format": "Format", "Qualität": "Quality", "Coverbild einbetten": "Embed cover art", "Bereit": "Ready",
            "Zielordner auswählen": "Choose output folder", "⬇ Download starten": "⬇ Start download",
            "⏸ Abbrechen": "⏸ Cancel", "Bricht den laufenden Download ab": "Cancel the current download",
            "📂 Ordner öffnen": "📂 Open folder", "ℹ Info": "ℹ About", "⚖ Rechtliches": "⚖ Legal",
            "Letzte Downloads": "Recent downloads", "Historie löschen": "Clear history",
            "Löscht die Download-Historie": "Clear download history",
            "Startet den Download der eingegebenen URL": "Start downloading the queued URLs",
            "Öffnet den aktuellen Zielordner": "Open the current output folder",
            "Zeigt Informationen über AudioHarvester": "About AudioHarvester",
            "Zeigt die Änderungen der aktuellen Versionen": "Show version history",
            "Zeigt rechtliche Hinweise": "Show legal information",
            "⚙ Einstellungen": "⚙ Settings",
        }
        for widget in self.findChildren(QWidget):
            # QGroupBox exposes its caption through title(), not text(), so it
            # needs its own translation pass.
            if isinstance(widget, QGroupBox):
                title = widget.title()
                if title in translations:
                    widget.setTitle(
                        translations[title] if self.language == "English" else title
                    )
                elif title in translations.values():
                    widget.setTitle(
                        next(de for de, en in translations.items() if en == title)
                        if self.language == "Deutsch" else title
                    )
            if hasattr(widget, "text") and callable(widget.text):
                current = widget.text()
                if current.startswith("Zielordner: ") or current.startswith("Output folder: "):
                    widget.setText(self.tr("Zielordner: ", "Output folder: ") + self.output_dir)
                elif current in translations:
                    widget.setText(translations[current] if self.language == "English" else current)
                elif current in translations.values():
                    widget.setText(next(de for de, en in translations.items() if en == current) if self.language == "Deutsch" else current)
            if hasattr(widget, "toolTip") and callable(widget.toolTip):
                tip = widget.toolTip()
                if tip in translations:
                    widget.setToolTip(translations[tip] if self.language == "English" else tip)
                elif tip in translations.values():
                    widget.setToolTip(next(de for de, en in translations.items() if en == tip) if self.language == "Deutsch" else tip)
        self.url_input.setPlaceholderText(self.tr("Eine URL pro Zeile", "One URL per line"))
        self.more_button.setText(self.tr("Mehr ▾", "More ▾"))
        self.changelog_action.setText(self.tr("Changelog", "Changelog"))
        self.legal_action.setText(self.tr("Rechtliches", "Legal information"))
        self.info_action.setText(self.tr("Info", "About"))
        self.update_settings_menu_language()
        self.update_button.setText(self.tr("⬆ Updates prüfen", "⬆ Check for updates"))
        if self.current_queue_item is None:
            self.current_download_label.setText(self.tr("Kein Download aktiv", "No download active"))
        else:
            current_url = self.current_queue_item.data(QUEUE_URL_ROLE)
            self.current_download_label.setText(self.tr(f"Aktueller Download: {current_url}", f"Current download: {current_url}"))
        self.refresh_queue_labels()
        self.toggle_log(self.log_toggle.isChecked())

    def save_current_settings(self):
        self.settings["output_dir"] = self.output_dir
        self.settings["download_thumbnail"] = self.embed_cover
        self.settings["format"] = self.selected_format
        self.settings["quality"] = self.selected_quality
        self.settings["filename_template"] = self.filename_template.text().strip() or "%(title)s"
        save_settings(self.settings)

    def closeEvent(self, event):
        self.settings["window_width"] = self.width()
        self.settings["window_height"] = self.height()
        save_settings(self.settings)
        super().closeEvent(event)

    def add_to_queue(self):
        urls = [line.strip() for line in self.url_input.toPlainText().splitlines() if line.strip()]
        if not urls:
            self.log.append(self.tr("Bitte mindestens eine URL eingeben.", "Please enter at least one URL."))
            return
        known = {
            self.queue_list.item(i).data(QUEUE_URL_ROLE)
            for i in range(self.queue_list.count())
        }
        added = 0
        for url in urls:
            if url not in known:
                item = QListWidgetItem()
                item.setData(QUEUE_URL_ROLE, url)
                self.queue_list.addItem(item)
                self.set_queue_item_status(item, "waiting")
                known.add(url)
                added += 1
        self.url_input.clear()
        self.status_label.setText(self.tr(f"{added} URL(s) zur Warteschlange hinzugefügt", f"Added {added} URL(s) to the queue"))

    def remove_queue_item(self):
        row = self.queue_list.currentRow()
        if row >= 0:
            item = self.queue_list.item(row)
            is_active = (
                self.current_queue_item is not None
                and item.data(QUEUE_URL_ROLE) == self.current_queue_item.data(QUEUE_URL_ROLE)
            )
            if not is_active:
                self.queue_list.takeItem(row)
                self.retry_failed_button.setEnabled(self.has_failed_downloads())

    def clear_queue(self):
        if not (hasattr(self, "worker") and self.worker.isRunning()):
            self.queue_list.clear()
            self.retry_failed_button.setEnabled(False)

    def retry_failed_downloads(self):
        retried = 0
        for index in range(self.queue_list.count()):
            item = self.queue_list.item(index)
            if item.data(QUEUE_STATUS_ROLE) == "failed":
                self.set_queue_item_status(item, "waiting")
                retried += 1
        if retried:
            self.log.append(self.tr(
                f"{retried} fehlgeschlagene Downloads erneut eingereiht.",
                f"Requeued {retried} failed download(s)."
            ))
            if not (hasattr(self, "worker") and self.worker.isRunning()):
                self.start_download()

    def start_download(self):
        if self.url_input.toPlainText().strip():
            self.add_to_queue()
        queue_item = self.next_waiting_item()
        if queue_item is None:
            self.log.append(self.tr("Keine wartenden Downloads in der Warteschlange.", "There are no waiting downloads in the queue."))
            return
        url = queue_item.data(QUEUE_URL_ROLE)

        # Fehler von yt-dlp direkt sichtbar machen, ohne dass der Nutzer erst
        # nach einem versteckten Protokoll-Schalter suchen muss.
        self.log_toggle.setChecked(True)

        self.download_cancelled = False

        self.save_current_settings()

        playlist_mode = "video"
        is_playlist = "list=" in url or "playlist" in url

        if is_playlist:
            msg = QMessageBox(self)

            msg.setWindowTitle(self.tr("Playlist erkannt", "Playlist detected"))

            msg.setText(
                self.tr("Diese URL gehört zu einer Playlist.\n\n", "This URL belongs to a playlist.\n\n") +
                self.tr("Möchtest du die gesamte Playlist herunterladen\noder nur den aktuell ausgewählten Titel?", "Would you like to download the entire playlist\nor only the selected track?")
            )

            playlist_button = msg.addButton(
                self.tr("Gesamte Playlist", "Entire playlist"),
                QMessageBox.ButtonRole.AcceptRole
            )

            msg.addButton(
                self.tr("Nur diesen Titel", "This track only"),
                QMessageBox.ButtonRole.RejectRole
            )

            msg.exec()

            if msg.clickedButton() == playlist_button:
                playlist_mode = "playlist"
                self.log.append(self.tr("Playlist-Modus: Ganze Playlist", "Playlist mode: entire playlist"))
            else:
                playlist_mode = "video"
                self.log.append(self.tr("Playlist-Modus: Nur dieses Audio", "Playlist mode: this track only"))

        self.progress.setValue(0)
        self.current_queue_item = queue_item
        self.set_queue_item_status(queue_item, "running")
        self.current_download_label.setText(self.tr(f"Aktueller Download: {url}", f"Current download: {url}"))
        queue_item.setToolTip(url)
        self.download_button.setEnabled(False)
        self.start_queue_button.setEnabled(False)
        self.add_queue_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        audio_format = self.selected_format
        quality = self.selected_quality

        self.log.append(self.tr("Starte Download...", "Starting download..."))
        self.log.append(f"{self.tr('Format', 'Format')}: {audio_format}")
        self.log.append(f"{self.tr('Qualität', 'Quality')}: {quality}")

        self.worker = DownloadWorker(
            url, 
            audio_format, 
            quality,
            self.output_dir,
            self.embed_cover,
            playlist_mode,
            self.filename_template.text().strip() or "%(title)s",
            self.language
        )

        self.worker.log_message.connect(self.log.append)
        self.worker.progress_changed.connect(self.progress.setValue)
        self.worker.status_changed.connect(self.status_label.setText)
        self.worker.finished_download.connect(self.download_finished)

        self.status_label.setText(self.tr("⬇️ Download läuft...", "⬇️ Download in progress..."))
        
        self.worker.start()

    def cancel_download(self):
        self.download_cancelled = True

        if hasattr(self, "worker"):
            self.worker.stop()

        self.cancel_button.setEnabled(False)

        self.status_label.setText(self.tr("⏹️ Download abgebrochen", "⏹️ Download cancelled"))
        self.log.append(self.tr("Download wurde abgebrochen.", "Download was cancelled."))

    def download_finished(self, code):
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.start_queue_button.setEnabled(True)
        self.add_queue_button.setEnabled(True)

        item = self.current_queue_item
        self.current_queue_item = None

        if self.download_cancelled:
            if item is not None:
                self.set_queue_item_status(item, "waiting")
            self.current_download_label.setText(self.tr("Download abgebrochen", "Download cancelled"))
            self.status_label.setText(self.tr("⏹️ Download abgebrochen", "⏹️ Download cancelled"))

            QTimer.singleShot(
                5000,
                lambda: self.status_label.setText(self.tr("Bereit", "Ready"))
)
            return

        if code == 0:
            self.progress.setValue(100)
            if item is not None:
                self.set_queue_item_status(item, "success")
            self.current_download_label.setText(self.tr("Download abgeschlossen", "Download complete"))

            QTimer.singleShot(
                1000,
                lambda: self.status_label.setText(self.tr("✅ Download erfolgreich", "✅ Download complete"))
            )

            QTimer.singleShot(
                6000,
                lambda: self.status_label.setText(self.tr("Bereit", "Ready"))
            )

            self.log.append(self.tr("Download erfolgreich.", "Download completed successfully."))

            title = getattr(self.worker, "video_title", "Download")

            self.history_list.insertItem(0, title)

            history = self.settings.get("history", [])
            history.insert(0, title)

            self.settings["history"] = history[:20]
            save_settings(self.settings)
            if self.next_waiting_item() is not None:
                QTimer.singleShot(250, self.start_download)

        else:
            if item is not None:
                self.set_queue_item_status(item, "failed")
            self.current_download_label.setText(self.tr("Download fehlgeschlagen", "Download failed"))
            self.status_label.setText(self.tr("❌ Fehler beim Download", "❌ Download failed"))
            self.log.append(self.tr(
                "Download fehlgeschlagen. Du kannst ihn über 'Fehlgeschlagene erneut versuchen' erneut starten.",
                "Download failed. Use 'Retry failed downloads' to try it again."
            ))
            self.log_toggle.setChecked(True)
            if self.next_waiting_item() is not None:
                QTimer.singleShot(250, self.start_download)

    def clear_history(self):
        msg = QMessageBox(self)

        msg.setWindowTitle(self.tr("Historie löschen", "Clear history"))
        msg.setText(self.tr("Möchtest du die Download-Historie wirklich löschen?", "Do you really want to clear the download history?"))

        ja_button = msg.addButton(
            self.tr("Ja", "Yes"),
            QMessageBox.ButtonRole.AcceptRole
        )

        nein_button = msg.addButton(
            self.tr("Nein", "No"),
            QMessageBox.ButtonRole.RejectRole
        )

        msg.exec()

        if msg.clickedButton() != ja_button:
            return

        self.history_list.clear()

        self.settings["history"] = []

        save_settings(self.settings)

        self.status_label.setText(self.tr("🗑️ Historie gelöscht", "🗑️ History cleared"))
        QTimer.singleShot(
            6000,
            lambda: self.status_label.setText(self.tr("Bereit", "Ready"))
        )

    def clear_url(self):
        self.url_input.clear()
        self.status_label.setText(self.tr("URL-Feld geleert", "URL field cleared"))

    def load_history_item(self, item):
        self.url_input.setPlainText(item.text())

        self.status_label.setText(
            self.tr("Eintrag aus Historie übernommen", "History item loaded")
        )

    def open_download_folder(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        subprocess.Popen(["xdg-open", self.output_dir])

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
             self.tr("Zielordner auswählen", "Choose output folder"),
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
