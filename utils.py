import hashlib
from urllib.parse import urlparse, urljoin


def process_links(links):
    final_links = []
    from url import UrlClass
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    for link in links:
        if link is None:
            continue
        url_ob = UrlClass(url=link)
        parsed = urlparse(str(url_ob))
        if parsed.scheme is None:
            # must be a local link
            host = url_ob.host
            if not re.match(regex, str(url_ob)) is None:
                final_links.append(UrlClass(url=urljoin(host, str(url_ob))))
        else:
            print(str(url_ob))
            final_links.append(url_ob)
    return final_links


def hash_func(s):
    return hashlib.md5(bytes(s, 'utf8')).hexdigest()
