import sys

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QComboBox, QPushButton,
    QLabel, QFileDialog, QMessageBox, QApplication
)
from src.core.dialogue_parser import DialogueParser
from src.core.tts_engine import TTSEngine


class TTSGeneratorView(QWidget):
    def __init__(self):
        super().__init__()
        self.tts_engine = TTSEngine()
        self.parser = DialogueParser()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        lbl_info = QLabel("Generatore Dialoghi Neurali (Online)")
        lbl_info.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(lbl_info)

        # --- Controlli Vocali ---
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Voce:"))

        self.voice_combo = QComboBox()
        self.voice_combo.setMinimumWidth(250)
        controls_layout.addWidget(self.voice_combo)

        self.btn_insert_marker = QPushButton("Inserisci Marker")
        self.btn_insert_marker.clicked.connect(self.insert_voice_marker)
        controls_layout.addWidget(self.btn_insert_marker)

        layout.addLayout(controls_layout)

        # --- Area Testo ---
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText(
            "Scrivi qui il dialogo...\n\n[voice=it-IT-DiegoNeural]\nCiao!\n[voice=it-IT-ElsaNeural]\nCome va?"
        )
        layout.addWidget(self.text_edit)

        # --- Pulsante Genera ---
        self.btn_generate = QPushButton("Salva e Genera Dialogo")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_generate.clicked.connect(self.generate_dialogue)
        layout.addWidget(self.btn_generate)

        self.setLayout(layout)
        self.resize(600, 500)
        self.populate_voices()

    def populate_voices(self):
        self.voice_combo.clear()
        voices = self.tts_engine.get_voices()

        default_idx = 0
        for i, v in enumerate(voices):
            # v['name'] è ora quello "bello" formattato dall'engine
            self.voice_combo.addItem(v['name'], v['id'])

            # Cerchiamo di preselezionare Diego (Italiano)
            if "Diego" in v['name'] and "Italiano" in v['name']:
                default_idx = i

        self.voice_combo.setCurrentIndex(default_idx)

    def insert_voice_marker(self):
        voice_id = self.voice_combo.currentData()
        # Per pulizia, nel testo inseriamo solo l'ID tecnico, ma l'utente ha scelto dal nome bello
        if voice_id:
            marker = f"\n[voice={voice_id}]\n"
            self.text_edit.insertPlainText(marker)
            self.text_edit.setFocus()

    def generate_dialogue(self):
        text = self.text_edit.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Attenzione", "Inserisci del testo.")
            return

        segments = self.parser.parse(text)
        if not segments:
            QMessageBox.warning(self, "Attenzione", "Nessun segmento trovato.")
            return

        # --- NUOVA LOGICA DI SALVATAGGIO ---
        # getSaveFileName restituisce una tupla (path, filter), ci serve solo path
        # Impostiamo la dir di default su "Documenti" o simile se vuoi, qui lascio vuoto (last visited)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva file audio",
            "dialogo_nuovo.mp3",  # Nome default suggerito
            "File Audio MP3 (*.mp3)"
        )

        if not file_path:
            return  # Utente ha premuto annulla

        self.btn_generate.setText("Generazione in corso...")
        self.btn_generate.setEnabled(False)
        QApplication.processEvents()

        try:
            # Passiamo il path completo scelto dall'utente
            success = self.tts_engine.generate_dialogue(segments, file_path)

            if success:
                QMessageBox.information(self, "Fatto", f"Dialogo salvato correttamente in:\n{file_path}")
            else:
                QMessageBox.critical(self, "Errore", "Errore durante la generazione.")
        finally:
            self.btn_generate.setText("Salva e Genera Dialogo")
            self.btn_generate.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = TTSGeneratorView()
    view.show()
    sys.exit(app.exec())