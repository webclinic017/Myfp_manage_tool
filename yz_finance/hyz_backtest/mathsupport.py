from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math


def average(x, bessel=False):
    '''
    Args:
      x: iterable with len

      oneless: (default ``False``) reduces the length of the array for the
                division.

    Returns:
      A float with the average of the elements of x
    '''
    return math.fsum(x) / (len(x) - bessel)


def variance(x, avgx=None):
    '''
    Args:
      x: iterable with len

    Returns:
      A list with the variance for each element of x
    '''
    if avgx is None:
        avgx = average(x)
    return [pow(y - avgx, 2.0) for y in x]


def standarddev(x, avgx=None, bessel=False):
    '''
    Args:
      x: iterable with len

      bessel: (default ``False``) to be passed to the average to divide by
      ``N - 1`` (Bessel's correction)

    Returns:
      A float with the standard deviation of the elements of x
    '''
    return math.sqrt(average(variance(x, avgx), bessel=bessel))
