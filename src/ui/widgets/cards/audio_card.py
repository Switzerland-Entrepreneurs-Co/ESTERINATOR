import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout

from src.ui.widgets.cards.base_card import BaseCardWidget


class AudioCardWidget(BaseCardWidget):
    play_requested = Signal(str)
    delete_requested = Signal(str)
    edit_requested = Signal(str)

    def __init__(self, file_path: str, color: str = "#FF6A3D"):
        super().__init__()
        self.file_path = file_path
        self.color = color
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Icona centrale: nota musicale Unicode 🎵
        icon_label = QLabel("🎵")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 72px;")
        layout.addWidget(icon_label)

        # Nome file senza path
        file_name = os.path.basename(self.file_path)
        title_label = QLabel(file_name)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(f"color: #333333; font-weight: bold; font-size: 16px;")
        layout.addWidget(title_label)

        # Linea divisoria sottile
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #E5E5E5;")
        layout.addWidget(divider)

        # Pulsanti play, edit, delete
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setAlignment(Qt.AlignCenter)

        # Play button ▶
        play_btn = QPushButton("▶")
        play_btn.setToolTip("Ascolta audio")
        play_btn.setStyleSheet(f"color: {self.color}; font-size: 24px; background: none; border: none;")
        play_btn.clicked.connect(lambda: self.play_requested.emit(self.file_path))
        btn_layout.addWidget(play_btn)

        # Edit button ✏
        edit_btn = QPushButton("✏")
        edit_btn.setToolTip("Modifica trascrizione")
        edit_btn.setStyleSheet(f"color: {self.color}; font-size: 24px; background: none; border: none;")
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.file_path))
        btn_layout.addWidget(edit_btn)

        # Delete button 🗑
        delete_btn = QPushButton("🗑")
        delete_btn.setToolTip("Elimina file")
        delete_btn.setStyleSheet(f"color: {self.color}; font-size: 24px; background: none; border: none;")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.file_path))
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)