'''
Adam Forestier
June 21, 2023
Takes in ingredients and returns recipe and image of recipe
'''

import openai
import re
import requests
import shutil

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

def save_img(img_response, file_name) -> int:
    '''
    arguments: response from api
    returns: status code
    description: save_img downloads the image that api has created
    '''
    img_url = img_response['data'][0]['url']
    img_results = requests.get(img_url, stream=True)
    if img_results.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(img_results.raw, f)
    else:
        print('ERROR LOADING IMAGE')
    return img_results.status_code

i = ['ground turkey', 'zucchini', 'tomatoes', 'rice']

response = openai.Completion.create(
    model='text-davinci-003',
    prompt=create_dish_prompt(ingredients=i),
    max_tokens=512,
    temperature=.7
)

# The recipe
recipe_text = response['choices'][0]['text']
print(recipe_text)

# get recipe title to generate photo
recipe_title = extract_recipe_title(recipe=recipe_text)

# Create image
img_response = openai.Image.create(
    prompt=recipe_title,
    n=1,
    size='256x256'
)

# Save image
save_img(img_response=img_response, file_name='recipe_photo.png')