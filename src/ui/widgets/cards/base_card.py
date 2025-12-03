from PySide6.QtWidgets import QFrame


class BaseCardWidget(QFrame):
    """
    Classe base astratta per le card,
    definisce struttura e stile comune
    """
    def __init__(self, width=160, height=180):
        super().__init__()
        self.setFixedSize(width, height)