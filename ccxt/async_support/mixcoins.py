# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError


class mixcoins (Exchange):

    def describe(self):
        return self.deep_extend(super(mixcoins, self).describe(), {
            'id': 'mixcoins',
            'name': 'MixCoins',
            'countries': ['GB', 'HK'],
            'rateLimit': 1500,
            'version': 'v1',
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30237212-ed29303c-9535-11e7-8af8-fcd381cfa20c.jpg',
                'api': 'https://mixcoins.com/api',
                'www': 'https://mixcoins.com',
                'doc': 'https://mixcoins.com/help/api/',
            },
            'api': {
                'public': {
                    'get': [
                        'ticker/',
                        'trades/',
                        'depth/',
                    ],
                },
                'private': {
                    'post': [
                        'cancel',
                        'info',
                        'orders',
                        'order',
                        'transactions',
                        'trade',
                    ],
                },
            },
            'markets': {
                'BTC/USD': {'id': 'btc_usd', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'btc', 'quoteId': 'usd', 'maker': 0.0015, 'taker': 0.0025},
                'ETH/BTC': {'id': 'eth_btc', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'eth', 'quoteId': 'btc', 'maker': 0.001, 'taker': 0.0015},
                'BCH/BTC': {'id': 'bch_btc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bch', 'quoteId': 'btc', 'maker': 0.001, 'taker': 0.0015},
                'LSK/BTC': {'id': 'lsk_btc', 'symbol': 'LSK/BTC', 'base': 'LSK', 'quote': 'BTC', 'baseId': 'lsk', 'quoteId': 'btc', 'maker': 0.0015, 'taker': 0.0025},
                'BCH/USD': {'id': 'bch_usd', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD', 'baseId': 'bch', 'quoteId': 'usd', 'maker': 0.001, 'taker': 0.0015},
                'ETH/USD': {'id': 'eth_usd', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD', 'baseId': 'eth', 'quoteId': 'usd', 'maker': 0.001, 'taker': 0.0015},
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostInfo(params)
        balances = self.safe_value(response['result'], 'wallet')
        result = {'info': response}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = currencyId
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            else:
                code = self.common_currency_code(currencyId.upper())
            balance = self.safe_value(balances, currencyId, {})
            account = self.account()
            account['free'] = self.safe_float(balance, 'avail')
            account['used'] = self.safe_float(balance, 'lock')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
        }
        response = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response['result'])

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
        }
        response = await self.publicGetTicker(self.extend(request, params))
        ticker = self.safe_value(response, 'result')
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'last')
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
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is not None:
            timestamp *= 1000
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'id')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'order': None,
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
            'market': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response['result'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'op': side,
            'amount': amount,
        }
        if type == 'market':
            request['order_type'] = 1
            request['price'] = price
        else:
            request['order_type'] = 0
        response = await self.privatePostTrade(self.extend(request, params))
        return {
            'info': response,
            'id': str(response['result']['id']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        return await self.privatePostCancel(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'nonce': nonce,
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.secret, hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'status' in response:
            #
            # todo add a unified standard handleErrors with self.exceptions in describe()
            #
            #     {"status":503,"message":"Maintenancing, try again later","result":null}
            #
            if response['status'] == 200:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))
