from enum import IntEnum

from PySide6.QtWidgets import QStackedWidget

from src.core.tts_engine import TTSEngine
from src.ui.screens.alias_editor import AliasEditor
from src.ui.screens.editor_view import AudioEditorView
from src.ui.screens.library_view import AudioLibraryView
from src.ui.screens.tts.tts_view import TTSGeneratorView

class PageIndex(IntEnum):
    TTS = 0
    LIBRARY = 1
    AUDIO_EDITOR = 2
    ALIAS_EDITOR = 3

# --- Contenuto centrale ---
class StackPane(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.pages = []

        self._init_pages()
        self._init_signals()

    def _init_pages(self):
        self.pages.append(TTSGeneratorView())
        self.pages.append(AudioLibraryView())
        self.pages.append(AudioEditorView())
        self.pages.append(AliasEditor())

        for page in self.pages:
            self.addWidget(page)

    # TODO: Rifletti sul rimuovere questo e i metodi che seguono
    def _init_signals(self):
        # Gestione segnali
        self.pages[PageIndex.LIBRARY].edit_requested.connect(self._on_edit_requested)
        self.pages[PageIndex.ALIAS_EDITOR].saved.connect(self._handle_alias_save)

    def _on_edit_requested(self, text_content):
        # Logica esistente: apri TTS e passa testo
        self.pages[PageIndex.TTS].set_editor_content(text_content)
        self.setCurrentIndex(PageIndex.TTS)

    def _handle_alias_save(self):
        # Ricarica keyword nell'engine (se necessario)
        TTSEngine().reload_keywords()
        # Aggiorna evidenziazione nel TTS view
        self.pages[PageIndex.TTS].refresh_highlighter_keywords()