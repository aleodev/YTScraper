from pytube.exceptions import VideoUnavailable
import dearpygui.dearpygui as dpg
import httpx
import yt_dlp
from pathlib import Path
from utils import prepare_temp_folder

# Format list
formats = {
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
codecs = {"ogg": "vorbis"}


class Scraper:
    def __init__(self):
        pass

    running = False

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
        # Retrieve requested format
        format = dpg.get_value("format").lower()
        codec = codecs.get(format, format)

        # Prep & clean temp folder
        prepare_temp_folder()

        # Define options for youtube-dl
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "temp/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": codec,
                    "preferredquality": "320",  # 128 for low quality
                }
            ],
            "noplaylist": True,
            "progress_hooks": [self.progress_hook],
            "quiet": True,
        }

        # Set progress label
        dpg.configure_item("progress", overlay="Downloading ...")

        # Download the audio
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as dlp:
                # Needed vars
                platform = dpg.get_value("platform").lower()

                # Process
                info_dict = dlp.extract_info(url, download=True)
                processed_path = Path(info_dict["requested_downloads"][0]["filepath"])

                # Extension
                extension = f".{format}"

                # Export path TODO:(convert this to use config instead and default to export folder)
                export_file_path = (
                    Path.cwd() / "export" / platform / (processed_path.stem + extension)
                )

                # Check if processed file exists
                if processed_path.is_file():
                    try:
                        # Create export path if doesn't exist
                        export_file_path.parent.mkdir(parents=True, exist_ok=True)

                        if processed_path.suffix != extension:
                            # Rename the file only if necessary
                            processed_path.rename(export_file_path)
                        else:
                            # If no renaming needed, just move the file
                            processed_path.replace(export_file_path)

                        # Print success message if successful
                        self.show_msg(
                            "success",
                            f"Successfully processed & exported {export_file_path}!",
                        )
                        dpg.configure_item(
                            "progress", default_value=0, overlay="Finished!"
                        )
                    except Exception as e:
                        # Print error message if any exception occurs
                        self.show_msg("Error", f"An error occurred: {e}")
                        dpg.configure_item(
                            "progress", default_value=0, overlay="Failed!"
                        )
                else:
                    # Print error message if the file does not exist
                    self.show_msg("Error", "Processed file does not exist.")
                    dpg.configure_item("progress", default_value=0, overlay="Failed!")

        except yt_dlp.DownloadError as e:
            # Handle specific yt_dlp download errors
            self.show_msg("Error", f"Download error: {e}")
            dpg.configure_item("progress", default_value=0, overlay="Failed!")
        except Exception as e:
            # Handle general exceptions
            self.show_msg("Error", f"An error occurred: {e}")
            dpg.configure_item("progress", default_value=0, overlay="Failed!")

    def run(self):
        # Run started
        self.running = True

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

        # Run finished
        self.running = False

    def progress_hook(self, d):
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
