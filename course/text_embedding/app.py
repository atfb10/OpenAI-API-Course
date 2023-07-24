'''
Adam Forestier
July 19, 2023

Text embedding - converts text to an N-dimensional vector

Once you have vectorized representations you have lots of potential use cases
    * Search: where results are ranked by relevance to query string
    * Clustering: Where text strings are grouped by similarity
    * Recommendations - where items w/ related text strings are recommended
    * Anomoly Detection - Where outliers w/ little relatedness are identified
    * Diversity Measurement - similarity distributions are measured
    * Classification - text strings are classified by their most similar label

Text embedding is a good substitute for fine tuning a model. It is far cheaper & you can store the vector embeddings locally
'''

import ast
import openai
import numpy as np
import pandas as pd
import tiktoken

from key import key as openai_key

openai.api_key = openai_key

'''
steps:
embed a query string to vector
perform a cosine similary between the query vector and all document vectors
choose most similar and inject context
'''

# Pricing
def num_tokens_from_string(string, encoding_name):
    encoding = tiktoken.get_encoding(encoding_name=encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_embedding(text):
    # Creates the vector
    result = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=text
    )
    return result['data'][0]['embedding']

def vector_similarity(vec1, vec2):
    return np.dot(np.array(vec1), np.array(vec2))

# Summary function
def summary(company, crunchbase_url, city, country, industry, investor_list):
    investors = "The investors in the company are"
    for investor in ast.literal_eval(investor_list):
        investors += f" {investor},"
    
    return f'{company} has headquarters in {city} in {country} and is in the field of {industry}. {investors}, More info at {crunchbase_url}'

def embed_prompt_lookup():
    question = input("what question do you have about a unicorn start-up? ")
    prompt_embedding = get_embedding(question)
    df['prompt_similarity'] = df['embedding'].apply(lambda vector: vector_similarity(vec1=vector, vec2=prompt_embedding))
    context = df.nlargest(1, 'prompt_similarity').iloc[0]['summary']
    prompt = f''' Only answer the question below if you have 100 percent certainty of the facts

                Context: {context}
                Q: {question}?
                A:'''
    
    response = openai.Completion.create(
    prompt=prompt,
    temperature=0,
    model='text-davinci-003',
    max_tokens=512
    )

    result = response['choices'][0]['text']
    return result

# Data
df = pd.read_csv('unicorns.csv')
df['summary'] = df.apply(lambda df: summary(df['Company'], df['Crunchbase Url'], df['City'], df['Country'], df['Industry'], df['Investors']), axis=1)
df['token_count'] = df['summary'].apply(lambda text:num_tokens_from_string(text, 'cl100k_base'))
total_cost = df['token_count'].sum() * .0004 / 1000 # .0004 per 1000 tokens USD
df['embedding'] = df['summary'].apply(get_embedding)
# df.to_csv('unicorns_with_embeddings.csv')

embed_prompt_lookup()