# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import DDoSProtection


class coinfalcon(Exchange):

    def describe(self):
        return self.deep_extend(super(coinfalcon, self).describe(), {
            'id': 'coinfalcon',
            'name': 'CoinFalcon',
            'countries': ['GB'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'fetchTickers': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/41822275-ed982188-77f5-11e8-92bb-496bcd14ca52.jpg',
                'api': 'https://coinfalcon.com',
                'www': 'https://coinfalcon.com',
                'doc': 'https://docs.coinfalcon.com',
                'fees': 'https://coinfalcon.com/fees',
                'referral': 'https://coinfalcon.com/?ref=CFJSVGTUPASB',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'markets/{market}/orders',
                        'markets/{market}/trades',
                    ],
                },
                'private': {
                    'get': [
                        'user/accounts',
                        'user/orders',
                        'user/orders/{id}',
                        'user/trades',
                    ],
                    'post': [
                        'user/orders',
                    ],
                    'delete': [
                        'user/orders/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'maker': 0.0,
                    'taker': 0.002,  # tiered fee starts at 0.2%
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetMarkets(params)
        markets = self.safe_value(response, 'data')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId, quoteId = market['name'].split('-')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'size_precision'),
                'price': self.safe_integer(market, 'price_precision'),
            }
            result.append({
                'id': market['name'],
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        if market is None:
            marketId = self.safe_string(ticker, 'name')
            market = self.safe_value(self.markets_by_id, marketId, market)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.milliseconds()
        last = float(ticker['last_price'])
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'change_in_24h'),
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'volume'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        tickers = self.fetch_tickers(params)
        return tickers[symbol]

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetMarkets(params)
        tickers = self.safe_value(response, 'data')
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'level': '3',
        }
        response = self.publicGetMarketsMarketOrders(self.extend(request, params))
        return self.parse_order_book(response['data'], None, 'bids', 'asks', 'price', 'size')

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'size')
        symbol = market['symbol']
        cost = None
        if price is not None:
            if amount is not None:
                cost = float(self.cost_to_precision(symbol, price * amount))
        tradeId = self.safe_string(trade, 'id')
        side = self.safe_string(trade, 'side')
        orderId = self.safe_string(trade, 'order_id')
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCurrencyCode = self.safe_string(trade, 'fee_currency_code')
            fee = {
                'cost': feeCost,
                'currency': self.safe_currency_code(feeCurrencyCode),
            }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since is not None:
            request['start_time'] = self.iso8601(since)
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetUserTrades(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since is not None:
            request['since'] = self.iso8601(since)
        response = self.publicGetMarketsMarketTrades(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserAccounts(params)
        result = {'info': response}
        balances = self.safe_value(response, 'data')
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = {
                'free': self.safe_float(balance, 'available_balance'),
                'used': self.safe_float(balance, 'hold_balance'),
                'total': self.safe_float(balance, 'balance'),
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            'fulfilled': 'closed',
            'canceled': 'canceled',
            'pending': 'open',
            'open': 'open',
            'partially_filled': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        if market is None:
            marketId = self.safe_string(order, 'market')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'size')
        filled = self.safe_float(order, 'size_filled')
        remaining = None
        cost = None
        if amount is not None:
            if filled is not None:
                remaining = float(self.amount_to_precision(symbol, amount - filled))
            if price is not None:
                cost = float(self.price_to_precision(symbol, filled * price))
        status = self.parse_order_status(self.safe_string(order, 'status'))
        type = self.safe_string(order, 'operation_type')
        if type is not None:
            type = type.split('_')
            type = type[0]
        side = self.safe_string(order, 'order_type')
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        # price/size must be string
        request = {
            'market': market['id'],
            'size': self.amount_to_precision(symbol, amount),
            'order_type': side,
        }
        if type == 'limit':
            price = self.price_to_precision(symbol, price)
            request['price'] = str(price)
        request['operation_type'] = type + '_order'
        response = self.privatePostUserOrders(self.extend(request, params))
        order = self.parse_order(response['data'], market)
        id = order['id']
        self.orders[id] = order
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateDeleteUserOrdersId(self.extend(request, params))
        market = self.market(symbol)
        return self.parse_order(response['data'], market)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateGetUserOrdersId(self.extend(request, params))
        return self.parse_order(response['data'])

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        if symbol is not None:
            request['market'] = self.market_id(symbol)
        if since is not None:
            request['since_time'] = self.iso8601(self.milliseconds())
        # TODO: test status=all if it works for closed orders too
        response = self.privateGetUserOrders(self.extend(request, params))
        return self.parse_orders(response['data'])

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/api/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                request += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    request += '?' + self.urlencode(query)
            else:
                body = self.json(query)
            seconds = str(self.seconds())
            payload = '|'.join([seconds, method, request])
            if body:
                payload += '|' + body
            signature = self.hmac(self.encode(payload), self.encode(self.secret))
            headers = {
                'CF-API-KEY': self.apiKey,
                'CF-API-TIMESTAMP': seconds,
                'CF-API-SIGNATURE': signature,
                'Content-Type': 'application/json',
            }
        url = self.urls['api'] + request
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if code < 400:
            return
        ErrorClass = self.safe_value({
            '401': AuthenticationError,
            '429': DDoSProtection,
        }, code, ExchangeError)
        raise ErrorClass(body)
