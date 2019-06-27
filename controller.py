import os
import urllib.request
from scraper import Scrapper


class Controller:

    def __init__(self):
        self._scraper = Scrapper(self)
        self._posts = {"title": [], "score": [], "id": [], "url": [], "comms_num": [], "created": [], "body": []}
        self._path = os.path.dirname(os.path.realpath(__file__)) + "/images"

    def add_subreddit(self, subreddit):
        self._scraper.add_subreddit(subreddit)
        self._scraper.scrape_posts()

    def add_post(self, post):
        self._posts["title"].append(post.title)
        self._posts["score"].append(post.score)
        self._posts["id"].append(post.id)
        self._posts["url"].append(post.url)
        self._posts["created"].append(post.created)
        print("retriving image")
        urllib.request.urlretrieve(post.url, self._path + "/image001.jpg")
