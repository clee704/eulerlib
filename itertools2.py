"""
    eulerlib.itertools2
    ~~~~~~~~~~~~~~~~~~~

    Iterators for efficient looping.

"""
from itertools import islice


class remember(object):

    def __init__(self, iterable):
        self._iterable = iterable
        self._seen = set()
        self._last = None

    def __iter__(self):
        return self

    def __next__(self):
        n = next(self._iterable)
        self._seen.add(n)
        self._last = n
        return n

    @property
    def last(self):
        return self._last

    def everseen(self, value):
        """Return *True* if the value matches one of all elements ever seen."""
        return value in self._seen


def pick(iterable, i):
    """Return the *i*-th item from the given iterater (indexes start from 0).
    Items before the item to be returned are discarded.

    """
    return next(islice(iterable, i, None))
