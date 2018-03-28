# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
import hashlib
import json
from ccxt.base.errors import ExchangeError


class coinone (Exchange):

    def describe(self):
        return self.deep_extend(super(coinone, self).describe(), {
            'id': 'coinone',
            'name': 'CoinOne',
            'countries': 'KR',  # Korea
            'rateLimit': 90,
            'version': 'v2',
            'has': {
                'CORS': False,
                'createMarketOrder': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38003300-adc12fba-323f-11e8-8525-725f53c4a659.jpg',
                'api': 'https://api.coinone.co.kr',
                'www': 'https://coinone.co.kr',
                'doc': 'https://doc.coinone.co.kr',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'orderbook/',
                        'trades/',
                        'ticker/',
                    ],
                },
                'private': {
                    'post': [
                        'account/btc_deposit_address/',
                        'account/balance/',
                        'account/daily_balance/',
                        'account/user_info/',
                        'account/virtual_account/',
                        'order/cancel_all/',
                        'order/cancel/',
                        'order/limit_buy/',
                        'order/limit_sell/',
                        'order/complete_orders/',
                        'order/limit_orders/',
                        'order/order_info/',
                        'transaction/auth_number/',
                        'transaction/history/',
                        'transaction/krw/history/',
                        'transaction/btc/',
                        'transaction/coin/',
                    ],
                },
            },
            'markets': {
                'BCH/KRW': {'id': 'bch', 'symbol': 'BCH/KRW', 'base': 'BCH', 'quote': 'KRW'},
                'BTC/KRW': {'id': 'btc', 'symbol': 'BTC/KRW', 'base': 'BTC', 'quote': 'KRW'},
                'BTG/KRW': {'id': 'btg', 'symbol': 'BTG/KRW', 'base': 'BTG', 'quote': 'KRW'},
                'ETC/KRW': {'id': 'etc', 'symbol': 'ETC/KRW', 'base': 'ETC', 'quote': 'KRW'},
                'ETH/KRW': {'id': 'eth', 'symbol': 'ETH/KRW', 'base': 'ETH', 'quote': 'KRW'},
                'IOT/KRW': {'id': 'iota', 'symbol': 'IOT/KRW', 'base': 'IOT', 'quote': 'KRW'},
                'LTC/KRW': {'id': 'ltc', 'symbol': 'LTC/KRW', 'base': 'LTC', 'quote': 'KRW'},
                'QTUM/KRW': {'id': 'qtum', 'symbol': 'QTUM/KRW', 'base': 'QTUM', 'quote': 'KRW'},
                'XRP/KRW': {'id': 'xrp', 'symbol': 'XRP/KRW', 'base': 'XRP', 'quote': 'KRW'},
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                    'tiers': {
                        'taker': [
                            [0, 0.001],
                            [100000000, 0.0009],
                            [1000000000, 0.0008],
                            [5000000000, 0.0007],
                            [10000000000, 0.0006],
                            [20000000000, 0.0005],
                            [30000000000, 0.0004],
                            [40000000000, 0.0003],
                            [50000000000, 0.0002],
                        ],
                        'maker': [
                            [0, 0.001],
                            [100000000, 0.0008],
                            [1000000000, 0.0006],
                            [5000000000, 0.0004],
                            [10000000000, 0.0002],
                            [20000000000, 0],
                            [30000000000, 0],
                            [40000000000, 0],
                            [50000000000, 0],
                        ],
                    },
                },
            },
        })

    def fetch_balance(self, params={}):
        response = self.privateGetV2AccountBalance()
        result = {'info': response}
        ids = list(self.markets.keys())
        for i in range(0, len(ids)):
            market = ids[i]
            id = market['id']
            symbol = market['symbol']
            if id in response:
                balance = response[id]
                account = {
                    'free': float(balance['avail']),
                    'used': float(balance['balance']) - float(balance['avail']),
                    'total': float(balance['balance']),
                }
                result[symbol] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, params={}):
        market = self.market(symbol)
        response = self.publicGetOrderbook(self.extend({
            'currency': market['id'],
            'format': 'json',
        }, params))
        return self.parse_order_book(response, None, 'bid', 'ask', 'price', 'qty')

    def fetch_ticker(self, symbol, params={}):
        market = self.market(symbol)
        response = self.publicGetTicker(self.extend({
            'currency': market['id'],
            'format': 'json',
        }, params))
        return self.parse_ticker(response, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'last')
        previousClose = self.safe_float(ticker, 'yesterday_last')
        change = None
        if last is not None and previousClose is not None:
            change = previousClose - last
        symbol = market['symbol'] if (market is not None) else None
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
            'open': self.safe_float(ticker, 'first'),
            'close': last,
            'last': last,
            'previousClose': previousClose,
            'change': change,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = int(trade['timestamp']) * 1000
        symbol = market['symbol'] if (market is not None) else None
        return {
            'id': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'symbol': symbol,
            'type': None,
            'side': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'qty'),
            'fee': None,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetTrades(self.extend({
            'currency': market['id'],
            'period': 'hour',
            'format': 'json',
        }, params))
        return self.parse_trades(response['completeOrders'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        order = {
            'price': price,
            'currency': self.market_id(symbol),
            'qty': amount,
        }
        method = 'privatePostOrder' + self.capitalize(type) + self.capitalize(side)
        response = getattr(self, method)(self.extend(order, params))
        # todo: return the full order structure
        # return self.parse_order(response, market)
        orderId = self.safe_string(response, 'orderId')
        return {
            'info': response,
            'id': orderId,
        }

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostOrderCancel({'orderID': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/' + request
        headers = {}
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            payload = base64.b64encode(self.json({'access_token': self.apiKey, 'nonce': nonce}))
            body = payload
            signature = self.hmac(payload, self.encode(self.secret.upper()), hashlib.sha512, 'hex')
            headers = {
                'content-type': 'application/json',
                'X-COINONE-PAYLOAD': payload,
                'X-COINONE-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            if 'result' in response:
                result = response['result']
                if result != 'success':
                    raise ExchangeError(self.id + ' ' + body)
            else:
                raise ExchangeError(self.id + ' ' + body)
