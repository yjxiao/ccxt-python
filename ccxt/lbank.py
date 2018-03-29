# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import DDoSProtection


class lbank (Exchange):

    def describe(self):
        return self.deep_extend(super(lbank, self).describe(), {
            'id': 'lbank',
            'name': 'LBank',
            'countries': 'CN',
            'version': 'v1',
            'has': {
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
            },
            'timeframes': {
                '1m': 'minute1',
                '5m': 'minute5',
                '15m': 'minute15',
                '30m': 'minute30',
                '1h': 'hour1',
                '2h': 'hour2',
                '4h': 'hour4',
                '6h': 'hour6',
                '8h': 'hour8',
                '12h': 'hour12',
                '1d': 'day1',
                '1w': 'week1',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38063602-9605e28a-3302-11e8-81be-64b1e53c4cfb.jpg',
                'api': 'https://api.lbank.info',
                'www': 'https://www.lbank.info',
                'doc': 'https://www.lbank.info/api/api-overview',
                'fees': 'https://lbankinfo.zendesk.com/hc/zh-cn/articles/115002295114--%E8%B4%B9%E7%8E%87%E8%AF%B4%E6%98%8E',
            },
            'api': {
                'public': {
                    'get': [
                        'currencyPairs',
                        'ticker',
                        'depth',
                        'trades',
                        'kline',
                    ],
                },
                'private': {
                    'post': [
                        'user_info',
                        'create_order',
                        'cancel_order',
                        'orders_info',
                        'orders_info_history',
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
                        'BTC': None,
                        'ZEC': 0.01,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        # 'QTUM': amount => max(0.01, amount * (0.1 / 100)),
                        'VEN': 10.0,
                        'BCH': 0.0002,
                        'SC': 50.0,
                        'BTM': 20.0,
                        'NAS': 1.0,
                        'EOS': 1.0,
                        'XWC': 5.0,
                        'BTS': 1.0,
                        'INK': 10.0,
                        'BOT': 3.0,
                        'YOYOW': 15.0,
                        'TGC': 10.0,
                        'NEO': 0.0,
                        'CMT': 20.0,
                        'SEER': 2000.0,
                        'FIL': None,
                        'BTG': None,
                    },
                },
            },
        })

    def fetch_markets(self):
        markets = self.publicGetCurrencyPairs()
        result = []
        for i in range(0, len(markets)):
            id = markets[i]
            baseId, quoteId = id.split('_')
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = '/'.join([base, quote])
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
                        'max': None,
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
                'info': id,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = ticker['timestamp']
        info = ticker
        ticker = info['ticker']
        last = self.safe_float(ticker, 'latest')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'change'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': info,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTicker(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTicker(self.extend({
            'symbol': 'all',
        }, params))
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker['symbol']
            market = self.marketsById[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_order_book(self, symbol, limit=60, params={}):
        self.load_markets()
        response = self.publicGetDepth(self.extend({
            'symbol': self.market_id(symbol),
            'size': min(limit, 60),
        }, params))
        return self.parse_order_book(response)

    def parse_trade(self, trade, market=None):
        symbol = market['symbol']
        timestamp = int(trade['date_ms'])
        price = float(trade['price'])
        amount = float(trade['amount'])
        cost = self.cost_to_precision(symbol, price * amount)
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'tid'),
            'order': None,
            'type': None,
            'side': trade['type'],
            'price': price,
            'amount': amount,
            'cost': float(cost),
            'fee': None,
            'info': self.safe_value(trade, 'info', trade),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'size': 100,
        }
        if since:
            request['time'] = int(since / 1000)
        if limit:
            request['size'] = limit
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': self.timeframes[timeframe],
            'size': 1000,
        }
        if since:
            request['time'] = int(since / 1000)
        if limit:
            request['size'] = limit
        response = self.publicGetKline(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostUserInfo(params)
        result = {'info': response}
        currencies = list(self.extend(response['info']['free'], response['info']['freeze']).keys())
        for i in range(0, len(currencies)):
            id = currencies[i]
            currency = self.common_currency_code(id)
            free = self.safe_float(response['info']['free'], id, 0.0)
            used = self.safe_float(response['info']['freeze'], id, 0.0)
            account = {
                'free': free,
                'used': used,
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        symbol = self.safe_value(self.marketsById, order['symbol'], {'symbol': None})
        timestamp = self.safe_integer(order, 'create_time')
        # Limit Order Request Returns: Order Price
        # Market Order Returns: cny amount of market order
        price = float(order['price'])
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'deal_amount')
        cost = filled * self.safe_float(order, 'avg_price')
        status = self.safe_integer(order, 'status')
        if status == -1 or status == 4:
            status = 'canceled'
        elif status == 2:
            status = 'closed'
        else:
            status = 'open'
        return {
            'id': self.safe_string(order, 'order_id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': self.safe_string(order, 'order_type'),
            'side': order['type'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'trades': None,
            'fee': None,
            'info': self.safe_value(order, 'info', order),
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        order = {
            'symbol': market['id'],
            'type': side,
            'amount': amount,
        }
        if type == 'market':
            order['type'] += '_market'
        else:
            order['price'] = price
        response = self.privatePostCreateOrder(self.extend(order, params))
        order = self.omit(order, 'type')
        order['order_id'] = response['order_id']
        order['type'] = side
        order['order_type'] = type
        order['create_time'] = self.milliseconds()
        order['info'] = response
        order = self.parse_order(order, market)
        id = order['id']
        self.orders[id] = order
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.privatePostCancelOrder(self.extend({
            'symbol': market['id'],
            'order_id': id,
        }, params))
        return response

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.privatePostOrdersInfo(self.extend({
            'symbol': market['id'],
            'order_id': id,
        }, params))
        return self.parse_order(response['orders'][0], market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.privatePostOrdersInfoHistory(self.extend({
            'symbol': market['id'],
            'current_page': 1,
            'page_length': 100,
        }, params))
        return self.parse_orders(response['orders'], None, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        response = self.fetch_orders(self.extend({
            'status': 0,
        }, params))
        return response

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        response = self.fetch_orders(self.extend({
            'status': 1,
        }, params))
        return response

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/' + self.verions + '/' + self.implode_params(path, params)
        # Every endpoint ends with ".do"
        url += '.do'
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.keysort(self.extend({
                'api_key': self.apiKey,
            }, params))
            queryString = self.rawencode(query) + '&secret_key=' + self.secret
            query['sign'] = self.hash(self.encode(queryString)).upper()
            body = self.urlencode(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        success = self.safe_string(response, 'result')
        if success == 'false':
            errorCode = self.safe_string(response, 'error_code')
            message = self.safe_string({
                '10000': 'Internal error',
                '10001': 'The required parameters can not be empty',
                '10002': 'verification failed',
                '10003': 'Illegal parameters',
                '10004': 'User requests are too frequent',
                '10005': 'Key does not exist',
                '10006': 'user does not exist',
                '10007': 'Invalid signature',
                '10008': 'This currency pair is not supported',
                '10009': 'Limit orders can not be missing orders and the number of orders',
                '10010': 'Order price or order quantity must be greater than 0',
                '10011': 'Market orders can not be missing the amount of the order',
                '10012': 'market sell orders can not be missing orders',
                '10013': 'is less than the minimum trading position 0.001',
                '10014': 'Account number is not enough',
                '10015': 'The order type is wrong',
                '10016': 'Account balance is not enough',
                '10017': 'Abnormal server',
                '10018': 'order inquiry can not be more than 50 less than one',
                '10019': 'withdrawal orders can not be more than 3 less than one',
                '10020': 'less than the minimum amount of the transaction limit of 0.001',
            }, errorCode, self.json(response))
            ErrorClass = self.safe_value({
                '10002': AuthenticationError,
                '10004': DDoSProtection,
                '10005': AuthenticationError,
                '10006': AuthenticationError,
                '10007': AuthenticationError,
                '10009': InvalidOrder,
                '10010': InvalidOrder,
                '10011': InvalidOrder,
                '10012': InvalidOrder,
                '10013': InvalidOrder,
                '10014': InvalidOrder,
                '10015': InvalidOrder,
                '10016': InvalidOrder,
            }, errorCode, ExchangeError)
            raise ErrorClass(message)
        return response
