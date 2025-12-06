from PySide6.QtWidgets import QStackedWidget

from src.ui.screens.alias_editor import AliasEditor
from src.ui.screens.editor_view import AudioEditorView
from src.ui.screens.library_view import AudioLibraryView
from src.ui.screens.tts.tts_view import TTSGeneratorView


# --- Contenuto centrale ---
class StackPane(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.pages = []

        self._init_pages()

    def _init_pages(self):
        self.pages.append(TTSGeneratorView()) # indice 0
        self.pages.append(AudioLibraryView()) # indice 1
        self.pages.append(AudioEditorView())                   # indice 2
        self.pages.append(AliasEditor())                       # indice 3

        for page in self.pages:
            self.addWidget(page)