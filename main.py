import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

# Assicurati che i file esistano in queste cartelle
from src.ui.tts_view import TTSGeneratorView
from src.ui.editor_view import AudioEditorView
from src.ui.library_view import AudioLibraryView  # <--- Importa la nuova vista


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESTERINATOR - Audio Suite")
        self.resize(1000, 750)  # Un po' più grande per accomodare tutto

        # --- CONFIGURAZIONE CARTELLA LIBRERIA ---
        # Crea una cartella "audio_library" nella directory del progetto
        base_dir = os.path.dirname(os.path.abspath(__file__))
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())