# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce


class coinegg (Exchange):

    def describe(self):
        return self.deep_extend(super(coinegg, self).describe(), {
            'id': 'coinegg',
            'name': 'CoinEgg',
            'countries': ['CN', 'UK'],
            'has': {
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/36770310-adfa764e-1c5a-11e8-8e09-449daac3d2fb.jpg',
                'api': {
                    'web': 'https://www.coinegg.com/coin',
                    'rest': 'https://api.coinegg.com/api/v1',
                },
                'www': 'https://www.coinegg.com',
                'doc': 'https://www.coinegg.com/explain.api.html',
                'fees': 'https://www.coinegg.com/fee.html',
            },
            'api': {
                'web': {
                    'get': [
                        '{quote}/allcoin',
                        '{quote}/trends',
                        '{quote}/{base}/order',
                        '{quote}/{base}/trades',
                        '{quote}/{base}/depth.js',
                    ],
                },
                'public': {
                    'get': [
                        'ticker/{quote}',
                        'depth/{quote}',
                        'orders/{quote}',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                    ],
                    'post': [
                        'trade_add/{quote}',
                        'trade_cancel/{quote}',
                        'trade_view/{quote}',
                        'trade_list/{quote}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.008,
                        'BCH': 0.002,
                        'LTC': 0.001,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'NEO': 0,
                        'QTUM': '1%',
                        'XRP': '1%',
                        'DOGE': '1%',
                        'LSK': '1%',
                        'XAS': '1%',
                        'BTS': '1%',
                        'GAME': '1%',
                        'GOOC': '1%',
                        'NXT': '1%',
                        'IFC': '1%',
                        'DNC': '1%',
                        'BLK': '1%',
                        'VRC': '1%',
                        'XPM': '1%',
                        'VTC': '1%',
                        'TFC': '1%',
                        'PLC': '1%',
                        'EAC': '1%',
                        'PPC': '1%',
                        'FZ': '1%',
                        'ZET': '1%',
                        'RSS': '1%',
                        'PGC': '1%',
                        'SKT': '1%',
                        'JBC': '1%',
                        'RIO': '1%',
                        'LKC': '1%',
                        'ZCC': '1%',
                        'MCC': '1%',
                        'QEC': '1%',
                        'MET': '1%',
                        'YTC': '1%',
                        'HLB': '1%',
                        'MRYC': '1%',
                        'MTC': '1%',
                        'KTC': 0,
                    },
                },
            },
            'exceptions': {
                '103': AuthenticationError,
                '104': AuthenticationError,
                '105': AuthenticationError,
                '106': InvalidNonce,
                '200': InsufficientFunds,
                '201': InvalidOrder,
                '202': InvalidOrder,
                '203': OrderNotFound,
                '402': DDoSProtection,
            },
        })

    async def fetch_markets(self):
        quoteIds = ['btc', 'usc']
        result = []
        for b in range(0, len(quoteIds)):
            quoteId = quoteIds[b]
            bases = await self.webGetQuoteAllcoin({
                'quote': quoteId,
            })
            baseIds = list(bases.keys())
            numBaseIds = len(baseIds)
            if numBaseIds < 1:
                raise ExchangeError(self.id + ' fetchMarkets() failed for ' + quoteId)
            for i in range(0, len(baseIds)):
                baseId = baseIds[i]
                market = bases[baseId]
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                id = baseId + quoteId
                symbol = base + '/' + quote
                precision = {
                    'amount': 8,
                    'price': 8,
                }
                lot = math.pow(10, -precision['amount'])
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'active': True,
                    'lot': lot,
                    'precision': precision,
                    'limits': {
                        'amount': {
                            'min': lot,
                            'max': math.pow(10, precision['amount']),
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

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = self.milliseconds()
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']),
            'low': float(ticker['low']),
            'bid': float(ticker['buy']),
            'ask': float(ticker['sell']),
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': float(ticker['last']),
            'change': self.safe_float(ticker, 'change'),
            'percentage': None,
            'average': None,
            'baseVolume': float(ticker['vol']),
            'quoteVolume': self.safe_float(ticker, 'quoteVol'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetTickerQuote(self.extend({
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }, params))
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        quoteIds = ['btc', 'usc']
        result = {}
        for b in range(0, len(quoteIds)):
            quoteId = quoteIds[b]
            tickers = await self.webGetQuoteAllcoin({
                'quote': quoteId,
            })
            baseIds = list(tickers.keys())
            if not len(baseIds):
                raise ExchangeError('fetchTickers failed')
            for i in range(0, len(baseIds)):
                baseId = baseIds[i]
                ticker = tickers[baseId]
                id = baseId + quoteId
                market = self.marketsById[id]
                symbol = market['symbol']
                result[symbol] = self.parse_ticker({
                    'high': ticker[4],
                    'low': ticker[5],
                    'buy': ticker[2],
                    'sell': ticker[3],
                    'last': ticker[1],
                    'change': ticker[8],
                    'vol': ticker[6],
                    'quoteVol': ticker[7],
                }, market)
        return result

    async def fetch_order_book(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        orderbook = await self.publicGetDepthQuote(self.extend({
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }, params))
        return self.parse_order_book(orderbook)

    def parse_trade(self, trade, market=None):
        timestamp = int(trade['date']) * 1000
        price = float(trade['price'])
        amount = float(trade['amount'])
        symbol = market['symbol']
        cost = self.cost_to_precision(symbol, price * amount)
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'tid'),
            'order': None,
            'type': 'limit',
            'side': trade['type'],
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        trades = await self.publicGetOrdersQuote(self.extend({
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }, params))
        return self.parse_trades(trades, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privateGetBalance(params)
        result = {'info': balances}
        balances = self.omit(balances['data'], 'uid')
        rows = list(balances.keys())
        for i in range(0, len(rows)):
            row = rows[i]
            id, type = row.split('_')
            id = id.upper()
            type = type.upper()
            currency = self.common_currency_code(id)
            if currency in self.currencies:
                if not(currency in list(result.keys())):
                    result[currency] = {
                        'free': None,
                        'used': None,
                        'total': None,
                    }
                type = (type == 'used' if 'LOCK' else 'free')
                result[currency][type] = float(balances[row])
        currencies = list(result.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            result[currency]['total'] = self.sum(result[currency]['free'], result[currency]['used'])
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        symbol = market['symbol']
        timestamp = self.parse8601(order['datetime'])
        price = float(order['price'])
        amount = float(order['amount_original'])
        remaining = float(order['amount_outstanding'])
        filled = amount - remaining
        status = self.safe_string(order, 'status')
        if status == 'cancelled':
            status = 'canceled'
        else:
            status = 'open' if remaining else 'closed'
        info = self.safe_value(order, 'info', order)
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': order['type'],
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': info,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostTradeAddQuote(self.extend({
            'coin': market['baseId'],
            'quote': market['quoteId'],
            'type': side,
            'amount': amount,
            'price': price,
        }, params))
        if not response['status']:
            raise InvalidOrder(self.json(response))
        id = response['id']
        order = self.parse_order({
            'id': id,
            'datetime': self.ymdhms(self.milliseconds()),
            'amount_original': amount,
            'amount_outstanding': amount,
            'price': price,
            'type': side,
            'info': response,
        }, market)
        self.orders[id] = order
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostTradeCancelQuote(self.extend({
            'id': id,
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }, params))
        if not response['status']:
            raise ExchangeError(self.json(response))
        return response

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostTradeViewQuote(self.extend({
            'id': id,
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }, params))
        return self.parse_order(response['data'], market)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        if since is not None:
            request['since'] = since / 1000
        orders = await self.privatePostTradeListQuote(self.extend(request, params))
        return self.parse_orders(orders['data'], market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        result = await self.fetch_orders(symbol, since, limit, self.extend({
            'type': 'open',
        }, params))
        return result

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        apiType = 'rest'
        if api == 'web':
            apiType = api
        url = self.urls['api'][apiType] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or api == 'web':
            if api == 'web':
                query['t'] = self.nonce()
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.urlencode(self.extend({
                'key': self.apiKey,
                'nonce': self.nonce(),
            }, query))
            secret = self.hash(self.secret)
            signature = self.hmac(self.encode(query), self.encode(secret))
            query += '&' + 'signature=' + signature
            if method == 'GET':
                url += '?' + query
            else:
                headers = {
                    'Content-type': 'application/x-www-form-urlencoded',
                }
                body = query
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        errorMessages = {
            '100': 'Required parameters can not be empty',
            '101': 'Illegal parameter',
            '102': 'coin does not exist',
            '103': 'Key does not exist',
            '104': 'Signature does not match',
            '105': 'Insufficient permissions',
            '106': 'Request expired(nonce error)',
            '200': 'Lack of balance',
            '201': 'Too small for the number of trading',
            '202': 'Price must be in 0 - 1000000',
            '203': 'Order does not exist',
            '204': 'Pending order amount must be above 0.001 BTC',
            '205': 'Restrict pending order prices',
            '206': 'Decimal place error',
            '401': 'System error',
            '402': 'Requests are too frequent',
            '403': 'Non-open API',
            '404': 'IP restriction does not request the resource',
            '405': 'Currency transactions are temporarily closed',
        }
        # checks against error codes
        if isinstance(body, basestring):
            if len(body) > 0:
                if body[0] == '{':
                    response = json.loads(body)
                    error = self.safe_string(response, 'code')
                    message = self.safe_string(errorMessages, code, 'Error')
                    if error is not None:
                        if error in self.exceptions:
                            raise self.exceptions[error](self.id + ' ' + message)
                        else:
                            raise ExchangeError(self.id + message)
