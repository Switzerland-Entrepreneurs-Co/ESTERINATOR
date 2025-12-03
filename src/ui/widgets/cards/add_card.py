from PySide6.QtWidgets import QVBoxLayout, QPushButton

from src.ui.widgets.cards.base_card import BaseCardWidget
from PySide6.QtCore import Signal, Qt

class AddCardWidget(BaseCardWidget):
    add_requested = Signal()

    def __init__(self, color: str = "#FF6A3D"):
        super().__init__()
        self.color = color
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignCenter)

        # Bottone grande "+" al centro
        add_btn = QPushButton("+")
        add_btn.setFixedSize(100, 100)
        add_btn.clicked.connect(lambda: self.add_requested.emit())
        layout.addWidget(add_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
