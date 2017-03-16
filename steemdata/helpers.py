import time

from funcy.decorators import contextmanager
from funcy.flow import decorator
from werkzeug.contrib.cache import SimpleCache


@contextmanager
def timeit():
    t1 = time.time()
    yield
    print("Time Elapsed: %.2f" % (time.time() - t1))


@decorator
def simple_cache(func, cache_obj, timeout=3600):
    if type(cache_obj) is not SimpleCache:
        return func()
    name = "%s_%s_%s" % (func._func.__name__, func._args, func._kwargs)
    cache_value = cache_obj.get(name)
    if cache_value:
        return cache_value
    else:
        out = func()
        cache_obj.set(name, out, timeout=timeout)
        return out


def create_cache():
    return SimpleCache()
