from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLayout, QLabel, QHBoxLayout

from src.core.utility.metadata_extractor import MetadataExtractor
from src.core.utility.res_path import ResourcesPath
from src.ui.components.divider import Divider
from src.ui.widgets.buttons.icon_button import IconButton
from src.ui.widgets.cards.card import Card

class AudioCard(Card):
    play_requested = Signal(str)
    edit_requested = Signal(str)
    delete_requested = Signal(str)

    def __init__(self, path: str):
        super().__init__(path)
        self.setProperty("class", "audio-card")

    # --- Metodi da implementare ---
    # Mostra l'icona
    def _icon(self) -> QLabel:
        # Icona
        icon_label = QLabel()
        icon_label.setFixedSize(60, 60)
        icon_label.setPixmap(QPixmap(ResourcesPath.AUDIO_CARD_MAIN).scaled(48,48))
        icon_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        icon_label.setProperty("class", "card-icon")

        return icon_label

    # Informazioni/metadati
    def _body(self) -> QLayout:
        body = QHBoxLayout()

        body.addWidget(Divider())

        metadata = MetadataExtractor.extract_mp3_metadata(self.path)
        audio_info = QLabel(f"{metadata['duration_str']} - {metadata['last_modified_str']}")
        body.addWidget(audio_info)

        body.addWidget(Divider())

        return body

    # Dove vanno i bottoni
    def _action_bar(self) -> QLayout:
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setAlignment(Qt.AlignCenter)

        play_btn = IconButton(
            icon_path_normal=ResourcesPath.AUDIO_CARD_PLAY,
            tooltip="Ascolta"
        )
        play_btn.clicked.connect(lambda: self.play_requested.emit(self.path))
        btn_layout.addWidget(play_btn)

        edit_btn = IconButton(
            icon_path_normal=ResourcesPath.AUDIO_CARD_EDIT,
            tooltip="Modifica"
        )
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.path))
        btn_layout.addWidget(edit_btn)

        delete_btn = IconButton(
            icon_path_normal=ResourcesPath.AUDIO_CARD_DELETE,
            tooltip="Elimina"
        )
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.path))
        btn_layout.addWidget(delete_btn)

        return btn_layout

    # ------