import os
import os.path as path
import json
import requests as web
import bs4 as bs
import hashlib
import time
from url import Url as UrlClass
from exceptions import NotControllerClass
import pathlib

_CONTROL = '__control__'


class Database:

    def __init__(self, host='crawler_files', db_loc='crawler_files/'):
        if not db_loc:
            db_loc = ''
        elif not os.path.exists(db_loc):
            os.mkdir(db_loc)
        self.working_dir = os.path.join(db_loc, host)
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)

    def file(self, key):
        f = os.path.join(self.working_dir, key + '.data')
        return f

    def exists(self, k):
        key = self.file(k)
        if os.path.isfile(key):
            return True
        elif not os.path.exists(key):
            return False

    def __setitem__(self, key, value):
        f = self.file(key)
        with open(f, 'w+') as file:
            json.dump(value, file)

    def __getitem__(self, key):
        f = self.file(key)
        if not self.exists(key):
            raise KeyError
        else:
            with open(f, 'r') as file:
                return json.load(file)


class TestDB:

    def __init__(self, host=_CONTROL):
        if host is _CONTROL:
            self.controller_mode = True
        else:
            self.controller_mode = False
        self.host_hash = host
        self.root = 'crawler_files\\'

    @property
    def host_folder(self):
        return path.join(self.root, self.host_hash)

    def _host_folder(self, host=None):
        return path.join(self.root, self.host_hash if host is None else host)

    def set_host(self, hashed_host):
        self.host_hash = hashed_host

    def get_folder(self, url):
        """
        Gets folder path of url
        :type url: Url
        :param url: MD5 hash of url for folder path
        :return: relative path to url folder
        """
        folder = path.join(self.root, self.host_hash, url.url_hash)
        return folder

    def get_html_path(self, url, folder=None):
        """
        Gets the path to the html file(if it exists) of url
        :type folder: str
        :type url: Url
        :param url: url to get the html path for
        :param folder: optional folder of host hash
        :return: path to html file of url
        """
        return path.join(self.get_folder(url) if folder is None else folder, 'raw_html.data')

    def url_datafile_path(self, url, folder=None):
        return path.join(self.get_folder(url) if folder is None else folder, 'url_data.json')

    def is_url_fetched(self, url, folder=None):
        """
        check if the html file of url exists, if not then it has not been fetched
        :param folder: Optional folder string to reduce compute time, minimal impact
        :param url: url_hash to check
        :return: bool if its fetched
        """
        folder = self.get_folder(url) if folder is None else folder
        if path.exists(folder):
            if path.exists(self.get_html_path(url, folder=folder)):
                return True
            else:
                return False
        else:
            self.new_url(url)
            return False

    def url_folder_exists(self, url, folder=None):
        """
        does the url_hash folder exist?
        :type folder: str
        :type url: Url
        :param url: Url object to check
        :param folder: optional folder string to save compute, albeit minimal impact
        :return: bool True if it exists
        """
        path_exists = path.exists(self.get_folder(url) if folder is None else folder)
        return path_exists

    def new_url(self, url):
        """
        Create a new entry for url in data structure
        :type url: Url
        :param url: Url object of entry to create
        """
        folder = self.get_folder(url)
        if not self.url_folder_exists(url, folder=folder):
            os.mkdir(folder)
            self.init_url_json(folder, url)
            # this should be all we have to do

    def init_url_json(self, url, folder=None):
        """
        Create url entry(unfetched)
        :type folder: str
        :type url: Url
        :param url: Url object of entry to create
        :param folder: string of folder to initialize
        """
        entry = {
            'url': url.to_string(),
            'url_hash': url.url_hash,
            'host': url.host,
            'host_hash': url.host_hash,
            'time_found': time.time()
        }
        with open(self.url_datafile_path(url), 'w+') as f:
            json.dump(url.to_dict(), f)

    def count_hosts(self):
        """
        Count number of unique hosts in db
        :rtype: int
        :return: int number of hosts
        """
        if self.controller_mode:
            return len(next(os.walk(self.root))[1]) - 1
        else:
            print('Access Denied: Not Controller Class')
            return None

    def host_generator(self):
        if not self.controller_mode:
            raise NotControllerClass()
        p = pathlib.Path('crawler_files/')
        for _dir in p.glob('*'):
            yield str(_dir).split('\\')[1]

    def get_url_by_hash(self, url):
        """
        Get a url object from hash and host hash
        :param url: url hash to get
        """
        url_ob = None
        if self.url_folder_exists(url):
            url_data_path = self.url_datafile_path(url)
            if path.exists(url_data_path) and path.isfile(url_data_path):
                with open(url_data_path, 'r') as file:
                    temp = json.load(file)
                    url_ob = UrlClass(url=temp['url'],
                                      host=temp['host'])
        return url_ob

    def get_url_list(self, nb_urls, _host):
        """
        Get a list of urls by host_hash
        :param _host: hashed host
        :param nb_urls: number of urls to grab
        """
        url_list = []
        p = pathlib.Path(self._host_folder(_host))
        for d in p.glob('*'):
            if len(url_list) >= nb_urls:
                break
            url_path = str(d).split('/')[1]
            with open(url_path, 'r') as file:
                url_list.append(str(json.load(file)['url']))
        return url_list


if __name__ == '__main__':
    _url = 'https://getpocket.com/explore/item/the-hidden-meanings-behind-15-company-names'
    host_hash = hashlib.md5(bytes('getpocket.com', 'utf8')).hexdigest()
    url_hash = hashlib.md5(bytes(_url, 'utf8')).hexdigest()
    db = Database(host=host_hash)
    db.fetched(url_hash, html)
