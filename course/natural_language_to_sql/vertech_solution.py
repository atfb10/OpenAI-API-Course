'''
Adam Forestier
July 7, 2023
Description: Convert natural language, into a SQL query based upon table structure
'''

import openai

from key import key as key

DATABASE_TYPE = 'Postgresql'

def create_table_definition(col_names: list[str]) -> str:
    prompt =  + """, with its properties:
    #
    # Sales({})
    #
    """.format(','.join(col for col in col_names))
    return prompt

def prompt_input():
    return input('Enter column names of your database. Seperate with columns with commas and no space')