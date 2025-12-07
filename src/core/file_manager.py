import os
import json

# TODO: Rendi questa classe staticaaa
class FileManager:
    def __init__(self, library_path):
        self.library_path = library_path
        os.makedirs(self.library_path, exist_ok=True)

    def sanitize_filename(self, filename):
        safe = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).strip()
        return safe if safe else "dialogo_senza_nome"

    def get_audio_path(self, filename):
        return os.path.join(self.library_path, f"{filename}.mp3")

    def get_json_path(self, filename):
        return os.path.join(self.library_path, f"{filename}.json")

    @staticmethod
    def check_file_exists(path):
        return os.path.exists(path)

    @staticmethod
    def check_file_extension(path, extension):
        return path.lower().endswith(extension)

    @staticmethod
    def delete_file(path):
        try:
            os.remove(path)
            json_path = os.path.splitext(path)[0] + ".json"
            if os.path.exists(json_path):
                os.remove(json_path)
        except Exception as e:
            # TODO: non fare un print...
            print("Eh vabbè")

    def save_project_json(self, filename, data):
        json_path = self.get_json_path(filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
