import pytube.exceptions
from pytube import YouTube
import requests
import tempfile

# Format List
formats = [  # Video
    "MP4", "FLV", "WMV", "MOV", "AVI",
    # Audio
    "MP3", "WAV", "AAC", "FLAC", "OGG", "WMA"]


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

    def verifyID(self, urlid):
        r = requests.get("https://www.youtube.com/watch?v=" + urlid)
        print(r)
        if "Video unavailable" in r.text:
            self.url = ""
        else:
            print("BAD")
            self.url = "https://www.youtube.com/watch?v=" + urlid

    def failedDownload(self, reason):
        self.status = reason
        self.progress = 0
        self.inProgress = False

    def save(self):
        match format:
            case "MP4":
                print('TO MP4')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
            case "FLV":
                print('TO FLV')
        print("SAVED")
