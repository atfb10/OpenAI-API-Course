'''
Adam Forestier
June 19, 2023
Description: Convert natural language, into a SQL query that can query a db
'''

'''
Notes: 
- WhisperAPI takes in an audio file and returns text
- Translates to Enlish
'''

import openai
import pandas as pd

from key import key as openai_key

# API key
openai.api_key = openai_key

# Read file and get transcript
audio_file = open("w_buffett.mp3", 'rb')
transcript = openai.Audio.transcripe("whisper-1", audio_file)

text = transcript['text']

# Summarize the text
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role':'system','content':'You are good at creating bullet point summaries and have knowledge of Warren Buffet'},
        {'role':'user','content':f'Summarize the following in bullet point form:\n{text}'}
    ]
)
result = response['choices'][0]['message']['content']

print(result)