import sys
from PySide6.QtWidgets import QApplication
from src.ui.screens.main_window import MainWindow
from src.ui.theme_loader import ThemeLoader

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Applichiamo lo stile
    loader = ThemeLoader()
    css = loader.load("src/resources/qss/dark.qss")
    app.setStyleSheet(css)

    # Pre-caricamento di risorse prima di lanciare l'applicazione
    

    window = MainWindow()
    window.show()
    sys.exit(app.exec())