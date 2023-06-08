# Import necessary libraries
# os for file path handling and directory creation
# sys for command line argument handling
# textwrap not used in this script, could be for future extension
import os
import sys
import textwrap

# Function to split text into tokens
def tokenize(text):
    """
    This is a very basic tokenizer and does not handle complex situations.
    For a more accurate count, you might want to use a library like NLTK or SpaCy.
    """
    # Splits text into tokens based on white space
    return text.split()

# Function to chunk text into smaller pieces
def chunk_text(file_name, max_tokens=4096):
    # Get the directory of the currently executing script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Create the full file path
    file_path = os.path.join(script_dir, file_name)

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the entire file content
        text = file.read()
        # Tokenize the text
        tokens = tokenize(text)

        # Initialize chunks and current_chunk
        chunks = []
        current_chunk = []

        # Iterate over tokens
        for token in tokens:
            # Append token to the current chunk
            current_chunk.append(token)
            # If the current chunk has reached the maximum tokens, add it to chunks and reset current_chunk
            if len(current_chunk) >= max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        # Return chunks
        return chunks

# Function to write chunks to files
def write_chunks_to_files(chunks, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over chunks
    for i, chunk in enumerate(chunks):
        # Write each chunk to a new file in the output directory
        with open(f"{output_dir}/chunk_{i+1}.txt", 'w') as file:
            file.write(chunk)

# If no command line arguments are given, print a message and exit
if len(sys.argv) < 2:
    print("Please provide the file name as a command line argument.")
    sys.exit(1)

# Get the file name from the first command line argument
file_name = sys.argv[1]
# Get the directory of the currently executing script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Set the output directory to the script directory
output_dir = script_dir

# Chunk the text from the input file
chunks = chunk_text(file_name)

# If there's more than one chunk
if len(chunks) > 1:
    # Delete the original file
    os.remove(os.path.join(script_dir, file_name))
    # Write chunks to new files in the output directory
    write_chunks_to_files(chunks, output_dir)
else:
    # If there's only one chunk, no changes are needed
    print("No changes needed.")
