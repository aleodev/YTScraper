from pytube.exceptions import VideoUnavailable
import dearpygui.dearpygui as dpg
import requests

# Format List
formats = [  # Video
    "MP4",
    "FLV",
    "WMV",
    "MOV",
    "AVI",
    # Audio
    "MP3",
    "WAV",
    "AAC",
    "FLAC",
    "OGG",
    "WMA",
]


class Scraper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scraper, cls).__new__(cls)
        return cls._instance

    # Conversion Format
    format = ""
    # Download Status
    status = ""
    # Download Progress
    progress = 0
    # Currently Downloading
    inProgress = False
    # Temp File Path
    temp_file_path = ""
    # Video URL
    url = ""

    def verify_url(self, urlid):
        r = requests.get("https://www.youtube.com/watch?v=" + urlid)
        if "Video unavailable" in r.text:
            self.url = ""  # SHOW MODAL WITH ERROR
        else:
            # print("BAD")
            self.url = "https://www.youtube.com/watch?v=" + urlid

    def failedDownload(self, reason):
        self.status = reason
        self.progress = 0
        self.inProgress = False

    def download(self):
        url = verify_url(self.url)

    def update_progress(self, progress):
        dpg.configure_item("progress", overlay="LOL", default_value=1)

    def save(self):
        match format:
            case "MP4":
                print("TO MP4")
            case "MP3":
                print("TO MP3")
            case "WAV":
                print("TO FLV")
        print("SAVED")
