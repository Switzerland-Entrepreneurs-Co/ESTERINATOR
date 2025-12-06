import os

# Calcola la root del progetto (assumendo che config.py sia in src/)
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

# Percorsi assoluti
AUDIO_LIBRARY_PATH = os.path.join(PROJECT_ROOT, "audio_library")
RESOURCES_PATH = os.path.join(SRC_DIR, "resources")
ICONS_PATH = os.path.join(RESOURCES_PATH, "icons")
THEMES_PATH = os.path.join(RESOURCES_PATH, "qss")

# Assicura che le cartelle esistano
os.makedirs(AUDIO_LIBRARY_PATH, exist_ok=True)