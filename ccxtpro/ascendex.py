# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.base.errors import AuthenticationError


class ascendex(Exchange, ccxt.ascendex):

    def describe(self):
        return self.deep_extend(super(ascendex, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': False,
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://ascendex.com:443/api/pro/v2/stream',
                        'private': 'wss://ascendex.com:443/{accountGroup}/api/pro/v2/stream',
                    },
                },
                'test': {
                    'ws': {
                        'public': 'wss://api-test.ascendex-sandbox.com:443/api/pro/v2/stream',
                        'private': 'wss://api-test.ascendex-sandbox.com:443/{accountGroup}/api/pro/v2/stream',
                    },
                },
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'OHLCVLimit': 1000,
                'categoriesAccount': {
                    'cash': 'spot',
                    'futures': 'swap',
                    'margin': 'margin',
                },
            },
        })

    async def watch_public(self, messageHash, params={}):
        url = self.urls['api']['ws']['public']
        id = self.nonce()
        request = {
            'id': str(id),
            'op': 'sub',
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def watch_private(self, channel, messageHash, params={}):
        await self.load_accounts()
        accountGroup = self.safe_string(self.options, 'account-group')
        url = self.urls['api']['ws']['private']
        url = self.implode_params(url, {'accountGroup': accountGroup})
        id = self.nonce()
        request = {
            'id': str(id),
            'op': 'sub',
            'ch': channel,
        }
        message = self.extend(request, params)
        await self.authenticate(url, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if (limit is None) or (limit > 1440):
            limit = 100
        interval = self.timeframes[timeframe]
        channel = 'bar' + ':' + interval + ':' + market['id']
        params = {
            'ch': channel,
        }
        ohlcv = await self.watch_public(channel, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        # {
        #     "m": "bar",
        #     "s": "ASD/USDT",
        #     "data": {
        #         "i":  "1",
        #         "ts": 1575398940000,
        #         "o":  "0.04993",
        #         "c":  "0.04970",
        #         "h":  "0.04993",
        #         "l":  "0.04970",
        #         "v":  "8052"
        #     }
        # }
        #
        marketId = self.safe_string(message, 's')
        symbol = self.safe_symbol(marketId)
        channel = self.safe_string(message, 'm')
        data = self.safe_value(message, 'data', {})
        interval = self.safe_string(data, 'i')
        messageHash = channel + ':' + interval + ':' + marketId
        timeframe = self.find_timeframe(interval)
        market = self.market(symbol)
        parsed = self.parse_ohlcv(message, market)
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        stored.append(parsed)
        client.resolve(stored, messageHash)
        return message

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        channel = 'trades' + ':' + market['id']
        params = self.extend(params, {
            'ch': channel,
        })
        trades = await self.watch_public(channel, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        # {
        #     m: 'trades',
        #     symbol: 'BTC/USDT',
        #     data: [
        #       {
        #         p: '40744.28',
        #         q: '0.00150',
        #         ts: 1647514330758,
        #         bm: True,
        #         seqnum: 72057633465800320
        #       }
        #     ]
        # }
        #
        marketId = self.safe_string(message, 'symbol')
        symbol = self.safe_symbol(marketId)
        channel = self.safe_string(message, 'm')
        messageHash = channel + ':' + marketId
        market = self.market(symbol)
        rawData = self.safe_value(message, 'data')
        if rawData is None:
            rawData = []
        trades = self.parse_trades(rawData, market)
        array = self.safe_value(self.trades, symbol)
        if array is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            array = ArrayCache(limit)
        for i in range(0, len(trades)):
            array.append(trades[i])
        self.trades[symbol] = array
        client.resolve(array, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        channel = 'depth-realtime' + ':' + market['id']
        params = self.extend(params, {
            'ch': channel,
        })
        orderbook = await self.watch_public(channel, params)
        return orderbook.limit(limit)

    async def watch_order_book_snapshot(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        action = 'depth-snapshot-realtime'
        channel = action + ':' + market['id']
        params = self.extend(params, {
            'action': action,
            'args': {
                'symbol': market['id'],
            },
            'op': 'req',
        })
        orderbook = await self.watch_public(channel, params)
        return orderbook.limit(limit)

    def handle_order_book_snapshot(self, client, message):
        #
        # {
        #     m: 'depth',
        #     symbol: 'BTC/USDT',
        #     data: {
        #       ts: 1647520500149,
        #       seqnum: 28590487626,
        #       asks: [
        #         [Array], [Array], [Array],
        #         [Array], [Array], [Array],
        #       ],
        #       bids: [
        #         [Array], [Array], [Array],
        #         [Array], [Array], [Array],
        #       ]
        #     }
        #   }
        #
        marketId = self.safe_string(message, 'symbol')
        symbol = self.safe_symbol(marketId)
        channel = self.safe_string(message, 'm')
        messageHash = channel + ':' + symbol
        orderbook = self.orderbooks[symbol]
        data = self.safe_value(message, 'data')
        snapshot = self.parse_order_book(data, symbol)
        snapshot['nonce'] = self.safe_integer(data, 'seqnum')
        orderbook.reset(snapshot)
        # unroll the accumulated deltas
        messages = orderbook.cache
        for i in range(0, len(messages)):
            message = messages[i]
            self.handle_order_book_message(client, message, orderbook)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def handle_order_book(self, client, message):
        #
        #   {
        #       m: 'depth',
        #       symbol: 'BTC/USDT',
        #       data: {
        #         ts: 1647515136144,
        #         seqnum: 28590470736,
        #         asks: [[Array], [Array]],
        #         bids: [[Array], [Array], [Array], [Array], [Array], [Array]]
        #       }
        #   }
        #
        channel = self.safe_string(message, 'm')
        marketId = self.safe_string(message, 'symbol')
        symbol = self.safe_symbol(marketId)
        messageHash = channel + ':' + marketId
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            orderbook = self.order_book({})
        if orderbook['nonce'] is None:
            orderbook.cache.append(message)
        else:
            self.handle_order_book_message(client, message, orderbook)
            client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        #
        # ["40990.47","0.01619"],
        #
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client, message, orderbook):
        #
        # {
        #     "m":"depth",
        #     "symbol":"BTC/USDT",
        #     "data":{
        #        "ts":1647527417715,
        #        "seqnum":28590257013,
        #        "asks":[
        #           ["40990.47","0.01619"],
        #           ["41021.21","0"],
        #           ["41031.59","0.06096"]
        #        ],
        #        "bids":[
        #           ["40990.46","0.76114"],
        #           ["40985.18","0"]
        #        ]
        #     }
        #  }
        #
        data = self.safe_value(message, 'data', {})
        seqNum = self.safe_integer(data, 'seqnum')
        if seqNum > orderbook['nonce']:
            asks = self.safe_value(data, 'asks', [])
            bids = self.safe_value(data, 'bids', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['nonce'] = seqNum
            timestamp = self.safe_integer(data, 'ts')
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    async def watch_balance(self, params={}):
        await self.load_markets()
        type, query = self.handle_market_type_and_params('watchBalance', None, params)
        channel = None
        messageHash = None
        if (type == 'spot') or (type == 'margin'):
            accountCategories = self.safe_value(self.options, 'accountCategories', {})
            accountCategory = self.safe_string(accountCategories, type, 'cash')  # cash, margin,
            accountCategory = accountCategory.upper()
            channel = 'order:' + accountCategory  # order and balance share the same channel
            messageHash = 'balance:' + type
        else:
            channel = 'futures-account-update'
            messageHash = 'balance:swap'
        return await self.watch_private(channel, messageHash, query)

    def handle_balance(self, client, message):
        #
        # cash account
        #
        # {
        #     "m": "balance",
        #     "accountId": "cshQtyfq8XLAA9kcf19h8bXHbAwwoqDo",
        #     "ac": "CASH",
        #     "data": {
        #         "a" : "USDT",
        #         "sn": 8159798,
        #         "tb": "600",
        #         "ab": "600"
        #     }
        # }
        #
        # margin account
        #
        # {
        #     "m": "balance",
        #     "accountId": "marOxpKJV83dxTRx0Eyxpa0gxc4Txt0P",
        #     "ac": "MARGIN",
        #     "data": {
        #         "a"  : "USDT",
        #         "sn" : 8159802,
        #         "tb" : "400",  # total Balance
        #         "ab" : "400",  # available balance
        #         "brw": "0",  # borrowws
        #         "int": "0"  # interest
        #     }
        # }
        #
        # futures
        # {
        #     "m"     : "futures-account-update",            # message
        #     "e"     : "ExecutionReport",                   # event type
        #     "t"     : 1612508562129,                       # time
        #     "acc"   : "futures-account-id",         # account ID
        #     "at"    : "FUTURES",                           # account type
        #     "sn"    : 23128,                               # sequence number,
        #     "id"    : "r177710001cbU3813942147C5kbFGOan",
        #     "col": [
        #       {
        #         "a": "USDT",               # asset code
        #         "b": "1000000",            # balance
        #         "f": "1"                   # discount factor
        #       }
        #     ],
        #     (...)
        #
        channel = self.safe_string(message, 'm')
        result = None
        type = None
        if (channel == 'order') or (channel == 'futures-order'):
            data = self.safe_value(message, 'data')
            marketId = self.safe_string(data, 's')
            market = self.safe_market(marketId)
            baseAccount = self.account()
            baseAccount['free'] = self.safe_string(data, 'bab')
            baseAccount['total'] = self.safe_string(data, 'btb')
            quoteAccount = self.account()
            quoteAccount['free'] = self.safe_string(data, 'qab')
            quoteAccount['total'] = self.safe_string(data, 'qtb')
            if market['contract']:
                type = 'swap'
                result = self.safe_value(self.balances, type, {})
            else:
                type = market['type']
                result = self.safe_value(self.balances, type, {})
            result[market['base']] = baseAccount
            result[market['quote']] = quoteAccount
        else:
            accountType = self.safe_string_lower_2(message, 'ac', 'at')
            categoriesAccounts = self.safe_value(self.options, 'categoriesAccount')
            type = self.safe_string(categoriesAccounts, accountType, 'spot')
            result = self.safe_value(self.balances, type, {})
            data = self.safe_value(message, 'data')
            balances = None
            if data is None:
                balances = self.safe_value(message, 'col')
            else:
                balances = [data]
            for i in range(0, len(balances)):
                balance = balances[i]
                code = self.safe_currency_code(self.safe_string(balance, 'a'))
                account = self.account()
                account['free'] = self.safe_string(balance, 'ab')
                account['total'] = self.safe_string_2(balance, 'tb', 'b')
                result[code] = account
        messageHash = 'balance' + ':' + type
        client.resolve(self.safe_balance(result), messageHash)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        type, query = self.handle_market_type_and_params('watchOrders', market, params)
        messageHash = None
        channel = None
        if type != 'spot':
            channel = 'futures-order'
            messageHash = 'order:FUTURES'
        else:
            accountCategories = self.safe_value(self.options, 'accountCategories', {})
            accountCategory = self.safe_string(accountCategories, type, 'cash')  # cash, margin
            accountCategory = accountCategory.upper()
            messageHash = 'order' + ':' + accountCategory
            channel = messageHash
        if symbol is not None:
            messageHash = messageHash + ':' + symbol
        orders = await self.watch_private(channel, messageHash, query)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client, message):
        #
        # spot order
        # {
        #   m: 'order',
        #   accountId: 'cshF5SlR9ukAXoDOuXbND4dVpBMw9gzH',
        #   ac: 'CASH',
        #   data: {
        #     sn: 19399016185,
        #     orderId: 'r17f9d7983faU7223046196CMlrj3bfC',
        #     s: 'LTC/USDT',
        #     ot: 'Limit',
        #     t: 1647614461160,
        #     p: '50',
        #     q: '0.1',
        #     sd: 'Buy',
        #     st: 'New',
        #     ap: '0',
        #     cfq: '0',
        #     sp: '',
        #     err: '',
        #     btb: '0',
        #     bab: '0',
        #     qtb: '8',
        #     qab: '2.995',
        #     cf: '0',
        #     fa: 'USDT',
        #     ei: 'NULL_VAL'
        #   }
        # }
        #
        #  futures order
        # {
        #     m: 'futures-order',
        #     sn: 19399927636,
        #     e: 'ExecutionReport',
        #     a: 'futF5SlR9ukAXoDOuXbND4dVpBMw9gzH',  # account id
        #     ac: 'FUTURES',
        #     t: 1647622515434,  # last execution time
        #      (...)
        # }
        #
        accountType = self.safe_string(message, 'ac')
        messageHash = 'order:' + accountType
        data = self.safe_value(message, 'data', message)
        order = self.parse_ws_order(data)
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        orders.append(order)
        symbolMessageHash = messageHash + ':' + order['symbol']
        client.resolve(orders, symbolMessageHash)
        client.resolve(orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        # spot order
        #    {
        #          sn: 19399016185,  #sequence number
        #          orderId: 'r17f9d7983faU7223046196CMlrj3bfC',
        #          s: 'LTC/USDT',
        #          ot: 'Limit',  # order type
        #          t: 1647614461160,  # last execution timestamp
        #          p: '50',  # price
        #          q: '0.1',  # quantity
        #          sd: 'Buy',  # side
        #          st: 'New',  # status
        #          ap: '0',  # average fill price
        #          cfq: '0',  # cumulated fill quantity
        #          sp: '',  # stop price
        #          err: '',
        #          btb: '0',  # base asset total balance
        #          bab: '0',  # base asset available balance
        #          qtb: '8',  # quote asset total balance
        #          qab: '2.995',  # quote asset available balance
        #          cf: '0',  # cumulated commission
        #          fa: 'USDT',  # fee asset
        #          ei: 'NULL_VAL'
        #        }
        #
        #  futures order
        # {
        #     m: 'futures-order',
        #     sn: 19399927636,
        #     e: 'ExecutionReport',
        #     a: 'futF5SlR9ukAXoDOuXbND4dVpBMw9gzH',  # account id
        #     ac: 'FUTURES',
        #     t: 1647622515434,  # last execution time
        #     ct: 1647622515413,  # order creation time
        #     orderId: 'r17f9df469b1U7223046196Okf5Kbmd',
        #     sd: 'Buy',  # side
        #     ot: 'Limit',  # order type
        #     ei: 'NULL_VAL',
        #     q: '1',  # quantity
        #     p: '50',  #price
        #     sp: '0',  # stopPrice
        #     spb: '',  # stopTrigger
        #     s: 'LTC-PERP',  # symbol
        #     st: 'New',  # state
        #     err: '',
        #     lp: '0',  # last filled price
        #     lq: '0',  # last filled quantity(base asset)
        #     ap: '0',  # average filled price
        #     cfq: '0',  # cummulative filled quantity(base asset)
        #     f: '0',  # commission fee of the current execution
        #     cf: '0',  # cumulative commission fee
        #     fa: 'USDT',  # fee asset
        #     psl: '0',
        #     pslt: 'market',
        #     ptp: '0',
        #     ptpt: 'market'
        #   }
        #
        status = self.parse_order_status(self.safe_string(order, 'st'))
        marketId = self.safe_string(order, 's')
        timestamp = self.safe_integer(order, 't')
        symbol = self.safe_symbol(marketId, market, '/')
        lastTradeTimestamp = self.safe_integer(order, 't')
        price = self.safe_string(order, 'p')
        amount = self.safe_string(order, 'q')
        average = self.safe_string(order, 'ap')
        filled = self.safe_string_2(order, 'cfq')
        id = self.safe_string(order, 'orderId')
        type = self.safe_string_lower(order, 'ot')
        side = self.safe_string_lower(order, 'sd')
        feeCost = self.safe_number(order, 'cf')
        fee = None
        if feeCost is not None:
            feeCurrencyId = self.safe_string(order, 'fa')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        stopPrice = self.parse_number(self.omit_zero(self.safe_string(order, 'sp')))
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'amount': amount,
            'cost': None,
            'average': average,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': fee,
            'trades': None,
        }, market)

    def handle_error_message(self, client, message):
        #
        # {
        #     m: 'disconnected',
        #     code: 100005,
        #     reason: 'INVALID_WS_REQUEST_DATA',
        #     info: 'Session is disconnected due to missing pong message from the client'
        #   }
        #
        errorCode = self.safe_integer(message, 'code')
        try:
            if errorCode is not None:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
                messageString = self.safe_value(message, 'message')
                if messageString is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], messageString, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                client.reject(e, 'authenticated')
                method = 'auth'
                if method in client.subscriptions:
                    del client.subscriptions[method]
                return False
            else:
                client.reject(e)
        return message

    def handle_authenticate(self, client, message):
        #
        #     {m: 'auth', id: '1647605234', code: 0}
        #
        future = client.futures['authenticated']
        future.resolve(1)
        return message

    def handle_message(self, client, message):
        if not self.handle_error_message(client, message):
            return
        #
        #     {m: 'ping', hp: 3}
        #
        #     {m: 'sub', ch: 'bar:BTC/USDT', code: 0}
        #
        #     {m: 'sub', id: '1647515701', ch: 'depth:BTC/USDT', code: 0}
        #
        #     {m: 'connected', type: 'unauth'}
        #
        #     {m: 'auth', id: '1647605234', code: 0}
        #
        # order or balance sub
        # {
        #     m: 'sub',
        #     id: '1647605952',
        #     ch: 'order:cshF5SlR9ukAXoDOuXbND4dVpBMw9gzH', or futures-order
        #     code: 0
        #   }
        #
        # ohlcv
        #  {
        #     m: 'bar',
        #     s: 'BTC/USDT',
        #     data: {
        #       i: '1',
        #       ts: 1647510060000,
        #       o: '40813.93',
        #       c: '40804.57',
        #       h: '40814.21',
        #       l: '40804.56',
        #       v: '0.01537'
        #     }
        #   }
        #
        # trades
        #
        #    {
        #        m: 'trades',
        #        symbol: 'BTC/USDT',
        #        data: [
        #          {
        #            p: '40762.26',
        #            q: '0.01500',
        #            ts: 1647514306759,
        #            bm: True,
        #            seqnum: 72057633465795180
        #          }
        #        ]
        #    }
        #
        # orderbook deltas
        #
        # {
        #     "m":"depth",
        #     "symbol":"BTC/USDT",
        #     "data":{
        #        "ts":1647527417715,
        #        "seqnum":28590257013,
        #        "asks":[
        #           ["40990.47","0.01619"],
        #           ["41021.21","0"],
        #           ["41031.59","0.06096"]
        #        ],
        #        "bids":[
        #           ["40990.46","0.76114"],
        #           ["40985.18","0"]
        #        ]
        #     }
        #  }
        #
        # orderbook snapshot
        #  {
        #     m: 'depth-snapshot',
        #     symbol: 'BTC/USDT',
        #     data: {
        #       ts: 1647525938513,
        #       seqnum: 28590504772,
        #       asks: [
        #         [Array], [Array], [Array], [Array], [Array], [Array], [Array],
        #         [Array], [Array], [Array], [Array], [Array], [Array], [Array],
        #         [Array], [Array], [Array], [Array], [Array], [Array], [Array],
        #          (...)
        #       ]
        #  }
        #
        # spot order update
        #  {
        #      "m": "order",
        #      "accountId": "cshQtyfq8XLAA9kcf19h8bXHbAwwoqDo",
        #      "ac": "CASH",
        #      "data": {
        #          "s":       "BTC/USDT",
        #          "sn":       8159711,
        #          "sd":      "Buy",
        #          "ap":      "0",
        #          "bab":     "2006.5974027",
        #          "btb":     "2006.5974027",
        #          "cf":      "0",
        #          "cfq":     "0",
        #          (...)
        #      }
        #  }
        # future order update
        # {
        #     m: 'futures-order',
        #     sn: 19404258063,
        #     e: 'ExecutionReport',
        #     a: 'futF5SlR9ukAXoDOuXbND4dVpBMw9gzH',
        #     ac: 'FUTURES',
        #     t: 1647681792543,
        #     ct: 1647622515413,
        #     orderId: 'r17f9df469b1U7223046196Okf5KbmdL',
        #         (...)
        #     ptpt: 'None'
        #   }
        #
        # balance update cash
        # {
        #     "m": "balance",
        #     "accountId": "cshQtyfq8XLAA9kcf19h8bXHbAwwoqDo",
        #     "ac": "CASH",
        #     "data": {
        #         "a" : "USDT",
        #         "sn": 8159798,
        #         "tb": "600",
        #         "ab": "600"
        #     }
        # }
        #
        # balance update margin
        # {
        #     "m": "balance",
        #     "accountId": "marOxpKJV83dxTRx0Eyxpa0gxc4Txt0P",
        #     "ac": "MARGIN",
        #     "data": {
        #         "a"  : "USDT",
        #         "sn" : 8159802,
        #         "tb" : "400",
        #         "ab" : "400",
        #         "brw": "0",
        #         "int": "0"
        #     }
        # }
        #
        subject = self.safe_string(message, 'm')
        methods = {
            'ping': self.handle_ping,
            'auth': self.handle_authenticate,
            'sub': self.handle_subscription_status,
            'depth-realtime': self.handle_order_book,
            'depth-snapshot-realtime': self.handle_order_book_snapshot,
            'trades': self.handle_trades,
            'bar': self.handle_ohlcv,
            'balance': self.handle_balance,
            'futures-account-update': self.handle_balance,
        }
        method = self.safe_value(methods, subject)
        if method is not None:
            method(client, message)
        if (subject == 'order') or (subject == 'futures-order'):
            # self.handle_order(client, message)
            # balance updates may be in the order structure
            # they may also be standalone balance updates related to account transfers
            self.handle_order(client, message)
            if subject == 'order':
                self.handle_balance(client, message)
        return message

    def handle_subscription_status(self, client, message):
        #
        #     {m: 'sub', ch: 'bar:BTC/USDT', code: 0}
        #
        #     {m: 'sub', id: '1647515701', ch: 'depth:BTC/USDT', code: 0}
        #
        channel = self.safe_string(message, 'ch', '')
        if channel.find('depth-realtime') > -1:
            self.handle_order_book_subscription(client, message)
        return message

    def handle_order_book_subscription(self, client, message):
        channel = self.safe_string(message, 'ch')
        parts = channel.split(':')
        marketId = parts[1]
        symbol = self.safe_symbol(marketId)
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({})
        self.spawn(self.watch_order_book_snapshot, symbol)

    async def pong(self, client, message):
        #
        #     {m: 'ping', hp: 3}
        #
        await client.send({'op': 'pong', 'hp': self.safe_integer(message, 'hp')})

    def handle_ping(self, client, message):
        self.spawn(self.pong, client, message)

    async def authenticate(self, url, params={}):
        self.check_required_credentials()
        messageHash = 'authenticated'
        client = self.client(url)
        future = self.safe_value(client.futures, messageHash)
        if future is None:
            client.future(messageHash)
            timestamp = str(self.milliseconds())
            urlParts = url.split('/')
            partsLength = len(urlParts)
            path = self.safe_string(urlParts, partsLength - 1)
            version = self.safe_string(urlParts, partsLength - 2)
            auth = timestamp + '+' + version + '/' + path
            secret = self.base64_to_binary(self.secret)
            signature = self.hmac(self.encode(auth), secret, hashlib.sha256, 'base64')
            request = {
                'op': 'auth',
                'id': str(self.nonce()),
                't': timestamp,
                'key': self.apiKey,
                'sig': signature,
            }
            self.spawn(self.watch, url, messageHash, self.extend(request, params))
        return await future
