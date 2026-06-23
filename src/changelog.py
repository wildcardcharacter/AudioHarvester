from pathlib import Path
from markdown import markdown

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton
)

def show_changelog_dialog(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("AudioHarvester Changelog")
    dialog.resize(700, 500)

    layout = QVBoxLayout()

    changelog_view = QTextEdit()
    changelog_view.setReadOnly(True)
    changelog_view.setLineWrapMode(
        QTextEdit.LineWrapMode.WidgetWidth
    )

    changelog_file = (
        Path(__file__).resolve().parent.parent
        / "CHANGELOG.md"
    )

    if changelog_file.exists():
        text = changelog_file.read_text(
            encoding="utf-8"
        )

        changelog_view.setHtml(
            markdown(text)
        )
    else:
        changelog_view.setPlainText(
            "CHANGELOG.md wurde nicht gefunden."
        )

    layout.addWidget(changelog_view)

    close_button = QPushButton("Schließen")
    close_button.clicked.connect(dialog.close)
    layout.addWidget(close_button)

    dialog.setLayout(layout)
    dialog.exec()