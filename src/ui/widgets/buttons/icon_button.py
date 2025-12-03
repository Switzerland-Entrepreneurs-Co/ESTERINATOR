from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self, icon_path: str, tooltip: str = "", icon_size: QSize = QSize(24, 24), color: str = None, text: str = "", parent=None):
        super().__init__(parent)
        icon = QIcon(icon_path)
        if icon.isNull():
            print(f"Errore: icona non trovata {icon_path}")
        self.setIcon(icon)
        self.setIconSize(icon_size)
        self.setToolTip(tooltip)
        if text != "":
            self.setText(text)
        # Stile base: niente bordo né sfondo
        style = "background-color: none; border: none;"
        if color:
            style += f"color: {color};"
        self.setStyleSheet(style)
