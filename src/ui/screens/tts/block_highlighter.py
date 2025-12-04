from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

from src.core.tts_engine import tts_engine


class BlockHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Lista di voci valide
        self.valid_keywords = tts_engine().get_keywords()

        # Dizionario dei colori per voce
        # TODO: ESPANDERE E CAMBIARE IN BASE ALLA PALETTE
        self.voice_colors = {
            # esempio:
            "it-IT-DiegoNeural": QColor("#ad3d6f"),
            "it-IT-AlessioMultilingualNeural": QColor("#932191"),
            "it-IT-IsabellaNeural": QColor("#e17327"),
        }

        # Colore fallback se la voce è valida ma senza colore dedicato
        self.default_color = QColor("#ad3d6f")

        # Regex per marker solitario
        self.marker_regex = QRegularExpression(r"^\s*\[([^\]]+)\]\s*$")


        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        self.error_format.setUnderlineColor(QColor("#ff4444"))

    # ------------------------------------------------------------------------

    def highlightBlock(self, text):
        prev_state = self.previousBlockState()

        match = self.marker_regex.match(text)
        if match.hasMatch():
            # Se riga è un marker, evidenzia e cambia stato
            self._highlight_marker(match)
            return

        if prev_state > 0:
            # Siamo sotto un marker valido
            self._highlight_dialog_line(text, prev_state)
            self.setCurrentBlockState(prev_state)  # IMPORTANTISSIMO: mantieni stato!
            return

        if prev_state == -1:
            # Siamo sotto un marker invalido
            self.setFormat(0, len(text), self.error_format)
            self.setCurrentBlockState(prev_state)  # mantieni stato
            return

        # Se nessun marker precedente, nessuna evidenza e stato 0
        self.setCurrentBlockState(0)

    # ------------------------------------------------------------------------

    def _highlight_marker(self, match):
        """Colora il marker e aggiorna lo stato del blocco."""
        content = match.captured(1)
        start = match.capturedStart()
        end = match.capturedEnd()

        # Determina validità
        if self._is_voice_valid(content):
            color_index = self._store_voice_color(content)
            color = self._get_color_from_state(color_index)
            self.setCurrentBlockState(color_index)

            # formato del marker con colore dinamico
            marker_fmt = QTextCharFormat()
            marker_fmt.setBackground(color)
            self.setFormat(start, end - start, marker_fmt)

        else:
            # marker non valido
            self.setFormat(start, end - start, self.error_format)
            self.setCurrentBlockState(-1)

    # ------------------------------------------------------------------------

    def _highlight_dialog_line(self, text, state):
        """Applica sottolineatura puntinata del colore associato al marker valido."""
        color = self._get_color_from_state(state)

        dotted_fmt = QTextCharFormat()
        dotted_fmt.setUnderlineStyle(QTextCharFormat.DotLine)
        dotted_fmt.setUnderlineColor(color)

        self.setFormat(0, len(text), dotted_fmt)

    # ------------------------------------------------------------------------

    def _get_color_from_state(self, state):
        """Ritorna il colore associato allo stato (state > 0)."""
        index = state - 1
        return self._color_list[index]

    # ------------------------------------------------------------------------

    def _store_voice_color(self, voice_name):
        """Assegna un colore alla voce e ritorna il suo indice per lo stato."""
        # Se non esiste già un colore, usa default
        color = self.voice_colors.get(voice_name, self.default_color)

        # Se non abbiamo già questa voce nella lista interna, la aggiungiamo
        if not hasattr(self, "_color_list"):
            self._color_list = []

        if color not in self._color_list:
            self._color_list.append(color)

        # restituisce indice + 1 (stato > 0)
        return self._color_list.index(color) + 1

    # ------------------------------------------------------------------------

    def _is_voice_valid(self, text):
        """Controlla se il contenuto del marker è una keyword valida."""
        return any(kw in text for kw in self.valid_keywords)
