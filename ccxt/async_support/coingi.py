# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
from ccxt.base.errors import ExchangeError


class coingi(Exchange):

    def describe(self):
        return self.deep_extend(super(coingi, self).describe(), {
            'id': 'coingi',
            'name': 'Coingi',
            'rateLimit': 1000,
            'countries': ['PA', 'BG', 'CN', 'US'],  # Panama, Bulgaria, China, US
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchMarkets': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
            },
            'urls': {
                'referral': 'https://www.coingi.com/?r=XTPPMC',
                'logo': 'https://user-images.githubusercontent.com/1294454/28619707-5c9232a8-7212-11e7-86d6-98fe5d15cc6e.jpg',
                'api': {
                    'www': 'https://coingi.com',
                    'current': 'https://api.coingi.com',
                    'user': 'https://api.coingi.com',
                },
                'www': 'https://coingi.com',
                'doc': 'https://coingi.docs.apiary.io',
            },
            'api': {
                'www': {
                    'get': [
                        '',
                    ],
                },
                'current': {
                    'get': [
                        'order-book/{pair}/{askCount}/{bidCount}/{depth}',
                        'transactions/{pair}/{maxCount}',
                        '24hour-rolling-aggregation',
                    ],
                },
                'user': {
                    'post': [
                        'balance',
                        'add-order',
                        'cancel-order',
                        'orders',
                        'transactions',
                        'create-crypto-withdrawal',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.2 / 100,
                    'maker': 0.2 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.001,
                        'LTC': 0.01,
                        'DOGE': 2,
                        'PPC': 0.02,
                        'VTC': 0.2,
                        'NMC': 2,
                        'DASH': 0.002,
                        'USD': 10,
                        'EUR': 10,
                    },
                    'deposit': {
                        'BTC': 0,
                        'LTC': 0,
                        'DOGE': 0,
                        'PPC': 0,
                        'VTC': 0,
                        'NMC': 0,
                        'DASH': 0,
                        'USD': 5,
                        'EUR': 1,
                    },
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.wwwGet(params)
        parts = response.split('do=currencyPairSelector-selectCurrencyPair" class="active">')
        currencyParts = parts[1].split('<div class="currency-pair-label">')
        result = []
        for i in range(1, len(currencyParts)):
            currencyPart = currencyParts[i]
            idParts = currencyPart.split('</div>')
            id = idParts[0]
            id = id.replace('/', '-')
            id = id.lower()
            baseId, quoteId = id.split('-')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': 8,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': id,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': math.pow(10, precision['amount']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        lowercaseCurrencies = []
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            lowercaseCurrencies.append(currency.lower())
        request = {
            'currencies': ','.join(lowercaseCurrencies),
        }
        response = await self.userPostBalance(self.extend(request, params))
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance['currency'], 'name')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            blocked = self.safe_float(balance, 'blocked')
            inOrders = self.safe_float(balance, 'inOrders')
            withdrawing = self.safe_float(balance, 'withdrawing')
            account['used'] = self.sum(blocked, inOrders, withdrawing)
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=512, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'depth': 32,  # maximum number of depth range steps 1-32
            'askCount': limit,  # maximum returned number of asks 1-512
            'bidCount': limit,  # maximum returned number of bids 1-512
        }
        orderbook = await self.currentGetOrderBookPairAskCountBidCountDepth(self.extend(request, params))
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'baseAmount')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': None,
            'last': None,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'baseVolume'),
            'quoteVolume': self.safe_float(ticker, 'counterVolume'),
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.currentGet24hourRollingAggregation(params)
        result = {}
        for t in range(0, len(response)):
            ticker = response[t]
            base = ticker['currencyPair']['base'].upper()
            quote = ticker['currencyPair']['counter'].upper()
            symbol = base + '/' + quote
            market = None
            if symbol in self.markets:
                market = self.markets[symbol]
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        tickers = await self.fetch_tickers(None, params)
        if symbol in tickers:
            return tickers[symbol]
        raise ExchangeError(self.id + ' return did not contain ' + symbol)

    def parse_trade(self, trade, market=None):
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        timestamp = self.safe_integer(trade, 'timestamp')
        id = self.safe_string(trade, 'id')
        marketId = self.safe_string(trade, 'currencyPair')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,  # type
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
            'pair': market['id'],
            'maxCount': 128,
        }
        response = await self.currentGetTransactionsPairMaxCount(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'currencyPair': self.market_id(symbol),
            'volume': amount,
            'price': price,
            'orderType': 0 if (side == 'buy') else 1,
        }
        response = await self.userPostAddOrder(self.extend(request, params))
        return {
            'info': response,
            'id': response['result'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderId': id,
        }
        return await self.userPostCancelOrder(self.extend(request, params))

    def sign(self, path, api='current', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api != 'www':
            url += '/' + api + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'current':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'user':
            self.check_required_credentials()
            nonce = self.nonce()
            request = self.extend({
                'token': self.apiKey,
                'nonce': nonce,
            }, query)
            auth = str(nonce) + '$' + self.apiKey
            request['signature'] = self.hmac(self.encode(auth), self.encode(self.secret))
            body = self.json(request)
            headers = {
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='current', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if not isinstance(response, basestring):
            if 'errors' in response:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
