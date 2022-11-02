# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.pro.base.exchange import Exchange
import ccxt.async_support
from ccxt.pro.base.cache import ArrayCache
import json


class ndax(Exchange, ccxt.async_support.ndax):

    def describe(self):
        return self.deep_extend(super(ndax, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTrades': True,
                'watchTicker': True,
                'watchOHLCV': True,
            },
            'urls': {
                'test': {
                    'ws': 'wss://ndaxmarginstaging.cdnhop.net:10456/WSAdminGatewa/',
                },
                'api': {
                    'ws': 'wss://api.ndax.io/WSGateway',
                },
            },
            # 'options': {
            #     'tradesLimit': 1000,
            #     'ordersLimit': 1000,
            #     'OHLCVLimit': 1000,
            # },
        })

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return requestId

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the ndax api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        omsId = self.safe_integer(self.options, 'omsId', 1)
        await self.load_markets()
        market = self.market(symbol)
        name = 'SubscribeLevel1'
        messageHash = name + ':' + market['id']
        url = self.urls['api']['ws']
        requestId = self.request_id()
        payload = {
            'OMSId': omsId,
            'InstrumentId': int(market['id']),  # conditionally optional
            # 'Symbol': market['info']['symbol'],  # conditionally optional
        }
        request = {
            'm': 0,  # message type, 0 request, 1 reply, 2 subscribe, 3 event, unsubscribe, 5 error
            'i': requestId,  # sequence number identifies an individual request or request-and-response pair, to your application
            'n': name,  # function name is the name of the function being called or that the server is responding to, the server echoes your call
            'o': self.json(payload),  # JSON-formatted string containing the data being sent with the message
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    def handle_ticker(self, client, message):
        payload = self.safe_value(message, 'o', {})
        #
        #     {
        #         "OMSId": 1,
        #         "InstrumentId": 1,
        #         "BestBid": 6423.57,
        #         "BestOffer": 6436.53,
        #         "LastTradedPx": 6423.57,
        #         "LastTradedQty": 0.96183964,
        #         "LastTradeTime": 1534862990343,
        #         "SessionOpen": 6249.64,
        #         "SessionHigh": 11111,
        #         "SessionLow": 4433,
        #         "SessionClose": 6249.64,
        #         "Volume": 0.96183964,
        #         "CurrentDayVolume": 3516.31668185,
        #         "CurrentDayNumTrades": 8529,
        #         "CurrentDayPxChange": 173.93,
        #         "CurrentNotional": 0.0,
        #         "Rolling24HrNotional": 0.0,
        #         "Rolling24HrVolume": 4319.63870783,
        #         "Rolling24NumTrades": 10585,
        #         "Rolling24HrPxChange": -0.4165607307408487,
        #         "TimeStamp": "1534862990358"
        #     }
        #
        ticker = self.parse_ticker(payload)
        symbol = ticker['symbol']
        market = self.market(symbol)
        self.tickers[symbol] = ticker
        name = 'SubscribeLevel1'
        messageHash = name + ':' + market['id']
        client.resolve(ticker, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the ndax api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        omsId = self.safe_integer(self.options, 'omsId', 1)
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        name = 'SubscribeTrades'
        messageHash = name + ':' + market['id']
        url = self.urls['api']['ws']
        requestId = self.request_id()
        payload = {
            'OMSId': omsId,
            'InstrumentId': int(market['id']),  # conditionally optional
            'IncludeLastCount': 100,  # the number of previous trades to retrieve in the immediate snapshot, 100 by default
        }
        request = {
            'm': 0,  # message type, 0 request, 1 reply, 2 subscribe, 3 event, unsubscribe, 5 error
            'i': requestId,  # sequence number identifies an individual request or request-and-response pair, to your application
            'n': name,  # function name is the name of the function being called or that the server is responding to, the server echoes your call
            'o': self.json(payload),  # JSON-formatted string containing the data being sent with the message
        }
        message = self.extend(request, params)
        trades = await self.watch(url, messageHash, message, messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        payload = self.safe_value(message, 'o', [])
        #
        # initial snapshot
        #
        #     [
        #         [
        #             6913253,       #  0 TradeId
        #             8,             #  1 ProductPairCode
        #             0.03340802,    #  2 Quantity
        #             19116.08,      #  3 Price
        #             2543425077,    #  4 Order1
        #             2543425482,    #  5 Order2
        #             1606935922416,  #  6 Tradetime
        #             0,             #  7 Direction
        #             1,             #  8 TakerSide
        #             0,             #  9 BlockTrade
        #             0,             # 10 Either Order1ClientId or Order2ClientId
        #         ]
        #     ]
        #
        name = 'SubscribeTrades'
        updates = {}
        for i in range(0, len(payload)):
            trade = self.parse_trade(payload[i])
            symbol = trade['symbol']
            tradesArray = self.safe_value(self.trades, symbol)
            if tradesArray is None:
                limit = self.safe_integer(self.options, 'tradesLimit', 1000)
                tradesArray = ArrayCache(limit)
            tradesArray.append(trade)
            self.trades[symbol] = tradesArray
            updates[symbol] = True
        symbols = list(updates.keys())
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            market = self.market(symbol)
            messageHash = name + ':' + market['id']
            tradesArray = self.safe_value(self.trades, symbol)
            client.resolve(tradesArray, messageHash)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        omsId = self.safe_integer(self.options, 'omsId', 1)
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        name = 'SubscribeTicker'
        messageHash = name + ':' + timeframe + ':' + market['id']
        url = self.urls['api']['ws']
        requestId = self.request_id()
        payload = {
            'OMSId': omsId,
            'InstrumentId': int(market['id']),  # conditionally optional
            'Interval': int(self.timeframes[timeframe]),
            'IncludeLastCount': 100,  # the number of previous candles to retrieve in the immediate snapshot, 100 by default
        }
        request = {
            'm': 0,  # message type, 0 request, 1 reply, 2 subscribe, 3 event, unsubscribe, 5 error
            'i': requestId,  # sequence number identifies an individual request or request-and-response pair, to your application
            'n': name,  # function name is the name of the function being called or that the server is responding to, the server echoes your call
            'o': self.json(payload),  # JSON-formatted string containing the data being sent with the message
        }
        message = self.extend(request, params)
        ohlcv = await self.watch(url, messageHash, message, messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #     {
        #         m: 1,
        #         i: 1,
        #         n: 'SubscribeTicker',
        #         o: [[1608284160000,23113.52,23070.88,23075.76,23075.39,162.44964300,23075.38,23075.39,8,1608284100000]],
        #     }
        #
        payload = self.safe_value(message, 'o', [])
        #
        #     [
        #         [
        #             1501603632000,      # 0 DateTime
        #             2700.33,            # 1 High
        #             2687.01,            # 2 Low
        #             2687.01,            # 3 Open
        #             2687.01,            # 4 Close
        #             24.86100992,        # 5 Volume
        #             0,                  # 6 Inside Bid Price
        #             2870.95,            # 7 Inside Ask Price
        #             1                   # 8 InstrumentId
        #             1608290188062.7678,  # 9 candle timestamp
        #         ]
        #     ]
        #
        updates = {}
        for i in range(0, len(payload)):
            ohlcv = payload[i]
            marketId = self.safe_string(ohlcv, 8)
            market = self.safe_market(marketId)
            symbol = market['symbol']
            updates[marketId] = {}
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            keys = list(self.timeframes.keys())
            for j in range(0, len(keys)):
                timeframe = keys[j]
                interval = self.timeframes[timeframe]
                duration = int(interval) * 1000
                timestamp = self.safe_integer(ohlcv, 0)
                parsed = [
                    int(timestamp / duration) * duration,
                    self.safe_float(ohlcv, 3),
                    self.safe_float(ohlcv, 1),
                    self.safe_float(ohlcv, 2),
                    self.safe_float(ohlcv, 4),
                    self.safe_float(ohlcv, 5),
                ]
                stored = self.safe_value(self.ohlcvs[symbol], timeframe, [])
                length = len(stored)
                if length and (parsed[0] == stored[length - 1][0]):
                    previous = stored[length - 1]
                    stored[length - 1] = [
                        parsed[0],
                        previous[1],
                        max(parsed[1], previous[1]),
                        min(parsed[2], previous[2]),
                        parsed[4],
                        self.sum(parsed[5], previous[5]),
                    ]
                    updates[marketId][timeframe] = True
                else:
                    if length and (parsed[0] < stored[length - 1][0]):
                        continue
                    else:
                        stored.append(parsed)
                        limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                        if length >= limit:
                            stored.pop(0)
                        updates[marketId][timeframe] = True
                self.ohlcvs[symbol][timeframe] = stored
        name = 'SubscribeTicker'
        marketIds = list(updates.keys())
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            timeframes = list(updates[marketId].keys())
            for j in range(0, len(timeframes)):
                timeframe = timeframes[j]
                messageHash = name + ':' + timeframe + ':' + marketId
                market = self.safe_market(marketId)
                symbol = market['symbol']
                stored = self.safe_value(self.ohlcvs[symbol], timeframe, [])
                client.resolve(stored, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the ndax api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        omsId = self.safe_integer(self.options, 'omsId', 1)
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        name = 'SubscribeLevel2'
        messageHash = name + ':' + market['id']
        url = self.urls['api']['ws']
        requestId = self.request_id()
        limit = 100 if (limit is None) else limit
        payload = {
            'OMSId': omsId,
            'InstrumentId': int(market['id']),  # conditionally optional
            # 'Symbol': market['info']['symbol'],  # conditionally optional
            'Depth': limit,  # default 100
        }
        request = {
            'm': 0,  # message type, 0 request, 1 reply, 2 subscribe, 3 event, unsubscribe, 5 error
            'i': requestId,  # sequence number identifies an individual request or request-and-response pair, to your application
            'n': name,  # function name is the name of the function being called or that the server is responding to, the server echoes your call
            'o': self.json(payload),  # JSON-formatted string containing the data being sent with the message
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'name': name,
            'symbol': symbol,
            'marketId': market['id'],
            'method': self.handle_order_book_subscription,
            'limit': limit,
            'params': params,
        }
        message = self.extend(request, params)
        orderbook = await self.watch(url, messageHash, message, messageHash, subscription)
        return orderbook.limit()

    def handle_order_book(self, client, message):
        #
        #     {
        #         m: 3,
        #         i: 2,
        #         n: 'Level2UpdateEvent',
        #         o: [[2,1,1608208308265,0,20782.49,1,25000,8,1,1]]
        #     }
        #
        payload = self.safe_value(message, 'o', [])
        #
        #     [
        #         0,   # 0 MDUpdateId
        #         1,   # 1 Number of Unique Accounts
        #         123,  # 2 ActionDateTime in Posix format X 1000
        #         0,   # 3 ActionType 0(New), 1(Update), 2(Delete)
        #         0.0,  # 4 LastTradePrice
        #         0,   # 5 Number of Orders
        #         0.0,  # 6 Price
        #         0,   # 7 ProductPairCode
        #         0.0,  # 8 Quantity
        #         0,   # 9 Side
        #     ],
        #
        firstBidAsk = self.safe_value(payload, 0, [])
        marketId = self.safe_string(firstBidAsk, 7)
        if marketId is None:
            return message
        market = self.safe_market(marketId)
        symbol = market['symbol']
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            return message
        timestamp = None
        nonce = None
        for i in range(0, len(payload)):
            bidask = payload[i]
            if timestamp is None:
                timestamp = self.safe_integer(bidask, 2)
            else:
                newTimestamp = self.safe_integer(bidask, 2)
                timestamp = max(timestamp, newTimestamp)
            if nonce is None:
                nonce = self.safe_integer(bidask, 0)
            else:
                newNonce = self.safe_integer(bidask, 0)
                nonce = max(nonce, newNonce)
            # 0 new, 1 update, 2 remove
            type = self.safe_integer(bidask, 3)
            price = self.safe_float(bidask, 6)
            amount = self.safe_float(bidask, 8)
            side = self.safe_integer(bidask, 9)
            # 0 buy, 1 sell, 2 short reserved for future use, 3 unknown
            orderbookSide = orderbook['bids'] if (side == 0) else orderbook['asks']
            # 0 new, 1 update, 2 remove
            if type == 0:
                orderbookSide.store(price, amount)
            elif type == 1:
                orderbookSide.store(price, amount)
            elif type == 2:
                orderbookSide.store(price, 0)
        orderbook['nonce'] = nonce
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        name = 'SubscribeLevel2'
        messageHash = name + ':' + marketId
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def handle_order_book_subscription(self, client, message, subscription):
        #
        #     {
        #         m: 1,
        #         i: 1,
        #         n: 'SubscribeLevel2',
        #         o: [[1,1,1608204295901,0,20782.49,1,18200,8,1,0]]
        #     }
        #
        payload = self.safe_value(message, 'o', [])
        #
        #     [
        #         [
        #             0,   # 0 MDUpdateId
        #             1,   # 1 Number of Unique Accounts
        #             123,  # 2 ActionDateTime in Posix format X 1000
        #             0,   # 3 ActionType 0(New), 1(Update), 2(Delete)
        #             0.0,  # 4 LastTradePrice
        #             0,   # 5 Number of Orders
        #             0.0,  # 6 Price
        #             0,   # 7 ProductPairCode
        #             0.0,  # 8 Quantity
        #             0,   # 9 Side
        #         ],
        #     ]
        #
        symbol = self.safe_string(subscription, 'symbol')
        snapshot = self.parse_order_book(payload, symbol)
        limit = self.safe_integer(subscription, 'limit')
        orderbook = self.order_book(snapshot, limit)
        self.orderbooks[symbol] = orderbook
        messageHash = self.safe_string(subscription, 'messageHash')
        client.resolve(orderbook, messageHash)

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         m: 1,
        #         i: 1,
        #         n: 'SubscribeLevel2',
        #         o: '[[1,1,1608204295901,0,20782.49,1,18200,8,1,0]]'
        #     }
        #
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        id = self.safe_integer(message, 'i')
        subscription = self.safe_value(subscriptionsById, id)
        if subscription is not None:
            method = self.safe_value(subscription, 'method')
            if method is None:
                return message
            else:
                return method(client, message, subscription)

    def handle_message(self, client, message):
        #
        #     {
        #         "m": 0,  # message type, 0 request, 1 reply, 2 subscribe, 3 event, unsubscribe, 5 error
        #         "i": 0,  # sequence number identifies an individual request or request-and-response pair, to your application
        #         "n":"function name",  # function name is the name of the function being called or that the server is responding to, the server echoes your call
        #         "o":"payload",  # JSON-formatted string containing the data being sent with the message
        #     }
        #
        #     {
        #         m: 1,
        #         i: 1,
        #         n: 'SubscribeLevel2',
        #         o: '[[1,1,1608204295901,0,20782.49,1,18200,8,1,0]]'
        #     }
        #
        #     {
        #         m: 3,
        #         i: 2,
        #         n: 'Level2UpdateEvent',
        #         o: '[[2,1,1608208308265,0,20782.49,1,25000,8,1,1]]'
        #     }
        #
        payload = self.safe_string(message, 'o')
        if payload is None:
            return message
        message['o'] = json.loads(payload)
        methods = {
            'SubscribeLevel2': self.handle_subscription_status,
            'SubscribeLevel1': self.handle_ticker,
            'Level2UpdateEvent': self.handle_order_book,
            'Level1UpdateEvent': self.handle_ticker,
            'SubscribeTrades': self.handle_trades,
            'TradeDataUpdateEvent': self.handle_trades,
            'SubscribeTicker': self.handle_ohlcv,
            'TickerDataUpdateEvent': self.handle_ohlcv,
        }
        event = self.safe_string(message, 'n')
        method = self.safe_value(methods, event)
        if method is None:
            return message
        else:
            return method(client, message)
