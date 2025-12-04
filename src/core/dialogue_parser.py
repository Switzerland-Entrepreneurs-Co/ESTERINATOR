import re

from src.core.tts_engine import tts_engine


class DialogueParser:
    def __init__(self):
        # Riconosce [marker]
        self.marker_pattern = re.compile(r'^\s*\[(.*)]\s*$', re.MULTILINE)

    """
        Restituisce una lista di segmenti:
        [{'voice': 'ID', 'text': 'contenuto'}, ...]
    """
    def parse(self, text):
        segments = []
        print(text)
        matches = list(self.marker_pattern.finditer(text))

        # Se non ci sono marker -> niente dialogo valido
        if not matches:
            print("il problema è qui?")
            return []

        for i, match in enumerate(matches):
            # Trasformiamo il marker nel formato canonico
            # (ad esempio da alias a voce effettiva)
            # Se voice_id = None, il marker è invalido
            voice_id = tts_engine().canon_format( match.group(1).strip() )
            print(voice_id)
            if voice_id is None:
                return []

            # Inizio del testo dopo questo marker
            start = match.end()

            # Fine del testo:
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            # Estraggo contenuto
            content = text[start:end].strip()

            if content:
                segments.append({
                    "voice": voice_id,
                    "text": content
                })

        return segments
