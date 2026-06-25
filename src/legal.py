from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PyQt6.QtCore import Qt


def show_legal_dialog(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Rechtlicher Hinweis")
    dialog.resize(600, 450)

    layout = QVBoxLayout()

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

    close_button = QPushButton("Schließen")
    close_button.clicked.connect(dialog.close)

    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()