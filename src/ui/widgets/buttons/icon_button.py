from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self, icon_path_normal: str, icon_path_hover: str = None,
                 tooltip: str = "", icon_size: QSize = QSize(24, 24),
                 text: str = "", parent=None):
        super().__init__(parent)
        self.icon_normal = QIcon(icon_path_normal)
        if self.icon_normal.isNull():
            print(f"Errore: icona non trovata {icon_path_normal}")

        self.icon_hover = QIcon(icon_path_hover) if icon_path_hover else self.icon_normal
        if icon_path_hover and self.icon_hover.isNull():
            print(f"Errore: icona hover non trovata {icon_path_hover}")

        self.setIcon(self.icon_normal)
        self.setIconSize(icon_size)
        self.setToolTip(tooltip)
        if text != "":
            self.setText(text)

        self.setProperty("class", "IconButton")

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)
