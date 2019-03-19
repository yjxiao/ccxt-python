# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib


class negociecoins (Exchange):

    def describe(self):
        return self.deep_extend(super(negociecoins, self).describe(), {
            'id': 'negociecoins',
            'name': 'NegocieCoins',
            'countries': ['BR'],
            'rateLimit': 1000,
            'version': 'v3',
            'has': {
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38008571-25a6246e-3258-11e8-969b-aeb691049245.jpg',
                'api': {
                    'public': 'https://broker.negociecoins.com.br/api/v3',
                    'private': 'https://broker.negociecoins.com.br/tradeapi/v1',
                },
                'www': 'https://www.negociecoins.com.br',
                'doc': [
                    'https://www.negociecoins.com.br/documentacao-tradeapi',
                    'https://www.negociecoins.com.br/documentacao-api',
                ],
                'fees': 'https://www.negociecoins.com.br/comissoes',
            },
            'api': {
                'public': {
                    'get': [
                        '{PAR}/ticker',
                        '{PAR}/orderbook',
                        '{PAR}/trades',
                        '{PAR}/trades/{timestamp_inicial}',
                        '{PAR}/trades/{timestamp_inicial}/{timestamp_final}',
                    ],
                },
                'private': {
                    'get': [
                        'user/balance',
                        'user/order/{orderId}',
                    ],
                    'post': [
                        'user/order',
                        'user/orders',
                    ],
                    'delete': [
                        'user/order/{orderId}',
                    ],
                },
            },
            'markets': {
                'B2X/BRL': {'id': 'b2xbrl', 'symbol': 'B2X/BRL', 'base': 'B2X', 'quote': 'BRL'},
                'BCH/BRL': {'id': 'bchbrl', 'symbol': 'BCH/BRL', 'base': 'BCH', 'quote': 'BRL'},
                'BTC/BRL': {'id': 'btcbrl', 'symbol': 'BTC/BRL', 'base': 'BTC', 'quote': 'BRL'},
                'BTG/BRL': {'id': 'btgbrl', 'symbol': 'BTG/BRL', 'base': 'BTG', 'quote': 'BRL'},
                'DASH/BRL': {'id': 'dashbrl', 'symbol': 'DASH/BRL', 'base': 'DASH', 'quote': 'BRL'},
                'LTC/BRL': {'id': 'ltcbrl', 'symbol': 'LTC/BRL', 'base': 'LTC', 'quote': 'BRL'},
            },
            'fees': {
                'trading': {
                    'maker': 0.003,
                    'taker': 0.004,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.001,
                        'BCH': 0.00003,
                        'BTG': 0.00009,
                        'LTC': 0.005,
                    },
                },
            },
            'limits': {
                'amount': {
                    'min': 0.001,
                    'max': None,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['date'] * 1000
        symbol = market['symbol'] if (market is not None) else None
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetPARTicker(self.extend({
            'PAR': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        orderbook = await self.publicGetPAROrderbook(self.extend({
            'PAR': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook, None, 'bid', 'ask', 'price', 'quantity')

    def parse_trade(self, trade, market=None):
        timestamp = trade['date'] * 1000
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        symbol = market['symbol']
        cost = float(self.cost_to_precision(symbol, price * amount))
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'tid'),
            'order': None,
            'type': 'limit',
            'side': trade['type'].lower(),
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if since is None:
            since = 0
        request = {
            'PAR': market['id'],
            'timestamp_inicial': int(since / 1000),
        }
        trades = await self.publicGetPARTradesTimestampInicial(self.extend(request, params))
        return self.parse_trades(trades, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetUserBalance(params)
        #
        #     {
        #         "coins": [
        #             {"name":"BRL","available":0.0,"openOrders":0.0,"withdraw":0.0,"total":0.0},
        #             {"name":"BTC","available":0.0,"openOrders":0.0,"withdraw":0.0,"total":0.0},
        #         ],
        #     }
        #
        result = {'info': response}
        balances = self.safe_value(response, 'coins')
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'name')
            code = self.common_currency_code(currencyId)
            openOrders = self.safe_float(balance, 'openOrders')
            withdraw = self.safe_float(balance, 'withdraw')
            account = {
                'free': self.safe_float(balance, 'total'),
                'used': self.sum(openOrders, withdraw),
                'total': self.safe_float(balance, 'available'),
            }
            account['used'] = account['total'] - account['free']
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        symbol = None
        if market is None:
            market = self.safe_value(self.marketsById, order['pair'])
            if market:
                symbol = market['symbol']
        timestamp = self.parse8601(order['created'])
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'quantity')
        cost = self.safe_float(order, 'total')
        remaining = self.safe_float(order, 'pending_quantity')
        filled = self.safe_float(order, 'executed_quantity')
        status = order['status']
        # cancelled, filled, partially filled, pending, rejected
        if status == 'filled':
            status = 'closed'
        elif status == 'cancelled':
            status = 'canceled'
        else:
            status = 'open'
        trades = None
        # if order['operations']:
        #     trades = self.parse_trades(order['operations'])
        return {
            'id': str(order['id']),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': order['type'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': {
                'currency': market['quote'],
                'cost': self.safe_float(order, 'fee'),
            },
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostUserOrder(self.extend({
            'pair': market['id'],
            'price': self.price_to_precision(symbol, price),
            'volume': self.amount_to_precision(symbol, amount),
            'type': side,
        }, params))
        order = self.parse_order(response[0], market)
        id = order['id']
        self.orders[id] = order
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        response = await self.privateDeleteUserOrderOrderId(self.extend({
            'orderId': id,
        }, params))
        return self.parse_order(response[0], market)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        order = await self.privateGetUserOrderOrderId(self.extend({
            'orderId': id,
        }, params))
        return self.parse_order(order[0])

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            # type: buy, sell
            # status: cancelled, filled, partially filled, pending, rejected
            # startId
            # endId
            # startDate yyyy-MM-dd
            # endDate: yyyy-MM-dd
        }
        if since is not None:
            request['startDate'] = self.ymd(since)
        if limit is not None:
            request['pageSize'] = limit
        orders = await self.privatePostUserOrders(self.extend(request, params))
        return self.parse_orders(orders, market)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders(symbol, since, limit, self.extend({
            'status': 'pending',
        }, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders(symbol, since, limit, self.extend({
            'status': 'filled',
        }, params))

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        queryString = self.urlencode(query)
        if api == 'public':
            if len(queryString):
                url += '?' + queryString
        else:
            self.check_required_credentials()
            timestamp = str(self.seconds())
            nonce = str(self.nonce())
            content = ''
            if len(queryString):
                body = self.json(query)
                content = self.hash(self.encode(body), 'md5', 'base64')
            else:
                body = ''
            uri = self.encode_uri_component(url).lower()
            payload = ''.join([self.apiKey, method, uri, timestamp, nonce, content])
            secret = base64.b64decode(self.secret)
            signature = self.hmac(self.encode(payload), secret, hashlib.sha256, 'base64')
            signature = self.binary_to_string(signature)
            auth = ':'.join([self.apiKey, signature, nonce, timestamp])
            headers = {
                'Authorization': 'amx ' + auth,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/json charset=UTF-8'
                headers['Content-Length'] = len(body)
            elif len(queryString):
                url += '?' + queryString
                body = None
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
