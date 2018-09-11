# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import OrderNotFound


class bitflyer (Exchange):

    def describe(self):
        return self.deep_extend(super(bitflyer, self).describe(), {
            'id': 'bitflyer',
            'name': 'bitFlyer',
            'countries': ['JP'],
            'version': 'v1',
            'rateLimit': 1000,  # their nonce-timestamp is in seconds...
            'has': {
                'CORS': False,
                'withdraw': True,
                'fetchMyTrades': True,
                'fetchOrders': True,
                'fetchOrder': True,
                'fetchOpenOrders': 'emulated',
                'fetchClosedOrders': 'emulated',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28051642-56154182-660e-11e7-9b0d-6042d1e6edd8.jpg',
                'api': 'https://api.bitflyer.jp',
                'www': 'https://bitflyer.jp',
                'doc': 'https://bitflyer.jp/API',
            },
            'api': {
                'public': {
                    'get': [
                        'getmarkets/usa',  # new(wip)
                        'getmarkets/eu',  # new(wip)
                        'getmarkets',     # or 'markets'
                        'getboard',       # ...
                        'getticker',
                        'getexecutions',
                        'gethealth',
                        'getboardstate',
                        'getchats',
                    ],
                },
                'private': {
                    'get': [
                        'getpermissions',
                        'getbalance',
                        'getcollateral',
                        'getcollateralaccounts',
                        'getaddresses',
                        'getcoinins',
                        'getcoinouts',
                        'getbankaccounts',
                        'getdeposits',
                        'getwithdrawals',
                        'getchildorders',
                        'getparentorders',
                        'getparentorder',
                        'getexecutions',
                        'getpositions',
                        'gettradingcommission',
                    ],
                    'post': [
                        'sendcoin',
                        'withdraw',
                        'sendchildorder',
                        'cancelchildorder',
                        'sendparentorder',
                        'cancelparentorder',
                        'cancelallchildorders',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.25 / 100,
                    'taker': 0.25 / 100,
                },
            },
        })

    def fetch_markets(self):
        jp_markets = self.publicGetGetmarkets()
        us_markets = self.publicGetGetmarketsUsa()
        eu_markets = self.publicGetGetmarketsEu()
        markets = self.array_concat(jp_markets, us_markets)
        markets = self.array_concat(markets, eu_markets)
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            id = market['product_code']
            spot = True
            future = False
            type = 'spot'
            if 'alias' in market:
                type = 'future'
                future = True
                spot = False
            currencies = id.split('_')
            baseId = None
            quoteId = None
            base = None
            quote = None
            numCurrencies = len(currencies)
            if numCurrencies == 1:
                baseId = id[0:3]
                quoteId = id[3:6]
            elif numCurrencies == 2:
                baseId = currencies[0]
                quoteId = currencies[1]
            else:
                baseId = currencies[1]
                quoteId = currencies[2]
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = (base + '/' + quote) if (numCurrencies == 2) else id
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'type': type,
                'spot': spot,
                'future': future,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetGetbalance()
        balances = {}
        for b in range(0, len(response)):
            account = response[b]
            currency = account['currency_code']
            balances[currency] = account
        result = {'info': response}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            account = self.account()
            if currency in balances:
                account['total'] = balances[currency]['amount']
                account['free'] = balances[currency]['available']
                account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetGetboard(self.extend({
            'product_code': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'size')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        ticker = self.publicGetGetticker(self.extend({
            'product_code': self.market_id(symbol),
        }, params))
        timestamp = self.parse8601(ticker['timestamp'])
        last = self.safe_float(ticker, 'ltp')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'best_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'best_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume_by_product'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        side = None
        order = None
        if 'side' in trade:
            if trade['side']:
                side = trade['side'].lower()
                id = side + '_child_order_acceptance_id'
                if id in trade:
                    order = trade[id]
        if order is None:
            order = self.safe_string(trade, 'child_order_acceptance_id')
        timestamp = self.parse8601(trade['exec_date'])
        return {
            'id': str(trade['id']),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': order,
            'type': None,
            'side': side,
            'price': trade['price'],
            'amount': trade['size'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetGetexecutions(self.extend({
            'product_code': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        order = {
            'product_code': self.market_id(symbol),
            'child_order_type': type.upper(),
            'side': side.upper(),
            'price': price,
            'size': amount,
        }
        result = self.privatePostSendchildorder(self.extend(order, params))
        # {"status": - 200, "error_message": "Insufficient funds", "data": null}
        return {
            'info': result,
            'id': result['child_order_acceptance_id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        return self.privatePostCancelchildorder(self.extend({
            'product_code': self.market_id(symbol),
            'child_order_acceptance_id': id,
        }, params))

    def parse_order_status(self, status):
        statuses = {
            'ACTIVE': 'open',
            'COMPLETED': 'closed',
            'CANCELED': 'canceled',
            'EXPIRED': 'canceled',
            'REJECTED': 'canceled',
        }
        if status in statuses:
            return statuses[status]
        return status.lower()

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(order['child_order_date'])
        amount = self.safe_float(order, 'size')
        remaining = self.safe_float(order, 'outstanding_size')
        filled = self.safe_float(order, 'executed_size')
        price = self.safe_float(order, 'price')
        cost = price * filled
        status = self.parse_order_status(self.safe_string(order, 'child_order_state'))
        type = order['child_order_type'].lower()
        side = order['side'].lower()
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'product_code')
            if marketId is not None:
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        fee = None
        feeCost = self.safe_float(order, 'total_commission')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
                'rate': None,
            }
        return {
            'id': order['child_order_acceptance_id'],
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
        }

    def fetch_orders(self, symbol=None, since=None, limit=100, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
            'count': limit,
        }
        response = self.privateGetGetchildorders(self.extend(request, params))
        orders = self.parse_orders(response, market, since, limit)
        if symbol is not None:
            orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    def fetch_open_orders(self, symbol=None, since=None, limit=100, params={}):
        request = {
            'child_order_state': 'ACTIVE',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=100, params={}):
        request = {
            'child_order_state': 'COMPLETED',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder() requires a symbol argument')
        orders = self.fetch_orders(symbol)
        ordersById = self.index_by(orders, 'id')
        if id in ordersById:
            return ordersById[id]
        raise OrderNotFound(self.id + ' No order found with id ' + id)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        response = self.privateGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        if code != 'JPY' and code != 'USD' and code != 'EUR':
            raise ExchangeError(self.id + ' allows withdrawing JPY, USD, EUR only, ' + code + ' is not supported')
        currency = self.currency(code)
        response = self.privatePostWithdraw(self.extend({
            'currency_code': currency['id'],
            'amount': amount,
            # 'bank_account_id': 1234,
        }, params))
        return {
            'info': response,
            'id': response['message_id'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/'
        if api == 'private':
            request += 'me/'
        request += path
        if method == 'GET':
            if params:
                request += '?' + self.urlencode(params)
        url = self.urls['api'] + request
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = ''.join([nonce, method, request])
            if params:
                if method != 'GET':
                    body = self.json(params)
                    auth += body
            headers = {
                'ACCESS-KEY': self.apiKey,
                'ACCESS-TIMESTAMP': nonce,
                'ACCESS-SIGN': self.hmac(self.encode(auth), self.encode(self.secret)),
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
