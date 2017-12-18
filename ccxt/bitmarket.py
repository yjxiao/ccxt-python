# -*- coding: utf-8 -*-

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError


class bitmarket (Exchange):

    def describe(self):
        return self.deep_extend(super(bitmarket, self).describe(), {
            'id': 'bitmarket',
            'name': 'BitMarket',
            'countries': ['PL', 'EU'],
            'rateLimit': 1500,
            'hasCORS': False,
            'hasFetchOHLCV': True,
            'hasWithdraw': True,
            'timeframes': {
                '90m': '90m',
                '6h': '6h',
                '1d': '1d',
                '1w': '7d',
                '1M': '1m',
                '3M': '3m',
                '6M': '6m',
                '1y': '1y',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27767256-a8555200-5ef9-11e7-96fd-469a65e2b0bd.jpg',
                'api': {
                    'public': 'https://www.bitmarket.net',
                    'private': 'https://www.bitmarket.pl/api2/',  # last slash is critical
                },
                'www': [
                    'https://www.bitmarket.pl',
                    'https://www.bitmarket.net',
                ],
                'doc': [
                    'https://www.bitmarket.net/docs.php?file=api_public.html',
                    'https://www.bitmarket.net/docs.php?file=api_private.html',
                    'https://github.com/bitmarket-net/api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'json/{market}/ticker',
                        'json/{market}/orderbook',
                        'json/{market}/trades',
                        'json/ctransfer',
                        'graphs/{market}/90m',
                        'graphs/{market}/6h',
                        'graphs/{market}/1d',
                        'graphs/{market}/7d',
                        'graphs/{market}/1m',
                        'graphs/{market}/3m',
                        'graphs/{market}/6m',
                        'graphs/{market}/1y',
                    ],
                },
                'private': {
                    'post': [
                        'info',
                        'trade',
                        'cancel',
                        'orders',
                        'trades',
                        'history',
                        'withdrawals',
                        'tradingdesk',
                        'tradingdeskStatus',
                        'tradingdeskConfirm',
                        'cryptotradingdesk',
                        'cryptotradingdeskStatus',
                        'cryptotradingdeskConfirm',
                        'withdraw',
                        'withdrawFiat',
                        'withdrawPLNPP',
                        'withdrawFiatFast',
                        'deposit',
                        'transfer',
                        'transfers',
                        'marginList',
                        'marginOpen',
                        'marginClose',
                        'marginCancel',
                        'marginModify',
                        'marginBalanceAdd',
                        'marginBalanceRemove',
                        'swapList',
                        'swapOpen',
                        'swapClose',
                    ],
                },
            },
            'markets': {
                'BCH/PLN': {'id': 'BCCPLN', 'symbol': 'BCH/PLN', 'base': 'BCH', 'quote': 'PLN'},
                'BTG/PLN': {'id': 'BTGPLN', 'symbol': 'BTG/PLN', 'base': 'BTG', 'quote': 'PLN'},
                'BTC/PLN': {'id': 'BTCPLN', 'symbol': 'BTC/PLN', 'base': 'BTC', 'quote': 'PLN'},
                'BTC/EUR': {'id': 'BTCEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR'},
                'LTC/PLN': {'id': 'LTCPLN', 'symbol': 'LTC/PLN', 'base': 'LTC', 'quote': 'PLN'},
                'LTC/BTC': {'id': 'LTCBTC', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC'},
                'LiteMineX/BTC': {'id': 'LiteMineXBTC', 'symbol': 'LiteMineX/BTC', 'base': 'LiteMineX', 'quote': 'BTC'},
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.45 / 100,
                    'maker': 0.15 / 100,
                    'tiers': {
                        'taker': [
                            [0, 0.45 / 100],
                            [99.99, 0.44 / 100],
                            [299.99, 0.43 / 100],
                            [499.99, 0.42 / 100],
                            [999.99, 0.41 / 100],
                            [1999.99, 0.40 / 100],
                            [2999.99, 0.39 / 100],
                            [4999.99, 0.38 / 100],
                            [9999.99, 0.37 / 100],
                            [19999.99, 0.36 / 100],
                            [29999.99, 0.35 / 100],
                            [49999.99, 0.34 / 100],
                            [99999.99, 0.33 / 100],
                            [199999.99, 0.32 / 100],
                            [299999.99, 0.31 / 100],
                            [499999.99, 0.0 / 100],
                        ],
                        'maker': [
                            [0, 0.15 / 100],
                            [99.99, 0.14 / 100],
                            [299.99, 0.13 / 100],
                            [499.99, 0.12 / 100],
                            [999.99, 0.11 / 100],
                            [1999.99, 0.10 / 100],
                            [2999.99, 0.9 / 100],
                            [4999.99, 0.8 / 100],
                            [9999.99, 0.7 / 100],
                            [19999.99, 0.6 / 100],
                            [29999.99, 0.5 / 100],
                            [49999.99, 0.4 / 100],
                            [99999.99, 0.3 / 100],
                            [199999.99, 0.2 / 100],
                            [299999.99, 0.1 / 100],
                            [499999.99, 0.0 / 100],
                        ],
                    },
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.0008,
                        'LTC': 0.005,
                        'BCH': 0.0008,
                        'BTG': 0.0008,
                        'DOGE': 1,
                        'EUR': 2,
                        'PLN': 2,
                    },
                    'deposit': {
                        'BTC': 0,
                        'LTC': 0,
                        'BCH': 0,
                        'BTG': 0,
                        'DOGE': 25,
                        'EUR': 2,  # SEPA. Transfer INT(SHA): 5 EUR
                        'PLN': 0,
                    },
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostInfo()
        data = response['data']
        balance = data['balances']
        result = {'info': data}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            account = self.account()
            if currency in balance['available']:
                account['free'] = balance['available'][currency]
            if currency in balance['blocked']:
                account['used'] = balance['blocked'][currency]
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, params={}):
        orderbook = self.publicGetJsonMarketOrderbook(self.extend({
            'market': self.market_id(symbol),
        }, params))
        timestamp = self.milliseconds()
        return {
            'bids': orderbook['bids'],
            'asks': orderbook['asks'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }

    def fetch_ticker(self, symbol, params={}):
        ticker = self.publicGetJsonMarketTicker(self.extend({
            'market': self.market_id(symbol),
        }, params))
        timestamp = self.milliseconds()
        vwap = float(ticker['vwap'])
        baseVolume = float(ticker['volume'])
        quoteVolume = baseVolume * vwap
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']),
            'low': float(ticker['low']),
            'bid': float(ticker['bid']),
            'ask': float(ticker['ask']),
            'vwap': vwap,
            'open': None,
            'close': None,
            'first': None,
            'last': float(ticker['last']),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        side = 'buy' if (trade['type'] == 'bid') else 'sell'
        timestamp = trade['date'] * 1000
        return {
            'id': str(trade['tid']),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': None,
            'side': side,
            'price': trade['price'],
            'amount': trade['amount'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetJsonMarketTrades(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='90m', since=None, limit=None):
        return [
            ohlcv['time'] * 1000,
            float(ohlcv['open']),
            float(ohlcv['high']),
            float(ohlcv['low']),
            float(ohlcv['close']),
            float(ohlcv['vol']),
        ]

    def fetch_ohlcv(self, symbol, timeframe='90m', since=None, limit=None, params={}):
        self.load_markets()
        method = 'publicGetGraphsMarket' + self.timeframes[timeframe]
        market = self.market(symbol)
        response = getattr(self, method)(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        response = self.privatePostTrade(self.extend({
            'market': self.market_id(symbol),
            'type': side,
            'amount': amount,
            'rate': price,
        }, params))
        result = {
            'info': response,
        }
        if 'id' in response['order']:
            result['id'] = response['id']
        return result

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostCancel({'id': id})

    def is_fiat(self, currency):
        if currency == 'EUR':
            return True
        if currency == 'PLN':
            return True
        return False

    def withdraw(self, currency, amount, address, params={}):
        self.load_markets()
        method = None
        request = {
            'currency': currency,
            'quantity': amount,
        }
        if self.is_fiat(currency):
            method = 'privatePostWithdrawFiat'
            if 'account' in params:
                request['account'] = params['account']  # bank account code for withdrawal
            else:
                raise ExchangeError(self.id + ' requires account parameter to withdraw fiat currency')
            if 'account2' in params:
                request['account2'] = params['account2']  # bank SWIFT code(EUR only)
            else:
                if currency == 'EUR':
                    raise ExchangeError(self.id + ' requires account2 parameter to withdraw EUR')
            if 'withdrawal_note' in params:
                request['withdrawal_note'] = params['withdrawal_note']  # a 10-character user-specified withdrawal note(PLN only)
            else:
                if currency == 'PLN':
                    raise ExchangeError(self.id + ' requires withdrawal_note parameter to withdraw PLN')
        else:
            method = 'privatePostWithdraw'
            request['address'] = address
        response = getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.implode_params(path + '.json', params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            query = self.extend({
                'tonce': nonce,
                'method': path,
            }, params)
            body = self.urlencode(query)
            headers = {
                'API-Key': self.apiKey,
                'API-Hash': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
