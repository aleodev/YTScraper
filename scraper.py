from pytube.exceptions import VideoUnavailable
import dearpygui.dearpygui as dpg
import requests

# Format List
formats = {
    "audio": [
        "MP3",
        "WAV",
        "AAC",
        "FLAC",
        "OGG",
        "WMA",
    ],
    "video": [
        "MP4",
        "FLV",
        "WMV",
        "MOV",
        "AVI",
    ],
}


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

    def verify_url(self):
        # r = requests.get("https://www.youtube.com/watch?v=" + urlid)
        # if "Video unavailable" in r.text:
        #     self.show_error("bad link")  # SHOW MODAL WITH ERROR
        # else:
        #     print("good")
        return None

    def download(self):
        url = self.verify_url()
        if url is not None:

            # Download..
            print("download")

    def show_error(self, msg):
        print(msg)

    def update_progress(self, progress):
        dpg.configure_item("progress", overlay=progress, default_value=progress)

    def save(self):
        match format:
            case "MP4":
                print("TO MP4")
            case "MP3":
                print("TO MP3")
            case "WAV":
                print("TO FLV")
        print("SAVED")
