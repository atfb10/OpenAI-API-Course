'''
Adam Forestier
July 25, 2023
'''

import openai

from key import key as openai_key

openai.api_key = openai_key

class CreateBot:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = [{'role':'system', 'content':system_prompt}]

    def chat(self):
        question = ''
        while question != 'e' and question != 'E':
            print('To terminate type \'e\'')
            question = input("")
            print('\n')

            self.messages.append({'role':'user', 'content': question})
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages
            )
            
            content = response['choices'][0]['message']['content']
            print(content + '\n')
            self.messages.append({'role':'assistant', 'content':content})


python_tutor = CreateBot('You are an expert python teacher instructor')
python_tutor.chat()