from pytube.exceptions import VideoUnavailable
import dearpygui.dearpygui as dpg
import httpx

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

    def show_error(self, msg):
        print(msg)

    def verify_url(self):
        raw_url = dpg.get_value("url")
        # Fetch
        try:
            r = httpx.get(raw_url)
            r.raise_for_status()
        except Exception as e:
            print(e)
            return False
        return raw_url

    def download_youtube(self, url):
        print(f"download youtube {url}")

    def download_soundcloud(self, url):
        print(f"download soundcloud {url}")

    def run(self):
        verified_url = self.verify_url()
        if verified_url:
            # Check platform
            platform = dpg.get_value("platform").lower()

            if platform in verified_url:
                if platform == "youtube":
                    self.download_youtube(verified_url)
                elif platform == "soundcloud":
                    self.download_soundcloud(verified_url)
                else:
                    self.show_error("The platform you selected isn't supported.")
            else:
                self.show_error(
                    "The link doesn't match the selected platform. Please check it."
                )

        else:
            self.show_error("You've entered an invalid url. Please try again.")

    def update_progress(self, progress):
        dpg.configure_item("progress", overlay=progress, default_value=progress)

    def convert(self):
        match format:
            case "MP4":
                print("TO MP4")
            case "MP3":
                print("TO MP3")
            case "WAV":
                print("TO FLV")
        print("SAVED")
