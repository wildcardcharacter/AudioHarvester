import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"


DEFAULT_SETTINGS = {
    "output_dir": str(Path.home() / "Musik" / "AudioHarvester"),
    "format": "MP3",
    "quality": "320 kbps",
    "download_thumbnail": False,
    "history": [],
    "window_width": 650,
    "window_height": 450,
    }


def load_settings():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            indent=4,
            ensure_ascii=False
        )
