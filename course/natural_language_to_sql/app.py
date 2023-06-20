'''
Adam Forestier
June 19, 2023
Description: Convert natural language, into a SQL query that can query a db
'''

import openai
import pandas as pd

from sqlalchemy import (
    create_engine,
    text
)

from key import key as openai_key


def create_table_defintion(df:pd.DataFrame):
    '''
    arguments: dataframe representing a sql table
    returns: prompt containing table definition to give to OpenAi
    description: create_table_definition() takes in a dataframe and returns a prompt for OpenAI API to consume containing the SQL table structure

    NOTE to self: Sales is the name of the table. Column names replace the {} from the .format call
    '''
    prompt = """### sqlite SQL table, with its properties:
    #
    # Sales({})
    #
    """.format(",".join(str(col) for col in df.columns))

    return prompt

def prompt_input():
    '''
    arguments: none
    returns: user input
    description: take in user input
    '''
    return input("Enter the information you want: ")

def combine_prompts(df: pd.DataFrame, query_prompt: str):
    '''
    arguments: dataframe representing database table, request from user
    returns: string of prompt for api to complete
    descritpion: combine_prompts creates a single prompt to feed to the api. It concacenates the table definition and user input into a single string
    '''
    table_definition = create_table_defintion(df=df)
    query_init_string = f'### A query to answer: {query_prompt}\nSELECT'
    return table_definition + query_init_string

def handle_response(response):
    '''
    arguments: api response
    returns: SQL query statement
    description: handle_response 
    '''
    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = f'SELECT {query}'
    return query

def execute_query(db, query):
    '''
    arguments: database to query, query statement
    returns: nothing
    description: execute_query utilzes the api generate query and calls it on the specified database
    '''
    with db.connect() as conn:
        result = conn.execute(text(query))
    print(f'QUERY: {query}\n')
    print(str(result.all()))
    return

# Key
openai.api_key = openai_key

# Read in data
df = pd.read_csv('sales_data_sample.csv')

# Set up temp db in ram
temp_db = create_engine(
    'sqlite:///:memory:',
    echo=False
)

# Push df to db 
data = df.to_sql(name='Sales', con=temp_db)

# Implement solution
txt = prompt_input()
prompt = combine_prompts(df=df, query_prompt=txt)
response = openai.Completion.create(
    model='text-davinci-003', # Model used
    prompt=prompt, # Prompt for api to complete
    temperature=0, # "Creativivty"
    max_tokens=150,  # Max length of prompt and response
    top_p=1.0, # "Creativity" - adjust only this OR temperature. Here I have kept top_p as default
    frequency_penalty=0, # Penalty assigned for repeating. -2 is lowest. 2 is highest penalty
    presence_penalty=0, # Penalty assigned for choosing another word that already exists in response. -2 is lowest, 2 is highest penalty
    stop=['#', ';'] # Stop words/symbols. ; is end of sql query. # is a comment
)

query = handle_response(response=response)
execute_query(db=temp_db, query=query)