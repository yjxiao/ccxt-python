# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import OrderNotFound
from ccxt.base.precise import Precise


class bitflyer(Exchange):

    def describe(self):
        return self.deep_extend(super(bitflyer, self).describe(), {
            'id': 'bitflyer',
            'name': 'bitFlyer',
            'countries': ['JP'],
            'version': 'v1',
            'rateLimit': 1000,  # their nonce-timestamp is in seconds...
            'hostname': 'bitflyer.com',  # or bitflyer.com
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': 'emulated',
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': 'emulated',
                'fetchOrder': 'emulated',
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28051642-56154182-660e-11e7-9b0d-6042d1e6edd8.jpg',
                'api': 'https://api.{hostname}',
                'www': 'https://bitflyer.com',
                'doc': 'https://lightning.bitflyer.com/docs?lang=en',
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
                        'getbalancehistory',
                        'getcollateral',
                        'getcollateralhistory',
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
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'BTC/JPY': {
                    'maker': 0.15 / 100,
                    'taker': 0.15 / 100,
                },
            },
        })

    def fetch_markets(self, params={}):
        jp_markets = self.publicGetGetmarkets(params)
        us_markets = self.publicGetGetmarketsUsa(params)
        eu_markets = self.publicGetGetmarketsEu(params)
        markets = self.array_concat(jp_markets, us_markets)
        markets = self.array_concat(markets, eu_markets)
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'product_code')
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
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = (base + '/' + quote) if (numCurrencies == 2) else id
            fees = self.safe_value(self.fees, symbol, self.fees['trading'])
            maker = self.safe_value(fees, 'maker', self.fees['trading']['maker'])
            taker = self.safe_value(fees, 'taker', self.fees['trading']['taker'])
            spot = True
            future = False
            type = 'spot'
            if ('alias' in market) or (currencies[0] == 'FX'):
                type = 'future'
                future = True
                spot = False
                maker = 0.0
                taker = 0.0
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'maker': maker,
                'taker': taker,
                'type': type,
                'spot': spot,
                'future': future,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetGetbalance(params)
        #
        #     [
        #         {
        #             "currency_code": "JPY",
        #             "amount": 1024078,
        #             "available": 508000
        #         },
        #         {
        #             "currency_code": "BTC",
        #             "amount": 10.24,
        #             "available": 4.12
        #         },
        #         {
        #             "currency_code": "ETH",
        #             "amount": 20.48,
        #             "available": 16.38
        #         }
        #     ]
        #
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_string(balance, 'amount')
            account['free'] = self.safe_string(balance, 'available')
            result[code] = account
        return self.parse_balance(result, False)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
        }
        orderbook = self.publicGetGetboard(self.extend(request, params))
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'size')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
        }
        ticker = self.publicGetGetticker(self.extend(request, params))
        timestamp = self.parse8601(self.safe_string(ticker, 'timestamp'))
        last = self.safe_number(ticker, 'ltp')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_number(ticker, 'best_bid'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'best_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'volume_by_product'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        side = self.safe_string_lower(trade, 'side')
        if side is not None:
            if len(side) < 1:
                side = None
        order = None
        if side is not None:
            id = side + '_child_order_acceptance_id'
            if id in trade:
                order = trade[id]
        if order is None:
            order = self.safe_string(trade, 'child_order_acceptance_id')
        timestamp = self.parse8601(self.safe_string(trade, 'exec_date'))
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'size')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        id = self.safe_string(trade, 'id')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': order,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        response = self.publicGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_type': type.upper(),
            'side': side.upper(),
            'price': price,
            'size': amount,
        }
        result = self.privatePostSendchildorder(self.extend(request, params))
        # {"status": - 200, "error_message": "Insufficient funds", "data": null}
        id = self.safe_string(result, 'child_order_acceptance_id')
        return {
            'info': result,
            'id': id,
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a `symbol` argument')
        self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_acceptance_id': id,
        }
        return self.privatePostCancelchildorder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'ACTIVE': 'open',
            'COMPLETED': 'closed',
            'CANCELED': 'canceled',
            'EXPIRED': 'canceled',
            'REJECTED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(self.safe_string(order, 'child_order_date'))
        amount = self.safe_number(order, 'size')
        remaining = self.safe_number(order, 'outstanding_size')
        filled = self.safe_number(order, 'executed_size')
        price = self.safe_number(order, 'price')
        status = self.parse_order_status(self.safe_string(order, 'child_order_state'))
        type = self.safe_string_lower(order, 'child_order_type')
        side = self.safe_string_lower(order, 'side')
        marketId = self.safe_string(order, 'product_code')
        symbol = self.safe_symbol(marketId, market)
        fee = None
        feeCost = self.safe_number(order, 'total_commission')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
                'rate': None,
            }
        id = self.safe_string(order, 'child_order_acceptance_id')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
            'average': None,
            'trades': None,
        })

    def fetch_orders(self, symbol=None, since=None, limit=100, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a `symbol` argument')
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
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a `symbol` argument')
        orders = self.fetch_orders(symbol)
        ordersById = self.index_by(orders, 'id')
        if id in ordersById:
            return ordersById[id]
        raise OrderNotFound(self.id + ' No order found with id ' + id)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        response = self.privateGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_positions(self, symbols=None, params={}):
        if symbols is None:
            raise ArgumentsRequired(self.id + ' fetchPositions() requires a `symbols` argument, exactly one symbol in an array')
        self.load_markets()
        request = {
            'product_code': self.market_ids(symbols),
        }
        response = self.privateGetpositions(self.extend(request, params))
        #
        #     [
        #         {
        #             "product_code": "FX_BTC_JPY",
        #             "side": "BUY",
        #             "price": 36000,
        #             "size": 10,
        #             "commission": 0,
        #             "swap_point_accumulate": -35,
        #             "require_collateral": 120000,
        #             "open_date": "2015-11-03T10:04:45.011",
        #             "leverage": 3,
        #             "pnl": 965,
        #             "sfd": -0.5
        #         }
        #     ]
        #
        # todo unify parsePosition/parsePositions
        return response

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        if code != 'JPY' and code != 'USD' and code != 'EUR':
            raise ExchangeError(self.id + ' allows withdrawing JPY, USD, EUR only, ' + code + ' is not supported')
        currency = self.currency(code)
        request = {
            'currency_code': currency['id'],
            'amount': amount,
            # 'bank_account_id': 1234,
        }
        response = self.privatePostWithdraw(self.extend(request, params))
        id = self.safe_string(response, 'message_id')
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/'
        if api == 'private':
            request += 'me/'
        request += path
        if method == 'GET':
            if params:
                request += '?' + self.urlencode(params)
        baseUrl = self.implode_params(self.urls['api'], {'hostname': self.hostname})
        url = baseUrl + request
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
