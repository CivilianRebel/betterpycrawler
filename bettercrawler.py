import multiprocessing as mp
from database import TestDB as Database
from crawler import Crawler


class Controller:

    def __init__(self, nb_processes=1, nb_urls_per_process=10):
        self.db = Database(host='__control__')
        self.nb_processes = nb_processes
        self.nb_urls_per_process = nb_urls_per_process
        self.crawlers = []
        self.jobs = {}

    def run(self):
        for crawler_idx in range(self.nb_processes):
            key = next(self.db.host_generator())
            self.jobs[key] = self.db.get_url_list(self.nb_urls_per_process, key)
            c = Crawler(key, self.jobs[key])
            self.crawlers.append(c)

        [crawler.start() for crawler in self.crawlers]
        [crawler.join() for crawler in self.crawlers]


if __name__ == '__main__':
    control = Controller(1, 10)
    # got no url in db structure, lets see what happens
    control.run()
