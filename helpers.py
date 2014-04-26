import functools
from itertools import islice


def pick(iterable, i):
    """Return the *i*-th item from the given iterater (indexes start from 0).
    Items before the item to be returned are discarded.

    """
    return next(islice(iterable, i, None))


def memoize(f):
    cache = {}

    @functools.wraps(f)
    def memoized_func(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = f(*args)
            return cache[args]

    memoized_func.cache = cache
    return memoized_func
