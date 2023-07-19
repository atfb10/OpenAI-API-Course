'''
Adam Forestier
July 19, 2023
'''

import json
import openai
import pandas as pd
import tiktoken

from key import key as openai_key

'''
NOTE: training your specific data is down in the terminal
'''

openai.api_key = openai_key

df = pd.read_csv('python_qa.csv')
questions, answers = df['Body'], df['Answer']

# Convert to json format for openai
qa_openai_format = [{"prompt": q, "completion": a} for q,a in zip(questions, answers)]

'''
NOTE: Creating json file for training the model. only using first 500 entries to save $$$
'''
dataset_size = 500
with open('example_training_data.json', 'w') as f:
    for entry in qa_openai_format[:dataset_size]:
        f.write(json.dumps(entry))
        f.write('\n')

fine_tuned_model = "babbage:ft-pieran-training-2023-02-13-08-01-05"

response = openai.Completion.create(
    model=fine_tuned_model, # Poorer model, because cheaper and testing effectiveness of fine tuning
    prompt=qa_openai_format[4]['prompt'],
    max_tokens=250,
    temperature=0
)

result = response['choices'][0]['text']

'''
NOTE: Estimating costs
'''
# Function that returns number of tokens from a given string
def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name=encoding_name)
    return len(encoding.encode(string))

token_counter = 0
for prompt_completion in qa_openai_format:
    for prompt, completion in prompt_completion.items():
        token_counter += num_tokens_from_string(prompt, 'gpt2')
        token_counter += num_tokens_from_string(completion, 'gpt2')

# $.0006 per 1000 tokens (training) * 4 epochs
cost_to_train = .0006*4*token_counter/1000