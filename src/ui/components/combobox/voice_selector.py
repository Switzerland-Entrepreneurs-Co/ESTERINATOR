from PySide6.QtWidgets import QComboBox

class VoiceSelector(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_voices = []

    def set_voices(self, voices):
        self.all_voices = voices

    def filter_by_language(self, lang_code):
        self.clear()
        filtered = [v for v in self.all_voices if v['id'].startswith(lang_code)]
        default_idx = 0
        for i, v in enumerate(filtered):
            self.addItem(v['name'], v['id'])
            if lang_code == "it" and "Diego" in v['name']:
                default_idx = i
        self.setCurrentIndex(default_idx)
