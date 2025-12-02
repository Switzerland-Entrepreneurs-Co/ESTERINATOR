import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListView, QLabel,
    QPushButton, QHBoxLayout, QMessageBox,
    QFileSystemModel, QMenu, QAbstractItemView
)
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices, QCursor, QAction


class AudioLibraryView(QWidget):
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

        # PULSANTE ELIMINA (Rosso per attenzione)
        self.btn_delete = QPushButton("Elimina File")
        self.btn_delete.setStyleSheet("background-color: #ffcccc; color: #cc0000; font-weight: bold;")
        self.btn_delete.clicked.connect(self.delete_selected_file)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    # --- LOGICA DI CANCELLAZIONE ---
    def delete_selected_file(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Attenzione", "Seleziona un file da eliminare.")
            return

        # Otteniamo il percorso del file selezionato
        file_path = self.model.filePath(index)
        file_name = self.model.fileName(index)

        # Controlliamo che sia un file e non una cartella (opzionale, ma sicuro)
        if os.path.isdir(file_path):
            QMessageBox.warning(self, "Errore", "Non puoi eliminare intere cartelle da qui.")
            return

        # Chiediamo conferma
        confirm = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare definitivamente:\n'{file_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                os.remove(file_path)
                # Non serve ricaricare manualmente, QFileSystemModel osserva i cambiamenti!
                print(f"[Library] Eliminato: {file_path}")
            except OSError as e:
                QMessageBox.critical(self, "Errore", f"Impossibile eliminare il file.\nErrore: {e}")

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