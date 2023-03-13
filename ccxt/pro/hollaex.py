# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import AuthenticationError


class hollaex(ccxt.async_support.hollaex):

    def describe(self):
        return self.deep_extend(super(hollaex, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchMyTrades': False,
                'watchOHLCV': False,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': False,
                'watchTickers': False,  # for now
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api.hollaex.com/stream',
                },
                'test': {
                    'ws': 'wss://api.sandbox.hollaex.com/stream',
                },
            },
            'options': {
                'watchBalance': {
                    # 'api-expires': None,
                },
                'watchOrders': {
                    # 'api-expires': None,
                },
            },
            'streaming': {
                'ping': self.ping,
            },
            'exceptions': {
                'ws': {
                    'exact': {
                        'Bearer or HMAC authentication required': BadSymbol,  # {error: 'Bearer or HMAC authentication required'}
                        'Error: wrong input': BadRequest,  # {error: 'Error: wrong input'}
                    },
                },
            },
        })

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the hollaex api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'orderbook' + ':' + market['id']
        orderbook = await self.watch_public(messageHash, params)
        return orderbook.limit()

    def handle_order_book(self, client, message):
        #
        #     {
        #         "topic":"orderbook",
        #         "action":"partial",
        #         "symbol":"ltc-usdt",
        #         "data":{
        #             "bids":[
        #                 [104.29, 5.2264],
        #                 [103.86,1.3629],
        #                 [101.82,0.5942]
        #             ],
        #             "asks":[
        #                 [104.81,9.5531],
        #                 [105.54,0.6416],
        #                 [106.18,1.4141],
        #             ],
        #             "timestamp":"2022-04-12T08:17:05.932Z"
        #         },
        #         "time":1649751425
        #     }
        #
        marketId = self.safe_string(message, 'symbol')
        channel = self.safe_string(message, 'topic')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        data = self.safe_value(message, 'data')
        timestamp = self.safe_string(data, 'timestamp')
        timestampMs = self.parse8601(timestamp)
        snapshot = self.parse_order_book(data, symbol, timestampMs)
        orderbook = None
        if not (symbol in self.orderbooks):
            orderbook = self.order_book(snapshot)
            self.orderbooks[symbol] = orderbook
        else:
            orderbook = self.orderbooks[symbol]
            orderbook.reset(snapshot)
        messageHash = channel + ':' + marketId
        client.resolve(orderbook, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the hollaex api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = 'trade' + ':' + market['id']
        trades = await self.watch_public(messageHash, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        #     {
        #         topic: 'trade',
        #         action: 'partial',
        #         symbol: 'btc-usdt',
        #         data: [
        #             {
        #                 size: 0.05145,
        #                 price: 41977.9,
        #                 side: 'buy',
        #                 timestamp: '2022-04-11T09:40:10.881Z'
        #             },
        #         ]
        #     }
        #
        channel = self.safe_string(message, 'topic')
        marketId = self.safe_string(message, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        data = self.safe_value(message, 'data', [])
        parsedTrades = self.parse_trades(data, market)
        for j in range(0, len(parsedTrades)):
            stored.append(parsedTrades[j])
        messageHash = channel + ':' + marketId
        client.resolve(stored, messageHash)
        client.resolve(stored, channel)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple trades made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the hollaex api endpoint
        :returns [dict]: a list of [order structures]{@link https://docs.ccxt.com/en/latest/manual.html#order-structure
        """
        await self.load_markets()
        messageHash = 'usertrade'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash += ':' + market['id']
        trades = await self.watch_private(messageHash, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_my_trades(self, client, message, subscription=None):
        #
        # {
        #     "topic":"usertrade",
        #     "action":"insert",
        #     "user_id":"103",
        #     "symbol":"xht-usdt",
        #     "data":[
        #        {
        #           "size":1,
        #           "side":"buy",
        #           "price":0.24,
        #           "symbol":"xht-usdt",
        #           "timestamp":"2022-05-13T09:30:15.014Z",
        #           "order_id":"6065a66e-e9a4-44a3-9726-4f8fa54b6bb6",
        #           "fee":0.001,
        #           "fee_coin":"xht",
        #           "is_same":true
        #        }
        #     ],
        #     "time":1652434215
        # }
        #
        channel = self.safe_string(message, 'topic')
        rawTrades = self.safe_value(message, 'data')
        # usually the first message is an empty array
        # when the user does not have any trades yet
        dataLength = len(rawTrades)
        if dataLength == 0:
            return 0
        if self.myTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            self.myTrades = ArrayCache(limit)
        stored = self.myTrades
        marketIds = {}
        for i in range(0, len(rawTrades)):
            trade = rawTrades[i]
            parsed = self.parse_trade(trade)
            stored.append(parsed)
            symbol = trade['symbol']
            market = self.market(symbol)
            marketId = market['id']
            marketIds[marketId] = True
        # non-symbol specific
        client.resolve(self.myTrades, channel)
        keys = list(marketIds.keys())
        for i in range(0, len(keys)):
            marketId = keys[i]
            messageHash = channel + ':' + marketId
            client.resolve(self.myTrades, messageHash)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the hollaex api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        messageHash = 'order'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash += ':' + market['id']
        orders = await self.watch_private(messageHash, params)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client, message, subscription=None):
        #
        #     {
        #         topic: 'order',
        #         action: 'insert',
        #         user_id: 155328,
        #         symbol: 'ltc-usdt',
        #         data: {
        #             symbol: 'ltc-usdt',
        #             side: 'buy',
        #             size: 0.05,
        #             type: 'market',
        #             price: 0,
        #             fee_structure: {maker: 0.1, taker: 0.1},
        #             fee_coin: 'ltc',
        #             id: 'ce38fd48-b336-400b-812b-60c636454231',
        #             created_by: 155328,
        #             filled: 0.05,
        #             method: 'market',
        #             created_at: '2022-04-11T14:09:00.760Z',
        #             updated_at: '2022-04-11T14:09:00.760Z',
        #             status: 'filled'
        #         },
        #         time: 1649686140
        #     }
        #
        #    {
        #        "topic":"order",
        #        "action":"partial",
        #        "user_id":155328,
        #        "data":[
        #           {
        #              "created_at":"2022-05-13T08:19:07.694Z",
        #              "fee":0,
        #              "meta":{
        #
        #              },
        #              "symbol":"ltc-usdt",
        #              "side":"buy",
        #              "size":0.1,
        #              "type":"limit",
        #              "price":55,
        #              "fee_structure":{
        #                 "maker":0.1,
        #                 "taker":0.1
        #              },
        #              "fee_coin":"ltc",
        #              "id":"d5e77182-ad4c-4ac9-8ce4-a97f9b43e33c",
        #              "created_by":155328,
        #              "filled":0,
        #              "status":"new",
        #              "updated_at":"2022-05-13T08:19:07.694Z",
        #              "stop":null
        #           }
        #        ],
        #        "time":1652430035
        #       }
        #
        channel = self.safe_string(message, 'topic')
        data = self.safe_value(message, 'data', {})
        # usually the first message is an empty array
        dataLength = len(data)
        if dataLength == 0:
            return 0
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        stored = self.orders
        rawOrders = None
        if not isinstance(data, list):
            rawOrders = [data]
        else:
            rawOrders = data
        marketIds = {}
        for i in range(0, len(rawOrders)):
            order = rawOrders[i]
            parsed = self.parse_order(order)
            stored.append(parsed)
            symbol = order['symbol']
            market = self.market(symbol)
            marketId = market['id']
            marketIds[marketId] = True
        # non-symbol specific
        client.resolve(self.orders, channel)
        keys = list(marketIds.keys())
        for i in range(0, len(keys)):
            marketId = keys[i]
            messageHash = channel + ':' + marketId
            client.resolve(self.orders, messageHash)

    async def watch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the hollaex api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        messageHash = 'wallet'
        return await self.watch_private(messageHash, params)

    def handle_balance(self, client, message):
        #
        #     {
        #         topic: 'wallet',
        #         action: 'partial',
        #         user_id: 155328,
        #         data: {
        #             eth_balance: 0,
        #             eth_available: 0,
        #             usdt_balance: 18.94344188,
        #             usdt_available: 18.94344188,
        #             ltc_balance: 0.00005,
        #             ltc_available: 0.00005,
        #         },
        #         time: 1649687396
        #     }
        #
        messageHash = self.safe_string(message, 'topic')
        data = self.safe_value(message, 'data')
        keys = list(data.keys())
        timestamp = self.safe_integer_product(message, 'time', 1000)
        self.balance['info'] = data
        self.balance['timestamp'] = timestamp
        self.balance['datetime'] = self.iso8601(timestamp)
        for i in range(0, len(keys)):
            key = keys[i]
            parts = key.split('_')
            currencyId = self.safe_string(parts, 0)
            code = self.safe_currency_code(currencyId)
            account = self.balance[code] if (code in self.balance) else self.account()
            second = self.safe_string(parts, 1)
            freeOrTotal = 'free' if (second == 'available') else 'total'
            account[freeOrTotal] = self.safe_string(data, key)
            self.balance[code] = account
        self.balance = self.safe_balance(self.balance)
        client.resolve(self.balance, messageHash)

    async def watch_public(self, messageHash, params={}):
        url = self.urls['api']['ws']
        request = {
            'op': 'subscribe',
            'args': [messageHash],
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def watch_private(self, messageHash, params={}):
        self.check_required_credentials()
        expires = self.safe_string(self.options, 'ws-expires')
        if expires is None:
            timeout = int((self.timeout / str(1000)))
            expires = self.sum(self.seconds(), timeout)
            expires = str(expires)
            # we need to memoize these values to avoid generating a new url on each method execution
            # that would trigger a new connection on each received message
            self.options['ws-expires'] = expires
        url = self.urls['api']['ws']
        auth = 'CONNECT' + '/stream' + expires
        signature = self.hmac(self.encode(auth), self.encode(self.secret))
        authParams = {
            'api-key': self.apiKey,
            'api-signature': signature,
            'api-expires': expires,
        }
        signedUrl = url + '?' + self.urlencode(authParams)
        request = {
            'op': 'subscribe',
            'args': [messageHash],
        }
        message = self.extend(request, params)
        return await self.watch(signedUrl, messageHash, message, messageHash)

    def handle_error_message(self, client, message):
        #
        #     {error: 'Bearer or HMAC authentication required'}
        #     {error: 'Error: wrong input'}
        #
        error = self.safe_integer(message, 'error')
        try:
            if error is not None:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['ws']['exact'], error, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                return False
        return message

    def handle_message(self, client, message):
        #
        # pong
        #
        #     {message: 'pong'}
        #
        # trade
        #
        #     {
        #         topic: 'trade',
        #         action: 'partial',
        #         symbol: 'btc-usdt',
        #         data: [
        #             {
        #                 size: 0.05145,
        #                 price: 41977.9,
        #                 side: 'buy',
        #                 timestamp: '2022-04-11T09:40:10.881Z'
        #             },
        #         ]
        #     }
        #
        # orderbook
        #
        #     {
        #         topic: 'orderbook',
        #         action: 'partial',
        #         symbol: 'ltc-usdt',
        #         data: {
        #             bids: [
        #                 [104.29, 5.2264],
        #                 [103.86,1.3629],
        #                 [101.82,0.5942]
        #             ],
        #             asks: [
        #                 [104.81,9.5531],
        #                 [105.54,0.6416],
        #                 [106.18,1.4141],
        #             ],
        #             timestamp: '2022-04-11T10:37:01.227Z'
        #         },
        #         time: 1649673421
        #     }
        #
        # order
        #
        #     {
        #         topic: 'order',
        #         action: 'insert',
        #         user_id: 155328,
        #         symbol: 'ltc-usdt',
        #         data: {
        #             symbol: 'ltc-usdt',
        #             side: 'buy',
        #             size: 0.05,
        #             type: 'market',
        #             price: 0,
        #             fee_structure: {maker: 0.1, taker: 0.1},
        #             fee_coin: 'ltc',
        #             id: 'ce38fd48-b336-400b-812b-60c636454231',
        #             created_by: 155328,
        #             filled: 0.05,
        #             method: 'market',
        #             created_at: '2022-04-11T14:09:00.760Z',
        #             updated_at: '2022-04-11T14:09:00.760Z',
        #             status: 'filled'
        #         },
        #         time: 1649686140
        #     }
        #
        # balance
        #
        #     {
        #         topic: 'wallet',
        #         action: 'partial',
        #         user_id: 155328,
        #         data: {
        #             eth_balance: 0,
        #             eth_available: 0,
        #             usdt_balance: 18.94344188,
        #             usdt_available: 18.94344188,
        #             ltc_balance: 0.00005,
        #             ltc_available: 0.00005,
        #         }
        #     }
        #
        if not self.handle_error_message(client, message):
            return
        content = self.safe_string(message, 'message')
        if content == 'pong':
            self.handle_pong(client, message)
            return
        methods = {
            'trade': self.handle_trades,
            'orderbook': self.handle_order_book,
            'order': self.handle_order,
            'wallet': self.handle_balance,
            'usertrade': self.handle_my_trades,
        }
        topic = self.safe_value(message, 'topic')
        method = self.safe_value(methods, topic)
        if method is not None:
            method(client, message)

    def ping(self, client):
        # hollaex does not support built-in ws protocol-level ping-pong
        return {'op': 'ping'}

    def handle_pong(self, client, message):
        client.lastPong = self.milliseconds()
        return message

    def on_error(self, client, error):
        self.options['ws-expires'] = None
        self.on_error(client, error)

    def on_close(self, client, error):
        self.options['ws-expires'] = None
        self.on_close(client, error)
