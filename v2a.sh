#!/bin/bash

# Use ffmpeg to convert a .mp4 video file to a .mp3 audio file
# -i specifies the input file
# -c:a specifies the audio codec to use
# -b:a specifies the audio bitrate
# The final argument is the name of the output file
ffmpeg -i video.mp4 -c:a libmp3lame -b:a 32k output.mp3

# Define the name of the output file
filename="output.mp3"

# Check if the output file exists
# If it doesn't, print an error message and exit the script
if [ ! -f "$filename" ]; then
    echo "File $filename does not exist."
    exit 1
fi

# Use stat to get the size of the file in bytes
filesize=$(stat -c%s "$filename")

# Convert the file size from bytes to megabytes using bc, a command-line calculator
filesizeMB=$(echo "$filesize/1048576" | bc -l)

# Compare the file size with 25MB
# If the file is larger than 25MB, split it into smaller chunks
# If it isn't, print a message and do nothing else
if (( $(echo "$filesizeMB >= 25" | bc -l) )); then
    echo "File is too big for Whisper. Breaking it down into chunks."
    file="output.mp3"
    output="split"
    overlap=30
    chunk_size=25000 # in kbytes

    # Get the duration of the audio file in seconds
    duration=$(ffprobe -i "$file" -show_entries format=duration -v quiet -of csv="p=0")
    # Calculate the duration of each chunk
    chunk_duration=$(( ($chunk_size * 8) / 32 )) # duration in seconds, we divide by the bitrate (32 kbit/s)
    # Calculate the number of chunks
    n=$(( ($duration + $chunk_duration - 1) / $chunk_duration ))

    # Loop through each chunk
    for ((i=0; i<$n; i++)); do
        # Calculate the start time of the chunk
        start=$(( $i * $chunk_duration - $overlap > 0 ? $i * $chunk_duration - $overlap : 0 ))
        # Use ffmpeg to copy a chunk of the audio file to a new file
        ffmpeg -hide_banner -loglevel panic -i "$file" -c copy -ss $start -t $chunk_duration "${output}_$i.mp3"
    done

else
    echo "Nothing needs to be done at this stage. The file is already compressed enough."
fi

# Remove the original video file
rm video.mp4
