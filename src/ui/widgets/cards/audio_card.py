import os
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout

from src.ui.widgets.buttons.icon_button import IconButton
from src.ui.widgets.cards.base_card import BaseCardWidget


class AudioCardWidget(BaseCardWidget):
    play_requested = Signal(str)
    delete_requested = Signal(str)
    edit_requested = Signal(str)

    def __init__(self, file_path: str, color: str = "#932191"):  # default viola
        super().__init__()
        self.file_path = file_path
        self.color = color
        self.setMinimumSize(200, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Icona centrale da file
        icon_path = "src/resources/icons/cards/normal/music_note.png"
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Errore: immagine non trovata {icon_path}")
        else:
            pixmap = pixmap.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        # Nome file senza path - testo grigio chiaro
        file_name = os.path.basename(self.file_path)
        title_label = QLabel(file_name)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Linea divisoria sottile chiara
        divider = QFrame()
        divider.setFixedHeight(1)
        layout.addWidget(divider)

        # Layout pulsanti
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setAlignment(Qt.AlignCenter)

        play_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/play.png",
            icon_path_hover="src/resources/icons/cards/hover/play.png",
            tooltip="Ascolta"
        )
        play_btn.clicked.connect(lambda: self.play_requested.emit(self.file_path))
        btn_layout.addWidget(play_btn)

        edit_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/edit.png",
            icon_path_hover="src/resources/icons/cards/hover/edit.png",
            tooltip="Modifica"
        )
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.file_path))
        btn_layout.addWidget(edit_btn)

        delete_btn = IconButton(
            icon_path_normal="src/resources/icons/cards/normal/delete.png",
            icon_path_hover="src/resources/icons/cards/hover/delete.png",
            tooltip="Elimina file"
        )
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.file_path))
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)
