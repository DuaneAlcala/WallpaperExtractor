import os
import urllib.request
import pandas
from scraper import Scrapper
from urllib.error import HTTPError


class Controller:

    def __init__(self):
        self._scraper = Scrapper(self)
        self._posts = {"title": [], "score": [], "id": [], "url": [], "comms_num": [], "created": [], "body": []}
        self._path = os.path.dirname(os.path.realpath(__file__)) + "/images"
        self.count = 0

    def add_subreddit(self, subreddit):
        self._scraper.add_subreddit(subreddit)
        self._scraper.scrape_posts()

    def add_post(self, post):
        self._posts["title"].append(post.title)
        self._posts["score"].append(post.score)
        self._posts["id"].append(post.id)
        self._posts["url"].append(post.url)
        self._posts["comms_num"].append(post.num_comments)
        self._posts["created"].append(post.created)
        self._posts["body"].append(post.selftext)
        # print("retriving image")
        try:
            urllib.request.urlretrieve(post.url, self._path + "/image00" + str(self.count) + ".jpg")
            self.count = self.count + 1
        except HTTPError:
            print("Cannot download as it is not an image")

    def test(self):
        topics_data = pandas.DataFrame(self._posts)
        topics_data.to_csv('FILENAME.csv', index=False)