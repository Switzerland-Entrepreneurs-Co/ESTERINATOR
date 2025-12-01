from PySide6.QtWidgets import QMainWindow, QTabWidget

# Import corretti basati sui nuovi nomi dei file (snake_case)
from src.ui.tts_view import TTSGeneratorView
from src.ui.editor_view import AudioEditorView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESTERINATOR - Audio Suite")
        self.resize(900, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: TTS Generator
        self.tts_view = TTSGeneratorView()
        self.tabs.addTab(self.tts_view, "Generatore TTS")

        # Tab 2: Audio Editor
        self.editor_view = AudioEditorView()
        self.tabs.addTab(self.editor_view, "Editor Audio")