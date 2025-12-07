from datetime import datetime
import math
import os

from mutagen.mp3 import MP3

from src.core.file_manager import FileManager


class MetadataExtractor:

    @staticmethod
    def extract_mp3_metadata(path: str):
        if not FileManager.check_file_exists(path):
            raise FileNotFoundError(f"File {path} non trovato.")
        elif not FileManager.check_file_extension(path, ".mp3"):
            raise ValueError(f"File {path} non è .mp3")

        audio = MP3(path)

        duration = audio.info.length
        minutes = math.floor(duration / 60)
        seconds = int(duration % 60)
        duration_str = f"{minutes}:{seconds:02d}"

        last_modified = datetime.fromtimestamp(os.path.getmtime(path))
        last_modified_str = last_modified.strftime("%d/%m/%Y %H:%M")

        return {
            "duration_seconds": duration,
            "duration_str": duration_str,
            "bitrate": audio.info.bitrate,
            "sample_rate": audio.info.sample_rate,
            "last_modified": last_modified,
            "last_modified_str": last_modified_str
        }