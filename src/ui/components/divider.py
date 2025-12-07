from PySide6.QtWidgets import QFrame


class Divider(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)  # divisore orizzontale
        self.setFrameShadow(QFrame.Sunken)  # opzionale
        self.setFixedHeight(1)

        self.setProperty("class", "divider")