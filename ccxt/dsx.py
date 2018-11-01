# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.liqui import liqui
import hashlib
from ccxt.base.errors import ArgumentsRequired


class dsx (liqui):

    def describe(self):
        return self.deep_extend(super(dsx, self).describe(), {
            'id': 'dsx',
            'name': 'DSX',
            'countries': ['UK'],
            'rateLimit': 1500,
            'version': 'v2',
            'has': {
                'CORS': False,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': False,
                'fetchOrderBooks': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27990275-1413158a-645a-11e7-931c-94717f7510e3.jpg',
                'api': {
                    'public': 'https://dsx.uk/mapi',  # market data
                    'private': 'https://dsx.uk/tapi',  # trading
                    'dwapi': 'https://dsx.uk/dwapi',  # deposit/withdraw
                },
                'www': 'https://dsx.uk',
                'doc': [
                    'https://api.dsx.uk',
                    'https://dsx.uk/api_docs/public',
                    'https://dsx.uk/api_docs/private',
                    '',
                ],
            },
            'api': {
                # market data(public)
                'public': {
                    'get': [
                        'barsFromMoment/{id}/{period}/{start}',  # empty reply :\
                        'depth/{pair}',
                        'info',
                        'lastBars/{id}/{period}/{amount}',  # period is(m, h or d)
                        'periodBars/{id}/{period}/{start}/{end}',
                        'ticker/{pair}',
                        'trades/{pair}',
                    ],
                },
                # trading(private)
                'private': {
                    'post': [
                        'info/account',
                        'history/transactions',
                        'history/trades',
                        'history/orders',
                        'orders',
                        'order/cancel',
                        'order/cancel/all',
                        'order/status',
                        'order/new',
                        'volume',
                        'fees',  # trading fee schedule
                    ],
                },
                # deposit / withdraw(private)
                'dwapi': {
                    'post': [
                        'deposit/cryptoaddress',
                        'withdraw/crypto',
                        'withdraw/fiat',
                        'withdraw/submit',
                        'withdraw/cancel',
                        'transaction/status',  # see 'history/transactions' in private tapi above
                    ],
                },
            },
            'options': {
                'fetchOrderMethod': 'privatePostOrderStatus',
                'fetchMyTradesMethod': 'privatePostHistoryTrades',
                'cancelOrderMethod': 'privatePostOrderCancel',
                'fetchTickersMaxLength': 250,
            },
        })

    def fetch_markets(self):
        response = self.publicGetInfo()
        markets = response['pairs']
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'quoted_currency')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'decimal_places'),
                'price': self.safe_integer(market, 'decimal_places'),
            }
            amountLimits = {
                'min': self.safe_float(market, 'min_amount'),
                'max': self.safe_float(market, 'max_amount'),
            }
            priceLimits = {
                'min': self.safe_float(market, 'min_price'),
                'max': self.safe_float(market, 'max_price'),
            }
            costLimits = {
                'min': self.safe_float(market, 'min_total'),
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            hidden = self.safe_integer(market, 'hidden')
            active = (hidden == 0)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'taker': market['fee'] / 100,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostInfoAccount()
        #
        #     {
        #       "success" : 1,
        #       "return" : {
        #         "funds" : {
        #           "BTC" : {
        #             "total" : 0,
        #             "available" : 0
        #           },
        #           "USD" : {
        #             "total" : 0,
        #             "available" : 0
        #           },
        #           "USDT" : {
        #             "total" : 0,
        #             "available" : 0
        #           }
        #         },
        #         "rights" : {
        #           "info" : 1,
        #           "trade" : 1
        #         },
        #         "transactionCount" : 0,
        #         "openOrders" : 0,
        #         "serverTime" : 1537451465
        #       }
        #     }
        #
        balances = response['return']
        result = {'info': balances}
        funds = balances['funds']
        ids = list(funds.keys())
        for c in range(0, len(ids)):
            id = ids[c]
            code = self.common_currency_code(id)
            account = {
                'free': funds[id]['available'],
                'used': 0.0,
                'total': funds[id]['total'],
            }
            account['used'] = account['total'] - account['free']
            result[code] = account
        return self.parse_balance(result)

    def parse_ticker(self, ticker, market=None):
        #
        #   {   high:  0.03492,
        #         low:  0.03245,
        #         avg:  29.46133,
        #         vol:  500.8661,
        #     vol_cur:  17.000797104,
        #        last:  0.03364,
        #         buy:  0.03362,
        #        sell:  0.03381,
        #     updated:  1537521993,
        #        pair: "ethbtc"       }
        #
        timestamp = ticker['updated'] * 1000
        symbol = None
        # dsx has 'pair' in the ticker, liqui does not have it
        marketId = self.safe_string(ticker, 'pair')
        market = self.safe_value(self.markets_by_id, marketId, market)
        if market is not None:
            symbol = market['symbol']
        # dsx average is inverted, liqui average is not
        average = self.safe_float(ticker, 'avg')
        if average is not None:
            if average > 0:
                average = 1 / average
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'vol'),  # dsx shows baseVolume in 'vol', liqui shows baseVolume in 'vol_cur'
            'quoteVolume': self.safe_float(ticker, 'vol_cur'),  # dsx shows baseVolume in 'vol_cur', liqui shows baseVolume in 'vol'
            'info': ticker,
        }

    def sign_body_with_secret(self, body):
        return self.decode(self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512, 'base64'))

    def get_version_string(self):
        return ''

    def get_private_path(self, path, params):
        return '/' + self.version + '/' + self.implode_params(path, params)

    def get_order_id_key(self):
        return 'orderId'

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if type == 'market' and price is None:
            raise ArgumentsRequired(self.id + ' createOrder requires a price argument even for market orders, that is the worst price that you agree to fill your order for')
        request = {
            'pair': market['id'],
            'type': side,
            'volume': self.amount_to_precision(symbol, amount),
            'rate': self.price_to_precision(symbol, price),
            'orderType': type,
        }
        price = float(price)
        amount = float(amount)
        response = self.privatePostOrderNew(self.extend(request, params))
        #
        #     {
        #       "success": 1,
        #       "return": {
        #         "received": 0,
        #         "remains": 10,
        #         "funds": {
        #           "BTC": {
        #             "total": 100,
        #             "available": 95
        #           },
        #           "USD": {
        #             "total": 10000,
        #             "available": 9995
        #           },
        #           "EUR": {
        #             "total": 1000,
        #             "available": 995
        #           },
        #           "LTC": {
        #             "total": 1000,
        #             "available": 995
        #           }
        #         },
        #         "orderId": 0,  # https://github.com/ccxt/ccxt/issues/3677
        #       }
        #     }
        #
        status = 'open'
        filled = 0.0
        remaining = amount
        responseReturn = self.safe_value(response, 'return')
        id = self.safe_string_2(responseReturn, 'orderId', 'order_id')
        if id == '0':
            id = self.safe_string(responseReturn, 'initOrderId', 'init_order_id')
            status = 'closed'
        filled = self.safe_float(responseReturn, 'received', 0.0)
        remaining = self.safe_float(responseReturn, 'remains', amount)
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': price * filled,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',  # Active
            '1': 'closed',  # Filled
            '2': 'canceled',  # Killed
            '3': 'canceling',  # Killing
            '7': 'canceled',  # Rejected
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # fetchOrder
        #
        #   {
        #     "pair": "btcusd",
        #     "type": "buy",
        #     "remainingVolume": 10,
        #     "volume": 10,
        #     "rate": 1000.0,
        #     "timestampCreated": 1496670,
        #     "status": 0,
        #     "orderType": "limit",
        #     "deals": [
        #       {
        #         "pair": "btcusd",
        #         "type": "buy",
        #         "amount": 1,
        #         "rate": 1000.0,
        #         "orderId": 1,
        #         "timestamp": 1496672724,
        #         "commission": 0.001,
        #         "commissionCurrency": "btc"
        #       }
        #     ]
        #   }
        #
        id = self.safe_string(order, 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_integer(order, 'timestampCreated')
        if timestamp is not None:
            timestamp = timestamp * 1000
        marketId = self.safe_string(order, 'pair')
        market = self.safe_value(self.markets_by_id, marketId, market)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        remaining = self.safe_float(order, 'remainingVolume')
        amount = self.safe_float(order, 'volume')
        price = self.safe_float(order, 'rate')
        filled = None
        cost = None
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
                cost = price * filled
        orderType = self.safe_string(order, 'orderType')
        side = self.safe_string(order, 'type')
        fee = None
        deals = self.safe_value(order, 'deals', [])
        numDeals = len(deals)
        trades = None
        lastTradeTimestamp = None
        if numDeals > 0:
            trades = self.parse_trades(deals)
            feeCost = None
            feeCurrency = None
            for i in range(0, len(trades)):
                trade = trades[i]
                if feeCost is None:
                    feeCost = 0
                feeCost += trade['fee']['cost']
                feeCurrency = trade['fee']['currency']
                lastTradeTimestamp = trade['timestamp']
            if feeCost is not None:
                fee = {
                    'cost': feeCost,
                    'currency': feeCurrency,
                }
        return {
            'info': order,
            'id': id,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'type': orderType,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderId': int(id),
        }
        response = self.privatePostOrderStatus(self.extend(request, params))
        #
        #     {
        #       "success": 1,
        #       "return": {
        #         "pair": "btcusd",
        #         "type": "buy",
        #         "remainingVolume": 10,
        #         "volume": 10,
        #         "rate": 1000.0,
        #         "timestampCreated": 1496670,
        #         "status": 0,
        #         "orderType": "limit",
        #         "deals": [
        #           {
        #             "pair": "btcusd",
        #             "type": "buy",
        #             "amount": 1,
        #             "rate": 1000.0,
        #             "orderId": 1,
        #             "timestamp": 1496672724,
        #             "commission": 0.001,
        #             "commissionCurrency": "btc"
        #           }
        #         ]
        #       }
        #     }
        #
        return self.parse_order(self.extend({
            'id': id,
        }, response['return']))

    def parse_orders_by_id(self, orders, symbol=None, since=None, limit=None):
        ids = list(orders.keys())
        result = []
        for i in range(0, len(ids)):
            id = ids[i]
            order = self.parse_order(self.extend({
                'id': str(id),
            }, orders[i]))
            result.append(order)
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            # 'count': 10,  # Decimal, The maximum number of orders to return
            # 'fromId': 123,  # Decimal, ID of the first order of the selection
            # 'endId': 321,  # Decimal, ID of the last order of the selection
            # 'order': 'ASC',  # String, Order in which orders shown. Possible values are "ASC" — from first to last, "DESC" — from last to first.
        }
        response = self.privatePostHistoryOrders(self.extend(request, params))
        #
        #     {
        #       "success": 1,
        #       "return": {
        #         "0": {
        #           "pair": "btcusd",
        #           "type": "buy",
        #           "remainingVolume": 10,
        #           "volume": 10,
        #           "rate": 1000.0,
        #           "timestampCreated": 1496670,
        #           "status": 0,
        #           "orderType": "limit"
        #         }
        #       }
        #     }
        #
        return self.parse_orders_by_id(self.safe_value(response, 'return', {}))

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            # 'count': 10,  # Decimal, The maximum number of orders to return
            # 'fromId': 123,  # Decimal, ID of the first order of the selection
            # 'endId': 321,  # Decimal, ID of the last order of the selection
            # 'order': 'ASC',  # String, Order in which orders shown. Possible values are "ASC" — from first to last, "DESC" — from last to first.
        }
        response = self.privatePostHistoryOrders(self.extend(request, params))
        #
        #     {
        #       "success": 1,
        #       "return": {
        #         "0": {
        #           "pair": "btcusd",
        #           "type": "buy",
        #           "remainingVolume": 10,
        #           "volume": 10,
        #           "rate": 1000.0,
        #           "timestampCreated": 1496670,
        #           "status": 0,
        #           "orderType": "limit"
        #         }
        #       }
        #     }
        #
        return self.parse_orders_by_id(self.safe_value(response, 'return', {}))
