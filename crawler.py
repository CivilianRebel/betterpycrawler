import requests as web
import bs4 as bs
import multiprocessing
from url import UrlClass
import utils
from database import TestDB as Database


class Crawler(multiprocessing.Process):

    def __init__(self, host, url_list, *args, **kwargs):
        super(Crawler, self).__init__()
        self.crawler_id = host
        self.debug = kwargs.get('debug', False)
        self.url_list = url_list
        self.database = Database(host)

    def run(self):
        for url in self.url_list:
            url_ob = UrlClass(url=url)
            if self.database.is_url_fetched(url_ob):
                if self.debug:
                    print('somehow its already been fetched', url)
                continue
            response = web.get(str(url_ob))
            soup = bs.BeautifulSoup(response.text, 'lxml')
            body = soup.body.text
            self.database.url_fetched(url_ob, body)
            links = [link for link in body.find_all('a')]
            links = [link.get('href') for link in links]
            links = utils.process_links(links)
            [self.database.new_url(link) for link in links]
