import hashlib
from urllib.parse import urlparse, urljoin
from url import Url as UrlClass


def process_links(links):
    final_links = []
    for link in links:
        url_ob = UrlClass(url=link)
        parsed = urlparse(str(url_ob))
        if parsed.scheme is None:
            # must be a local link
            host = url_ob.host
            if not re.match(regex, str(url_ob)) is None:
                final_links.append(urljoin(host, str(url_ob)))
    return final_links


def hash_func(s):
    return hashlib.md5(bytes(s, 'utf8')).hexdigest()
