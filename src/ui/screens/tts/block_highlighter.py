from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PySide6.QtCore import QRegularExpression

class BlockHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Keyword valide per il primo []
        self.valid_keywords = ["ok", "ciao", "apple"]

        # Formati
        self.block_fmt = QTextCharFormat()              # highlight per singolo blocco
        self.block_fmt.setBackground(QColor(255, 230, 120, 160))

        self.dotted_fmt = QTextCharFormat()             # sottolineatura a puntini
        self.dotted_fmt.setUnderlineStyle(QTextCharFormat.DotLine)

        self.error_fmt = QTextCharFormat()              # wave underline rossa
        self.error_fmt.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        self.error_fmt.setUnderlineColor(QColor("#ff4444"))

        # Regex per trovare [ ... ]
        self.block_regex = QRegularExpression(r"\[([^\]]*)\]")

    def highlightBlock(self, text):
        # Lista dei match: (start, end, contenuto)
        blocks = []

        it = self.block_regex.globalMatch(text)
        while it.hasNext():
            m = it.next()
            start = m.capturedStart()
            end = m.capturedEnd()
            content = m.captured(1)
            blocks.append((start, end, content))

            # 🔵 Highlight base di ogni blocco
            self.setFormat(start, end - start, self.block_fmt)

        # Nessun blocco → niente da fare
        if not blocks:
            return

        # 🔴 Error checking sulla PRIMA coppia []
        first_content = blocks[0][2]
        if not self.is_valid(first_content):
            first_start, first_end, _ = blocks[0]
            self.setFormat(first_start, first_end - first_start, self.error_fmt)

        # 🔵 Sottolineatura puntinata tra blocchi consecutivi
        for i in range(len(blocks) - 1):
            first_end = blocks[i][1]
            second_start = blocks[i+1][0]

            if second_start > first_end:
                length = second_start - first_end
                # sottolineatura con lo stesso colore del primo blocco
                self.dotted_fmt.setUnderlineColor(QColor("#ffaa00"))
                self.setFormat(first_end, length, self.dotted_fmt)

    def is_valid(self, text):
        """
        Decide se il contenuto del primo [] è valido.
        Puoi personalizzarlo come ti serve.
        """
        for kw in self.valid_keywords:
            if kw in text:
                return True
        return False
