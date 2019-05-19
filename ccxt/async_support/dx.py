# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import RequestTimeout
from ccxt.base.decimal_to_precision import ROUND
from ccxt.base.decimal_to_precision import DECIMAL_PLACES
from ccxt.base.decimal_to_precision import NO_PADDING


class dx (Exchange):

    def describe(self):
        return self.deep_extend(super(dx, self).describe(), {
            'id': 'dx',
            'name': 'DX.Exchange',
            'countries': ['GB', 'EU'],
            'rateLimit': 1500,
            'version': 'v1',
            'has': {
                'cancelAllOrders': False,
                'cancelOrder': True,
                'cancelOrders': False,
                'CORS': False,
                'createDepositAddress': False,
                'createLimitOrder': True,
                'createMarketOrder': True,
                'createOrder': True,
                'deposit': False,
                'editOrder': False,
                'fetchBalance': True,
                'fetchBidsAsks': False,
                'fetchClosedOrders': True,
                'fetchCurrencies': False,
                'fetchDepositAddress': False,
                'fetchDeposits': False,
                'fetchFundingFees': False,
                'fetchL2OrderBook': False,
                'fetchLedger': False,
                'fetchMarkets': True,
                'fetchMyTrades': False,
                'fetchOHLCV': True,
                'fetchOpenOrders': False,
                'fetchOrder': False,
                'fetchOrderBook': False,
                'fetchOrderBooks': False,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchTrades': False,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'fetchTradingLimits': False,
                'fetchTransactions': False,
                'fetchWithdrawals': False,
                'privateAPI': True,
                'publicAPI': True,
                'withdraw': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '1h': '1h',
                '1d': '1d',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/57979980-6483ff80-7a2d-11e9-9224-2aa20665703b.jpg',
                'api': 'https://acl.dx.exchange',
                'www': 'https://dx.exchange',
                'doc': 'https://apidocs.dx.exchange/',
                'fees': 'https://dx.exchange/fees',
                'referral': 'https://dx.exchange/registration?dx_cid=20&dx_scname=100001100000038139',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                    'tiers': {
                        'taker': [
                            [0, 0.25 / 100],
                            [1000000, 0.2 / 100],
                            [5000000, 0.15 / 100],
                            [10000000, 0.1 / 100],
                        ],
                        'maker': [
                            [0, 0.25 / 100],
                            [1000000, 0.2 / 100],
                            [5000000, 0.15 / 100],
                            [10000000, 0.1 / 100],
                        ],
                    },
                },
                'funding': {
                },
            },
            'exceptions': {
                'exact': {
                    'EOF': BadRequest,
                },
                'broad': {
                    'json: cannot unmarshal object into Go value of type': BadRequest,
                    'not allowed to cancel self order': BadRequest,
                    'request timed out': RequestTimeout,
                    'balance_freezing.freezing validation.balance_freeze': InsufficientFunds,
                    'order_creation.validation.validation': InvalidOrder,
                },
            },
            'api': {
                'public': {
                    'post': [
                        'AssetManagement.GetInstruments',
                        'AssetManagement.GetTicker',
                        'AssetManagement.History',
                        'Authorization.LoginByToken',
                    ],
                },
                'private': {
                    'post': [
                        'Balance.Get',
                        'OrderManagement.Cancel',
                        'OrderManagement.Create',
                        'OrderManagement.OpenOrders',
                        'OrderManagement.OrderHistory',
                    ],
                },
            },
            'commonCurrencies': {
                'BCH': 'Bitcoin Cash',
            },
            'precisionMode': DECIMAL_PLACES,
            'options': {
                'orderTypes': {
                    'market': 1,
                    'limit': 2,
                },
                'orderSide': {
                    'buy': 1,
                    'sell': 2,
                },
            },
        })

    def number_to_object(self, number):
        string = self.decimal_to_precision(number, ROUND, 10, DECIMAL_PLACES, NO_PADDING)
        decimals = self.precision_from_string(string)
        valueStr = string.replace('.', '')
        return {
            'value': self.safe_integer({'a': valueStr}, 'a', None),
            'decimals': decimals,
        }

    def object_to_number(self, obj):
        value = self.decimal_to_precision(obj['value'], ROUND, 0, DECIMAL_PLACES, NO_PADDING)
        decimals = self.decimal_to_precision(-obj['decimals'], ROUND, 0, DECIMAL_PLACES, NO_PADDING)
        return self.safe_float({
            'a': value + 'e' + decimals,
        }, 'a', None)

    async def fetch_markets(self, params={}):
        markets = await self.publicPostAssetManagementGetInstruments(params)
        instruments = markets['result']['instruments']
        result = []
        for i in range(0, len(instruments)):
            instrument = instruments[i]
            id = instrument['id']
            symbol = instrument['asset']['fullName']
            base, quote = symbol.split('/')
            amountPrecision = 0
            if instrument['meQuantityMultiplier'] != 0:
                amountPrecision = math.log10(instrument['meQuantityMultiplier'])
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': instrument['asset']['baseCurrencyId'],
                'quoteId': instrument['asset']['quotedCurrencyId'],
                'info': instrument,
                'precision': {
                    'amount': amountPrecision,
                    'price': instrument['asset']['tailDigits'],
                },
                'limits': {
                    'amount': {
                        'min': instrument['minOrderQuantity'],
                        'max': instrument['maxOrderQuantity'],
                    },
                    'price': {
                        'min': 0,
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
            })
        return result

    def parse_ticker(self, ticker, market=None):
        tickerKeys = list(ticker.keys())
        # Python needs an integer to access self.markets_by_id
        # and a string to access the ticker object
        tickerKey = tickerKeys[0]
        instrumentId = self.safe_integer({'a': tickerKey}, 'a')
        ticker = ticker[tickerKey]
        symbol = self.markets_by_id[instrumentId]['symbol']
        last = self.safe_float(ticker, 'last')
        timestamp = self.safe_integer(ticker, 'time') / 1000
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24'),
            'low': self.safe_float(ticker, 'low24'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'change'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume24'),
            'quoteVolume': self.safe_float(ticker, 'volume24converted'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'instrumentIds': [market['id']],
            'currencyId': market['quoteId'],
        }
        response = await self.publicPostAssetManagementGetTicker(self.extend(request, params))
        return self.parse_ticker(response['result']['tickers'], market)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_float(ohlcv, 'date') * 1000,
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'timestampFrom': since,
            'timestampTill': None,
            'instrumentId': market['id'],
            'type': self.timeframes[timeframe],
            'pagination': {
                'limit': limit,
                'offset': 0,
            },
        }
        response = await self.publicPostAssetManagementHistory(self.extend(request, params))
        return self.parse_ohlcvs(response['result']['assets'], market, timeframe, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'pagination': {
                'limit': limit,
                'offset': 0,
            },
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['instrumentId'] = market['id']
        response = await self.privatePostOrderManagementOpenOrders(self.extend(request, params))
        return self.parse_orders(response['result']['orders'], market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'pagination': {
                'limit': limit,
                'offset': 0,
            },
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['instrumentId'] = market['id']
        response = await self.privatePostOrderManagementOrderHistory(self.extend(request, params))
        return self.parse_orders(response['result']['ordersForHistory'], market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        openOrders = await self.fetch_open_orders(symbol, since, limit, params)
        orders = await self.fetch_closed_orders(symbol, since, limit, params)
        return self.array_concat(orders, openOrders)

    def parse_order(self, order, market=None):
        orderStatusMap = {
            '1': 'open',
        }
        innerOrder = self.safe_value_2(order, 'order', None)
        if innerOrder is not None:
            # fetchClosedOrders returns orders in an extra object
            order = innerOrder
            orderStatusMap = {
                '1': 'closed',
                '2': 'canceled',
            }
        side = 'buy'
        if order['direction'] == self.options['orderSide']['sell']:
            side = 'sell'
        status = None
        orderStatus = self.safe_string(order, 'status', None)
        if orderStatus in orderStatusMap:
            status = orderStatusMap[orderStatus]
        symbol = self.markets_by_id[order['instrumentId']]['symbol']
        orderType = 'limit'
        if order['orderType'] == self.options['orderTypes']['market']:
            orderType = 'market'
        timestamp = order['time'] * 1000
        quantity = self.object_to_number(order['quantity'])
        filledQuantity = self.object_to_number(order['filledQuantity'])
        result = {
            'info': order,
            'id': order['externalOrderId'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': orderType,
            'side': side,
            'price': self.object_to_number(order['price']),
            'average': None,
            'amount': quantity,
            'remaining': quantity - filledQuantity,
            'filled': filledQuantity,
            'status': status,
            'fee': None,
        }
        return result

    async def sign_in(self, params={}):
        self.check_required_credentials()
        result = await self.publicPostAuthorizationLoginByToken(self.extend({
            'token': self.apiKey,
            'secret': self.secret,
        }, params))
        expiresIn = result['result']['expiry']
        self.options['expires'] = self.sum(self.milliseconds(), expiresIn * 1000)
        self.options['accessToken'] = result['result']['token']
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostBalanceGet(params)
        result = {'info': response}
        balances = response['result']['balance']
        balancesKeys = list(balances.keys())
        for i in range(0, len(balancesKeys)):
            instrumentId = balancesKeys[i]
            balance = balances[instrumentId]
            symbol = instrumentId
            if instrumentId in self.currencies_by_id:
                symbol = self.currencies_by_id[instrumentId]['code']
            account = {
                'free': float(balance['available']),
                'used': float(balance['frozen']),
                'total': float(balance['total']),
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[symbol] = account
        return self.parse_balance(result)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        direction = self.options['orderSide'][side]
        order = {
            'order': {
                'direction': direction,
                'instrumentId': self.market_id(symbol),
                'orderType': 2,
                'quantity': self.number_to_object(amount),
            },
        }
        order['order']['orderType'] = self.options['orderTypes'][type]
        if type == 'limit':
            order['order']['price'] = self.number_to_object(price)
        result = await self.privatePostOrderManagementCreate(self.extend(order, params))
        return {
            'info': result,
            'id': result['result']['externalOrderId'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        return await self.privatePostOrderManagementCancel({'externalOrderId': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if isinstance(params, list):
            arrayLength = len(params)
            if arrayLength == 0:
                # In PHP params = array() causes self to fail, because
                # the API requests an object, not an array, even if it is empty
                params = {'__associative': True}
        parameters = {
            'jsonrpc': '2.0',
            'id': self.milliseconds(),
            'method': path,
            'params': [params],
        }
        url = self.urls['api']
        headers = {'Content-Type': 'application/json-rpc'}
        if method == 'GET':
            if parameters:
                url += '?' + self.urlencode(parameters)
        else:
            body = self.json(parameters)
        if api == 'private':
            token = self.safe_string(self.options, 'accessToken')
            if token is None:
                raise AuthenticationError(self.id + ' ' + path + ' endpoint requires a prior call to signIn() method')
            expires = self.safe_integer(self.options, 'expires')
            if expires is not None:
                if self.milliseconds() >= expires:
                    raise AuthenticationError(self.id + ' accessToken expired, call signIn() method')
            headers['Authorization'] = token
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if not response:
            return  # fallback to default error handler
        error = response['error']
        if error:
            feedback = self.id + ' ' + self.json(response)
            exact = self.exceptions['exact']
            if error in exact:
                raise exact[error](feedback)
            broad = self.exceptions['broad']
            broadKey = self.findBroadlyMatchedKey(broad, error)
            if broadKey is not None:
                raise broad[broadKey](feedback)
            raise ExchangeError(feedback)  # unknown error
