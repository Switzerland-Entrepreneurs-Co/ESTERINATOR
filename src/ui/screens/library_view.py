from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QMessageBox, QScrollArea, QGridLayout
)
from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices

from src.ui.widgets.cards.add_card import AddCardWidget
from src.ui.widgets.cards.audio_card import AudioCardWidget
import os
import json


class AudioLibraryView(QWidget):
    edit_requested = Signal(str)

    def __init__(self, library_path):
        super().__init__()
        self.library_path = os.path.abspath(library_path)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        header = QLabel(f"📂 Libreria Audio: {self.library_path}")
        header.setStyleSheet("color: gray; font-size: 11px;")
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

        open_btn = QPushButton("Apri Cartella")
        open_btn.clicked.connect(self.open_system_folder)
        btns.addWidget(open_btn)

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

        # Aggiungi prima la card per creare nuovo file
        add_card = AddCardWidget(color="#FF7AAC")
        # TODO: Fai in modo che apra la TTSView senza testo
        self.grid.addWidget(add_card, row, col)

        col += 1
        if col >= columns:
            col = 0
            row += 1

        # Poi aggiungi le card audio
        for fname in os.listdir(self.library_path):
            if fname.lower().endswith((".wav", ".mp3")):
                full_path = os.path.join(self.library_path, fname)
                color = "#FF7AAC"

                card = AudioCardWidget(full_path, color=color)

                card.play_requested.connect(self.play_file)
                card.delete_requested.connect(self.delete_file)
                card.edit_requested.connect(self.load_text_for_editing)

                self.grid.addWidget(card, row, col)

                col += 1
                if col >= columns:
                    col = 0
                    row += 1

    def play_file(self, file_path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def delete_file(self, file_path):
        name = os.path.basename(file_path)

        confirm = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Vuoi davvero eliminare '{name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            os.remove(file_path)
            json_path = os.path.splitext(file_path)[0] + ".json"
            if os.path.exists(json_path):
                os.remove(json_path)
            self.refresh_view()
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

    def load_text_for_editing(self, file_path):
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
