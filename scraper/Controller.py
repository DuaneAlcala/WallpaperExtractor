import os
import urllib.request
import pandas
import queue
import sys
from interface.Gui import Gui
from scraper.Scraper import Scrapper
from urllib.error import HTTPError


class Controller:

    def __init__(self, root):
        self._scraper = Scrapper(self)
        self._posts = {"title": [], "score": [], "id": [], "url": [], "comms_num": [], "created": [], "body": []}
        self._path = os.path.dirname(sys.modules['__main__'].__file__) + "/images/"

        self._root = root
        self._message_queue = queue.Queue()
        self._gui = Gui(self, root, self._message_queue)

        self._subreddits = []

        self.count = 0

    def add_subreddit(self, subreddit_name):
        self._subreddits.append(subreddit_name)

    def remove_subreddit(self, subreddit_name):
        self._subreddits.remove(subreddit_name)

    def start_scrape(self):
        if len(self._subreddits) != 0:
            print("HERE")
            self._scraper.scrape_posts(self._subreddits)

    def add_post(self, post):
        self._posts["title"].append(post.title)
        self._posts["score"].append(post.score)
        self._posts["id"].append(post.id)
        self._posts["url"].append(post.url)
        self._posts["comms_num"].append(post.num_comments)
        self._posts["created"].append(post.created)
        self._posts["body"].append(post.selftext)
        try:
            urllib.request.urlretrieve(post.url, self._path + "image00" + str(self.count) + ".jpg")
            self.count = self.count + 1
        except HTTPError:
            print("Cannot download as it is not an image")

    def test(self):
        topics_data = pandas.DataFrame(self._posts)
        topics_data.to_csv('FILENAME.csv', index=False)
