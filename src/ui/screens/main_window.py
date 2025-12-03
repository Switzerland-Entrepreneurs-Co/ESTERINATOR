from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from src.ui.screens.library_view import AudioLibraryView
from src.ui.screens.tts.tts_view import TTSGeneratorView
from src.ui.screens.editor_view import AudioEditorView

import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESTERINATOR - Audio Suite")
        self.resize(1000, 750)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(base_dir)
        base_dir = os.path.dirname(base_dir)
        self.library_path = os.path.join(base_dir, "audio_library")

        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)

        # Widget centrale e layout orizzontale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Sidebar sinistra ---
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar.setStyleSheet("background-color: #2E3440;")  # esempio colore scuro blu/grigio
        sidebar.setFixedWidth(200)

        # Logo (puoi sostituirlo con una QLabel con immagine)
        logo_label = QLabel()
        pixmap = QPixmap("src/resources/icons/logo.png")
        logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        # Pulsanti di navigazione
        self.btn_tts = QPushButton("Generatore TTS")
        self.btn_library = QPushButton("Libreria Audio")
        self.btn_editor = QPushButton("Editor Audio")

        for btn in (self.btn_tts, self.btn_library, self.btn_editor):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sidebar_layout.addWidget(btn)

        main_layout.addWidget(sidebar)

        # --- Contenuto centrale ---
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Le pagine
        self.tts_view = TTSGeneratorView(self.library_path)
        self.library_view = AudioLibraryView(self.library_path)
        self.editor_view = AudioEditorView()

        self.stack.addWidget(self.tts_view)      # indice 0
        self.stack.addWidget(self.library_view)  # indice 1
        self.stack.addWidget(self.editor_view)   # indice 2

        # Connessioni pulsanti per cambiare pagina
        self.btn_tts.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_library.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_editor.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        self.library_view.edit_requested.connect(self.on_edit_requested)

    def on_edit_requested(self, text_content):
        self.tts_view.set_editor_content(text_content)
        self.stack.setCurrentIndex(0)
