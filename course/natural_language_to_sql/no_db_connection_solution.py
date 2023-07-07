'''
Adam Forestier
July 7, 2023
Description: Convert natural language, into a SQL query based upon table structure
'''

import openai

from key import key as key

DATABASE_TYPE = 'Postgresql'

def create_table_definition(table_name: str, col_names: list[str]) -> str:
    prompt =  f'### {DATABASE_TYPE} SQL table' + """, with its properties:
    #
    # {table}({columns})
    #
    """.format(table=table_name, columns = ','.join(col for col in col_names))
    return prompt

def prompt_input():
    return input('Enter column names of your database. Seperate with columns with commas and no space')

p = create_table_definition(table_name='test', col_names=['cheese', 'food', 'bread'])
print(p)