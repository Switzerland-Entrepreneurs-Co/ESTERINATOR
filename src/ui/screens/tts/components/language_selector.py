import os
from PySide6.QtWidgets import QComboBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class LanguageSelector(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(32, 32))
        self.setMinimumWidth(50)
        self.icon_paths = self.load_icon_paths()

    def load_icon_paths(self):
        # Puoi estrarre la mappa da sopra
        return {
            # Italiano
            "it": "src/resources/icons/flags/it.png",  # Italia

            # Inglese (varie nazioni, tipicamente UK o USA)
            "en": "src/resources/icons/flags/en.png",  # English (UK/USA)

            # Francese
            "fr": "src/resources/icons/flags/fr.png",  # Francia

            # Spagnolo
            "es": "src/resources/icons/flags/es.png",  # Spagna

            # Tedesco
            "de": "src/resources/icons/flags/de.png",  # Germania

            # Portoghese (Portogallo)
            "pt": "src/resources/icons/flags/pt.png",  # Portogallo

            # Russo
            "ru": "src/resources/icons/flags/ru.png",  # Russia

            # Cinese (semplificato)
            "zh": "src/resources/icons/flags/zh.png",  # Cina

            # Giapponese
            "ja": "src/resources/icons/flags/ja.png",  # Giappone

            # Coreano
            "ko": "src/resources/icons/flags/ko.png",  # Corea del Sud

            # Olandese
            "nl": "src/resources/icons/flags/nl.png",  # Paesi Bassi

            # Polacco
            "pl": "src/resources/icons/flags/pl.png",  # Polonia

            # Svedese
            "sv": "src/resources/icons/flags/sv.png",  # Svezia

            # Danese
            "da": "src/resources/icons/flags/da.png",  # Danimarca

            # Norvegese
            "no": "src/resources/icons/flags/no.png",  # Norvegia

            # Finlandese
            "fi": "src/resources/icons/flags/fi.png",  # Finlandia

            # Turco
            "tr": "src/resources/icons/flags/tr.png",  # Turchia

            # Arabo (generico)
            "ar": "src/resources/icons/flags/ar.png",  # Paesi Arabi (bandiera arabo generica o specifica)

            # Hindi (India)
            "hi": "src/resources/icons/flags/hi.png",  # India (Hindi)

            # Indonesiano
            "id": "src/resources/icons/flags/id.png",  # Indonesia

            # Greco
            "el": "src/resources/icons/flags/el.png",  # Grecia

            # Ungherese
            "hu": "src/resources/icons/flags/hu.png",  # Ungheria

            # Ceco
            "cs": "src/resources/icons/flags/cs.png",  # Repubblica Ceca

            # Rumeno
            "ro": "src/resources/icons/flags/ro.png",  # Romania

            # Thai
            "th": "src/resources/icons/flags/th.png",  # Thailandia

            # Ebraico
            "he": "src/resources/icons/flags/he.png",  # Israele (ebraico)

            # Slovacco
            "sk": "src/resources/icons/flags/sk.png",  # Slovacchia

            # Bulgaro
            "bg": "src/resources/icons/flags/bg.png",  # Bulgaria

            # Ucraino
            "uk": "src/resources/icons/flags/uk.png",  # Ucraina

            # Malay
            "ms": "src/resources/icons/flags/ms.png",  # Malesia

            # Vietnamese
            "vi": "src/resources/icons/flags/vi.png",  # Vietnam

            # Catalano
            "ca": "src/resources/icons/flags/ca.png",  # Catalogna (Spagna)

            # Irish
            "ga": "src/resources/icons/flags/ga.png",  # Irlanda (Gaelico)

            # Basco
            "eu": "src/resources/icons/flags/eu.png",  # Paese Basco (Spagna)

            # Galiziano
            "gl": "src/resources/icons/flags/gl.png",  # Galizia (Spagna)
        }

    def get_flag_icon(self, lang_code):
        path = self.icon_paths.get(lang_code)
        if path and os.path.exists(path):
            return QIcon(path)
        return QIcon()

    def populate_languages(self, available_languages):
        self.clear()
        custom_order = ["it", "en", "es", "fr"]

        # Aggiungi in ordine custom
        for lang_code in custom_order:
            if lang_code in available_languages:
                icon = self.get_flag_icon(lang_code)
                self.addItem(icon, "", lang_code)

        # Altre lingue
        others = available_languages - set(custom_order)
        for lang_code in sorted(others):
            icon = self.get_flag_icon(lang_code)
            self.addItem(icon, "", lang_code)
