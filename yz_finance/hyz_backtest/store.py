from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections

from hyz_backtest.metabase import MetaParams
from hyz_backtest.utils.py3 import with_metaclass


class MetaSingleton(MetaParams):
    '''Metaclass to make a metaclassed class a singleton'''
    def __init__(cls, name, bases, dct):
        super(MetaSingleton, cls).__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = (
                super(MetaSingleton, cls).__call__(*args, **kwargs))

        return cls._singleton


class Store(with_metaclass(MetaSingleton, object)):
    '''Base class for all Stores'''

    _started = False

    params = ()

    def getdata(self, *args, **kwargs):
        '''Returns ``DataCls`` with args, kwargs'''
        data = self.DataCls(*args, **kwargs)
        data._store = self
        return data

    @classmethod
    def getbroker(cls, *args, **kwargs):
        '''Returns broker with *args, **kwargs from registered ``BrokerCls``'''
        broker = cls.BrokerCls(*args, **kwargs)
        broker._store = cls
        return broker

    BrokerCls = None  # broker class will autoregister
    DataCls = None  # data class will auto register

    def start(self, data=None, broker=None):
        if not self._started:
            self._started = True
            self.notifs = collections.deque()
            self.datas = list()
            self.broker = None

        if data is not None:
            self._cerebro = self._env = data._env
            self.datas.append(data)

            if self.broker is not None:
                if hasattr(self.broker, 'data_started'):
                    self.broker.data_started(data)

        elif broker is not None:
            self.broker = broker

    def stop(self):
        pass

    def put_notification(self, msg, *args, **kwargs):
        self.notifs.append((msg, args, kwargs))

    def get_notifications(self):
        '''Return the pending "store" notifications'''
        self.notifs.append(None)  # put a mark / threads could still append
        return [x for x in iter(self.notifs.popleft, None)]
