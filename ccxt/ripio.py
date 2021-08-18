# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class ripio(Exchange):

    def describe(self):
        return self.deep_extend(super(ripio, self).describe(), {
            'id': 'ripio',
            'name': 'Ripio',
            'countries': ['AR', 'BR'],  # Argentina
            'rateLimit': 50,
            'version': 'v1',
            'pro': True,
            # new metainfo interface
            'has': {
                'CORS': False,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/94507548-a83d6a80-0218-11eb-9998-28b9cec54165.jpg',
                'api': {
                    'public': 'https://api.exchange.ripio.com/api',
                    'private': 'https://api.exchange.ripio.com/api',
                },
                'www': 'https://exchange.ripio.com',
                'doc': [
                    'https://exchange.ripio.com/en/api/',
                ],
                'fees': 'https://exchange.ripio.com/en/fee',
            },
            'api': {
                'public': {
                    'get': [
                        'rate/all/',
                        'rate/{pair}/',
                        'orderbook/{pair}/',
                        'tradehistory/{pair}/',
                        'pair/',
                        'currency/',
                        'orderbook/{pair}/depth/',
                    ],
                },
                'private': {
                    'get': [
                        'balances/exchange_balances/',
                        'order/{pair}/{order_id}/',
                        'order/{pair}/',
                        'trade/{pair}/',
                    ],
                    'post': [
                        'order/{pair}/',
                        'order/{pair}/{order_id}/cancel/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.0 / 100,
                    'maker': 0.0 / 100,
                },
            },
            'precisionMode': TICK_SIZE,
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'exceptions': {
                'exact': {
                },
                'broad': {
                    'Authentication credentials were not provided': AuthenticationError,  # {"detail":"Authentication credentials were not provided."}
                    'Disabled pair': BadSymbol,  # {"status_code":400,"errors":{"pair":["Invalid/Disabled pair BTC_ARS"]},"message":"An error has occurred, please check the form."}
                    'Invalid order type': InvalidOrder,  # {"status_code":400,"errors":{"order_type":["Invalid order type. Valid options: ['MARKET', 'LIMIT']"]},"message":"An error has occurred, please check the form."}
                    'Your balance is not enough': InsufficientFunds,  # {"status_code":400,"errors":{"non_field_errors":["Your balance is not enough for self order: You have 0 BTC but you need 1 BTC"]},"message":"An error has occurred, please check the form."}
                    "Order couldn't be created": ExchangeError,  # {'status_code': 400,'errors': {'non_field_errors': _("Order couldn't be created")}, 'message': _('Seems like an unexpected error occurred. Please try again later or write us to support@ripio.com if the problem persists.')}
                    # {"status_code":404,"errors":{"order":["Order 286e560e-b8a2-464b-8b84-15a7e2a67eab not found."]},"message":"An error has occurred, please check the form."}
                    # {"status_code":404,"errors":{"trade":["Trade <trade_id> not found."]},"message":"An error has occurred, please check the form."}
                    'not found': OrderNotFound,
                    'Invalid pair': BadSymbol,  # {"status_code":400,"errors":{"pair":["Invalid pair FOOBAR"]},"message":"An error has occurred, please check the form."}
                    'amount must be a number': BadRequest,  # {"status_code":400,"errors":{"amount":["amount must be a number"]},"message":"An error has occurred, please check the form."}
                    'Total must be at least': InvalidOrder,  # {"status_code":400,"errors":{"non_field_errors":["Total must be at least 10."]},"message":"An error has occurred, please check the form."}
                    'Account not found': BadRequest,  # {"error_description": "Account not found."}, "status": 404
                    'Wrong password provided': AuthenticationError,  # {'error': "Wrong password provided."}, “status_code”: 400
                    'User tokens limit': DDoSProtection,  # {'error': "User tokens limit. Can't create more than 10 tokens."}, “status_code”: 400
                    'Something unexpected ocurred': ExchangeError,  # {'status_code': 400, 'errors': {'non_field_errors': 'Something unexpected ocurred!'}, 'message': 'Seems like an unexpected error occurred. Please try again later or write us to support@ripio.com if the problem persists.'}
                    # {'status_code': 404, 'errors': {'account_balance': ['Exchange balance <currency>not found.']},'message': 'An error has occurred, please check the form.'}
                    # {'status_code': 404, 'errors': {'account_balance': ['Account balance <id> not found.']},'message': 'An error has occurred, please check the form.'}
                    'account_balance': BadRequest,
                },
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetPair(params)
        #
        #     {
        #         "next":null,
        #         "previous":null,
        #         "results":[
        #             {
        #                 "base":"BTC",
        #                 "base_name":"Bitcoin",
        #                 "quote":"USDC",
        #                 "quote_name":"USD Coin",
        #                 "symbol":"BTC_USDC",
        #                 "fees":[
        #                     {"traded_volume":0.0,"maker_fee":0.0,"taker_fee":0.0,"cancellation_fee":0.0}
        #                 ],
        #                 "country":"ZZ",
        #                 "enabled":true,
        #                 "priority":10,
        #                 "min_amount":"0.00001",
        #                 "price_tick":"0.000001",
        #                 "min_value":"10",
        #                 "limit_price_threshold":"25.00"
        #             },
        #         ]
        #     }
        #
        result = []
        results = self.safe_value(response, 'results', [])
        for i in range(0, len(results)):
            market = results[i]
            baseId = self.safe_string(market, 'base')
            quoteId = self.safe_string(market, 'quote')
            id = self.safe_string(market, 'symbol')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_number(market, 'min_amount'),
                'price': self.safe_number(market, 'price_tick'),
            }
            limits = {
                'amount': {
                    'min': self.safe_number(market, 'min_amount'),
                    'max': None,
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': self.safe_number(market, 'min_value'),
                    'max': None,
                },
            }
            active = self.safe_value(market, 'enabled', True)
            fees = self.safe_value(market, 'fees', [])
            firstFee = self.safe_value(fees, 0, {})
            maker = self.safe_number(firstFee, 'maker_fee', 0.0)
            taker = self.safe_number(firstFee, 'taker_fee', 0.0)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'maker': maker,
                'taker': taker,
                'limits': limits,
                'info': market,
                'active': active,
            })
        return result

    def fetch_currencies(self, params={}):
        response = self.publicGetCurrency(params)
        #
        #     {
        #         "next":null,
        #         "previous":null,
        #         "results":[
        #             {
        #                 "name":"Argentine Peso",
        #                 "symbol":"$",
        #                 "currency":"ARS",
        #                 "country":"AR",
        #                 "decimal_places":"2",
        #                 "enabled":true
        #             },
        #             {
        #                 "name":"Bitcoin Cash",
        #                 "symbol":"BCH",
        #                 "currency":"BCH",
        #                 "country":"AR",
        #                 "decimal_places":"8",
        #                 "enabled":true
        #             },
        #             {
        #                 "name":"Bitcoin",
        #                 "symbol":"BTC",
        #                 "currency":"BTC",
        #                 "country":"AR",
        #                 "decimal_places":"8",
        #                 "enabled":true
        #             }
        #         ]
        #     }
        #
        results = self.safe_value(response, 'results', [])
        result = {}
        for i in range(0, len(results)):
            currency = results[i]
            id = self.safe_string(currency, 'currency')
            code = self.safe_currency_code(id)
            name = self.safe_string(currency, 'name')
            active = self.safe_value(currency, 'enabled', True)
            precision = self.safe_integer(currency, 'decimal_places')
            result[code] = {
                'id': id,
                'code': code,
                'name': name,
                'info': currency,  # the original payload
                'active': active,
                'fee': None,
                'precision': precision,
                'limits': {
                    'amount': {'min': None, 'max': None},
                    'withdraw': {'min': None, 'max': None},
                },
            }
        return result

    def parse_ticker(self, ticker, market=None):
        #
        # fetchTicker, fetchTickers
        #
        #     {
        #         "pair":"BTC_USDC",
        #         "last_price":"10850.02",
        #         "low":"10720.03",
        #         "high":"10909.99",
        #         "variation":"1.21",
        #         "volume":"0.83868",
        #         "base":"BTC",
        #         "base_name":"Bitcoin",
        #         "quote":"USDC",
        #         "quote_name":"USD Coin",
        #         "bid":"10811.00",
        #         "ask":"10720.03",
        #         "avg":"10851.47",
        #         "ask_volume":"0.00140",
        #         "bid_volume":"0.00185",
        #         "created_at":"2020-09-28 21:44:51.228920+00:00"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(ticker, 'created_at'))
        marketId = self.safe_string(ticker, 'pair')
        symbol = self.safe_symbol(marketId, market)
        last = self.safe_number(ticker, 'last_price')
        average = self.safe_number(ticker, 'avg')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'bid'),
            'bidVolume': self.safe_number(ticker, 'bid_volume'),
            'ask': self.safe_number(ticker, 'ask'),
            'askVolume': self.safe_number(ticker, 'ask_volume'),
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': average,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetRatePair(self.extend(request, params))
        #
        #     {
        #         "pair":"BTC_USDC",
        #         "last_price":"10850.02",
        #         "low":"10720.03",
        #         "high":"10909.99",
        #         "variation":"1.21",
        #         "volume":"0.83868",
        #         "base":"BTC",
        #         "base_name":"Bitcoin",
        #         "quote":"USDC",
        #         "quote_name":"USD Coin",
        #         "bid":"10811.00",
        #         "ask":"10720.03",
        #         "avg":"10851.47",
        #         "ask_volume":"0.00140",
        #         "bid_volume":"0.00185",
        #         "created_at":"2020-09-28 21:44:51.228920+00:00"
        #     }
        #
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetRateAll(params)
        #
        #     [
        #         {
        #             "pair":"BTC_USDC",
        #             "last_price":"10850.02",
        #             "low":"10720.03",
        #             "high":"10909.99",
        #             "variation":"1.21",
        #             "volume":"0.83868",
        #             "base":"BTC",
        #             "base_name":"Bitcoin",
        #             "quote":"USDC",
        #             "quote_name":"USD Coin",
        #             "bid":"10811.00",
        #             "ask":"10720.03",
        #             "avg":"10851.47",
        #             "ask_volume":"0.00140",
        #             "bid_volume":"0.00185",
        #             "created_at":"2020-09-28 21:44:51.228920+00:00"
        #         }
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        response = self.publicGetOrderbookPair(self.extend(request, params))
        #
        #     {
        #         "buy":[
        #             {"amount":"0.00230","total":"24.95","price":"10850.02"},
        #             {"amount":"0.07920","total":"858.52","price":"10840.00"},
        #             {"amount":"0.00277","total":"30.00","price":"10833.03"},
        #         ],
        #         "sell":[
        #             {"amount":"0.03193","total":"348.16","price":"10904.00"},
        #             {"amount":"0.00210","total":"22.90","price":"10905.70"},
        #             {"amount":"0.00300","total":"32.72","price":"10907.98"},
        #         ],
        #         "updated_id":47225
        #     }
        #
        orderbook = self.parse_order_book(response, symbol, None, 'buy', 'sell', 'price', 'amount')
        orderbook['nonce'] = self.safe_integer(response, 'updated_id')
        return orderbook

    def parse_trade(self, trade, market=None):
        #
        # public fetchTrades, private fetchMyTrades
        #
        #     {
        #         "created_at":1601322501,
        #         "amount":"0.00276",
        #         "price":"10850.020000",
        #         "side":"SELL",
        #         "pair":"BTC_USDC",
        #         "taker_fee":"0",
        #         "taker_side":"SELL",
        #         "maker_fee":"0",
        #         "taker":2577953,
        #         "maker":2577937
        #     }
        #
        # createOrder fills
        #
        #     {
        #         "pair":"BTC_USDC",
        #         "exchanged":0.002,
        #         "match_price":10593.99,
        #         "maker_fee":0.0,
        #         "taker_fee":0.0,
        #         "timestamp":1601730306942
        #     }
        #
        id = self.safe_string(trade, 'id')
        timestamp = self.safe_integer(trade, 'timestamp')
        timestamp = self.safe_timestamp(trade, 'created_at', timestamp)
        side = self.safe_string(trade, 'side')
        takerSide = self.safe_string(trade, 'taker_side')
        takerOrMaker = 'taker' if (takerSide == side) else 'maker'
        if side is not None:
            side = side.lower()
        priceString = self.safe_string_2(trade, 'price', 'match_price')
        amountString = self.safe_string_2(trade, 'amount', 'exchanged')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        marketId = self.safe_string(trade, 'pair')
        market = self.safe_market(marketId, market)
        feeCost = self.safe_number(trade, takerOrMaker + '_fee')
        orderId = self.safe_string(trade, takerOrMaker)
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': market['base'] if (side == 'buy') else market['quote'],
            }
        return {
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'takerOrMaker': takerOrMaker,
            'fee': fee,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetTradehistoryPair(self.extend(request, params))
        #
        #     [
        #         {
        #             "created_at":1601322501,
        #             "amount":"0.00276",
        #             "price":"10850.020000",
        #             "side":"SELL",
        #             "pair":"BTC_USDC",
        #             "taker_fee":"0",
        #             "taker_side":"SELL",
        #             "maker_fee":"0",
        #             "taker":2577953,
        #             "maker":2577937
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalancesExchangeBalances(params)
        #
        #     [
        #         {
        #             "id":603794,
        #             "currency":"USD Coin",
        #             "symbol":"USDC",
        #             "available":"0",
        #             "locked":"0",
        #             "code":"exchange",
        #             "balance_type":"crypto"
        #         },
        #     ]
        #
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'symbol')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'available')
            account['used'] = self.safe_string(balance, 'locked')
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        uppercaseType = type.upper()
        uppercaseSide = side.upper()
        request = {
            'pair': market['id'],
            'order_type': uppercaseType,  # LIMIT, MARKET
            'side': uppercaseSide,  # BUY or SELL
            'amount': self.amount_to_precision(symbol, amount),
        }
        if uppercaseType == 'LIMIT':
            request['limit_price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrderPair(self.extend(request, params))
        #
        #     {
        #         "order_id": "160f523c-f6ef-4cd1-a7c9-1a8ede1468d8",
        #         "pair": "BTC_ARS",
        #         "side": "BUY",
        #         "amount": "0.00400",
        #         "notional": null,
        #         "fill_or_kill": False,
        #         "all_or_none": False,
        #         "order_type": "LIMIT",
        #         "status": "OPEN",
        #         "created_at": 1578413945,
        #         "filled": "0.00000",
        #         "limit_price": "10.00",
        #         "stop_price": null,
        #         "distance": null
        #     }
        #
        # createOrder market type
        #
        #     {
        #         "order_id":"d6b60c01-8624-44f2-9e6c-9e8cd677ea5c",
        #         "pair":"BTC_USDC",
        #         "side":"BUY",
        #         "amount":"0.00200",
        #         "notional":"50",
        #         "fill_or_kill":false,
        #         "all_or_none":false,
        #         "order_type":"MARKET",
        #         "status":"OPEN",
        #         "created_at":1601730306,
        #         "filled":"0.00000",
        #         "fill_price":10593.99,
        #         "fee":0.0,
        #         "fills":[
        #             {
        #                 "pair":"BTC_USDC",
        #                 "exchanged":0.002,
        #                 "match_price":10593.99,
        #                 "maker_fee":0.0,
        #                 "taker_fee":0.0,
        #                 "timestamp":1601730306942
        #             }
        #         ],
        #         "filled_at":"2020-10-03T13:05:06.942186Z",
        #         "limit_price":"0.000000",
        #         "stop_price":null,
        #         "distance":null
        #     }
        #
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'order_id': id,
        }
        response = self.privatePostOrderPairOrderIdCancel(self.extend(request, params))
        #
        #     {
        #         "order_id": "286e560e-b8a2-464b-8b84-15a7e2a67eab",
        #         "pair": "BTC_ARS",
        #         "side": "SELL",
        #         "amount": "0.00100",
        #         "notional": null,
        #         "fill_or_kill": False,
        #         "all_or_none": False,
        #         "order_type": "LIMIT",
        #         "status": "CANC",
        #         "created_at": 1575472707,
        #         "filled": "0.00000",
        #         "limit_price": "681000.00",
        #         "stop_price": null,
        #         "distance": null
        #     }
        #
        return self.parse_order(response, market)

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'order_id': id,
        }
        response = self.privateGetOrderPairOrderId(self.extend(request, params))
        #
        #     {
        #         "order_id": "0b4ff48e-cfd6-42db-8d8c-3b536da447af",
        #         "pair": "BTC_ARS",
        #         "side": "BUY",
        #         "amount": "0.00100",
        #         "notional": null,
        #         "fill_or_kill": False,
        #         "all_or_none": False,
        #         "order_type": "LIMIT",
        #         "status": "OPEN",
        #         "created_at": 1575472944,
        #         "filled": "0.00000",
        #         "limit_price": "661000.00",
        #         "stop_price": null,
        #         "distance": null
        #     }
        #
        return self.parse_order(response, market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            # 'status': 'OPEN,PART,CLOS,CANC,COMP',
            # 'offset': 0,
            # 'limit': limit,
        }
        if limit is not None:
            request['offset'] = limit
        response = self.privateGetOrderPair(self.extend(request, params))
        #
        #     {
        #         "next": "https://api.exchange.ripio.com/api/v1/order/BTC_ARS/?limit=20&offset=20&page=1&page_size=25&status=OPEN%2CPART",
        #         "previous": null,
        #         "results": {
        #             "data": [
        #                 {
        #                     "order_id": "ca74280b-6966-4b73-a720-68709078922b",
        #                     "pair": "BTC_ARS",
        #                     "side": "SELL",
        #                     "amount": "0.00100",
        #                     "notional": null,
        #                     "fill_or_kill": False,
        #                     "all_or_none": False,
        #                     "order_type": "LIMIT",
        #                     "status": "OPEN",
        #                     "created_at": 1578340134,
        #                     "filled": "0.00000",
        #                     "limit_price": "665000.00",
        #                     "stop_price": null,
        #                     "distance": null
        #                 },
        #             ]
        #         }
        #     }
        #
        results = self.safe_value(response, 'results', {})
        data = self.safe_value(results, 'data', [])
        return self.parse_orders(data, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'OPEN,PART',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'CLOS,CANC,COMP',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'OPEN': 'open',
            'PART': 'open',
            'CLOS': 'canceled',
            'CANC': 'canceled',
            'COMP': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder, cancelOrder, fetchOpenOrders, fetchClosedOrders, fetchOrders, fetchOrder
        #
        #     {
        #         "order_id": "286e560e-b8a2-464b-8b84-15a7e2a67eab",
        #         "pair": "BTC_ARS",
        #         "side": "SELL",
        #         "amount": "0.00100",
        #         "notional": null,
        #         "fill_or_kill": False,
        #         "all_or_none": False,
        #         "order_type": "LIMIT",
        #         "status": "CANC",
        #         "created_at": 1575472707,
        #         "filled": "0.00000",
        #         "limit_price": "681000.00",
        #         "stop_price": null,
        #         "distance": null
        #     }
        #
        #     {
        #         "order_id":"d6b60c01-8624-44f2-9e6c-9e8cd677ea5c",
        #         "pair":"BTC_USDC",
        #         "side":"BUY",
        #         "amount":"0.00200",
        #         "notional":"50",
        #         "fill_or_kill":false,
        #         "all_or_none":false,
        #         "order_type":"MARKET",
        #         "status":"OPEN",
        #         "created_at":1601730306,
        #         "filled":"0.00000",
        #         "fill_price":10593.99,
        #         "fee":0.0,
        #         "fills":[
        #             {
        #                 "pair":"BTC_USDC",
        #                 "exchanged":0.002,
        #                 "match_price":10593.99,
        #                 "maker_fee":0.0,
        #                 "taker_fee":0.0,
        #                 "timestamp":1601730306942
        #             }
        #         ],
        #         "filled_at":"2020-10-03T13:05:06.942186Z",
        #         "limit_price":"0.000000",
        #         "stop_price":null,
        #         "distance":null
        #     }
        #
        id = self.safe_string(order, 'order_id')
        amount = self.safe_number(order, 'amount')
        cost = self.safe_number(order, 'notional')
        type = self.safe_string_lower(order, 'order_type')
        priceField = 'fill_price' if (type == 'market') else 'limit_price'
        price = self.safe_number(order, priceField)
        side = self.safe_string_lower(order, 'side')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_timestamp(order, 'created_at')
        average = self.safe_value(order, 'fill_price')
        filled = self.safe_number(order, 'filled')
        remaining = None
        fills = self.safe_value(order, 'fills')
        trades = None
        lastTradeTimestamp = None
        if fills is not None:
            numFills = len(fills)
            if numFills > 0:
                filled = 0
                cost = 0
                trades = self.parse_trades(fills, market, None, None, {
                    'order': id,
                    'side': side,
                })
                for i in range(0, len(trades)):
                    trade = trades[i]
                    filled = self.sum(trade['amount'], filled)
                    cost = self.sum(trade['cost'], cost)
                    lastTradeTimestamp = trade['timestamp']
                if (average is None) and (filled > 0):
                    average = cost / filled
        if filled is not None:
            if (cost is None) and (price is not None):
                cost = price * filled
            if amount is not None:
                remaining = max(0, amount - filled)
        marketId = self.safe_string(order, 'pair')
        symbol = self.safe_symbol(marketId, market, '_')
        stopPrice = self.safe_number(order, 'stop_price')
        return {
            'id': id,
            'clientOrderId': None,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
            'trades': trades,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            # 'offset': 0,
            # 'limit': limit,
        }
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetTradePair(self.extend(request, params))
        #
        #     {
        #         "next": "https://api.exchange.ripio.com/api/v1/trade/<pair>/?limit=20&offset=20",
        #         "previous": null,
        #         "results": {
        #             "data": [
        #                 {
        #                     "created_at": 1578414028,
        #                     "amount": "0.00100",
        #                     "price": "665000.00",
        #                     "side": "BUY",
        #                     "taker_fee": "0",
        #                     "taker_side": "BUY",
        #                     "match_price": "66500000",
        #                     "maker_fee": "0",
        #                     "taker": 4892,
        #                     "maker": 4889
        #                 },
        #             ]
        #         }
        #     }
        #
        results = self.safe_value(response, 'results', {})
        data = self.safe_value(results, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + request
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            if method == 'POST':
                body = self.json(query)
            else:
                if query:
                    url += '?' + self.urlencode(query)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.apiKey,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        #
        #      {"detail":"Authentication credentials were not provided."}
        #      {"status_code":400,"errors":{"pair":["Invalid pair FOOBAR"]},"message":"An error has occurred, please check the form."}
        #      {"status_code":400,"errors":{"order_type":["Invalid order type. Valid options: ['MARKET', 'LIMIT']"]},"message":"An error has occurred, please check the form."}
        #      {"status_code":400,"errors":{"non_field_errors":"Something unexpected ocurred!"},"message":"Seems like an unexpected error occurred. Please try again later or write us to support@ripio.com if the problem persists."}
        #      {"status_code":400,"errors":{"pair":["Invalid/Disabled pair BTC_ARS"]},"message":"An error has occurred, please check the form."}
        #
        detail = self.safe_string(response, 'detail')
        if detail is not None:
            feedback = self.id + ' ' + body
            # self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], detail, feedback)
        errors = self.safe_value(response, 'errors')
        if errors is not None:
            feedback = self.id + ' ' + body
            keys = list(errors.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                error = self.safe_value(errors, key, [])
                message = self.safe_string(error, 0)
                # self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
            raise ExchangeError(feedback)  # unknown message
