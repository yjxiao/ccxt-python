# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.abstract.btcbox import ImplicitAPI
import hashlib
import json
from ccxt.base.types import OrderSide
from ccxt.base.types import OrderType
from typing import Optional
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce
from ccxt.base.errors import AuthenticationError
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class btcbox(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(btcbox, self).describe(), {
            'id': 'btcbox',
            'name': 'BtcBox',
            'countries': ['JP'],
            'rateLimit': 1000,
            'version': 'v1',
            'pro': False,
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchMarginMode': False,
                'fetchMarkOHLCV': False,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchTrades': True,
                'fetchTransfer': False,
                'fetchTransfers': False,
                'fetchWithdrawal': False,
                'fetchWithdrawals': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'transfer': False,
                'withdraw': False,
                'ws': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87327317-98c55400-c53c-11ea-9a11-81f7d951cc74.jpg',
                'api': {
                    'rest': 'https://www.btcbox.co.jp/api',
                },
                'www': 'https://www.btcbox.co.jp/',
                'doc': 'https://blog.btcbox.jp/en/archives/8762',
                'fees': 'https://support.btcbox.co.jp/hc/en-us/articles/360001235694-Fees-introduction',
            },
            'api': {
                'public': {
                    'get': [
                        'depth',
                        'orders',
                        'ticker',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'trade_add',
                        'trade_cancel',
                        'trade_list',
                        'trade_view',
                        'wallet',
                    ],
                },
            },
            'markets': {
                'BTC/JPY': {'id': 'btc', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY', 'baseId': 'btc', 'quoteId': 'jpy', 'taker': self.parse_number('0.0005'), 'maker': self.parse_number('0.0005'), 'type': 'spot', 'spot': True},
                'ETH/JPY': {'id': 'eth', 'symbol': 'ETH/JPY', 'base': 'ETH', 'quote': 'JPY', 'baseId': 'eth', 'quoteId': 'jpy', 'taker': self.parse_number('0.0010'), 'maker': self.parse_number('0.0010'), 'type': 'spot', 'spot': True},
                'LTC/JPY': {'id': 'ltc', 'symbol': 'LTC/JPY', 'base': 'LTC', 'quote': 'JPY', 'baseId': 'ltc', 'quoteId': 'jpy', 'taker': self.parse_number('0.0010'), 'maker': self.parse_number('0.0010'), 'type': 'spot', 'spot': True},
                'BCH/JPY': {'id': 'bch', 'symbol': 'BCH/JPY', 'base': 'BCH', 'quote': 'JPY', 'baseId': 'bch', 'quoteId': 'jpy', 'taker': self.parse_number('0.0010'), 'maker': self.parse_number('0.0010'), 'type': 'spot', 'spot': True},
            },
            'precisionMode': TICK_SIZE,
            'exceptions': {
                '104': AuthenticationError,
                '105': PermissionDenied,
                '106': InvalidNonce,
                '107': InvalidOrder,  # price should be an integer
                '200': InsufficientFunds,
                '201': InvalidOrder,  # amount too small
                '202': InvalidOrder,  # price should be [0 : 1000000]
                '203': OrderNotFound,
                '401': OrderNotFound,  # cancel canceled, closed or non-existent order
                '402': DDoSProtection,
            },
        })

    def parse_balance(self, response):
        result = {'info': response}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            currencyId = currency['id']
            free = currencyId + '_balance'
            if free in response:
                account = self.account()
                used = currencyId + '_lock'
                account['free'] = self.safe_string(response, free)
                account['used'] = self.safe_string(response, used)
                result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: a `balance structure <https://github.com/ccxt/ccxt/wiki/Manual#balance-structure>`
        """
        await self.load_markets()
        response = await self.privatePostBalance(params)
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        response = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'])

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = self.safe_symbol(None, market)
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'vol'),
            'quoteVolume': self.safe_string(ticker, 'volume'),
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol: str, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        response = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #      {
        #          "date":"0",
        #          "price":3,
        #          "amount":0.1,
        #          "tid":"1",
        #          "type":"buy"
        #      }
        #
        timestamp = self.safe_timestamp(trade, 'date')
        market = self.safe_market(None, market)
        id = self.safe_string(trade, 'tid')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        type = None
        side = self.safe_string(trade, 'type')
        return self.safe_trade({
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': None,
        }, market)

    async def fetch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns Trade[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        response = await self.publicGetOrders(self.extend(request, params))
        #
        #     [
        #          {
        #              "date":"0",
        #              "price":3,
        #              "amount":0.1,
        #              "tid":"1",
        #              "type":"buy"
        #          },
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float [price]: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: an `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'amount': amount,
            'price': price,
            'type': side,
            'coin': market['baseId'],
        }
        response = await self.privatePostTradeAdd(self.extend(request, params))
        #
        #     {
        #         "result":true,
        #         "id":"11"
        #     }
        #
        return self.parse_order(response, market)

    async def cancel_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        # a special case for btcbox – default symbol is BTC/JPY
        if symbol is None:
            symbol = 'BTC/JPY'
        market = self.market(symbol)
        request = {
            'id': id,
            'coin': market['baseId'],
        }
        response = await self.privatePostTradeCancel(self.extend(request, params))
        #
        #     {"result":true, "id":"11"}
        #
        return self.parse_order(response, market)

    def parse_order_status(self, status):
        statuses = {
            # TODO: complete list
            'part': 'open',  # partially or not at all executed
            'all': 'closed',  # fully executed
            'cancelled': 'canceled',
            'closed': 'closed',  # never encountered, seems to be bug in the doc
            'no': 'closed',  # not clarified in the docs...
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "id":11,
        #         "datetime":"2014-10-21 10:47:20",
        #         "type":"sell",
        #         "price":42000,
        #         "amount_original":1.2,
        #         "amount_outstanding":1.2,
        #         "status":"closed",
        #         "trades":[]  # no clarification of trade value structure of order endpoint
        #     }
        #
        id = self.safe_string(order, 'id')
        datetimeString = self.safe_string(order, 'datetime')
        timestamp = None
        if datetimeString is not None:
            timestamp = self.parse8601(order['datetime'] + '+09:00')  # Tokyo time
        amount = self.safe_string(order, 'amount_original')
        remaining = self.safe_string(order, 'amount_outstanding')
        price = self.safe_string(order, 'price')
        # status is set by fetchOrder method only
        status = self.parse_order_status(self.safe_string(order, 'status'))
        # fetchOrders do not return status, use heuristic
        if status is None:
            if Precise.string_equals(remaining, '0'):
                status = 'closed'
        trades = None  # todo: self.parse_trades(order['trades'])
        market = self.safe_market(None, market)
        side = self.safe_string(order, 'type')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'amount': amount,
            'remaining': remaining,
            'filled': None,
            'side': side,
            'type': None,
            'timeInForce': None,
            'postOnly': None,
            'status': status,
            'symbol': market['symbol'],
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'cost': None,
            'trades': trades,
            'fee': None,
            'info': order,
            'average': None,
        }, market)

    async def fetch_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        # a special case for btcbox – default symbol is BTC/JPY
        if symbol is None:
            symbol = 'BTC/JPY'
        market = self.market(symbol)
        request = self.extend({
            'id': id,
            'coin': market['baseId'],
        }, params)
        response = await self.privatePostTradeView(self.extend(request, params))
        #
        #      {
        #          "id":11,
        #          "datetime":"2014-10-21 10:47:20",
        #          "type":"sell",
        #          "price":42000,
        #          "amount_original":1.2,
        #          "amount_outstanding":1.2,
        #          "status":"closed",
        #          "trades":[]
        #      }
        #
        return self.parse_order(response, market)

    async def fetch_orders_by_type(self, type, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        await self.load_markets()
        # a special case for btcbox – default symbol is BTC/JPY
        if symbol is None:
            symbol = 'BTC/JPY'
        market = self.market(symbol)
        request = {
            'type': type,  # 'open' or 'all'
            'coin': market['baseId'],
        }
        response = await self.privatePostTradeList(self.extend(request, params))
        #
        # [
        #      {
        #          "id":"7",
        #          "datetime":"2014-10-20 13:27:38",
        #          "type":"buy",
        #          "price":42750,
        #          "amount_original":0.235,
        #          "amount_outstanding":0.235
        #      },
        # ]
        #
        orders = self.parse_orders(response, market, since, limit)
        # status(open/closed/canceled) is None
        # btcbox does not return status, but we know it's 'open' queried for open orders
        if type == 'open':
            for i in range(0, len(orders)):
                orders[i]['status'] = 'open'
        return orders

    async def fetch_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of  orde structures to retrieve
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns Order[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        return await self.fetch_orders_by_type('all', symbol, since, limit, params)

    async def fetch_open_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of  open orders structures to retrieve
        :param dict [params]: extra parameters specific to the btcbox api endpoint
        :returns Order[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        return await self.fetch_orders_by_type('open', symbol, since, limit, params)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']['rest'] + '/' + self.version + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            query = self.extend({
                'key': self.apiKey,
                'nonce': nonce,
            }, params)
            request = self.urlencode(query)
            secret = self.hash(self.encode(self.secret), 'sha256')
            query['signature'] = self.hmac(self.encode(request), self.encode(secret), hashlib.sha256)
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return None  # resort to defaultErrorHandler
        # typical error response: {"result":false,"code":"401"}
        if httpCode >= 400:
            return None  # resort to defaultErrorHandler
        result = self.safe_value(response, 'result')
        if result is None or result is True:
            return None  # either public API(no error codes expected) or success
        code = self.safe_value(response, 'code')
        feedback = self.id + ' ' + body
        self.throw_exactly_matched_exception(self.exceptions, code, feedback)
        raise ExchangeError(feedback)  # unknown message

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None, config={}):
        response = await self.fetch2(path, api, method, params, headers, body, config)
        if isinstance(response, str):
            # sometimes the exchange returns whitespace prepended to json
            response = self.strip(response)
            if not self.is_json_encoded_object(response):
                raise ExchangeError(self.id + ' ' + response)
            response = json.loads(response)
        return response
