# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported


class _1broker (Exchange):

    def describe(self):
        return self.deep_extend(super(_1broker, self).describe(), {
            'id': '_1broker',
            'name': '1Broker',
            'countries': ['US'],
            'rateLimit': 1500,
            'version': 'v2',
            'has': {
                'publicAPI': False,
                'CORS': True,
                'fetchTrades': False,
                'fetchOHLCV': True,
            },
            'timeframes': {
                '1m': '60',  # not working for some reason, returns {"server_time":"2018-03-26T03:52:27.912Z","error":true,"warning":false,"response":null,"error_code":-1,"error_message":"Error while trying to fetch historical market data. An invalid resolution was probably used."}
                '15m': '900',
                '1h': '3600',
                '1d': '86400',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766021-420bd9fc-5ecb-11e7-8ed6-56d0081efed2.jpg',
                'api': 'https://1broker.com/api',
                'www': 'https://1broker.com',
                'doc': 'https://1broker.com/?c=en/content/api-documentation',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'api': {
                'private': {
                    'get': [
                        'market/bars',
                        'market/categories',
                        'market/details',
                        'market/list',
                        'market/quotes',
                        'market/ticks',
                        'order/cancel',
                        'order/create',
                        'order/open',
                        'position/close',
                        'position/close_cancel',
                        'position/edit',
                        'position/history',
                        'position/open',
                        'position/shared/get',
                        'social/profile_statistics',
                        'social/profile_trades',
                        'user/bitcoin_deposit_address',
                        'user/details',
                        'user/overview',
                        'user/quota_status',
                        'user/transaction_log',
                    ],
                },
            },
        })

    async def fetch_categories(self):
        response = await self.privateGetMarketCategories()
        # they return an empty string among their categories, wtf?
        categories = response['response']
        result = []
        for i in range(0, len(categories)):
            if categories[i]:
                result.append(categories[i])
        return result

    async def fetch_markets(self):
        self_ = self  # workaround for Babel bug(not passing `self` to _recursive() call)
        categories = await self.fetch_categories()
        result = []
        for c in range(0, len(categories)):
            category = categories[c]
            markets = await self_.privateGetMarketList({
                'category': category.lower(),
            })
            for p in range(0, len(markets['response'])):
                market = markets['response'][p]
                id = market['symbol']
                symbol = None
                base = None
                quote = None
                if (category == 'FOREX') or (category == 'CRYPTO'):
                    symbol = market['name']
                    parts = symbol.split('/')
                    base = parts[0]
                    quote = parts[1]
                else:
                    base = id
                    quote = 'USD'
                    symbol = base + '/' + quote
                base = self_.common_currency_code(base)
                quote = self_.common_currency_code(quote)
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'info': market,
                })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balance = await self.privateGetUserOverview()
        response = balance['response']
        result = {
            'info': response,
        }
        currencies = list(self.currencies.keys())
        for c in range(0, len(currencies)):
            currency = currencies[c]
            result[currency] = self.account()
        total = self.safe_float(response, 'balance')
        result['BTC']['free'] = total
        result['BTC']['total'] = total
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        response = await self.privateGetMarketQuotes(self.extend({
            'symbols': self.market_id(symbol),
        }, params))
        orderbook = response['response'][0]
        timestamp = self.parse8601(orderbook['updated'])
        bidPrice = self.safe_float(orderbook, 'bid')
        askPrice = self.safe_float(orderbook, 'ask')
        bid = [bidPrice, None]
        ask = [askPrice, None]
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'bids': [bid],
            'asks': [ask],
            'nonce': None,
        }

    async def fetch_trades(self, symbol):
        raise NotSupported(self.id + ' fetchTrades() method not implemented yet')

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        result = await self.privateGetMarketBars(self.extend({
            'symbol': self.market_id(symbol),
            'resolution': 60,
            'limit': 1,
        }, params))
        ticker = result['response'][0]
        timestamp = self.parse8601(ticker['date'])
        open = self.safe_float(ticker, 'o')
        close = self.safe_float(ticker, 'c')
        change = close - open
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'h'),
            'low': self.safe_float(ticker, 'l'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': change / open * 100,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.parse8601(ohlcv['date']),
            float(ohlcv['o']),
            float(ohlcv['h']),
            float(ohlcv['l']),
            float(ohlcv['c']),
            None,
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'resolution': self.timeframes[timeframe],
        }
        if since is not None:
            request['date_start'] = self.iso8601(since)  # they also support date_end
        if limit is not None:
            request['limit'] = limit
        result = await self.privateGetMarketBars(self.extend(request, params))
        return self.parse_ohlcvs(result['response'], market, timeframe, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        order = {
            'symbol': self.market_id(symbol),
            'margin': amount,
            'direction': 'short' if (side == 'sell') else 'long',
            'leverage': 1,
            'type': side,
        }
        if type == 'limit':
            order['price'] = price
        else:
            order['type'] += '_market'
        result = await self.privateGetOrderCreate(self.extend(order, params))
        return {
            'info': result,
            'id': result['response']['order_id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostOrderCancel({'order_id': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        self.check_required_credentials()
        url = self.urls['api'] + '/' + self.version + '/' + path + '.php'
        query = self.extend({'token': self.apiKey}, params)
        url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'warning' in response:
            if response['warning']:
                raise ExchangeError(self.id + ' ' + self.json(response))
        if 'error' in response:
            if response['error']:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
