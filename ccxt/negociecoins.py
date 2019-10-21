# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ArgumentsRequired


class negociecoins (Exchange):

    def describe(self):
        return self.deep_extend(super(negociecoins, self).describe(), {
            'id': 'negociecoins',
            'name': 'NegocieCoins',
            'countries': ['BR'],
            'rateLimit': 1000,
            'version': 'v3',
            'has': {
                'createMarketOrder': False,
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
                    'maker': 0.005,
                    'taker': 0.005,
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
        timestamp = self.safe_timestamp(ticker, 'date')
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

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'PAR': market['id'],
        }
        ticker = self.publicGetPARTicker(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'PAR': self.market_id(symbol),
        }
        response = self.publicGetPAROrderbook(self.extend(request, params))
        return self.parse_order_book(response, None, 'bid', 'ask', 'price', 'quantity')

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'tid')
        type = 'limit'
        side = self.safe_string_lower(trade, 'type')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': None,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if since is None:
            since = 0
        request = {
            'PAR': market['id'],
            'timestamp_inicial': int(since / 1000),
        }
        response = self.publicGetPARTradesTimestampInicial(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserBalance(params)
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
            code = self.safe_currency_code(currencyId)
            openOrders = self.safe_float(balance, 'openOrders')
            withdraw = self.safe_float(balance, 'withdraw')
            account = {
                'free': self.safe_float(balance, 'total'),
                'used': self.sum(openOrders, withdraw),
                'total': self.safe_float(balance, 'available'),
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            'filled': 'closed',
            'cancelled': 'canceled',
            'partially filled': 'open',
            'pending': 'open',
            'rejected': 'rejected',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'pair')
            market = self.safe_value(self.marketsById, marketId)
            if market:
                symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'created'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'quantity')
        cost = self.safe_float(order, 'total')
        remaining = self.safe_float(order, 'pending_quantity')
        filled = self.safe_float(order, 'executed_quantity')
        status = self.parse_order_status(self.safe_string(order, 'status'))
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

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'price': self.price_to_precision(symbol, price),
            'volume': self.amount_to_precision(symbol, amount),
            'type': side,
        }
        response = self.privatePostUserOrder(self.extend(request, params))
        order = self.parse_order(response[0], market)
        id = order['id']
        self.orders[id] = order
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.markets[symbol]
        request = {
            'orderId': id,
        }
        response = self.privateDeleteUserOrderOrderId(self.extend(request, params))
        return self.parse_order(response[0], market)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderId': id,
        }
        order = self.privateGetUserOrderOrderId(self.extend(request, params))
        return self.parse_order(order[0])

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
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
        orders = self.privatePostUserOrders(self.extend(request, params))
        return self.parse_orders(orders, market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'pending',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'filled',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

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
            signature = self.decode(signature)
            auth = ':'.join([self.apiKey, signature, nonce, timestamp])
            headers = {
                'Authorization': 'amx ' + auth,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/json; charset=UTF-8'
                headers['Content-Length'] = len(body)
            elif len(queryString):
                url += '?' + queryString
                body = None
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
