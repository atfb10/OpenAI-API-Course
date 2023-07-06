'''
Adam Forestier
July 6, 2023
Translates tet from 1 language to another
'''

import openai
import requests
import bs4
# import shutil

from key import key as openai_key

openai.api_key = openai_key

country_newspapers = {'Spain': 'https://elpais.com/', 'France':'https://www.lemonde.fr/'}

# Uppdate dictionary to have css class for article titles on each site
country_newspapers = {'Spain': ('https://elpais.com/', '.c_t'), 'France':('https://www.lemonde.fr/', '.article__title-label')}

def create_prompt():
    '''
    creates prompt for API from the first 3 articles on each newspaper site.
    args: none
    returns: prompt
    '''
    country = input('What country are you interested in for news? Spain or France: ')
    try:
        url, tag = country_newspapers[country]
    except:
        print('Must be Spain or France') 
        return
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, 'html.parser')
    country_headlines = ''
    for item in soup.select(tag)[:3]:
        country_headlines += item.getText() + '\n'
    prompt = 'Detect the langauge of the news headlines below, then translate a summary of the headlines to English in a conversational  \n'
    return prompt + country_headlines

prompt = create_prompt()

response = openai.Completion.create(
    model='text-davinci-003',
    prompt=prompt,
    temperature=.1,
    max_tokens=200
)

result = response['choices'][0]['text']

print(result)