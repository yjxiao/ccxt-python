import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

from ccxtpro.base.order_book import OrderBook, IndexedOrderBook, CountedOrderBook, IncrementalOrderBook, IncrementalIndexedOrderBook  # noqa: F402


def equals(a, b):
    return a == b


# --------------------------------------------------------------------------------------------------------------------

orderBookInput = {
    'bids': [[10.0, 10], [9.1, 11], [8.2, 12], [7.3, 13], [6.4, 14], [4.5, 13], [4.5, 0]],
    'asks': [[16.6, 10], [15.5, 11], [14.4, 12], [13.3, 13], [12.2, 14], [11.1, 13]],
    'timestamp': 1574827239000,
    'nonce': 69,
}

orderBookTarget = {
    'bids': [[10.0, 10], [9.1, 11], [8.2, 12], [7.3, 13], [6.4, 14]],
    'asks': [[11.1, 13], [12.2, 14], [13.3, 13], [14.4, 12], [15.5, 11], [16.6, 10]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

storeBid = {
    'bids': [[10.0, 10], [9.1, 11], [8.2, 12], [7.3, 13], [6.4, 14], [3, 4]],
    'asks': [[11.1, 13], [12.2, 14], [13.3, 13], [14.4, 12], [15.5, 11], [16.6, 10]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedOrderBookTarget = {
    'bids': [[10.0, 10], [9.1, 11], [8.2, 12], [7.3, 13], [6.4, 14]],
    'asks': [[11.1, 13], [12.2, 14], [13.3, 13], [14.4, 12], [15.5, 11]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedDeletedOrderBookTarget = {
    'bids': [[10.0, 10], [9.1, 11], [8.2, 12], [7.3, 13], [6.4, 14]],
    'asks': [[11.1, 13], [12.2, 14], [13.3, 13], [14.4, 12]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

indexedOrderBookInput = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[16.6, 10, '1240'], [15.5, 11, '1241'], [14.4, 12, '1242'], [13.3, 13, '1243'], [12.2, 14, '1244'], [11.1, 13, '1244']],
    'timestamp': 1574827239000,
    'nonce': 69,
}

indexedOrderBookTarget = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[11.1, 13, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedIndexedOrderBookTarget = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238']],
    'asks': [[11.1, 13, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

incrementalIndexedOrderBookTarget = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[11.1, 27, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedIncrementalIndexedOrderBookTarget = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238']],
    'asks': [[11.1, 27, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

storedIncrementalIndexedOrderBookTarget = {
    'bids': [[10.0, 13, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[11.1, 27, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

anotherStoredIncrementalIndexedOrderBookTarget = {
    'bids': [[10.2, 13, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[11.1, 27, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

overwrite1234 = {
    'bids': [[9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[11.1, 13, '1244'], [13.3, 13, '1243'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

overwrite1244 = {
    'bids': [[10.0, 10, '1234'], [9.1, 11, '1235'], [8.2, 12, '1236'], [7.3, 13, '1237'], [6.4, 14, '1238'], [4.5, 13, '1239']],
    'asks': [[13.3, 13, '1243'], [13.5, 13, '1244'], [14.4, 12, '1242'], [15.5, 11, '1241'], [16.6, 10, '1240']],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

countedOrderBookInput = {
    'bids': [[10.0, 10, 1], [9.1, 11, 1], [8.2, 12, 1], [7.3, 13, 1], [7.3, 0, 1], [6.4, 14, 5], [4.5, 13, 5], [4.5, 13, 1], [4.5, 13, 0]],
    'asks': [[16.6, 10, 1], [15.5, 11, 1], [14.4, 12, 1], [13.3, 13, 3], [12.2, 14, 3], [11.1, 13, 3], [11.1, 13, 12]],
    'timestamp': 1574827239000,
    'nonce': 69,
}

countedOrderBookTarget = {
    'bids': [[10.0, 10, 1], [9.1, 11, 1], [8.2, 12, 1], [6.4, 14, 5]],
    'asks': [[11.1, 13, 12], [12.2, 14, 3], [13.3, 13, 3], [14.4, 12, 1], [15.5, 11, 1], [16.6, 10, 1]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

storedCountedOrderbookTarget = {
    'bids': [[10.0, 10, 1], [9.1, 11, 1], [8.2, 12, 1], [6.4, 14, 5], [1, 1, 6]],
    'asks': [[11.1, 13, 12], [12.2, 14, 3], [13.3, 13, 3], [14.4, 12, 1], [15.5, 11, 1], [16.6, 10, 1]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedCountedOrderBookTarget = {
    'bids': [[10.0, 10, 1], [9.1, 11, 1], [8.2, 12, 1], [6.4, 14, 5]],
    'asks': [[11.1, 13, 12], [12.2, 14, 3], [13.3, 13, 3], [14.4, 12, 1], [15.5, 11, 1]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

incrementalOrderBookInput = {
    'bids': [[10.0, 1], [10.0, 2], [9.1, 0], [8.2, 1], [7.3, 1], [6.4, 1]],
    'asks': [[11.1, 5], [11.1, -6], [11.1, 2], [12.2, 10], [12.2, -9.875], [12.2, 0], [13.3, 3], [14.4, 4], [15.5, 1], [16.6, 3]],
    'timestamp': 1574827239000,
    'nonce': 69,
}

incremetalOrderBookTarget = {
    'bids': [[10.0, 3], [8.2, 1], [7.3, 1], [6.4, 1]],
    'asks': [[11.1, 2], [12.2, 0.125], [13.3, 3], [14.4, 4], [15.5, 1], [16.6, 3]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

limitedIncremetalOrderBookTarget = {
    'bids': [[10.0, 3], [8.2, 1], [7.3, 1], [6.4, 1]],
    'asks': [[11.1, 2], [12.2, 0.125], [13.3, 3], [14.4, 4], [15.5, 1]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

storedIncremetalOrderBookTarget = {
    'bids': [[10.0, 3], [8.2, 1], [7.3, 1], [6.4, 1], [3, 3]],
    'asks': [[11.1, 2], [12.2, 0.125], [13.3, 3], [14.4, 4], [15.5, 1], [16.6, 3]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

doubleStoredIncremetalOrderBookTarget = {
    'bids': [[10.0, 3], [8.2, 1], [7.3, 1], [6.4, 1], [3, 10]],
    'asks': [[11.1, 2], [12.2, 0.125], [13.3, 3], [14.4, 4], [15.5, 1], [16.6, 3]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

negativeStoredIncremetalOrderBookTarget = {
    'bids': [[10.0, 3], [8.2, 1], [7.3, 1], [6.4, 1]],
    'asks': [[11.1, 2], [12.2, 0.125], [13.3, 3], [14.4, 4], [16.6, 3]],
    'timestamp': 1574827239000,
    'datetime': '2019-11-27T04:00:39.000Z',
    'nonce': 69,
}

bids = None
asks = None

# --------------------------------------------------------------------------------------------------------------------

orderBook = OrderBook(orderBookInput)
limited = OrderBook(orderBookInput, 5)
orderBook.limit()
assert equals(orderBook, orderBookTarget)

orderBook.limit(5)
limited.limit()
assert equals(orderBook, limitedOrderBookTarget)
assert equals(limited, limitedOrderBookTarget)
orderBook.limit()
assert equals(orderBook, orderBookTarget)

bids = orderBook['bids']
bids.store(1000, 0)
orderBook.limit()
assert equals(orderBook, orderBookTarget)
bids.store(3, 4)
orderBook.limit()
assert equals(orderBook, storeBid)
bids.store(3, 0)
orderBook.limit()
assert equals(orderBook, orderBookTarget)
asks = limited['asks']
asks.store(15.5, 0)
limited.limit()
assert equals(limited, limitedDeletedOrderBookTarget)

# --------------------------------------------------------------------------------------------------------------------

indexedOrderBook = IndexedOrderBook(indexedOrderBookInput)
limitedIndexedOrderBook = IndexedOrderBook(indexedOrderBookInput, 5)
indexedOrderBook.limit()
assert equals(indexedOrderBook, indexedOrderBookTarget)

indexedOrderBook.limit(5)
limitedIndexedOrderBook.limit()
assert equals(indexedOrderBook, limitedIndexedOrderBookTarget)
assert equals(limitedIndexedOrderBook, limitedIndexedOrderBookTarget)
indexedOrderBook.limit()
assert equals(indexedOrderBook, indexedOrderBookTarget)

bids = indexedOrderBook['bids']
bids.store(1000, 0, '12345')
assert equals(indexedOrderBook, indexedOrderBookTarget)
bids.store(10, 0, '1234')
indexedOrderBook.limit()
assert equals(indexedOrderBook, overwrite1234)
indexedOrderBook = IndexedOrderBook(indexedOrderBookInput)
asks = indexedOrderBook['asks']
asks.store(13.5, 13, '1244')
indexedOrderBook.limit()
assert equals(indexedOrderBook, overwrite1244)

# --------------------------------------------------------------------------------------------------------------------

countedOrderBook = CountedOrderBook(countedOrderBookInput)
limitedCountedOrderBook = CountedOrderBook(countedOrderBookInput, 5)
countedOrderBook.limit()
assert equals(countedOrderBook, countedOrderBookTarget)

countedOrderBook.limit(5)
limitedCountedOrderBook.limit()
assert equals(countedOrderBook, limitedCountedOrderBookTarget)
assert equals(limitedCountedOrderBook, limitedCountedOrderBookTarget)
countedOrderBook.limit()
assert equals(countedOrderBook, countedOrderBookTarget)

bids = countedOrderBook['bids']
bids.store(5, 0, 6)
countedOrderBook.limit()
assert equals(countedOrderBook, countedOrderBookTarget)
bids.store(1, 1, 6)
countedOrderBook.limit()
assert equals(countedOrderBook, storedCountedOrderbookTarget)

# --------------------------------------------------------------------------------------------------------------------

incrementalOrderBook = IncrementalOrderBook(incrementalOrderBookInput)
limitedIncrementalOrderBook = IncrementalOrderBook(incrementalOrderBookInput, 5)
incrementalOrderBook.limit()
assert equals(incrementalOrderBook, incremetalOrderBookTarget)

incrementalOrderBook.limit(5)
limitedIncrementalOrderBook.limit()
assert equals(incrementalOrderBook, limitedIncremetalOrderBookTarget)
assert equals(limitedIncrementalOrderBook, limitedIncremetalOrderBookTarget)
incrementalOrderBook.limit()
assert equals(incrementalOrderBook, incremetalOrderBookTarget)

bids = incrementalOrderBook['bids']
bids.store(3, 3)
incrementalOrderBook.limit()
assert equals(incrementalOrderBook, storedIncremetalOrderBookTarget)
bids.store(3, 7)
incrementalOrderBook.limit()
assert equals(incrementalOrderBook, doubleStoredIncremetalOrderBookTarget)
bids.store(17, 0)
assert equals(incrementalOrderBook, doubleStoredIncremetalOrderBookTarget)
incrementalOrderBook = IncrementalOrderBook(incrementalOrderBookInput)
asks = incrementalOrderBook['asks']
asks.store(15.5, -10)
incrementalOrderBook.limit()
assert equals(incrementalOrderBook, negativeStoredIncremetalOrderBookTarget)

# --------------------------------------------------------------------------------------------------------------------

incrementalIndexedOrderBook = IncrementalIndexedOrderBook(indexedOrderBookInput)
limitedIncrementalIndexedOrderBook = IncrementalIndexedOrderBook(indexedOrderBookInput, 5)
incrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, incrementalIndexedOrderBookTarget)

incrementalIndexedOrderBook.limit(5)
limitedIncrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, limitedIncrementalIndexedOrderBookTarget)
assert equals(limitedIncrementalIndexedOrderBook, limitedIncrementalIndexedOrderBookTarget)
incrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, incrementalIndexedOrderBookTarget)

bids = incrementalIndexedOrderBook['bids']
bids.store(5, 0, 'xxyy')
incrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, incrementalIndexedOrderBookTarget)
bids.store(10.0, 3, '1234')  # price does match merge size
incrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, storedIncrementalIndexedOrderBookTarget)
incrementalIndexedOrderBook = IncrementalIndexedOrderBook(indexedOrderBookInput)
bids = incrementalIndexedOrderBook['bids']
bids.store(10.2, 3, '1234')  # price does not match merge size
incrementalIndexedOrderBook.limit()
assert equals(incrementalIndexedOrderBook, anotherStoredIncrementalIndexedOrderBookTarget)

# --------------------------------------------------------------------------------------------------------------------

resetBook = OrderBook(storeBid)
resetBook.limit()
resetBook.reset(orderBookInput)
resetBook.limit()
assert equals(resetBook, orderBookTarget)
