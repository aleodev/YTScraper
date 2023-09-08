from pytube import YouTube
from moviepy.editor import VideoFileClip

# Define URL
video_url = "https://www.youtube.com/watch?v=SmgGO_wgh6I"

# Define the output directory for downloaded and converted files
download_dir = ""
output_dir = "output/"

# Create YT object
yt = YouTube(video_url)

# Define ITAG quality & download
stream = yt.streams.get_by_itag(22)
downloaded_video_path = stream.download(output_path=download_dir)

# Convert video
video_clip = VideoFileClip(downloaded_video_path)
mp3_output_path = output_dir + "video1.mp3"
video_clip.audio.write_audiofile(mp3_output_path)
