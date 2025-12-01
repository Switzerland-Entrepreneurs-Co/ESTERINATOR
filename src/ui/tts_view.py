from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QComboBox, QPushButton,
    QLabel, QFileDialog, QMessageBox
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

        # --- Controlli Vocali ---
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Seleziona Voce:"))

        self.voice_combo = QComboBox()
        controls_layout.addWidget(self.voice_combo)

        self.btn_insert_marker = QPushButton("Inserisci Marker Voce")
        self.btn_insert_marker.clicked.connect(self.insert_voice_marker)
        controls_layout.addWidget(self.btn_insert_marker)

        layout.addLayout(controls_layout)

        # --- Area di Testo ---
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText(
            "Scrivi qui il dialogo...\n\nEsempio:\n[voice=Microsoft Lucia Desktop]\nCiao!\n[voice=Microsoft Elsa Desktop]\nCome va?"
        )
        layout.addWidget(self.text_edit)

        # --- Pulsante Generazione ---
        self.btn_generate = QPushButton("Genera Dialogo (Audio)")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_generate.clicked.connect(self.generate_dialogue)
        layout.addWidget(self.btn_generate)

        self.setLayout(layout)

        self.populate_voices()

    def populate_voices(self):
        self.voice_combo.clear()
        voices = self.tts_engine.get_voices()
        for v in voices:
            self.voice_combo.addItem(v['name'], v['id'])

    def insert_voice_marker(self):
        voice_id = self.voice_combo.currentData()
        if voice_id:
            marker = f"\n[voice={voice_id}]\n"
            self.text_edit.insertPlainText(marker)
            self.text_edit.setFocus()

    def generate_dialogue(self):
        text = self.text_edit.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Attenzione", "Inserisci del testo prima di generare.")
            return

        segments = self.parser.parse(text)
        if not segments:
            QMessageBox.warning(self, "Attenzione", "Nessun segmento valido trovato (hai usato i marker?)")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Seleziona cartella output")
        if not output_dir:
            return

        files = self.tts_engine.generate_dialogue(segments, output_dir)
        if files:
            QMessageBox.information(self, "Successo", f"Generati {len(files)} file audio in:\n{output_dir}")
        else:
            QMessageBox.critical(self, "Errore", "Errore nella generazione dell'audio.")
