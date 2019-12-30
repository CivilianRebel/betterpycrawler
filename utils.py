import hashlib


def hash_func(s):
    return hashlib.md5(bytes(s, 'utf8')).hexdigest()
