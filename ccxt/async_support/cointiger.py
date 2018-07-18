# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.huobipro import huobipro

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.decimal_to_precision import ROUND
from ccxt.base.decimal_to_precision import TRUNCATE


class cointiger (huobipro):

    def describe(self):
        return self.deep_extend(super(cointiger, self).describe(), {
            'id': 'cointiger',
            'name': 'CoinTiger',
            'countries': ['CN'],
            'hostname': 'api.cointiger.pro',
            'has': {
                'fetchCurrencies': False,
                'fetchTickers': True,
                'fetchTradingLimits': False,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrderTrades': False,  # not tested yet
            },
            'headers': {
                'Language': 'en_US',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/39797261-d58df196-5363-11e8-9880-2ec78ec5bd25.jpg',
                'api': {
                    'public': 'https://api.cointiger.pro/exchange/trading/api/market',
                    'private': 'https://api.cointiger.pro/exchange/trading/api',
                    'exchange': 'https://www.cointiger.pro/exchange',
                    'v2public': 'https://api.cointiger.pro/exchange/trading/api/v2',
                    'v2': 'https://api.cointiger.pro/exchange/trading/api/v2',
                },
                'www': 'https://www.cointiger.pro',
                'referral': 'https://www.cointiger.pro/exchange/register.html?refCode=FfvDtt',
                'doc': 'https://github.com/cointiger/api-docs-en/wiki',
            },
            'api': {
                'v2public': {
                    'get': [
                        'timestamp',
                        'currencys',
                    ],
                },
                'v2': {
                    'get': [
                        'order/orders',
                        'order/match_results',
                        'order/make_detail',
                        'order/details',
                    ],
                    'post': [
                        'order',
                        'order/batchcancel',
                    ],
                },
                'public': {
                    'get': [
                        'history/kline',  # 获取K线数据
                        'detail/merged',  # 获取聚合行情(Ticker)
                        'depth',  # 获取 Market Depth 数据
                        'trade',  # 获取 Trade Detail 数据
                        'history/trade',  # 批量获取最近的交易记录
                        'detail',  # 获取 Market Detail 24小时成交量数据
                    ],
                },
                'exchange': {
                    'get': [
                        'footer/tradingrule.html',
                        'api/public/market/detail',
                    ],
                },
                'private': {
                    'get': [
                        'user/balance',
                        'order/new',
                        'order/history',
                        'order/trade',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete': [
                        'order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.001,
                    'taker': 0.001,
                },
            },
            'exceptions': {
                #    {"code":"1","msg":"系统错误","data":null}
                #    {“code”:“1",“msg”:“Balance insufficient,余额不足“,”data”:null}
                '1': ExchangeError,
                '2': ExchangeError,
                '5': InvalidOrder,
                '6': InvalidOrder,
                '8': OrderNotFound,
                '16': AuthenticationError,  # funding password not set
                '100001': ExchangeError,
                '100002': ExchangeNotAvailable,
                '100003': ExchangeError,
                '100005': AuthenticationError,
            },
        })

    async def fetch_markets(self):
        response = await self.v2publicGetCurrencys()
        #
        #     {
        #         code: '0',
        #         msg: 'suc',
        #         data: {
        #             'bitcny-partition': [
        #                 {
        #                     baseCurrency: 'btc',
        #                     quoteCurrency: 'bitcny',
        #                     pricePrecision: 2,
        #                     amountPrecision: 4,
        #                     withdrawFeeMin: 0.0005,
        #                     withdrawFeeMax: 0.005,
        #                     withdrawOneMin: 0.01,
        #                     withdrawOneMax: 10,
        #                     depthSelect: {step0: '0.01', step1: '0.1', step2: '1'}
        #                 },
        #                 ...
        #             ],
        #             ...
        #         },
        #     }
        #
        keys = list(response['data'].keys())
        result = []
        for i in range(0, len(keys)):
            key = keys[i]
            partition = response['data'][key]
            for j in range(0, len(partition)):
                market = partition[j]
                baseId = self.safe_string(market, 'baseCurrency')
                quoteId = self.safe_string(market, 'quoteCurrency')
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                id = baseId + quoteId
                uppercaseId = id.upper()
                symbol = base + '/' + quote
                precision = {
                    'amount': market['amountPrecision'],
                    'price': market['pricePrecision'],
                }
                active = True
                entry = {
                    'id': id,
                    'uppercaseId': uppercaseId,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'info': market,
                    'active': active,
                    'precision': precision,
                    'limits': {
                        'amount': {
                            'min': math.pow(10, -precision['amount']),
                            'max': None,
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
                }
                result.append(entry)
        self.options['marketsByUppercaseId'] = self.index_by(result, 'uppercaseId')
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'id')
        close = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'percentChange')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24hr'),
            'low': self.safe_float(ticker, 'low24hr'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': None,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'baseVolume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetDepth(self.extend({
            'symbol': market['id'],  # self endpoint requires a lowercase market id
            'type': 'step0',
        }, params))
        data = response['data']['depth_data']
        if 'tick' in data:
            if not data['tick']:
                raise ExchangeError(self.id + ' fetchOrderBook() returned empty response: ' + self.json(response))
            orderbook = data['tick']
            timestamp = data['ts']
            return self.parse_order_book(orderbook, timestamp, 'buys')
        raise ExchangeError(self.id + ' fetchOrderBook() returned unrecognized response: ' + self.json(response))

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['uppercaseId']
        response = await self.exchangeGetApiPublicMarketDetail(params)
        if not(marketId in list(response.keys())):
            raise ExchangeError(self.id + ' fetchTicker symbol ' + symbol + '(' + marketId + ') not found')
        return self.parse_ticker(response[marketId], market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.exchangeGetApiPublicMarketDetail(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = id
            if id in self.options['marketsByUppercaseId']:
                # self endpoint returns uppercase ids
                symbol = self.options['marketsByUppercaseId'][id]['symbol']
                market = self.options['marketsByUppercaseId'][id]
            result[symbol] = self.parse_ticker(response[id], market)
        return result

    def parse_trade(self, trade, market=None):
        #
        #   {     volume: "0.014",
        #          symbol: "ethbtc",
        #         buy_fee: "0.00001400",
        #         orderId:  32235710,
        #           price: "0.06923825",
        #         created:  1531605169000,
        #              id:  3785005,
        #          source:  1,
        #            type: "buy-limit",
        #     bid_user_id:  326317         }]}
        #
        # --------------------------------------------------------------------
        #
        #     {
        #         "volume": {
        #             "amount": "1.000",
        #             "icon": "",
        #             "title": "成交量"
        #                   },
        #         "price": {
        #             "amount": "0.04978883",
        #             "icon": "",
        #             "title": "委托价格"
        #                  },
        #         "created_at": 1513245134000,
        #         "deal_price": {
        #             "amount": 0.04978883000000000000000000000000,
        #             "icon": "",
        #             "title": "成交价格"
        #                       },
        #         "id": 138
        #     }
        #
        id = self.safe_string(trade, 'id')
        orderId = self.safe_string(trade, 'orderId')
        orderType = self.safe_string(trade, 'type')
        type = None
        side = None
        if orderType is not None:
            parts = orderType.split('-')
            side = parts[0]
            type = parts[1]
        side = self.safe_string(trade, 'side', side)
        amount = None
        price = None
        cost = None
        if side is None:
            price = self.safe_float(trade['price'], 'amount')
            amount = self.safe_float(trade['volume'], 'amount')
            cost = self.safe_float(trade['deal_price'], 'amount')
        else:
            side = side.lower()
            price = self.safe_float(trade, 'price')
            amount = self.safe_float_2(trade, 'amount', 'volume')
        fee = None
        if side is not None:
            feeCostField = side + '_fee'
            feeCost = self.safe_float(trade, feeCostField)
            if feeCost is not None:
                feeCurrency = None
                if market is not None:
                    feeCurrency = market['base']
                fee = {
                    'cost': feeCost,
                    'currency': feeCurrency,
                }
        if amount is not None:
            if price is not None:
                if cost is None:
                    cost = amount * price
        timestamp = self.safe_integer_2(trade, 'created_at', 'ts')
        timestamp = self.safe_integer(trade, 'created', timestamp)
        symbol = None
        if market is not None:
            symbol = market['symbol']
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
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=1000, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetHistoryTrade(self.extend(request, params))
        return self.parse_trades(response['data']['trade_data'], market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        response = await self.privateGetOrderTrade(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        return self.parse_trades(response['data']['list'], market, since, limit)

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetHistoryKline(self.extend(request, params))
        return self.parse_ohlcvs(response['data']['kline_data'], market, timeframe, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetUserBalance(params)
        #
        #     {
        #         "code": "0",
        #         "msg": "suc",
        #         "data": [{
        #             "normal": "1813.01144179",
        #             "lock": "1325.42036785",
        #             "coin": "btc"
        #         }, {
        #             "normal": "9551.96692244",
        #             "lock": "547.06506717",
        #             "coin": "eth"
        #         }]
        #     }
        #
        balances = response['data']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            id = balance['coin']
            code = id.upper()
            code = self.common_currency_code(code)
            if id in self.currencies_by_id:
                code = self.currencies_by_id[id]['code']
            account = self.account()
            account['used'] = float(balance['lock'])
            account['free'] = float(balance['normal'])
            account['total'] = self.sum(account['used'], account['free'])
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrderTrades requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = await self.v2GetOrderMakeDetail(self.extend(request, params))
        #
        # the above endpoint often returns an empty array
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: [{     volume: "0.014",
        #                      symbol: "ethbtc",
        #                     buy_fee: "0.00001400",
        #                     orderId:  32235710,
        #                       price: "0.06923825",
        #                     created:  1531605169000,
        #                          id:  3785005,
        #                      source:  1,
        #                        type: "buy-limit",
        #                 bid_user_id:  326317         }]}
        #
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_orders_by_status(self, status=None, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        method = 'privateGetOrderNew' if (status == 'open') else 'privateGetOrderHistory'
        response = await getattr(self, method)(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        orders = response['data']['list']
        result = []
        for i in range(0, len(orders)):
            order = self.extend(orders[i], {
                'status': status,
            })
            result.append(self.parse_order(order, market, since, limit))
        return result

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('open', symbol, since, limit, params)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('closed', symbol, since, limit, params)

    async def fetch_order(self, id, symbol=None, params={}):
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: {     symbol: "ethbtc",
        #                       fee: "0.00000200",
        #                 avg_price: "0.06863752",
        #                    source:  1,
        #                      type: "buy-limit",
        #                     mtime:  1531340305000,
        #                    volume: "0.002",
        #                   user_id:  326317,
        #                     price: "0.06863752",
        #                     ctime:  1531340304000,
        #               deal_volume: "0.00200000",
        #                        id:  31920243,
        #                deal_money: "0.00013727",
        #                    status:  2              }}
        #
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': str(id),
        }
        response = await self.v2GetOrderDetails(self.extend(request, params))
        return self.parse_order(response['data'], market)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',  # pending
            '1': 'open',
            '2': 'closed',
            '3': 'open',
            '4': 'canceled',
            '6': 'error',
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        #
        #  v1
        #
        #      {
        #            volume: {"amount": "0.054", "icon": "", "title": "volume"},
        #         age_price: {"amount": "0.08377697", "icon": "", "title": "Avg price"},
        #              side: "BUY",
        #             price: {"amount": "0.00000000", "icon": "", "title": "price"},
        #        created_at: 1525569480000,
        #       deal_volume: {"amount": "0.64593598", "icon": "", "title": "Deal volume"},
        #   "remain_volume": {"amount": "1.00000000", "icon": "", "title": "尚未成交"
        #                id: 26834207,
        #             label: {go: "trade", title: "Traded", click: 1},
        #          side_msg: "Buy"
        #      },
        #
        #  v2
        #
        #     {code:   "0",
        #        msg:   "suc",
        #       data: {     symbol: "ethbtc",
        #                       fee: "0.00000200",
        #                 avg_price: "0.06863752",
        #                    source:  1,
        #                      type: "buy-limit",
        #                     mtime:  1531340305000,
        #                    volume: "0.002",
        #                   user_id:  326317,
        #                     price: "0.06863752",
        #                     ctime:  1531340304000,
        #               deal_volume: "0.00200000",
        #                        id:  31920243,
        #                deal_money: "0.00013727",
        #                    status:  2              }}
        #
        id = self.safe_string(order, 'id')
        side = self.safe_string(order, 'side')
        type = None
        orderType = self.safe_string(order, 'type')
        status = self.safe_string(order, 'status')
        timestamp = self.safe_integer(order, 'created_at')
        timestamp = self.safe_integer(order, 'ctime', timestamp)
        lastTradeTimestamp = self.safe_integer_2(order, 'mtime', 'finished-at')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'symbol')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        remaining = None
        amount = None
        filled = None
        price = None
        cost = None
        fee = None
        if side is not None:
            side = side.lower()
            amount = self.safe_float(order['volume'], 'amount')
            remaining = self.safe_float(order['remain_volume'], 'amount') if ('remain_volume' in list(order.keys())) else None
            filled = self.safe_float(order['deal_volume'], 'amount') if ('deal_volume' in list(order.keys())) else None
            price = self.safe_float(order['price'], 'amount') if ('price' in list(order.keys())) else None
            if 'age_price' in order:
                average = self.safe_float(order['age_price'], 'amount')
                if (average is not None) and(average > 0):
                    price = average
        else:
            if orderType is not None:
                parts = orderType.split('-')
                side = parts[0]
                type = parts[1]
                cost = self.safe_float(order, 'deal_money')
                price = self.safe_float(order, 'price')
                average = self.safe_float(order, 'avg_price')
                if (average is not None) and(average > 0):
                    price = average
                amount = self.safe_float_2(order, 'amount', 'volume')
                filled = self.safe_float(order, 'deal_volume')
                feeCost = self.safe_float(order, 'fee')
                if feeCost is not None:
                    feeCurrency = None
                    if market is not None:
                        if side == 'buy':
                            feeCurrency = market['base']
                        elif side == 'sell':
                            feeCurrency = market['quote']
                    fee = {
                        'cost': feeCost,
                        'currency': feeCurrency,
                    }
            status = self.parse_order_status(status)
        if amount is not None:
            if remaining is not None:
                if filled is None:
                    filled = max(0, amount - remaining)
            elif filled is not None:
                cost = filled * price
                if remaining is None:
                    remaining = max(0, amount - filled)
        if status is None:
            if (remaining is not None) and(remaining > 0):
                status = 'open'
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': None,
        }
        return result

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, ROUND, self.markets[symbol]['precision']['price'])

    def price_to_precision(self, symbol, price):
        return self.decimal_to_precision(price, ROUND, self.markets[symbol]['precision']['price'])

    def amount_to_precision(self, symbol, amount):
        return self.decimal_to_precision(amount, TRUNCATE, self.markets[symbol]['precision']['amount'])

    def fee_to_precision(self, currency, fee):
        return self.decimal_to_precision(fee, ROUND, self.currencies[currency]['precision'])

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if not self.password:
            raise AuthenticationError(self.id + ' createOrder requires exchange.password to be set to user trading password(not login passwordnot )')
        self.check_required_credentials()
        market = self.market(symbol)
        orderType = 1 if (type == 'limit') else 2
        order = {
            'symbol': market['id'],
            'side': side.upper(),
            'type': orderType,
            'volume': self.amount_to_precision(symbol, amount),
            'capital_password': self.password,
        }
        if (type == 'market') and(side == 'buy'):
            if price is None:
                raise InvalidOrder(self.id + ' createOrder requires price argument for market buy orders to calculate total cost according to exchange rules')
            order['volume'] = self.amount_to_precision(symbol, amount * price)
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        else:
            if price is None:
                order['price'] = self.price_to_precision(symbol, 0)
            else:
                order['price'] = self.price_to_precision(symbol, price)
        response = await self.privatePostOrder(self.extend(order, params))
        #
        #     {"order_id":34343}
        #
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': str(response['data']['order_id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        if symbol is None:
            raise ExchangeError(self.id + ' cancelOrder requires a symbol argument')
        market = self.market(symbol)
        response = await self.privateDeleteOrder(self.extend({
            'symbol': market['id'],
            'order_id': id,
        }, params))
        return {
            'id': id,
            'symbol': symbol,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        self.check_required_credentials()
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        if api == 'private' or api == 'v2':
            timestamp = str(self.milliseconds())
            query = self.keysort(self.extend({
                'time': timestamp,
            }, params))
            keys = list(query.keys())
            auth = ''
            for i in range(0, len(keys)):
                auth += keys[i] + str(query[keys[i]])
            auth += self.secret
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            isCreateOrderMethod = (path == 'order') and(method == 'POST')
            urlParams = {} if isCreateOrderMethod else query
            url += '?' + self.urlencode(self.keysort(self.extend({
                'api_key': self.apiKey,
                'time': timestamp,
            }, urlParams)))
            url += '&sign=' + signature
            if method == 'POST':
                body = self.urlencode(query)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        elif api == 'public' or api == 'v2public':
            url += '?' + self.urlencode(self.extend({
                'api_key': self.apiKey,
            }, params))
        else:
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            if 'code' in response:
                #
                #     {"code": "100005", "msg": "request sign illegal", "data": null}
                #
                code = self.safe_string(response, 'code')
                if (code is not None) and(code != '0'):
                    message = self.safe_string(response, 'msg')
                    feedback = self.id + ' ' + self.json(response)
                    exceptions = self.exceptions
                    if code in exceptions:
                        if code == 1:
                            #    {"code":"1","msg":"系统错误","data":null}
                            #    {“code”:“1",“msg”:“Balance insufficient,余额不足“,”data”:null}
                            if message.find('Balance insufficient') >= 0:
                                raise InsufficientFunds(feedback)
                        elif code == 2:
                            if message == 'offsetNot Null':
                                raise ExchangeError(feedback)
                            elif message == 'Parameter error':
                                raise ExchangeError(feedback)
                        raise exceptions[code](feedback)
                    else:
                        raise ExchangeError(self.id + ' unknown "error" value: ' + self.json(response))
