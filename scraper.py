from pytube.exceptions import VideoUnavailable
import dearpygui.dearpygui as dpg
import httpx
import yt_dlp

# Format list
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


# def progress_hook(d):


class Scraper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scraper, cls).__new__(cls)
        return cls._instance

    def show_msg(self, type, msg):
        dpg.configure_item("dialog", show=True, label=type)
        dpg.set_value(f"dialog_msg", msg)

    def verify_url(self):
        raw_url = dpg.get_value("url")

        # Fetch url
        try:
            r = httpx.get(raw_url)
            r.raise_for_status()
        except Exception:
            return False
        return raw_url

    def dl_youtube(self, url):
        print(f"download youtube {url}")

    # https://soundcloud.com/grinchn4abuck/grinchn4-all-onmy-own

    def dl_soundcloud(self, url):
        format = dpg.get_value("format")
        # Define options for youtube-dl
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "export/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format.lower(),
                    "preferredquality": "320",  # 128 for low quality
                }
            ],
            "noplaylist": True,
            "progress_hooks": [self.update_progress],
            "quiet": True,
        }

        # Set progress label
        dpg.configure_item("progress", overlay="Downloading ...")

        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            dpg.configure_item("progress", default_value=0, overlay="Finished!")
            # self.show_msg("Success", ydl.prepare_filename(info_dict))
            # original_file = ydl.prepare_filename(info_dict)

        # Determine the new file name
        # original_ext = os.path.splitext(original_file)[1]
        # base_name = os.path.splitext(original_file)[0]
        # new_file = f"{base_name}.{format.lower()}"

        # Rename the file if it exists
        # if os.path.exists(original_file):
        #     os.rename(original_file, new_file)
        #     self.show_msg("success", f"Successfully downloaded & exported {new_file}!")
        # else:
        #     self.show_msg("error", "The file was not found after download.")

    def run(self):
        # Check url validity
        verified_url = self.verify_url()

        if verified_url:
            # Check platform
            platform = dpg.get_value("platform").lower()

            if platform in verified_url:
                if platform == "youtube":
                    self.dl_youtube(verified_url)
                elif platform == "soundcloud":
                    self.dl_soundcloud(verified_url)
                else:
                    self.show_msg("Error", "The platform you selected isn't supported.")
            else:
                self.show_msg(
                    "Error",
                    "The link doesn't match the selected platform. Please check it.",
                )
        else:
            self.show_msg("Error", "You've entered an invalid url. Please try again.")

    def update_progress(self, d):
        status = d.get("status")
        total = d.get("total_bytes_estimate")
        downloaded = d.get("downloaded_bytes")
        progress = None
        if status == "downloading" and downloaded and total:
            progress = min(1.0, max(0.0, downloaded / total))
        elif status == "finished":
            progress = 1
            dpg.configure_item("progress", overlay="Processing ...")
        dpg.set_value("progress", progress)

    def convert(self):
        match format:
            case "MP4":
                print("TO MP4")
            case "MP3":
                print("TO MP3")
            case "WAV":
                print("TO FLV")
        print("SAVED")
