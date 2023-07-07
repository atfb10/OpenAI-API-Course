def combine_prompts() -> str:
    """
This function combines the output of three other functions to create a query prompt for a user.

Parameters:
    None

Returns:
    str: A string containing a query prompt for the user.

    """    table, columns = define_table()
    query_request = input_query_request()
    table_definition = create_table_definition(table_name=table, col_names=columns)
    query_initializer_str = f'### A query to answer: {query_request}\nSELECT'
    return table_definition + query_initializer_str


def create_table_definition(table_name: str, col_names: list[str]) -> str:
    """
    Creates a table definition for a given table name and list of column names.
    
    Parameters:
    table_name (str): The name of the table.
    col_names (list[str]): A list of strings representing the column names.
    
    Returns:
    str: A string representing the table definition.
     """    prompt =  f'### {DATABASE_TYPE} SQL table' + """, with its properties:
    #
    # {table}({columns})
    #
    """.format(table=table_name, columns = ','.join(col for col in col_names))
    return prompt


def define_table() -> tuple:
    """
This function defines a table and its columns.

Parameters:
    None

Returns:
    tuple: A tuple containing the table name and a list of column names.

Example:
    define_table() -> ('table_name', ['column1', 'column2', 'column3'])
     """
    table = input('Enter table name: ') 
    cols = input('Enter column names of your database. Seperate column names with commas and no space: ')
    col_list = cols.split(',')
    return (table, col_list)


def handle_response(api_response) -> str:
    """
This function takes an API response as an argument and returns a string.

The function checks if the response starts with a space and if so, adds the string 'SELECT' to the beginning of the response.

Args:
    api_response (dict): The API response to be handled.

Returns:
    str: The modified API response.
     """    query = response['choices'][0]['text']
    if query.startswith(' '):
        query = f'SELECT {query}'
    return query


def input_query_request() -> str:
    """
This function prompts the user to input a query they would like written.

Parameters:
    None

Returns:
    str: The query the user has inputted.
     """    return input('Type the query you want written: ')


def write_query_to_txt(query: str) -> None:
    """
 Writes a given query to a text file.
 
 Parameters:
 query (str): The query to be written to the text file.
 
 Returns:
 None
 
     """    with open(QUERY_FILE_NAME, 'w') as write_file:
        write_file.write(query)
    return
