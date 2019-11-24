# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import ROUND


class latoken(Exchange):

    def describe(self):
        return self.deep_extend(super(latoken, self).describe(), {
            'id': 'latoken',
            'name': 'Latoken',
            'countries': ['KY'],  # Cayman Islands
            'version': 'v1',
            'rateLimit': 2000,
            'certified': False,
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': False,
                'publicAPI': True,
                'privateAPI': True,
                'cancelOrder': True,
                'cancelAllOrders': True,
                'createMarketOrder': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchCanceledOrders': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': False,
                'fetchOrdersByStatus': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/61511972-24c39f00-aa01-11e9-9f7c-471f1d6e5214.jpg',
                'api': 'https://api.latoken.com',
                'www': 'https://latoken.com',
                'doc': [
                    'https://api.latoken.com',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'ExchangeInfo/time',
                        'ExchangeInfo/limits',
                        'ExchangeInfo/pairs',
                        'ExchangeInfo/pairs/{currency}',
                        'ExchangeInfo/pair',
                        'ExchangeInfo/currencies',
                        'ExchangeInfo/currencies/{symbol}',
                        'MarketData/tickers',
                        'MarketData/ticker/{symbol}',
                        'MarketData/orderBook/{symbol}',
                        'MarketData/orderBook/{symbol}/{limit}',
                        'MarketData/trades/{symbol}',
                        'MarketData/trades/{symbol}/{limit}',
                    ],
                },
                'private': {
                    'get': [
                        'Account/balances',
                        'Account/balances/{currency}',
                        'Order/status',
                        'Order/active',
                        'Order/get_order',
                        'Order/trades',
                    ],
                    'post': [
                        'Order/new',
                        'Order/test-order',
                        'Order/cancel',
                        'Order/cancel_all',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'TSL': 'Treasure SL',
            },
            'options': {
                'createOrderMethod': 'private_post_order_new',  # private_post_order_test_order
            },
            'exceptions': {
                'exact': {
                    'Signature or ApiKey is not valid': AuthenticationError,
                    'Request is out of time': InvalidNonce,
                    'Symbol must be specified': BadRequest,
                },
                'broad': {
                    'Request limit reached': DDoSProtection,
                    'Pair': BadRequest,
                    'Price needs to be greater than': InvalidOrder,
                    'Amount needs to be greater than': InvalidOrder,
                    'The Symbol field is required': InvalidOrder,
                    'OrderType is not valid': InvalidOrder,
                    'Side is not valid': InvalidOrder,
                    'Cancelable order whit': OrderNotFound,
                    'Order': OrderNotFound,
                },
            },
        })

    def nonce(self):
        return self.milliseconds()

    def fetch_time(self, params={}):
        response = self.publicGetExchangeInfoTime(params)
        #
        #     {
        #         "time": "2019-04-18T9:00:00.0Z",
        #         "unixTimeSeconds": 1555578000,
        #         "unixTimeMiliseconds": 1555578000000
        #     }
        #
        return self.safe_integer(response, 'unixTimeMiliseconds')

    def fetch_markets(self, params={}):
        response = self.publicGetExchangeInfoPairs(params)
        #
        #     [
        #         {
        #             "pairId": 502,
        #             "symbol": "LAETH",
        #             "baseCurrency": "LA",
        #             "quotedCurrency": "ETH",
        #             "makerFee": 0.01,
        #             "takerFee": 0.01,
        #             "pricePrecision": 8,
        #             "amountPrecision": 8,
        #             "minQty": 0.1
        #         }
        #     ]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'symbol')
            # the exchange shows them inverted
            baseId = self.safe_string(market, 'baseCurrency')
            quoteId = self.safe_string(market, 'quotedCurrency')
            numericId = self.safe_integer(market, 'pairId')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'price': self.safe_integer(market, 'pricePrecision'),
                'amount': self.safe_integer(market, 'amountPrecision'),
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'minQty'),
                    'max': None,
                },
                'price': {
                    'min': math.pow(10, -precision['price']),
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            result.append({
                'id': id,
                'numericId': numericId,
                'info': market,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': None,  # assuming True
                'precision': precision,
                'limits': limits,
            })
        return result

    def fetch_currencies(self, params={}):
        response = self.publicGetExchangeInfoCurrencies(params)
        #
        #     [
        #         {
        #             "currencyId": 102,
        #             "symbol": "LA",
        #             "name": "Latoken",
        #             "precission": 8,
        #             "type": "ERC20",
        #             "fee": 0.1
        #         }
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'symbol')
            numericId = self.safe_integer(currency, 'currencyId')
            code = self.safe_currency_code(id)
            precision = self.safe_integer(currency, 'precission')
            fee = self.safe_float(currency, 'fee')
            active = None
            result[code] = {
                'id': id,
                'numericId': numericId,
                'code': code,
                'info': currency,
                'name': code,
                'active': active,
                'fee': fee,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                },
            }
        return result

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = amount * rate
        precision = market['precision']['price']
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
            precision = market['precision']['amount']
        cost = self.decimal_to_precision(cost, ROUND, precision, self.precisionMode)
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(cost),
        }

    def fetch_balance(self, currency=None, params={}):
        self.load_markets()
        response = self.privateGetAccountBalances(params)
        #
        #     [
        #         {
        #             "currencyId": 102,
        #             "symbol": "LA",
        #             "name": "Latoken",
        #             "amount": 1054.66,
        #             "available": 900.66,
        #             "frozen": 154,
        #             "pending": 0
        #         }
        #     ]
        #
        result = {
            'info': response,
        }
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'symbol')
            code = self.safe_currency_code(currencyId)
            frozen = self.safe_float(balance, 'frozen')
            pending = self.safe_float(balance, 'pending')
            used = self.sum(frozen, pending)
            account = {
                'free': self.safe_float(balance, 'available'),
                'used': used,
                'total': self.safe_float(balance, 'amount'),
            }
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit': 10,
        }
        if limit is not None:
            request['limit'] = limit  # default 10, max 100
        response = self.publicGetMarketDataOrderBookSymbolLimit(self.extend(request, params))
        #
        #     {
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "spread": 0.07,
        #         "asks": [
        #             {"price": 136.3, "quantity": 7.024}
        #         ],
        #         "bids": [
        #             {"price": 136.2, "quantity": 6.554}
        #         ]
        #     }
        #
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'quantity')

    def parse_ticker(self, ticker, market=None):
        symbol = self.find_symbol(self.safe_string(ticker, 'symbol'), market)
        open = self.safe_float(ticker, 'open')
        close = self.safe_float(ticker, 'close')
        change = None
        if open is not None and close is not None:
            change = close - open
        percentage = self.safe_float(ticker, 'priceChange')
        timestamp = self.nonce()
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'low': self.safe_float(ticker, 'low'),
            'high': self.safe_float(ticker, 'high'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'volume'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetMarketDataTickerSymbol(self.extend(request, params))
        #
        #     {
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "volume": 1023314.3202,
        #         "open": 134.82,
        #         "low": 133.95,
        #         "high": 136.22,
        #         "close": 135.12,
        #         "priceChange": 0.22
        #     }
        #
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetMarketDataTickers(params)
        #
        #     [
        #         {
        #             "pairId": 502,
        #             "symbol": "LAETH",
        #             "volume": 1023314.3202,
        #             "open": 134.82,
        #             "low": 133.95,
        #             "high": 136.22,
        #             "close": 135.12,
        #             "priceChange": 0.22
        #         }
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            if symbols is None or self.in_array(symbol, symbols):
                result[symbol] = ticker
        return result

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         side: 'buy',
        #         price: 0.33634,
        #         amount: 0.01,
        #         timestamp: 1564240008000  # milliseconds
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         id: '1564223032.892829.3.tg15',
        #         orderId: '1564223032.671436.707548@1379:1',
        #         commission: 0,
        #         side: 'buy',
        #         price: 0.32874,
        #         amount: 0.607,
        #         timestamp: 1564223033  # seconds
        #     }
        #
        type = None
        timestamp = self.safe_integer_2(trade, 'timestamp', 'time')
        if timestamp is not None:
            # 03 Jan 2009 - first block
            if timestamp < 1230940800000:
                timestamp *= 1000
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        side = self.safe_string(trade, 'side')
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'id')
        orderId = self.safe_string(trade, 'orderId')
        feeCost = self.safe_float(trade, 'commission')
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
            }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': type,
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default 50, max 100
        response = self.publicGetMarketDataTradesSymbol(self.extend(request, params))
        #
        #     {
        #         "pairId":370,
        #         "symbol":"ETHBTC",
        #         "tradeCount":51,
        #         "trades": [
        #             {
        #                 side: 'buy',
        #                 price: 0.33634,
        #                 amount: 0.01,
        #                 timestamp: 1564240008000  # milliseconds
        #             }
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'trades', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.privateGetOrderTrades(self.extend(request, params))
        #
        #     {
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "tradeCount": 1,
        #         "trades": [
        #             {
        #                 id: '1564223032.892829.3.tg15',
        #                 orderId: '1564223032.671436.707548@1379:1',
        #                 commission: 0,
        #                 side: 'buy',
        #                 price: 0.32874,
        #                 amount: 0.607,
        #                 timestamp: 1564223033  # seconds
        #             }
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'trades', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'active': 'open',
            'partiallyFilled': 'open',
            'filled': 'closed',
            'cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "orderId":"1563460093.134037.704945@0370:2",
        #         "cliOrdId":"",
        #         "pairId":370,
        #         "symbol":"ETHBTC",
        #         "side":"sell",
        #         "orderType":"limit",
        #         "price":1.0,
        #         "amount":1.0
        #     }
        #
        # cancelOrder, fetchOrder, fetchOpenOrders, fetchClosedOrders, fetchCanceledOrders
        #
        #     {
        #         "orderId": "1555492358.126073.126767@0502:2",
        #         "cliOrdId": "myNewOrder",
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "side": "buy",
        #         "orderType": "limit",
        #         "price": 136.2,
        #         "amount": 0.57,
        #         "orderStatus": "partiallyFilled",
        #         "executedAmount": 0.27,
        #         "reaminingAmount": 0.3,
        #         "timeCreated": 155551580736,
        #         "timeFilled": 0
        #     }
        #
        id = self.safe_string(order, 'orderId')
        timestamp = self.safe_timestamp(order, 'timeCreated')
        marketId = self.safe_string(order, 'symbol')
        symbol = marketId
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        side = self.safe_string(order, 'side')
        type = self.safe_string(order, 'orderType')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'executedAmount')
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = amount - filled
        status = self.parse_order_status(self.safe_string(order, 'orderStatus'))
        cost = None
        if filled is not None:
            if price is not None:
                cost = filled * price
        timeFilled = self.safe_timestamp(order, 'timeFilled')
        lastTradeTimestamp = None
        if (timeFilled is not None) and (timeFilled > 0):
            lastTradeTimestamp = timeFilled
        return {
            'id': id,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'average': None,
            'remaining': remaining,
            'fee': None,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_with_method('private_get_order_active', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('filled', symbol, since, limit, params)

    def fetch_canceled_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('cancelled', symbol, since, limit, params)

    def fetch_orders_by_status(self, status, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': status,
        }
        return self.fetch_orders_with_method('private_get_order_status', symbol, since, limit, self.extend(request, params))

    def fetch_orders_with_method(self, method, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrdersWithMethod requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default 100
        response = getattr(self, method)(self.extend(request, params))
        #
        #     [
        #         {
        #             "orderId": "1555492358.126073.126767@0502:2",
        #             "cliOrdId": "myNewOrder",
        #             "pairId": 502,
        #             "symbol": "LAETH",
        #             "side": "buy",
        #             "orderType": "limit",
        #             "price": 136.2,
        #             "amount": 0.57,
        #             "orderStatus": "partiallyFilled",
        #             "executedAmount": 0.27,
        #             "reaminingAmount": 0.3,
        #             "timeCreated": 155551580736,
        #             "timeFilled": 0
        #         }
        #     ]
        #
        return self.parse_orders(response, market, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderId': id,
        }
        response = self.privateGetOrderGetOrder(self.extend(request, params))
        #
        #     {
        #         "orderId": "1555492358.126073.126767@0502:2",
        #         "cliOrdId": "myNewOrder",
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "side": "buy",
        #         "orderType": "limit",
        #         "price": 136.2,
        #         "amount": 0.57,
        #         "orderStatus": "partiallyFilled",
        #         "executedAmount": 0.27,
        #         "reaminingAmount": 0.3,
        #         "timeCreated": 155551580736,
        #         "timeFilled": 0
        #     }
        #
        return self.parse_order(response)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        request = {
            'symbol': self.market_id(symbol),
            'side': side,
            'price': self.price_to_precision(symbol, price),
            'amount': self.amount_to_precision(symbol, amount),
            'orderType': type,
        }
        method = self.safe_string(self.options, 'createOrderMethod', 'private_post_order_new')
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "orderId":"1563460093.134037.704945@0370:2",
        #         "cliOrdId":"",
        #         "pairId":370,
        #         "symbol":"ETHBTC",
        #         "side":"sell",
        #         "orderType":"limit",
        #         "price":1.0,
        #         "amount":1.0
        #     }
        #
        return self.parse_order(response)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderId': id,
        }
        response = self.privatePostOrderCancel(self.extend(request, params))
        #
        #     {
        #         "orderId": "1555492358.126073.126767@0502:2",
        #         "cliOrdId": "myNewOrder",
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "side": "buy",
        #         "orderType": "limit",
        #         "price": 136.2,
        #         "amount": 0.57,
        #         "orderStatus": "partiallyFilled",
        #         "executedAmount": 0.27,
        #         "reaminingAmount": 0.3,
        #         "timeCreated": 155551580736,
        #         "timeFilled": 0
        #     }
        #
        return self.parse_order(response)

    def cancel_all_orders(self, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelAllOrders requires a symbol argument')
        self.load_markets()
        marketId = self.market_id(symbol)
        request = {
            'symbol': marketId,
        }
        response = self.privatePostOrderCancelAll(self.extend(request, params))
        #
        #     {
        #         "pairId": 502,
        #         "symbol": "LAETH",
        #         "cancelledOrders": [
        #             "1555492358.126073.126767@0502:2"
        #         ]
        #     }
        #
        result = []
        canceledOrders = self.safe_value(response, 'cancelledOrders', [])
        for i in range(0, len(canceledOrders)):
            order = self.parse_order({
                'symbol': marketId,
                'orderId': canceledOrders[i],
                'orderStatus': 'canceled',
            })
            result.append(order)
        return result

    def sign(self, path, api='public', method='GET', params=None, headers=None, body=None):
        request = '/api/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            nonce = self.nonce()
            query = self.extend({
                'timestamp': nonce,
            }, query)
        urlencodedQuery = self.urlencode(query)
        if query:
            request += '?' + urlencodedQuery
        if api == 'private':
            self.check_required_credentials()
            signature = self.hmac(self.encode(request), self.encode(self.secret))
            headers = {
                'X-LA-KEY': self.apiKey,
                'X-LA-SIGNATURE': signature,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                body = urlencodedQuery
        url = self.urls['api'] + request
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            return
        #
        #     {"message": "Request limit reachednot ", "details": "Request limit reached. Maximum allowed: 1 per 1s. Please try again in 1 second(s)."}
        #     {"error": {"message": "Pair 370 is not found","errorType":"RequestError","statusCode":400}}
        #     {"error": {"message": "Signature or ApiKey is not valid","errorType":"RequestError","statusCode":400}}
        #     {"error": {"message": "Request is out of time", "errorType": "RequestError", "statusCode":400}}
        #     {"error": {"message": "Price needs to be greater than 0","errorType":"ValidationError","statusCode":400}}
        #     {"error": {"message": "Side is not valid, Price needs to be greater than 0, Amount needs to be greater than 0, The Symbol field is required., OrderType is not valid","errorType":"ValidationError","statusCode":400}}
        #     {"error": {"message": "Cancelable order whit ID 1563460289.571254.704945@0370:1 not found","errorType":"RequestError","statusCode":400}}
        #     {"error": {"message": "Symbol must be specified","errorType":"RequestError","statusCode":400}}
        #     {"error": {"message": "Order 1563460289.571254.704945@0370:1 is not found","errorType":"RequestError","statusCode":400}}
        #
        message = self.safe_string(response, 'message')
        exact = self.exceptions['exact']
        feedback = self.id + ' ' + body
        if message is not None:
            if message in exact:
                raise exact[message](feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
        error = self.safe_value(response, 'error', {})
        errorMessage = self.safe_string(error, 'message')
        if errorMessage is not None:
            if errorMessage in exact:
                raise exact[errorMessage](feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], errorMessage, feedback)
            raise ExchangeError(feedback)  # unknown message
