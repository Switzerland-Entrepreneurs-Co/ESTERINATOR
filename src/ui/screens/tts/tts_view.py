from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLabel, QPushButton,
    QMessageBox, QInputDialog, QApplication
)

from src.ui.screens.tts.components.language_selector import LanguageSelector
from src.ui.screens.tts.components.voice_selector import VoiceSelector
from src.core.dialogue_parser import DialogueParser
from src.core.tts_engine import TTSEngine
from src.core.file_manager import FileManager

class TTSGeneratorView(QWidget):
    def __init__(self, library_path):
        super().__init__()
        self.library_path = library_path

        self.tts_engine = TTSEngine()
        self.parser = DialogueParser()
        self.file_manager = FileManager(library_path)

        self.init_ui()
        self.load_voices()

    def init_ui(self):
        layout = QVBoxLayout()

        lbl_info = QLabel("Generatore Dialoghi Neurali (Online)")
        lbl_info.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(lbl_info)

        controls_layout = QHBoxLayout()

        controls_layout.addWidget(QLabel("Lingua:"))
        self.language_combo = LanguageSelector()
        controls_layout.addWidget(self.language_combo)

        controls_layout.addWidget(QLabel("Voce:"))
        self.voice_combo = VoiceSelector()
        controls_layout.addWidget(self.voice_combo)

        self.btn_insert_marker = QPushButton("Inserisci Marker")
        self.btn_insert_marker.clicked.connect(self.insert_voice_marker)
        controls_layout.addWidget(self.btn_insert_marker)

        layout.addLayout(controls_layout)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText("Inserisci testo qui...")
        layout.addWidget(self.text_edit)

        self.btn_generate = QPushButton("Salva e Genera Dialogo")
        self.btn_generate.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_generate.clicked.connect(self.generate_dialogue)
        layout.addWidget(self.btn_generate)

        self.setLayout(layout)
        self.resize(600, 500)

        # Connetti cambio lingua
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)

    def load_voices(self):
        voices = self.tts_engine.get_voices()
        self.voice_combo.set_voices(voices)

        languages = set(v['id'][:2] for v in voices)
        self.language_combo.populate_languages(languages)

        # Seleziona italiano di default se possibile
        default_index = 0
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == "it":
                default_index = i
                break
        self.language_combo.setCurrentIndex(default_index)

        self.voice_combo.filter_by_language(self.language_combo.itemData(default_index))

    def on_language_changed(self, index):
        lang_code = self.language_combo.itemData(index)
        if lang_code:
            self.voice_combo.filter_by_language(lang_code)

    def insert_voice_marker(self):
        voice_id = self.voice_combo.currentData()
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

        filename, ok = QInputDialog.getText(self, "Salva Audio", "Nome del file (senza estensione):")
        if not ok or not filename:
            return

        safe_filename = self.file_manager.sanitize_filename(filename)
        full_path = self.file_manager.get_audio_path(safe_filename)

        if full_path and self._file_exists(full_path):
            reply = QMessageBox.question(
                self, "Sovrascrivi",
                f"Il file '{safe_filename}.mp3' esiste già. Vuoi sovrascriverlo?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.btn_generate.setText("Generazione in corso...")
        self.btn_generate.setEnabled(False)
        QApplication.processEvents()

        try:
            success = self.tts_engine.generate_dialogue(segments, full_path)
            if success:
                project_data = {
                    "text": text,
                    "version": "1.0"
                }
                try:
                    self.file_manager.save_project_json(safe_filename, project_data)
                except Exception as e:
                    print(f"Attenzione: impossibile salvare il file progetto: {e}")

                QMessageBox.information(self, "Fatto", f"Salvato in Libreria:\n{safe_filename}.mp3")
            else:
                QMessageBox.critical(self, "Errore", "Errore durante la generazione.")
        finally:
            self.btn_generate.setText("Salva e Genera Dialogo")
            self.btn_generate.setEnabled(True)

    def _file_exists(self, path):
        import os
        return os.path.exists(path)

    def set_editor_content(self, text):
        self.text_edit.setPlainText(text)