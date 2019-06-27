from scraper import Scrapper


class Controller:

    def __init__(self):
        self._scraper = Scrapper()

    def add_subreddit(self, subreddit):
        self._scraper.add_subreddit(subreddit)
        self._scraper.scrape_posts()
