from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PyQt6.QtGui import (
    QPixmap,
    QDesktopServices
)

from PyQt6.QtCore import (
    Qt,
    QUrl
)

from version import VERSION
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
ICON_FILE = PROJECT_DIR / "icons" / "audioharvester.png"


def show_info_dialog(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Über AudioHarvester")
    dialog.resize(450, 550)

    layout = QVBoxLayout()

    icon_label = QLabel()
    pixmap = QPixmap(str(ICON_FILE))

    if not pixmap.isNull():
        icon_label.setPixmap(
            pixmap.scaledToWidth(96)
        )
        icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(icon_label)

    text_label = QLabel(
        f"Version {VERSION}<br><br>"

        "Audio-Downloader für Linux auf Basis von yt-dlp und ffmpeg.<br>"
        "Erstellt mit Python und PyQt6.<br><br>"

        "<b>Funktionen:</b><br>"
        "Unterstützung für MP3, Opus und M4A<br>"
        "Auswahl der Audioqualität<br>"
        "Coverbilder einbetten<br>"
        "Metadaten-Unterstützung<br>"
        "Playlist-Downloads mit Einzeltrack-Modus<br>"
        "Download abbrechen<br>"
        "Download-Historie<br>"
        "Historie verwalten<br>"
        "Frei wählbarer Zielordner<br>"
        "Einstellungen speichern<br>"
        "XFCE-Menüintegration<br>"
        "Installierbares DEB-Paket<br>"
        "Automatische yt-dlp-Erkennung<br><br>"
        "Integrierter Changelog-Viewer<br>"
        "Tooltips und GUI-Verbesserungen<br><br>"

        "<b>Autor:</b> Markus <br><br>"

        '🌐 <a href="https://wildcardcharacter.github.io">'
        "Website"
        "</a><br>"

        '📧 <a href="mailto:wildcardcharacter@icloud.com">'
        "E-Mail"
        "</a><br><br>"

        "─────────────────<br><br>"

        "Wenn dir AudioHarvester gefällt und du die Entwicklung "
        "unterstützen möchtest:"
    )

    text_label.setOpenExternalLinks(True)
    text_label.setTextFormat(Qt.TextFormat.RichText)
    text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    text_label.setWordWrap(True)

    layout.addWidget(text_label)

    support_button = QPushButton(
        "☕ AudioHarvester unterstützen"
    )

    support_button.clicked.connect(
        lambda: QDesktopServices.openUrl(
            QUrl(
                "https://buymeacoffee.com/wildcardcharacter"
            )
        )
    )

    layout.addWidget(support_button)

    close_button = QPushButton("Schließen")
    close_button.clicked.connect(dialog.close)

    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()