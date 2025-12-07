from PySide6.QtWidgets import QMessageBox


class Popup:
    @staticmethod
    def delete_file_popup(parent, file_path: str):
        confirm = QMessageBox.question(
            parent,
            "Conferma Eliminazione",
            f"Vuoi davvero eliminare '{file_path}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        return confirm == QMessageBox.Yes