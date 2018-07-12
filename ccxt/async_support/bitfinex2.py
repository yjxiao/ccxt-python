# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.bitfinex import bitfinex
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import NotSupported


class bitfinex2 (bitfinex):

    def describe(self):
        return self.deep_extend(super(bitfinex2, self).describe(), {
            'id': 'bitfinex2',
            'name': 'Bitfinex v2',
            'countries': ['VG'],
            'version': 'v2',
            # new metainfo interface
            'has': {
                'CORS': True,
                'createLimitOrder': False,
                'createMarketOrder': False,
                'createOrder': False,
                'deposit': False,
                'editOrder': False,
                'fetchDepositAddress': False,
                'fetchClosedOrders': False,
                'fetchFundingFees': False,
                'fetchMyTrades': False,
                'fetchOHLCV': True,
                'fetchOpenOrders': False,
                'fetchOrder': True,
                'fetchTickers': True,
                'fetchTradingFees': False,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '3h': '3h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1D',
                '1w': '7D',
                '2w': '14D',
                '1M': '1M',
            },
            'rateLimit': 1500,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766244-e328a50c-5ed2-11e7-947b-041416579bb3.jpg',
                'api': 'https://api.bitfinex.com',
                'www': 'https://www.bitfinex.com',
                'doc': [
                    'https://bitfinex.readme.io/v2/docs',
                    'https://github.com/bitfinexcom/bitfinex-api-node',
                ],
                'fees': 'https://www.bitfinex.com/fees',
            },
            'api': {
                'v1': {
                    'get': [
                        'symbols',
                        'symbols_details',
                    ],
                },
                'public': {
                    'get': [
                        'platform/status',
                        'tickers',
                        'ticker/{symbol}',
                        'trades/{symbol}/hist',
                        'book/{symbol}/{precision}',
                        'book/{symbol}/P0',
                        'book/{symbol}/P1',
                        'book/{symbol}/P2',
                        'book/{symbol}/P3',
                        'book/{symbol}/R0',
                        'stats1/{key}:{size}:{symbol}/{side}/{section}',
                        'stats1/{key}:{size}:{symbol}/long/last',
                        'stats1/{key}:{size}:{symbol}/long/hist',
                        'stats1/{key}:{size}:{symbol}/short/last',
                        'stats1/{key}:{size}:{symbol}/short/hist',
                        'candles/trade:{timeframe}:{symbol}/{section}',
                        'candles/trade:{timeframe}:{symbol}/last',
                        'candles/trade:{timeframe}:{symbol}/hist',
                    ],
                    'post': [
                        'calc/trade/avg',
                    ],
                },
                'private': {
                    'post': [
                        'auth/r/wallets',
                        'auth/r/orders/{symbol}',
                        'auth/r/orders/{symbol}/new',
                        'auth/r/orders/{symbol}/hist',
                        'auth/r/order/{symbol}:{id}/trades',
                        'auth/r/trades/{symbol}/hist',
                        'auth/r/positions',
                        'auth/r/funding/offers/{symbol}',
                        'auth/r/funding/offers/{symbol}/hist',
                        'auth/r/funding/loans/{symbol}',
                        'auth/r/funding/loans/{symbol}/hist',
                        'auth/r/funding/credits/{symbol}',
                        'auth/r/funding/credits/{symbol}/hist',
                        'auth/r/funding/trades/{symbol}/hist',
                        'auth/r/info/margin/{key}',
                        'auth/r/info/funding/{key}',
                        'auth/r/movements/{currency}/hist',
                        'auth/r/stats/perf:{timeframe}/hist',
                        'auth/r/alerts',
                        'auth/w/alert/set',
                        'auth/w/alert/{type}:{symbol}:{price}/del',
                        'auth/calc/order/avail',
                        'auth/r/ledgers/{symbol}/hist',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.0005,
                        'BCH': 0.0005,
                        'ETH': 0.01,
                        'EOS': 0.1,
                        'LTC': 0.001,
                        'OMG': 0.1,
                        'IOT': 0.0,
                        'NEO': 0.0,
                        'ETC': 0.01,
                        'XRP': 0.02,
                        'ETP': 0.01,
                        'ZEC': 0.001,
                        'BTG': 0.0,
                        'DASH': 0.01,
                        'XMR': 0.04,
                        'QTM': 0.01,
                        'EDO': 0.5,
                        'DAT': 1.0,
                        'AVT': 0.5,
                        'SAN': 0.1,
                        'USDT': 5.0,
                        'SPK': 9.2784,
                        'BAT': 9.0883,
                        'GNT': 8.2881,
                        'SNT': 14.303,
                        'QASH': 3.2428,
                        'YYW': 18.055,
                    },
                },
            },
        })

    def is_fiat(self, code):
        fiat = {
            'USD': 'USD',
            'EUR': 'EUR',
        }
        return(code in list(fiat.keys()))

    def get_currency_id(self, code):
        return 'f' + code

    async def fetch_markets(self):
        markets = await self.v1GetSymbolsDetails()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            id = market['pair'].upper()
            baseId = id[0:3]
            quoteId = id[3:6]
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            id = 't' + id
            baseId = self.get_currency_id(baseId)
            quoteId = self.get_currency_id(quoteId)
            precision = {
                'price': market['price_precision'],
                'amount': market['price_precision'],
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'minimum_order_size'),
                    'max': self.safe_float(market, 'maximum_order_size'),
                },
                'price': {
                    'min': math.pow(10, -precision['price']),
                    'max': math.pow(10, precision['price']),
                },
            }
            limits['cost'] = {
                'min': limits['amount']['min'] * limits['price']['min'],
                'max': None,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': limits,
                'lot': math.pow(10, -precision['amount']),
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostAuthRWallets()
        balanceType = self.safe_string(params, 'type', 'exchange')
        result = {'info': response}
        for b in range(0, len(response)):
            balance = response[b]
            accountType = balance[0]
            currency = balance[1]
            total = balance[2]
            available = balance[4]
            if accountType == balanceType:
                code = currency
                if currency in self.currencies_by_id:
                    code = self.currencies_by_id[currency]['code']
                elif currency[0] == 't':
                    currency = currency[1:]
                    code = currency.upper()
                    code = self.common_currency_code(code)
                else:
                    code = self.common_currency_code(code)
                account = self.account()
                account['total'] = total
                if not available:
                    if available == 0:
                        account['free'] = 0
                        account['used'] = total
                    else:
                        account['free'] = total
                else:
                    account['free'] = available
                    account['used'] = account['total'] - account['free']
                result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        orderbook = await self.publicGetBookSymbolPrecision(self.extend({
            'symbol': self.market_id(symbol),
            'precision': 'R0',
        }, params))
        timestamp = self.milliseconds()
        result = {
            'bids': [],
            'asks': [],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'nonce': None,
        }
        for i in range(0, len(orderbook)):
            order = orderbook[i]
            price = order[1]
            amount = order[2]
            side = 'bids' if (amount > 0) else 'asks'
            amount = abs(amount)
            result[side].append([price, amount])
        result['bids'] = self.sort_by(result['bids'], 0, True)
        result['asks'] = self.sort_by(result['asks'], 0)
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        length = len(ticker)
        last = ticker[length - 4]
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': ticker[length - 2],
            'low': ticker[length - 1],
            'bid': ticker[length - 10],
            'bidVolume': None,
            'ask': ticker[length - 8],
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': ticker[length - 6],
            'percentage': ticker[length - 5],
            'average': None,
            'baseVolume': ticker[length - 3],
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(self.extend({
            'symbols': ','.join(self.ids),
        }, params))
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker[0]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        ticker = await self.publicGetTickerSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        id, timestamp, amount, price = trade
        side = 'sell' if (amount < 0) else 'buy'
        if amount < 0:
            amount = -amount
        return {
            'id': str(id),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
        }

    async def fetch_trades(self, symbol, since=None, limit=120, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'sort': '-1',
            'limit': limit,  # default = max = 120
        }
        if since is not None:
            request['start'] = since
        response = await self.publicGetTradesSymbolHist(self.extend(request, params))
        trades = self.sort_by(response, 1)
        return self.parse_trades(trades, market, None, limit)

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=100, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if since is None:
            since = self.milliseconds() - self.parse_timeframe(timeframe) * limit * 1000
        request = {
            'symbol': market['id'],
            'timeframe': self.timeframes[timeframe],
            'sort': 1,
            'limit': limit,
            'start': since,
        }
        response = await self.publicGetCandlesTradeTimeframeSymbolHist(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        raise NotSupported(self.id + ' createOrder not implemented yet')

    def cancel_order(self, id, symbol=None, params={}):
        raise NotSupported(self.id + ' cancelOrder not implemented yet')

    async def fetch_order(self, id, symbol=None, params={}):
        raise NotSupported(self.id + ' fetchOrder not implemented yet')

    async def fetch_deposit_address(self, currency, params={}):
        raise NotSupported(self.id + ' fetchDepositAddress() not implemented yet.')

    async def withdraw(self, currency, amount, address, tag=None, params={}):
        raise NotSupported(self.id + ' withdraw not implemented yet')

    async def fetch_my_trades(self, symbol=None, since=None, limit=25, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit': limit,
            'end': self.seconds(),
        }
        if since is not None:
            request['start'] = int(since / 1000)
        response = await self.privatePostAuthRTradesSymbolHist(self.extend(request, params))
        # return self.parse_trades(response, market, since, limit)  # not implemented yet for bitfinex v2
        return response

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'v1':
            request = api + request
        else:
            request = self.version + request
        url = self.urls['api'] + '/' + request
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            body = self.json(query)
            auth = '/api' + '/' + request + nonce + body
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha384)
            headers = {
                'bfx-nonce': nonce,
                'bfx-apikey': self.apiKey,
                'bfx-signature': signature,
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if response:
            if 'message' in response:
                if response['message'].find('not enough exchange balance') >= 0:
                    raise InsufficientFunds(self.id + ' ' + self.json(response))
                raise ExchangeError(self.id + ' ' + self.json(response))
            return response
        elif response == '':
            raise ExchangeError(self.id + ' returned empty response')
        return response
