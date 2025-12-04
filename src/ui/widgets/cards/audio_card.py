import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QHBoxLayout

from src.ui.widgets.buttons.icon_button import IconButton
from src.ui.widgets.cards.base_card import BaseCardWidget


class AudioCardWidget(BaseCardWidget):
    play_requested = Signal(str)
    delete_requested = Signal(str)
    edit_requested = Signal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.setProperty("class", "AudioCardWidget")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        # NON settare l'allineamento del layout verticale a center,
        # perché fa centrare TUTTO verticalmente, creando spazi strani
        # layout.setAlignment(Qt.AlignCenter)  # rimosso

        # Icona centrale
        icon_path = "src/resources/icons/cards/normal/music_note.png"
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Errore: immagine non trovata {icon_path}")
        else:
            pixmap = pixmap.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)

        # Titolo file
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        title_label = QLabel(file_name)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label, alignment=Qt.AlignHCenter)

        # Linea divisoria
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setProperty("role", "divider")  # utile se usi CSS che si basa su role
        layout.addWidget(divider)

        # Layout pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setContentsMargins(0, 10, 0, 0)  # margine superiore per distanziare i pulsanti dal divider
        btn_layout.setAlignment(Qt.AlignCenter)      # centra i pulsanti orizzontalmente

        # Play
        play_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/play.png",
            icon_path_hover="src/resources/icons/cards/hover/play.png",
            tooltip="Ascolta"
        )
        play_btn.clicked.connect(lambda: self.play_requested.emit(self.file_path))
        btn_layout.addWidget(play_btn)

        # Edit
        edit_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/edit.png",
            icon_path_hover="src/resources/icons/cards/hover/edit.png",
            tooltip="Modifica"
        )
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.file_path))
        btn_layout.addWidget(edit_btn)

        # Delete
        delete_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/delete.png",
            icon_path_hover="src/resources/icons/cards/hover/delete.png",
            tooltip="Elimina file"
        )
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.file_path))
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
