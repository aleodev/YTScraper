from pathlib import Path

FORMATS = {
    "audio": [
        "MP3",
        "WAV",
        "AAC",
        "FLAC",
        "OGG",
    ],
    "video": [
        "MP4",
        "FLV",
        "WMV",
        "MOV",
        "AVI",
    ],
}
CODECS = {"ogg": "vorbis"}
VIDEO_QUALITY_MAP = {"Low": "480", "Medium": "720", "High": "1080"}
AUDIO_QUALITY_MAP = {"Low": "128", "Medium": "192", "High": "320"}
QUALITY_LABEL_MAP = {"Low": "(LQ)", "Medium": "(MQ)", "High": "(HQ)"}
ROOT_DIR = Path.cwd()
CONFIG_PATH = Path.cwd() / "config.ini"
TEMP_PATH = Path.cwd() / "temp"
THEME_COLORS = {  # old alpha == 153
    "color": (0, 183, 113, 153),
    "light": (0, 151, 93, 153),
    "dark": (0, 151, 93, 153),
    "disabled": (0, 0, 0, 0),
}
