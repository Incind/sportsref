import collections
import functools
import os
import time
import urlparse

import appdirs

__all__ = [
    'switchToDir',
    'cacheHTML',
]

def switchToDir(dirPath):
    """
    Decorator that switches to given directory before executing function, and
    then returning to orignal directory.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            orig_cwd = os.getcwd()
            os.chdir(dirPath)
            ret = func(*args, **kwargs)
            os.chdir(orig_cwd)
            return ret
        return wrapper

    return decorator

def cacheHTML(func):
    """Caches the HTML returned by the specified function `func`. Caches it in
    the user cache determined by the appdirs package.
    """

    CACHE_DIR = appdirs.user_cache_dir('pfr', 'mgoldberg')
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    @functools.wraps(func)
    def wrapper(url):
        parsed = urlparse.urlparse(url)
        relURL = parsed.path
        if parsed.query:
            relURL += '?' + parsed.query
        relURL = relURL.strip('/').replace('/', '__')
        fn = '{}/{}'.format(CACHE_DIR, relURL)

        # TODO: fix this problem?
        if len(fn) > 255:
            # filename is too long, just evaluate the function
            return func(url)#.encode('ascii', 'replace')
        
        # set time variables
        if os.path.isfile(fn):
            modtime = int(os.path.getmtime(fn))
            curtime = int(time.time())
        # if file found and it's been <= a month, read from file
        if os.path.isfile(fn) and curtime - modtime <= 30*24*60*60:
            with open(fn, 'r') as f:
                text = f.read()
            return text
        # otherwise, download html and cache it
        else:
            text = func(url)#.encode('ascii', 'replace')
            with open(fn, 'w+') as f:
                f.write(text)
            return text
    
    return wrapper

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        if (not isinstance(args, collections.Hashable)
                or not isinstance(kwargs, collections.Hashable)):
            # cannot hash the arguments, so evaluate and return
            return self.func(*args, **kwargs)
        if (args, kwargs) in self.cache:
            return self.cache[args, kwargs]
        else:
            value = self.func(*args, **kwargs)
            self.cache[args, kwargs] = value
            return value

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)
