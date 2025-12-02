import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListView, QLabel,
    QPushButton, QHBoxLayout, QMessageBox,
    QFileSystemModel, QMenu, QAbstractItemView
)
from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices, QCursor, QAction


class AudioLibraryView(QWidget):
    # Creiamo un segnale che dice: "Ehi Main, qualcuno vuole editare questo testo!"
    edit_requested = Signal(str)

    def __init__(self, library_path):
        super().__init__()
        self.library_path = library_path

        # Assicuriamoci che il path sia assoluto
        if not os.path.isabs(self.library_path):
            self.library_path = os.path.abspath(self.library_path)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Intestazione ---
        header = QLabel(f"📂 Libreria Audio: {self.library_path}")
        header.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(header)

        # --- Modello File System ---
        self.model = QFileSystemModel()
        self.model.setRootPath(self.library_path)
        # Filtro per vedere solo file audio
        self.model.setNameFilters(["*.mp3", "*.wav"])
        self.model.setNameFilterDisables(False)

        # --- Vista Lista ---
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(self.library_path))
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)  # Una selezione alla volta per sicurezza

        # Eventi
        self.list_view.doubleClicked.connect(self.play_file)

        # ABILITIAMO IL TASTO DESTRO (Context Menu)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.list_view)

        # --- Pulsanti Azione ---
        btn_layout = QHBoxLayout()

        self.btn_open_folder = QPushButton("Apri Cartella")
        self.btn_open_folder.clicked.connect(self.open_system_folder)
        btn_layout.addWidget(self.btn_open_folder)

        self.btn_refresh = QPushButton("Aggiorna")
        self.btn_refresh.clicked.connect(self.refresh_view)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_edit = QPushButton("✏️ Edita Testo")
        self.btn_edit.setStyleSheet("background-color: #FFF3E0; color: #E65100; font-weight: bold;")
        self.btn_edit.clicked.connect(self.load_text_for_editing)
        btn_layout.addWidget(self.btn_edit)

        # PULSANTE ELIMINA (Rosso per attenzione)
        self.btn_delete = QPushButton("Elimina File")
        self.btn_delete.setStyleSheet("background-color: #ffcccc; color: #cc0000; font-weight: bold;")
        self.btn_delete.clicked.connect(self.delete_selected_file)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    # --- LOGICA EDITA ---
    def load_text_for_editing(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Attenzione", "Seleziona un file da editare.")
            return

        mp3_path = self.model.filePath(index)

        # Cerchiamo il file JSON corrispondente
        # Se il file è "audio.mp3", cerchiamo "audio.json"
        base_path = os.path.splitext(mp3_path)[0]
        json_path = base_path + ".json"

        if not os.path.exists(json_path):
            QMessageBox.warning(
                self, "Dati mancanti",
                "Non trovo il testo originale per questo file.\n"
                "(Forse è stato generato con una versione vecchia o il file .json è stato cancellato)"
            )
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text_content = data.get("text", "")

                # Emettiamo il segnale con il testo trovato
                self.edit_requested.emit(text_content)

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile leggere il file progetto:\n{e}")

    # --- LOGICA DI CANCELLAZIONE ---
    def delete_selected_file(self):
        index = self.list_view.currentIndex()
        if not index.isValid(): return

        file_path = self.model.filePath(index)
        file_name = self.model.fileName(index)

        confirm = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Vuoi eliminare '{file_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                os.remove(file_path)  # Rimuove MP3

                # Rimuove anche il JSON se esiste, per non lasciare spazzatura
                base_path = os.path.splitext(file_path)[0]
                json_path = base_path + ".json"
                if os.path.exists(json_path):
                    os.remove(json_path)

            except OSError as e:
                QMessageBox.critical(self, "Errore", f"Errore eliminazione: {e}")


    # --- MENU TASTO DESTRO ---
    def show_context_menu(self, point):
        index = self.list_view.indexAt(point)
        if not index.isValid():
            return

        menu = QMenu(self)

        # Azione Play
        action_play = QAction("Riproduci", self)
        action_play.triggered.connect(lambda: self.play_file(index))
        menu.addAction(action_play)

        # Azione Elimina
        action_delete = QAction("Elimina", self)
        action_delete.triggered.connect(self.delete_selected_file)
        menu.addAction(action_delete)

        # Azione Edita
        action_edit = menu.addAction("✏️ Edita Testo")
        action_edit.triggered.connect(self.load_text_for_editing)

        # Mostra il menu alla posizione del cursore
        menu.exec(QCursor.pos())

    # --- ALTRE FUNZIONI ---
    def play_file(self, index):
        file_path = self.model.filePath(index)
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def open_system_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.library_path))

    def refresh_view(self):
        # Reset del path per forzare refresh
        self.model.setRootPath("")
        self.model.setRootPath(self.library_path)
        self.list_view.setRootIndex(self.model.index(self.library_path))