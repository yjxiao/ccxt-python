# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import DDoSProtection


class btcalpha (Exchange):

    def describe(self):
        return self.deep_extend(super(btcalpha, self).describe(), {
            'id': 'btcalpha',
            'name': 'BTC-Alpha',
            'countries': ['US'],
            'version': 'v1',
            'has': {
                'fetchTicker': False,
                'fetchOHLCV': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
            },
            'timeframes': {
                '1m': '1',
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '4h': '240',
                '1d': 'D',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/42625213-dabaa5da-85cf-11e8-8f99-aa8f8f7699f0.jpg',
                'api': 'https://btc-alpha.com/api',
                'www': 'https://btc-alpha.com',
                'doc': 'https://btc-alpha.github.io/api-docs',
                'fees': 'https://btc-alpha.com/fees/',
                'referral': 'https://btc-alpha.com/?r=123788',
            },
            'api': {
                'public': {
                    'get': [
                        'currencies/',
                        'pairs/',
                        'orderbook/{pair_name}/',
                        'exchanges/',
                        'charts/{pair}/{type}/chart/',
                    ],
                },
                'private': {
                    'get': [
                        'wallets/',
                        'orders/own/',
                        'order/{id}/',
                        'exchanges/own/',
                        'deposits/',
                        'withdraws/',
                    ],
                    'post': [
                        'order/',
                        'order-cancel/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.00135,
                        'LTC': 0.0035,
                        'XMR': 0.018,
                        'ZEC': 0.002,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'SIB': 1.5,
                        'CCRB': 4,
                        'PZM': 0.05,
                        'ITI': 0.05,
                        'DCY': 5,
                        'R': 5,
                        'ATB': 0.05,
                        'BRIA': 0.05,
                        'KZC': 0.05,
                        'HWC': 1,
                        'SPA': 1,
                        'SMS': 0.001,
                        'REC': 0.01,
                        'SUP': 1,
                        'BQ': 100,
                        'GDS': 0.1,
                        'EVN': 300,
                        'TRKC': 0.01,
                        'UNI': 1,
                        'STN': 1,
                        'BCH': None,
                        'QBIC': 0.5,
                    },
                },
            },
        })

    async def fetch_markets(self):
        markets = await self.publicGetPairs()
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['name']
            base = self.common_currency_code(market['currency1'])
            quote = self.common_currency_code(market['currency2'])
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': int(market['price_precision']),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': float(market['minimum_order_size']),
                        'max': float(market['maximum_order_size']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': math.pow(10, precision['price']),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair_name': self.market_id(symbol),
        }
        if limit:
            request['limit_sell'] = limit
            request['limit_buy'] = limit
        reponse = await self.publicGetOrderbookPairName(self.extend(request, params))
        return self.parse_order_book(reponse, None, 'buy', 'sell', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        symbol = None
        if not market:
            market = self.safe_value(self.marketsById, trade['pair'])
        if market:
            symbol = market['symbol']
        timestamp = int(trade['timestamp'] * 1000)
        price = float(trade['price'])
        amount = float(trade['amount'])
        cost = self.cost_to_precision(symbol, price * amount)
        id = self.safe_string(trade, 'id')
        if not id:
            id = self.safe_string(trade, 'tid')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': self.safe_string(trade, 'o_id'),
            'type': 'limit',
            'side': trade['type'],
            'price': price,
            'amount': amount,
            'cost': float(cost),
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        if limit:
            request['limit'] = limit
        trades = await self.publicGetExchanges(self.extend(request, params))
        return self.parse_trades(trades, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='5m', since=None, limit=None):
        return [
            ohlcv['time'] * 1000,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['volume'],
        ]

    async def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': self.timeframes[timeframe],
        }
        if limit:
            request['limit'] = limit
        if since:
            request['since'] = int(since / 1000)
        response = await self.publicGetChartsPairTypeChart(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privateGetWallets(params)
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = self.common_currency_code(balance['currency'])
            used = self.safe_float(balance, 'reserve')
            total = self.safe_float(balance, 'balance')
            free = None
            if used is not None:
                if total is not None:
                    free = total - used
            result[currency] = {
                'free': free,
                'used': used,
                'total': total,
            }
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            '1': 'open',
            '2': 'canceled',
            '3': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        symbol = None
        if not market:
            market = self.safe_value(self.marketsById, order['pair'])
        if market:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'date')
        if timestamp is not None:
            timestamp *= 1000
        price = float(order['price'])
        amount = self.safe_float(order, 'amount')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'oid')
        if not id:
            id = self.safe_string(order, 'id')
        trades = self.safe_value(order, 'trades')
        if trades:
            trades = self.parse_trades(trades, market)
        side = self.safe_string_2(order, 'my_side', 'type')
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'trades': trades,
            'fee': None,
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostOrder(self.extend({
            'pair': market['id'],
            'type': side,
            'amount': amount,
            'price': self.price_to_precision(symbol, price),
        }, params))
        if not response['success']:
            raise InvalidOrder(self.id + ' ' + self.json(response))
        return self.parse_order(response, market)

    async def cancel_order(self, id, symbol=None, params={}):
        response = await self.privatePostOrderCancel(self.extend({
            'order': id,
        }, params))
        return response

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        order = await self.privateGetOrderId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(order)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol:
            market = self.market(symbol)
            request['pair'] = market['id']
        if limit:
            request['limit'] = limit
        orders = await self.privateGetOrdersOwn(self.extend(request, params))
        return self.parse_orders(orders, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, self.extend({
            'status': '1',
        }, params))
        return orders

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, self.extend({
            'status': '3',
        }, params))
        return orders

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if symbol:
            market = self.market(symbol)
            request['pair'] = market['id']
        if limit:
            request['limit'] = limit
        trades = await self.privateGetExchangesOwn(self.extend(request, params))
        return self.parse_trades(trades, None, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.urlencode(self.keysort(self.omit(params, self.extract_params(path))))
        url = self.urls['api'] + '/'
        if path != 'charts/{pair}/{type}/chart/':
            url += 'v1/'
        url += self.implode_params(path, params)
        headers = {'Accept': 'application/json'}
        if api == 'public':
            if len(query):
                url += '?' + query
        else:
            self.check_required_credentials()
            payload = self.apiKey
            if method == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = query
                payload += body
            elif len(query):
                url += '?' + query
            headers['X-KEY'] = self.apiKey
            headers['X-SIGN'] = self.hmac(self.encode(payload), self.encode(self.secret))
            headers['X-NONCE'] = str(self.nonce())
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if code < 400:
            return
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            message = self.id + ' ' + self.safe_value(response, 'detail', body)
            if code == 401 or code == 403:
                raise AuthenticationError(message)
            elif code == 429:
                raise DDoSProtection(message)
            raise ExchangeError(message)
