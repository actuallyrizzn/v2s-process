# Import the OpenAI library for API access and the requests library for making HTTP requests
import openai
import requests

# Set your OpenAI API key
openai.api_key = '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'

# Open the output.mp3 file in read-binary mode
with open('output.mp3', 'rb') as audio_file:
    # Call the OpenAI API's Audio.transcribe method to transcribe the audio file
    # The 'file' parameter is the audio file
    # The 'model' parameter specifies the model to use for transcription (in this case, 'whisper-1')
    # The 'response_format' parameter specifies the format of the response (in this case, 'text')
    # The 'language' parameter specifies the language of the audio (in this case, 'en' for English)
    response = openai.Audio.transcribe(
        file=audio_file,
        model='whisper-1',
        response_format='text',
        language='en'
    )

# Print the response from the API
print(response)
