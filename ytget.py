# Import necessary libraries
from pytube import YouTube
import os
import re
import sys
import logging
import argparse
import time

# Function to display download progress
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = bytes_downloaded / total_size
    download_speed = bytes_downloaded / (time.time() - start_time)
    remaining_bytes = bytes_remaining
    estimated_remaining_time = remaining_bytes / download_speed if download_speed > 0 else 0

    # Display progress
    sys.stdout.write("\r")
    sys.stdout.write(f"Progress: [{int(progress * 100):3}%] ")
    sys.stdout.write(f"Download Speed: {human_readable_size(download_speed)}/s ")
    sys.stdout.write(f"Remaining Time: {format_time(estimated_remaining_time)} ")
    sys.stdout.flush()

# Function to download a YouTube video
def download_video(url: str, destination_dir: str = None, output_filename: str = 'video.mp4') -> list[str]:
    if destination_dir is None:
        destination_dir = os.getcwd()
    suggestions = []
    if not re.match(r'^https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|live/)|youtu\.be/)([\w-]+)$', url):
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
            global start_time
            start_time = time.time()

            video.download(output_path=destination_dir, filename=output_filename)

            sys.stdout.write("\n")  # Move to a new line after download completes
            suggestions.append(f'Video saved to {os.path.join(destination_dir, output_filename)}')
    except pytube.exceptions.RegexMatchError:
        suggestions.append('Invalid URL format')
    except pytube.exceptions.VideoUnavailable:
        suggestions.append('The video is unavailable')
    except pytube.exceptions.LiveStreamError:
        suggestions.append('The video is a live stream')
    except pytube.exceptions.ExtractError:
        suggestions.append('Error occurred while extracting video information')
    except pytube.exceptions.PytubeError:
        suggestions.append('Error occurred while downloading the video')
    except Exception as e:
        suggestions.append(f'Unexpected error occurred: {e}')
    return suggestions

# Utility function to format time in HH:MM:SS format
def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Utility function to convert bytes to human-readable size
def human_readable_size(size: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"

# Create parser
parser = argparse.ArgumentParser(description='Download YouTube videos.')
parser.add_argument('url', help='YouTube video URL.')
parser.add_argument('-l', '--log', action='store_true', help='Enable logging.')
parser.add_argument('-f', '--filename', default='video.mp4', help='Output file name.')
args = parser.parse_args()

# Set up logging
if args.log:
    logging.basicConfig(level=logging.INFO)

suggestions = download_video(args.url, output_filename=args.filename)

for suggestion in suggestions:
    if args.log:
        logging.info(suggestion)
    else:
        print(suggestion)
