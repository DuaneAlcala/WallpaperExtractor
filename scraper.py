import secrets

import praw


class Scrapper:

    def __init__(self):
        self._connection = praw.Reddit(client_id=secrets.client_id,
                                       client_secret=secrets.client_secret,
                                       user_agent=secrets.user_agent,
                                       username=secrets.username,
                                       password=secrets.password)
        self._selected_subreddits = []
        self._upvote_threshold = None
        self._download_limit = None

    def scrape_posts(self):
        for sub in self._selected_subreddits:
            subreddit = self._connection.subreddit(sub)

            if subreddit is None:
                print("No such subreddit: " + sub)
                print("Moving to next...")
                continue

            print("Retrieving information from subreddit: " + sub)

            for post in subreddit.top(limit=10):
                print(post.title, post.id)

    def add_subreddit(self, subreddit):
        self._selected_subreddits.append(subreddit)

    def set_upvote_threshold(self, upvote_threshold):
        self._upvote_threshold = upvote_threshold

    def set_download_limit(self, download_limit):
        self._download_limit = download_limit

