from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QMessageBox, QScrollArea, QGridLayout
)
from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices

from src.config import AUDIO_LIBRARY_PATH
import os
import json

from src.core.file_manager import FileManager
from src.ui.popup import Popup
from src.ui.widgets.cards.audio_card import AudioCard


class AudioLibraryView(QWidget):
    edit_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.library_path = os.path.abspath(AUDIO_LIBRARY_PATH)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Header è un pulsante che apre la cartella audio
        header = QPushButton(f"📂 Libreria Audio: {self.library_path}")
        header.clicked.connect(self.open_system_folder)
        main_layout.addWidget(header)

        # --- Scroll area con card ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.container.setLayout(self.grid)

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

        # --- Bottoni ---
        btns = QHBoxLayout()

        # TODO: Rimuovere la necessità di questo schifo (con un Observer?)
        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.clicked.connect(self.refresh_view)
        btns.addWidget(refresh_btn)

        main_layout.addLayout(btns)
        self.setLayout(main_layout)

        self.refresh_view()

    def refresh_view(self):
        # Pulisci la griglia
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        columns = 5  # Numero colonne nella griglia
        row = 0
        col = 0

        col += 1
        if col >= columns:
            col = 0
            row += 1

        # Poi aggiungi le card audio
        for fname in os.listdir(self.library_path):
            if fname.lower().endswith((".wav", ".mp3")):
                full_path = os.path.join(self.library_path, fname)

                card = AudioCard(full_path)

                card.play_requested.connect(self.play_file_signal)
                card.delete_requested.connect(self.delete_file_signal)
                card.edit_requested.connect(self.edit_file_signal)

                self.grid.addWidget(card, row, col)

                col += 1
                if col >= columns:
                    col = 0
                    row += 1


    # TODO: SPOSTARE QUESTI SU UN CONTROLLER E NON ALLA CAZZO DI VIEW
    # -------------------------------------------------------------
    def play_file_signal(self, file_path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def delete_file_signal(self, file_path):
        if Popup.delete_file_popup(self, file_path):
            FileManager.delete_file(file_path)

    def edit_file_signal(self, file_path):
        json_path = os.path.splitext(file_path)[0] + ".json"

        if not os.path.exists(json_path):
            QMessageBox.warning(self, "Dati mancanti", "File testo (.json) inesistente.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = data.get("text", "")
            self.edit_requested.emit(text)

    def open_system_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.library_path))

    # -------------------------------------------------------------
