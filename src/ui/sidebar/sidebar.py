from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy

from src.ui.components.logo import Logo

# Sidebar sinistra della main
class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.init_ui()

    # Qui mettiamo tutti i bottoni
    def _generate_buttons(self, sidebar_layout):
        # Pulsanti di navigazione
        self.buttons.append(QPushButton("Generatore TTS"))
        self.buttons.append(QPushButton("Libreria Audio"))
        self.buttons.append(QPushButton("Editor Audio"))
        self.buttons.append(QPushButton("Alias Editor"))

        for btn in self.buttons:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sidebar_layout.addWidget(btn)

    # Chiamata da MainWindow per configurare il comportamento dei bottoni
    def config_buttons(self, callback: callable):
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda _, idx=i: callback(idx))

    def init_ui(self):
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(220)  # leggermente più largo per 4 bottoni

        # Creazione del logo nella sidebar
        sidebar_layout.addWidget(Logo())

        # Aggiunta dei bottonis
        self._generate_buttons(sidebar_layout)

        self.setLayout(sidebar_layout)