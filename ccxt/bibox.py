# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class bibox (Exchange):

    def describe(self):
        return self.deep_extend(super(bibox, self).describe(), {
            'id': 'bibox',
            'name': 'Bibox',
            'countries': ['CN', 'US', 'KR'],
            'version': 'v1',
            'has': {
                'CORS': False,
                'publicAPI': False,
                'fetchBalance': True,
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchFundingFees': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'createMarketOrder': False,  # or they will return https://github.com/ccxt/ccxt/issues/2338
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '12h': '12hour',
                '1d': 'day',
                '1w': 'week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/34902611-2be8bf1a-f830-11e7-91a2-11b2f292e750.jpg',
                'api': 'https://api.bibox.com',
                'www': 'https://www.bibox.com',
                'doc': [
                    'https://github.com/Biboxcom/api_reference/wiki/home_en',
                    'https://github.com/Biboxcom/api_reference/wiki/api_reference',
                ],
                'fees': 'https://bibox.zendesk.com/hc/en-us/articles/115004417013-Fee-Structure-on-Bibox',
            },
            'api': {
                'public': {
                    'post': [
                        # TODO: rework for full endpoint/cmd paths here
                        'mdata',
                    ],
                    'get': [
                        'mdata',
                    ],
                },
                'private': {
                    'post': [
                        'user',
                        'orderpending',
                        'transfer',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.0,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {},
                    'deposit': {},
                },
            },
            'exceptions': {
                '2021': InsufficientFunds,  # Insufficient balance available for withdrawal
                '2015': AuthenticationError,  # Google authenticator is wrong
                '2027': InsufficientFunds,  # Insufficient balance available(for trade)
                '2033': OrderNotFound,  # operation failednot  Orders have been completed or revoked
                '2067': InvalidOrder,  # Does not support market orders
                '2068': InvalidOrder,  # The number of orders can not be less than
                '3012': AuthenticationError,  # invalid apiKey
                '3024': PermissionDenied,  # wrong apikey permissions
                '3025': AuthenticationError,  # signature failed
                '4000': ExchangeNotAvailable,  # current network is unstable
                '4003': DDoSProtection,  # server busy please try again later
            },
            'commonCurrencies': {
                'KEY': 'Bihu',
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetMdata(self.extend({
            'cmd': 'marketAll',
        }, params))
        markets = response['result']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId = market['coin_symbol']
            quoteId = market['currency_symbol']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            id = base + '_' + quote
            precision = {
                'amount': 4,
                'price': 8,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': base,
                'quoteId': quote,
                'active': True,
                'info': market,
                'lot': math.pow(10, -precision['amount']),
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    def parse_ticker(self, ticker, market=None):
        # we don't set values that are not defined by the exchange
        timestamp = self.safe_integer(ticker, 'timestamp')
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            base = ticker['coin_symbol']
            quote = ticker['currency_symbol']
            symbol = self.common_currency_code(base) + '/' + self.common_currency_code(quote)
        last = self.safe_float(ticker, 'last')
        change = self.safe_float(ticker, 'change')
        baseVolume = None
        if 'vol' in ticker:
            baseVolume = self.safe_float(ticker, 'vol')
        else:
            baseVolume = self.safe_float(ticker, 'vol24H')
        open = None
        if (last is not None) and(change is not None):
            open = last - change
        iso8601 = None
        if timestamp is not None:
            iso8601 = self.iso8601(timestamp)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': iso8601,
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
            'percentage': self.safe_string(ticker, 'percent'),
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': self.safe_float(ticker, 'amount'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMdata(self.extend({
            'cmd': 'ticker',
            'pair': market['id'],
        }, params))
        return self.parse_ticker(response['result'], market)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            tickers.append(self.parse_ticker(rawTickers[i]))
        return self.filter_by_array(tickers, 'symbol', symbols)

    def fetch_tickers(self, symbols=None, params={}):
        response = self.publicGetMdata(self.extend({
            'cmd': 'marketAll',
        }, params))
        return self.parse_tickers(response['result'], symbols)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'time')
        timestamp = self.safe_integer(trade, 'createdAt', timestamp)
        side = self.safe_integer(trade, 'side')
        side = self.safe_integer(trade, 'order_side', side)
        side = 'buy' if (side == 1) else 'sell'
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'pair')
            if marketId is None:
                baseId = self.safe_string(trade, 'coin_symbol')
                quoteId = self.safe_string(trade, 'currency_symbol')
                if (baseId is not None) and(quoteId is not None):
                    marketId = baseId + '_' + quoteId
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        feeCurrency = self.safe_string(trade, 'fee_symbol')
        if feeCurrency is not None:
            if feeCurrency in self.currencies_by_id:
                feeCurrency = self.currencies_by_id[feeCurrency]['code']
            else:
                feeCurrency = self.common_currency_code(feeCurrency)
        feeRate = None  # todo: deduce from market if market is defined
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = price * amount
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
                'rate': feeRate,
            }
        return {
            'info': trade,
            'id': self.safe_string(trade, 'id'),
            'order': None,  # Bibox does not have it(documented) yet
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        size = limit if (limit) else 200
        response = self.publicGetMdata(self.extend({
            'cmd': 'deals',
            'pair': market['id'],
            'size': size,
        }, params))
        return self.parse_trades(response['result'], market, since, limit)

    def fetch_order_book(self, symbol, limit=200, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'cmd': 'depth',
            'pair': market['id'],
        }
        request['size'] = limit  # default = 200 ?
        response = self.publicGetMdata(self.extend(request, params))
        return self.parse_order_book(response['result'], self.safe_float(response['result'], 'update_time'), 'bids', 'asks', 'price', 'volume')

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['time'],
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['vol'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMdata(self.extend({
            'cmd': 'kline',
            'pair': market['id'],
            'period': self.timeframes[timeframe],
            'size': limit,
        }, params))
        return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    def fetch_currencies(self, params={}):
        response = self.privatePostTransfer({
            'cmd': 'transfer/coinList',
            'body': {},
        })
        currencies = response['result']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['symbol']
            code = self.common_currency_code(id)
            precision = 8
            deposit = currency['enable_deposit']
            withdraw = currency['enable_withdraw']
            active = True if (deposit and withdraw) else False
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': currency['name'],
                'active': active,
                'fee': None,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': math.pow(10, precision),
                    },
                },
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostTransfer({
            'cmd': 'transfer/assets',
            'body': self.extend({
                'select': 1,
            }, params),
        })
        balances = response['result']
        result = {'info': balances}
        indexed = None
        if 'assets_list' in balances:
            indexed = self.index_by(balances['assets_list'], 'coin_symbol')
        else:
            indexed = balances
        keys = list(indexed.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            code = id.upper()
            if code.find('TOTAL_') >= 0:
                code = code[6:]
            if code in self.currencies_by_id:
                code = self.currencies_by_id[code]['code']
            account = self.account()
            balance = indexed[id]
            if isinstance(balance, basestring):
                balance = float(balance)
                account['free'] = balance
                account['used'] = 0.0
                account['total'] = balance
            else:
                account['free'] = float(balance['balance'])
                account['used'] = float(balance['freeze'])
                account['total'] = self.sum(account['free'], account['used'])
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        orderType = 2 if (type == 'limit') else 1
        orderSide = 1 if (side == 'buy') else 2
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/trade',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,
                'order_type': orderType,
                'order_side': orderSide,
                'pay_bix': 0,
                'amount': amount,
                'price': price,
            }, params),
        })
        return {
            'info': response,
            'id': self.safe_string(response, 'result'),
        }

    def cancel_order(self, id, symbol=None, params={}):
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/cancelTrade',
            'body': self.extend({
                'orders_id': id,
            }, params),
        })
        return response

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/order',
            'body': self.extend({
                'id': id,
            }, params),
        })
        order = self.safe_value(response, 'result')
        if self.is_empty(order):
            raise OrderNotFound(self.id + ' order ' + id + ' not found')
        return self.parse_order(order)

    def parse_order(self, order, market=None):
        symbol = None
        if market is None:
            marketId = None
            baseId = self.safe_string(order, 'coin_symbol')
            quoteId = self.safe_string(order, 'currency_symbol')
            if (baseId is not None) and(quoteId is not None):
                marketId = baseId + '_' + quoteId
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        type = 'market' if (order['order_type'] == 1) else 'limit'
        timestamp = order['createdAt']
        price = self.safe_float(order, 'price')
        price = self.safe_float(order, 'deal_price', price)
        filled = self.safe_float(order, 'deal_amount')
        amount = self.safe_float(order, 'amount')
        cost = self.safe_float(order, 'money')
        cost = self.safe_float(order, 'deal_money', cost)
        remaining = None
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
            if cost is None:
                cost = price * filled
        side = 'buy' if (order['order_side'] == 1) else 'sell'
        status = self.safe_string(order, 'status')
        if status is not None:
            status = self.parse_order_status(status)
        result = {
            'info': order,
            'id': self.safe_string(order, 'id'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost if cost else float(price) * filled,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': self.safe_float(order, 'fee'),
        }
        return result

    def parse_order_status(self, status):
        statuses = {
            # original comments from bibox:
            '1': 'open',  # pending
            '2': 'open',  # part completed
            '3': 'closed',  # completed
            '4': 'canceled',  # part canceled
            '5': 'canceled',  # canceled
            '6': 'canceled',  # canceling
        }
        return self.safe_string(statuses, status, status.lower())

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        market = None
        pair = None
        if symbol is not None:
            self.load_markets()
            market = self.market(symbol)
            pair = market['id']
        size = limit if (limit) else 200
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/orderPendingList',
            'body': self.extend({
                'pair': pair,
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': size,
            }, params),
        })
        orders = self.safe_value(response['result'], 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=200, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchClosedOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/pendingHistoryList',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': limit,
            }, params),
        })
        orders = self.safe_value(response['result'], 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        size = limit if (limit) else 200
        response = self.privatePostOrderpending({
            'cmd': 'orderpending/orderHistoryList',
            'body': self.extend({
                'pair': market['id'],
                'account_type': 0,  # 0 - regular, 1 - margin
                'page': 1,
                'size': size,
            }, params),
        })
        trades = self.safe_value(response['result'], 'items', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privatePostTransfer({
            'cmd': 'transfer/transferIn',
            'body': self.extend({
                'coin_symbol': currency['id'],
            }, params),
        })
        address = self.safe_string(response, 'result')
        result = {
            'info': response,
            'address': address,
        }
        return result

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        if self.password is None:
            if not('trade_pwd' in list(params.keys())):
                raise ExchangeError(self.id + ' withdraw() requires self.password set on the exchange instance or a trade_pwd parameter')
        if not('totp_code' in list(params.keys())):
            raise ExchangeError(self.id + ' withdraw() requires a totp_code parameter for 2FA authentication')
        body = {
            'trade_pwd': self.password,
            'coin_symbol': currency['id'],
            'amount': amount,
            'addr': address,
        }
        if tag is not None:
            body['address_remark'] = tag
        response = self.privatePostTransfer({
            'cmd': 'transfer/transferOut',
            'body': self.extend(body, params),
        })
        return {
            'info': response,
            'id': None,
        }

    def fetch_funding_fees(self, codes=None, params={}):
        #  by default it will try load withdrawal fees of all currencies(with separate requests)
        #  however if you define codes = ['ETH', 'BTC'] in args it will only load those
        self.load_markets()
        withdrawFees = {}
        info = {}
        if codes is None:
            codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            response = self.privatePostTransfer({
                'cmd': 'transfer/transferOutInfo',
                'body': self.extend({
                    'coin_symbol': currency['id'],
                }, params),
            })
            info[code] = response
            withdrawFees[code] = response['result']['withdraw_fee']
        return {
            'info': info,
            'withdraw': withdrawFees,
            'deposit': {},
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        cmds = self.json([params])
        if api == 'public':
            if method != 'GET':
                body = {'cmds': cmds}
            elif params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            body = {
                'cmds': cmds,
                'apikey': self.apiKey,
                'sign': self.hmac(self.encode(cmds), self.encode(self.secret), hashlib.md5),
            }
        if body is not None:
            body = self.json(body, {'convertArraysToObjects': True})
        headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if len(body) > 0:
            if body[0] == '{':
                response = json.loads(body)
                if 'error' in response:
                    if 'code' in response['error']:
                        code = self.safe_string(response['error'], 'code')
                        feedback = self.id + ' ' + body
                        exceptions = self.exceptions
                        if code in exceptions:
                            raise exceptions[code](feedback)
                        else:
                            raise ExchangeError(feedback)
                    raise ExchangeError(self.id + ': "error" in response: ' + body)
                if not('result' in list(response.keys())):
                    raise ExchangeError(self.id + ' ' + body)

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if method == 'GET':
            return response
        else:
            return response['result'][0]
