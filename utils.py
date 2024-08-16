from pathlib import Path
import shutil


def prepare_temp_folder():
    temp_folder = Path.cwd() / "temp"
    if temp_folder.exists():
        shutil.rmtree(temp_folder)
    temp_folder.mkdir(parents=True, exist_ok=True)
