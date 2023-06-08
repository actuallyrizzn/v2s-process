import os
import openai
import time
import sys
from collections import OrderedDict

# Authenticate OpenAI API
openai.api_key = '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'

# Max tokens for a chunk
chunk_max = 4000

# Initialize list for summaries
summaries = []

# Spinner to show script is working
def spinner():
    while True:
        for cursor in '|/-\\':
            yield cursor

spin = spinner()

def spin_cursor():
    sys.stdout.write(next(spin))
    sys.stdout.flush()
    sys.stdout.write('\b')

# Get list of all files in current directory
files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')]

print("Checking files in the current directory...")

if len(files) > 1:
    print("Multiple chunk files found. Combining...")
    # Combine all chunk files into one
    with open('combined.txt', 'w') as outfile:
        for fname in files:
            with open(fname) as infile:
                outfile.write(infile.read())
    transcript_file = 'combined.txt'
else:
    print("Single transcript file found.")
    transcript_file = files[0]

print("Transcript file prepared.")

with open(transcript_file, 'r') as file:
    data = file.read()

print("Breaking transcript into chunks...")
chunks = [data[i:i+chunk_max] for i in range(0, len(data), chunk_max)]

print("Transcript broken into", len(chunks), "chunks.")

print("Generating summaries...")

for chunk in chunks:
    response = openai.Completion.create(
        engine="text-davinci-003",  # or your preferred engine
        prompt=f"Here is the transcribed text from a video discussion: \n\n{chunk}\n\n Could you please summarize the main topics or points of view presented by the speakers?",
        temperature=0.5,
        max_tokens=200
    )

    # Spin cursor while waiting for response
    while response == None:
        spin_cursor()
        time.sleep(0.1)
    
    summaries.append(response.choices[0].text.strip())

print("Summaries generated.")

print("Deduplicating summaries...")
summaries = list(OrderedDict.fromkeys(summaries))

print("Writing summaries to file...")
with open("summary.txt", 'w') as outfile:
    for summary in summaries:
        outfile.write(summary + '\n')

print("Summary file created.")

print("Cleaning up original files...")
for f in files:
    os.remove(f)

if os.path.exists("combined.txt"):
    os.remove("combined.txt")

print("Cleanup completed.")
