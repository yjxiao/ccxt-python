# -*- coding: utf-8 -*-

import operator

INFINITY = float('inf')


class OrderBookSide(list):
    side = None  # set to True for bids and False for asks
    # sorted(..., reverse=self.side)

    def __init__(self, deltas=[]):
        # allocate memory for the list here (it will not be resized...)
        super(OrderBookSide, self).__init__()
        self._index = {}
        self.update(deltas)

    def storeArray(self, delta):
        price = delta[0]
        size = delta[1]
        if size:
            self._index[price] = size
        else:
            if price in self._index:
                del self._index[price]

    def store(self, price, size):
        if size:
            self._index[price] = size
        else:
            if price in self._index:
                del self._index[price]

    def limit(self, n=None):
        first_element = operator.itemgetter(0)
        generator = (list(t) for t in self._index.items())
        array = sorted(generator, key=first_element, reverse=self.side)
        if n and n < len(array):
            array = array[:n]
        self.clear()
        self.extend(array)
        return self

    def update(self, deltas):
        for delta in deltas:
            self.storeArray(delta)


# -----------------------------------------------------------------------------
# some exchanges limit the number of bids/asks in the aggregated orderbook
# orders beyond the limit threshold are not updated with new ws deltas
# those orders should not be returned to the user, they are outdated quickly

class LimitedOrderBookSide(OrderBookSide):
    def __init__(self, deltas=[], depth=None):
        self._depth = depth
        super(LimitedOrderBookSide, self).__init__(deltas)

    def limit(self, n=None):
        first_element = operator.itemgetter(0)
        generator = (list(t) for t in self._index.items())
        array = sorted(generator, key=first_element, reverse=self.side)
        limit = min(n or INFINITY, self._depth or INFINITY)
        if limit < len(array):
            array = array[:limit]
        self._index = dict(array)
        self.clear()
        self.extend(array)
        return self


# -----------------------------------------------------------------------------
# overwrites absolute volumes at price levels
# or deletes price levels based on order counts (3rd value in a bidask delta)

class CountedOrderBookSide(OrderBookSide):
    def store(self, price, size, count):
        if count and size:
            self._index[price] = [price, size, count]
        else:
            if price in self._index:
                del self._index[price]

    def storeArray(self, delta):
        price, size, count = delta
        if count and size:
            self._index[price] = delta
        else:
            if price in self._index:
                del self._index[price]

    def limit(self, n=None):
        first_element = operator.itemgetter(0)
        generator = (list(t) for t in self._index.values())
        array = sorted(generator, key=first_element, reverse=self.side)
        if n and n < len(array):
            array = array[:n]
        self.clear()
        self.extend(array)
        return self

# -----------------------------------------------------------------------------
# indexed by order ids (3rd value in a bidask delta)


class IndexedOrderBookSide(OrderBookSide):
    def store(self, price, size, order_id):
        if size:
            self._index[order_id] = [price, size, order_id]
        else:
            if order_id in self._index:
                del self._index[order_id]

    def restore(self, price, size, order_id):  # price is presumably None
        if size:
            array = self._index.get(order_id)
            price = array[0] if price is None else price
            self._index[order_id] = [price, size, order_id]
        else:
            del self._index[order_id]

    def storeArray(self, delta):
        size = delta[1]
        order_id = delta[2]
        if size:
            self._index[order_id] = delta
        else:
            if order_id in self._index:
                del self._index[order_id]

    def limit(self, n=None):
        first_element = operator.itemgetter(0)
        generator = (list(t) for t in self._index.values())
        array = sorted(generator, key=first_element, reverse=self.side)
        if n and n < len(array):
            array = array[:n]
        self.clear()
        self.extend(array)
        return self


# -----------------------------------------------------------------------------
# limited and order-id-based

class LimitedIndexedOrderBookSide(IndexedOrderBookSide, LimitedOrderBookSide):
    pass


# -----------------------------------------------------------------------------
# adjusts the volumes by positive or negative relative changes or differences

class IncrementalOrderBookSide(OrderBookSide):
    def store(self, price, size):
        result = self._index.get(price, 0) + size
        if result > 0:
            self._index[price] = result
            return
        if price in self._index:
            del self._index[price]

    def storeArray(self, delta):
        price, size = delta
        result = self._index.get(price, 0) + size
        if result > 0:
            self._index[price] = result
            return
        if price in self._index:
            del self._index[price]


# -----------------------------------------------------------------------------
# incremental and indexed (2 in 1)

class IncrementalIndexedOrderBookSide(OrderBookSide):
    def store(self, price, size, order_id):
        if size:
            result = self._index.get(price, 0) + size
            if result > 0:
                self._index[order_id] = result
                return
        if order_id in self._index:
            del self._index[order_id]

    def storeArray(self, delta):
        price, size, order_id = delta
        if size:
            result = self._index.get(price, 0) + size
            if result > 0:
                self._index[order_id] = result
                return
        if order_id in self._index:
            del self._index[order_id]


# -----------------------------------------------------------------------------
# a more elegant syntax is possible here, but native inheritance is portable

class Asks(OrderBookSide): side = False                                     # noqa
class Bids(OrderBookSide): side = True                                      # noqa
class LimitedAsks(LimitedOrderBookSide): side = False                       # noqa
class LimitedBids(LimitedOrderBookSide): side = True                        # noqa
class CountedAsks(CountedOrderBookSide): side = False                       # noqa
class CountedBids(CountedOrderBookSide): side = True                        # noqa
class IndexedAsks(IndexedOrderBookSide): side = False                       # noqa
class IndexedBids(IndexedOrderBookSide): side = True                        # noqa
class LimitedIndexedAsks(LimitedIndexedOrderBookSide): side = False         # noqa
class LimitedIndexedBids(LimitedIndexedOrderBookSide): side = True          # noqa
class IncrementalAsks(IncrementalOrderBookSide): side = False               # noqa
class IncrementalBids(IncrementalOrderBookSide): side = True                # noqa
class IncrementalIndexedAsks(IncrementalIndexedOrderBookSide): side = False # noqa
class IncrementalIndexedBids(IncrementalIndexedOrderBookSide): side = True  # noqa
