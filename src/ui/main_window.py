from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QSizePolicy, QMessageBox
)
from src.config import AUDIO_LIBRARY_PATH, ICONS_PATH
from src.core.tts_engine import tts_engine
from src.ui.screens.library_view import AudioLibraryView
from src.ui.screens.tts.tts_view import TTSGeneratorView
from src.ui.screens.editor_view import AudioEditorView
from src.ui.screens.alias_editor import AliasEditor  # Nuova schermata AliasEditor

import os

from src.ui.sidebar.sidebar import Sidebar
from src.ui.sidebar.stack_pane import StackPane


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESTERINATOR - Text to Esterina")
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

        # Le pagine
        self.tts_view = TTSGeneratorView(self.library_path)
        self.library_view = AudioLibraryView(self.library_path)
        self.editor_view = AudioEditorView()
        self.alias_editor_view = AliasEditor()  # Passo base_dir a AliasEditor

        self.stack.addWidget(self.tts_view)         # indice 0
        self.stack.addWidget(self.library_view)     # indice 1
        self.stack.addWidget(self.editor_view)      # indice 2
        self.stack.addWidget(self.alias_editor_view)  # indice 3

        # Gestione segnali
        self.library_view.edit_requested.connect(self.on_edit_requested)
        self.alias_editor_view.saved.connect(self.handle_alias_save)

    def on_edit_requested(self, text_content):
        # Logica esistente: apri TTS e passa testo
        self.tts_view.set_editor_content(text_content)
        self.stack.setCurrentIndex(0)

    def handle_alias_save(self):
        # Ricarica keyword nell'engine (se necessario)
        tts_engine().reload_keywords()
        # Aggiorna evidenziazione nel TTS view
        self.tts_view.refresh_highlighter_keywords()
