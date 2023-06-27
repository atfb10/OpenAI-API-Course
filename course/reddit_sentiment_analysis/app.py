'''
Adam Forestier
June 27, 2023
Determines sentiment of Reddit Post
'''

import openai
import praw
import requests

from key import key as openai_key
from key import (
    client_id,
    client_secret
)

# API key
openai.api_key = openai_key

# Reddit
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent='sentiment analysis test'
)
sub_stocks = reddit.subreddit("stocks")

def get_titles_and_comments(sub_r='stocks', limit=6, num_comments=3, skip_pinned=2) -> dict:
    '''
    args: user defined subreddit, number of categories, number of comments by category, and skip the top 2 comments by default because they are pinned comments
    returns:
    description: get_titles_and_comments gets all titles and comments by subreddit
    '''
    subreddit = reddit.subreddit(sub_r)
    title_and_comments = {}

    for counter, post in enumerate(subreddit.hot(limit=limit)):
        if counter < skip_pinned:
            continue

        counter += (1-skip_pinned)

        title_and_comments[counter] = ""
        submission = reddit.submission(post.id)
        title = post.title
        title_and_comments[counter] += 'Title: ' + title + '\n'
        title_and_comments[counter] += 'Comments: \n\n'

        comment_counter = 0
        for comment in submission.comments:
            if not comment.body == ['deleted']:
                title_and_comments[counter] += comment.body + '\n'
                comment_counter += 1
            if comment_counter == num_comments:
                break

    return title_and_comments


def create_prompt(title_and_comments: str) -> str:
    '''
    arguments: single value from title and comments dictionary
    returns: prompt
    description: create_prompt returns a prompt to feed to openai api
    '''
    task = 'Return the stock ticker or company name mentioned in the following title and comments. Classify the sentiment around the compnay as positive, negative, or neutral. If no ticker company is mentioned, write: \'No Company Mentioned\': \n\n'
    return task + title_and_comments


# Get title and comments dictionary
t_and_c = get_titles_and_comments()

# Perform analysis for each subreddit and its comments
for key, title_with_comments in t_and_c.items():
    prompt = create_prompt(title_with_comments)
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=256,
        temperature=0,
        top_p=1.0
    )
    print(title_with_comments)
    print(f"Sentiment Report from OpenAi: {response['choices'][0]['text']}")
    print('--------------------------------------------------------------------------------')