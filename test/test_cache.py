import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

from ccxtpro.base.cache import ArrayCache  # noqa: F402


def equals(a, b):
    return a == b


# --------------------------------------------------------------------------------------------------------------------

cache = ArrayCache(3)

cache.append(1)
cache.append(2)
cache.append(3)
cache.append(4)

assert(equals(cache, [2, 3, 4]))

cache.append(5)
cache.append(6)
cache.append(7)
cache.append(8)

assert(equals(cache, [6, 7, 8]))

cache.clear()

assert(equals(cache, []))

cache.append(1)

assert(equals(cache, [1]))

# --------------------------------------------------------------------------------------------------------------------

cache = ArrayCache(1)

cache.append(1)
cache.append(2)

assert(equals(cache, [2]))
