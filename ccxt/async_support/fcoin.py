# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import base64
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce


class fcoin (Exchange):

    def describe(self):
        return self.deep_extend(super(fcoin, self).describe(), {
            'id': 'fcoin',
            'name': 'FCoin',
            'countries': ['CN'],
            'rateLimit': 2000,
            'userAgent': self.userAgents['chrome39'],
            'version': 'v2',
            'accounts': None,
            'accountsById': None,
            'hostname': 'api.fcoin.com',
            'has': {
                'CORS': False,
                'fetchDepositAddress': False,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': False,
                'fetchTradingLimits': False,
                'withdraw': False,
                'fetchCurrencies': False,
            },
            'timeframes': {
                '1m': 'M1',
                '3m': 'M3',
                '5m': 'M5',
                '15m': 'M15',
                '30m': 'M30',
                '1h': 'H1',
                '1d': 'D1',
                '1w': 'W1',
                '1M': 'MN',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/42244210-c8c42e1e-7f1c-11e8-8710-a5fb63b165c4.jpg',
                'api': 'https://api.fcoin.com',
                'www': 'https://www.fcoin.com',
                'referral': 'https://www.fcoin.com/i/Z5P7V',
                'doc': 'https://developer.fcoin.com',
                'fees': 'https://support.fcoin.com/hc/en-us/articles/360003715514-Trading-Rules',
            },
            'api': {
                'market': {
                    'get': [
                        'ticker/{symbol}',
                        'depth/{level}/{symbol}',
                        'trades/{symbol}',
                        'candles/{timeframe}/{symbol}',
                    ],
                },
                'public': {
                    'get': [
                        'symbols',
                        'currencies',
                        'server-time',
                    ],
                },
                'private': {
                    'get': [
                        'accounts/balance',
                        'orders',
                        'orders/{order_id}',
                        'orders/{order_id}/match-results',  # check order result
                    ],
                    'post': [
                        'orders',
                        'orders/{order_id}/submit-cancel',  # cancel order
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
            'limits': {
                'amount': {'min': 0.01, 'max': 100000},
            },
            'options': {
                'createMarketBuyOrderRequiresPrice': True,
                'limits': {
                    'BTM/USDT': {'amount': {'min': 0.1, 'max': 10000000}},
                    'ETC/USDT': {'amount': {'min': 0.001, 'max': 400000}},
                    'ETH/USDT': {'amount': {'min': 0.001, 'max': 10000}},
                    'LTC/USDT': {'amount': {'min': 0.001, 'max': 40000}},
                    'BCH/USDT': {'amount': {'min': 0.001, 'max': 5000}},
                    'BTC/USDT': {'amount': {'min': 0.001, 'max': 1000}},
                    'ICX/ETH': {'amount': {'min': 0.01, 'max': 3000000}},
                    'OMG/ETH': {'amount': {'min': 0.01, 'max': 500000}},
                    'FT/USDT': {'amount': {'min': 1, 'max': 10000000}},
                    'ZIL/ETH': {'amount': {'min': 1, 'max': 10000000}},
                    'ZIP/ETH': {'amount': {'min': 1, 'max': 10000000}},
                    'FT/BTC': {'amount': {'min': 1, 'max': 10000000}},
                    'FT/ETH': {'amount': {'min': 1, 'max': 10000000}},
                },
            },
            'exceptions': {
                '400': NotSupported,  # Bad Request
                '401': AuthenticationError,
                '405': NotSupported,
                '429': DDoSProtection,  # Too Many Requests, exceed api request limit
                '1002': ExchangeNotAvailable,  # System busy
                '1016': InsufficientFunds,
                '3008': InvalidOrder,
                '6004': InvalidNonce,
                '6005': AuthenticationError,  # Illegal API Signature
            },
            'commonCurrencies': {
                'DAG': 'DAGX',
                'PAI': 'PCHAIN',
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetSymbols()
        result = []
        markets = response['data']
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['name']
            baseId = market['base_currency']
            quoteId = market['quote_currency']
            base = baseId.upper()
            base = self.common_currency_code(base)
            quote = quoteId.upper()
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'price': market['price_decimal'],
                'amount': market['amount_decimal'],
            }
            limits = {
                'price': {
                    'min': math.pow(10, -precision['price']),
                    'max': math.pow(10, precision['price']),
                },
            }
            if symbol in self.options['limits']:
                limits = self.extend(self.options['limits'][symbol], limits)
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
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccountsBalance(params)
        result = {'info': response}
        balances = response['data']
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['currency']
            code = currencyId.upper()
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            else:
                code = self.common_currency_code(code)
            account = self.account()
            account['free'] = float(balance['available'])
            account['total'] = float(balance['balance'])
            account['used'] = float(balance['frozen'])
            result[code] = account
        return self.parse_balance(result)

    def parse_bids_asks(self, orders, priceKey=0, amountKey=1):
        result = []
        length = len(orders)
        halfLength = int(length / 2)
        # += 2 in the for loop below won't transpile
        for i in range(0, halfLength):
            index = i * 2
            priceField = self.sum(index, priceKey)
            amountField = self.sum(index, amountKey)
            result.append([
                self.safe_float(orders, priceField),
                self.safe_float(orders, amountField),
            ])
        return result

    async def fetch_order_book(self, symbol=None, limit=None, params={}):
        await self.load_markets()
        if limit is not None:
            if (limit == 20) or (limit == 100):
                limit = 'L' + str(limit)
            else:
                raise ExchangeError(self.id + ' fetchOrderBook supports limit of 20, 100 or no limit. Other values are not accepted')
        else:
            limit = 'full'
        request = self.extend({
            'symbol': self.market_id(symbol),
            'level': limit,  # L20, L100, full
        }, params)
        response = await self.marketGetDepthLevelSymbol(request)
        orderbook = response['data']
        return self.parse_order_book(orderbook, orderbook['ts'], 'bids', 'asks', 0, 1)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.marketGetTickerSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(ticker['data'], market)

    def parse_ticker(self, ticker, market=None):
        timestamp = None
        symbol = None
        if market is None:
            tickerType = self.safe_string(ticker, 'type')
            if tickerType is not None:
                parts = tickerType.split('.')
                id = parts[1]
                if id in self.markets_by_id:
                    market = self.markets_by_id[id]
        values = ticker['ticker']
        last = values[0]
        if market is not None:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': values[7],
            'low': values[8],
            'bid': values[2],
            'bidVolume': values[3],
            'ask': values[4],
            'askVolume': values[5],
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': values[9],
            'quoteVolume': values[10],
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = int(trade['ts'])
        side = trade['side'].lower()
        orderId = self.safe_string(trade, 'id')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = price * amount
        fee = None
        return {
            'id': orderId,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'order': orderId,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=50, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit': limit,
        }
        if since is not None:
            request['timestamp'] = int(since / 1000)
        response = await self.marketGetTradesSymbol(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            # for market buy it requires the amount of quote currency to spend
            if side == 'buy':
                if self.options['createMarketBuyOrderRequiresPrice']:
                    if price is None:
                        raise InvalidOrder(self.id + " createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount, or, alternatively, add .options['createMarketBuyOrderRequiresPrice'] = False to supply the cost in the amount argument(the exchange-specific behaviour)")
                    else:
                        amount = amount * price
        await self.load_markets()
        orderType = type
        request = {
            'symbol': self.market_id(symbol),
            'amount': self.amount_to_precision(symbol, amount),
            'side': side,
            'type': orderType,
        }
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        result = await self.privatePostOrders(self.extend(request, params))
        return {
            'info': result,
            'id': result['data'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privatePostOrdersOrderIdSubmitCancel(self.extend({
            'order_id': id,
        }, params))
        order = self.parse_order(response)
        return self.extend(order, {
            'id': id,
            'status': 'canceled',
        })

    def parse_order_status(self, status):
        statuses = {
            'submitted': 'open',
            'canceled': 'canceled',
            'partial_filled': 'open',
            'partial_canceled': 'canceled',
            'filled': 'closed',
            'pending_cancel': 'canceled',
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        side = self.safe_string(order, 'side')
        status = self.parse_order_status(self.safe_string(order, 'state'))
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'symbol')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        orderType = self.safe_string(order, 'type')
        timestamp = self.safe_integer(order, 'created_at')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'filled_amount')
        remaining = None
        price = self.safe_float(order, 'price')
        cost = self.safe_float(order, 'executed_value')
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
            if cost is None:
                if price is not None:
                    cost = price * filled
            elif (cost > 0) and(filled > 0):
                price = cost / filled
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['base'] if (side == 'buy') else market['quote']
        feeCost = self.safe_float(order, 'fill_fees')
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'average': None,
            'status': status,
            'fee': {
                'cost': feeCost,
                'currency': feeCurrency,
            },
            'trades': None,
        }
        return result

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = self.extend({
            'order_id': id,
        }, params)
        response = await self.privateGetOrdersOrderId(request)
        return self.parse_order(response['data'])

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        result = await self.fetch_orders(symbol, since, limit, {'states': 'submitted,partial_filled'})
        return result

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        result = await self.fetch_orders(symbol, since, limit, {'states': 'filled'})
        return result

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'states': 'submitted,partial_filled,partial_canceled,filled,canceled',
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['id'] * 1000,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['base_vol'],
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=100, params={}):
        await self.load_markets()
        if limit is None:
            raise ExchangeError(self.id + ' fetchOHLCV requires a limit argument')
        market = self.market(symbol)
        request = self.extend({
            'symbol': market['id'],
            'timeframe': self.timeframes[timeframe],
            'limit': limit,
        }, params)
        response = await self.marketGetCandlesTimeframeSymbol(request)
        return self.parse_ohlcvs(response['data'], market, timeframe, since, limit)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/'
        request += '' if (api == 'private') else (api + '/')
        request += self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + request
        if (api == 'public') or (api == 'market'):
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            timestamp = str(self.nonce())
            query = self.keysort(query)
            if method == 'GET':
                if query:
                    url += '?' + self.rawencode(query)
            # HTTP_METHOD + HTTP_REQUEST_URI + TIMESTAMP + POST_BODY
            auth = method + url + timestamp
            if method == 'POST':
                if query:
                    body = self.json(query)
                    auth += self.urlencode(query)
            payload = base64.b64encode(self.encode(auth))
            signature = self.hmac(payload, self.encode(self.secret), hashlib.sha1, 'binary')
            signature = self.decode(base64.b64encode(signature))
            headers = {
                'FC-ACCESS-KEY': self.apiKey,
                'FC-ACCESS-SIGNATURE': signature,
                'FC-ACCESS-TIMESTAMP': timestamp,
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            status = self.safe_string(response, 'status')
            if status != '0':
                feedback = self.id + ' ' + body
                if status in self.exceptions:
                    exceptions = self.exceptions
                    raise exceptions[status](feedback)
                raise ExchangeError(feedback)
