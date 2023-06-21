'''
Adam Forestier
June 21, 2023
Takes in ingredients and returns recipe and image of recipe
'''

import openai
import re

from key import key as openai_key

openai.api_key = openai_key

def create_dish_prompt(ingredients: list) -> str:
    '''
    arguments: list of ingredents
    returns: prompt to send to 
    descriptioN: create_dish_prompt creates prompt to send to api based on recipe list
    '''
    prompt = f"Create a detailed recipe based only on only the following ingredients. Here is the list of ingredents: {', '.join(ingredients)}. Additionally, assign a title starting with 'Recipe Title: ' to this recipe."
    return prompt

def extract_recipe_title(recipe: str) -> str:
    '''
    arguments: recipe text
    returns: the name of the recipe
    description: extract_recipe_title returns the title of the dish
    '''
    title = re.findall("^.*Recipe Title: .*$", recipe, re.MULTILINE)[0].strip().split("Recipe Title: ")[1]
    return title

i = ['butter', 'eggs', 'milk', 'bacon', 'havarti cheese', 'spinach', 'french bread']

response = openai.Completion.create(
    model='text-davinci-003',
    prompt=create_dish_prompt(ingredients=i),
    max_tokens=512,
    temperature=.7
)

recipe_text = response['choices'][0]['text']
print(extract_recipe_title(recipe=recipe_text))