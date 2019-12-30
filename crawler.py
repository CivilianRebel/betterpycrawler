import requests as web
import bs4 as bs
import multiprocessing
from database import TestDB as Database


class Crawler(multiprocessing.Process):

    def __init__(self, host, url_list):
        super(Crawler, self).__init__()
        self.crawler_id = host
        self.database = Database(host)

    def run(self):
