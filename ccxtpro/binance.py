# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt
from ccxt.base.errors import ExchangeError


class binance(ccxtpro.Exchange, ccxt.binance):

    def describe(self):
        return self.deep_extend(super(binance, self).describe(), {
            'has': {
                'watchOrderBook': True,
                'watchTrades': True,
                'watchOHLCV': True,
                'watchTicker': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://stream.binance.com:9443/ws',
                },
            },
            'options': {
                'watchOrderBookRate': 100,  # get updates every 100ms or 1000ms
                'tradesLimit': 1000,
                'OHLCVLimit': 3,
            },
        })

    async def load_markets(self, reload=False, params={}):
        markets = await super(binance, self).load_markets(reload, params)
        marketsByLowercaseId = self.safe_value(self.options, 'marketsByLowercaseId')
        if (marketsByLowercaseId is None) or reload:
            marketsByLowercaseId = {}
            for i in range(0, len(self.symbols)):
                symbol = self.symbols[i]
                market = self.markets[symbol]
                lowercaseId = self.safe_string_lower(market, 'id')
                market['lowercaseId'] = lowercaseId
                self.markets_by_id[market['id']] = market
                self.markets[symbol] = market
                marketsByLowercaseId[lowercaseId] = self.markets[symbol]
            self.options['marketsByLowercaseId'] = marketsByLowercaseId
        return markets

    async def watch_order_book(self, symbol, limit=None, params={}):
        #
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#partial-book-depth-streams
        #
        # <symbol>@depth<levels>@100ms or <symbol>@depth<levels>(1000ms)
        # valid <levels> are 5, 10, or 20
        #
        if limit is not None:
            if (limit != 5) and (limit != 10) and (limit != 20):
                raise ExchangeError(self.id + ' watchOrderBook limit argument must be None, 5, 10 or 20')
        await self.load_markets()
        market = self.market(symbol)
        #
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#how-to-manage-a-local-order-book-correctly
        #
        # 1. Open a stream to wss://stream.binance.com:9443/ws/bnbbtc@depth.
        # 2. Buffer the events you receive from the stream.
        # 3. Get a depth snapshot from https://www.binance.com/api/v1/depth?symbol=BNBBTC&limit=1000 .
        # 4. Drop any event where u is <= lastUpdateId in the snapshot.
        # 5. The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
        # 6. While listening to the stream, each new event's U should be equal to the previous event's u+1.
        # 7. The data in each event is the absolute quantity for a price level.
        # 8. If the quantity is 0, remove the price level.
        # 9. Receiving an event that removes a price level that is not in your local order book can happen and is normal.
        #
        name = 'depth'
        messageHash = market['lowercaseId'] + '@' + name
        url = self.urls['api']['ws']  # + '/' + messageHash
        requestId = self.nonce()
        watchOrderBookRate = self.safe_string(self.options, 'watchOrderBookRate', '100')
        request = {
            'method': 'SUBSCRIBE',
            'params': [
                messageHash + '@' + watchOrderBookRate + 'ms',
            ],
            'id': requestId,
        }
        subscription = {
            'id': str(requestId),
            'messageHash': messageHash,
            'name': name,
            'symbol': symbol,
            'method': self.handle_order_book_subscription,
            'limit': limit,
        }
        message = self.extend(request, params)
        # 1. Open a stream to wss://stream.binance.com:9443/ws/bnbbtc@depth.
        future = self.watch(url, messageHash, message, messageHash, subscription)
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def limit_order_book(self, orderbook, symbol, limit=None, params={}):
        return orderbook.limit(limit)

    async def fetch_order_book_snapshot(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        messageHash = self.safe_string(subscription, 'messageHash')
        # 3. Get a depth snapshot from https://www.binance.com/api/v1/depth?symbol=BNBBTC&limit=1000 .
        # todo: self is a synch blocking call in ccxt.php - make it async
        snapshot = await self.fetch_order_book(symbol)
        orderbook = self.orderbooks[symbol]
        orderbook.reset(snapshot)
        # unroll the accumulated deltas
        messages = orderbook.cache
        for i in range(0, len(messages)):
            message = messages[i]
            self.handle_order_book_message(client, message, orderbook)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client, message, orderbook):
        u = self.safe_integer_2(message, 'u', 'lastUpdateId')
        # merge accumulated deltas
        # 4. Drop any event where u is <= lastUpdateId in the snapshot.
        if u > orderbook['nonce']:
            U = self.safe_integer(message, 'U')
            # 5. The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
            if (U is not None) and ((U - 1) > orderbook['nonce']):
                # todo: client.reject from handleOrderBookMessage properly
                raise ExchangeError(self.id + ' handleOrderBook received an out-of-order nonce')
            self.handle_deltas(orderbook['asks'], self.safe_value(message, 'a', []))
            self.handle_deltas(orderbook['bids'], self.safe_value(message, 'b', []))
            orderbook['nonce'] = u
            timestamp = self.safe_integer(message, 'E')
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_order_book(self, client, message):
        #
        # initial snapshot is fetched with ccxt's fetchOrderBook
        # the feed does not include a snapshot, just the deltas
        #
        #     {
        #         "e": "depthUpdate",  # Event type
        #         "E": 1577554482280,  # Event time
        #         "s": "BNBBTC",  # Symbol
        #         "U": 157,  # First update ID in event
        #         "u": 160,  # Final update ID in event
        #         "b": [ # bids
        #             ["0.0024", "10"],  # price, size
        #         ],
        #         "a": [ # asks
        #             ["0.0026", "100"],  # price, size
        #         ]
        #     }
        #
        marketId = self.safe_string(message, 's')
        market = None
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
        name = 'depth'
        messageHash = market['lowercaseId'] + '@' + name
        orderbook = self.orderbooks[symbol]
        if orderbook['nonce'] is not None:
            # 5. The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
            # 6. While listening to the stream, each new event's U should be equal to the previous event's u+1.
            nonce = orderbook['nonce']
            self.handle_order_book_message(client, message, orderbook)
            if nonce < orderbook['nonce']:
                client.resolve(orderbook, messageHash)
        else:
            # 2. Buffer the events you receive from the stream.
            orderbook.cache.append(message)

    def sign_message(self, client, messageHash, message, params={}):
        # todo: implement binance signMessage
        return message

    def handle_order_book_subscription(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_string(subscription, 'limit')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({}, limit)
        # fetch the snapshot in a separate async call
        self.spawn(self.fetch_order_book_snapshot, client, message, subscription)

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         "result": null,
        #         "id": 1574649734450
        #     }
        #
        id = self.safe_string(message, 'id')
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        subscription = self.safe_value(subscriptionsById, id, {})
        method = self.safe_value(subscription, 'method')
        if method is not None:
            method(client, message, subscription)
        return message

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        name = 'trade'
        messageHash = market['lowercaseId'] + '@' + name
        url = self.urls['api']['ws']  # + '/' + messageHash
        requestId = self.nonce()
        request = {
            'method': 'SUBSCRIBE',
            'params': [
                messageHash,
            ],
            'id': requestId,
        }
        subscribe = {
            'id': requestId,
        }
        future = self.watch(url, messageHash, request, messageHash, subscribe)
        return await self.after(future, self.filterBySinceLimit, since, limit)

    def handle_trade(self, client, message):
        # The Trade Streams push raw trade information; each trade has a unique buyer and seller.
        # Update Speed: Real-time
        #
        # {
        #   e: 'trade',
        #   E: 1579481530911,
        #   s: 'ETHBTC',
        #   t: 158410082,
        #   p: '0.01914100',
        #   q: '0.00700000',
        #   b: 586187049,
        #   a: 586186710,
        #   T: 1579481530910,
        #   m: False,
        #   M: True
        # }
        marketId = self.safe_string(message, 's')
        market = None
        symbol = marketId
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
        lowerCaseId = self.safe_string_lower(message, 's')
        event = self.safe_string(message, 'e')
        messageHash = lowerCaseId + '@' + event
        parsed = self.parse_trade(message, market)
        array = self.safe_value(self.trades, symbol, [])
        array.append(parsed)
        length = len(array)
        if length > self.options['tradesLimit']:
            array.pop(0)
        self.trades[symbol] = array
        client.resolve(array, messageHash)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        url = self.urls['api']['ws']
        market = self.market(symbol)
        marketId = market['lowercaseId']
        interval = self.timeframes[timeframe]
        name = 'kline_'
        messageHash = marketId + '@' + name + interval
        requestId = self.nonce()
        request = {
            'method': 'SUBSCRIBE',
            'params': [
                messageHash,
            ],
            'id': requestId,
        }
        subscribe = {
            'id': requestId,
        }
        return await self.watch(url, messageHash, request, messageHash, subscribe)

    def handle_ohclv(self, client, message):
        # {
        #   e: 'kline',
        #   E: 1579482921215,
        #   s: 'ETHBTC',
        #   k: {
        #     t: 1579482900000,
        #     T: 1579482959999,
        #     s: 'ETHBTC',
        #     i: '1m',
        #     f: 158411535,
        #     L: 158411550,
        #     o: '0.01913200',
        #     c: '0.01913500',
        #     h: '0.01913700',
        #     l: '0.01913200',
        #     v: '5.08400000',
        #     n: 16,
        #     x: False,
        #     q: '0.09728060',
        #     V: '3.30200000',
        #     Q: '0.06318500',
        #     B: '0'
        #   }
        # }
        marketId = self.safe_string(message, 's')
        lowercaseMarketId = self.safe_string_lower(message, 's')
        event = self.safe_string(message, 'e')
        kline = self.safe_value(message, 'k')
        interval = self.safe_string(kline, 'i')
        messageHash = lowercaseMarketId + '@' + event + '_' + interval
        timestamp = self.safe_integer(kline, 't')
        open = self.safe_float(kline, 'o')
        high = self.safe_float(kline, 'h')
        low = self.safe_float(kline, 'l')
        close = self.safe_float(kline, 'c')
        volume = self.safe_float(kline, 'v')
        parsed = [
            timestamp,
            open,
            high,
            low,
            close,
            volume,
        ]
        symbol = marketId
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
        if not (symbol in self.ohlcvs):
            self.ohlcvs[symbol] = []
        stored = self.ohlcvs[symbol]
        length = len(stored)
        if length and parsed[0] == stored[length - 1][0]:
            stored[length - 1] = parsed
        else:
            stored.append(parsed)
            if length + 1 > self.options['OHLCVLimit']:
                stored.pop(0)
        self.ohlcvs[symbol] = stored
        client.resolve(stored, messageHash)

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        url = self.urls['api']['ws']
        market = self.market(symbol)
        marketId = market['lowercaseId']
        name = 'ticker'
        messageHash = marketId + '@' + name
        requestId = self.nonce()
        request = {
            'method': 'SUBSCRIBE',
            'params': [
                messageHash,
            ],
            'id': requestId,
        }
        subscribe = {
            'id': requestId,
        }
        return await self.watch(url, messageHash, request, messageHash, subscribe)

    def handle_ticker(self, client, message):
        # 24hr rolling window ticker statistics for a single symbol. These are NOT the statistics of the UTC day, but a 24hr rolling window for the previous 24hrs.
        #
        # Update Speed: 1000ms
        # {
        #   e: '24hrTicker',
        #   E: 1579485598569,
        #   s: 'ETHBTC',
        #   p: '-0.00004000',
        #   P: '-0.209',
        #   w: '0.01920495',
        #   x: '0.01916500',
        #   c: '0.01912500',
        #   Q: '0.10400000',
        #   b: '0.01912200',
        #   B: '4.10400000',
        #   a: '0.01912500',
        #   A: '0.00100000',
        #   o: '0.01916500',
        #   h: '0.01956500',
        #   l: '0.01887700',
        #   v: '173518.11900000',
        #   q: '3332.40703994',
        #   O: 1579399197842,
        #   C: 1579485597842,
        #   F: 158251292,
        #   L: 158414513,
        #   n: 163222
        # }
        event = 'ticker'  # message['e'] == 24hrTicker
        wsMarketId = self.safe_string_lower(message, 's')
        messageHash = wsMarketId + '@' + event
        timestamp = self.safe_integer(message, 'C')
        symbol = None
        marketId = self.safe_string(message, 's')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
        last = self.safe_float(message, 'c')
        parsed = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(message, 'h'),
            'low': self.safe_float(message, 'l'),
            'bid': self.safe_float(message, 'b'),
            'bidVolume': self.safe_float(message, 'B'),
            'ask': self.safe_float(message, 'a'),
            'askVolume': self.safe_float(message, 'A'),
            'vwap': self.safe_float(message, 'w'),
            'open': self.safe_float(message, 'o'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(message, 'x'),  # previous day close
            'change': self.safe_float(message, 'p'),
            'percentage': self.safe_float(message, 'P'),
            'average': None,
            'baseVolume': self.safe_float(message, 'v'),
            'quoteVolume': self.safe_float(message, 'q'),
            'info': message,
        }
        client.resolve(parsed, messageHash)

    def handle_message(self, client, message):
        methods = {
            'depthUpdate': self.handle_order_book,
            'trade': self.handle_trade,
            'kline': self.handle_ohclv,
            '24hrTicker': self.handle_ticker,
        }
        event = self.safe_string(message, 'e')
        method = self.safe_value(methods, event)
        if method is None:
            requestId = self.safe_string(message, 'id')
            if requestId is not None:
                return self.handle_subscription_status(client, message)
            return message
        else:
            return method(client, message)
