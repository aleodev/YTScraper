import dearpygui.dearpygui as dpg
import httpx
import yt_dlp
from pathlib import Path
from utils import setup_temp
from constants import CODECS, FORMATS, AUDIO_QUALITY_MAP, VIDEO_QUALITY_MAP


class Scraper:
    def __init__(self):
        pass

    running = False

    @staticmethod
    def show_msg(type, msg):
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

    def download(self, url):
        # Retrieve requested format
        format = dpg.get_value("format").lower()
        quality = dpg.get_value("quality")
        codec = CODECS.get(format, format)
        # Prep & clean temp folder
        setup_temp()

        # Set progress label
        dpg.configure_item("progress", overlay="Downloading ...")

        # Define options for either audio or video
        if format.upper() in FORMATS["audio"]:
            kbps = AUDIO_QUALITY_MAP.get(quality, "best")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "temp/%(title)s.%(ext)s",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": codec,
                        "preferredquality": kbps,
                    }
                ],
                "noplaylist": True,
                "progress_hooks": [self.progress_hook],
                "quiet": True,
            }
        elif format.upper() in FORMATS["video"]:
            resolution = VIDEO_QUALITY_MAP.get(quality, "best")
            ydl_opts = {
                "format": f"bestvideo[height<={resolution}][ext={format}]+bestaudio/best",
                "outtmpl": f"temp/%(title)s.{format}",
                "noplaylist": True,
                "progress_hooks": [self.progress_hook],
                "quiet": True,
            }
        else:
            raise ValueError("Unsupported format selected.")

        # Download start
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as dlp:
                platform = dpg.get_value("platform").lower()

                # Process
                info_dict = dlp.extract_info(url, download=True)
                processed_path = Path(info_dict["requested_downloads"][0]["filepath"])
                # Extension
                extension = f".{format}"
                # Filename
                filename = (
                    processed_path.name
                    if processed_path.suffix == extension
                    else processed_path.stem + extension
                )
                # Fix multiple extension issue
                filename = Path(filename)
                filename = (
                    filename.with_suffix("") if len(filename.suffixes) > 1 else filename
                )

                # Export path TODO:(convert this to use config instead and default to export folder)
                export_dir = Path(dpg.get_value("output"))
                export_file_path = export_dir / platform / filename

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
        dpg.configure_item("download", enabled=False)

        # Check url validity
        verified_url = self.verify_url()

        if verified_url:
            # Check platform
            platform = dpg.get_value("platform").lower()
            if platform in verified_url:
                if platform in ("youtube", "soundcloud"):
                    self.download(verified_url)
                else:
                    self.show_msg("Error", "Unsupported platform selected.")
            else:
                self.show_msg(
                    "Error",
                    "Incorrect platform selected.",
                )
        else:
            self.show_msg("Error", "Invalid url.")

        # Run finished
        self.running = False
        dpg.configure_item("download", enabled=True)

    def progress_hook(self, d):
        status = d.get("status")
        total = d.get("total_bytes_estimate") or d.get("total_bytes")
        downloaded = d.get("downloaded_bytes")
        progress = None
        if status == "downloading" and downloaded and total:
            progress = min(1.0, max(0.0, downloaded / total))
        elif status == "finished":
            progress = 1
            dpg.configure_item("progress", overlay="Processing ...")

        dpg.set_value("progress", progress)
