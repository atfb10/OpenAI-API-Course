'''
Adam Forestier
July 7, 2023
Description: Convert natural language, into a SQL query based upon table structure
'''

'''
Instructions
1. Create an OpenAI developer key
2. Put api key in system variables OR create hidden python file named 'key', and instantiate variable named key = {your key}
3. Install openai python library -> pip install openai
4. Change the constant 'DATABASE_TYPE' to your relational database type
5. OPTIONAL: change the name of the file the query is written to
6. Change directories to where you have the python file saved via Powershell
7. Run command: python write_query.py (Must have python3 installed with path enabled) 
'''

import openai

from key import key as key
openai.api_key = key

DATABASE_TYPE = 'Postgresql'
QUERY_FILE_NAME = 'query.txt'

def create_table_definition(table_name: str, col_names: list[str]) -> str:
    prompt =  f'### {DATABASE_TYPE} SQL table' + """, with its properties:
    #
    # {table}({columns})
    #
    """.format(table=table_name, columns = ','.join(col for col in col_names))
    return prompt

def define_table() -> tuple:

    table = input('Enter table name: ') 
    cols = input('Enter column names of your database. Seperate column names with commas and no space: ')
    col_list = cols.split(',')
    return (table, col_list)

def input_query_request() -> str:
    return input('Type the query you want written: ')

def combine_prompts() -> str:
    table, columns = define_table()
    query_request = input_query_request()
    table_definition = create_table_definition(table_name=table, col_names=columns)
    query_initializer_str = f'### A query to answer: {query_request}\nSELECT'
    return table_definition + query_initializer_str

def handle_response(api_response) -> str:
    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = f'SELECT {query}'
    return query

def write_query_to_txt(query: str) -> None:
    with open(QUERY_FILE_NAME, 'w') as write_file:
        write_file.write(query)
    return

prompt = combine_prompts()
response = openai.Completion.create(
    model='text-davinci-003',
    prompt=prompt,
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0,
    stop=['#', ';']
)
query = handle_response(api_response=response)
write_query_to_txt(query=query)