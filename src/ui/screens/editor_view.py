from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class AudioEditorView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Audio Editor Waveform View (Placeholder)")

        btn_load = QPushButton("Carica Traccia (To Do)")

        layout.addWidget(label)
        layout.addWidget(btn_load)

        self.setLayout(layout)