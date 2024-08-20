import dearpygui.dearpygui as dpg
import httpx
import yt_dlp
from pathlib import Path
from utils import setup_temp, sanitize_url, show_msg, set_gui_interaction
from constants import (
    CODECS,
    FORMATS,
    AUDIO_QUALITY_MAP,
    VIDEO_QUALITY_MAP,
    QUALITY_LABEL_MAP,
    TEMP_PATH,
)


class Digger:
    def __init__(self):
        pass

    running = False

    def verify_url(self):
        raw_url = dpg.get_value("url")
        # Check if URL passes platform url check
        if any(
            keyword in raw_url
            for keyword in ["youtube.com/watch?v=", "soundcloud.com/"]
        ):
            # If url passes platform url check, sanitized url
            sanitized_url = sanitize_url(raw_url)
            # Fetch url
            try:
                r = httpx.get(sanitized_url)
                r.raise_for_status()
                return sanitized_url
            except Exception:
                show_msg("Error", "Invalid url.")
                return False
        else:
            show_msg("Error", "Invalid url.")
            return False

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
                "outtmpl": "temp/%(id)s.%(ext)s",
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
                "outtmpl": f"temp/%(id)s.{format}",
                "noplaylist": True,
                "progress_hooks": [self.progress_hook],
                "quiet": True,
            }
        else:
            raise ValueError("Unsupported format selected.")

        # Download start
        try:
            # Get output dir from input
            output_dir_input = Path(dpg.get_value("output"))
            # Compare output dir with TEMP_PATH
            if Path(output_dir_input) == TEMP_PATH:
                raise Exception("The temp directory can't be used.")

            with yt_dlp.YoutubeDL(ydl_opts) as dlp:
                platform = dpg.get_value("platform").lower()
                custom_title = dpg.get_value("title").lower()

                # Process
                info_dict = dlp.extract_info(url, download=True)
                title = info_dict["title"]
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
                # Custom title
                custom_filename = filename.with_name(
                    f"{custom_title or title}{filename.suffix}"
                )

                # Separate files by platform if set in config
                separate = dpg.get_value("separate_platforms")

                # Output path TODO:(convert this to use config instead and default to export folder)
                output_dir = (
                    output_dir_input / platform if separate else output_dir_input
                )

                # Check if the directory exists, and create it if it doesn't
                output_dir.mkdir(parents=True, exist_ok=True)

                # Combine the output directory with the filename
                output_file_path = output_dir / custom_filename

                # Add quality label if set in config
                label_quality = dpg.get_value("label_quality")
                label = QUALITY_LABEL_MAP[quality]
                if label_quality:
                    output_file_path = output_file_path.with_name(
                        output_file_path.stem + f" {label}" + output_file_path.suffix
                    )

                # Check if processed file exists
                if processed_path.is_file():
                    try:
                        # Create output path if doesn't exist
                        output_file_path.parent.mkdir(parents=True, exist_ok=True)
                        overwrite = dpg.get_value("overwrite_files")

                        # Overwrite if set in config
                        if overwrite:
                            processed_path.replace(output_file_path)
                        else:
                            processed_path.rename(output_file_path)

                        # Print success message if successful
                        show_msg(
                            "success",
                            f"Successfully processed & exported {output_file_path}!",
                        )
                        dpg.configure_item(
                            "progress", default_value=0, overlay="Finished!"
                        )
                    except Exception as e:
                        # Print error message if any exception occurs
                        show_msg("Error", f"An error occurred: {e}")
                        dpg.configure_item(
                            "progress", default_value=0, overlay="Failed!"
                        )
                else:
                    # Print error message if the file does not exist
                    show_msg("Error", "Processed file does not exist.")
                    dpg.configure_item("progress", default_value=0, overlay="Failed!")

        except yt_dlp.DownloadError as e:
            # Handle specific yt_dlp download errors
            show_msg("Error", f"Download error: {e.msg}")
            dpg.configure_item("progress", default_value=0, overlay="Failed!")
        except Exception as e:
            # Handle general exceptions
            show_msg("Error", f"An error occurred: {e}")
            dpg.configure_item("progress", default_value=0, overlay="Failed!")

    def run(self):
        if dpg.get_value("url") == "":
            show_msg("Error", "No url specified.")
            return
        # Run started
        set_gui_interaction(False)
        self.running = True

        # Check url validity
        verified_url = self.verify_url()

        if verified_url:
            # Check platform
            selected_platform = dpg.get_value("platform").lower()
            if selected_platform in verified_url:
                if selected_platform in ("youtube", "soundcloud"):
                    self.download(verified_url)
                else:
                    show_msg("Error", "Unsupported platform selected.")
            else:
                show_msg(
                    "Error",
                    "Incorrect platform selected.",
                )
        # Run finished
        set_gui_interaction(True)
        self.running = False
        dpg.set_value("title", "")
