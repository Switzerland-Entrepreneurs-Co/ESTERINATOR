from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class AudioEditorView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Audio Editor Waveform View (Placeholder)")
        label.setStyleSheet("border: 2px dashed #666; padding: 50px;")

        btn_load = QPushButton("Carica Traccia (To Do)")

        layout.addWidget(label)
        layout.addWidget(btn_load)

        self.setLayout(layout)