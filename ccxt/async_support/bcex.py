# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class bcex (Exchange):

    def describe(self):
        return self.deep_extend(super(bcex, self).describe(), {
            'id': 'bcex',
            'name': 'BCEX',
            'countries': ['CN', 'CA'],
            'version': '1',
            'has': {
                'fetchBalance': True,
                'fetchMarkets': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchTrades': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/43362240-21c26622-92ee-11e8-9464-5801ec526d77.jpg',
                'api': 'https://www.bcex.top',
                'www': 'https://www.bcex.top',
                'doc': 'https://www.bcex.top/api_market/market/',
                'fees': 'http://bcex.udesk.cn/hc/articles/57085',
                'referral': 'https://www.bcex.top/user/reg/type/2/pid/758978',
            },
            'api': {
                'public': {
                    'get': [
                        'Api_Market/getPriceList',  # tickers
                        'Api_Order/ticker',  # last ohlcv candle(ticker)
                        'Api_Order/depth',  # orderbook
                        'Api_Market/getCoinTrade',  # ticker
                        'Api_Order/marketOrder',  # trades...
                    ],
                    'post': [
                        'Api_Market/getPriceList',  # tickers
                        'Api_Order/ticker',  # last ohlcv candle(ticker)
                        'Api_Order/depth',  # orderbook
                        'Api_Market/getCoinTrade',  # ticker
                        'Api_Order/marketOrder',  # trades...
                    ],
                },
                'private': {
                    'post': [
                        'Api_Order/cancel',
                        'Api_Order/coinTrust',  # limit order
                        'Api_Order/orderList',  # open / all orders(my trades?)
                        'Api_Order/orderInfo',
                        'Api_Order/tradeList',  # open / all orders
                        'Api_Order/trustList',  # ?
                        'Api_User/userBalance',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'bid': 0.0,
                    'ask': 0.02 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'ckusd': 0.0,
                        'other': 0.05 / 100,
                    },
                    'deposit': {},
                },
                'exceptions': {
                    '该币不存在,非法操作': ExchangeError,  # {code: 1, msg: "该币不存在,非法操作"} - returned when a required symbol parameter is missing in the request(also, maybe on other types of errors as well)
                    '公钥不合法': AuthenticationError,  # {code: 1, msg: '公钥不合法'} - wrong public key
                },
            },
        })

    async def fetch_markets(self):
        response = await self.publicGetApiMarketGetPriceList()
        result = []
        keys = list(response.keys())
        for i in range(0, len(keys)):
            currentMarketId = keys[i]
            currentMarkets = response[currentMarketId]
            for j in range(0, len(currentMarkets)):
                market = currentMarkets[j]
                baseId = market['coin_from']
                quoteId = market['coin_to']
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                id = baseId + '2' + quoteId
                symbol = base + '/' + quote
                active = True
                precision = {
                    'amount': None,  # todo: might need self for proper order placement
                    'price': None,  # todo: find a way to get these values
                }
                limits = {
                    'amount': {
                        'min': None,  # todo
                        'max': None,
                    },
                    'price': {
                        'min': None,  # todo
                        'max': None,
                    },
                    'cost': {
                        'min': None,  # todo
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
                    'active': active,
                    'precision': precision,
                    'limits': limits,
                    'info': market,
                })
        return result

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer_2(trade, 'date', 'created')
        if timestamp is not None:
            timestamp = timestamp * 1000
        id = self.safe_string(trade, 'tid')
        orderId = self.safe_string(trade, 'order_id')
        amount = self.safe_float_2(trade, 'number', 'amount')
        price = self.safe_float(trade, 'price')
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        side = self.safe_string(trade, 'type')
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'order': orderId,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['limit'] = limit
        market = self.market(symbol)
        response = await self.publicPostApiOrderMarketOrder(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostApiUserUserBalance(params)
        data = response['data']
        keys = list(data.keys())
        result = {}
        for i in range(0, len(keys)):
            key = keys[i]
            amount = self.safe_float(data, key)
            parts = key.split('_')
            currencyId = parts[0]
            lockOrOver = parts[1]
            code = currencyId.upper()
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            else:
                code = self.common_currency_code(code)
            if not(code in list(result.keys())):
                account = self.account()
                result[code] = account
            if lockOrOver == 'lock':
                result[code]['used'] = float(amount)
            else:
                result[code]['free'] = float(amount)
        keys = list(result.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            total = self.sum(result[key]['used'], result[key]['total'])
            result[key]['total'] = total
        result['info'] = data
        return self.parse_balance(result)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        request = {
            'part': market['quoteId'],
            'coin': market['baseId'],
        }
        response = await self.publicPostApiMarketGetCoinTrade(self.extend(request, params))
        timestamp = self.milliseconds()
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(response, 'max'),
            'low': self.safe_float(response, 'min'),
            'bid': self.safe_float(response, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(response, 'sale'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': self.safe_float(response, 'price'),
            'last': self.safe_float(response, 'price'),
            'previousClose': None,
            'change': None,
            'percentage': self.safe_float(response, 'change_24h'),
            'average': None,
            'baseVolume': self.safe_float(response, 'volume_24h'),
            'quoteVolume': None,
            'info': response,
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        marketId = self.market_id(symbol)
        request = {
            'symbol': marketId,
        }
        response = await self.publicPostApiOrderDepth(self.extend(request, params))
        data = response['data']
        orderbook = self.parse_order_book(data, data['date'] * 1000)
        return orderbook

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.privatePostApiOrderOrderList(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'open',  # partially filled
            '2': 'closed',
            '3': 'canceled',
        }
        if status in statuses:
            return statuses[status]
        return status

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            'trust_id': id,
        }
        response = await self.privatePostApiOrderOrderInfo(self.extend(request, params))
        order = response['data']
        timestamp = order['created'] * 1000
        status = self.parseStatus(order['status'])
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': order['flag'],
            'side': None,
            'price': order['price'],
            'cost': None,
            'average': None,
            'amount': order['number'],
            'filled': order['numberdeal'],
            'remaining': order['numberover'],
            'status': status,
            'fee': None,
        }
        return result

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = order['datetime'] * 1000
        iso8601 = self.iso8601(timestamp)
        symbol = market['symbol']
        type = None
        side = order['type']
        price = order['price']
        average = order['avg_price']
        amount = order['amount']
        remaining = order['amount_outstanding']
        filled = amount - remaining
        status = self.safe_string(order, 'status')
        status = self.parse_order_status(status)
        cost = filled * price
        fee = None
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': iso8601,
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }
        return result

    async def fetch_orders_by_type(self, type, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'type': type,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = await self.privatePostApiOrderTradeList(self.extend(request, params))
        if 'data' in response:
            return self.parse_orders(response['data'], market, since, limit)
        return []

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_type('open', symbol, since, limit, params)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_type('all', symbol, since, limit, params)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        order = {
            'symbol': self.market_id(symbol),
            'type': side,
            'price': price,
            'number': amount,
        }
        response = await self.privatePostApiOrderCoinTrust(self.extend(order, params))
        data = response['data']
        return {
            'info': response,
            'id': self.safe_string(data, 'order_id'),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {}
        if symbol is not None:
            request['symbol'] = symbol
        if id is not None:
            request['order_id'] = id
        results = await self.privatePostApiOrderCancel(self.extend(request, params))
        return results

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            payload = self.urlencode({'api_key': self.apiKey})
            if query:
                payload += self.urlencode(self.keysort(query))
            auth = payload + '&secret_key=' + self.secret
            signature = self.hash(self.encode(auth))
            body = payload + '&sign=' + signature
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            feedback = self.id + ' ' + body
            code = self.safe_value(response, 'code')
            if code is not None:
                if code != 0:
                    #
                    # {code: 1, msg: "该币不存在,非法操作"} - returned when a required symbol parameter is missing in the request(also, maybe on other types of errors as well)
                    # {code: 1, msg: '公钥不合法'} - wrong public key
                    #
                    message = self.safe_string(response, 'msg')
                    exceptions = self.exceptions
                    if message in exceptions:
                        raise exceptions[message](feedback)
                    else:
                        raise ExchangeError(feedback)
