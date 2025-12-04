import re
from pathlib import Path

class AliasParser:
    def __init__(self):
        self.pattern = re.compile(r"\s*(.+?)\s*->\s*(.+)\s*")

    # Fa il parsing del file di mapping delle alias
    # voices contiene tutte le voci effettivamente esistenti
    #
    #
    # Se non dovesse esserci corrispondenza (eg l'utente mappa un alias a una voce inesistente)
    # l'alias viene ignorato
    def map_aliases(self, voices):
        # Crea file e cartella se non esistono
        folder = Path("config")
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / "alias_map.txt"
        # Se non esiste, crealo vuoto
        if not file_path.exists():
            file_path.touch()

        alias_to_voice = {}

        # Legge il file e crea l'associazione
        with (file_path.open("r")) as f:
            for line in f:
                m = self.pattern.match(line)
                if m:
                    alias = m.group(1)
                    voice = m.group(2)

                    if voice not in voices:
                        continue

                    alias_to_voice[alias] = voice

        return alias_to_voice