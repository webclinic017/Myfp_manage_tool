from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from datetime import datetime

import hyz_backtest as bt
from hyz_backtest.utils.py3 import range


class MetaChainer(bt.DataBase.__class__):
    def __init__(cls, name, bases, dct):
        '''Class has already been created ... register'''
        # Initialize the class
        super(MetaChainer, cls).__init__(name, bases, dct)

    def donew(cls, *args, **kwargs):
        '''Intercept const. to copy timeframe/compression from 1st data'''
        # Create the object and set the params in place
        _obj, args, kwargs = super(MetaChainer, cls).donew(*args, **kwargs)

        if args:
            _obj.p.timeframe = args[0]._timeframe
            _obj.p.compression = args[0]._compression

        return _obj, args, kwargs


class Chainer(bt.with_metaclass(MetaChainer, bt.DataBase)):
    '''Class that chains datas'''

    def islive(self):
        '''Returns ``True`` to notify ``Cerebro`` that preloading and runonce
        should be deactivated'''
        return True

    def __init__(self, *args):
        self._args = args

    def start(self):
        super(Chainer, self).start()
        for d in self._args:
            d.setenvironment(self._env)
            d._start()

        # put the references in a separate list to have pops
        self._ds = list(self._args)
        self._d = self._ds.pop(0) if self._ds else None
        self._lastdt = datetime.min

    def stop(self):
        super(Chainer, self).stop()
        for d in self._args:
            d.stop()

    def get_notifications(self):
        return [] if self._d is None else self._d.get_notifications()

    def _gettz(self):
        '''To be overriden by subclasses which may auto-calculate the
        timezone'''
        if self._args:
            return self._args[0]._gettz()
        return bt.utils.date.Localizer(self.p.tz)

    def _load(self):
        while self._d is not None:
            if not self._d.next():  # no values from current data source
                self._d = self._ds.pop(0) if self._ds else None
                continue

            # Cannot deliver a date equal or less than an alredy delivered
            dt = self._d.datetime.datetime()
            if dt <= self._lastdt:
                continue

            self._lastdt = dt

            for i in range(self._d.size()):
                self.lines[i][0] = self._d.lines[i][0]

            return True

        # Out of the loop -> self._d is None, no data feed to return from
        return False
