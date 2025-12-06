from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout
)
from src.config import AUDIO_LIBRARY_PATH
import os

from src.ui.sidebar.sidebar import Sidebar
from src.ui.sidebar.stack_pane import StackPane


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Esterinator - Text to Esterina")
        self.resize(1000, 750)

        self.library_path = AUDIO_LIBRARY_PATH

        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)

        # Widget centrale e layout orizzontale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # --- Contenuto centrale ---
        self.stack = StackPane()
        main_layout.addWidget(self.stack)

        self.sidebar.config_buttons(self.stack.setCurrentIndex)

