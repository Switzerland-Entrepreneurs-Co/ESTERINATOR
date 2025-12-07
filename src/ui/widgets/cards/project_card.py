from PySide6.QtWidgets import QLayout

from src.ui.widgets.cards.card import Card


class ProjectCard(Card):
    def __init__(self, path: str):
        super().__init__(path)

    # --- Metodi da implementare ---
    # Mostra l'icona
    def _icon(self) -> QLayout:
        pass

    # Informazioni/metadati
    def _body(self) -> QLayout:
        pass

    # Dove vanno i bottoni
    def _action_bar(self) -> QLayout:
        pass
    # ------