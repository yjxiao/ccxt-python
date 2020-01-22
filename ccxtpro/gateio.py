# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class gateio(ccxtpro.Exchange, ccxt.gateio):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'has': {
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTrades': True,
                'watchOHLCV': True,
                'watchBalance': True,
                'watchOrders': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://ws.gate.io/v3',
                },
            },
        })

    async def watch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        wsMarketId = marketId.upper()
        requestId = self.nonce()
        url = self.urls['api']['ws']
        if not limit:
            limit = 30
        elif limit != 1 and limit != 5 and limit != 10 and limit != 20 and limit != 30:
            raise ExchangeError(self.id + ' watchOrderBook limit argument must be None, 1, 5, 10, 20, or 30')
        interval = self.safe_string(params, 'interval', '0.00000001')
        floatInterval = float(interval)
        precision = -1 * math.log10(floatInterval)
        if (precision < 0) or (precision > 8) or (precision % 1 != 0.0):
            raise ExchangeError(self.id + ' invalid interval')
        messageHash = 'depth.update' + ':' + marketId
        subscribeMessage = {
            'id': requestId,
            'method': 'depth.subscribe',
            'params': [wsMarketId, limit, interval],
        }
        subscription = {
            'id': requestId,
        }
        future = self.watch(url, messageHash, subscribeMessage, messageHash, subscription)
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def sign_message(self, client, messageHash, message, params={}):
        # todo: implement gateio signMessage
        return message

    def limit_order_book(self, orderbook, symbol, limit=None, params={}):
        return orderbook.limit(limit)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book(self, client, message):
        params = self.safe_value(message, 'params', [])
        clean = self.safe_value(params, 0)
        book = self.safe_value(params, 1)
        marketId = self.safe_string_lower(params, 2)
        symbol = None
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
        else:
            symbol = marketId
        method = self.safe_string(message, 'method')
        messageHash = method + ':' + marketId
        orderBook = None
        if clean:
            orderBook = self.order_book({})
            self.orderbooks[symbol] = orderBook
        else:
            orderBook = self.orderbooks[symbol]
        self.handle_deltas(orderBook['asks'], self.safe_value(book, 'asks', []))
        self.handle_deltas(orderBook['bids'], self.safe_value(book, 'bids', []))
        client.resolve(orderBook, messageHash)

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        wsMarketId = marketId.upper()
        requestId = self.nonce()
        url = self.urls['api']['ws']
        subscribeMessage = {
            'id': requestId,
            'method': 'ticker.subscribe',
            'params': [wsMarketId],
        }
        subscription = {
            'id': requestId,
        }
        messageHash = 'ticker.update' + ':' + marketId
        return await self.watch(url, messageHash, subscribeMessage, messageHash, subscription)

    def handle_ticker(self, client, message):
        result = message['params']
        marketId = self.safe_string_lower(result, 0)
        market = None
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        ticker = result[1]
        parsed = self.parse_ticker(ticker, market)
        methodType = message['method']
        messageHash = methodType + ':' + marketId
        client.resolve(parsed, messageHash)

    async def watch_trades(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id'].upper()
        requestId = self.nonce()
        url = self.urls['api']['ws']
        subscribeMessage = {
            'id': requestId,
            'method': 'trades.subscribe',
            'params': [marketId],
        }
        subscription = {
            'id': requestId,
        }
        messageHash = 'trades.update' + ':' + marketId
        return await self.watch(url, messageHash, subscribeMessage, messageHash, subscription)

    def handle_trades(self, client, messsage):
        result = messsage['params']
        marketId = result[0]
        normalMarketId = marketId.lower()
        market = None
        if normalMarketId in self.markets_by_id:
            market = self.markets_by_id[normalMarketId]
        if not (marketId in self.trades):
            self.trades[marketId] = []
        trades = result[1]
        for i in range(0, len(trades)):
            trade = trades[i]
            parsed = self.parse_trade(trade, market)
            self.trades[marketId].append(parsed)
        methodType = messsage['method']
        messageHash = methodType + ':' + marketId
        client.resolve(self.trades[marketId], messageHash)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id'].upper()
        requestId = self.nonce()
        url = self.urls['api']['ws']
        interval = int(self.timeframes[timeframe])
        subscribeMessage = {
            'id': requestId,
            'method': 'kline.subscribe',
            'params': [marketId, interval],
        }
        subscription = {
            'id': requestId,
        }
        messageHash = 'kline.update' + ':' + marketId
        return await self.watch(url, messageHash, subscribeMessage, messageHash, subscription)

    async def authenticate(self):
        url = self.urls['api']['ws']
        client = self.client(url)
        future = client.future('authenticated')
        method = 'server.sign'
        authenticate = self.safe_value(client.subscriptions, method)
        if authenticate is None:
            requestId = self.milliseconds()
            requestIdString = str(requestId)
            signature = self.hmac(self.encode(requestIdString), self.encode(self.secret), hashlib.sha512, 'base64')
            authenticateMessage = {
                'id': requestId,
                'method': method,
                'params': [self.apiKey, self.decode(signature), requestId],
            }
            subscribe = {
                'id': requestId,
                'method': self.handle_authentication_message,
            }
            self.spawn(self.watch, url, requestId, authenticateMessage, method, subscribe)
        return await future

    def handle_ohlcv(self, client, message):
        ohlcv = message['params'][0]
        marketId = ohlcv[7]
        normalMarketId = marketId.lower()
        market = None
        if normalMarketId in self.markets_by_id:
            market = self.markets_by_id[normalMarketId]
        parsed = self.parse_ohlcv(ohlcv, market)
        methodType = message['method']
        messageHash = methodType + ':' + marketId
        client.resolve(parsed, messageHash)

    async def watch_balance(self, params={}):
        await self.load_markets()
        self.check_required_credentials()
        url = self.urls['api']['ws']
        future = self.authenticate()
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
        return await self.after_dropped(future, self.watch, url, method, subscribeMessage, method, subscription)

    async def fetch_balance_snapshot(self):
        await self.load_markets()
        self.check_required_credentials()
        url = self.urls['api']['ws']
        future = self.authenticate()
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
        return await self.after_dropped(future, self.watch, url, requestId, subscribeMessage, method, subscription)

    def handle_balance_snapshot(self, client, message):
        messageHash = message['id']
        result = message['result']
        self.handle_balance_message(client, messageHash, result)
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
            account['free'] = self.safe_float(balance, 'available')
            account['used'] = self.safe_float(balance, 'freeze')
            self.balance[code] = account
        client.resolve(self.parse_balance(self.balance), messageHash)

    async def watch_orders(self, params={}):
        self.check_required_credentials()
        await self.load_markets()
        url = self.urls['api']['ws']
        future = self.authenticate()
        requestId = self.nonce()
        method = 'order.update'
        subscribeMessage = {
            'id': requestId,
            'method': 'order.subscribe',
            'params': [],
        }
        return await self.after_dropped(future, self.watch, url, method, subscribeMessage, method)

    def handle_order(self, client, message):
        messageHash = message['method']
        order = message['params'][1]
        marketId = order['market']
        normalMarketId = marketId.lower()
        market = None
        if normalMarketId in self.markets_by_id:
            market = self.markets_by_id[normalMarketId]
        parsed = self.parse_order(order, market)
        client.resolve(parsed, messageHash)

    def handle_authentication_message(self, client, message, subscription):
        result = self.safe_value(message, 'result')
        status = self.safe_string(result, 'status')
        if status == 'success':
            # client.resolve(True, 'authenticated') will del the future
            # we want to remember that we are authenticated in subsequent call to private methods
            future = client.futures['authenticated']
            future.resolve(True)
        else:
            # del authenticate subscribeHash to release the "subscribe lock"
            # allows subsequent calls to subscribe to reauthenticate
            # avoids sending two authentication messages before receiving a reply
            error = AuthenticationError('not success')
            client.reject(error, 'autheticated')
            if 'server.sign' in client.subscriptions:
                del client.subscriptions['server.sign']

    def handle_error_message(self, client, message):
        # todo use error map here
        error = self.safe_value(message, 'error', {})
        code = self.safe_integer(error, 'code')
        if code == 11 or code == 6:
            error = AuthenticationError('invalid credentials')
            client.reject(error, message['id'])
            client.reject(error, 'authenticated')

    def handle_balance_subscription(self, client, message, subscription):
        self.spawn(self.fetch_balance_snapshot)

    def handle_subscription_status(self, client, message):
        messageId = message['id']
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        subscription = self.safe_value(subscriptionsById, messageId, {})
        if 'method' in subscription:
            method = subscription['method']
            method(client, message, subscription)
        client.resolve(message, messageId)

    def handle_message(self, client, message):
        self.handle_error_message(client, message)
        methods = {
            'depth.update': self.handle_order_book,
            'ticker.update': self.handle_ticker,
            'trades.update': self.handle_trades,
            'kline.update': self.handle_ohlcv,
            'balance.update': self.handle_balance,
            'order.update': self.handle_order,
        }
        methodType = self.safe_string(message, 'method')
        method = self.safe_value(methods, methodType)
        if method is None:
            messageId = self.safe_integer(message, 'id')
            if messageId is not None:
                self.handle_subscription_status(client, message)
        else:
            method(client, message)
