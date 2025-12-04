from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

from src.core.tts_engine import tts_engine


class BlockHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.valid_keywords = tts_engine().get_keywords()
        self.voice_colors = {
            "it-IT-DiegoNeural": QColor("#ad3d6f"),
            "it-IT-AlessioMultilingualNeural": QColor("#932191"),
            "it-IT-IsabellaNeural": QColor("#e17327"),
        }
        self.default_color = QColor("#ad3d6f")
        self.marker_regex = QRegularExpression(r"^\s*\[([^\]]+)\]\s*$")

        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        self.error_format.setUnderlineColor(QColor("#ff4444"))

    def refresh_keywords(self):
        """Ricarica le keyword e rifa l'highlight completo."""
        self.valid_keywords = tts_engine().get_keywords()
        self.rehighlight()

    def highlightBlock(self, text):
        prev_state = self.previousBlockState()

        match = self.marker_regex.match(text)
        if match.hasMatch():
            self._highlight_marker(match)
            return

        if prev_state > 0:
            self._highlight_dialog_line(text, prev_state)
            self.setCurrentBlockState(prev_state)
            return

        if prev_state == -1:
            self.setFormat(0, len(text), self.error_format)
            self.setCurrentBlockState(prev_state)
            return

        self.setCurrentBlockState(0)

    def _highlight_marker(self, match):
        content = match.captured(1).strip()
        start = match.capturedStart()
        end = match.capturedEnd()

        if self._is_voice_valid(content):
            color_index = self._store_voice_color(content)
            color = self._get_color_from_state(color_index)
            self.setCurrentBlockState(color_index)

            marker_fmt = QTextCharFormat()
            marker_fmt.setBackground(color)
            self.setFormat(start, end - start, marker_fmt)
        else:
            self.setFormat(start, end - start, self.error_format)
            self.setCurrentBlockState(-1)

    def _highlight_dialog_line(self, text, state):
        color = self._get_color_from_state(state)

        dotted_fmt = QTextCharFormat()
        dotted_fmt.setUnderlineStyle(QTextCharFormat.DotLine)
        dotted_fmt.setUnderlineColor(color)

        self.setFormat(0, len(text), dotted_fmt)

    def _get_color_from_state(self, state):
        index = state - 1
        return self._color_list[index]

    def _store_voice_color(self, voice_name):
        color = self.voice_colors.get(voice_name, self.default_color)

        if not hasattr(self, "_color_list"):
            self._color_list = []

        if color not in self._color_list:
            self._color_list.append(color)

        return self._color_list.index(color) + 1

    def _is_voice_valid(self, text):
        # Match esatto (strip per sicurezza)
        return text.strip() in self.valid_keywords
