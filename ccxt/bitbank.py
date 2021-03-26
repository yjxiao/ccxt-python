# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import InvalidNonce


class bitbank(Exchange):

    def describe(self):
        return self.deep_extend(super(bitbank, self).describe(), {
            'id': 'bitbank',
            'name': 'bitbank',
            'countries': ['JP'],
            'version': 'v1',
            'has': {
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '4h': '4hour',
                '8h': '8hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/37808081-b87f2d9c-2e59-11e8-894d-c1900b7584fe.jpg',
                'api': {
                    'public': 'https://public.bitbank.cc',
                    'private': 'https://api.bitbank.cc',
                },
                'www': 'https://bitbank.cc/',
                'doc': 'https://docs.bitbank.cc/',
                'fees': 'https://bitbank.cc/docs/fees/',
            },
            'api': {
                'public': {
                    'get': [
                        '{pair}/ticker',
                        '{pair}/depth',
                        '{pair}/transactions',
                        '{pair}/transactions/{yyyymmdd}',
                        '{pair}/candlestick/{candletype}/{yyyymmdd}',
                    ],
                },
                'private': {
                    'get': [
                        'user/assets',
                        'user/spot/order',
                        'user/spot/active_orders',
                        'user/spot/trade_history',
                        'user/withdrawal_account',
                    ],
                    'post': [
                        'user/spot/order',
                        'user/spot/cancel_order',
                        'user/spot/cancel_orders',
                        'user/spot/orders_info',
                        'user/request_withdrawal',
                    ],
                },
            },
            'markets': {
                'BAT/JPY': {'id': 'bat_jpy', 'symbol': 'BAT/JPY', 'base': 'BAT', 'quote': 'JPY', 'baseId': 'bat', 'quoteId': 'jpy'},
                'BAT/BTC': {'id': 'bat_btc', 'symbol': 'BAT/BTC', 'base': 'BAT', 'quote': 'BTC', 'baseId': 'bat', 'quoteId': 'btc'},
                'BCH/BTC': {'id': 'bcc_btc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bcc', 'quoteId': 'btc'},
                'BCH/JPY': {'id': 'bcc_jpy', 'symbol': 'BCH/JPY', 'base': 'BCH', 'quote': 'JPY', 'baseId': 'bcc', 'quoteId': 'jpy'},
                'BTC/JPY': {'id': 'btc_jpy', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY', 'baseId': 'btc', 'quoteId': 'jpy'},
                'ETH/BTC': {'id': 'eth_btc', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'eth', 'quoteId': 'btc'},
                'ETH/JPY': {'id': 'eth_jpy', 'symbol': 'ETH/JPY', 'base': 'ETH', 'quote': 'JPY', 'baseId': 'eth', 'quoteId': 'jpy'},
                'LTC/BTC': {'id': 'ltc_btc', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC', 'baseId': 'ltc', 'quoteId': 'btc'},
                'LTC/JPY': {'id': 'ltc_jpy', 'symbol': 'LTC/JPY', 'base': 'LTC', 'quote': 'JPY', 'baseId': 'ltc', 'quoteId': 'jpy'},
                'MONA/BTC': {'id': 'mona_btc', 'symbol': 'MONA/BTC', 'base': 'MONA', 'quote': 'BTC', 'baseId': 'mona', 'quoteId': 'btc'},
                'MONA/JPY': {'id': 'mona_jpy', 'symbol': 'MONA/JPY', 'base': 'MONA', 'quote': 'JPY', 'baseId': 'mona', 'quoteId': 'jpy'},
                'QTUM/BTC': {'id': 'qtum_btc', 'symbol': 'QTUM/BTC', 'base': 'QTUM', 'quote': 'BTC', 'baseId': 'qtum', 'quoteId': 'btc'},
                'QTUM/JPY': {'id': 'qtum_jpy', 'symbol': 'QTUM/JPY', 'base': 'QTUM', 'quote': 'JPY', 'baseId': 'qtum', 'quoteId': 'jpy'},
                'XLM/BTC': {'id': 'xlm_btc', 'symbol': 'XLM/BTC', 'base': 'XLM', 'quote': 'BTC', 'baseId': 'xlm', 'quoteId': 'btc'},
                'XLM/JPY': {'id': 'xlm_jpy', 'symbol': 'XLM/JPY', 'base': 'XLM', 'quote': 'JPY', 'baseId': 'xlm', 'quoteId': 'jpy'},
                'XRP/BTC': {'id': 'xrp_btc', 'symbol': 'XRP/BTC', 'base': 'XRP', 'quote': 'BTC', 'baseId': 'xrp', 'quoteId': 'btc'},
                'XRP/JPY': {'id': 'xrp_jpy', 'symbol': 'XRP/JPY', 'base': 'XRP', 'quote': 'JPY', 'baseId': 'xrp', 'quoteId': 'jpy'},
            },
            'fees': {
                'trading': {
                    'maker': -0.02 / 100,
                    'taker': 0.12 / 100,
                },
                'funding': {
                    'withdraw': {
                        # 'JPY': 756 if (amount > 30000) else 540,
                        'BTC': 0.001,
                        'LTC': 0.001,
                        'XRP': 0.15,
                        'ETH': 0.0005,
                        'MONA': 0.001,
                        'BCC': 0.001,
                    },
                },
            },
            'precision': {
                'price': 8,
                'amount': 8,
            },
            'exceptions': {
                '20001': AuthenticationError,
                '20002': AuthenticationError,
                '20003': AuthenticationError,
                '20005': AuthenticationError,
                '20004': InvalidNonce,
                '40020': InvalidOrder,
                '40021': InvalidOrder,
                '40025': ExchangeError,
                '40013': OrderNotFound,
                '40014': OrderNotFound,
                '50008': PermissionDenied,
                '50009': OrderNotFound,
                '50010': OrderNotFound,
                '60001': InsufficientFunds,
                '60005': InvalidOrder,
            },
        })

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'timestamp')
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetPairTicker(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_ticker(data, market)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        response = self.publicGetPairDepth(self.extend(request, params))
        orderbook = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, timestamp)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'executed_at')
        symbol = None
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        price = self.safe_number(trade, 'price')
        amount = self.safe_number(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = float(self.cost_to_precision(symbol, price * amount))
        id = self.safe_string_2(trade, 'transaction_id', 'trade_id')
        takerOrMaker = self.safe_string(trade, 'maker_taker')
        fee = None
        feeCost = self.safe_number(trade, 'fee_amount_quote')
        if feeCost is not None:
            fee = {
                'currency': feeCurrency,
                'cost': feeCost,
            }
        orderId = self.safe_string(trade, 'order_id')
        type = self.safe_string(trade, 'type')
        side = self.safe_string(trade, 'side')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': type,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetPairTransactions(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = self.safe_value(data, 'transactions', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         "0.02501786",
        #         "0.02501786",
        #         "0.02501786",
        #         "0.02501786",
        #         "0.0000",
        #         1591488000000
        #     ]
        #
        return [
            self.safe_integer(ohlcv, 5),
            self.safe_number(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
        ]

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        date = self.milliseconds()
        date = self.ymd(date)
        date = date.split('-')
        request = {
            'pair': market['id'],
            'candletype': self.timeframes[timeframe],
            'yyyymmdd': ''.join(date),
        }
        response = self.publicGetPairCandlestickCandletypeYyyymmdd(self.extend(request, params))
        #
        #     {
        #         "success":1,
        #         "data":{
        #             "candlestick":[
        #                 {
        #                     "type":"5min",
        #                     "ohlcv":[
        #                         ["0.02501786","0.02501786","0.02501786","0.02501786","0.0000",1591488000000],
        #                         ["0.02501747","0.02501953","0.02501747","0.02501953","0.3017",1591488300000],
        #                         ["0.02501762","0.02501762","0.02500392","0.02500392","0.1500",1591488600000],
        #                     ]
        #                 }
        #             ],
        #             "timestamp":1591508668190
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        candlestick = self.safe_value(data, 'candlestick', [])
        first = self.safe_value(candlestick, 0, {})
        ohlcv = self.safe_value(first, 'ohlcv', [])
        return self.parse_ohlcvs(ohlcv, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUserAssets(params)
        result = {'info': response}
        data = self.safe_value(response, 'data', {})
        assets = self.safe_value(data, 'assets', [])
        for i in range(0, len(assets)):
            balance = assets[i]
            currencyId = self.safe_string(balance, 'asset')
            code = self.safe_currency_code(currencyId)
            account = {
                'free': self.safe_number(balance, 'free_amount'),
                'used': self.safe_number(balance, 'locked_amount'),
                'total': self.safe_number(balance, 'onhand_amount'),
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            'UNFILLED': 'open',
            'PARTIALLY_FILLED': 'open',
            'FULLY_FILLED': 'closed',
            'CANCELED_UNFILLED': 'canceled',
            'CANCELED_PARTIALLY_FILLED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'order_id')
        marketId = self.safe_string(order, 'pair')
        symbol = None
        if marketId and not market and (marketId in self.marketsById):
            market = self.marketsById[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'ordered_at')
        price = self.safe_number(order, 'price')
        amount = self.safe_number(order, 'start_amount')
        filled = self.safe_number(order, 'executed_amount')
        remaining = self.safe_number(order, 'remaining_amount')
        average = self.safe_number(order, 'average_price')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        type = self.safe_string_lower(order, 'type')
        side = self.safe_string_lower(order, 'side')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
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
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        })

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if price is None:
            raise InvalidOrder(self.id + ' createOrder() requires a price argument for both market and limit orders')
        request = {
            'pair': market['id'],
            'amount': self.amount_to_precision(symbol, amount),
            'price': self.price_to_precision(symbol, price),
            'side': side,
            'type': type,
        }
        response = self.privatePostUserSpotOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
        }
        response = self.privatePostUserSpotCancelOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return data

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
        }
        response = self.privateGetUserSpotOrder(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        if since is not None:
            request['since'] = int(since / 1000)
        response = self.privateGetUserSpotActiveOrders(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        orders = self.safe_value(data, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {}
        if market is not None:
            request['pair'] = market['id']
        if limit is not None:
            request['count'] = limit
        if since is not None:
            request['since'] = int(since / 1000)
        response = self.privateGetUserSpotTradeHistory(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = self.safe_value(data, 'trades', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
        }
        response = self.privateGetUserWithdrawalAccount(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        # Not sure about self if there could be more than one account...
        accounts = self.safe_value(data, 'accounts', [])
        firstAccount = self.safe_value(accounts, 0, {})
        address = self.safe_string(firstAccount, 'address')
        return {
            'currency': currency,
            'address': address,
            'tag': None,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        if not ('uuid' in params):
            raise ExchangeError(self.id + ' uuid is required for withdrawal')
        self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
            'amount': amount,
        }
        response = self.privatePostUserRequestWithdrawal(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        txid = self.safe_string(data, 'txid')
        return {
            'info': response,
            'id': txid,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'][api] + '/'
        if api == 'public':
            url += self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce
            url += self.version + '/' + self.implode_params(path, params)
            if method == 'POST':
                body = self.json(query)
                auth += body
            else:
                auth += '/' + self.version + '/' + path
                if query:
                    query = self.urlencode(query)
                    url += '?' + query
                    auth += '?' + query
            headers = {
                'Content-Type': 'application/json',
                'ACCESS-KEY': self.apiKey,
                'ACCESS-NONCE': nonce,
                'ACCESS-SIGNATURE': self.hmac(self.encode(auth), self.encode(self.secret)),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        success = self.safe_integer(response, 'success')
        data = self.safe_value(response, 'data')
        if not success or not data:
            errorMessages = {
                '10000': 'URL does not exist',
                '10001': 'A system error occurred. Please contact support',
                '10002': 'Invalid JSON format. Please check the contents of transmission',
                '10003': 'A system error occurred. Please contact support',
                '10005': 'A timeout error occurred. Please wait for a while and try again',
                '20001': 'API authentication failed',
                '20002': 'Illegal API key',
                '20003': 'API key does not exist',
                '20004': 'API Nonce does not exist',
                '20005': 'API signature does not exist',
                '20011': 'Two-step verification failed',
                '20014': 'SMS authentication failed',
                '30001': 'Please specify the order quantity',
                '30006': 'Please specify the order ID',
                '30007': 'Please specify the order ID array',
                '30009': 'Please specify the stock',
                '30012': 'Please specify the order price',
                '30013': 'Trade Please specify either',
                '30015': 'Please specify the order type',
                '30016': 'Please specify asset name',
                '30019': 'Please specify uuid',
                '30039': 'Please specify the amount to be withdrawn',
                '40001': 'The order quantity is invalid',
                '40006': 'Count value is invalid',
                '40007': 'End time is invalid',
                '40008': 'end_id Value is invalid',
                '40009': 'The from_id value is invalid',
                '40013': 'The order ID is invalid',
                '40014': 'The order ID array is invalid',
                '40015': 'Too many specified orders',
                '40017': 'Incorrect issue name',
                '40020': 'The order price is invalid',
                '40021': 'The trading classification is invalid',
                '40022': 'Start date is invalid',
                '40024': 'The order type is invalid',
                '40025': 'Incorrect asset name',
                '40028': 'uuid is invalid',
                '40048': 'The amount of withdrawal is illegal',
                '50003': 'Currently, self account is in a state where you can not perform the operation you specified. Please contact support',
                '50004': 'Currently, self account is temporarily registered. Please try again after registering your account',
                '50005': 'Currently, self account is locked. Please contact support',
                '50006': 'Currently, self account is locked. Please contact support',
                '50008': 'User identification has not been completed',
                '50009': 'Your order does not exist',
                '50010': 'Can not cancel specified order',
                '50011': 'API not found',
                '60001': 'The number of possessions is insufficient',
                '60002': 'It exceeds the quantity upper limit of the tender buying order',
                '60003': 'The specified quantity exceeds the limit',
                '60004': 'The specified quantity is below the threshold',
                '60005': 'The specified price is above the limit',
                '60006': 'The specified price is below the lower limit',
                '70001': 'A system error occurred. Please contact support',
                '70002': 'A system error occurred. Please contact support',
                '70003': 'A system error occurred. Please contact support',
                '70004': 'We are unable to accept orders as the transaction is currently suspended',
                '70005': 'Order can not be accepted because purchase order is currently suspended',
                '70006': 'We can not accept orders because we are currently unsubscribed ',
                '70009': 'We are currently temporarily restricting orders to be carried out. Please use the limit order.',
                '70010': 'We are temporarily raising the minimum order quantity as the system load is now rising.',
            }
            errorClasses = self.exceptions
            code = self.safe_string(data, 'code')
            message = self.safe_string(errorMessages, code, 'Error')
            ErrorClass = self.safe_value(errorClasses, code)
            if ErrorClass is not None:
                raise ErrorClass(message)
            else:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
