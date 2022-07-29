import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

from ccxtpro.base.cache import ArrayCache, ArrayCacheByTimestamp, ArrayCacheBySymbolById  # noqa: F402


def equals(a, b):
    return a == b


# ----------------------------------------------------------------------------

cache = ArrayCache(3)

cache.append({'symbol': 'BTC/USDT', 'data': 1})
cache.append({'symbol': 'BTC/USDT', 'data': 2})
cache.append({'symbol': 'BTC/USDT', 'data': 3})
cache.append({'symbol': 'BTC/USDT', 'data': 4})

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'data': 2},
    {'symbol': 'BTC/USDT', 'data': 3},
    {'symbol': 'BTC/USDT', 'data': 4},
]))

cache.append({'symbol': 'BTC/USDT', 'data': 5})
cache.append({'symbol': 'BTC/USDT', 'data': 6})
cache.append({'symbol': 'BTC/USDT', 'data': 7})
cache.append({'symbol': 'BTC/USDT', 'data': 8})

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'data': 6},
    {'symbol': 'BTC/USDT', 'data': 7},
    {'symbol': 'BTC/USDT', 'data': 8},
]))

cache.clear()

cache.append({'symbol': 'BTC/USDT', 'data': 1})

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'data': 1},
]))

# ----------------------------------------------------------------------------

cache = ArrayCache(1)

cache.append({'symbol': 'BTC/USDT', 'data': 1})
cache.append({'symbol': 'BTC/USDT', 'data': 2})

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'data': 2},
]))

# ----------------------------------------------------------------------------

cache = ArrayCacheByTimestamp()

ohlcv1 = [100, 1, 2, 3]
ohlcv2 = [200, 5, 6, 7]
cache.append(ohlcv1)
cache.append(ohlcv2)

assert equals(cache, [ohlcv1, ohlcv2])

modify2 = [200, 10, 11, 12]
cache.append(modify2)

assert equals(cache, [ohlcv1, modify2])

# ----------------------------------------------------------------------------

cache = ArrayCacheBySymbolById()

object1 = {'symbol': 'BTC/USDT', 'id': 'abcdef', 'i': 1}
object2 = {'symbol': 'ETH/USDT', 'id': 'qwerty', 'i': 2}
object3 = {'symbol': 'BTC/USDT', 'id': 'abcdef', 'i': 3}
cache.append(object1)
cache.append(object2)
cache.append(object3)  # should update index 0

assert equals(cache, [object2, object3])

cache = ArrayCacheBySymbolById(5)

for i in range(1, 11):
    cache.append({
        'symbol': 'BTC/USDT',
        'id': str(i),
        'i': i,
    })

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '6', 'i': 6},
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 7},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 8},
    {'symbol': 'BTC/USDT', 'id': '9', 'i': 9},
    {'symbol': 'BTC/USDT', 'id': '10', 'i': 10},
]))

for i in range(1, 11):
    cache.append({
        'symbol': 'BTC/USDT',
        'id': str(i),
        'i': i + 10,
    })

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '6', 'i': 16},
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 17},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 18},
    {'symbol': 'BTC/USDT', 'id': '9', 'i': 19},
    {'symbol': 'BTC/USDT', 'id': '10', 'i': 20},
]))

middle = {'symbol': 'BTC/USDT', 'id': '8', 'i': 28}
cache.append(middle)

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '6', 'i': 16},
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 17},
    {'symbol': 'BTC/USDT', 'id': '9', 'i': 19},
    {'symbol': 'BTC/USDT', 'id': '10', 'i': 20},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 28},
]))

otherMiddle = {'symbol': 'BTC/USDT', 'id': '7', 'i': 27}
cache.append(otherMiddle)

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '6', 'i': 16},
    {'symbol': 'BTC/USDT', 'id': '9', 'i': 19},
    {'symbol': 'BTC/USDT', 'id': '10', 'i': 20},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 28},
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 27},
]))

for i in range(30, 33):
    cache.append({
        'symbol': 'BTC/USDT',
        'id': str(i),
        'i': i + 10,
    })

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 28},
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 27},
    {'symbol': 'BTC/USDT', 'id': '30', 'i': 40},
    {'symbol': 'BTC/USDT', 'id': '31', 'i': 41},
    {'symbol': 'BTC/USDT', 'id': '32', 'i': 42}]))

first = {'symbol': 'BTC/USDT', 'id': '8', 'i': 38}
cache.append(first)

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 27},
    {'symbol': 'BTC/USDT', 'id': '30', 'i': 40},
    {'symbol': 'BTC/USDT', 'id': '31', 'i': 41},
    {'symbol': 'BTC/USDT', 'id': '32', 'i': 42},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 38},
]))

another = {'symbol': 'BTC/USDT', 'id': '30', 'i': 50}
cache.append(another)

assert(equals(cache, [
    {'symbol': 'BTC/USDT', 'id': '7', 'i': 27},
    {'symbol': 'BTC/USDT', 'id': '31', 'i': 41},
    {'symbol': 'BTC/USDT', 'id': '32', 'i': 42},
    {'symbol': 'BTC/USDT', 'id': '8', 'i': 38},
    {'symbol': 'BTC/USDT', 'id': '30', 'i': 50},
]))

# ----------------------------------------------------------------------------

# test ArrayCacheBySymbolById limit with symbol set
symbol = 'BTC/USDT'
cache = ArrayCacheBySymbolById()
initialLength = 5
for i in range(0, initialLength):
    cache.append({
        'symbol': symbol,
        'id': str(i),
        'i': i,
    })

limited = cache.getLimit(symbol, None)

assert initialLength == limited

cache = ArrayCacheBySymbolById()
appendItemsLength = 3
for i in range(0, appendItemsLength):
    cache.append({
        'symbol': symbol,
        'id': str(i),
        'i': i,
    })

outsideLimit = 5
limited = cache.getLimit(symbol, outsideLimit)

assert appendItemsLength == limited

outsideLimit = 2  # if limit < newsUpdate that should be returned
limited = cache.getLimit(symbol, outsideLimit)

assert outsideLimit == limited

# ----------------------------------------------------------------------------

# test ArrayCacheBySymbolById limit with symbol None
symbol = 'BTC/USDT'
cache = ArrayCacheBySymbolById()
initialLength = 5
for i in range(0, initialLength):
    cache.append({
        'symbol': symbol,
        'id': str(i),
        'i': i,
    })

limited = cache.getLimit(None, None)

assert initialLength == limited

cache = ArrayCacheBySymbolById()
appendItemsLength = 3
for i in range(0, appendItemsLength):
    cache.append({
        'symbol': symbol,
        'id': str(i),
        'i': i,
    })

outsideLimit = 5
limited = cache.getLimit(symbol, outsideLimit)

assert appendItemsLength == limited

outsideLimit = 2  # if limit < newsUpdate that should be returned
limited = cache.getLimit(symbol, outsideLimit)

assert outsideLimit == limited


# ----------------------------------------------------------------------------
# test ArrayCacheBySymbolById, same order should not increase the limit

cache = ArrayCacheBySymbolById()
symbol = 'BTC/USDT'
otherSymbol = 'ETH/USDT'

cache.append({'symbol': symbol, 'id': 'singleId', 'i': 3})
cache.append({'symbol': symbol, 'id': 'singleId', 'i': 3})
cache.append({'symbol': otherSymbol, 'id': 'singleId', 'i': 3})
outsideLimit = 5
limited = cache.getLimit(symbol, outsideLimit)
limited2 = cache.getLimit(None, outsideLimit)

assert 1 == limited
assert 2 == limited2


# ----------------------------------------------------------------------------
# test testLimitArrayCacheByTimestamp limit

cache = ArrayCacheByTimestamp()

initialLength = 5
for i in range(0, initialLength):
    cache.append([
        i * 10,
        i * 10,
        i * 10,
        i * 10
    ])

limited = cache.getLimit(None, None)

assert initialLength == limited

appendItemsLength = 3
for i in range(0, appendItemsLength):
    cache.append([
        i * 4,
        i * 4,
        i * 4,
        i * 4
    ])

outsideLimit = 5
limited = cache.getLimit(None, outsideLimit)

assert appendItemsLength == limited

outsideLimit = 2  # if limit < newsUpdate that should be returned
limited = cache.getLimit(None, outsideLimit)

assert outsideLimit == limited
