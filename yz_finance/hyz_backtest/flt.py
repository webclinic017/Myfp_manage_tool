from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from .metabase import MetaParams
from .utils.py3 import with_metaclass


__all__ = ['Filter']


class MetaFilter(MetaParams):
    pass


class Filter(with_metaclass(MetaParams, object)):

    _firsttime = True

    def __init__(self, data):
        pass

    def __call__(self, data):
        if self._firsttime:
            self.nextstart(data)
            self._firsttime = False

        self.next(data)

    def nextstart(self, data):
        pass

    def next(self, data):
        pass
