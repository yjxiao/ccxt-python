# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
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
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': 'emulated',
                'fetchMyTrades': False,
                'fetchTickers': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/36770310-adfa764e-1c5a-11e8-8e09-449daac3d2fb.jpg',
                'api': {
                    'web': 'https://trade.coinegg.com/web',
                    'rest': 'https://api.coinegg.com/api/v1',
                },
                'www': 'https://www.coinegg.com',
                'doc': 'https://www.coinegg.com/explain.api.html',
                'fees': 'https://www.coinegg.com/fee.html',
                'referral': 'https://www.coinegg.com/user/register?invite=523218',
            },
            'api': {
                'web': {
                    'get': [
                        'symbol/ticker?right_coin={quote}',
                        '{quote}/trends',
                        '{quote}/{base}/order',
                        '{quote}/{base}/trades',
                        '{quote}/{base}/depth.js',
                    ],
                },
                'public': {
                    'get': [
                        'ticker/region/{quote}',
                        'depth/region/{quote}',
                        'orders/region/{quote}',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'trade_add/region/{quote}',
                        'trade_cancel/region/{quote}',
                        'trade_view/region/{quote}',
                        'trade_list/region/{quote}',
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
            'errorMessages': {
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
            },
            'options': {
                'quoteIds': ['btc', 'eth', 'usc', 'usdt'],
            },
            'commonCurrencies': {
                'JBC': 'JubaoCoin',
            },
        })

    def fetch_markets(self, params={}):
        quoteIds = self.options['quoteIds']
        result = []
        for b in range(0, len(quoteIds)):
            quoteId = quoteIds[b]
            response = self.webGetSymbolTickerRightCoinQuote({
                'quote': quoteId,
            })
            tickers = self.safe_value(response, 'data', [])
            for i in range(0, len(tickers)):
                ticker = tickers[i]
                id = ticker['symbol']
                baseId = id.split('_')[0]
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                symbol = base + '/' + quote
                precision = {
                    'amount': 8,
                    'price': 8,
                }
                result.append({
                    'id': id,
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
                    'info': ticker,
                })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'change')
        open = None
        change = None
        average = None
        if percentage is not None:
            relativeChange = percentage / 100
            open = last / self.sum(1, relativeChange)
            change = last - open
            average = self.sum(last, open) / 2
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
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': self.safe_float(ticker, 'quoteVol'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        response = self.publicGetTickerRegionQuote(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        response = self.publicGetDepthRegionQuote(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is not None:
            timestamp *= 1000
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        symbol = market['symbol']
        cost = None
        if amount is not None:
            if price is not None:
                cost = self.cost_to_precision(symbol, price * amount)
        type = 'limit'
        side = self.safe_string(trade, 'type')
        id = self.safe_string(trade, 'tid')
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        response = self.publicGetOrdersRegionQuote(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalance(params)
        result = {'info': response}
        data = self.safe_value(response, 'data', {})
        balances = self.omit(data, 'uid')
        keys = list(balances.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            currencyId, accountType = key.split('_')
            code = currencyId
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            else:
                code = self.common_currency_code(currencyId.upper())
            if not(code in list(result.keys())):
                result[code] = self.account()
            type = 'used' if (accountType == 'lock') else 'free'
            result[code][type] = self.safe_float(balances, key)
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'datetime'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount_original')
        remaining = self.safe_float(order, 'amount_outstanding')
        filled = None
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
        status = self.safe_string(order, 'status')
        if status == 'cancelled':
            status = 'canceled'
        else:
            status = 'open' if remaining else 'closed'
        info = self.safe_value(order, 'info', order)
        type = 'limit'
        side = self.safe_string(order, 'type')
        id = self.safe_string(order, 'id')
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': info,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
            'type': side,
            'amount': amount,
            'price': price,
        }
        response = self.privatePostTradeAddRegionQuote(self.extend(request, params))
        id = self.safe_string(response, 'id')
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

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': id,
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        return self.privatePostTradeCancelRegionQuote(self.extend(request, params))

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': id,
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        response = self.privatePostTradeViewRegionQuote(self.extend(request, params))
        return self.parse_order(response['data'], market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'quote': market['quoteId'],
        }
        if since is not None:
            request['since'] = since / 1000
        response = self.privatePostTradeListRegionQuote(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'type': 'open',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        apiType = 'rest'
        if api == 'web':
            apiType = api
        url = self.urls['api'][apiType] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or api == 'web':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.urlencode(self.extend({
                'key': self.apiKey,
                'nonce': self.nonce(),
            }, query))
            secret = self.hash(self.encode(self.secret))
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

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if response is None:
            return
        # private endpoints return the following structure:
        # {"result":true,"data":{...}} - success
        # {"result":false,"code":"103"} - failure
        # {"code":0,"msg":"Suceess","data":{"uid":"2716039","btc_balance":"0.00000000","btc_lock":"0.00000000","xrp_balance":"0.00000000","xrp_lock":"0.00000000"}}
        result = self.safe_value(response, 'result')
        if result is None:
            # public endpoint ← self comment left here by the contributor, in fact a missing result does not necessarily mean a public endpoint...
            # we should just check the code and don't rely on the result at all here...
            return
        if result is True:
            # success
            return
        errorCode = self.safe_string(response, 'code')
        errorMessages = self.errorMessages
        message = self.safe_string(errorMessages, errorCode, 'Unknown Error')
        if errorCode in self.exceptions:
            raise self.exceptions[errorCode](self.id + ' ' + message)
        else:
            raise ExchangeError(self.id + ' ' + message)
