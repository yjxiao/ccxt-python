# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache
import hashlib
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired


class okex(Exchange, ccxt.okex):

    def describe(self):
        return self.deep_extend(super(okex, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchOrderBook': True,
                'watchTrades': True,
                'watchBalance': True,
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://real.okex.com:8443/ws/v3',
                },
                'test': {
                    'ws': 'wss://real.okex.com:8443/ws/v3?BrokerId=181',
                },
            },
            'options': {
                'watchOrderBook': {
                    'limit': 400,  # max
                    'type': 'spot',  # margin
                    'depth': 'depth_l2_tbt',  # depth5, depth
                },
                'watchBalance': 'spot',  # margin, futures, swap
                'ws': {
                    'inflate': True,
                },
            },
            'streaming': {
                # okex does not support built-in ws protocol-level ping-pong
                # instead it requires a custom text-based ping-pong
                'ping': self.ping,
                'keepAlive': 20000,
            },
        })

    async def subscribe(self, channel, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        url = self.urls['api']['ws']
        messageHash = market['type'] + '/' + channel + ':' + market['id']
        request = {
            'op': 'subscribe',
            'args': [messageHash],
        }
        return await self.watch(url, messageHash, self.deep_extend(request, params), messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        trades = await self.subscribe('trade', symbol, params)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_ticker(self, symbol, params={}):
        return await self.subscribe('ticker', symbol, params)

    def handle_trade(self, client, message):
        #
        #     {
        #         table: 'spot/trade',
        #         data: [
        #             {
        #                 side: 'buy',
        #                 trade_id: '30770973',
        #                 price: '4665.4',
        #                 size: '0.019',
        #                 instrument_id: 'BTC-USDT',
        #                 timestamp: '2020-03-16T13:41:46.526Z'
        #             }
        #         ]
        #     }
        #
        table = self.safe_string(message, 'table')
        data = self.safe_value(message, 'data', [])
        tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
        for i in range(0, len(data)):
            trade = self.parse_trade(data[i])
            symbol = trade['symbol']
            marketId = self.safe_string(trade['info'], 'instrument_id')
            messageHash = table + ':' + marketId
            stored = self.safe_value(self.trades, symbol)
            if stored is None:
                stored = ArrayCache(tradesLimit)
                self.trades[symbol] = stored
            stored.append(trade)
            client.resolve(stored, messageHash)
        return message

    def handle_ticker(self, client, message):
        #
        #     {
        #         table: 'spot/ticker',
        #         data: [
        #             {
        #                 last: '4634.1',
        #                 open_24h: '5305.6',
        #                 best_bid: '4631.6',
        #                 high_24h: '5950',
        #                 low_24h: '4448.8',
        #                 base_volume_24h: '147913.11435388',
        #                 quote_volume_24h: '756850119.99108082',
        #                 best_ask: '4631.7',
        #                 instrument_id: 'BTC-USDT',
        #                 timestamp: '2020-03-16T13:16:25.677Z',
        #                 best_bid_size: '0.12348942',
        #                 best_ask_size: '0.00100014',
        #                 last_qty: '0.00331822'
        #             }
        #         ]
        #     }
        #
        table = self.safe_string(message, 'table')
        data = self.safe_value(message, 'data', [])
        for i in range(0, len(data)):
            ticker = self.parse_ticker(data[i])
            symbol = ticker['symbol']
            marketId = self.safe_string(ticker['info'], 'instrument_id')
            messageHash = table + ':' + marketId
            self.tickers[symbol] = ticker
            client.resolve(ticker, messageHash)
        return message

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        interval = self.timeframes[timeframe]
        name = 'candle' + interval + 's'
        ohlcv = await self.subscribe(name, symbol, params)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #     {
        #         table: "spot/candle60s",
        #         data: [
        #             {
        #                 candle: [
        #                     "2020-03-16T14:29:00.000Z",
        #                     "4948.3",
        #                     "4966.7",
        #                     "4939.1",
        #                     "4945.3",
        #                     "238.36021657"
        #                 ],
        #                 instrument_id: "BTC-USDT"
        #             }
        #         ]
        #     }
        #
        table = self.safe_string(message, 'table')
        data = self.safe_value(message, 'data', [])
        parts = table.split('/')
        part1 = self.safe_string(parts, 1)
        interval = part1.replace('candle', '')
        interval = interval.replace('s', '')
        # use a reverse lookup in a static map instead
        timeframe = self.find_timeframe(interval)
        for i in range(0, len(data)):
            marketId = self.safe_string(data[i], 'instrument_id')
            candle = self.safe_value(data[i], 'candle')
            market = self.safe_market(marketId)
            symbol = market['symbol']
            parsed = self.parse_ohlcv(candle, market)
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            stored = self.safe_value(self.ohlcvs[symbol], timeframe)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCache(limit)
                self.ohlcvs[symbol][timeframe] = stored
            length = len(stored)
            if length and parsed[0] == stored[length - 1][0]:
                stored[length - 1] = parsed
            else:
                stored.append(parsed)
            messageHash = table + ':' + marketId
            client.resolve(stored, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        options = self.safe_value(self.options, 'watchOrderBook', {})
        depth = self.safe_string(options, 'depth', 'depth_l2_tbt')
        orderbook = await self.subscribe(depth, symbol, params)
        return self.limit_order_book(orderbook, symbol, limit, params)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book_message(self, client, message, orderbook):
        #
        #     {
        #         instrument_id: "BTC-USDT",
        #         asks: [
        #             ["4568.5", "0.49723138", "2"],
        #             ["4568.7", "0.5013", "1"],
        #             ["4569.1", "0.4398", "1"],
        #         ],
        #         bids: [
        #             ["4568.4", "0.84187666", "5"],
        #             ["4568.3", "0.75661506", "6"],
        #             ["4567.8", "2.01", "2"],
        #         ],
        #         timestamp: "2020-03-16T11:11:43.388Z",
        #         checksum: 473370408
        #     }
        #
        asks = self.safe_value(message, 'asks', [])
        bids = self.safe_value(message, 'bids', [])
        self.handle_deltas(orderbook['asks'], asks)
        self.handle_deltas(orderbook['bids'], bids)
        timestamp = self.parse8601(self.safe_string(message, 'timestamp'))
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_order_book(self, client, message):
        #
        # first message(snapshot)
        #
        #     {
        #         table: "spot/depth",
        #         action: "partial",
        #         data: [
        #             {
        #                 instrument_id: "BTC-USDT",
        #                 asks: [
        #                     ["4568.5", "0.49723138", "2"],
        #                     ["4568.7", "0.5013", "1"],
        #                     ["4569.1", "0.4398", "1"],
        #                 ],
        #                 bids: [
        #                     ["4568.4", "0.84187666", "5"],
        #                     ["4568.3", "0.75661506", "6"],
        #                     ["4567.8", "2.01", "2"],
        #                 ],
        #                 timestamp: "2020-03-16T11:11:43.388Z",
        #                 checksum: 473370408
        #             }
        #         ]
        #     }
        #
        # subsequent updates
        #
        #     {
        #         table: "spot/depth",
        #         action: "update",
        #         data: [
        #             {
        #                 instrument_id:   "BTC-USDT",
        #                 asks: [
        #                     ["4598.8", "0", "0"],
        #                     ["4599.1", "0", "0"],
        #                     ["4600.3", "0", "0"],
        #                 ],
        #                 bids: [
        #                     ["4598.5", "0.08", "1"],
        #                     ["4598.2", "0.0337323", "1"],
        #                     ["4598.1", "0.12681801", "3"],
        #                 ],
        #                 timestamp: "2020-03-16T11:20:35.139Z",
        #                 checksum: 740786981
        #             }
        #         ]
        #     }
        #
        action = self.safe_string(message, 'action')
        data = self.safe_value(message, 'data', [])
        table = self.safe_string(message, 'table')
        if action == 'partial':
            for i in range(0, len(data)):
                update = data[i]
                marketId = self.safe_string(update, 'instrument_id')
                market = self.safe_market(marketId)
                symbol = market['symbol']
                options = self.safe_value(self.options, 'watchOrderBook', {})
                # default limit is 400 bidasks
                limit = self.safe_integer(options, 'limit', 400)
                orderbook = self.order_book({}, limit)
                self.orderbooks[symbol] = orderbook
                self.handle_order_book_message(client, update, orderbook)
                messageHash = table + ':' + marketId
                client.resolve(orderbook, messageHash)
        else:
            for i in range(0, len(data)):
                update = data[i]
                marketId = self.safe_string(update, 'instrument_id')
                market = self.safe_market(marketId)
                symbol = market['symbol']
                if symbol in self.orderbooks:
                    orderbook = self.orderbooks[symbol]
                    self.handle_order_book_message(client, update, orderbook)
                    messageHash = table + ':' + marketId
                    client.resolve(orderbook, messageHash)
        return message

    async def authenticate(self, params={}):
        self.check_required_credentials()
        url = self.urls['api']['ws']
        messageHash = 'login'
        client = self.client(url)
        future = self.safe_value(client.subscriptions, messageHash)
        if future is None:
            future = client.future('authenticated')
            timestamp = str(self.seconds())
            method = 'GET'
            path = '/users/self/verify'
            auth = timestamp + method + path
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256, 'base64')
            request = {
                'op': messageHash,
                'args': [
                    self.apiKey,
                    self.password,
                    timestamp,
                    signature,
                ],
            }
            self.spawn(self.watch, url, messageHash, request, messageHash, future)
        return await future

    async def watch_balance(self, params={}):
        defaultType = self.safe_string_2(self.options, 'watchBalance', 'defaultType')
        type = self.safe_string(params, 'type', defaultType)
        if type is None:
            raise ArgumentsRequired(self.id + " watchBalance requires a type parameter(one of 'spot', 'margin', 'futures', 'swap')")
        # query = self.omit(params, 'type')
        negotiation = await self.authenticate()
        return await self.subscribe_to_user_account(negotiation, params)

    async def subscribe_to_user_account(self, negotiation, params={}):
        defaultType = self.safe_string_2(self.options, 'watchBalance', 'defaultType')
        type = self.safe_string(params, 'type', defaultType)
        if type is None:
            raise ArgumentsRequired(self.id + " watchBalance requires a type parameter(one of 'spot', 'margin', 'futures', 'swap')")
        await self.load_markets()
        currencyId = self.safe_string(params, 'currency')
        code = self.safe_string(params, 'code', self.safe_currency_code(currencyId))
        currency = None
        if code is not None:
            currency = self.currency(code)
        marketId = self.safe_string(params, 'instrument_id')
        symbol = self.safe_string(params, 'symbol')
        market = None
        if symbol is not None:
            market = self.market(symbol)
        elif marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        marketUndefined = (market is None)
        currencyUndefined = (currency is None)
        if type == 'spot':
            if currencyUndefined:
                raise ArgumentsRequired(self.id + " watchBalance requires a 'currency'(id) or a unified 'code' parameter for " + type + ' accounts')
        elif (type == 'margin') or (type == 'swap') or (type == 'option'):
            if marketUndefined:
                raise ArgumentsRequired(self.id + " watchBalance requires a 'instrument_id'(id) or a unified 'symbol' parameter for " + type + ' accounts')
        elif type == 'futures':
            if currencyUndefined and marketUndefined:
                raise ArgumentsRequired(self.id + " watchBalance requires a 'currency'(id), or unified 'code', or 'instrument_id'(id), or unified 'symbol' parameter for " + type + ' accounts')
        suffix = None
        if not currencyUndefined:
            suffix = currency['id']
        elif not marketUndefined:
            suffix = market['id']
        accountType = 'spot' if (type == 'margin') else type
        account = 'margin_account' if (type == 'margin') else 'account'
        messageHash = accountType + '/' + account
        subscriptionHash = messageHash + ':' + suffix
        url = self.urls['api']['ws']
        request = {
            'op': 'subscribe',
            'args': [subscriptionHash],
        }
        query = self.omit(params, ['currency', 'code', 'instrument_id', 'symbol', 'type'])
        return await self.watch(url, messageHash, self.deep_extend(request, query), subscriptionHash)

    def handle_balance(self, client, message):
        #
        # spot
        #
        #     {
        #         table: 'spot/account',
        #         data: [
        #             {
        #                 available: '11.044827320825',
        #                 currency: 'USDT',
        #                 id: '',
        #                 balance: '11.044827320825',
        #                 hold: '0'
        #             }
        #         ]
        #     }
        #
        # margin
        #
        #     {
        #         table: "spot/margin_account",
        #         data: [
        #             {
        #                 maint_margin_ratio: "0.08",
        #                 liquidation_price: "0",
        #                 'currency:USDT': {available: "0", balance: "0", borrowed: "0", hold: "0", lending_fee: "0"},
        #                 tiers: "1",
        #                 instrument_id:   "ETH-USDT",
        #                 'currency:ETH': {available: "0", balance: "0", borrowed: "0", hold: "0", lending_fee: "0"}
        #             }
        #         ]
        #     }
        #
        table = self.safe_string(message, 'table')
        parts = table.split('/')
        type = self.safe_string(parts, 0)
        if type == 'spot':
            part1 = self.safe_string(parts, 1)
            if part1 == 'margin_account':
                type = 'margin'
        data = self.safe_value(message, 'data', [])
        for i in range(0, len(data)):
            balance = self.parseBalanceByType(type, data)
            oldBalance = self.safe_value(self.balance, type, {})
            newBalance = self.deep_extend(oldBalance, balance)
            self.balance[type] = self.parse_balance(newBalance)
            client.resolve(self.balance[type], table)

    def handle_subscription_status(self, client, message):
        #
        #     {"event":"subscribe","channel":"spot/depth:BTC-USDT"}
        #
        # channel = self.safe_string(message, 'channel')
        # client.subscriptions[channel] = message
        return message

    def handle_authenticate(self, client, message):
        #
        #     {event: 'login', success: True}
        #
        client.resolve(message, 'authenticated')
        return message

    def ping(self, client):
        # okex does not support built-in ws protocol-level ping-pong
        # instead it requires custom text-based ping-pong
        return 'ping'

    def handle_pong(self, client, message):
        client.lastPong = self.milliseconds()
        return message

    def handle_error_message(self, client, message):
        #
        #     {event: 'error', message: 'Invalid sign', errorCode: 30013}
        #     {"event":"error","message":"Unrecognized request: {\"event\":\"subscribe\",\"channel\":\"spot/depth:BTC-USDT\"}","errorCode":30039}
        #
        errorCode = self.safe_string(message, 'errorCode')
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
                method = 'login'
                if method in client.subscriptions:
                    del client.subscriptions[method]
                return False
        return message

    def handle_message(self, client, message):
        if not self.handle_error_message(client, message):
            return
        #
        #     {"event":"error","message":"Unrecognized request: {\"event\":\"subscribe\",\"channel\":\"spot/depth:BTC-USDT\"}","errorCode":30039}
        #     {"event":"subscribe","channel":"spot/depth:BTC-USDT"}
        #     {
        #         table: "spot/depth",
        #         action: "partial",
        #         data: [
        #             {
        #                 instrument_id:   "BTC-USDT",
        #                 asks: [
        #                     ["5301.8", "0.03763319", "1"],
        #                     ["5302.4", "0.00305", "2"],
        #                 ],
        #                 bids: [
        #                     ["5301.7", "0.58911427", "6"],
        #                     ["5301.6", "0.01222922", "4"],
        #                 ],
        #                 timestamp: "2020-03-16T03:25:00.440Z",
        #                 checksum: -2088736623
        #             }
        #         ]
        #     }
        #
        if message == 'pong':
            return self.handle_pong(client, message)
        table = self.safe_string(message, 'table')
        if table is None:
            event = self.safe_string(message, 'event')
            if event is not None:
                methods = {
                    # 'info': self.handleSystemStatus,
                    # 'book': 'handleOrderBook',
                    'login': self.handle_authenticate,
                    'subscribe': self.handle_subscription_status,
                }
                method = self.safe_value(methods, event)
                if method is None:
                    return message
                else:
                    return method(client, message)
        else:
            parts = table.split('/')
            name = self.safe_string(parts, 1)
            methods = {
                'depth': self.handle_order_book,
                'depth5': self.handle_order_book,
                'depth_l2_tbt': self.handle_order_book,
                'ticker': self.handle_ticker,
                'trade': self.handle_trade,
                'account': self.handle_balance,
                'margin_account': self.handle_balance,
                # ...
            }
            method = self.safe_value(methods, name)
            if name.find('candle') >= 0:
                method = self.handle_ohlcv
            if method is None:
                return message
            else:
                return method(client, message)
