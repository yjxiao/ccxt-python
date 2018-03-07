# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.acx import acx
from ccxt.base.errors import ExchangeError


class kuna (acx):

    def describe(self):
        return self.deep_extend(super(kuna, self).describe(), {
            'id': 'kuna',
            'name': 'Kuna',
            'countries': 'UA',
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'withdraw': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31697638-912824fa-b3c1-11e7-8c36-cf9606eb94ac.jpg',
                'api': 'https://kuna.io',
                'www': 'https://kuna.io',
                'doc': 'https://kuna.io/documents/api',
                'fees': 'https://kuna.io/documents/api',
            },
            'api': {
                'public': {
                    'get': [
                        'tickers',  # all of them at once
                        'tickers/{market}',
                        'order_book',
                        'order_book/{market}',
                        'trades',
                        'trades/{market}',
                        'timestamp',
                    ],
                },
                'private': {
                    'get': [
                        'members/me',
                        'orders',
                        'trades/my',
                    ],
                    'post': [
                        'orders',
                        'order/delete',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                },
                'funding': {
                    'withdraw': {
                        'UAH': '1%',
                        'BTC': 0.001,
                        'BCH': 0.001,
                        'ETH': 0.01,
                        'WAVES': 0.01,
                        'GOL': 0.0,
                        'GBG': 0.0,
                        # 'RMC': 0.001 BTC
                        # 'ARN': 0.01 ETH
                        # 'R': 0.01 ETH
                        # 'EVR': 0.01 ETH
                    },
                    'deposit': {
                        # 'UAH': (amount) => amount * 0.001 + 5
                    },
                },
            },
        })

    async def fetch_markets(self):
        predefinedMarkets = [
            {'id': 'btcuah', 'symbol': 'BTC/UAH', 'base': 'BTC', 'quote': 'UAH', 'baseId': 'btc', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'ethuah', 'symbol': 'ETH/UAH', 'base': 'ETH', 'quote': 'UAH', 'baseId': 'eth', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'gbguah', 'symbol': 'GBG/UAH', 'base': 'GBG', 'quote': 'UAH', 'baseId': 'gbg', 'quoteId': 'uah', 'precision': {'amount': 3, 'price': 2}, 'lot': 0.001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 0.01, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},  # Golos Gold(GBG != GOLOS)
            {'id': 'kunbtc', 'symbol': 'KUN/BTC', 'base': 'KUN', 'quote': 'BTC', 'baseId': 'kun', 'quoteId': 'btc', 'precision': {'amount': 6, 'price': 6}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 0.000001, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'bchbtc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bch', 'quoteId': 'btc', 'precision': {'amount': 6, 'price': 6}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 0.000001, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'bchuah', 'symbol': 'BCH/UAH', 'base': 'BCH', 'quote': 'UAH', 'baseId': 'bch', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'wavesuah', 'symbol': 'WAVES/UAH', 'base': 'WAVES', 'quote': 'UAH', 'baseId': 'waves', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 0.000001, 'limits': {'amount': {'min': 0.000001, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 0.000001, 'max': None}}},
            {'id': 'arnbtc', 'symbol': 'ARN/BTC', 'base': 'ARN', 'quote': 'BTC', 'baseId': 'arn', 'quoteId': 'btc'},
            {'id': 'b2bbtc', 'symbol': 'B2B/BTC', 'base': 'B2B', 'quote': 'BTC', 'baseId': 'b2b', 'quoteId': 'btc'},
            {'id': 'evrbtc', 'symbol': 'EVR/BTC', 'base': 'EVR', 'quote': 'BTC', 'baseId': 'evr', 'quoteId': 'btc'},
            {'id': 'golgbg', 'symbol': 'GOL/GBG', 'base': 'GOL', 'quote': 'GBG', 'baseId': 'gol', 'quoteId': 'gbg'},
            {'id': 'rbtc', 'symbol': 'R/BTC', 'base': 'R', 'quote': 'BTC', 'baseId': 'r', 'quoteId': 'btc'},
            {'id': 'rmcbtc', 'symbol': 'RMC/BTC', 'base': 'RMC', 'quote': 'BTC', 'baseId': 'rmc', 'quoteId': 'btc'},
        ]
        markets = []
        tickers = await self.publicGetTickers()
        for i in range(0, len(predefinedMarkets)):
            market = predefinedMarkets[i]
            if market['id'] in tickers:
                markets.append(market)
        marketsById = self.index_by(markets, 'id')
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if not(id in list(marketsById.keys())):
                baseId = id.replace('btc', '')
                baseId = baseId.replace('uah', '')
                baseId = baseId.replace('gbg', '')
                if len(baseId) > 0:
                    baseIdLength = len(baseId) - 0  # a transpiler workaround
                    quoteId = id[baseIdLength:]
                    base = baseId.upper()
                    quote = quoteId.upper()
                    base = self.common_currency_code(base)
                    quote = self.common_currency_code(quote)
                    symbol = base + '/' + quote
                    markets.append({
                        'id': id,
                        'symbol': symbol,
                        'base': base,
                        'quote': quote,
                        'baseId': baseId,
                        'quoteId': quoteId,
                    })
        return markets

    async def fetch_order_book(self, symbol, limit=None, params={}):
        market = self.market(symbol)
        orderBook = await self.publicGetOrderBook(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_order_book(orderBook, None, 'bids', 'asks', 'price', 'remaining_volume')

    async def fetch_l3_order_book(self, symbol, limit=None, params={}):
        return self.fetch_order_book(symbol, limit, params)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol argument')
        market = self.market(symbol)
        orders = await self.privateGetOrders(self.extend({
            'market': market['id'],
        }, params))
        # todo emulation of fetchClosedOrders, fetchOrders, fetchOrder
        # with order cache + fetchOpenOrders
        # as in BTC-e, Liqui, Yobit, DSX, Tidex, WEX
        return self.parse_orders(orders, market, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['created_at'])
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'id': str(trade['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'price': float(trade['price']),
            'amount': float(trade['volume']),
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = await self.publicGetTrades(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    def parse_my_trade(self, trade, market):
        timestamp = self.parse8601(trade['created_at'])
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'id': trade['id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'price': trade['price'],
            'amount': trade['volume'],
            'cost': trade['funds'],
            'symbol': symbol,
            'side': trade['side'],
            'order': trade['order_id'],
        }

    def parse_my_trades(self, trades, market=None):
        parsedTrades = []
        for i in range(0, len(trades)):
            trade = trades[i]
            parsedTrade = self.parse_my_trade(trade, market)
            parsedTrades.append(parsedTrade)
        return parsedTrades

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol argument')
        market = self.market(symbol)
        response = await self.privateGetTradesMy({'market': market['id']})
        return self.parse_my_trades(response, market)
