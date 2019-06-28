from scraper import secrets

import praw
from prawcore.exceptions import Redirect
from prawcore.exceptions import NotFound


class Scrapper:

    def __init__(self, controller):
        self._connection = praw.Reddit(client_id=secrets.client_id,
                                       client_secret=secrets.client_secret,
                                       user_agent=secrets.user_agent,
                                       username=secrets.username,
                                       password=secrets.password)
        self._upvote_threshold = None
        self._download_limit = None
        self._controller = controller

    def scrape_posts(self, selected_subreddits):
        for sub in selected_subreddits:
            subreddit = self._connection.subreddit(sub)
            try:
                subreddit = self._connection.subreddit(sub)

                print("Retrieving information from subreddit: " + sub)

                for post in subreddit.top(limit=15):
                    print(post.title, post.id)
                    self._controller.add_post(post)
            except Redirect:
                print("No such subreddit: " + sub)
                print("Moving to next...")
                continue
            except NotFound:
                print("No such subreddit exists: " + sub)
                continue
        self._controller.stop_refresh()

    def set_upvote_threshold(self, upvote_threshold):
        self._upvote_threshold = upvote_threshold

    def set_download_limit(self, download_limit):
        self._download_limit = download_limit
