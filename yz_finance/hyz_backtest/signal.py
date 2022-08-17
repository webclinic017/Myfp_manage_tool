from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import hyz_backtest as bt

(

    SIGNAL_NONE,
    SIGNAL_LONGSHORT,
    SIGNAL_LONG,
    SIGNAL_LONG_INV,
    SIGNAL_LONG_ANY,
    SIGNAL_SHORT,
    SIGNAL_SHORT_INV,
    SIGNAL_SHORT_ANY,
    SIGNAL_LONGEXIT,
    SIGNAL_LONGEXIT_INV,
    SIGNAL_LONGEXIT_ANY,
    SIGNAL_SHORTEXIT,
    SIGNAL_SHORTEXIT_INV,
    SIGNAL_SHORTEXIT_ANY,

) = range(14)


SignalTypes = [
    SIGNAL_NONE,
    SIGNAL_LONGSHORT,
    SIGNAL_LONG, SIGNAL_LONG_INV, SIGNAL_LONG_ANY,
    SIGNAL_SHORT, SIGNAL_SHORT_INV, SIGNAL_SHORT_ANY,
    SIGNAL_LONGEXIT, SIGNAL_LONGEXIT_INV, SIGNAL_LONGEXIT_ANY,
    SIGNAL_SHORTEXIT, SIGNAL_SHORTEXIT_INV, SIGNAL_SHORTEXIT_ANY
]


class Signal(bt.Indicator):
    SignalTypes = SignalTypes

    lines = ('signal',)

    def __init__(self):
        self.lines.signal = self.data0.lines[0]
        self.plotinfo.plotmaster = getattr(self.data0, '_clock', self.data0)
