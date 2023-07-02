'''
Adam Forestier
July 2, 2023
Takes Python file, for each function creates docstring, returns python file that contains docstrings for each function
'''

import openai
import inspect
from pathlib import Path

import test_functions
from key import key as openai_key

openai.api_key = openai_key

def docstring_prompt(code: str) -> str:
    prompt = f'{code}\n # A high quality Python docstring of the above Python function:\n \"\"\"'
    return prompt

def merge_docstring_and_function(function_string, docstring):
    split_func = function_string.split('\n')
    first_p, second_p = split_func[0], split_func[1:]
    merged_function = first_p+'\n    """'+docstring+'    """'+'\n'.join(second_p)
    return merged_function

def get_all_functions(module):
    return [mem for mem in inspect.getmembers(module, inspect.isfunction) if mem[1].__module__ == module.__name__]

def get_openai_completion(prompt):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt = prompt,
        temperature = 0,
        max_tokens = 100,
        top_p = 1.0,
        stop = ["\"\"\""]
    )
    return response['choices'][0]['text']

if __name__ == "__main__":
    functions_to_prompt = test_functions
    all_funcs = get_all_functions(test_functions)
    functions_with_prompts = []
    
    for func in all_funcs:
        code = inspect.getsource(func[1])
        prompt = docstring_prompt(code=code)
        response = get_openai_completion(prompt=prompt)
        
        merged_code = merge_docstring_and_function(function_string=code, docstring=response)
        functions_with_prompts.append(merged_code)

    functions_to_prompt_name = Path(functions_to_prompt.__file__).stem
    with open(f"{functions_to_prompt_name}_withdocstring.py", "w") as f:
        f.write("\n\n".join(functions_with_prompts))