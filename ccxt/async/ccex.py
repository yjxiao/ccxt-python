# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError


class ccex (Exchange):

    def describe(self):
        return self.deep_extend(super(ccex, self).describe(), {
            'id': 'ccex',
            'name': 'C-CEX',
            'countries': ['DE', 'EU'],
            'rateLimit': 1500,
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOrderBooks': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766433-16881f90-5ed8-11e7-92f8-3d92cc747a6c.jpg',
                'api': {
                    'web': 'https://c-cex.com/t',
                    'public': 'https://c-cex.com/t/api_pub.html',
                    'private': 'https://c-cex.com/t/api.html',
                },
                'www': 'https://c-cex.com',
                'doc': 'https://c-cex.com/?id=api',
            },
            'api': {
                'web': {
                    'get': [
                        'coinnames',
                        '{market}',
                        'pairs',
                        'prices',
                        'volume_{coin}',
                    ],
                },
                'public': {
                    'get': [
                        'balancedistribution',
                        'markethistory',
                        'markets',
                        'marketsummaries',
                        'orderbook',
                        'fullorderbook',
                    ],
                },
                'private': {
                    'get': [
                        'buylimit',
                        'cancel',
                        'getbalance',
                        'getbalances',
                        'getopenorders',
                        'getorder',
                        'getorderhistory',
                        'mytrades',
                        'selllimit',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'taker': 0.2 / 100,
                    'maker': 0.2 / 100,
                },
            },
            'commonCurrencies': {
                'IOT': 'IoTcoin',
                'BLC': 'Cryptobullcoin',
                'XID': 'InternationalDiamond',
                'LUX': 'Luxmi',
                'CRC': 'CoreCoin',
            },
        })

    async def fetch_markets(self):
        result = {}
        response = await self.webGetPairs()
        markets = response['pairs']
        for i in range(0, len(markets)):
            id = markets[i]
            baseId, quoteId = id.split('-')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            result[symbol] = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': id,
            }
        # an alternative documented parser
        #     markets = await self.publicGetMarkets()
        #     for p in range(0, len(markets['result'])):
        #         market = markets['result'][p]
        #         id = market['MarketName']
        #         base = market['MarketCurrency']
        #         quote = market['BaseCurrency']
        #         base = self.common_currency_code(base)
        #         quote = self.common_currency_code(quote)
        #         symbol = base + '/' + quote
        #         result.append({
        #             'id': id,
        #             'symbol': symbol,
        #             'base': base,
        #             'quote': quote,
        #             'info': market,
        #         })
        #     }
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetGetbalances()
        balances = response['result']
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            code = balance['Currency']
            currency = self.common_currency_code(code)
            account = {
                'free': balance['Available'],
                'used': balance['Pending'],
                'total': balance['Balance'],
            }
            result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'type': 'both',
        }
        if limit is not None:
            request['depth'] = limit  # 100
        response = await self.publicGetOrderbook(self.extend(request, params))
        orderbook = response['result']
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'Rate', 'Quantity')

    async def fetch_order_books(self, symbols=None, params={}):
        await self.load_markets()
        orderbooks = {}
        response = await self.publicGetFullorderbook()
        types = list(response['result'].keys())
        for i in range(0, len(types)):
            type = types[i]
            bidasks = response['result'][type]
            bidasksByMarketId = self.group_by(bidasks, 'Market')
            marketIds = list(bidasksByMarketId.keys())
            for j in range(0, len(marketIds)):
                marketId = marketIds[j]
                symbol = marketId.upper()
                side = type
                if symbol in self.markets_by_id:
                    market = self.markets_by_id[symbol]
                    symbol = market['symbol']
                else:
                    base, quote = symbol.split('-')
                    invertedId = quote + '-' + base
                    if invertedId in self.markets_by_id:
                        market = self.markets_by_id[invertedId]
                        symbol = market['symbol']
                if not(symbol in list(orderbooks.keys())):
                    orderbooks[symbol] = {}
                orderbooks[symbol][side] = bidasksByMarketId[marketId]
        result = {}
        keys = list(orderbooks.keys())
        for k in range(0, len(keys)):
            key = keys[k]
            result[key] = self.parse_order_book(orderbooks[key], None, 'buy', 'sell', 'Rate', 'Quantity')
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['updated'] * 1000
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = float(ticker['lastprice'])
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']),
            'low': float(ticker['low']),
            'bid': float(ticker['buy']),
            'bidVolume': None,
            'ask': float(ticker['sell']),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': float(ticker['avg']),
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'buysupport'),
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.webGetPrices(params)
        result = {'info': tickers}
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            ticker = tickers[id]
            market = None
            symbol = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                uppercase = id.upper()
                base, quote = uppercase.split('-')
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                symbol = base + '/' + quote
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.webGetMarket(self.extend({
            'market': market['id'].lower(),
        }, params))
        ticker = response['ticker']
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = self.parse8601(trade['TimeStamp'])
        return {
            'id': str(trade['Id']),
            'info': trade,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['OrderType'].lower(),
            'price': trade['Price'],
            'amount': trade['Quantity'],
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetMarkethistory(self.extend({
            'market': market['id'],
            'type': 'both',
            'depth': 100,
        }, params))
        return self.parse_trades(response['result'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        method = 'privateGet' + self.capitalize(side) + type
        response = await getattr(self, method)(self.extend({
            'market': self.market_id(symbol),
            'quantity': amount,
            'rate': price,
        }, params))
        return {
            'info': response,
            'id': response['result']['uuid'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privateGetCancel({'uuid': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            query = self.keysort(self.extend({
                'a': path,
                'apikey': self.apiKey,
                'nonce': nonce,
            }, params))
            url += '?' + self.urlencode(query)
            headers = {'apisign': self.hmac(self.encode(url), self.encode(self.secret), hashlib.sha512)}
        elif api == 'public':
            url += '?' + self.urlencode(self.extend({
                'a': 'get' + path,
            }, params))
        else:
            url += '/' + self.implode_params(path, params) + '.json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if api == 'web':
            return response
        if 'success' in response:
            if response['success']:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))
