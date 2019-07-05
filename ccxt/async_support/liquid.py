# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce


class liquid (Exchange):

    def describe(self):
        return self.deep_extend(super(liquid, self).describe(), {
            'id': 'liquid',
            'name': 'Liquid',
            'countries': ['JP', 'CN', 'TW'],
            'version': '2',
            'rateLimit': 1000,
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/45798859-1a872600-bcb4-11e8-8746-69291ce87b04.jpg',
                'api': 'https://api.liquid.com',
                'www': 'https://www.liquid.com',
                'doc': [
                    'https://developers.liquid.com',
                ],
                'fees': 'https://help.liquid.com/getting-started-with-liquid/the-platform/fee-structure',
                'referral': 'https://www.liquid.com?affiliate=SbzC62lt30976',
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'products',
                        'products/{id}',
                        'products/{id}/price_levels',
                        'executions',
                        'ir_ladders/{currency}',
                    ],
                },
                'private': {
                    'get': [
                        'accounts/balance',
                        'accounts/main_asset',
                        'accounts/{id}',
                        'crypto_accounts',
                        'executions/me',
                        'fiat_accounts',
                        'loan_bids',
                        'loans',
                        'orders',
                        'orders/{id}',
                        'orders/{id}/trades',
                        'orders/{id}/executions',
                        'trades',
                        'trades/{id}/loans',
                        'trading_accounts',
                        'trading_accounts/{id}',
                        'transactions',
                    ],
                    'post': [
                        'fiat_accounts',
                        'loan_bids',
                        'orders',
                    ],
                    'put': [
                        'loan_bids/{id}/close',
                        'loans/{id}',
                        'orders/{id}',
                        'orders/{id}/cancel',
                        'trades/{id}',
                        'trades/{id}/close',
                        'trades/close_all',
                        'trading_accounts/{id}',
                    ],
                },
            },
            'skipJsonOnStatusCodes': [401],
            'exceptions': {
                'API rate limit exceeded. Please retry after 300s': DDoSProtection,
                'API Authentication failed': AuthenticationError,
                'Nonce is too small': InvalidNonce,
                'Order not found': OrderNotFound,
                'Can not update partially filled order': InvalidOrder,
                'Can not update non-live order': OrderNotFound,
                'not_enough_free_balance': InsufficientFunds,
                'must_be_positive': InvalidOrder,
                'less_than_order_size': InvalidOrder,
            },
            'commonCurrencies': {
                'WIN': 'WCOIN',
                'HOT': 'HOT Token',
            },
            'options': {
                'cancelOrderException': True,
            },
        })

    async def fetch_currencies(self, params={}):
        response = await self.publicGetCurrencies(params)
        #
        #     [
        #         {
        #             currency_type: 'fiat',
        #             currency: 'USD',
        #             symbol: '$',
        #             assets_precision: 2,
        #             quoting_precision: 5,
        #             minimum_withdrawal: '15.0',
        #             withdrawal_fee: 5,
        #             minimum_fee: null,
        #             minimum_order_quantity: null,
        #             display_precision: 2,
        #             depositable: True,
        #             withdrawable: True,
        #             discount_fee: 0.5,
        #         },
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'currency')
            code = self.safeCurrencyCode(id)
            active = currency['depositable'] and currency['withdrawable']
            amountPrecision = self.safe_integer(currency, 'display_precision')
            pricePrecision = self.safe_integer(currency, 'quoting_precision')
            precision = max(amountPrecision, pricePrecision)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': code,
                'active': active,
                'fee': self.safe_float(currency, 'withdrawal_fee'),
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -amountPrecision),
                        'max': math.pow(10, amountPrecision),
                    },
                    'price': {
                        'min': math.pow(10, -pricePrecision),
                        'max': math.pow(10, pricePrecision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_float(currency, 'minimum_withdrawal'),
                        'max': None,
                    },
                },
            }
        return result

    async def fetch_markets(self, params={}):
        markets = await self.publicGetProducts()
        #
        #     [
        #         {
        #             id: '7',
        #             product_type: 'CurrencyPair',
        #             code: 'CASH',
        #             name: ' CASH Trading',
        #             market_ask: 8865.79147,
        #             market_bid: 8853.95988,
        #             indicator: 1,
        #             currency: 'SGD',
        #             currency_pair_code: 'BTCSGD',
        #             symbol: 'S$',
        #             btc_minimum_withdraw: null,
        #             fiat_minimum_withdraw: null,
        #             pusher_channel: 'product_cash_btcsgd_7',
        #             taker_fee: 0,
        #             maker_fee: 0,
        #             low_market_bid: '8803.25579',
        #             high_market_ask: '8905.0',
        #             volume_24h: '15.85443468',
        #             last_price_24h: '8807.54625',
        #             last_traded_price: '8857.77206',
        #             last_traded_quantity: '0.00590974',
        #             quoted_currency: 'SGD',
        #             base_currency: 'BTC',
        #             disabled: False,
        #         },
        #     ]
        #
        currencies = await self.fetch_currencies()
        currenciesByCode = self.index_by(currencies, 'code')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = str(market['id'])
            baseId = market['base_currency']
            quoteId = market['quoted_currency']
            base = self.safeCurrencyCode(baseId)
            quote = self.safeCurrencyCode(quoteId)
            symbol = base + '/' + quote
            maker = self.safe_float(market, 'maker_fee')
            taker = self.safe_float(market, 'taker_fee')
            active = not market['disabled']
            baseCurrency = self.safe_value(currenciesByCode, base)
            quoteCurrency = self.safe_value(currenciesByCode, quote)
            precision = {
                'amount': 8,
                'price': 8,
            }
            minAmount = None
            if baseCurrency is not None:
                minAmount = self.safe_float(baseCurrency['info'], 'minimum_order_quantity')
                precision['amount'] = self.safe_integer(baseCurrency['info'], 'quoting_precision')
            minPrice = None
            if quoteCurrency is not None:
                precision['price'] = self.safe_integer(quoteCurrency['info'], 'display_precision')
                minPrice = math.pow(10, -precision['price'])
            minCost = None
            if minPrice is not None:
                if minAmount is not None:
                    minCost = minPrice * minAmount
            limits = {
                'amount': {
                    'min': minAmount,
                    'max': None,
                },
                'price': {
                    'min': minPrice,
                    'max': None,
                },
                'cost': {
                    'min': minCost,
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
                'maker': maker,
                'taker': taker,
                'limits': limits,
                'precision': precision,
                'active': active,
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccountsBalance(params)
        #
        #     [
        #         {"currency":"USD","balance":"0.0"},
        #         {"currency":"BTC","balance":"0.0"},
        #         {"currency":"ETH","balance":"0.1651354"}
        #     ]
        #
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safeCurrencyCode(currencyId)
            total = self.safe_float(balance, 'balance')
            account = {
                'free': total,
                'used': 0.0,
                'total': total,
            }
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        response = await self.publicGetProductsIdPriceLevels(self.extend(request, params))
        return self.parse_order_book(response, None, 'buy_price_levels', 'sell_price_levels')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        last = None
        if 'last_traded_price' in ticker:
            if ticker['last_traded_price']:
                length = len(ticker['last_traded_price'])
                if length > 0:
                    last = self.safe_float(ticker, 'last_traded_price')
        symbol = None
        if market is None:
            marketId = self.safe_string(ticker, 'id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId = self.safe_string(ticker, 'base_currency')
                quoteId = self.safe_string(ticker, 'quoted_currency')
                if symbol in self.markets:
                    market = self.markets[symbol]
                else:
                    symbol = self.safeCurrencyCode(baseId) + '/' + self.safeCurrencyCode(quoteId)
        if market is not None:
            symbol = market['symbol']
        change = None
        percentage = None
        average = None
        open = self.safe_float(ticker, 'last_price_24h')
        if open is not None and last is not None:
            change = last - open
            average = self.sum(last, open) / 2
            if open > 0:
                percentage = change / open * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high_market_ask'),
            'low': self.safe_float(ticker, 'low_market_bid'),
            'bid': self.safe_float(ticker, 'market_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'market_ask'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'volume_24h'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetProducts(params)
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = await self.publicGetProductsId(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market):
        # {            id:  12345,
        #         quantity: "6.789",
        #            price: "98765.4321",
        #       taker_side: "sell",
        #       created_at:  1512345678,
        #          my_side: "buy"           }
        timestamp = self.safe_integer(trade, 'created_at') * 1000
        orderId = self.safe_string(trade, 'order_id')
        # 'taker_side' gets filled for both fetchTrades and fetchMyTrades
        takerSide = self.safe_string(trade, 'taker_side')
        # 'my_side' gets filled for fetchMyTrades only and may differ from 'taker_side'
        mySide = self.safe_string(trade, 'my_side')
        side = mySide if (mySide is not None) else takerSide
        takerOrMaker = None
        if mySide is not None:
            takerOrMaker = 'taker' if (takerSide == mySide) else 'maker'
        cost = None
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'quantity')
        if price is not None:
            if amount is not None:
                cost = price * amount
        id = self.safe_string(trade, 'id')
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_id': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            # timestamp should be in seconds, whereas we use milliseconds in since and everywhere
            request['timestamp'] = int(since / 1000)
        response = await self.publicGetExecutions(self.extend(request, params))
        result = response if (since is not None) else response['models']
        return self.parse_trades(result, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        # the `with_details` param is undocumented - it adds the order_id to the results
        request = {
            'product_id': market['id'],
            'with_details': True,
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetExecutionsMe(self.extend(request, params))
        return self.parse_trades(response['models'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'order_type': type,
            'product_id': self.market_id(symbol),
            'side': side,
            'quantity': self.amount_to_precision(symbol, amount),
        }
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        response = await self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #         "id": 2157474,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.0",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "live",
        #         "leverage_level": 1,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0"
        #     }
        #
        return self.parse_order(response)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privatePutOrdersIdCancel(self.extend(request, params))
        order = self.parse_order(response)
        if order['status'] == 'closed':
            if self.options['cancelOrderException']:
                raise OrderNotFound(self.id + ' order closed already: ' + self.json(response))
        return order

    async def edit_order(self, id, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if price is None:
            raise ArgumentsRequired(self.id + ' editOrder requires the price argument')
        request = {
            'order': {
                'quantity': self.amount_to_precision(symbol, amount),
                'price': self.price_to_precision(symbol, price),
            },
            'id': id,
        }
        response = await self.privatePutOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def parse_order_status(self, status):
        statuses = {
            'live': 'open',
            'filled': 'closed',
            'cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "id": 2157474,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.0",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "live",
        #         "leverage_level": 1,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0"
        #     }
        #
        # fetchOrder, fetchOrders, fetchOpenOrders, fetchClosedOrders
        #
        #     {
        #         "id": 2157479,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.01",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "filled",
        #         "leverage_level": 2,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0",
        #         "executions": [
        #             {
        #                 "id": 4566133,
        #                 "quantity": "0.01",
        #                 "price": "500.0",
        #                 "taker_side": "buy",
        #                 "my_side": "sell",
        #                 "created_at": 1465396785
        #             }
        #         ]
        #     }
        #
        orderId = self.safe_string(order, 'id')
        timestamp = self.safe_integer(order, 'created_at')
        if timestamp is not None:
            timestamp = timestamp * 1000
        marketId = self.safe_string(order, 'product_id')
        market = self.safe_value(self.markets_by_id, marketId)
        status = self.parse_order_status(self.safe_string(order, 'status'))
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'filled_quantity')
        price = self.safe_float(order, 'price')
        symbol = None
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        type = self.safe_string(order, 'order_type')
        tradeCost = 0
        tradeFilled = 0
        average = self.safe_float(order, 'average_price')
        trades = self.parse_trades(self.safe_value(order, 'executions', []), market, None, None, {
            'order': orderId,
            'type': type,
        })
        numTrades = len(trades)
        for i in range(0, numTrades):
            # php copies values upon assignment, but not references them
            # todo rewrite self(shortly)
            trade = trades[i]
            trade['order'] = orderId
            trade['type'] = type
            tradeFilled = self.sum(tradeFilled, trade['amount'])
            tradeCost = self.sum(tradeCost, trade['cost'])
        cost = None
        lastTradeTimestamp = None
        if numTrades > 0:
            lastTradeTimestamp = trades[numTrades - 1]['timestamp']
            if not average and(tradeFilled > 0):
                average = tradeCost / tradeFilled
            if cost is None:
                cost = tradeCost
            if filled is None:
                filled = tradeFilled
        remaining = None
        if amount is not None and filled is not None:
            remaining = amount - filled
        side = self.safe_string(order, 'side')
        return {
            'id': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'type': type,
            'status': status,
            'symbol': symbol,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': filled,
            'cost': cost,
            'remaining': remaining,
            'average': average,
            'trades': trades,
            'fee': {
                'currency': feeCurrency,
                'cost': self.safe_float(order, 'order_fee'),
            },
            'info': order,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privateGetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {
            # 'funding_currency': market['quoteId'],  # filter orders based on "funding" currency(quote currency)
            # 'product_id': market['id'],
            # 'status': 'live',  # 'filled', 'cancelled'
            # 'trading_type': 'spot',  # 'margin', 'cfd'
            'with_details': 1,  # return full order details including executions
        }
        if symbol is not None:
            market = self.market(symbol)
            request['product_id'] = market['id']
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetOrders(self.extend(request, params))
        #
        #     {
        #         "models": [
        #             {
        #                 "id": 2157474,
        #                 "order_type": "limit",
        #                 "quantity": "0.01",
        #                 "disc_quantity": "0.0",
        #                 "iceberg_total_quantity": "0.0",
        #                 "side": "sell",
        #                 "filled_quantity": "0.0",
        #                 "price": "500.0",
        #                 "created_at": 1462123639,
        #                 "updated_at": 1462123639,
        #                 "status": "live",
        #                 "leverage_level": 1,
        #                 "source_exchange": "QUOINE",
        #                 "product_id": 1,
        #                 "product_code": "CASH",
        #                 "funding_currency": "USD",
        #                 "currency_pair_code": "BTCUSD",
        #                 "order_fee": "0.0",
        #                 "executions": [],  # optional
        #             }
        #         ],
        #         "current_page": 1,
        #         "total_pages": 1
        #     }
        #
        orders = self.safe_value(response, 'models', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'live'}
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'filled'}
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        headers = {
            'X-Quoine-API-Version': self.version,
            'Content-Type': 'application/json',
        }
        if api == 'private':
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            elif query:
                body = self.json(query)
            nonce = self.nonce()
            request = {
                'path': url,
                'nonce': nonce,
                'token_id': self.apiKey,
                'iat': int(math.floor(nonce / 1000)),  # issued at
            }
            headers['X-Quoine-Auth'] = self.jwt(request, self.encode(self.secret))
        else:
            if query:
                url += '?' + self.urlencode(query)
        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if code >= 200 and code < 300:
            return
        exceptions = self.exceptions
        if code == 401:
            # expected non-json response
            if body in exceptions:
                raise exceptions[body](self.id + ' ' + body)
            else:
                return
        if code == 429:
            raise DDoSProtection(self.id + ' ' + body)
        if response is None:
            return
        feedback = self.id + ' ' + body
        message = self.safe_string(response, 'message')
        errors = self.safe_value(response, 'errors')
        if message is not None:
            #
            #  {"message": "Order not found"}
            #
            if message in exceptions:
                raise exceptions[message](feedback)
        elif errors is not None:
            #
            #  {"errors": {"user": ["not_enough_free_balance"]}}
            #  {"errors": {"quantity": ["less_than_order_size"]}}
            #  {"errors": {"order": ["Can not update partially filled order"]}}
            #
            types = list(errors.keys())
            for i in range(0, len(types)):
                type = types[i]
                errorMessages = errors[type]
                for j in range(0, len(errorMessages)):
                    message = errorMessages[j]
                    if message in exceptions:
                        raise exceptions[message](feedback)
        else:
            raise ExchangeError(feedback)
