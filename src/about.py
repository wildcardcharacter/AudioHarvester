from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from version import VERSION


MODULE_DIR = Path(__file__).resolve().parent
ICON_FILE = next(
    (
        path
        for path in (
            MODULE_DIR.parent / "assets" / "icons" / "audioharvester.png",
            MODULE_DIR / "assets" / "icons" / "audioharvester.png",
            MODULE_DIR / "icons" / "audioharvester.png",
        )
        if path.exists()
    ),
    MODULE_DIR / "icons" / "audioharvester.png",
)


def show_info_dialog(parent=None, language="Deutsch"):
    english = language == "English"
    dialog = QDialog(parent)
    dialog.setWindowTitle("About AudioHarvester" if english else "Über AudioHarvester")
    dialog.setMinimumSize(400, 460)
    dialog.resize(500, 600)

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(12)

    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(4, 4, 4, 8)
    content_layout.setSpacing(14)

    hero = QFrame()
    hero.setObjectName("aboutHero")
    hero.setStyleSheet(
        "QFrame#aboutHero { background: palette(alternate-base); "
        "border: 1px solid palette(mid); border-radius: 10px; }"
    )
    hero_layout = QHBoxLayout(hero)
    hero_layout.setContentsMargins(16, 14, 16, 14)
    hero_layout.setSpacing(16)

    icon_label = QLabel()
    pixmap = QPixmap(str(ICON_FILE))
    if not pixmap.isNull():
        icon_label.setPixmap(pixmap.scaled(76, 76, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation))
        hero_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignVCenter)

    identity_layout = QVBoxLayout()
    title = QLabel("AudioHarvester")
    title.setStyleSheet("font-size: 21px; font-weight: 650;")
    identity_layout.addWidget(title)

    subtitle = QLabel(
        "Audio-Downloader für Linux mit yt-dlp und ffmpeg."
        if not english
        else "A Linux audio downloader powered by yt-dlp and ffmpeg."
    )
    subtitle.setWordWrap(True)
    subtitle.setStyleSheet("color: palette(placeholder-text);")
    identity_layout.addWidget(subtitle)

    version = QLabel(f"Version {VERSION}")
    version.setStyleSheet("font-weight: 600; padding-top: 3px;")
    identity_layout.addWidget(version)
    hero_layout.addLayout(identity_layout, 1)
    content_layout.addWidget(hero)

    features_heading = QLabel("Funktionen" if not english else "Features")
    features_heading.setStyleSheet("font-size: 15px; font-weight: 600;")
    content_layout.addWidget(features_heading)

    features = (
        "Warteschlange für mehrere URLs und Playlists\n"
        "MP3, Opus und M4A mit wählbarer Qualität\n"
        "Coverbilder, Metadaten und Dateinamenvorlagen\n"
        "Download-Verlauf und eigener Zielordner\n"
        "Updateprüfung und Installation neuer Versionen\n"
        "Deutsche und englische Oberfläche"
        if not english
        else "Queue for multiple URLs and playlists\n"
        "MP3, Opus and M4A with selectable quality\n"
        "Cover art, metadata, and filename templates\n"
        "Download history and custom output folder\n"
        "Check for and install updates\n"
        "German and English interface"
    )
    feature_list = QLabel("•  " + features.replace("\n", "\n•  "))
    feature_list.setWordWrap(True)
    feature_list.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    feature_list.setStyleSheet(
        "padding: 12px 14px; background: palette(alternate-base); "
        "border: 1px solid palette(mid); border-radius: 8px; line-height: 1.5;"
    )
    content_layout.addWidget(feature_list)

    author = QLabel(
        "Entwickelt von <b>Markus</b> · Python und PyQt6"
        if not english
        else "Created by <b>Markus</b> · Python and PyQt6"
    )
    author.setTextFormat(Qt.TextFormat.RichText)
    author.setAlignment(Qt.AlignmentFlag.AlignCenter)
    content_layout.addWidget(author)

    links = QLabel(
        '<a href="https://wildcardcharacter.github.io">Website</a> '
        ' · <a href="https://github.com/wildcardcharacter/AudioHarvester">GitHub</a> '
        ' · <a href="mailto:wildcardcharacter@icloud.com">E-Mail</a>'
    )
    links.setOpenExternalLinks(True)
    links.setAlignment(Qt.AlignmentFlag.AlignCenter)
    content_layout.addWidget(links)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    scroll_area.setWidget(content)
    layout.addWidget(scroll_area, 1)

    support_button = QPushButton(
        "☕ AudioHarvester unterstützen" if not english else "☕ Support AudioHarvester"
    )
    support_button.clicked.connect(
        lambda: QDesktopServices.openUrl(
            QUrl("https://buymeacoffee.com/wildcardcharacter")
        )
    )
    layout.addWidget(support_button)

    close_button = QPushButton("Schließen" if not english else "Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    dialog.exec()
