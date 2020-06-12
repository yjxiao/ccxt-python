# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import NotSupported


class xbtce(Exchange):

    def describe(self):
        return self.deep_extend(super(xbtce, self).describe(), {
            'id': 'xbtce',
            'name': 'xBTCe',
            'countries': ['RU'],
            'rateLimit': 2000,  # responses are cached every 2 seconds
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'createMarketOrder': False,
                'fetchOHLCV': False,
            },
            'urls': {
                'referral': 'https://xbtce.com/?agent=XX97BTCXXXG687021000B',
                'logo': 'https://user-images.githubusercontent.com/1294454/28059414-e235970c-662c-11e7-8c3a-08e31f78684b.jpg',
                'api': 'https://cryptottlivewebapi.xbtce.net:8443/api',
                'www': 'https://www.xbtce.com',
                'doc': [
                    'https://www.xbtce.com/tradeapi',
                    'https://support.xbtce.info/Knowledgebase/Article/View/52/25/xbtce-exchange-api',
                ],
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'currency',
                        'currency/{filter}',
                        'level2',
                        'level2/{filter}',
                        'quotehistory/{symbol}/{periodicity}/bars/ask',
                        'quotehistory/{symbol}/{periodicity}/bars/bid',
                        'quotehistory/{symbol}/level2',
                        'quotehistory/{symbol}/ticks',
                        'symbol',
                        'symbol/{filter}',
                        'tick',
                        'tick/{filter}',
                        'ticker',
                        'ticker/{filter}',
                        'tradesession',
                    ],
                },
                'private': {
                    'get': [
                        'tradeserverinfo',
                        'tradesession',
                        'currency',
                        'currency/{filter}',
                        'level2',
                        'level2/{filter}',
                        'symbol',
                        'symbol/{filter}',
                        'tick',
                        'tick/{filter}',
                        'account',
                        'asset',
                        'asset/{id}',
                        'position',
                        'position/{id}',
                        'trade',
                        'trade/{id}',
                        'quotehistory/{symbol}/{periodicity}/bars/ask',
                        'quotehistory/{symbol}/{periodicity}/bars/ask/info',
                        'quotehistory/{symbol}/{periodicity}/bars/bid',
                        'quotehistory/{symbol}/{periodicity}/bars/bid/info',
                        'quotehistory/{symbol}/level2',
                        'quotehistory/{symbol}/level2/info',
                        'quotehistory/{symbol}/periodicities',
                        'quotehistory/{symbol}/ticks',
                        'quotehistory/{symbol}/ticks/info',
                        'quotehistory/cache/{symbol}/{periodicity}/bars/ask',
                        'quotehistory/cache/{symbol}/{periodicity}/bars/bid',
                        'quotehistory/cache/{symbol}/level2',
                        'quotehistory/cache/{symbol}/ticks',
                        'quotehistory/symbols',
                        'quotehistory/version',
                    ],
                    'post': [
                        'trade',
                        'tradehistory',
                    ],
                    'put': [
                        'trade',
                    ],
                    'delete': [
                        'trade',
                    ],
                },
            },
            'commonCurrencies': {
                'DSH': 'DASH',
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.privateGetSymbol(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'Symbol')
            baseId = self.safe_string(market, 'MarginCurrency')
            quoteId = self.safe_string(market, 'ProfitCurrency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            symbol = symbol if market['IsTradeAllowed'] else id
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': None,
                'precision': self.precision,
                'limits': self.limits,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privateGetAsset(params)
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'Currency')
            code = self.safe_currency_code(currencyId)
            account = {
                'free': self.safe_float(balance, 'FreeAmount'),
                'used': self.safe_float(balance, 'LockedAmount'),
                'total': self.safe_float(balance, 'Amount'),
            }
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'filter': market['id'],
        }
        response = await self.privateGetLevel2Filter(self.extend(request, params))
        orderbook = response[0]
        timestamp = self.safe_integer(orderbook, 'Timestamp')
        return self.parse_order_book(orderbook, timestamp, 'Bids', 'Asks', 'Price', 'Volume')

    def parse_ticker(self, ticker, market=None):
        timestamp = 0
        last = None
        if 'LastBuyTimestamp' in ticker:
            if timestamp < ticker['LastBuyTimestamp']:
                timestamp = ticker['LastBuyTimestamp']
                last = ticker['LastBuyPrice']
        if 'LastSellTimestamp' in ticker:
            if timestamp < ticker['LastSellTimestamp']:
                timestamp = ticker['LastSellTimestamp']
                last = ticker['LastSellPrice']
        if not timestamp:
            timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': ticker['DailyBestBuyPrice'],
            'low': ticker['DailyBestSellPrice'],
            'bid': ticker['BestBid'],
            'bidVolume': None,
            'ask': ticker['BestAsk'],
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': ticker['DailyTradedTotalVolume'],
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTicker(params)
        tickers = self.index_by(response, 'Symbol')
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                baseId = id[0:3]
                quoteId = id[3:6]
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'filter': market['id'],
        }
        response = await self.publicGetTickerFilter(self.extend(request, params))
        length = len(response)
        if length < 1:
            raise ExchangeError(self.id + ' fetchTicker returned empty response, xBTCe public API error')
        tickers = self.index_by(response, 'Symbol')
        ticker = tickers[market['id']]
        return self.parse_ticker(ticker, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        # no method for trades?
        return await self.privateGetTrade(params)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_integer(ohlcv, 'Timestamp'),
            self.safe_float(ohlcv, 'Open'),
            self.safe_float(ohlcv, 'High'),
            self.safe_float(ohlcv, 'Low'),
            self.safe_float(ohlcv, 'Close'),
            self.safe_float(ohlcv, 'Volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        #     minutes = int(timeframe / 60)  # 1 minute by default
        #     periodicity = str(minutes)
        #     await self.load_markets()
        #     market = self.market(symbol)
        #     if since is None:
        #         since = self.seconds() - 86400 * 7  # last day by defulat
        #     if limit is None:
        #         limit = 1000  # default
        #     response = await self.privateGetQuotehistorySymbolPeriodicityBarsBid(self.extend({
        #         'symbol': market['id'],
        #         'periodicity': periodicity,
        #         'timestamp': since,
        #         'count': limit,
        #     }, params))
        #     return self.parse_ohlcvs(response['Bars'], market, since, limit)
        raise NotSupported(self.id + ' fetchOHLCV is disabled by the exchange')

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        request = {
            'pair': self.market_id(symbol),
            'type': side,
            'amount': amount,
            'rate': price,
        }
        response = await self.privatePostTrade(self.extend(request, params))
        return {
            'info': response,
            'id': str(response['Id']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'Type': 'Cancel',
            'Id': id,
        }
        return await self.privateDeleteTrade(self.extend(request, params))

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if not self.apiKey:
            raise AuthenticationError(self.id + ' requires apiKey for all requests, their public API is always busy')
        if not self.uid:
            raise AuthenticationError(self.id + ' requires uid property for authentication and trading, their public API is always busy')
        url = self.urls['api'] + '/' + self.version
        if api == 'public':
            url += '/' + api
        url += '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            headers = {'Accept-Encoding': 'gzip, deflate'}
            nonce = str(self.nonce())
            if method == 'POST':
                if query:
                    headers['Content-Type'] = 'application/json'
                    body = self.json(query)
                else:
                    url += '?' + self.urlencode(query)
            auth = nonce + self.uid + self.apiKey + method + url
            if body:
                auth += body
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256, 'base64')
            credentials = self.uid + ':' + self.apiKey + ':' + nonce + ':' + self.decode(signature)
            headers['Authorization'] = 'HMAC ' + credentials
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
