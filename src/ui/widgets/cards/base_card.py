from PySide6.QtWidgets import QFrame


class BaseCardWidget(QFrame):
    """
    Classe base astratta per le card,
    definisce struttura e stile comune
    """
    def __init__(self, width=160, height=180):
        super().__init__()
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 15px;
                border: 1px solid #E5E5E5;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)