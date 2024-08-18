from pathlib import Path
import shutil
import configparser
import os
from constants import CONFIG_PATH, TEMP_PATH


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
