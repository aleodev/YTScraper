<div align="center">
<img style="width: 150px;"src="https://i.imgur.com/gqJkfDY.png"/>
  <h1><code>Track Digger</code></h1>

  <p>
    <strong>a sampler's <i>dream</i>
  </p>

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## Overview

Track Digger is a Python application that allows you to download and extract audio or video from YouTube and SoundCloud. It supports a wide selection of audio and video formats, provides custom output settings, and features a user-friendly graphical interface powered by Dear PyGui.


## Features

- **Supports multiple formats:** Easily choose between various audio and video formats.
- **Custom output settings:** Specify output directories, filenames, and more.
- **Platform separation:** Organize downloads into separate folders based on the platform (YouTube/SoundCloud).
- **Quality labeling:** Add quality labels (e.g., 'HQ') to filenames.
- **Overwrite controls:** Optionally overwrite existing files in the output directory.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install required packages:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Using the GUI:**
   - Enter the URL of the YouTube or SoundCloud link you wish to download.
   - Select your desired output format, quality, and destination folder.
   - Click 'DOWNLOAD' to start the process.

## Configuration

- **Output Folder:** You can set a default output folder. The application will save all downloads to this folder unless another folder is specified.
- **Separate Platforms:** If enabled, files are saved in separate folders based on the platform.
- **Overwrite Files:** If enabled, existing files with the same name will be overwritten.
- **Label Quality:** If enabled, quality labels (e.g., 'HQ') will be appended to filenames.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.