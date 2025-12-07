import os

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLayout, QLabel


class Card(QFrame):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self._init_ui()

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

    # Metodo template
    def _init_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(12, 12, 12, 12)
        main.setSpacing(10)

        main.addLayout(self._top_bar())
        main.addLayout(self._body())
        main.addLayout(self._action_bar())

    # Icona e titolo
    def _top_bar(self):
        top = QHBoxLayout()

        top.addLayout(self._icon())
        top.addLayout(self._title_subtitle())
        # TODO: Scopri se serve
        # top.addLayout(self._menu_button())

        return top

    # Titolo e sottotitolo della card
    def _title_subtitle(self) -> QVBoxLayout:
        title_box = QVBoxLayout()

        title = os.path.splitext(os.path.basename(self.path))[0]

        title_label = QLabel(title)
        title_label.setProperty("class", "card-title")
        # TODO: Questo è temporaneo, cambiare con un sottotitolo vero
        subtitle_label = QLabel(os.path.dirname(self.path))
        subtitle_label.setProperty("class", "card-subtitle")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)

        return title_box