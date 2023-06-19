'''
Adam Forestier
June 19, 2023
Description: Setup and test API key
'''

import openai
import os

from key import key as openai_key

openai.api_key = openai_key
response = openai.Completion.create(
    model='text-davinci-003',
    prompt='Give me two reasons to learn OpenAI API with Python',
    max_tokens=300
)
print(response)