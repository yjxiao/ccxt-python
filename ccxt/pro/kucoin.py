# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.async_support.base.ws.client import Client
from typing import Optional
from ccxt.base.errors import ExchangeError


class kucoin(ccxt.async_support.kucoin):

    def describe(self):
        return self.deep_extend(super(kucoin, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchMyTrades': True,
                'watchTickers': False,  # for now
                'watchTicker': True,
                'watchTrades': True,
                'watchBalance': True,
                'watchOHLCV': True,
            },
            'options': {
                'tradesLimit': 1000,
                'watchTicker': {
                    'name': 'market/snapshot',  # market/ticker
                },
                'watchOrderBook': {
                    'snapshotDelay': 5,
                    'snapshotMaxRetries': 3,
                },
            },
            'streaming': {
                # kucoin does not support built-in ws protocol-level ping-pong
                # instead it requires a custom json-based text ping-pong
                # https://docs.kucoin.com/#ping
                'ping': self.ping,
            },
        })

    def negotiate(self, privateChannel, params={}):
        connectId = 'private' if privateChannel else 'public'
        urls = self.safe_value(self.options, 'urls', {})
        if connectId in urls:
            return urls[connectId]
        # we store an awaitable to the url
        # so that multiple calls don't asynchronously
        # fetch different urls and overwrite each other
        urls[connectId] = self.spawn(self.negotiate_helper, privateChannel, params)
        self.options['urls'] = urls
        return urls[connectId]

    async def negotiate_helper(self, privateChannel, params={}):
        response = None
        connectId = 'private' if privateChannel else 'public'
        if privateChannel:
            response = await self.privatePostBulletPrivate(params)
            #
            #     {
            #         code: "200000",
            #         data: {
            #             instanceServers: [
            #                 {
            #                     pingInterval:  50000,
            #                     endpoint: "wss://push-private.kucoin.com/endpoint",
            #                     protocol: "websocket",
            #                     encrypt: True,
            #                     pingTimeout: 10000
            #                 }
            #             ],
            #             token: "2neAiuYvAU61ZDXANAGAsiL4-iAExhsBXZxftpOeh_55i3Ysy2q2LEsEWU64mdzUOPusi34M_wGoSf7iNyEWJ1UQy47YbpY4zVdzilNP-Bj3iXzrjjGlWtiYB9J6i9GjsxUuhPw3BlrzazF6ghq4Lzf7scStOz3KkxjwpsOBCH4=.WNQmhZQeUKIkh97KYgU0Lg=="
            #         }
            #     }
            #
        else:
            response = await self.publicPostBulletPublic(params)
        data = self.safe_value(response, 'data', {})
        instanceServers = self.safe_value(data, 'instanceServers', [])
        firstInstanceServer = self.safe_value(instanceServers, 0)
        pingInterval = self.safe_integer(firstInstanceServer, 'pingInterval')
        endpoint = self.safe_string(firstInstanceServer, 'endpoint')
        token = self.safe_string(data, 'token')
        result = endpoint + '?' + self.urlencode({
            'token': token,
            'privateChannel': privateChannel,
            'connectId': connectId,
        })
        client = self.client(result)
        client.keepAlive = pingInterval
        return result

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return requestId

    async def subscribe(self, url, messageHash, subscriptionHash, params={}, subscription=None):
        requestId = str(self.request_id())
        request = {
            'id': requestId,
            'type': 'subscribe',
            'topic': subscriptionHash,
            'response': True,
        }
        message = self.extend(request, params)
        client = self.client(url)
        if not (subscriptionHash in client.subscriptions):
            client.subscriptions[requestId] = subscriptionHash
        return await self.watch(url, messageHash, message, subscriptionHash, subscription)

    async def watch_ticker(self, symbol: str, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = await self.negotiate(False)
        method, query = self.handle_option_and_params(params, 'watchTicker', 'method', '/market/snapshot')
        topic = method + ':' + market['id']
        messageHash = 'ticker:' + symbol
        return await self.subscribe(url, messageHash, topic, query)

    def handle_ticker(self, client: Client, message):
        #
        # market/snapshot
        #
        # updates come in every 2 sec unless there
        # were no changes since the previous update
        #
        #     {
        #         "data": {
        #             "sequence": "1545896669291",
        #             "data": {
        #                 "trading": True,
        #                 "symbol": "KCS-BTC",
        #                 "buy": 0.00011,
        #                 "sell": 0.00012,
        #                 "sort": 100,
        #                 "volValue": 3.13851792584,  # total
        #                 "baseCurrency": "KCS",
        #                 "market": "BTC",
        #                 "quoteCurrency": "BTC",
        #                 "symbolCode": "KCS-BTC",
        #                 "datetime": 1548388122031,
        #                 "high": 0.00013,
        #                 "vol": 27514.34842,
        #                 "low": 0.0001,
        #                 "changePrice": -1.0e-5,
        #                 "changeRate": -0.0769,
        #                 "lastTradedPrice": 0.00012,
        #                 "board": 0,
        #                 "mark": 0
        #             }
        #         },
        #         "subject": "trade.snapshot",
        #         "topic": "/market/snapshot:KCS-BTC",
        #         "type": "message"
        #     }
        #
        # market/ticker
        #
        #     {
        #         type: 'message',
        #         topic: '/market/ticker:BTC-USDT',
        #         subject: 'trade.ticker',
        #         data: {
        #             bestAsk: '62163',
        #             bestAskSize: '0.99011388',
        #             bestBid: '62162.9',
        #             bestBidSize: '0.04794181',
        #             price: '62162.9',
        #             sequence: '1621383371852',
        #             size: '0.00832274',
        #             time: 1634641987564
        #         }
        #     }
        #
        topic = self.safe_string(message, 'topic')
        market = None
        if topic is not None:
            parts = topic.split(':')
            marketId = self.safe_string(parts, 1)
            market = self.safe_market(marketId, market, '-')
        data = self.safe_value(message, 'data', {})
        rawTicker = self.safe_value(data, 'data', data)
        ticker = self.parse_ticker(rawTicker, market)
        symbol = ticker['symbol']
        self.tickers[symbol] = ticker
        messageHash = 'ticker:' + symbol
        client.resolve(ticker, messageHash)

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        url = await self.negotiate(False)
        market = self.market(symbol)
        symbol = market['symbol']
        period = self.safe_string(self.timeframes, timeframe, timeframe)
        topic = '/market/candles:' + market['id'] + '_' + period
        messageHash = 'candles:' + symbol + ':' + timeframe
        ohlcv = await self.subscribe(url, messageHash, topic, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client: Client, message):
        #
        #     {
        #         data: {
        #             symbol: 'BTC-USDT',
        #             candles: [
        #                 '1624881240',
        #                 '34138.8',
        #                 '34121.6',
        #                 '34138.8',
        #                 '34097.9',
        #                 '3.06097133',
        #                 '104430.955068564'
        #             ],
        #             time: 1624881284466023700
        #         },
        #         subject: 'trade.candles.update',
        #         topic: '/market/candles:BTC-USDT_1min',
        #         type: 'message'
        #     }
        #
        data = self.safe_value(message, 'data', {})
        marketId = self.safe_string(data, 'symbol')
        candles = self.safe_value(data, 'candles', [])
        topic = self.safe_string(message, 'topic')
        parts = topic.split('_')
        interval = self.safe_string(parts, 1)
        # use a reverse lookup in a static map instead
        timeframe = self.find_timeframe(interval)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        messageHash = 'candles:' + symbol + ':' + timeframe
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        ohlcv = self.parse_ohlcv(candles, market)
        stored.append(ohlcv)
        client.resolve(stored, messageHash)

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        url = await self.negotiate(False)
        market = self.market(symbol)
        symbol = market['symbol']
        topic = '/market/match:' + market['id']
        messageHash = 'trades:' + symbol
        trades = await self.subscribe(url, messageHash, topic, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trade(self, client: Client, message):
        #
        #     {
        #         data: {
        #             sequence: '1568787654360',
        #             symbol: 'BTC-USDT',
        #             side: 'buy',
        #             size: '0.00536577',
        #             price: '9345',
        #             takerOrderId: '5e356c4a9f1a790008f8d921',
        #             time: '1580559434436443257',
        #             type: 'match',
        #             makerOrderId: '5e356bffedf0010008fa5d7f',
        #             tradeId: '5e356c4aeefabd62c62a1ece'
        #         },
        #         subject: 'trade.l3match',
        #         topic: '/market/match:BTC-USDT',
        #         type: 'message'
        #     }
        #
        data = self.safe_value(message, 'data', {})
        trade = self.parse_trade(data)
        symbol = trade['symbol']
        messageHash = 'trades:' + symbol
        trades = self.safe_value(self.trades, symbol)
        if trades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            trades = ArrayCache(limit)
            self.trades[symbol] = trades
        trades.append(trade)
        client.resolve(trades, messageHash)

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        #
        # https://docs.kucoin.com/#level-2-market-data
        #
        # 1. After receiving the websocket Level 2 data flow, cache the data.
        # 2. Initiate a REST request to get the snapshot data of Level 2 order book.
        # 3. Playback the cached Level 2 data flow.
        # 4. Apply the new Level 2 data flow to the local snapshot to ensure that
        # the sequence of the new Level 2 update lines up with the sequence of
        # the previous Level 2 data. Discard all the message prior to that
        # sequence, and then playback the change to snapshot.
        # 5. Update the level2 full data based on sequence according to the
        # size. If the price is 0, ignore the messages and update the sequence.
        # If the size=0, update the sequence and remove the price of which the
        # size is 0 out of level 2. Fr other cases, please update the price.
        #
        if limit is not None:
            if (limit != 20) and (limit != 100):
                raise ExchangeError(self.id + " watchOrderBook 'limit' argument must be None, 20 or 100")
        await self.load_markets()
        url = await self.negotiate(False)
        market = self.market(symbol)
        symbol = market['symbol']
        topic = '/market/level2:' + market['id']
        messageHash = 'orderbook:' + symbol
        subscription = {
            'method': self.handle_order_book_subscription,
            'symbol': symbol,
            'limit': limit,
        }
        orderbook = await self.subscribe(url, messageHash, topic, params, subscription)
        return orderbook.limit()

    def handle_order_book(self, client: Client, message):
        #
        # initial snapshot is fetched with ccxt's fetchOrderBook
        # the feed does not include a snapshot, just the deltas
        #
        #     {
        #         "type":"message",
        #         "topic":"/market/level2:BTC-USDT",
        #         "subject":"trade.l2update",
        #         "data":{
        #             "sequenceStart":1545896669105,
        #             "sequenceEnd":1545896669106,
        #             "symbol":"BTC-USDT",
        #             "changes": {
        #                 "asks": [["6","1","1545896669105"]],  # price, size, sequence
        #                 "bids": [["4","1","1545896669106"]]
        #             }
        #         }
        #     }
        #
        data = self.safe_value(message, 'data')
        marketId = self.safe_string(data, 'symbol')
        symbol = self.safe_symbol(marketId, None, '-')
        messageHash = 'orderbook:' + symbol
        storedOrderBook = self.orderbooks[symbol]
        nonce = self.safe_integer(storedOrderBook, 'nonce')
        deltaEnd = self.safe_integer(data, 'sequenceEnd')
        if nonce is None:
            cacheLength = len(storedOrderBook.cache)
            topic = self.safe_string(message, 'topic')
            subscription = client.subscriptions[topic]
            limit = self.safe_integer(subscription, 'limit')
            snapshotDelay = self.handle_option('watchOrderBook', 'snapshotDelay', 5)
            if cacheLength == snapshotDelay:
                self.spawn(self.load_order_book, client, messageHash, symbol, limit)
            storedOrderBook.cache.append(data)
            return
        elif nonce >= deltaEnd:
            return
        self.handle_delta(storedOrderBook, data)
        client.resolve(storedOrderBook, messageHash)

    def get_cache_index(self, orderbook, cache):
        firstDelta = self.safe_value(cache, 0)
        nonce = self.safe_integer(orderbook, 'nonce')
        firstDeltaStart = self.safe_integer(firstDelta, 'sequenceStart')
        if nonce < firstDeltaStart - 1:
            return -1
        for i in range(0, len(cache)):
            delta = cache[i]
            deltaStart = self.safe_integer(delta, 'sequenceStart')
            deltaEnd = self.safe_integer(delta, 'sequenceEnd')
            if (nonce >= deltaStart - 1) and (nonce < deltaEnd):
                return i
        return len(cache)

    def handle_delta(self, orderbook, delta):
        orderbook['nonce'] = self.safe_integer(delta, 'sequenceEnd')
        timestamp = self.safe_integer(delta, 'time')
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        changes = self.safe_value(delta, 'changes')
        bids = self.safe_value(changes, 'bids', [])
        asks = self.safe_value(changes, 'asks', [])
        storedBids = orderbook['bids']
        storedAsks = orderbook['asks']
        self.handle_bid_asks(storedBids, bids)
        self.handle_bid_asks(storedAsks, asks)

    def handle_bid_asks(self, bookSide, bidAsks):
        for i in range(0, len(bidAsks)):
            bidAsk = self.parse_bid_ask(bidAsks[i])
            bookSide.storeArray(bidAsk)

    def handle_order_book_subscription(self, client: Client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        self.orderbooks[symbol] = self.order_book({}, limit)
        # moved snapshot initialization to handleOrderBook to fix
        # https://github.com/ccxt/ccxt/issues/6820
        # the general idea is to fetch the snapshot after the first delta
        # but not before, because otherwise we cannot synchronize the feed

    def handle_subscription_status(self, client: Client, message):
        #
        #     {
        #         id: '1578090438322',
        #         type: 'ack'
        #     }
        #
        id = self.safe_string(message, 'id')
        subscriptionHash = self.safe_string(client.subscriptions, id)
        subscription = self.safe_value(client.subscriptions, subscriptionHash)
        del client.subscriptions[id]
        method = self.safe_value(subscription, 'method')
        if method is not None:
            method(client, message, subscription)

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

    async def watch_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of  orde structures to retrieve
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        url = await self.negotiate(True)
        topic = '/spotMarket/tradeOrders'
        request = {
            'privateChannel': True,
        }
        messageHash = 'orders'
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash = messageHash + ':' + symbol
        orders = await self.subscribe(url, messageHash, topic, self.extend(request, params))
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def parse_ws_order_status(self, status):
        statuses = {
            'open': 'open',
            'filled': 'closed',
            'match': 'open',
            'update': 'open',
            'canceled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_ws_order(self, order, market=None):
        #
        #     {
        #         'symbol': 'XCAD-USDT',
        #         'orderType': 'limit',
        #         'side': 'buy',
        #         'orderId': '6249167327218b000135e749',
        #         'type': 'canceled',
        #         'orderTime': 1648957043065280224,
        #         'size': '100.452',
        #         'filledSize': '0',
        #         'price': '2.9635',
        #         'clientOid': 'buy-XCAD-USDT-1648957043010159',
        #         'remainSize': '0',
        #         'status': 'done',
        #         'ts': 1648957054031001037
        #     }
        #
        id = self.safe_string(order, 'orderId')
        clientOrderId = self.safe_string(order, 'clientOid')
        orderType = self.safe_string_lower(order, 'orderType')
        price = self.safe_string(order, 'price')
        filled = self.safe_string(order, 'filledSize')
        amount = self.safe_string(order, 'size')
        rawType = self.safe_string(order, 'type')
        status = self.parse_ws_order_status(rawType)
        timestamp = self.safe_integer(order, 'orderTime')
        marketId = self.safe_string(order, 'symbol')
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        side = self.safe_string_lower(order, 'side')
        return self.safe_order({
            'info': order,
            'symbol': symbol,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'type': orderType,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'amount': amount,
            'cost': None,
            'average': None,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': None,
            'trades': None,
        }, market)

    def handle_order(self, client: Client, message):
        messageHash = 'orders'
        data = self.safe_value(message, 'data')
        parsed = self.parse_ws_order(data)
        symbol = self.safe_string(parsed, 'symbol')
        orderId = self.safe_string(parsed, 'id')
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        cachedOrders = self.orders
        orders = self.safe_value(cachedOrders.hashmap, symbol, {})
        order = self.safe_value(orders, orderId)
        if order is not None:
            # todo add others to calculate average etc
            stopPrice = self.safe_value(order, 'stopPrice')
            if stopPrice is not None:
                parsed['stopPrice'] = stopPrice
            if order['status'] == 'closed':
                parsed['status'] = 'closed'
        cachedOrders.append(parsed)
        client.resolve(self.orders, messageHash)
        symbolSpecificMessageHash = messageHash + ':' + symbol
        client.resolve(self.orders, symbolSpecificMessageHash)

    async def watch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches information on multiple trades made by the user
        :param str symbol: unified market symbol of the market trades were made in
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trade structures to retrieve
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict[]: a list of [trade structures]{@link https://github.com/ccxt/ccxt/wiki/Manual#trade-structure
        """
        await self.load_markets()
        url = await self.negotiate(True)
        topic = '/spot/tradeFills'
        request = {
            'privateChannel': True,
        }
        messageHash = 'myTrades'
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash = messageHash + ':' + market['symbol']
        trades = await self.subscribe(url, messageHash, topic, self.extend(request, params))
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_my_trade(self, client: Client, message):
        trades = self.myTrades
        if trades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            trades = ArrayCacheBySymbolById(limit)
        data = self.safe_value(message, 'data')
        parsed = self.parse_ws_trade(data)
        trades.append(parsed)
        messageHash = 'myTrades'
        client.resolve(trades, messageHash)
        symbolSpecificMessageHash = messageHash + ':' + parsed['symbol']
        client.resolve(trades, symbolSpecificMessageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        # {
        #     fee: 0.00262148,
        #     feeCurrency: 'USDT',
        #     feeRate: 0.001,
        #     orderId: '62417436b29df8000183df2f',
        #     orderType: 'market',
        #     price: 131.074,
        #     side: 'sell',
        #     size: 0.02,
        #     symbol: 'LTC-USDT',
        #     time: '1648456758734571745',
        #     tradeId: '624174362e113d2f467b3043'
        #   }
        #
        marketId = self.safe_string(trade, 'symbol')
        market = self.safe_market(marketId, market, '-')
        symbol = market['symbol']
        type = self.safe_string(trade, 'orderType')
        side = self.safe_string(trade, 'side')
        tradeId = self.safe_string(trade, 'tradeId')
        price = self.safe_string(trade, 'price')
        amount = self.safe_string(trade, 'size')
        order = self.safe_string(trade, 'orderId')
        timestamp = self.safe_integer_product(trade, 'time', 0.000001)
        feeCurrency = market['quote']
        feeRate = self.safe_string(trade, 'feeRate')
        feeCost = self.safe_string(trade, 'fee')
        fee = {
            'cost': feeCost,
            'rate': feeRate,
            'currency': feeCurrency,
        }
        return self.safe_trade({
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': order,
            'type': type,
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': fee,
        }, market)

    async def watch_balance(self, params={}):
        """
        watch balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the kucoin api endpoint
        :returns dict: a `balance structure <https://github.com/ccxt/ccxt/wiki/Manual#balance-structure>`
        """
        await self.load_markets()
        url = await self.negotiate(True)
        topic = '/account/balance'
        request = {
            'privateChannel': True,
        }
        messageHash = 'balance'
        return await self.subscribe(url, messageHash, topic, self.extend(request, params))

    def handle_balance(self, client: Client, message):
        #
        # {
        #     "id":"6217a451294b030001e3a26a",
        #     "type":"message",
        #     "topic":"/account/balance",
        #     "userId":"6217707c52f97f00012a67db",
        #     "channelType":"private",
        #     "subject":"account.balance",
        #     "data":{
        #        "accountId":"62177fe67810720001db2f18",
        #        "available":"89",
        #        "availableChange":"-30",
        #        "currency":"USDT",
        #        "hold":"0",
        #        "holdChange":"0",
        #        "relationContext":{
        #        },
        #        "relationEvent":"main.transfer",
        #        "relationEventId":"6217a451294b030001e3a26a",
        #        "time":"1645716561816",
        #        "total":"89"
        #     }
        #
        data = self.safe_value(message, 'data', {})
        messageHash = 'balance'
        currencyId = self.safe_string(data, 'currency')
        relationEvent = self.safe_string(data, 'relationEvent')
        requestAccountType = None
        if relationEvent is not None:
            relationEventParts = relationEvent.split('.')
            requestAccountType = self.safe_string(relationEventParts, 0)
        selectedType = self.safe_string_2(self.options, 'watchBalance', 'defaultType', 'trade')  # trade, main, margin or other
        accountsByType = self.safe_value(self.options, 'accountsByType')
        uniformType = self.safe_string(accountsByType, requestAccountType, 'trade')
        if not (uniformType in self.balance):
            self.balance[uniformType] = {}
        self.balance[uniformType]['info'] = data
        timestamp = self.safe_integer(data, 'time')
        self.balance[uniformType]['timestamp'] = timestamp
        self.balance[uniformType]['datetime'] = self.iso8601(timestamp)
        code = self.safe_currency_code(currencyId)
        account = self.account()
        account['free'] = self.safe_string(data, 'available')
        account['used'] = self.safe_string(data, 'hold')
        account['total'] = self.safe_string(data, 'total')
        self.balance[uniformType][code] = account
        self.balance[uniformType] = self.safe_balance(self.balance[uniformType])
        if uniformType == selectedType:
            client.resolve(self.balance[uniformType], messageHash)

    def handle_subject(self, client: Client, message):
        #
        #     {
        #         "type":"message",
        #         "topic":"/market/level2:BTC-USDT",
        #         "subject":"trade.l2update",
        #         "data":{
        #             "sequenceStart":1545896669105,
        #             "sequenceEnd":1545896669106,
        #             "symbol":"BTC-USDT",
        #             "changes": {
        #                 "asks": [["6","1","1545896669105"]],  # price, size, sequence
        #                 "bids": [["4","1","1545896669106"]]
        #             }
        #         }
        #     }
        #
        subject = self.safe_string(message, 'subject')
        methods = {
            'trade.l2update': self.handle_order_book,
            'trade.ticker': self.handle_ticker,
            'trade.snapshot': self.handle_ticker,
            'trade.l3match': self.handle_trade,
            'trade.candles.update': self.handle_ohlcv,
            'account.balance': self.handle_balance,
            '/spot/tradeFills': self.handle_my_trade,
            'orderChange': self.handle_order,
        }
        method = self.safe_value(methods, subject)
        if method is None:
            return message
        else:
            return method(client, message)

    def ping(self, client):
        # kucoin does not support built-in ws protocol-level ping-pong
        # instead it requires a custom json-based text ping-pong
        # https://docs.kucoin.com/#ping
        id = str(self.request_id())
        return {
            'id': id,
            'type': 'ping',
        }

    def handle_pong(self, client: Client, message):
        client.lastPong = self.milliseconds()
        # https://docs.kucoin.com/#ping

    def handle_error_message(self, client: Client, message):
        #
        #    {
        #        id: '1',
        #        type: 'error',
        #        code: 415,
        #        data: 'type is not supported'
        #    }
        #
        data = self.safe_string(message, 'data', '')
        self.handle_errors(None, None, client.url, None, None, data, message, None, None)

    def handle_message(self, client: Client, message):
        type = self.safe_string(message, 'type')
        methods = {
            # 'heartbeat': self.handleHeartbeat,
            'welcome': self.handle_system_status,
            'ack': self.handle_subscription_status,
            'message': self.handle_subject,
            'pong': self.handle_pong,
            'error': self.handle_error_message,
        }
        method = self.safe_value(methods, type)
        if method is not None:
            return method(client, message)
