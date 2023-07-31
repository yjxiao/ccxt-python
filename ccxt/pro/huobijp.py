# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheByTimestamp
from ccxt.async_support.base.ws.client import Client
from typing import Optional
from ccxt.base.errors import ExchangeError


class huobijp(ccxt.async_support.huobijp):

    def describe(self):
        return self.deep_extend(super(huobijp, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTickers': False,  # for now
                'watchTicker': True,
                'watchTrades': True,
                'watchBalance': False,  # for now
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'api': {
                            'public': 'wss://{hostname}/ws',
                            'private': 'wss://{hostname}/ws/v2',
                        },
                    },
                },
            },
            'options': {
                'tradesLimit': 1000,
                'OHLCVLimit': 1000,
                'api': 'api',  # or api-aws for clients hosted on AWS
                'ws': {
                    'gunzip': True,
                },
            },
        })

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return str(requestId)

    async def watch_ticker(self, symbol: str, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the huobijp api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        # only supports a limit of 150 at self time
        messageHash = 'market.' + market['id'] + '.detail'
        api = self.safe_string(self.options, 'api', 'api')
        hostname = {'hostname': self.hostname}
        url = self.implode_params(self.urls['api']['ws'][api]['public'], hostname)
        requestId = self.request_id()
        request = {
            'sub': messageHash,
            'id': requestId,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'params': params,
        }
        return await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)

    def handle_ticker(self, client: Client, message):
        #
        #     {
        #         ch: 'market.btcusdt.detail',
        #         ts: 1583494163784,
        #         tick: {
        #             id: 209988464418,
        #             low: 8988,
        #             high: 9155.41,
        #             open: 9078.91,
        #             close: 9136.46,
        #             vol: 237813910.5928412,
        #             amount: 26184.202558551195,
        #             version: 209988464418,
        #             count: 265673
        #         }
        #     }
        #
        tick = self.safe_value(message, 'tick', {})
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        ticker = self.parse_ticker(tick, market)
        timestamp = self.safe_value(message, 'ts')
        ticker['timestamp'] = timestamp
        ticker['datetime'] = self.iso8601(timestamp)
        symbol = ticker['symbol']
        self.tickers[symbol] = ticker
        client.resolve(ticker, ch)
        return message

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the huobijp api endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        # only supports a limit of 150 at self time
        messageHash = 'market.' + market['id'] + '.trade.detail'
        api = self.safe_string(self.options, 'api', 'api')
        hostname = {'hostname': self.hostname}
        url = self.implode_params(self.urls['api']['ws'][api]['public'], hostname)
        requestId = self.request_id()
        request = {
            'sub': messageHash,
            'id': requestId,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'params': params,
        }
        trades = await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client: Client, message):
        #
        #     {
        #         ch: "market.btcusdt.trade.detail",
        #         ts: 1583495834011,
        #         tick: {
        #             id: 105004645372,
        #             ts: 1583495833751,
        #             data: [
        #                 {
        #                     id: 1.050046453727319e+22,
        #                     ts: 1583495833751,
        #                     tradeId: 102090727790,
        #                     amount: 0.003893,
        #                     price: 9150.01,
        #                     direction: "sell"
        #                 }
        #             ]
        #         }
        #     }
        #
        tick = self.safe_value(message, 'tick', {})
        data = self.safe_value(tick, 'data', {})
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        tradesCache = self.safe_value(self.trades, symbol)
        if tradesCache is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            tradesCache = ArrayCache(limit)
            self.trades[symbol] = tradesCache
        for i in range(0, len(data)):
            trade = self.parse_trade(data[i], market)
            tradesCache.append(trade)
        client.resolve(tradesCache, ch)
        return message

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the huobijp api endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        interval = self.safe_string(self.timeframes, timeframe, timeframe)
        messageHash = 'market.' + market['id'] + '.kline.' + interval
        api = self.safe_string(self.options, 'api', 'api')
        hostname = {'hostname': self.hostname}
        url = self.implode_params(self.urls['api']['ws'][api]['public'], hostname)
        requestId = self.request_id()
        request = {
            'sub': messageHash,
            'id': requestId,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'timeframe': timeframe,
            'params': params,
        }
        ohlcv = await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client: Client, message):
        #
        #     {
        #         ch: 'market.btcusdt.kline.1min',
        #         ts: 1583501786794,
        #         tick: {
        #             id: 1583501760,
        #             open: 9094.5,
        #             close: 9094.51,
        #             low: 9094.5,
        #             high: 9094.51,
        #             amount: 0.44639786263800907,
        #             vol: 4059.76919054,
        #             count: 16
        #         }
        #     }
        #
        ch = self.safe_string(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        interval = self.safe_string(parts, 3)
        timeframe = self.find_timeframe(interval)
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        tick = self.safe_value(message, 'tick')
        parsed = self.parse_ohlcv(tick, market)
        stored.append(parsed)
        client.resolve(stored, ch)

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the huobijp api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        if (limit is not None) and (limit != 150):
            raise ExchangeError(self.id + ' watchOrderBook accepts limit = 150 only')
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        # only supports a limit of 150 at self time
        limit = 150 if (limit is None) else limit
        messageHash = 'market.' + market['id'] + '.mbp.' + str(limit)
        api = self.safe_string(self.options, 'api', 'api')
        hostname = {'hostname': self.hostname}
        url = self.implode_params(self.urls['api']['ws'][api]['public'], hostname)
        requestId = self.request_id()
        request = {
            'sub': messageHash,
            'id': requestId,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
            'symbol': symbol,
            'limit': limit,
            'params': params,
            'method': self.handle_order_book_subscription,
        }
        orderbook = await self.watch(url, messageHash, self.extend(request, params), messageHash, subscription)
        return orderbook.limit()

    def handle_order_book_snapshot(self, client: Client, message, subscription):
        #
        #     {
        #         id: 1583473663565,
        #         rep: 'market.btcusdt.mbp.150',
        #         status: 'ok',
        #         data: {
        #             seqNum: 104999417756,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        symbol = self.safe_string(subscription, 'symbol')
        messageHash = self.safe_string(subscription, 'messageHash')
        orderbook = self.orderbooks[symbol]
        data = self.safe_value(message, 'data')
        snapshot = self.parse_order_book(data, symbol)
        snapshot['nonce'] = self.safe_integer(data, 'seqNum')
        orderbook.reset(snapshot)
        # unroll the accumulated deltas
        messages = orderbook.cache
        for i in range(0, len(messages)):
            message = messages[i]
            self.handle_order_book_message(client, message, orderbook)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    async def watch_order_book_snapshot(self, client, message, subscription):
        messageHash = self.safe_string(subscription, 'messageHash')
        try:
            symbol = self.safe_string(subscription, 'symbol')
            limit = self.safe_integer(subscription, 'limit')
            params = self.safe_value(subscription, 'params')
            api = self.safe_string(self.options, 'api', 'api')
            hostname = {'hostname': self.hostname}
            url = self.implode_params(self.urls['api']['ws'][api]['public'], hostname)
            requestId = self.request_id()
            request = {
                'req': messageHash,
                'id': requestId,
            }
            # self is a temporary subscription by a specific requestId
            # it has a very short lifetime until the snapshot is received over ws
            snapshotSubscription = {
                'id': requestId,
                'messageHash': messageHash,
                'symbol': symbol,
                'limit': limit,
                'params': params,
                'method': self.handle_order_book_snapshot,
            }
            orderbook = await self.watch(url, requestId, request, requestId, snapshotSubscription)
            return orderbook.limit()
        except Exception as e:
            del client.subscriptions[messageHash]
            client.reject(e, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client: Client, message, orderbook):
        #
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        tick = self.safe_value(message, 'tick', {})
        seqNum = self.safe_integer(tick, 'seqNum')
        prevSeqNum = self.safe_integer(tick, 'prevSeqNum')
        if (prevSeqNum <= orderbook['nonce']) and (seqNum > orderbook['nonce']):
            asks = self.safe_value(tick, 'asks', [])
            bids = self.safe_value(tick, 'bids', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['nonce'] = seqNum
            timestamp = self.safe_integer(message, 'ts')
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_order_book(self, client: Client, message):
        #
        # deltas
        #
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        messageHash = self.safe_string(message, 'ch')
        ch = self.safe_value(message, 'ch')
        parts = ch.split('.')
        marketId = self.safe_string(parts, 1)
        symbol = self.safe_symbol(marketId)
        orderbook = self.orderbooks[symbol]
        if orderbook['nonce'] is None:
            orderbook.cache.append(message)
        else:
            self.handle_order_book_message(client, message, orderbook)
            client.resolve(orderbook, messageHash)

    def handle_order_book_subscription(self, client: Client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({}, limit)
        # watch the snapshot in a separate async call
        self.spawn(self.watch_order_book_snapshot, client, message, subscription)

    def handle_subscription_status(self, client: Client, message):
        #
        #     {
        #         "id": 1583414227,
        #         "status": "ok",
        #         "subbed": "market.btcusdt.mbp.150",
        #         "ts": 1583414229143
        #     }
        #
        id = self.safe_string(message, 'id')
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        subscription = self.safe_value(subscriptionsById, id)
        if subscription is not None:
            method = self.safe_value(subscription, 'method')
            if method is not None:
                return method(client, message, subscription)
            # clean up
            if id in client.subscriptions:
                del client.subscriptions[id]
        return message

    def handle_system_status(self, client: Client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         id: '1578090234088',  # connectId
        #         type: 'welcome',
        #     }
        #
        return message

    def handle_subject(self, client: Client, message):
        #
        #     {
        #         ch: "market.btcusdt.mbp.150",
        #         ts: 1583472025885,
        #         tick: {
        #             seqNum: 104998984994,
        #             prevSeqNum: 104998984977,
        #             bids: [
        #                 [9058.27, 0],
        #                 [9058.43, 0],
        #                 [9058.99, 0],
        #             ],
        #             asks: [
        #                 [9084.27, 0.2],
        #                 [9085.69, 0],
        #                 [9085.81, 0],
        #             ]
        #         }
        #     }
        #
        ch = self.safe_value(message, 'ch')
        parts = ch.split('.')
        type = self.safe_string(parts, 0)
        if type == 'market':
            methodName = self.safe_string(parts, 2)
            methods = {
                'mbp': self.handle_order_book,
                'detail': self.handle_ticker,
                'trade': self.handle_trades,
                'kline': self.handle_ohlcv,
                # ...
            }
            method = self.safe_value(methods, methodName)
            if method is None:
                return message
            else:
                return method(client, message)

    async def pong(self, client, message):
        #
        #     {ping: 1583491673714}
        #
        await client.send({'pong': self.safe_integer(message, 'ping')})

    def handle_ping(self, client: Client, message):
        self.spawn(self.pong, client, message)

    def handle_error_message(self, client: Client, message):
        #
        #     {
        #         ts: 1586323747018,
        #         status: 'error',
        #         'err-code': 'bad-request',
        #         'err-msg': 'invalid mbp.150.symbol linkusdt',
        #         id: '2'
        #     }
        #
        status = self.safe_string(message, 'status')
        if status == 'error':
            id = self.safe_string(message, 'id')
            subscriptionsById = self.index_by(client.subscriptions, 'id')
            subscription = self.safe_value(subscriptionsById, id)
            if subscription is not None:
                errorCode = self.safe_string(message, 'err-code')
                try:
                    self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, self.json(message))
                except Exception as e:
                    messageHash = self.safe_string(subscription, 'messageHash')
                    client.reject(e, messageHash)
                    client.reject(e, id)
                    if id in client.subscriptions:
                        del client.subscriptions[id]
            return False
        return message

    def handle_message(self, client: Client, message):
        if self.handle_error_message(client, message):
            #
            #     {"id":1583414227,"status":"ok","subbed":"market.btcusdt.mbp.150","ts":1583414229143}
            #
            #           ________________________
            #
            # sometimes huobijp responds with half of a JSON response like
            #
            #     ' {"ch":"market.ethbtc.m '
            #
            # self is passed to handleMessage string since it failed to be decoded
            #
            if self.safe_string(message, 'id') is not None:
                self.handle_subscription_status(client, message)
            elif self.safe_string(message, 'ch') is not None:
                # route by channel aka topic aka subject
                self.handle_subject(client, message)
            elif self.safe_string(message, 'ping') is not None:
                self.handle_ping(client, message)
