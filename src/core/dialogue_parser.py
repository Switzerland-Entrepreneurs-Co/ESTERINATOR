import re

class DialogueParser:
    def __init__(self):
        # Riconosce [voice=qualcosa]
        self.marker_pattern = re.compile(r'\[(.*?)]', re.IGNORECASE)

    def parse(self, text):
        """
        Restituisce una lista di segmenti:v
        [{'voice': 'ID', 'text': 'contenuto'}, ...]
        """

        segments = []
        matches = list(self.marker_pattern.finditer(text))

        # Se non ci sono marker -> niente dialogo valido
        if not matches:
            return []

        for i, match in enumerate(matches):
            voice_id = match.group(1).strip()

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
