# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class _1btcxe (Exchange):

    def describe(self):
        return self.deep_extend(super(_1btcxe, self).describe(), {
            'id': '_1btcxe',
            'name': '1BTCXE',
            'countries': 'PA',  # Panama
            'comment': 'Crypto Capital API',
            'has': {
                'CORS': True,
                'withdraw': True,
            },
            'timeframes': {
                '1d': '1year',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766049-2b294408-5ecc-11e7-85cc-adaff013dc1a.jpg',
                'api': 'https://1btcxe.com/api',
                'www': 'https://1btcxe.com',
                'doc': 'https://1btcxe.com/api-docs.php',
            },
            'api': {
                'public': {
                    'get': [
                        'stats',
                        'historical-prices',
                        'order-book',
                        'transactions',
                    ],
                },
                'private': {
                    'post': [
                        'balances-and-info',
                        'open-orders',
                        'user-transactions',
                        'btc-deposit-address/get',
                        'btc-deposit-address/new',
                        'deposits/get',
                        'withdrawals/get',
                        'orders/new',
                        'orders/edit',
                        'orders/cancel',
                        'orders/status',
                        'withdrawals/new',
                    ],
                },
            },
        })

    def fetch_markets(self):
        return [
            {'id': 'USD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD'},
            {'id': 'EUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR'},
            {'id': 'CNY', 'symbol': 'BTC/CNY', 'base': 'BTC', 'quote': 'CNY'},
            {'id': 'RUB', 'symbol': 'BTC/RUB', 'base': 'BTC', 'quote': 'RUB'},
            {'id': 'CHF', 'symbol': 'BTC/CHF', 'base': 'BTC', 'quote': 'CHF'},
            {'id': 'JPY', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY'},
            {'id': 'GBP', 'symbol': 'BTC/GBP', 'base': 'BTC', 'quote': 'GBP'},
            {'id': 'CAD', 'symbol': 'BTC/CAD', 'base': 'BTC', 'quote': 'CAD'},
            {'id': 'AUD', 'symbol': 'BTC/AUD', 'base': 'BTC', 'quote': 'AUD'},
            {'id': 'AED', 'symbol': 'BTC/AED', 'base': 'BTC', 'quote': 'AED'},
            {'id': 'BGN', 'symbol': 'BTC/BGN', 'base': 'BTC', 'quote': 'BGN'},
            {'id': 'CZK', 'symbol': 'BTC/CZK', 'base': 'BTC', 'quote': 'CZK'},
            {'id': 'DKK', 'symbol': 'BTC/DKK', 'base': 'BTC', 'quote': 'DKK'},
            {'id': 'HKD', 'symbol': 'BTC/HKD', 'base': 'BTC', 'quote': 'HKD'},
            {'id': 'HRK', 'symbol': 'BTC/HRK', 'base': 'BTC', 'quote': 'HRK'},
            {'id': 'HUF', 'symbol': 'BTC/HUF', 'base': 'BTC', 'quote': 'HUF'},
            {'id': 'ILS', 'symbol': 'BTC/ILS', 'base': 'BTC', 'quote': 'ILS'},
            {'id': 'INR', 'symbol': 'BTC/INR', 'base': 'BTC', 'quote': 'INR'},
            {'id': 'MUR', 'symbol': 'BTC/MUR', 'base': 'BTC', 'quote': 'MUR'},
            {'id': 'MXN', 'symbol': 'BTC/MXN', 'base': 'BTC', 'quote': 'MXN'},
            {'id': 'NOK', 'symbol': 'BTC/NOK', 'base': 'BTC', 'quote': 'NOK'},
            {'id': 'NZD', 'symbol': 'BTC/NZD', 'base': 'BTC', 'quote': 'NZD'},
            {'id': 'PLN', 'symbol': 'BTC/PLN', 'base': 'BTC', 'quote': 'PLN'},
            {'id': 'RON', 'symbol': 'BTC/RON', 'base': 'BTC', 'quote': 'RON'},
            {'id': 'SEK', 'symbol': 'BTC/SEK', 'base': 'BTC', 'quote': 'SEK'},
            {'id': 'SGD', 'symbol': 'BTC/SGD', 'base': 'BTC', 'quote': 'SGD'},
            {'id': 'THB', 'symbol': 'BTC/THB', 'base': 'BTC', 'quote': 'THB'},
            {'id': 'TRY', 'symbol': 'BTC/TRY', 'base': 'BTC', 'quote': 'TRY'},
            {'id': 'ZAR', 'symbol': 'BTC/ZAR', 'base': 'BTC', 'quote': 'ZAR'},
        ]

    def fetch_balance(self, params={}):
        response = self.privatePostBalancesAndInfo()
        balance = response['balances-and-info']
        result = {'info': balance}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            account = self.account()
            account['free'] = self.safe_float(balance['available'], currency, 0.0)
            account['used'] = self.safe_float(balance['on_hold'], currency, 0.0)
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        response = self.publicGetOrderBook(self.extend({
            'currency': self.market_id(symbol),
        }, params))
        return self.parse_order_book(response['order-book'], None, 'bid', 'ask', 'price', 'order_amount')

    def fetch_ticker(self, symbol, params={}):
        response = self.publicGetStats(self.extend({
            'currency': self.market_id(symbol),
        }, params))
        ticker = response['stats']
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': float(ticker['max']),
            'low': float(ticker['min']),
            'bid': float(ticker['bid']),
            'ask': float(ticker['ask']),
            'vwap': None,
            'open': float(ticker['open']),
            'close': None,
            'first': None,
            'last': float(ticker['last_price']),
            'change': float(ticker['daily_change']),
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': float(ticker['total_btc_traded']),
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        return [
            self.parse8601(ohlcv['date'] + ' 00:00:00'),
            None,
            None,
            None,
            float(ohlcv['price']),
            None,
        ]

    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetHistoricalPrices(self.extend({
            'currency': market['id'],
            'timeframe': self.timeframes[timeframe],
        }, params))
        ohlcvs = self.omit(response['historical-prices'], 'request_currency')
        return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)

    def parse_trade(self, trade, market):
        timestamp = int(trade['timestamp']) * 1000
        return {
            'id': trade['id'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': None,
            'side': trade['maker_type'],
            'price': float(trade['price']),
            'amount': float(trade['amount']),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetTransactions(self.extend({
            'currency': market['id'],
        }, params))
        trades = self.omit(response['transactions'], 'request_currency')
        return self.parse_trades(trades, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        order = {
            'side': side,
            'type': type,
            'currency': self.market_id(symbol),
            'amount': amount,
        }
        if type == 'limit':
            order['limit_price'] = price
        result = self.privatePostOrdersNew(self.extend(order, params))
        return {
            'info': result,
            'id': result,
        }

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostOrdersCancel({'id': id})

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.load_markets()
        response = self.privatePostWithdrawalsNew(self.extend({
            'currency': currency,
            'amount': float(amount),
            'address': address,
        }, params))
        return {
            'info': response,
            'id': response['result']['uuid'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if self.id == 'cryptocapital':
            raise ExchangeError(self.id + ' is an abstract base API for _1btcxe')
        url = self.urls['api'] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            query = self.extend({
                'api_key': self.apiKey,
                'nonce': self.nonce(),
            }, params)
            request = self.json(query)
            query['signature'] = self.hmac(self.encode(request), self.encode(self.secret))
            body = self.json(query)
            headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'errors' in response:
            errors = []
            for e in range(0, len(response['errors'])):
                error = response['errors'][e]
                errors.append(error['code'] + ': ' + error['message'])
            errors = ' '.join(errors)
            raise ExchangeError(self.id + ' ' + errors)
        return response
