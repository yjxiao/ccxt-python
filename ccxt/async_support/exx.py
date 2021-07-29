# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.precise import Precise


class exx(Exchange):

    def describe(self):
        return self.deep_extend(super(exx, self).describe(), {
            'id': 'exx',
            'name': 'EXX',
            'countries': ['CN'],
            'rateLimit': 1000 / 10,
            'userAgent': self.userAgents['chrome'],
            'has': {
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchMarkets': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/37770292-fbf613d0-2de4-11e8-9f79-f2dc451b8ccb.jpg',
                'api': {
                    'public': 'https://api.exx.com/data/v1',
                    'private': 'https://trade.exx.com/api',
                },
                'www': 'https://www.exx.com/',
                'doc': 'https://www.exx.com/help/restApi',
                'fees': 'https://www.exx.com/help/rate',
                'referral': 'https://www.exx.com/r/fde4260159e53ab8a58cc9186d35501f?recommQd=1',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'tickers',
                        'ticker',
                        'depth',
                        'trades',
                    ],
                },
                'private': {
                    'get': [
                        'order',
                        'cancel',
                        'getOrder',
                        'getOpenOrders',
                        'getBalance',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.001'),
                    'taker': self.parse_number('0.001'),
                },
                'funding': {
                    'withdraw': {
                        'BCC': 0.0003,
                        'BCD': 0.0,
                        'BOT': 10.0,
                        'BTC': 0.001,
                        'BTG': 0.0,
                        'BTM': 25.0,
                        'BTS': 3.0,
                        'EOS': 1.0,
                        'ETC': 0.01,
                        'ETH': 0.01,
                        'ETP': 0.012,
                        'HPY': 0.0,
                        'HSR': 0.001,
                        'INK': 20.0,
                        'LTC': 0.005,
                        'MCO': 0.6,
                        'MONA': 0.01,
                        'QASH': 5.0,
                        'QCASH': 5.0,
                        'QTUM': 0.01,
                        'USDT': 5.0,
                    },
                },
            },
            'commonCurrencies': {
                'DOS': 'DEMOS',
                'TV': 'TIV',  # Ti-Value
            },
            'exceptions': {
                '103': AuthenticationError,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarkets(params)
        ids = list(response.keys())
        result = []
        for i in range(0, len(ids)):
            id = ids[i]
            market = response[id]
            baseId, quoteId = id.split('_')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            active = market['isOpen'] is True
            amountPrecisionString = self.safe_string(market, 'amountScale')
            pricePrecisionString = self.safe_string(market, 'priceScale')
            amountLimit = self.parse_precision(amountPrecisionString)
            priceLimit = self.parse_precision(pricePrecisionString)
            precision = {
                'amount': int(amountPrecisionString),
                'price': int(pricePrecisionString),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': self.parse_number(amountLimit),
                        'max': None,
                    },
                    'price': {
                        'min': self.parse_number(priceLimit),
                        'max': None,
                    },
                    'cost': {
                        'min': self.safe_number(market, 'minAmount'),
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'date')
        ticker = ticker['ticker']
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_number(ticker, 'riseRate'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTickers(params)
        result = {}
        timestamp = self.milliseconds()
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if not (id in self.markets_by_id):
                continue
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = {
                'date': timestamp,
                'ticker': response[id],
            }
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'currency': self.market_id(symbol),
        }
        response = await self.publicGetDepth(self.extend(request, params))
        timestamp = self.safe_timestamp(response, 'timestamp')
        return self.parse_order_book(response, symbol, timestamp)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        symbol = None
        if market is not None:
            symbol = market['symbol']
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

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetGetBalance(params)
        result = {'info': response}
        balances = self.safe_value(response, 'funds')
        currencies = list(balances.keys())
        for i in range(0, len(currencies)):
            currencyId = currencies[i]
            balance = balances[currencyId]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'balance')
            account['used'] = self.safe_string(balance, 'freeze')
            account['total'] = self.safe_string(balance, 'total')
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "fees": 0,
        #         "total_amount": 1,
        #         "trade_amount": 0,
        #         "price": 30,
        #         "currency": “eth_hsr",
        #         "id": "13878",
        #         "trade_money": 0,
        #         "type": "buy",
        #         "trade_date": 1509728897772,
        #         "status": 0
        #     }
        #
        symbol = market['symbol']
        timestamp = int(order['trade_date'])
        price = self.safe_number(order, 'price')
        cost = self.safe_number(order, 'trade_money')
        amount = self.safe_number(order, 'total_amount')
        filled = self.safe_number(order, 'trade_amount', 0.0)
        status = self.safe_integer(order, 'status')
        if status == 1:
            status = 'canceled'
        elif status == 2:
            status = 'closed'
        else:
            status = 'open'
        fee = None
        if 'fees' in order:
            fee = {
                'cost': self.safe_number(order, 'fees'),
                'currency': market['quote'],
            }
        return self.safe_order({
            'id': self.safe_string(order, 'id'),
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'timeInForce': None,
            'postOnly': None,
            'side': order['type'],
            'price': price,
            'stopPrice': None,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'trades': None,
            'fee': fee,
            'info': order,
            'average': None,
        })

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'type': side,
            'price': price,
            'amount': amount,
        }
        response = await self.privateGetOrder(self.extend(request, params))
        id = self.safe_string(response, 'id')
        order = self.parse_order({
            'id': id,
            'trade_date': self.milliseconds(),
            'total_amount': amount,
            'price': price,
            'type': side,
            'info': response,
        }, market)
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': id,
            'currency': market['id'],
        }
        response = await self.privateGetCancel(self.extend(request, params))
        return response

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': id,
            'currency': market['id'],
        }
        response = await self.privateGetGetOrder(self.extend(request, params))
        return self.parse_order(response, market)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.privateGetGetOpenOrders(self.extend(request, params))
        if not isinstance(response, list):
            return []
        return self.parse_orders(response, market, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            query = self.urlencode(self.keysort(self.extend({
                'accesskey': self.apiKey,
                'nonce': self.nonce(),
            }, params)))
            signed = self.hmac(self.encode(query), self.encode(self.secret), hashlib.sha512)
            url += '?' + query + '&signature=' + signed
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        #
        #  {"result":false,"message":"服务端忙碌"}
        #  ... and other formats
        #
        code = self.safe_string(response, 'code')
        message = self.safe_string(response, 'message')
        feedback = self.id + ' ' + body
        if code == '100':
            return
        if code is not None:
            self.throw_exactly_matched_exception(self.exceptions, code, feedback)
            if code == '308':
                # self is returned by the exchange when there are no open orders
                # {"code":308,"message":"Not Found Transaction Record"}
                return
            else:
                raise ExchangeError(feedback)
        result = self.safe_value(response, 'result')
        if result is not None:
            if not result:
                if message == u'服务端忙碌':
                    raise ExchangeNotAvailable(feedback)
                else:
                    raise ExchangeError(feedback)
