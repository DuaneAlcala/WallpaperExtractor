import secrets

import praw

reddit_connection = praw.Reddit(client_id=secrets.client_id,
                                client_secret=secrets.client_secret,
                                user_agent=secrets.user_agent,
                                username=secrets.username,
                                password=secrets.password)

subreddit = reddit_connection.subreddit('MostBeautiful')
top = subreddit.top(limit=10)

for post in subreddit.top(limit=10):
    print(post.title, post.id)
