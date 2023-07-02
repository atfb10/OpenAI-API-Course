'''
Adam Forestier
July 2, 2023
Takes Python function and returns a docstring for it
'''

import openai
import re
import requests
import shutil

from key import key as openai_key

openai.api_key = openai_key

def docstring_prompt(code: str) -> str:
    prompt = f'{code}\n # A high quality Python docstring of the above Python function:\n \"\"\"'
    return prompt