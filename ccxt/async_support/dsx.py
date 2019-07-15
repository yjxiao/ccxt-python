# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.liqui import liqui
import hashlib
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder


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
                'createDepositAddress': True,
                'fetchDepositAddress': True,
                'fetchTransactions': True,
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
                    'https://dsx.uk/developers/publicApiV2',
                    'https://api.dsx.uk',
                    'https://dsx.uk/api_docs/public',
                    'https://dsx.uk/api_docs/private',
                    '',
                ],
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.15 / 100,
                    'taker': 0.25 / 100,
                },
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
            'exceptions': {
                'exact': {
                    "Order wasn't cancelled": InvalidOrder,  # non-existent order
                },
            },
            'options': {
                'fetchOrderMethod': 'privatePostOrderStatus',
                'fetchMyTradesMethod': 'privatePostHistoryTrades',
                'cancelOrderMethod': 'privatePostOrderCancel',
                'fetchTickersMaxLength': 250,
            },
        })

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        currency = None
        request = {}
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if since is not None:
            request['since'] = since
        if limit is not None:
            request['count'] = limit
        response = await self.privatePostHistoryTransactions(self.extend(request, params))
        #
        #     {
        #         "success": 1,
        #         "return": [
        #             {
        #                 "id": 1,
        #                 "timestamp": 11,
        #                 "type": "Withdraw",
        #                 "amount": 1,
        #                 "currency": "btc",
        #                 "confirmationsCount": 6,
        #                 "address": "address",
        #                 "status": 2,
        #                 "commission": 0.0001
        #             }
        #         ]
        #     }
        #
        transactions = self.safe_value(response, 'return', [])
        return self.parseTransactions(transactions, currency, since, limit)

    def parse_transaction_status(self, status):
        statuses = {
            '1': 'failed',
            '2': 'ok',
            '3': 'pending',
            '4': 'failed',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        #     {
        #         "id": 1,
        #         "timestamp": 11,  # 11 in their docs(
        #         "type": "Withdraw",
        #         "amount": 1,
        #         "currency": "btc",
        #         "confirmationsCount": 6,
        #         "address": "address",
        #         "status": 2,
        #         "commission": 0.0001
        #     }
        #
        timestamp = self.safe_integer(transaction, 'timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
        type = self.safe_string(transaction, 'type')
        if type is not None:
            if type == 'Incoming':
                type = 'deposit'
            elif type == 'Withdraw':
                type = 'withdrawal'
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        return {
            'id': self.safe_string(transaction, 'id'),
            'txid': self.safe_string(transaction, 'txid'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': self.safe_string(transaction, 'address'),
            'type': type,
            'amount': self.safe_float(transaction, 'amount'),
            'currency': code,
            'status': status,
            'fee': {
                'currency': code,
                'cost': self.safe_float(transaction, 'commission'),
                'rate': None,
            },
            'info': transaction,
        }

    async def fetch_markets(self, params={}):
        response = await self.publicGetInfo(params)
        markets = response['pairs']
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'quoted_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
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
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostInfoAccount()
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
        balances = self.safe_value(response, 'return')
        result = {'info': response}
        funds = self.safe_value(balances, 'funds')
        currencyIds = list(funds.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            balance = self.safe_value(funds, currencyId, {})
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['total'] = self.safe_float(balance, 'total')
            result[code] = account
        return self.parse_balance(result)

    async def create_deposit_address(self, code, params={}):
        request = {
            'new': 1,
        }
        response = await self.fetch_deposit_address(code, self.extend(request, params))
        return response

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = await self.dwapiPostDepositCryptoaddress(self.extend(request, params))
        result = self.safe_value(response, 'return', {})
        address = self.safe_string(result, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,  # not documented in DSX API
            'info': response,
        }

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

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
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
        response = await self.privatePostOrderNew(self.extend(request, params))
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

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "amount" : 0.0128,
        #         "price" : 6483.99000,
        #         "timestamp" : 1540334614,
        #         "tid" : 35684364,
        #         "type" : "ask"
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "number": "36635882",  # <-- self is present if the trade has come from the '/order/status' call
        #         "id": "36635882",  # <-- self may have been artifically added by the parseTrades method
        #         "pair": "btcusd",
        #         "type": "buy",
        #         "volume": 0.0595,
        #         "rate": 9750,
        #         "orderId": 77149299,
        #         "timestamp": 1519612317,
        #         "commission": 0.00020825,
        #         "commissionCurrency": "btc"
        #     }
        #
        timestamp = self.safe_integer(trade, 'timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
        side = self.safe_string(trade, 'type')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        price = self.safe_float_2(trade, 'rate', 'price')
        id = self.safe_string_2(trade, 'number', 'id')
        orderId = self.safe_string(trade, 'orderId')
        if 'pair' in trade:
            marketId = self.safe_string(trade, 'pair')
            market = self.safe_value(self.markets_by_id, marketId, market)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        amount = self.safe_float_2(trade, 'amount', 'volume')
        type = 'limit'  # all trades are still limit trades
        takerOrMaker = None
        fee = None
        feeCost = self.safe_float(trade, 'commission')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'commissionCurrency')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        isYourOrder = self.safe_value(trade, 'is_your_order')
        if isYourOrder is not None:
            takerOrMaker = 'taker'
            if isYourOrder:
                takerOrMaker = 'maker'
            if fee is None:
                fee = self.calculate_fee(symbol, type, side, amount, price, takerOrMaker)
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    def parse_order(self, order, market=None):
        #
        # fetchOrder
        #
        #   {
        #     "number": 36635882,
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

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderId': int(id),
        }
        response = await self.privatePostOrderStatus(self.extend(request, params))
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
            }, orders[id]))
            result.append(order)
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # 'count': 10,  # Decimal, The maximum number of orders to return
            # 'fromId': 123,  # Decimal, ID of the first order of the selection
            # 'endId': 321,  # Decimal, ID of the last order of the selection
            # 'order': 'ASC',  # String, Order in which orders shown. Possible values are "ASC" — from first to last, "DESC" — from last to first.
        }
        response = await self.privatePostOrders(self.extend(request, params))
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
        return self.parse_orders_by_id(self.safe_value(response, 'return', {}), symbol, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # 'count': 10,  # Decimal, The maximum number of orders to return
            # 'fromId': 123,  # Decimal, ID of the first order of the selection
            # 'endId': 321,  # Decimal, ID of the last order of the selection
            # 'order': 'ASC',  # String, Order in which orders shown. Possible values are "ASC" — from first to last, "DESC" — from last to first.
        }
        response = await self.privatePostHistoryOrders(self.extend(request, params))
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
        return self.parse_orders_by_id(self.safe_value(response, 'return', {}), symbol, since, limit)

    def parse_trades(self, trades, market=None, since=None, limit=None, params={}):
        result = []
        if isinstance(trades, list):
            for i in range(0, len(trades)):
                result.append(self.parse_trade(trades[i], market))
        else:
            ids = list(trades.keys())
            for i in range(0, len(ids)):
                id = ids[i]
                trade = self.parse_trade(trades[id], market)
                result.append(self.extend(trade, {'id': id}, params))
        result = self.sort_by(result, 'timestamp')
        symbol = market['symbol'] if (market is not None) else None
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        query = self.omit(params, self.extract_params(path))
        if api == 'private' or api == 'dwapi':
            url += self.get_private_path(path, params)
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'nonce': nonce,
                'method': path,
            }, query))
            signature = self.sign_body_with_secret(body)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': signature,
            }
        elif api == 'public':
            url += self.get_version_string() + '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            url += '/' + self.implode_params(path, params)
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                if query:
                    body = self.json(query)
                    headers = {
                        'Content-Type': 'application/json',
                    }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
