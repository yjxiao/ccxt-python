# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection


class bitmart(Exchange):

    def describe(self):
        return self.deep_extend(super(bitmart, self).describe(), {
            'id': 'bitmart',
            'name': 'BitMart',
            'countries': ['US', 'CN', 'HK', 'KR'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': True,
                'fetchMarkets': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchCurrencies': True,
                'fetchOrderBook': True,
                'fetchTrades': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'cancelAllOrders': True,
                'fetchOrders': False,
                'fetchOrderTrades': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchCanceledOrders': True,
                'fetchOrder': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/61835713-a2662f80-ae85-11e9-9d00-6442919701fd.jpg',
                'api': 'https://openapi.bitmart.com',
                'www': 'https://www.bitmart.com/',
                'doc': 'https://github.com/bitmartexchange/bitmart-official-api-docs',
                'referral': 'http://www.bitmart.com/?r=rQCFLh',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'token': {
                    'post': [
                        'authentication',
                    ],
                },
                'public': {
                    'get': [
                        'currencies',
                        'ping',
                        'steps',
                        'symbols',
                        'symbols_details',
                        'symbols/{symbol}/kline',
                        'symbols/{symbol}/orders',
                        'symbols/{symbol}/trades',
                        'ticker',
                        'time',
                    ],
                },
                'private': {
                    'get': [
                        'orders',
                        'orders/{id}',
                        'trades',
                        'wallet',
                    ],
                    'post': [
                        'orders',
                    ],
                    'delete': [
                        'orders',
                        'orders/{id}',
                    ],
                },
            },
            'timeframes': {
                '1m': 1,
                '3m': 3,
                '5m': 5,
                '15m': 15,
                '30m': 30,
                '45m': 45,
                '1h': 60,
                '2h': 120,
                '3h': 180,
                '4h': 240,
                '1d': 1440,
                '1w': 10080,
                '1M': 43200,
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.002,
                    'maker': 0.001,
                    'tiers': {
                        'taker': [
                            [0, 0.20 / 100],
                            [10, 0.18 / 100],
                            [50, 0.16 / 100],
                            [250, 0.14 / 100],
                            [1000, 0.12 / 100],
                            [5000, 0.10 / 100],
                            [25000, 0.08 / 100],
                            [50000, 0.06 / 100],
                        ],
                        'maker': [
                            [0, 0.1 / 100],
                            [10, 0.09 / 100],
                            [50, 0.08 / 100],
                            [250, 0.07 / 100],
                            [1000, 0.06 / 100],
                            [5000, 0.05 / 100],
                            [25000, 0.04 / 100],
                            [50000, 0.03 / 100],
                        ],
                    },
                },
            },
            'exceptions': {
                'exact': {
                    'Place order error': InvalidOrder,  # {"message":"Place order error"}
                    'Not found': OrderNotFound,  # {"message":"Not found"}
                    'Visit too often, please try again later': DDoSProtection,  # {"code":-30,"msg":"Visit too often, please try again later","subMsg":"","data":{}}
                    'Unknown symbol': BadSymbol,  # {"message":"Unknown symbol"}
                },
                'broad': {
                    'Maximum price is': InvalidOrder,  # {"message":"Maximum price is 0.112695"}
                    # {"message":"Required Integer parameter 'status' is not present"}
                    # {"message":"Required String parameter 'symbol' is not present"}
                    # {"message":"Required Integer parameter 'offset' is not present"}
                    # {"message":"Required Integer parameter 'limit' is not present"}
                    # {"message":"Required Long parameter 'from' is not present"}
                    # {"message":"Required Long parameter 'to' is not present"}
                    'is not present': BadRequest,
                },
            },
        })

    async def fetch_time(self, params={}):
        response = await self.publicGetTime(params)
        #
        #     {
        #         "server_time": 1527777538000
        #     }
        #
        return self.safe_integer(response, 'server_time')

    async def sign_in(self, params={}):
        message = self.apiKey + ':' + self.secret + ':' + self.uid
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.apiKey,
            'client_secret': self.hmac(self.encode(message), self.encode(self.secret), hashlib.sha256),
        }
        response = await self.tokenPostAuthentication(self.extend(data, params))
        accessToken = self.safe_string(response, 'access_token')
        if not accessToken:
            raise AuthenticationError(self.id + ' signIn() failed to authenticate. Access token missing from response.')
        expiresIn = self.safe_integer(response, 'expires_in')
        self.options['expires'] = self.sum(self.nonce(), expiresIn * 1000)
        self.options['accessToken'] = accessToken
        return response

    async def fetch_markets(self, params={}):
        markets = await self.publicGetSymbolsDetails(params)
        #
        #     [
        #         {
        #             "id":"1SG_BTC",
        #             "base_currency":"1SG",
        #             "quote_currency":"BTC",
        #             "quote_increment":"0.1",
        #             "base_min_size":"0.1000000000",
        #             "base_max_size":"10000000.0000000000",
        #             "price_min_precision":4,
        #             "price_max_precision":6,
        #             "expiration":"NA"
        #         }
        #     ]
        #
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'id')
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'quote_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            #
            # https://github.com/bitmartexchange/bitmart-official-api-docs/blob/master/rest/public/symbols_details.md#response-details
            # from the above API doc:
            # quote_increment Minimum order price as well as the price increment
            # price_min_precision Minimum price precision(digit) used to query price and kline
            # price_max_precision Maximum price precision(digit) used to query price and kline
            #
            # the docs are wrong: https://github.com/ccxt/ccxt/issues/5612
            #
            quoteIncrement = self.safe_string(market, 'quote_increment')
            amountPrecision = self.precision_from_string(quoteIncrement)
            pricePrecision = self.safe_integer(market, 'price_max_precision')
            precision = {
                'amount': amountPrecision,
                'price': pricePrecision,
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'base_min_size'),
                    'max': self.safe_float(market, 'base_max_size'),
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        marketId = self.safe_string(ticker, 'symbol_id')
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            elif marketId is not None:
                baseId, quoteId = marketId.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        last = self.safe_float(ticker, 'current_price')
        percentage = self.safe_float(ticker, 'fluctuation')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highest_price'),
            'low': self.safe_float(ticker, 'lowest_price'),
            'bid': self.safe_float(ticker, 'bid_1'),
            'bidVolume': self.safe_float(ticker, 'bid_1_amount'),
            'ask': self.safe_float(ticker, 'ask_1'),
            'askVolume': self.safe_float(ticker, 'ask_1_amount'),
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': percentage * 100,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'base_volume'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        response = await self.publicGetTicker(self.extend(request, params))
        #
        #     {
        #         "volume":"97487.38",
        #         "ask_1":"0.00148668",
        #         "base_volume":"144.59",
        #         "lowest_price":"0.00144362",
        #         "bid_1":"0.00148017",
        #         "highest_price":"0.00151000",
        #         "ask_1_amount":"92.03",
        #         "current_price":"0.00148230",
        #         "fluctuation":"+0.0227",
        #         "symbol_id":"XRP_ETH",
        #         "url":"https://www.bitmart.com/trade?symbol=XRP_ETH",
        #         "bid_1_amount":"134.78"
        #     }
        #
        return self.parse_ticker(response)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTicker(params)
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_currencies(self, params={}):
        currencies = await self.publicGetCurrencies(params)
        #
        #     [
        #         {
        #             "name":"CNY1",
        #             "withdraw_enabled":false,
        #             "id":"CNY1",
        #             "deposit_enabled":false
        #         }
        #     ]
        #
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            currencyId = self.safe_string(currency, 'id')
            code = self.safe_currency_code(currencyId)
            name = self.safe_string(currency, 'name')
            withdrawEnabled = self.safe_value(currency, 'withdraw_enabled')
            depositEnabled = self.safe_value(currency, 'deposit_enabled')
            active = withdrawEnabled and depositEnabled
            result[code] = {
                'id': currencyId,
                'code': code,
                'name': name,
                'info': currency,  # the original payload
                'active': active,
                'fee': None,
                'precision': None,
                'limits': {
                    'amount': {'min': None, 'max': None},
                    'price': {'min': None, 'max': None},
                    'cost': {'min': None, 'max': None},
                    'withdraw': {'min': None, 'max': None},
                },
            }
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            # 'precision': 4,  # optional price precision / depth level whose range is defined in symbol details
        }
        response = await self.publicGetSymbolsSymbolOrders(self.extend(request, params))
        return self.parse_order_book(response, None, 'buys', 'sells', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "amount":"2.29275119",
        #         "price":"0.021858",
        #         "count":"104.8930",
        #         "order_time":1563997286061,
        #         "type":"sell"
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         active: True,
        #             amount: '0.2000',
        #             entrustType: 1,
        #             entrust_id: 979648824,
        #             fees: '0.0000085532',
        #             price: '0.021383',
        #             symbol: 'ETH_BTC',
        #             timestamp: 1574343514000,
        #             trade_id: 329418828
        #     },
        #
        id = self.safe_string(trade, 'trade_id')
        timestamp = self.safe_integer_2(trade, 'timestamp', 'order_time')
        type = None
        side = self.safe_string_lower(trade, 'type')
        if (side is None) and ('entrustType' in trade):
            side = 'sell' if trade['entrustType'] else 'buy'
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        orderId = self.safe_integer(trade, 'entrust_id')
        marketId = self.safe_string(trade, 'symbol')
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                baseId, quoteId = marketId.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if symbol is None:
            if market is not None:
                symbol = market['symbol']
        feeCost = self.safe_float(trade, 'fees')
        fee = None
        if feeCost is not None:
            feeCurrencyCode = None
            if market is not None:
                feeCurrencyCode = market['base'] if (side == 'buy') else market['quote']
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'takerOrMaker': None,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetSymbolsSymbolTrades(self.extend(request, params))
        #
        #     [
        #         {
        #             "amount":"2.29275119",
        #             "price":"0.021858",
        #             "count":"104.8930",
        #             "order_time":1563997286061,
        #             "type":"sell"
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'offset': 0,  # current page, starts from 0
            'limit': 500,
        }
        if limit is not None:
            request['limit'] = limit  # default 500, max 1000
        response = await self.privateGetTrades(self.extend(request, params))
        #
        #     {
        #         "total_trades": 216,
        #         "total_pages": 22,
        #         "current_page": 0,
        #         "trades": [
        #             {
        #                 "symbol": "BMX_ETH",
        #                 "amount": "1.0",
        #                 "fees": "0.0005000000",
        #                 "trade_id": 2734956,
        #                 "price": "0.00013737",
        #                 "active": True,
        #                 "entrust_id": 5576623,
        #                 "timestamp": 1545292334000
        #             },
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'trades', [])
        return self.parse_trades(trades, market, since, limit)

    async def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'entrust_id': id,
        }
        return await self.fetch_my_trades(symbol, since, limit, self.extend(request, params))

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_integer(ohlcv, 'timestamp'),
            self.safe_float(ohlcv, 'open_price'),
            self.safe_float(ohlcv, 'highest_price'),
            self.safe_float(ohlcv, 'lowest_price'),
            self.safe_float(ohlcv, 'current_price'),
            self.safe_float(ohlcv, 'volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        if since is None and limit is None:
            raise ArgumentsRequired(self.id + ' fetchOHLCV requires either a `since` argument or a `limit` argument(or both)')
        await self.load_markets()
        market = self.market(symbol)
        periodInSeconds = self.parse_timeframe(timeframe)
        duration = periodInSeconds * limit * 1000
        to = self.milliseconds()
        if since is None:
            since = to - duration
        else:
            to = self.sum(since, duration)
        request = {
            'symbol': market['id'],
            'from': since,  # start time of k-line data(in milliseconds, required)
            'to': to,  # end time of k-line data(in milliseconds, required)
            'step': self.timeframes[timeframe],  # steps of sampling(in minutes, default 1 minute, optional)
        }
        response = await self.publicGetSymbolsSymbolKline(self.extend(request, params))
        #
        #     [
        #         {
        #             "timestamp":1525761000000,
        #             "open_price":"0.010130",
        #             "highest_price":"0.010130",
        #             "lowest_price":"0.010130",
        #             "current_price":"0.010130",
        #             "volume":"0.000000"
        #         }
        #     ]
        #
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privateGetWallet(params)
        #
        #     [
        #         {
        #             "name":"Bitcoin",
        #             "available":"0.0000000000",
        #             "frozen":"0.0000000000",
        #             "id":"BTC"
        #         }
        #     ]
        #
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'id')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['used'] = self.safe_float(balance, 'frozen')
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "entrust_id":1223181
        #     }
        #
        # cancelOrder
        #
        #     {}
        #
        # fetchOrder, fetchOrdersByStatus, fetchOpenOrders, fetchClosedOrders
        #
        #     {
        #         "entrust_id":1223181,
        #         "symbol":"BMX_ETH",
        #         "timestamp":1528060666000,
        #         "side":"buy",
        #         "price":"1.000000",
        #         "fees":"0.1",
        #         "original_amount":"1",
        #         "executed_amount":"1",
        #         "remaining_amount":"0",
        #         "status":3
        #     }
        #
        id = self.safe_string(order, 'entrust_id')
        timestamp = self.milliseconds()
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = self.find_symbol(self.safe_string(order, 'symbol'), market)
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'original_amount')
        cost = None
        filled = self.safe_float(order, 'executed_amount')
        remaining = self.safe_float(order, 'remaining_amount')
        if amount is not None:
            if remaining is not None:
                if filled is None:
                    filled = amount - remaining
            if filled is not None:
                if remaining is None:
                    remaining = amount - filled
                if cost is None:
                    if price is not None:
                        cost = price * filled
        side = self.safe_string(order, 'side')
        type = None
        return {
            'id': id,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': None,
            'average': None,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
            'trades': None,
        }

    def parse_order_status(self, status):
        statuses = {
            '0': 'all',
            '1': 'open',
            '2': 'open',
            '3': 'closed',
            '4': 'canceled',
            '5': 'open',
            '6': 'closed',
        }
        return self.safe_string(statuses, status, status)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'side': side.lower(),
            'amount': float(self.amount_to_precision(symbol, amount)),
            'price': float(self.price_to_precision(symbol, price)),
        }
        response = await self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #         "entrust_id":1223181
        #     }
        #
        return self.parse_order(response, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        intId = int(id)
        request = {
            'id': intId,
            'entrust_id': intId,
        }
        response = await self.privateDeleteOrdersId(self.extend(request, params))
        #
        # responds with an empty object {}
        #
        return self.parse_order(response)

    async def cancel_all_orders(self, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelAllOrders requires a symbol argument')
        side = self.safe_string(params, 'side')
        if side is None:
            raise ArgumentsRequired(self.id + " cancelAllOrders requires a `side` parameter('buy' or 'sell')")
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'side': side,  # 'buy' or 'sell'
        }
        response = await self.privateDeleteOrders(self.extend(request, params))
        #
        # responds with an empty object {}
        #
        return response

    async def fetch_orders_by_status(self, status, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrdersByStatus requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500  # default 500, max 1000
        request = {
            'symbol': market['id'],
            'status': status,
            'offset': 0,  # current page, starts from 0
            'limit': limit,
        }
        response = await self.privateGetOrders(self.extend(request, params))
        #
        #     {
        #         "orders":[
        #             {
        #                 "entrust_id":1223181,
        #                 "symbol":"BMX_ETH",
        #                 "timestamp":1528060666000,
        #                 "side":"buy",
        #                 "price":"1.000000",
        #                 "fees":"0.1",
        #                 "original_amount":"1",
        #                 "executed_amount":"1",
        #                 "remaining_amount":"0",
        #                 "status":3
        #             }
        #         ],
        #         "total_pages":1,
        #         "total_orders":1,
        #         "current_page":0,
        #     }
        #
        orders = self.safe_value(response, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        # 5 = pending & partially filled orders
        return await self.fetch_orders_by_status(5, symbol, since, limit, params)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        # 3 = closed orders
        return await self.fetch_orders_by_status(3, symbol, since, limit, params)

    async def fetch_canceled_orders(self, symbol=None, since=None, limit=None, params={}):
        # 4 = canceled orders
        return await self.fetch_orders_by_status(4, symbol, since, limit, params)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privateGetOrdersId(self.extend(request, params))
        #
        #     {
        #         "entrust_id":1223181,
        #         "symbol":"BMX_ETH",
        #         "timestamp":1528060666000,
        #         "side":"buy",
        #         "price":"1.000000",
        #         "fees":"0.1",
        #         "original_amount":"1",
        #         "executed_amount":"1",
        #         "remaining_amount":"0",
        #         "status":3
        #     }
        #
        return self.parse_order(response)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'token':
            self.check_required_credentials()
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        else:
            nonce = self.nonce()
            self.check_required_credentials()
            token = self.safe_string(self.options, 'accessToken')
            if token is None:
                raise AuthenticationError(self.id + ' ' + path + ' endpoint requires an accessToken option or a prior call to signIn() method')
            expires = self.safe_integer(self.options, 'expires')
            if expires is not None:
                if nonce >= expires:
                    raise AuthenticationError(self.id + ' accessToken expired, supply a new accessToken or call the signIn() method')
            if query:
                url += '?' + self.urlencode(query)
            headers = {
                'Content-Type': 'application/json',
                'X-BM-TIMESTAMP': str(nonce),
                'X-BM-AUTHORIZATION': 'Bearer ' + token,
            }
            if method != 'GET':
                query = self.keysort(query)
                body = self.json(query)
                message = self.urlencode(query)
                headers['X-BM-SIGNATURE'] = self.hmac(self.encode(message), self.encode(self.secret), hashlib.sha256)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        #
        #     {"message":"Maximum price is 0.112695"}
        #     {"message":"Required Integer parameter 'status' is not present"}
        #     {"message":"Required String parameter 'symbol' is not present"}
        #     {"message":"Required Integer parameter 'offset' is not present"}
        #     {"message":"Required Integer parameter 'limit' is not present"}
        #     {"message":"Required Long parameter 'from' is not present"}
        #     {"message":"Required Long parameter 'to' is not present"}
        #     {"message":"Invalid status. status=6 not support any more, please use 3:deal_success orders, 4:cancelled orders"}
        #     {"message":"Not found"}
        #     {"message":"Place order error"}
        #
        feedback = self.id + ' ' + body
        message = self.safe_string_2(response, 'message', 'msg')
        if message is not None:
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
            raise ExchangeError(feedback)  # unknown message
