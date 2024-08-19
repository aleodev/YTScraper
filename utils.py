from pathlib import Path
import shutil
import configparser
from urllib.parse import urlparse
from constants import CONFIG_PATH, TEMP_PATH
import dearpygui.dearpygui as dpg


# App Utils
def setup_temp():
    # Clean temp and create if its deleted
    if TEMP_PATH.exists():
        shutil.rmtree(TEMP_PATH)
    TEMP_PATH.mkdir(parents=True, exist_ok=True)


def setup_config(section, default_config):
    # Setup config
    config = configparser.ConfigParser()

    # Config doesnt exist
    if not Path.is_file(CONFIG_PATH):
        config[section] = default_config
        with open(CONFIG_PATH, "w") as f:
            config.write(f)

    else:
        config.read(CONFIG_PATH)
        # Config exists without section
        if not config.has_section(section):
            config.add_section(section)
            for key, value in default_config.items():
                config.set(section, key, value)
            with open(CONFIG_PATH, "w") as f:
                config.write(f)


def sanitize_url(url):
    # Define the base prefixes
    base_prefixes = ["soundcloud.com", "youtube.com"]

    # Find which base prefix is in the URL
    for prefix in base_prefixes:
        if prefix in url:
            # Extract the part of the URL starting from the base prefix
            start_index = url.find(prefix)
            return f"https://www.{url[start_index:].lstrip('/')}"

    # If no base prefix matched, return the original URL
    return url


# GUI Utils
def show_msg(type, msg):
    dpg.configure_item("dialog", show=True, label=type)
    dpg.set_value(f"dialog_msg", msg)


def set_gui_interaction(enable):
    dpg.configure_item("url", readonly=not enable)
    dpg.configure_item("title", readonly=not enable)
    dpg.configure_item("output", readonly=not enable)
    dpg.configure_item("output_dialog_button", enabled=enable)
    dpg.configure_item("overwrite_files", enabled=enable)
    dpg.configure_item("separate_platforms", enabled=enable)
    dpg.configure_item("download", show=enable, enabled=enable)
