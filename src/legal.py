from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
)

from PyQt6.QtCore import Qt


def show_legal_dialog(parent=None, language="Deutsch"):
    english = language == "English"
    dialog = QDialog(parent)
    dialog.setWindowTitle("Legal notice" if english else "Rechtlicher Hinweis")
    dialog.resize(620, 520)
    dialog.setMinimumSize(380, 320)

    layout = QVBoxLayout()
    layout.setContentsMargins(18, 16, 18, 16)
    layout.setSpacing(12)

    title_label = QLabel("<h2>Legal notice</h2>" if english else "<h2>Rechtlicher Hinweis</h2>")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title_label)

    text_label = QLabel(
        ("AudioHarvester is a tool for downloading audio content.<br><br>"
        "<b>Please note:</b><br><br>"
        "• Downloads should only be made from lawful sources.<br><br>"
        "• Circumventing technical protection measures is prohibited.<br><br>"
        "• YouTube's terms of service may prohibit downloads.<br><br>"
        "• Content may not be shared or used commercially without permission.<br><br>"
        "<b>Each user is responsible for complying with applicable laws and terms of service.</b>" if english else
        "AudioHarvester ist ein Werkzeug zum Herunterladen von Audioinhalten.<br><br>"
        "<b>Bitte beachten Sie:</b><br><br>"
        "• Privatkopien können für den persönlichen Gebrauch zulässig sein.<br><br>"
        "• Downloads sollten nur von rechtmäßigen Quellen erfolgen.<br><br>"
        "• Das Umgehen technischer Schutzmaßnahmen ist nicht erlaubt.<br><br>"
        "• YouTube-Nutzungsbedingungen können Downloads untersagen.<br><br>"
        "• Inhalte dürfen nicht ohne Erlaubnis verbreitet oder kommerziell genutzt werden.<br><br>"
        "<b>Jeder Nutzer ist selbst verantwortlich, geltende Gesetze und Nutzungsbedingungen einzuhalten.</b>")
    )

    text_label.setWordWrap(True)
    text_label.setTextFormat(Qt.TextFormat.RichText)
    text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    text_label.setMargin(14)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    scroll_area.setWidget(text_label)
    layout.addWidget(scroll_area, 1)

    close_button = QPushButton("Close" if english else "Schließen")
    close_button.clicked.connect(dialog.close)

    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()
