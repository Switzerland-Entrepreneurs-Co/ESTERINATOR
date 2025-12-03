from PySide6.QtWidgets import QMainWindow, QTabWidget
from src.ui.screens.library_view import AudioLibraryView

import os

# Import corretti basati sui nuovi nomi dei file (snake_case)
from src.ui.screens.tts.tts_view import TTSGeneratorView
from src.ui.screens.editor_view import AudioEditorView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESTERINATOR - Audio Suite")
        self.resize(1000, 750)  # Un po' più grande per accomodare tutto

        # --- CONFIGURAZIONE CARTELLA LIBRERIA ---
        # Crea una cartella "audio_library" nella directory del progetto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(base_dir)
        base_dir = os.path.dirname(base_dir)
        print(base_dir)
        # Se main.py è nella root, ok. Se è in src, potresti dover fare os.path.dirname due volte.
        # Assumiamo main.py sia nella root del progetto:
        self.library_path = os.path.join(base_dir, "audio_library")

        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)

        # --- UI ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: TTS Generator (Passiamo il path della libreria)
        self.tts_view = TTSGeneratorView(self.library_path)
        self.tabs.addTab(self.tts_view, "Generatore TTS")

        # Tab 2: Audio Library (Passiamo lo stesso path)
        self.library_view = AudioLibraryView(self.library_path)
        self.tabs.addTab(self.library_view, "Libreria Audio")

        # Tab 3: Editor Audio
        self.editor_view = AudioEditorView()
        self.tabs.addTab(self.editor_view, "Editor Audio")

        self.library_view.edit_requested.connect(self.on_edit_requested)

    def on_edit_requested(self, text_content):
        # 1. Imposta il testo nella vista TTS
        self.tts_view.set_editor_content(text_content)

        # 2. Cambia la tab attiva (0 è l'indice del Generatore TTS)
        self.tabs.setCurrentIndex(0)