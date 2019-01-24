# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import DDoSProtection


class coinfalcon (Exchange):

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

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarkets()
        markets = response['data']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId, quoteId = market['name'].split('-')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
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
            'change': float(ticker['change_in_24h']),
            'percentage': None,
            'average': None,
            'baseVolume': float(ticker['volume']),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        tickers = await self.fetch_tickers(params)
        return tickers[symbol]

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetMarkets()
        tickers = response['data']
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        response = await self.publicGetMarketsMarketOrders(self.extend({
            'market': self.market_id(symbol),
            'level': '3',
        }, params))
        return self.parse_order_book(response['data'], None, 'bids', 'asks', 'price', 'size')

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['created_at'])
        price = float(trade['price'])
        amount = float(trade['size'])
        symbol = market['symbol']
        cost = float(self.cost_to_precision(symbol, price * amount))
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': None,
            'order': None,
            'type': None,
            'side': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since is not None:
            request['since'] = self.iso8601(since)
        response = await self.publicGetMarketsMarketTrades(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetUserAccounts(params)
        result = {'info': response}
        balances = response['data']
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency_code')
            uppercase = currencyId.upper()
            code = self.common_currency_code(uppercase)
            if uppercase in self.currencies_by_id:
                code = self.currencies_by_id[uppercase]['code']
            account = {
                'free': float(balance['available_balance']),
                'used': float(balance['hold_balance']),
                'total': float(balance['balance']),
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        if market is None:
            marketId = self.safe_string(order, 'market')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(order['created_at'])
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'size')
        filled = self.safe_float(order, 'size_filled')
        remaining = float(self.amount_to_precision(symbol, amount - filled))
        cost = float(self.price_to_precision(symbol, amount * price))
        # pending, open, partially_filled, fullfilled, canceled
        status = order['status']
        if status == 'fulfilled':
            status = 'closed'
        elif status == 'canceled':
            status = 'canceled'
        else:
            status = 'open'
        type = order['operation_type'].split('_')
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': type[0],
            'side': order['order_type'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        # price/size must be string
        amount = self.amount_to_precision(symbol, amount)
        request = {
            'market': market['id'],
            'size': amount,
            'order_type': side,
        }
        if type == 'limit':
            price = self.price_to_precision(symbol, price)
            request['price'] = str(price)
        request['operation_type'] = type + '_order'
        response = await self.privatePostUserOrders(self.extend(request, params))
        order = self.parse_order(response['data'], market)
        id = order['id']
        self.orders[id] = order
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privateDeleteUserOrdersId(self.extend({
            'id': id,
        }, params))
        market = self.market(symbol)
        return self.parse_order(response['data'], market)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privateGetUserOrdersId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response['data'])

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if symbol is not None:
            request['market'] = self.market_id(symbol)
        if since is not None:
            request['since_time'] = self.iso8601(self.milliseconds())
        # TODO: test status=all if it works for closed orders too
        response = await self.privateGetUserOrders(self.extend(request, params))
        return self.parse_orders(response['data'])

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + 'api/' + self.version + '/' + self.implode_params(path, params)
        url = self.urls['api'] + request
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
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
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if code < 400:
            return
        ErrorClass = self.safe_value({
            '401': AuthenticationError,
            '429': DDoSProtection,
        }, code, ExchangeError)
        raise ErrorClass(body)
