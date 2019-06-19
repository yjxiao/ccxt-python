# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ExchangeError


class lakebtc (Exchange):

    def describe(self):
        return self.deep_extend(super(lakebtc, self).describe(), {
            'id': 'lakebtc',
            'name': 'LakeBTC',
            'countries': ['US'],
            'version': 'api_v2',
            'has': {
                'CORS': True,
                'createMarketOrder': False,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28074120-72b7c38a-6660-11e7-92d9-d9027502281d.jpg',
                'api': 'https://api.lakebtc.com',
                'www': 'https://www.lakebtc.com',
                'doc': [
                    'https://www.lakebtc.com/s/api_v2',
                    'https://www.lakebtc.com/s/api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'bcorderbook',
                        'bctrades',
                        'ticker',
                    ],
                },
                'private': {
                    'post': [
                        'buyOrder',
                        'cancelOrders',
                        'getAccountInfo',
                        'getExternalAccounts',
                        'getOrders',
                        'getTrades',
                        'openOrders',
                        'sellOrder',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.15 / 100,
                    'taker': 0.2 / 100,
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetTicker(params)
        result = []
        keys = list(response.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            market = response[id]
            baseId = id[0:3]
            quoteId = id[3:6]
            base = baseId.upper()
            quote = quoteId.upper()
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetAccountInfo(params)
        balances = self.safe_value(response, 'balance', {})
        result = {'info': response}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = currencyId
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            else:
                code = self.common_currency_code(currencyId)
            balance = self.safe_float(balances, currencyId)
            account = {
                'free': balance,
                'used': 0.0,
                'total': balance,
            }
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        response = await self.publicGetBcorderbook(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTicker(params)
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            symbol = ids[i]
            ticker = response[symbol]
            market = None
            if symbol in self.markets_by_id:
                market = self.markets_by_id[symbol]
                symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        tickers = await self.publicGetTicker(params)
        return self.parse_ticker(tickers[market['id']], market)

    def parse_trade(self, trade, market):
        timestamp = self.safe_integer(trade, 'date') * 1000
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': str(trade['tid']),
            'order': None,
            'type': None,
            'side': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetBctrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        method = 'privatePost' + self.capitalize(side) + 'Order'
        market = self.market(symbol)
        order = {
            'params': [price, amount, market['id']],
        }
        response = await getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'id'),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'params': [id],
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    def nonce(self):
        return self.microseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version
        if api == 'public':
            url += '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            queryParams = ''
            if 'params' in params:
                paramsList = params['params']
                queryParams = ','.join(paramsList)
            query = self.urlencode({
                'tonce': nonce,
                'accesskey': self.apiKey,
                'requestmethod': method.lower(),
                'id': nonce,
                'method': path,
                'params': queryParams,
            })
            body = self.json({
                'method': path,
                'params': queryParams,
                'id': nonce,
            })
            signature = self.hmac(self.encode(query), self.encode(self.secret), hashlib.sha1)
            auth = self.encode(self.apiKey + ':' + signature)
            headers = {
                'Json-Rpc-Tonce': str(nonce),
                'Authorization': 'Basic ' + self.decode(base64.b64encode(auth)),
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'error' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
