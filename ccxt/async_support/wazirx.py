# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.precise import Precise


class wazirx(Exchange):

    def describe(self):
        return self.deep_extend(super(wazirx, self).describe(), {
            'id': 'wazirx',
            'name': 'WazirX',
            'countries': ['IN'],
            'version': 'v2',
            'rateLimit': 100,
            'has': {
                'CORS': False,
                'spot': True,
                'margin': None,  # has but unimplemented
                'swap': False,
                'future': False,
                'option': False,
                'cancelAllOrders': True,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchBidsAsks': False,
                'fetchClosedOrders': False,
                'fetchCurrencies': False,
                'fetchDepositAddress': False,
                'fetchDepositAddressesByNetwork': False,
                'fetchDeposits': True,
                'fetchFundingFees': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': False,
                'fetchOHLCV': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPremiumIndexOHLCV': False,
                'fetchStatus': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'fetchTransactions': False,
                'fetchTransfers': False,
                'fetchWithdrawals': False,
                'transfer': False,
                'withdraw': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/148647666-c109c20b-f8ac-472f-91c3-5f658cb90f49.jpeg',
                'api': 'https://api.wazirx.com/sapi/v1',
                'www': 'https://wazirx.com',
                'doc': 'https://docs.wazirx.com/#public-rest-api-for-wazirx',
                'fees': 'https://wazirx.com/fees',
                'referral': 'https://wazirx.com/invite/k7rrnks5',
            },
            'api': {
                'public': {
                    'get': {
                        'exchangeInfo': 1,
                        'depth': 1,
                        'ping': 1,
                        'systemStatus': 1,
                        'tickers/24hr': 1,
                        'ticker/24hr': 1,
                        'time': 1,
                        'trades': 1,
                    },
                },
                'private': {
                    'get': {
                        'account': 1,
                        'allOrders': 1,
                        'funds': 1,
                        'historicalTrades': 1,
                        'openOrders': 1,
                        'order': 1,
                        'myTrades': 1,
                    },
                    'post': {
                        'order': 1,
                        'order/test': 1,
                    },
                    'delete': {
                        'order': 1,
                        'openOrders': 1,
                    },
                },
            },
            'fees': {
                'WRX': {'maker': self.parse_number('0.0'), 'taker': self.parse_number('0.0')},
            },
            'exceptions': {
                'exact': {
                    '-1121': BadSymbol,  # {"code": -1121, "message": "Invalid symbol."}
                    '1999': BadRequest,  # {"code":1999,"message":"symbol is missing, symbol does not have a valid value"} message varies depending on the error
                    '2002': InsufficientFunds,  # {"code":2002,"message":"Not enough USDT balance to execute self order"}
                    '2005': BadRequest,  # {"code":2005,"message":"Signature is incorrect."}
                    '2078': PermissionDenied,  # {"code":2078,"message":"Permission denied."}
                    '2098': BadRequest,  # {"code":2098,"message":"Request out of receiving window."}
                    '2031': InvalidOrder,  # {"code":2031,"message":"Minimum buy amount must be worth 2.0 USDT"}
                    '2113': BadRequest,  # {"code":2113,"message":"RecvWindow must be in range 1..60000"}
                    '2115': BadRequest,  # {"code":2115,"message":"Signature not found."}
                    '2136': RateLimitExceeded,  # {"code":2136,"message":"Too many api request"}
                    '94001': InvalidOrder,  # {"code":94001,"message":"Stop price not found."}
                },
            },
            'options': {
                # 'fetchTradesMethod': 'privateGetHistoricalTrades',
                'recvWindow': 10000,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetExchangeInfo(params)
        #
        # {
        #     "timezone":"UTC",
        #     "serverTime":1641336850932,
        #     "symbols":[
        #     {
        #         "symbol":"btcinr",
        #         "status":"trading",
        #         "baseAsset":"btc",
        #         "quoteAsset":"inr",
        #         "baseAssetPrecision":5,
        #         "quoteAssetPrecision":0,
        #         "orderTypes":[
        #             "limit",
        #             "stop_limit"
        #         ],
        #         "isSpotTradingAllowed":true,
        #         "filters":[
        #             {
        #                 "filterType":"PRICE_FILTER",
        #                 "minPrice":"1",
        #                 "tickSize":"1"
        #             }
        #         ]
        #     },
        #
        markets = self.safe_value(response, 'symbols', [])
        result = []
        for i in range(0, len(markets)):
            entry = markets[i]
            id = self.safe_string(entry, 'symbol')
            baseId = self.safe_string(entry, 'baseAsset')
            quoteId = self.safe_string(entry, 'quoteAsset')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            isSpot = self.safe_value(entry, 'isSpotTradingAllowed')
            filters = self.safe_value(entry, 'filters')
            minPrice = None
            for j in range(0, len(filters)):
                filter = filters[j]
                filterType = self.safe_string(filter, 'filterType')
                if filterType == 'PRICE_FILTER':
                    minPrice = self.safe_number(filter, 'minPrice')
            fee = self.safe_value(self.fees, quote, {})
            takerString = self.safe_string(fee, 'taker', '0.2')
            takerString = Precise.string_div(takerString, '100')
            makerString = self.safe_string(fee, 'maker', '0.2')
            makerString = Precise.string_div(makerString, '100')
            status = self.safe_string(entry, 'status')
            result.append({
                'id': id,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': isSpot,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': (status == 'trading'),
                'contract': False,
                'linear': None,
                'inverse': None,
                'taker': self.parse_number(takerString),
                'maker': self.parse_number(makerString),
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.safe_integer(entry, 'baseAssetPrecision'),
                    'price': self.safe_integer(entry, 'quoteAssetPrecision'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': minPrice,
                        'max': None,
                    },
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': entry,
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # [1, 5, 10, 20, 50, 100, 500, 1000]
        response = await self.publicGetDepth(self.extend(request, params))
        #
        #     {
        #          "timestamp":1559561187,
        #          "asks":[
        #                     ["8540.0","1.5"],
        #                     ["8541.0","0.0042"]
        #                 ],
        #          "bids":[
        #                     ["8530.0","0.8814"],
        #                     ["8524.0","1.4"]
        #                 ]
        #      }
        #
        timestamp = self.safe_integer(response, 'timestamp')
        return self.parse_order_book(response, symbol, timestamp)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        ticker = await self.publicGetTicker24hr(self.extend(request, params))
        #
        # {
        #     "symbol":"wrxinr",
        #     "baseAsset":"wrx",
        #     "quoteAsset":"inr",
        #     "openPrice":"94.77",
        #     "lowPrice":"92.7",
        #     "highPrice":"95.17",
        #     "lastPrice":"94.03",
        #     "volume":"1118700.0",
        #     "bidPrice":"94.02",
        #     "askPrice":"94.03",
        #     "at":1641382455000
        # }
        #
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers24hr()
        #
        # [
        #     {
        #        "symbol":"btcinr",
        #        "baseAsset":"btc",
        #        "quoteAsset":"inr",
        #        "openPrice":"3698486",
        #        "lowPrice":"3641155.0",
        #        "highPrice":"3767999.0",
        #        "lastPrice":"3713212.0",
        #        "volume":"254.11582",
        #        "bidPrice":"3715021.0",
        #        "askPrice":"3715022.0",
        #     }
        #     ...
        # ]
        #
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            parsedTicker = self.parse_ticker(ticker)
            symbol = parsedTicker['symbol']
            result[symbol] = parsedTicker
        return result

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # Default 500; max 1000.
        method = self.safe_string(self.options, 'fetchTradesMethod', 'publicGetTrades')
        response = await getattr(self, method)(self.extend(request, params))
        # [
        #     {
        #         "id":322307791,
        #         "price":"93.7",
        #         "qty":"0.7",
        #         "quoteQty":"65.59",
        #         "time":1641386701000,
        #         "isBuyerMaker":false
        #     },
        # ]
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        #     {
        #         "id":322307791,
        #         "price":"93.7",
        #         "qty":"0.7",
        #         "quoteQty":"65.59",
        #         "time":1641386701000,
        #         "isBuyerMaker":false
        #     }
        #
        id = self.safe_string(trade, 'id')
        timestamp = self.parse8601(self.safe_string(trade, 'time'))
        datetime = self.iso8601(timestamp)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        isBuyerMaker = self.safe_value(trade, 'isBuyerMaker')
        side = 'sell' if isBuyerMaker else 'buy'
        price = self.safe_number(trade, 'price')
        amount = self.safe_number(trade, 'qty')
        cost = self.safe_number(trade, 'quoteQty')
        return self.safe_trade({
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': datetime,
            'symbol': symbol,
            'order': id,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        })

    async def fetch_status(self, params={}):
        response = await self.publicGetSystemStatus(params)
        #
        #  {"status":"normal","message":"System is running normally."}
        #
        status = self.safe_string(response, 'status')
        status = 'ok' if (status == 'normal') else 'maintenance'
        self.status = self.extend(self.status, {
            'status': status,
            'updated': self.milliseconds(),
        })
        return self.status

    async def fetch_time(self, params={}):
        response = await self.publicGetTime(params)
        #
        #     {
        #         "serverTime":1635467280514
        #     }
        #
        return self.safe_integer(response, 'serverTime')

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #        "symbol":"btcinr",
        #        "baseAsset":"btc",
        #        "quoteAsset":"inr",
        #        "openPrice":"3698486",
        #        "lowPrice":"3641155.0",
        #        "highPrice":"3767999.0",
        #        "lastPrice":"3713212.0",
        #        "volume":"254.11582",  # base volume
        #        "bidPrice":"3715021.0",
        #        "askPrice":"3715022.0",
        #        "at":1641382455000  # only on fetchTicker
        #     }
        #
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        last = self.safe_string(ticker, 'lastPrice')
        open = self.safe_string(ticker, 'openPrice')
        high = self.safe_string(ticker, 'highPrice')
        low = self.safe_string(ticker, 'lowPrice')
        baseVolume = self.safe_string(ticker, 'volume')
        bid = self.safe_string(ticker, 'bidPrice')
        ask = self.safe_string(ticker, 'askPrice')
        timestamp = self.safe_string(ticker, 'at')
        return self.safe_ticker({
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
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }, market, False)

    def parse_balance(self, response):
        result = {}
        for i in range(0, len(response)):
            balance = response[i]
            id = self.safe_string(balance, 'asset')
            code = self.safe_currency_code(id)
            account = self.account()
            account['free'] = self.safe_string(balance, 'free')
            account['used'] = self.safe_string(balance, 'locked')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetFunds(params)
        #
        # [
        #       {
        #          "asset":"inr",
        #          "free":"0.0",
        #          "locked":"0.0"
        #       },
        # ]
        #
        return self.parse_balance(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetAllOrders(self.extend(request, params))
        # [
        #     {
        #         "id": 28,
        #         "symbol": "wrxinr",
        #         "price": "9293.0",
        #         "origQty": "10.0",
        #         "executedQty": "8.2",
        #         "status": "cancel",
        #         "type": "limit",
        #         "side": "sell",
        #         "createdTime": 1499827319559,
        #         "updatedTime": 1499827319559
        #     },
        #     {
        #         "id": 30,
        #         "symbol": "wrxinr",
        #         "price": "9293.0",
        #         "stopPrice": "9200.0",
        #         "origQty": "10.0",
        #         "executedQty": "0.0",
        #         "status": "cancel",
        #         "type": "stop_limit",
        #         "side": "sell",
        #         "createdTime": 1499827319559,
        #         "updatedTime": 1507725176595
        #     }
        # ]
        orders = self.parse_orders(response, market, since, limit)
        orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = await self.privateGetOpenOrders(self.extend(request, params))
        # [
        #     {
        #         "id": 28,
        #         "symbol": "wrxinr",
        #         "price": "9293.0",
        #         "origQty": "10.0",
        #         "executedQty": "8.2",
        #         "status": "cancel",
        #         "type": "limit",
        #         "side": "sell",
        #         "createdTime": 1499827319559,
        #         "updatedTime": 1499827319559
        #     },
        #     {
        #         "id": 30,
        #         "symbol": "wrxinr",
        #         "price": "9293.0",
        #         "stopPrice": "9200.0",
        #         "origQty": "10.0",
        #         "executedQty": "0.0",
        #         "status": "cancel",
        #         "type": "stop_limit",
        #         "side": "sell",
        #         "createdTime": 1499827319559,
        #         "updatedTime": 1507725176595
        #     }
        # ]
        orders = self.parse_orders(response, market, since, limit)
        return orders

    async def cancel_all_orders(self, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelAllOrders requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        return await self.privateDeleteOpenOrders(self.extend(request, params))

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'orderId': id,
        }
        response = await self.privateDeleteOrder(self.extend(request, params))
        return self.parse_order(response)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if not (type == 'limit') or (type == 'stop_limit'):
            raise ExchangeError(self.id + ' createOrder() supports limit and stop_limit orders only')
        if price is None:
            raise ExchangeError(self.id + ' createOrder() requires a price argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'side': side,
            'quantity': amount,
            'type': 'limit',
        }
        request['price'] = self.price_to_precision(symbol, price)
        stopPrice = self.safe_string(params, 'stopPrice')
        if stopPrice is not None:
            request['type'] = 'stop_limit'
        response = await self.privatePostOrder(self.extend(request, params))
        # {
        #     "id": 28,
        #     "symbol": "wrxinr",
        #     "price": "9293.0",
        #     "origQty": "10.0",
        #     "executedQty": "8.2",
        #     "status": "wait",
        #     "type": "limit",
        #     "side": "sell",
        #     "createdTime": 1499827319559,
        #     "updatedTime": 1499827319559
        # }
        return self.parse_order(response, market)

    def parse_order(self, order, market=None):
        # {
        #     "id":1949417813,
        #     "symbol":"ltcusdt",
        #     "type":"limit",
        #     "side":"sell",
        #     "status":"done",
        #     "price":"146.2",
        #     "origQty":"0.05",
        #     "executedQty":"0.05",
        #     "createdTime":1641252564000,
        #     "updatedTime":1641252564000
        # },
        created = self.safe_integer(order, 'createdTime')
        updated = self.safe_integer(order, 'updatedTime')
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        amount = self.safe_string(order, 'quantity')
        filled = self.safe_string(order, 'executedQty')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'id')
        price = self.safe_string(order, 'price')
        type = self.safe_string_lower(order, 'type')
        side = self.safe_string_lower(order, 'side')
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': created,
            'datetime': self.iso8601(created),
            'lastTradeTimestamp': updated,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'cost': None,
            'fee': None,
            'average': None,
            'trades': [],
        }, market)

    def parse_order_status(self, status):
        statuses = {
            'wait': 'open',
            'done': 'closed',
            'cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        if api == 'private':
            self.check_required_credentials()
            timestamp = self.milliseconds()
            data = self.extend({'recvWindow': self.options['recvWindow'], 'timestamp': timestamp}, params)
            data = self.keysort(data)
            signature = self.hmac(self.encode(self.urlencode(data)), self.encode(self.secret), hashlib.sha256)
            url += '?' + self.urlencode(data)
            url += '&signature=' + signature
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Api-Key': self.apiKey,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        #
        # {"code":2098,"message":"Request out of receiving window."}
        #
        if response is None:
            return
        errorCode = self.safe_string(response, 'code')
        if errorCode is not None:
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
            raise ExchangeError(feedback)
