import os

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel

from src.config import ICONS_PATH


# Logo
class Logo(QLabel):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logo_path = os.path.join(ICONS_PATH, "logo.png")
        pixmap = QPixmap(logo_path)
        self.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)