import time
from utils import hash_func
from tldextract import extract


class Url:

    def __init__(self, url=None, host=None, *args, **kwargs):
        self.debug = kwargs.get('debug', False)
        if url is None:
            print(f'Url is None... Be sure to call url.set_url(url_str) to avoid errors')
        self.url = url
        if host is not None:
            print('This parameter is not implemented yet')

    def set_url(self, url_str):
        """
        Set object url field which is required
        :type url_str: str
        :param url_str: String containing url
        """
        self.url = url_str
        return self

    @property
    def host(self):
        return self.identify_host()

    def set_host(self, host):
        """
        Set host(example.com not including www)
        Optional but recommended if you intend to implement your own hostname
        resolution solution as the one I use is not ideal
        :type host: str
        :param host: String containing host to set to field variable 'host'
        """
        raise NotImplementedError

    def __str__(self):
        """
        String representation of url field
        :return: the string url as set by constructor or url.set_url()
        """
        return self.url

    @property
    def host_hash(self):
        """
        MD5 Hashed hostname
        :rtype: str
        :return: string hash of hostname
        """
        if self.host is None:
            if self.url is not None:
                self.identify_host()
            else:
                url_not_set_error()
        return hash_func(self.host)

    @property
    def url_hash(self):
        """
        MD5 Hashed representation of url
        :rtype: str
        :return: string containing hashed url
        """
        if self.url is None:
            url_not_set_error()
        else:
            return hash_func(self.url)

    def to_string(self):
        """
        Analog for __str__()
        :rtype: str
        :return: String representation of self.url
        """
        return str(self)

    def to_dict(self):
        """
        Convert this object and all relevant details to dictionary
        :rtype: dict
        :return: Dict containing relevant details. Keys: [url, url_hash, host, host_hash, time_found]
        """
        entry = {
            'url': str(self),
            'url_hash': self.url_hash,
            'host': self.host,
            'host_hash': self.host_hash,
            'time_found': time.time()
        }
        return entry

    def identify_host(self):
        tsd, td, tsu = extract(self.url)  # prints abc, hostname, com
        return td + '.' + tsu


def url_not_set_error():
    print('You forgot to set the URL. Use the url.set_url(url_here) function next time')
    raise AttributeError()
