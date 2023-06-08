# Import necessary libraries
from pytube import YouTube
import os
import re
import sys

# Function to display download progress
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    liveprogress = (bytes_downloaded / total_size) * 100
    print("Downloading... {:.2f}%".format(liveprogress), end="\r")

# Function to download a YouTube video
def download_video(url: str, destination_dir: str = None) -> list[str]:
    if destination_dir is None:
        destination_dir = os.getcwd()
    suggestions = []
    if not re.match(r'^https?://(?:www\.)?youtube\.com/(?:watch\?v=|live/)([\w-]+)$', url):
        suggestions.append('Invalid URL format')
        return suggestions
    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
        url = f'https://www.youtube.com/watch?v={video_id}'
    if not os.path.isdir(os.path.abspath(destination_dir)):
        suggestions.append('Invalid destination directory')
        return suggestions
    try:
        youtube = YouTube(url, on_progress_callback=progress_function)
        video = youtube.streams.get_highest_resolution()
        if video is None:
            suggestions.append('No suitable stream found')
        else:
            video.download(output_path=destination_dir, filename='video.mp4')
            suggestions.append(f'Video saved to {os.path.join(destination_dir, "video.mp4")}')
    except Exception as e:
        suggestions.append(f'Error: {e}')
    return suggestions

if len(sys.argv) > 1:
    url = sys.argv[1]
    suggestions = download_video(url)
    for suggestion in suggestions:
        print(suggestion)
else:
    print('Please provide a YouTube video URL as a command line argument.')
