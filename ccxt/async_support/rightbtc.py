# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import ROUND


class rightbtc (Exchange):

    def describe(self):
        return self.deep_extend(super(rightbtc, self).describe(), {
            'id': 'rightbtc',
            'name': 'RightBTC',
            'countries': ['AE'],
            'has': {
                'privateAPI': False,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': False,
                'fetchOrder': 'emulated',
                'fetchMyTrades': True,
            },
            'timeframes': {
                '1m': 'min1',
                '5m': 'min5',
                '15m': 'min15',
                '30m': 'min30',
                '1h': 'hr1',
                '1d': 'day1',
                '1w': 'week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/42633917-7d20757e-85ea-11e8-9f53-fffe9fbb7695.jpg',
                'api': 'https://www.rightbtc.com/api',
                'www': 'https://www.rightbtc.com',
                'doc': [
                    'https://52.53.159.206/api/trader/',
                    'https://support.rightbtc.com/hc/en-us/articles/360012809412',
                ],
                # eslint-disable-next-line no-useless-escape
                # 'fees': 'https://www.rightbtc.com/\#\not /support/fee',
            },
            'api': {
                'public': {
                    'get': [
                        # 'getAssetsTradingPairs/zh',  # 404
                        'trading_pairs',
                        'ticker/{trading_pair}',
                        'tickers',
                        'depth/{trading_pair}',
                        'depth/{trading_pair}/{count}',
                        'trades/{trading_pair}',
                        'trades/{trading_pair}/{count}',
                        'candlestick/latest/{trading_pair}',
                        'candlestick/{timeSymbol}/{trading_pair}',
                        'candlestick/{timeSymbol}/{trading_pair}/{count}',
                    ],
                },
                'trader': {
                    'get': [
                        'balance/{symbol}',
                        'balances',
                        'deposits/{asset}/{page}',
                        'withdrawals/{asset}/{page}',
                        'orderpage/{trading_pair}/{cursor}',
                        'orders/{trading_pair}/{ids}',  # ids are a slash-separated list of {id}/{id}/{id}/...
                        'history/{trading_pair}/{ids}',
                        'historys/{trading_pair}/{page}',
                        'trading_pairs',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete': [
                        'order/{trading_pair}/{ids}',
                    ],
                },
            },
            # HARDCODING IS DEPRECATED, THE FEES BELOW SHOULD BE REWRITTEN
            'fees': {
                'trading': {
                    # min trading fees
                    # 0.0001 BTC
                    # 0.01 ETP
                    # 0.001 ETH
                    # 0.1 BITCNY
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'withdraw': {
                        # 'BTM': n => 3 + n * (1 / 100),
                        # 'ZDC': n => 1 + n * (0.5 / 100),
                        # 'ZGC': n => 0.5 + n * (0.5 / 100),
                        # 'BTS': n => 1 + n * (1 / 100),
                        # 'DLT': n => 3 + n * (1 / 100),
                        # 'SNT': n => 10 + n * (1 / 100),
                        # 'XNC': n => 1 + n * (1 / 100),
                        # 'ICO': n => 3 + n * (1 / 100),
                        # 'CMC': n => 1 + n * (0.5 / 100),
                        # 'GXS': n => 0.2 + n * (1 / 100),
                        # 'OBITS': n => 0.3 + n * (1 / 100),
                        # 'ICS': n => 2 + n * (1 / 100),
                        # 'TIC': n => 2 + n * (1 / 100),
                        # 'IND': n => 20 + n * (1 / 100),
                        # 'MVC': n => 20 + n * (1 / 100),
                        # 'BitCNY': n => 0.1 + n * (1 / 100),
                        # 'MTX': n => 1 + n * (1 / 100),
                        'ETP': 0.01,
                        'BTC': 0.001,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'STORJ': 3,
                        'LTC': 0.001,
                        'ZEC': 0.001,
                        'BCC': 0.001,
                        'XRB': 0,
                        'NXS': 0.1,
                    },
                },
            },
            'commonCurrencies': {
                'XRB': 'NANO',
            },
            'exceptions': {
                'ERR_USERTOKEN_NOT_FOUND': AuthenticationError,
                'ERR_ASSET_NOT_EXISTS': ExchangeError,
                'ERR_ASSET_NOT_AVAILABLE': ExchangeError,
                'ERR_BALANCE_NOT_ENOUGH': InsufficientFunds,
                'ERR_CREATE_ORDER': InvalidOrder,
                'ERR_CANDLESTICK_DATA': ExchangeError,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetTradingPairs(params)
        # zh = await self.publicGetGetAssetsTradingPairsZh()
        markets = self.extend(response['status']['message'])
        marketIds = list(markets.keys())
        result = []
        for i in range(0, len(marketIds)):
            id = marketIds[i]
            market = markets[id]
            baseId = self.safe_string(market, 'bid_asset_symbol')
            quoteId = self.safe_string(market, 'ask_asset_symbol')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'bid_asset_decimals'),
                'price': self.safe_integer(market, 'ask_asset_decimals'),
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
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': math.pow(10, precision['price']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': math.pow(10, precision['price']),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def divide_safe_float(self, x, key, divisor):
        value = self.safe_float(x, key)
        if value is not None:
            return value / divisor
        return value

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'date')
        last = self.divide_safe_float(ticker, 'last', 1e8)
        high = self.divide_safe_float(ticker, 'high', 1e8)
        low = self.divide_safe_float(ticker, 'low', 1e8)
        bid = self.divide_safe_float(ticker, 'buy', 1e8)
        ask = self.divide_safe_float(ticker, 'sell', 1e8)
        baseVolume = self.divide_safe_float(ticker, 'vol24h', 1e8)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': high,
            'low': low,
            'bid': bid,
            'bidVolume': None,
            'ask': ask,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
        }
        response = await self.publicGetTickerTradingPair(self.extend(request, params))
        result = self.safe_value(response, 'result')
        if not result:
            raise ExchangeError(self.id + ' fetchTicker returned an empty response for symbol ' + symbol)
        return self.parse_ticker(result, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTickers(params)
        tickers = response['result']
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker['market']
            if not(id in list(self.marketsById.keys())):
                continue
            market = self.marketsById[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'trading_pair': self.market_id(symbol),
        }
        method = 'publicGetDepthTradingPair'
        if limit is not None:
            method += 'Count'
            request['count'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        bidsasks = {}
        types = ['bid', 'ask']
        for ti in range(0, len(types)):
            type = types[ti]
            bidsasks[type] = []
            for i in range(0, len(response['result'][type])):
                price, amount, total = response['result'][type][i]
                bidsasks[type].append([
                    price / 1e8,
                    amount / 1e8,
                    total / 1e8,
                ])
        return self.parse_order_book(bidsasks, None, 'bid', 'ask')

    def parse_trade(self, trade, market=None):
        #
        #     {
        #         "order_id": 118735,
        #         "trade_id": 7,
        #         "trading_pair": "BTCCNY",
        #         "side": "B",
        #         "quantity": 1000000000,
        #         "price": 900000000,
        #         "created_at": "2017-06-06T20:45:27.000Z"
        #     }
        #
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        id = self.safe_string(trade, 'tid')
        id = self.safe_string(trade, 'trade_id', id)
        orderId = self.safe_string(trade, 'order_id')
        price = self.divide_safe_float(trade, 'price', 1e8)
        amount = self.safe_float(trade, 'amount')
        amount = self.safe_float(trade, 'quantity', amount)
        if amount is not None:
            amount = amount / 1e8
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'trading_pair')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        cost = self.cost_to_precision(symbol, price * amount)
        cost = float(cost)
        side = self.safe_string(trade, 'side')
        side = side.lower()
        if side == 'b':
            side = 'buy'
        elif side == 's':
            side = 'sell'
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
        }
        response = await self.publicGetTradesTradingPair(self.extend(request, params))
        return self.parse_trades(response['result'], market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='5m', since=None, limit=None):
        return [
            ohlcv[0],
            ohlcv[2] / 1e8,
            ohlcv[3] / 1e8,
            ohlcv[4] / 1e8,
            ohlcv[5] / 1e8,
            ohlcv[1] / 1e8,
        ]

    async def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'timeSymbol': self.timeframes[timeframe],
        }
        response = await self.publicGetCandlestickTimeSymbolTradingPair(self.extend(request, params))
        return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.traderGetBalances(params)
        #
        #     {
        #         "status": {
        #             "success": 1,
        #             "message": "GET_BALANCES"
        #         },
        #         "result": [
        #             {
        #                 "asset": "ETP",
        #                 "balance": "5000000000000",
        #                 "frozen": "0",
        #                 "state": "1"
        #             },
        #             {
        #                 "asset": "CNY",
        #                 "balance": "10000000000000",
        #                 "frozen": "240790000",
        #                 "state": "1"
        #             }
        #         ]
        #     }
        #
        result = {'info': response}
        balances = response['result']
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['asset']
            code = self.common_currency_code(currencyId)
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            free = self.divide_safe_float(balance, 'balance', 1e8)
            used = self.divide_safe_float(balance, 'frozen', 1e8)
            total = self.sum(free, used)
            #
            # https://github.com/ccxt/ccxt/issues/3873
            #
            #     if total is not None:
            #         if used is not None:
            #             free = total - used
            #         }
            #     }
            #
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[code] = account
        return self.parse_balance(result)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        order = {
            'trading_pair': market['id'],
            # We need to use decimalToPrecision here, since
            #   0.036*1e8 == 3599999.9999999995
            # which would get truncated to 3599999 after int// which would then be rejected by rightBtc because it's too precise
            'quantity': int(self.decimal_to_precision(amount * 1e8, ROUND, 0, self.precisionMode)),
            'limit': int(self.decimal_to_precision(price * 1e8, ROUND, 0, self.precisionMode)),
            'type': type.upper(),
            'side': side.upper(),
        }
        response = await self.traderPostOrder(self.extend(order, params))
        return self.parse_order(response)

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'ids': id,
        }
        response = await self.traderDeleteOrderTradingPairIds(self.extend(request, params))
        return response

    def parse_order_status(self, status):
        statuses = {
            'NEW': 'open',
            'TRADE': 'closed',  # TRADE means filled or partially filled orders
            'CANCEL': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # fetchOrder / fetchOpenOrders
        #
        #     {
        #         "id": 4180528,
        #         "quantity": 20000000,
        #         "rest": 20000000,
        #         "limit": 1000000,
        #         "price": null,
        #         "side": "BUY",
        #         "created": 1496005693738
        #     }
        #
        # fetchOrders
        #
        #     {
        #         "trading_pair": "ETPCNY",
        #         "status": "TRADE",
        #         "fee": 0.23,
        #         "min_fee": 10000000,
        #         "created_at": "2017-05-25T00:12:27.000Z",
        #         "cost": 1152468000000,
        #         "limit": 3600000000,
        #         "id": 11060,
        #         "quantity": 32013000000,
        #         "filled_quantity": 32013000000
        #     }
        #
        id = self.safe_string(order, 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        marketId = self.safe_string(order, 'trading_pair')
        if market is None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = marketId
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'created')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        if 'time' in order:
            timestamp = order['time']
        elif 'transactTime' in order:
            timestamp = order['transactTime']
        price = self.safe_float_2(order, 'limit', 'price')
        if price is not None:
            price = price / 1e8
        amount = self.divide_safe_float(order, 'quantity', 1e8)
        filled = self.divide_safe_float(order, 'filled_quantity', 1e8)
        remaining = self.divide_safe_float(order, 'rest', 1e8)
        cost = self.divide_safe_float(order, 'cost', 1e8)
        # lines 483-494 should be generalized into a base class method
        if amount is not None:
            if remaining is None:
                if filled is not None:
                    remaining = max(0, amount - filled)
            if filled is None:
                if remaining is not None:
                    filled = max(0, amount - remaining)
        type = 'limit'
        side = self.safe_string(order, 'side')
        if side is not None:
            side = side.lower()
        feeCost = self.divide_safe_float(order, 'min_fee', 1e8)
        fee = None
        if feeCost is not None:
            feeCurrency = None
            if market is not None:
                feeCurrency = market['quote']
            fee = {
                'rate': self.safe_float(order, 'fee'),
                'cost': feeCost,
                'currency': feeCurrency,
            }
        trades = None
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'ids': id,
        }
        response = await self.traderGetOrdersTradingPairIds(self.extend(request, params))
        #
        # response = {
        #         "status": {
        #             "success": 1,
        #             "message": "SUC_LIST_AVTICE_ORDERS"
        #         },
        #         "result": [
        #             {
        #                 "id": 4180528,
        #                 "quantity": 20000000,
        #                 "rest": 20000000,
        #                 "limit": 1000000,
        #                 "price": null,
        #                 "side": "BUY",
        #                 "created": 1496005693738
        #             }
        #         ]
        #     }
        #
        orders = self.parse_orders(response['result'], market)
        ordersById = self.index_by(orders, 'id')
        if not(id in list(ordersById.keys())):
            raise OrderNotFound(self.id + ' fetchOrder could not find order ' + str(id) + ' in open orders.')
        return ordersById[id]

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'cursor': 0,
        }
        response = await self.traderGetOrderpageTradingPairCursor(self.extend(request, params))
        #
        # response = {
        #         "status": {
        #             "success": 1,
        #             "message": "SUC_LIST_AVTICE_ORDERS_PAGE"
        #         },
        #         "result": {
        #             "cursor": "0",
        #             "orders": [
        #                 {
        #                     "id": 4180528,
        #                     "quantity": 20000000,
        #                     "rest": 20000000,
        #                     "limit": 1000000,
        #                     "price": null,
        #                     "side": "BUY",
        #                     "created": 1496005693738
        #                 }
        #             ]
        #         }
        #     }
        #
        return self.parse_orders(response['result']['orders'], market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        ids = self.safe_string(params, 'ids')
        if (symbol is None) or (ids is None):
            raise ArgumentsRequired(self.id + " fetchOrders requires a 'symbol' argument and an extra 'ids' parameter. The 'ids' should be an array or a string of one or more order ids separated with slashes.")  # eslint-disable-line quotes
        if isinstance(ids, list):
            ids = '/'.join(ids)
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'ids': ids,
        }
        response = await self.traderGetHistoryTradingPairIds(self.extend(request, params))
        #
        # response = {
        #         "status": {
        #             "success": 1,
        #             "message": null
        #         },
        #         "result": [
        #             {
        #                 "trading_pair": "ETPCNY",
        #                 "status": "TRADE",
        #                 "fee": 0.23,
        #                 "min_fee": 10000000,
        #                 "created_at": "2017-05-25T00:12:27.000Z",
        #                 "cost": 1152468000000,
        #                 "limit": 3600000000,
        #                 "id": 11060,
        #                 "quantity": 32013000000,
        #                 "filled_quantity": 32013000000
        #             }
        #         ]
        #     }
        #
        return self.parse_orders(response['result'], None, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'trading_pair': market['id'],
            'page': 0,
        }
        response = await self.traderGetHistorysTradingPairPage(self.extend(request, params))
        #
        # response = {
        #         "status": {
        #             "success": 1,
        #             "message": null
        #         },
        #         "result": [
        #             {
        #                 "order_id": 118735,
        #                 "trade_id": 7,
        #                 "trading_pair": "BTCCNY",
        #                 "side": "B",
        #                 "quantity": 1000000000,
        #                 "price": 900000000,
        #                 "created_at": "2017-06-06T20:45:27.000Z"
        #             },
        #             {
        #                 "order_id": 118734,
        #                 "trade_id": 7,
        #                 "trading_pair": "BTCCNY",
        #                 "side": "S",
        #                 "quantity": 1000000000,
        #                 "price": 900000000,
        #                 "created_at": "2017-06-06T20:45:27.000Z"
        #             }
        #         ]
        #     }
        #
        return self.parse_trades(response['result'], None, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/' + api + '/' + self.implode_params(path, params)
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            headers = {
                'apikey': self.apiKey,
                'signature': self.secret,
            }
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None:
            return  # fallback to default error handler
        status = self.safe_value(response, 'status')
        if status is not None:
            #
            #     {"status":{"success":0,"message":"ERR_USERTOKEN_NOT_FOUND"}}
            #
            success = self.safe_string(status, 'success')
            if success != '1':
                message = self.safe_string(status, 'message')
                feedback = self.id + ' ' + self.json(response)
                exceptions = self.exceptions
                if message in exceptions:
                    raise exceptions[message](feedback)
                raise ExchangeError(feedback)
