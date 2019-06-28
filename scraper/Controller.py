import os
import urllib.request
import pandas
import queue
import sys
import threading
from interface.Gui import Gui
from scraper.Scraper import Scrapper
from urllib.error import HTTPError


class Controller:

    def __init__(self, root):
        self._scraper = Scrapper(self)
        self._posts = {"title": [], "score": [], "id": [], "url": [], "comms_num": [], "created": [], "body": []}
        self._path = os.path.dirname(sys.modules['__main__'].__file__) + "/images/"

        self._root = root
        self._images_queue = queue.Queue()
        self._gui = Gui(self, root, self._images_queue)

        self._subreddits = []

        self.count = 0
        self._do_refresh_flag = 0
        self._thread1 = threading.Thread(target=self.__scrape)

    def add_subreddit(self, subreddit_name):
        self._subreddits.append(subreddit_name)

    def remove_subreddit(self, subreddit_name):
        self._subreddits.remove(subreddit_name)

    def start_scrape(self):
        if len(self._subreddits) != 0:
            self._do_refresh_flag = 1
            self._refresh_call()
            self._thread1.start()

    def __scrape(self):
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
            image_name = self._path + "image00" + str(self.count) + ".jpg"
            urllib.request.urlretrieve(post.url, image_name)
            self._images_queue.put(image_name)
            self.count = self.count + 1
        except HTTPError:
            print("Cannot download as it is not an image")

    def _refresh_call(self):
        if self._do_refresh_flag == 1:
            self._gui.refresh_images()
            self._root.after(100, self._refresh_call)

    def stop_refresh(self):
        self._do_refresh_flag = 0
        self._gui.refresh_images()

    def test(self):
        topics_data = pandas.DataFrame(self._posts)
        topics_data.to_csv('FILENAME.csv', index=False)
