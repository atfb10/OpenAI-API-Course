'''
Adam Forestier
July 2, 2023
Takes Python function and returns a docstring for it
'''

import openai
import inspect

from key import key as openai_key

openai.api_key = openai_key

def hi(name: str) -> None:
    print(f'Hello {name}')
    return

def return_even(num_list: list) -> list:
    evens = []
    for i in return_even:
        if i // 2 == 0:
            evens.append(i)
    return evens

def docstring_prompt(code: str) -> str:
    prompt = f'{code}\n # A high quality Python docstring of the above Python function:\n \"\"\"'
    return prompt

def merge_docstring_and_function(og_func, docstring):
    function_str = inspect.getsource(og_func)
    split_func = function_str.split('\n')
    first_p, second_p = split_func[0], split_func[1:]
    merged_function = first_p+'\n    """'+docstring+'    """'+'\n'.join(second_p)
    return merged_function

prompt = docstring_prompt(inspect.getsource(return_even))
response = openai.Completion.create(
    model='text-davinci-003',
    prompt = prompt,
    temperature = 0,
    max_tokens = 100,
    top_p = 1.0,
    stop = ["\"\"\""]
)

docstring = response['choices'][0]['text']

merged = merge_docstring_and_function(og_func=return_even, docstring=docstring)
print(merged)