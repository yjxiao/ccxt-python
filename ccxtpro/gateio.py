# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import NotSupported
from ccxt.base.errors import InvalidNonce


class gateio(Exchange, ccxt.gateio):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchTrades': True,
                'watchMyTrades': True,
                'watchOHLCV': True,
                'watchBalance': True,
                'watchOrders': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://ws.gate.io/v4',
                    'spot': 'wss://api.gateio.ws/ws/v4/',
                    'swap': {
                        'usdt': 'wss://fx-ws.gateio.ws/v4/ws/usdt',
                        'btc': 'wss://fx-ws.gateio.ws/v4/ws/btc',
                    },
                    'future': {
                        'usdt': 'wss://fx-ws.gateio.ws/v4/ws/delivery/usdt',
                        'btc': 'wss://fx-ws.gateio.ws/v4/ws/delivery/btc',
                    },
                    'option': 'wss://op-ws.gateio.live/v4/ws',
                },
                'test': {
                    'swap': {
                        'usdt': 'wss://fx-ws-testnet.gateio.ws/v4/ws/usdt',
                        'btc': 'wss://fx-ws-testnet.gateio.ws/v4/ws/btc',
                    },
                    'future': {
                        'usdt': 'wss://fx-ws-testnet.gateio.ws/v4/ws/usdt',
                        'btc': 'wss://fx-ws-testnet.gateio.ws/v4/ws/btc',
                    },
                    'option': 'wss://op-ws-testnet.gateio.live/v4/ws',
                },
            },
            'options': {
                'tradesLimit': 1000,
                'OHLCVLimit': 1000,
                'watchTradesSubscriptions': {},
                'watchTickerSubscriptions': {},
                'watchOrderBookSubscriptions': {},
                'watchOrderBook': {
                    'interval': '100ms',
                },
            },
            'exceptions': {
                'ws': {
                    'exact': {
                        '2': BadRequest,
                        '4': AuthenticationError,
                        '6': AuthenticationError,
                        '11': AuthenticationError,
                    },
                },
            },
        })

    async def watch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        marketId = market['id']
        options = self.safe_value(self.options, 'watchOrderBook', {})
        defaultLimit = self.safe_integer(options, 'limit', 20)
        if not limit:
            limit = defaultLimit
        defaultInterval = self.safe_string(options, 'interval', '100ms')
        interval = self.safe_string(params, 'interval', defaultInterval)
        type = market['type']
        messageType = self.get_uniform_type(type)
        method = messageType + '.' + 'order_book_update'
        messageHash = method + ':' + market['symbol']
        url = self.get_url_by_market_type(type, market['inverse'])
        payload = [marketId, interval]
        if type != 'spot':
            # contract pairs require limit in the payload
            stringLimit = str(limit)
            payload.append(stringLimit)
        subscriptionParams = {
            'method': self.handle_order_book_subscription,
            'symbol': symbol,
            'limit': limit,
        }
        orderbook = await self.subscribe_public(url, method, messageHash, payload, subscriptionParams)
        return orderbook.limit(limit)

    def handle_order_book_subscription(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({}, limit)
        options = self.safe_value(self.options, 'handleOrderBookSubscription', {})
        fetchOrderBookSnapshot = self.safe_value(options, 'fetchOrderBookSnapshot', False)
        if fetchOrderBookSnapshot:
            fetchingOrderBookSnapshot = 'fetchingOrderBookSnapshot'
            subscription[fetchingOrderBookSnapshot] = True
            messageHash = subscription['messageHash']
            client.subscriptions[messageHash] = subscription
            self.spawn(self.fetch_order_book_snapshot, client, message, subscription)

    async def fetch_order_book_snapshot(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        messageHash = self.safe_string(subscription, 'messageHash')
        try:
            snapshot = await self.fetch_order_book(symbol, limit)
            orderbook = self.orderbooks[symbol]
            messages = orderbook.cache
            firstMessage = self.safe_value(messages, 0, {})
            result = self.safe_value(firstMessage, 'result')
            seqNum = self.safe_integer(result, 'U')
            nonce = self.safe_integer(snapshot, 'nonce')
            # if the received snapshot is earlier than the first cached delta
            # then we cannot align it with the cached deltas and we need to
            # retry synchronizing in maxAttempts
            if (seqNum is None) or (nonce < seqNum):
                maxAttempts = self.safe_integer(self.options, 'maxOrderBookSyncAttempts', 3)
                numAttempts = self.safe_integer(subscription, 'numAttempts', 0)
                # retry to synchronize if we haven't reached maxAttempts yet
                if numAttempts < maxAttempts:
                    # safety guard
                    if messageHash in client.subscriptions:
                        numAttempts = self.sum(numAttempts, 1)
                        subscription['numAttempts'] = numAttempts
                        client.subscriptions[messageHash] = subscription
                        self.spawn(self.fetch_order_book_snapshot, client, message, subscription)
                else:
                    # raise upon failing to synchronize in maxAttempts
                    raise InvalidNonce(self.id + ' failed to synchronize WebSocket feed with the snapshot for symbol ' + symbol + ' in ' + str(maxAttempts) + ' attempts')
            else:
                orderbook.reset(snapshot)
                # unroll the accumulated deltas
                for i in range(0, len(messages)):
                    message = messages[i]
                    self.handle_order_book_message(client, message, orderbook)
                self.orderbooks[symbol] = orderbook
                client.resolve(orderbook, messageHash)
        except Exception as e:
            client.reject(e, messageHash)

    def handle_order_book(self, client, message):
        #
        #     {
        #         "time":1649770575,
        #         "channel":"spot.order_book_update",
        #         "event":"update",
        #         "result":{
        #             "t":1649770575537,
        #             "e":"depthUpdate",
        #             "E":1649770575,
        #             "s":"LTC_USDT",
        #             "U":2622528153,
        #             "u":2622528265,
        #             "b":[
        #                 ["104.18","3.9398"],
        #                 ["104.56","19.0603"],
        #                 ["104.94","0"],
        #                 ["103.72","0"],
        #                 ["105.01","52.6186"],
        #                 ["104.76","0"],
        #                 ["104.97","0"],
        #                 ["104.71","0"],
        #                 ["104.84","25.8604"],
        #                 ["104.51","47.6508"],
        #             ],
        #             "a":[
        #                 ["105.26","40.5519"],
        #                 ["106.08","35.4396"],
        #                 ["105.2","0"],
        #                 ["105.45","8.5834"],
        #                 ["105.5","20.17"],
        #                 ["105.11","54.8359"],
        #                 ["105.52","28.5605"],
        #                 ["105.27","6.6325"],
        #                 ["105.3","4.291446"],
        #                 ["106.03","9.712"],
        #             ]
        #         }
        #     }
        #
        channel = self.safe_string(message, 'channel')
        result = self.safe_value(message, 'result')
        marketId = self.safe_string(result, 's')
        symbol = self.safe_symbol(marketId)
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            orderbook = self.order_book({})
            self.orderbooks[symbol] = orderbook
        messageHash = channel + ':' + symbol
        subscription = self.safe_value(client.subscriptions, messageHash, {})
        fetchingOrderBookSnapshot = 'fetchingOrderBookSnapshot'
        isFetchingOrderBookSnapshot = self.safe_value(subscription, fetchingOrderBookSnapshot, False)
        if not isFetchingOrderBookSnapshot:
            subscription[fetchingOrderBookSnapshot] = True
            client.subscriptions[messageHash] = subscription
            self.spawn(self.fetch_order_book_snapshot, client, message, subscription)
        if orderbook['nonce'] is None:
            orderbook.cache.append(message)
        else:
            messageHash = channel + ':' + symbol
            self.handle_order_book_message(client, message, orderbook, messageHash)

    def handle_order_book_message(self, client, message, orderbook, messageHash=None):
        #
        # spot
        #
        #     {
        #         time: 1650189272,
        #         channel: 'spot.order_book_update',
        #         event: 'update',
        #         result: {
        #             t: 1650189272515,
        #             e: 'depthUpdate',
        #             E: 1650189272,
        #             s: 'GMT_USDT',
        #             U: 140595902,
        #             u: 140595902,
        #             b: [
        #                 ['2.51518', '228.119'],
        #                 ['2.50587', '1510.11'],
        #                 ['2.49944', '67.6'],
        #             ],
        #             a: [
        #                 ['2.5182', '4.199'],
        #                 ['2.51926', '1874'],
        #                 ['2.53528', '96.529'],
        #             ]
        #         }
        #     }
        #
        # swap
        #
        #     {
        #         id: null,
        #         time: 1650188898,
        #         channel: 'futures.order_book_update',
        #         event: 'update',
        #         error: null,
        #         result: {
        #             t: 1650188898938,
        #             s: 'GMT_USDT',
        #             U: 1577718307,
        #             u: 1577719254,
        #             b: [
        #                 {p: '2.5178', s: 0},
        #                 {p: '2.5179', s: 0},
        #                 {p: '2.518', s: 0},
        #             ],
        #             a: [
        #                 {p: '2.52', s: 0},
        #                 {p: '2.5201', s: 0},
        #                 {p: '2.5203', s: 0},
        #             ]
        #         }
        #     }
        #
        result = self.safe_value(message, 'result')
        prevSeqNum = self.safe_integer(result, 'U')
        seqNum = self.safe_integer(result, 'u')
        nonce = orderbook['nonce']
        # we have to add +1 because if the current seqNumber on iteration X is 5
        # on the iteration X+1, prevSeqNum will be(5+1)
        nextNonce = self.sum(nonce, 1)
        if (prevSeqNum <= nextNonce) and (seqNum >= nextNonce):
            asks = self.safe_value(result, 'a', [])
            bids = self.safe_value(result, 'b', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['nonce'] = seqNum
            timestamp = self.safe_integer(result, 't')
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            if messageHash is not None:
                client.resolve(orderbook, messageHash)
        return orderbook

    def handle_delta(self, bookside, delta):
        price = None
        amount = None
        if isinstance(delta, list):
            # spot
            price = self.safe_float(delta, 0)
            amount = self.safe_float(delta, 1)
        else:
            # swap
            price = self.safe_float(delta, 'p')
            amount = self.safe_float(delta, 's')
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        type = market['type']
        messageType = self.get_uniform_type(type)
        channel = messageType + '.' + 'tickers'
        messageHash = channel + '.' + market['symbol']
        payload = [marketId]
        url = self.get_url_by_market_type(type, market['inverse'])
        return await self.subscribe_public(url, channel, messageHash, payload)

    def handle_ticker(self, client, message):
        #
        #    {
        #        time: 1649326221,
        #        channel: 'spot.tickers',
        #        event: 'update',
        #        result: {
        #          currency_pair: 'BTC_USDT',
        #          last: '43444.82',
        #          lowest_ask: '43444.82',
        #          highest_bid: '43444.81',
        #          change_percentage: '-4.0036',
        #          base_volume: '5182.5412425462',
        #          quote_volume: '227267634.93123952',
        #          high_24h: '47698',
        #          low_24h: '42721.03'
        #        }
        #    }
        #
        channel = self.safe_string(message, 'channel')
        result = self.safe_value(message, 'result')
        if not isinstance(result, list):
            result = [result]
        for i in range(0, len(result)):
            ticker = result[i]
            parsed = self.parse_ticker(ticker)
            symbol = parsed['symbol']
            self.tickers[symbol] = parsed
            messageHash = channel + '.' + symbol
            client.resolve(self.tickers[symbol], messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        marketId = market['id']
        type = market['type']
        messageType = self.get_uniform_type(type)
        method = messageType + '.trades'
        messageHash = method
        if symbol is not None:
            messageHash += ':' + market['symbol']
        url = self.get_url_by_market_type(type, market['inverse'])
        payload = [marketId]
        trades = await self.subscribe_public(url, method, messageHash, payload)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        # {
        #     time: 1648725035,
        #     channel: 'spot.trades',
        #     event: 'update',
        #     result: [{
        #       id: 3130257995,
        #       create_time: 1648725035,
        #       create_time_ms: '1648725035923.0',
        #       side: 'sell',
        #       currency_pair: 'LTC_USDT',
        #       amount: '0.0116',
        #       price: '130.11'
        #     }]
        # }
        #
        channel = self.safe_string(message, 'channel')
        result = self.safe_value(message, 'result')
        if not isinstance(result, list):
            result = [result]
        parsedTrades = self.parse_trades(result)
        marketIds = {}
        for i in range(0, len(parsedTrades)):
            trade = parsedTrades[i]
            symbol = trade['symbol']
            cachedTrades = self.safe_value(self.trades, symbol)
            if cachedTrades is None:
                limit = self.safe_integer(self.options, 'tradesLimit', 1000)
                cachedTrades = ArrayCache(limit)
                self.trades[symbol] = cachedTrades
            cachedTrades.append(trade)
            marketIds[symbol] = True
        keys = list(marketIds.keys())
        for i in range(0, len(keys)):
            symbol = keys[i]
            hash = channel + ':' + symbol
            stored = self.safe_value(self.trades, symbol)
            client.resolve(stored, hash)
        client.resolve(self.trades, channel)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        marketId = market['id']
        type = market['type']
        interval = self.timeframes[timeframe]
        messageType = self.get_uniform_type(type)
        method = messageType + '.candlesticks'
        messageHash = method + ':' + interval + ':' + market['symbol']
        url = self.get_url_by_market_type(type, market['inverse'])
        payload = [interval, marketId]
        ohlcv = await self.subscribe_public(url, method, messageHash, payload)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        # {
        #     "time": 1606292600,
        #     "channel": "spot.candlesticks",
        #     "event": "update",
        #     "result": {
        #       "t": "1606292580",  # total volume
        #       "v": "2362.32035",  # volume
        #       "c": "19128.1",  # close
        #       "h": "19128.1",  # high
        #       "l": "19128.1",  # low
        #       "o": "19128.1",  # open
        #       "n": "1m_BTC_USDT"  # sub
        #     }
        #   }
        #
        channel = self.safe_string(message, 'channel')
        result = self.safe_value(message, 'result')
        isArray = isinstance(result, list)
        if not isArray:
            result = [result]
        marketIds = {}
        for i in range(0, len(result)):
            ohlcv = result[i]
            subscription = self.safe_string(ohlcv, 'n', '')
            parts = subscription.split('_')
            timeframe = self.safe_string(parts, 0)
            prefix = timeframe + '_'
            marketId = subscription.replace(prefix, '')
            symbol = self.safe_symbol(marketId, None, '_')
            parsed = self.parse_ohlcv(ohlcv)
            stored = self.safe_value(self.ohlcvs, symbol)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol] = stored
            stored.append(parsed)
            marketIds[symbol] = timeframe
        keys = list(marketIds.keys())
        for i in range(0, len(keys)):
            symbol = keys[i]
            timeframe = marketIds[symbol]
            interval = self.timeframes[timeframe]
            hash = channel + ':' + interval + ':' + symbol
            stored = self.safe_value(self.ohlcvs, symbol)
            client.resolve(stored, hash)

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']
        client = self.client(url)
        future = client.future('authenticated')
        method = 'server.sign'
        authenticate = self.safe_value(client.subscriptions, method)
        if authenticate is None:
            requestId = self.milliseconds()
            requestIdString = str(requestId)
            signature = self.hmac(self.encode(requestIdString), self.encode(self.secret), hashlib.sha512, 'hex')
            authenticateMessage = {
                'id': requestId,
                'method': method,
                'params': [self.apiKey, signature, requestId],
            }
            subscribe = {
                'id': requestId,
                'method': self.handle_authentication_message,
            }
            self.spawn(self.watch, url, requestId, authenticateMessage, method, subscribe)
        return await future

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        subType = None
        type = None
        marketId = 'not all'
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            type = market['type']
            marketId = market['id']
        else:
            type, params = self.handle_market_type_and_params('watchMyTrades', None, params)
            if type != 'spot':
                options = self.safe_value(self.options, 'watchMyTrades', {})
                subType = self.safe_value(options, 'subType', 'linear')
                subType = self.safe_value(params, 'subType', subType)
                params = self.omit(params, 'subType')
        messageType = self.get_uniform_type(type)
        method = messageType + '.usertrades'
        messageHash = method
        if symbol is not None:
            messageHash += ':' + symbol
        isInverse = (subType == 'inverse')
        url = self.get_url_by_market_type(type, isInverse)
        payload = [marketId]
        # uid required for non spot markets
        requiresUid = (type != 'spot')
        trades = await self.subscribe_private(url, method, messageHash, payload, requiresUid)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_my_trades(self, client, message):
        #
        # {
        #     "time": 1543205083,
        #     "channel": "futures.usertrades",
        #     "event": "update",
        #     "error": null,
        #     "result": [
        #       {
        #         "id": "3335259",
        #         "create_time": 1628736848,
        #         "create_time_ms": 1628736848321,
        #         "contract": "BTC_USD",
        #         "order_id": "4872460",
        #         "size": 1,
        #         "price": "40000.4",
        #         "role": "maker"
        #       }
        #     ]
        # }
        #
        result = self.safe_value(message, 'result', [])
        channel = self.safe_string(message, 'channel')
        tradesLength = len(result)
        if tradesLength == 0:
            return
        cachedTrades = self.myTrades
        if cachedTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            cachedTrades = ArrayCacheBySymbolById(limit)
        parsed = self.parse_trades(result)
        marketIds = {}
        for i in range(0, len(parsed)):
            trade = parsed[i]
            cachedTrades.append(trade)
            symbol = trade['symbol']
            marketIds[symbol] = True
        keys = list(marketIds.keys())
        for i in range(0, len(keys)):
            market = keys[i]
            hash = channel + ':' + market
            client.resolve(cachedTrades, hash)
        client.resolve(cachedTrades, channel)

    async def watch_balance(self, params={}):
        await self.load_markets()
        self.check_required_credentials()
        url = self.urls['api']['ws']
        await self.authenticate()
        requestId = self.nonce()
        method = 'balance.update'
        subscribeMessage = {
            'id': requestId,
            'method': 'balance.subscribe',
            'params': [],
        }
        subscription = {
            'id': requestId,
            'method': self.handle_balance_subscription,
        }
        return await self.watch(url, method, subscribeMessage, method, subscription)

    async def fetch_balance_snapshot(self):
        await self.load_markets()
        self.check_required_credentials()
        url = self.urls['api']['ws']
        await self.authenticate()
        requestId = self.nonce()
        method = 'balance.query'
        subscribeMessage = {
            'id': requestId,
            'method': method,
            'params': [],
        }
        subscription = {
            'id': requestId,
            'method': self.handle_balance_snapshot,
        }
        return await self.watch(url, requestId, subscribeMessage, method, subscription)

    def handle_balance_snapshot(self, client, message):
        messageHash = self.safe_string(message, 'id')
        result = self.safe_value(message, 'result')
        self.handle_balance_message(client, messageHash, result)
        client.resolve(self.balance, 'balance.update')
        if 'balance.query' in client.subscriptions:
            del client.subscriptions['balance.query']

    def handle_balance(self, client, message):
        messageHash = message['method']
        result = message['params'][0]
        self.handle_balance_message(client, messageHash, result)

    def handle_balance_message(self, client, messageHash, result):
        keys = list(result.keys())
        for i in range(0, len(keys)):
            account = self.account()
            key = keys[i]
            code = self.safe_currency_code(key)
            balance = result[key]
            account['free'] = self.safe_string(balance, 'available')
            account['used'] = self.safe_string(balance, 'freeze')
            self.balance[code] = account
        self.balance = self.safe_balance(self.balance)
        client.resolve(self.balance, messageHash)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' watchOrders requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        type = 'spot'
        if market['future'] or market['swap']:
            type = 'futures'
        elif market['option']:
            type = 'options'
        method = type + '.orders'
        messageHash = method
        messageHash = method + ':' + market['id']
        url = self.get_url_by_market_type(market['type'], market['inverse'])
        payload = [market['id']]
        # uid required for non spot markets
        requiresUid = (type != 'spot')
        orders = await self.subscribe_private(url, method, messageHash, payload, requiresUid)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_since_limit(orders, since, limit, 'timestamp', True)

    def handle_order(self, client, message):
        #
        # {
        #     "time": 1605175506,
        #     "channel": "spot.orders",
        #     "event": "update",
        #     "result": [
        #       {
        #         "id": "30784435",
        #         "user": 123456,
        #         "text": "t-abc",
        #         "create_time": "1605175506",
        #         "create_time_ms": "1605175506123",
        #         "update_time": "1605175506",
        #         "update_time_ms": "1605175506123",
        #         "event": "put",
        #         "currency_pair": "BTC_USDT",
        #         "type": "limit",
        #         "account": "spot",
        #         "side": "sell",
        #         "amount": "1",
        #         "price": "10001",
        #         "time_in_force": "gtc",
        #         "left": "1",
        #         "filled_total": "0",
        #         "fee": "0",
        #         "fee_currency": "USDT",
        #         "point_fee": "0",
        #         "gt_fee": "0",
        #         "gt_discount": True,
        #         "rebated_fee": "0",
        #         "rebated_fee_currency": "USDT"
        #       }
        #     ]
        # }
        #
        orders = self.safe_value(message, 'result', [])
        channel = self.safe_string(message, 'channel')
        ordersLength = len(orders)
        if ordersLength > 0:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            if self.orders is None:
                self.orders = ArrayCacheBySymbolById(limit)
            stored = self.orders
            marketIds = {}
            parsedOrders = self.parse_orders(orders)
            for i in range(0, len(parsedOrders)):
                parsed = parsedOrders[i]
                # inject order status
                info = self.safe_value(parsed, 'info')
                event = self.safe_string(info, 'event')
                if event == 'put':
                    parsed['status'] = 'open'
                elif event == 'finish':
                    parsed['status'] = 'closed'
                stored.append(parsed)
                symbol = parsed['symbol']
                market = self.market(symbol)
                marketIds[market['id']] = True
            keys = list(marketIds.keys())
            for i in range(0, len(keys)):
                messageHash = channel + ':' + keys[i]
                client.resolve(self.orders, messageHash)

    def handle_authentication_message(self, client, message, subscription):
        result = self.safe_value(message, 'result')
        status = self.safe_string(result, 'status')
        if status == 'success':
            # client.resolve(True, 'authenticated') will del the future
            # we want to remember that we are authenticated in subsequent call to private methods
            future = self.safe_value(client.futures, 'authenticated')
            if future is not None:
                future.resolve(True)
        else:
            # del authenticate subscribeHash to release the "subscribe lock"
            # allows subsequent calls to subscribe to reauthenticate
            # avoids sending two authentication messages before receiving a reply
            error = AuthenticationError(self.id + ' handleAuthenticationMessage() error')
            client.reject(error, 'authenticated')
            if 'server.sign' in client.subscriptions:
                del client.subscriptions['server.sign']

    def handle_error_message(self, client, message):
        # {
        #     time: 1647274664,
        #     channel: 'futures.orders',
        #     event: 'subscribe',
        #     error: {code: 2, message: 'unknown contract BTC_USDT_20220318'},
        # }
        # {
        #     time: 1647276473,
        #     channel: 'futures.orders',
        #     event: 'subscribe',
        #     error: {
        #       code: 4,
        #       message: '{"label":"INVALID_KEY","message":"Invalid key provided"}\n'
        #     },
        #     result: null
        #   }
        error = self.safe_value(message, 'error', {})
        code = self.safe_integer(error, 'code')
        if code is not None:
            id = self.safe_string(message, 'id')
            subscriptionsById = self.index_by(client.subscriptions, 'id')
            subscription = self.safe_value(subscriptionsById, id)
            if subscription is not None:
                try:
                    self.throw_exactly_matched_exception(self.exceptions['ws']['exact'], code, self.json(message))
                except Exception as e:
                    messageHash = self.safe_string(subscription, 'messageHash')
                    client.reject(e, messageHash)
                    client.reject(e, id)
                    if id in client.subscriptions:
                        del client.subscriptions[id]

    def handle_balance_subscription(self, client, message, subscription):
        self.spawn(self.fetch_balance_snapshot)

    def handle_subscription_status(self, client, message):
        messageId = self.safe_integer(message, 'id')
        if messageId is not None:
            subscriptionsById = self.index_by(client.subscriptions, 'id')
            subscription = self.safe_value(subscriptionsById, messageId, {})
            method = self.safe_value(subscription, 'method')
            if method is not None:
                method(client, message, subscription)
            client.resolve(message, messageId)

    def handle_message(self, client, message):
        #
        # subscribe
        # {
        #     time: 1649062304,
        #     id: 1649062303,
        #     channel: 'spot.candlesticks',
        #     event: 'subscribe',
        #     result: {status: 'success'}
        # }
        # candlestick
        # {
        #     time: 1649063328,
        #     channel: 'spot.candlesticks',
        #     event: 'update',
        #     result: {
        #       t: '1649063280',
        #       v: '58932.23174896',
        #       c: '45966.47',
        #       h: '45997.24',
        #       l: '45966.47',
        #       o: '45975.18',
        #       n: '1m_BTC_USDT',
        #       a: '1.281699'
        #     }
        #  }
        # orders
        # {
        #     "time": 1630654851,
        #     "channel": "options.orders", or futures.orders or spot.orders
        #     "event": "update",
        #     "result": [
        #        {
        #           "contract": "BTC_USDT-20211130-65000-C",
        #           "create_time": 1637897000,
        #             (...)
        #     ]
        # }
        # orderbook
        # {
        #     time: 1649770525,
        #     channel: 'spot.order_book_update',
        #     event: 'update',
        #     result: {
        #       t: 1649770525653,
        #       e: 'depthUpdate',
        #       E: 1649770525,
        #       s: 'LTC_USDT',
        #       U: 2622525645,
        #       u: 2622525665,
        #       b: [
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array]
        #       ],
        #       a: [
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array], [Array],
        #         [Array]
        #       ]
        #     }
        #   }
        self.handle_error_message(client, message)
        methods = {
            # missing migration to v4
            'balance.update': self.handle_balance,
        }
        methodType = self.safe_string(message, 'method')
        method = self.safe_value(methods, methodType)
        if method is None:
            event = self.safe_string(message, 'event')
            if event == 'subscribe':
                self.handle_subscription_status(client, message)
                return
            channel = self.safe_string(message, 'channel', '')
            channelParts = channel.split('.')
            channelType = self.safe_value(channelParts, 1)
            v4Methods = {
                'usertrades': self.handle_my_trades,
                'candlesticks': self.handle_ohlcv,
                'orders': self.handle_order,
                'tickers': self.handle_ticker,
                'trades': self.handle_trades,
                'order_book_update': self.handle_order_book,
            }
            method = self.safe_value(v4Methods, channelType)
        if method is not None:
            method(client, message)

    def get_uniform_type(self, type):
        uniformType = 'spot'
        if type == 'future' or type == 'swap':
            uniformType = 'futures'
        elif type == 'option':
            uniformType = 'options'
        return uniformType

    def get_url_by_market_type(self, type, isInverse=False):
        if type == 'spot':
            spotUrl = self.urls['api']['spot']
            if spotUrl is None:
                raise NotSupported(self.id + ' does not have a testnet for the ' + type + ' market type.')
            return spotUrl
        if type == 'swap':
            baseUrl = self.urls['api']['swap']
            return baseUrl['btc'] if isInverse else baseUrl['usdt']
        if type == 'future':
            baseUrl = self.urls['api']['future']
            return baseUrl['btc'] if isInverse else baseUrl['usdt']
        if type == 'option':
            return self.urls['api']['option']

    def request_id(self):
        # their support said that reqid must be an int32, not documented
        reqid = self.sum(self.safe_integer(self.options, 'reqid', 0), 1)
        self.options['reqid'] = reqid
        return reqid

    async def subscribe_public(self, url, channel, messageHash, payload, subscriptionParams={}):
        requestId = self.request_id()
        time = self.seconds()
        request = {
            'id': requestId,
            'time': time,
            'channel': channel,
            'event': 'subscribe',
            'payload': payload,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
        }
        subscription = self.extend(subscription, subscriptionParams)
        return await self.watch(url, messageHash, request, messageHash, subscription)

    async def subscribe_private(self, url, channel, messageHash, payload, requiresUid=False):
        self.check_required_credentials()
        # uid is required for some subscriptions only so it's not a part of required credentials
        if requiresUid:
            if self.uid is None or len(self.uid) == 0:
                raise ArgumentsRequired(self.id + ' requires uid to subscribe')
            idArray = [self.uid]
            payload = self.array_concat(idArray, payload)
        time = self.seconds()
        event = 'subscribe'
        signaturePayload = 'channel=' + channel + '&' + 'event=' + event + '&' + 'time=' + str(time)
        signature = self.hmac(self.encode(signaturePayload), self.encode(self.secret), hashlib.sha512, 'hex')
        auth = {
            'method': 'api_key',
            'KEY': self.apiKey,
            'SIGN': signature,
        }
        requestId = self.request_id()
        request = {
            'id': requestId,
            'time': time,
            'channel': channel,
            'event': 'subscribe',
            'payload': payload,
            'auth': auth,
        }
        subscription = {
            'id': requestId,
            'messageHash': messageHash,
        }
        return await self.watch(url, messageHash, request, messageHash, subscription)
