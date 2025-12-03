import os
import json

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

    def save_project_json(self, filename, data):
        json_path = self.get_json_path(filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
