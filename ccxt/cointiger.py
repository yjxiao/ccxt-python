# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.huobipro import huobipro

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import ExchangeNotAvailable


class cointiger (huobipro):

    def describe(self):
        return self.deep_extend(super(cointiger, self).describe(), {
            'id': 'cointiger',
            'name': 'CoinTiger',
            'countries': 'CN',
            'hostname': 'api.cointiger.com',
            'has': {
                'fetchCurrencies': False,
                'fetchTickers': True,
                'fetchOrder': False,
            },
            'headers': {
                'Language': 'en_US',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/39797261-d58df196-5363-11e8-9880-2ec78ec5bd25.jpg',
                'api': {
                    'public': 'https://api.cointiger.com/exchange/trading/api/market',
                    'private': 'https://api.cointiger.com/exchange/trading/api',
                    'exchange': 'https://www.cointiger.com/exchange',
                },
                'www': 'https://www.cointiger.com',
                'referral': 'https://www.cointiger.com/exchange/register.html?refCode=FfvDtt',
                'doc': 'https://github.com/cointiger/api-docs-en/wiki',
            },
            'api': {
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
            'exceptions': {
                '1': InsufficientFunds,
                '2': ExchangeError,
                '5': InvalidOrder,
                '16': AuthenticationError,  # funding password not set
                '100001': ExchangeError,
                '100002': ExchangeNotAvailable,
                '100003': ExchangeError,
                '100005': AuthenticationError,
            },
        })

    def fetch_markets(self):
        self.parseJsonResponse = False
        response = self.exchangeGetFooterTradingruleHtml()
        self.parseJsonResponse = True
        rows = response.split('<tr>')
        numRows = len(rows)
        limit = numRows - 1
        result = []
        for i in range(1, limit):
            row = rows[i]
            parts = row.split('<span style="color:#ffffff">')
            numParts = len(parts)
            if (numParts < 6) or (parts[1].find('Kind&nbsp') >= 0):
                continue
            id = parts[1].split('</span>')[0]
            minAmount = parts[2].split('</span>')[0]
            minPrice = parts[4].split('</span>')[0]
            precision = {
                'amount': self.precision_from_string(minAmount),
                'price': self.precision_from_string(minPrice),
            }
            id = id.split('&nbsp')[0]
            baseId, quoteId = id.split('/')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            baseId = baseId.lower()
            quoteId = quoteId.lower()
            id = baseId + quoteId
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'uppercaseId': id.upper(),
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'taker': 0.001,
                'maker': 0.001,
                'limits': {
                    'amount': {
                        'min': float(minAmount),
                        'max': None,
                    },
                    'price': {
                        'min': float(minPrice),
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
                'info': None,
            })
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

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetDepth(self.extend({
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

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        response = self.exchangeGetApiPublicMarketDetail(params)
        if not(marketId in list(response.keys())):
            raise ExchangeError(self.id + ' fetchTicker symbol ' + symbol + '(' + marketId + ') not found')
        return self.parse_ticker(response[marketId], market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.exchangeGetApiPublicMarketDetail(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = id
            if id in self.options['marketsByUppercaseId']:
                # self endpoint returns uppercase ids
                symbol = self.options['marketsByUppercaseId'][id]['symbol']
            result[symbol] = self.parse_ticker(response[id], market)
        return result

    def parse_trade(self, trade, market=None):
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
        side = self.safe_string(trade, 'side')
        amount = None
        price = None
        cost = None
        if side is not None:
            side = side.lower()
            price = self.safe_float(trade, 'price')
            amount = self.safe_float(trade, 'amount')
        else:
            price = self.safe_float(trade['price'], 'amount')
            amount = self.safe_float(trade['volume'], 'amount')
            cost = self.safe_float(trade['deal_price'], 'amount')
        if amount is not None:
            if price is not None:
                if cost is None:
                    cost = amount * price
        timestamp = self.safe_value(trade, 'created_at')
        if timestamp is None:
            timestamp = self.safe_value(trade, 'ts')
        iso8601 = self.iso8601(timestamp) if (timestamp is not None) else None
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': str(trade['id']),
            'order': None,
            'timestamp': timestamp,
            'datetime': iso8601,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = self.publicGetHistoryTrade(self.extend(request, params))
        return self.parse_trades(response['data']['trade_data'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        response = self.privateGetOrderTrade(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        return self.parse_trades(response['data']['list'], market, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        if limit is not None:
            request['size'] = limit
        response = self.publicGetHistoryKline(self.extend(request, params))
        return self.parse_ohlcvs(response['data']['kline_data'], market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserBalance(params)
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
            account['free'] = balance['normal']
            account['total'] = self.sum(account['used'], account['free'])
            result[code] = account
        return self.parse_balance(result)

    def fetch_orders_by_status(self, status=None, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        method = 'privateGetOrderNew' if (status == 'open') else 'privateGetOrderHistory'
        response = getattr(self, method)(self.extend({
            'symbol': market['id'],
            'offset': 1,
            'limit': limit,
        }, params))
        return self.parse_orders(response['data']['list'], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('open', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('closed', symbol, since, limit, params)

    def parse_order(self, order, market=None):
        side = self.safe_string(order, 'side')
        side = side.lower()
        #
        #      {
        #            volume: {"amount": "0.054", "icon": "", "title": "volume"},
        #         age_price: {"amount": "0.08377697", "icon": "", "title": "Avg price"},
        #              side:   "BUY",
        #             price: {"amount": "0.00000000", "icon": "", "title": "price"},
        #        created_at:   1525569480000,
        #       deal_volume: {"amount": "0.64593598", "icon": "", "title": "Deal volume"},
        #   "remain_volume": {"amount": "1.00000000", "icon": "", "title": "尚未成交"
        #                id:   26834207,
        #             label: {go: "trade", title: "Traded", click: 1},
        #          side_msg:   "Buy"
        #      },
        #
        type = None
        status = None
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = order['created_at']
        amount = self.safe_float(order['volume'], 'amount')
        remaining = self.safe_float(order['remain_volume'], 'amount') if ('remain_volume' in list(order.keys())) else None
        filled = self.safe_float(order['deal_volume'], 'amount') if ('deal_volume' in list(order.keys())) else None
        price = self.safe_float(order['age_price'], 'amount') if ('age_price' in list(order.keys())) else None
        if price is None:
            price = self.safe_float(order['price'], 'amount') if ('price' in list(order.keys())) else None
        cost = None
        average = None
        if amount is not None:
            if remaining is not None:
                if filled is None:
                    filled = amount - remaining
            elif filled is not None:
                cost = filled * price
                average = float(cost / filled)
                if remaining is None:
                    remaining = amount - filled
        if (remaining is not None) and(remaining > 0):
            status = 'open'
        result = {
            'info': order,
            'id': str(order['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
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
        response = self.privatePostOrder(self.extend(order, params))
        #
        #     {"order_id":34343}
        #
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': str(response['order_id']),
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

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        if symbol is None:
            raise ExchangeError(self.id + ' cancelOrder requires a symbol argument')
        market = self.market(symbol)
        return self.privateDeleteOrder(self.extend({
            'symbol': market['id'],
            'order_id': id,
        }, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        self.check_required_credentials()
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        if api == 'private':
            timestamp = str(self.milliseconds())
            query = self.keysort(self.extend({
                'time': timestamp,
            }, params))
            keys = list(query.keys())
            auth = ''
            for i in range(0, len(keys)):
                auth += keys[i] + query[keys[i]]
            auth += self.secret
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            isCreateOrderMethod = (path == 'order') and(method == 'POST')
            urlParams = {} if isCreateOrderMethod else query
            url += '?' + self.urlencode(self.keysort(self.extend({
                'api_key': self.apiKey,
                'time': timestamp,
            }, urlParams)))
            url += '&sign=' + self.decode(signature)
            if method == 'POST':
                body = self.urlencode(query)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        elif api == 'public':
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
                #     {"code":"100005","msg":"request sign illegal","data":null}
                #
                code = self.safe_string(response, 'code')
                if (code is not None) and(code != '0'):
                    message = self.safe_string(response, 'msg')
                    feedback = self.id + ' ' + self.json(response)
                    exceptions = self.exceptions
                    if code in exceptions:
                        if code == 2:
                            if message == 'offsetNot Null':
                                raise ExchangeError(feedback)
                            elif message == 'Parameter error':
                                raise ExchangeError(feedback)
                        raise exceptions[code](feedback)
                    else:
                        raise ExchangeError(self.id + ' unknown "error" value: ' + self.json(response))
