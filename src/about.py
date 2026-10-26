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


MODULE_DIR = Path(__file__).resolve().parent
ICON_FILE = next(
    (path for path in (
        MODULE_DIR.parent / "assets" / "icons" / "audioharvester.png",
        MODULE_DIR / "assets" / "icons" / "audioharvester.png",
        MODULE_DIR / "icons" / "audioharvester.png",
    ) if path.exists()),
    MODULE_DIR / "icons" / "audioharvester.png",
)


def show_info_dialog(parent=None, language="Deutsch"):
    english = language == "English"
    dialog = QDialog(parent)
    dialog.setWindowTitle("About AudioHarvester" if english else "Über AudioHarvester")
    dialog.resize(480, 620)

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

    info_text = (
        "A Linux audio downloader powered by yt-dlp and ffmpeg.<br>"
        "Created with Python and PyQt6.<br><br>"
        "<b>Features</b><br>"
        "• Queue and batch download multiple URLs<br>"
        "• MP3, Opus and M4A formats with quality selection<br>"
        "• Optional embedded cover art and metadata<br>"
        "• Playlist download or selected track only<br>"
        "• Custom filename templates and output folder<br>"
        "• Cancel downloads and review download history<br>"
        "• Choose German or English in Settings<br>"
        "• Integrated changelog and legal information<br>"
        "• Automatic yt-dlp detection<br><br>" if english else
        "Audio-Downloader für Linux auf Basis von yt-dlp und ffmpeg.<br>"
        "Erstellt mit Python und PyQt6.<br><br>"
        "<b>Funktionen</b><br>"
        "• Warteschlange und mehrere URLs auf einmal herunterladen<br>"
        "• MP3, Opus und M4A mit wählbarer Qualität<br>"
        "• Coverbild und Metadaten optional einbetten<br>"
        "• Ganze Playlist oder nur ausgewählten Titel laden<br>"
        "• Eigene Dateinamenvorlagen und Zielordner<br>"
        "• Downloads abbrechen und Verlauf einsehen<br>"
        "• Deutsch oder Englisch in den Einstellungen auswählen<br>"
        "• Integrierte Changelog- und Rechtsdialoge<br>"
        "• Automatische yt-dlp-Erkennung<br><br>"
    )

    text_label = QLabel(
        f"Version {VERSION}<br><br>" + info_text +
        ("<b>Author:</b> Markus <br><br>" if english else "<b>Autor:</b> Markus <br><br>") +
        '🌐 <a href="https://wildcardcharacter.github.io">' + "Website" + "</a><br>" +
        '📧 <a href="mailto:wildcardcharacter@icloud.com">' + ("Email" if english else "E-Mail") + "</a><br><br>" +
        "─────────────────<br><br>" +
        ("If you enjoy AudioHarvester and would like to support its development:" if english else
         "Wenn dir AudioHarvester gefällt und du die Entwicklung unterstützen möchtest:")
    )

    text_label.setOpenExternalLinks(True)
    text_label.setTextFormat(Qt.TextFormat.RichText)
    text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    text_label.setWordWrap(True)

    layout.addWidget(text_label)

    support_button = QPushButton(
        "☕ Support AudioHarvester" if english else "☕ AudioHarvester unterstützen"
    )

    support_button.clicked.connect(
        lambda: QDesktopServices.openUrl(
            QUrl(
                "https://buymeacoffee.com/wildcardcharacter"
            )
        )
    )

    layout.addWidget(support_button)

    close_button = QPushButton("Close" if english else "Schließen")
    close_button.clicked.connect(dialog.close)

    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()
