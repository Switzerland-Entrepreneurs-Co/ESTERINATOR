from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from pathlib import Path

class AliasEditor(QWidget):
    saved = Signal(str)  # Segnale emesso con il contenuto salvato

    def __init__(self, base_dir: str):
        super().__init__()
        self.base_dir = Path(base_dir)
        self.alias_map_path = self.base_dir / "config" / "alias_map.txt"
        self.init_ui()
        self.load_file()  # Carica o crea il file all’avvio

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("eg. Esterina -> it-IT-Isabella-Neural")
        layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Salva")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.on_save_clicked)

    def load_file(self):
        """Carica alias_map.txt o lo crea se non esiste."""
        try:
            # Crea cartella config se non esiste
            self.alias_map_path.parent.mkdir(parents=True, exist_ok=True)

            # Crea file vuoto se non esiste
            if not self.alias_map_path.exists():
                self.alias_map_path.touch()

            # Ora leggi il contenuto
            content = self.alias_map_path.read_text(encoding="utf-8")
            self.text_edit.setPlainText(content)

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile accedere a alias_map.txt:\n{e}")

    def on_save_clicked(self):
        """Salva il contenuto modificato su alias_map.txt."""
        content = self.text_edit.toPlainText()
        try:
            self.alias_map_path.write_text(content, encoding="utf-8")
            self.saved.emit(content)
            QMessageBox.information(self, "Salvataggio", "File alias_map.txt salvato correttamente.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile salvare alias_map.txt:\n{e}")
