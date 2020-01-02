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
        self.database = None

    def run(self):
        self.database = Database(host=self.crawler_id)
        print(f'{self.crawler_id}: {len(self.url_list)} urls')
        for url_ob in self.url_list:
            if self.database.is_url_fetched(url_ob):
                if self.debug:
                    print('somehow its already been fetched', url_ob)
                continue
            response = web.get(str(url_ob))
            soup = bs.BeautifulSoup(response.text, 'lxml')
            body = soup.body
            self.database.url_fetched(url_ob, body.text)
            links = [link.get('href') for link in body.find_all('a')]
            print(links)
            links = utils.process_links(links)
            [self.database.new_url(link) for link in links]
