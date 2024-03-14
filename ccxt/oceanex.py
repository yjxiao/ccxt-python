# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.abstract.oceanex import ImplicitAPI
from ccxt.base.types import Balances, Int, Market, Num, Order, OrderBook, OrderSide, OrderType, Str, Strings, Ticker, Tickers, Trade
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import AuthenticationError
from ccxt.base.decimal_to_precision import TICK_SIZE


class oceanex(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(oceanex, self).describe(), {
            'id': 'oceanex',
            'name': 'OceanEx',
            'countries': ['BS'],  # Bahamas
            'version': 'v1',
            'rateLimit': 3000,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/58385970-794e2d80-8001-11e9-889c-0567cd79b78e.jpg',
                'api': {
                    'rest': 'https://api.oceanex.pro',
                },
                'www': 'https://www.oceanex.pro.com',
                'doc': 'https://api.oceanex.pro/doc/v1',
                'referral': 'https://oceanex.pro/signup?referral=VE24QX',
            },
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': None,  # has but unimplemented
                'future': None,
                'option': None,
                'cancelAllOrders': True,
                'cancelOrder': True,
                'cancelOrders': True,
                'createMarketOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchClosedOrders': True,
                'fetchCrossBorrowRate': False,
                'fetchCrossBorrowRates': False,
                'fetchDepositAddress': False,
                'fetchDepositAddresses': False,
                'fetchDepositAddressesByNetwork': False,
                'fetchIsolatedBorrowRate': False,
                'fetchIsolatedBorrowRates': False,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': True,
                'fetchTransactionFees': None,
            },
            'timeframes': {
                '1m': '1',
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '2h': '120',
                '4h': '240',
                '6h': '360',
                '12h': '720',
                '1d': '1440',
                '3d': '4320',
                '1w': '10080',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'tickers/{pair}',
                        'tickers_multi',
                        'order_book',
                        'order_book/multi',
                        'fees/trading',
                        'trades',
                        'timestamp',
                    ],
                    'post': [
                        'k',
                    ],
                },
                'private': {
                    'get': [
                        'key',
                        'members/me',
                        'orders',
                        'orders/filter',
                    ],
                    'post': [
                        'orders',
                        'orders/multi',
                        'order/delete',
                        'order/delete/multi',
                        'orders/clear',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': self.parse_number('0.001'),
                    'taker': self.parse_number('0.001'),
                },
            },
            'commonCurrencies': {
                'PLA': 'Plair',
            },
            'precisionMode': TICK_SIZE,
            'exceptions': {
                'codes': {
                    '-1': BadRequest,
                    '-2': BadRequest,
                    '1001': BadRequest,
                    '1004': ArgumentsRequired,
                    '1006': AuthenticationError,
                    '1008': AuthenticationError,
                    '1010': AuthenticationError,
                    '1011': PermissionDenied,
                    '2001': AuthenticationError,
                    '2002': InvalidOrder,
                    '2004': OrderNotFound,
                    '9003': PermissionDenied,
                },
                'exact': {
                    'market does not have a valid value': BadRequest,
                    'side does not have a valid value': BadRequest,
                    'Account::AccountError: Cannot lock funds': InsufficientFunds,
                    'The account does not exist': AuthenticationError,
                },
            },
        })

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for oceanex
        :see: https://api.oceanex.pro/doc/v1/#markets-post
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: an array of objects representing market data
        """
        request = {'show_details': True}
        response = self.publicGetMarkets(self.extend(request, params))
        #
        #    {
        #        "id": "xtzusdt",
        #        "name": "XTZ/USDT",
        #        "ask_precision": "8",
        #        "bid_precision": "8",
        #        "enabled": True,
        #        "price_precision": "4",
        #        "amount_precision": "3",
        #        "usd_precision": "4",
        #        "minimum_trading_amount": "1.0"
        #    },
        #
        markets = self.safe_value(response, 'data', [])
        return self.parse_markets(markets)

    def parse_market(self, market) -> Market:
        id = self.safe_value(market, 'id')
        name = self.safe_value(market, 'name')
        baseId, quoteId = name.split('/')
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        baseId = baseId.lower()
        quoteId = quoteId.lower()
        symbol = base + '/' + quote
        return {
            'id': id,
            'symbol': symbol,
            'base': base,
            'quote': quote,
            'settle': None,
            'baseId': baseId,
            'quoteId': quoteId,
            'settleId': None,
            'type': 'spot',
            'spot': True,
            'margin': False,
            'swap': False,
            'future': False,
            'option': False,
            'active': None,
            'contract': False,
            'linear': None,
            'inverse': None,
            'contractSize': None,
            'expiry': None,
            'expiryDatetime': None,
            'strike': None,
            'optionType': None,
            'precision': {
                'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'amount_precision'))),
                'price': self.parse_number(self.parse_precision(self.safe_string(market, 'price_precision'))),
            },
            'limits': {
                'leverage': {
                    'min': None,
                    'max': None,
                },
                'amount': {
                    'min': None,
                    'max': None,
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': self.safe_number(market, 'minimum_trading_amount'),
                    'max': None,
                },
            },
            'created': None,
            'info': market,
        }

    def fetch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://api.oceanex.pro/doc/v1/#ticker-post
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetTickersPair(self.extend(request, params))
        #
        #     {
        #         "code":0,
        #         "message":"Operation successful",
        #         "data": {
        #             "at":1559431729,
        #             "ticker": {
        #                 "buy":"0.0065",
        #                 "sell":"0.00677",
        #                 "low":"0.00677",
        #                 "high":"0.00677",
        #                 "last":"0.00677",
        #                 "vol":"2000.0"
        #             }
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_ticker(data, market)

    def fetch_tickers(self, symbols: Strings = None, params={}) -> Tickers:
        """
        fetches price tickers for multiple markets, statistical information calculated over the past 24 hours for each market
        :see: https://api.oceanex.pro/doc/v1/#multiple-tickers-post
        :param str[]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a dictionary of `ticker structures <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        if symbols is None:
            symbols = self.symbols
        marketIds = self.market_ids(symbols)
        request = {'markets': marketIds}
        response = self.publicGetTickersMulti(self.extend(request, params))
        #
        #     {
        #         "code":0,
        #         "message":"Operation successful",
        #         "data": {
        #             "at":1559431729,
        #             "ticker": {
        #                 "buy":"0.0065",
        #                 "sell":"0.00677",
        #                 "low":"0.00677",
        #                 "high":"0.00677",
        #                 "last":"0.00677",
        #                 "vol":"2000.0"
        #             }
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            ticker = data[i]
            marketId = self.safe_string(ticker, 'market')
            market = self.safe_market(marketId)
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array_tickers(result, 'symbol', symbols)

    def parse_ticker(self, data, market: Market = None):
        #
        #         {
        #             "at":1559431729,
        #             "ticker": {
        #                 "buy":"0.0065",
        #                 "sell":"0.00677",
        #                 "low":"0.00677",
        #                 "high":"0.00677",
        #                 "last":"0.00677",
        #                 "vol":"2000.0"
        #             }
        #         }
        #
        ticker = self.safe_value(data, 'ticker', {})
        timestamp = self.safe_timestamp(data, 'at')
        symbol = self.safe_symbol(None, market)
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
            'close': self.safe_string(ticker, 'last'),
            'last': self.safe_string(ticker, 'last'),
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    def fetch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://api.oceanex.pro/doc/v1/#order-book-post
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetOrderBook(self.extend(request, params))
        #
        #     {
        #         "code":0,
        #         "message":"Operation successful",
        #         "data": {
        #             "timestamp":1559433057,
        #             "asks": [
        #                 ["100.0","20.0"],
        #                 ["4.74","2000.0"],
        #                 ["1.74","4000.0"],
        #             ],
        #             "bids":[
        #                 ["0.0065","5482873.4"],
        #                 ["0.00649","4781956.2"],
        #                 ["0.00648","2876006.8"],
        #             ],
        #         }
        #     }
        #
        orderbook = self.safe_value(response, 'data', {})
        timestamp = self.safe_timestamp(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, symbol, timestamp)

    def fetch_order_books(self, symbols: Strings = None, limit: Int = None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data for multiple markets
        :see: https://api.oceanex.pro/doc/v1/#multiple-order-books-post
        :param str[]|None symbols: list of unified market symbols, all symbols fetched if None, default is None
        :param int [limit]: max number of entries per orderbook to return, default is None
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbol
        """
        self.load_markets()
        if symbols is None:
            symbols = self.symbols
        marketIds = self.market_ids(symbols)
        request = {
            'markets': marketIds,
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetOrderBookMulti(self.extend(request, params))
        #
        #     {
        #         "code":0,
        #         "message":"Operation successful",
        #         "data": [
        #             {
        #                 "timestamp":1559433057,
        #                 "market": "bagvet",
        #                 "asks": [
        #                     ["100.0","20.0"],
        #                     ["4.74","2000.0"],
        #                     ["1.74","4000.0"],
        #                 ],
        #                 "bids":[
        #                     ["0.0065","5482873.4"],
        #                     ["0.00649","4781956.2"],
        #                     ["0.00648","2876006.8"],
        #                 ],
        #             },
        #             ...,
        #         ],
        #     }
        #
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            orderbook = data[i]
            marketId = self.safe_string(orderbook, 'market')
            symbol = self.safe_symbol(marketId)
            timestamp = self.safe_timestamp(orderbook, 'timestamp')
            result[symbol] = self.parse_order_book(orderbook, symbol, timestamp)
        return result

    def fetch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :see: https://api.oceanex.pro/doc/v1/#trades-post
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Trade[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = min(limit, 1000)
        response = self.publicGetTrades(self.extend(request, params))
        #
        #      {
        #          "code":0,
        #          "message":"Operation successful",
        #          "data": [
        #              {
        #                  "id":220247666,
        #                  "price":"3098.62",
        #                  "volume":"0.00196",
        #                  "funds":"6.0732952",
        #                  "market":"ethusdt",
        #                  "created_at":"2022-04-19T19:03:15Z",
        #                  "created_on":1650394995,
        #                  "side":"bid"
        #              },
        #          ]
        #      }
        #
        data = self.safe_value(response, 'data')
        return self.parse_trades(data, market, since, limit)

    def parse_trade(self, trade, market: Market = None) -> Trade:
        #
        # fetchTrades(public)
        #
        #      {
        #          "id":220247666,
        #          "price":"3098.62",
        #          "volume":"0.00196",
        #          "funds":"6.0732952",
        #          "market":"ethusdt",
        #          "created_at":"2022-04-19T19:03:15Z",
        #          "created_on":1650394995,
        #          "side":"bid"
        #      }
        #
        side = self.safe_value(trade, 'side')
        if side == 'bid':
            side = 'buy'
        elif side == 'ask':
            side = 'sell'
        marketId = self.safe_value(trade, 'market')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.safe_timestamp(trade, 'created_on')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'volume')
        return self.safe_trade({
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'id'),
            'order': None,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': None,
        }, market)

    def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :see: https://api.oceanex.pro/doc/v1/#api-server-time-post
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = self.publicGetTimestamp(params)
        #
        #     {"code":0,"message":"Operation successful","data":1559433420}
        #
        return self.safe_timestamp(response, 'data')

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :see: https://api.oceanex.pro/doc/v1/#trading-fees-post
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/#/?id=fee-structure>` indexed by market symbols
        """
        response = self.publicGetFeesTrading(params)
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            group = data[i]
            maker = self.safe_value(group, 'ask_fee', {})
            taker = self.safe_value(group, 'bid_fee', {})
            marketId = self.safe_string(group, 'market')
            symbol = self.safe_symbol(marketId)
            result[symbol] = {
                'info': group,
                'symbol': symbol,
                'maker': self.safe_number(maker, 'value'),
                'taker': self.safe_number(taker, 'value'),
                'percentage': True,
            }
        return result

    def fetch_key(self, params={}):
        response = self.privateGetKey(params)
        return self.safe_value(response, 'data')

    def parse_balance(self, response) -> Balances:
        data = self.safe_value(response, 'data')
        balances = self.safe_value(data, 'accounts', [])
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_value(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'balance')
            account['used'] = self.safe_string(balance, 'locked')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}) -> Balances:
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :see: https://api.oceanex.pro/doc/v1/#account-info-post
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/#/?id=balance-structure>`
        """
        self.load_markets()
        response = self.privateGetMembersMe(params)
        return self.parse_balance(response)

    def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        """
        create a trade order
        :see: https://api.oceanex.pro/doc/v1/#new-order-post
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float [price]: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'side': side,
            'ord_type': type,
            'volume': self.amount_to_precision(symbol, amount),
        }
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrders(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data, market)

    def fetch_order(self, id: str, symbol: Str = None, params={}):
        """
        fetches information on an order made by the user
        :see: https://api.oceanex.pro/doc/v1/#order-status-get
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        ids = [id]
        request = {'ids': ids}
        response = self.privateGetOrders(self.extend(request, params))
        data = self.safe_value(response, 'data')
        dataLength = len(data)
        if data is None:
            raise OrderNotFound(self.id + ' could not found matching order')
        if isinstance(id, list):
            orders = self.parse_orders(data, market)
            return orders[0]
        if dataLength == 0:
            raise OrderNotFound(self.id + ' could not found matching order')
        return self.parse_order(data[0], market)

    def fetch_open_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetch all unfilled currently open orders
        :see: https://api.oceanex.pro/doc/v1/#order-status-get
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of  open orders structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'states': ['wait'],
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetches information on multiple closed orders made by the user
        :see: https://api.oceanex.pro/doc/v1/#order-status-get
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'states': ['done', 'cancel'],
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetches information on multiple orders made by the user
        :see: https://api.oceanex.pro/doc/v1/#order-status-with-filters-post
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        states = self.safe_value(params, 'states', ['wait', 'done', 'cancel'])
        query = self.omit(params, 'states')
        request = {
            'market': market['id'],
            'states': states,
            'need_price': 'True',
        }
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetOrdersFilter(self.extend(request, query))
        data = self.safe_value(response, 'data', [])
        result = []
        for i in range(0, len(data)):
            orders = self.safe_value(data[i], 'orders', [])
            status = self.parse_order_status(self.safe_value(data[i], 'state'))
            parsedOrders = self.parse_orders(orders, market, since, limit, {'status': status})
            result = self.array_concat(result, parsedOrders)
        return result

    def parse_ohlcv(self, ohlcv, market: Market = None) -> list:
        # [
        #    1559232000,
        #    8889.22,
        #    9028.52,
        #    8889.22,
        #    9028.52
        #    0.3121
        # ]
        return [
            self.safe_timestamp(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
            self.safe_number(ohlcv, 5),
        ]

    def fetch_ohlcv(self, symbol: str, timeframe='1m', since: Int = None, limit: Int = None, params={}) -> List[list]:
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :see: https://api.oceanex.pro/doc/v1/#k-line-post
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'period': self.safe_string(self.timeframes, timeframe, timeframe),
        }
        if since is not None:
            request['timestamp'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.publicPostK(self.extend(request, params))
        ohlcvs = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)

    def parse_order(self, order, market: Market = None) -> Order:
        #
        #     {
        #         "created_at": "2019-01-18T00:38:18Z",
        #         "trades_count": 0,
        #         "remaining_volume": "0.2",
        #         "price": "1001.0",
        #         "created_on": "1547771898",
        #         "side": "buy",
        #         "volume": "0.2",
        #         "state": "wait",
        #         "ord_type": "limit",
        #         "avg_price": "0.0",
        #         "executed_volume": "0.0",
        #         "id": 473797,
        #         "market": "veteth"
        #     }
        #
        status = self.parse_order_status(self.safe_value(order, 'state'))
        marketId = self.safe_string_2(order, 'market', 'market_id')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.safe_timestamp(order, 'created_on')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        price = self.safe_string(order, 'price')
        average = self.safe_string(order, 'avg_price')
        amount = self.safe_string(order, 'volume')
        remaining = self.safe_string(order, 'remaining_volume')
        filled = self.safe_string(order, 'executed_volume')
        return self.safe_order({
            'info': order,
            'id': self.safe_string(order, 'id'),
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': self.safe_value(order, 'ord_type'),
            'timeInForce': None,
            'postOnly': None,
            'side': self.safe_value(order, 'side'),
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'average': average,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'status': status,
            'cost': None,
            'trades': None,
            'fee': None,
        }, market)

    def parse_order_status(self, status):
        statuses = {
            'wait': 'open',
            'done': 'closed',
            'cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def cancel_order(self, id: str, symbol: Str = None, params={}):
        """
        cancels an open order
        :see: https://api.oceanex.pro/doc/v1/#cancel-order-post
        :param str id: order id
        :param str symbol: not used by oceanex cancelOrder()
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        response = self.privatePostOrderDelete(self.extend({'id': id}, params))
        data = self.safe_value(response, 'data')
        return self.parse_order(data)

    def cancel_orders(self, ids, symbol: Str = None, params={}):
        """
        cancel multiple orders
        :see: https://api.oceanex.pro/doc/v1/#cancel-multiple-orders-post
        :param str[] ids: order ids
        :param str symbol: not used by oceanex cancelOrders()
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        response = self.privatePostOrderDeleteMulti(self.extend({'ids': ids}, params))
        data = self.safe_value(response, 'data')
        return self.parse_orders(data)

    def cancel_all_orders(self, symbol: Str = None, params={}):
        """
        cancel all open orders
        :see: https://api.oceanex.pro/doc/v1/#cancel-all-orders-post
        :param str symbol: unified market symbol, only orders in the market of self symbol are cancelled when symbol is not None
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        response = self.privatePostOrdersClear(params)
        data = self.safe_value(response, 'data')
        return self.parse_orders(data)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']['rest'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if path == 'tickers_multi' or path == 'order_book/multi':
                request = '?'
                markets = self.safe_value(params, 'markets')
                for i in range(0, len(markets)):
                    request += 'markets[]=' + markets[i] + '&'
                limit = self.safe_value(params, 'limit')
                if limit is not None:
                    request += 'limit=' + limit
                url += request
            elif query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            request = {
                'uid': self.apiKey,
                'data': query,
            }
            # to set the private key:
            # fs = require('fs')
            # exchange.secret = fs.readFileSync('oceanex.pem', 'utf8')
            jwt_token = self.jwt(request, self.encode(self.secret), 'sha256', True)
            url += '?user_jwt=' + jwt_token
        headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        #
        #     {"code":1011,"message":"This IP 'x.x.x.x' is not allowed","data":{}}
        #
        if response is None:
            return None
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'message')
        if (errorCode is not None) and (errorCode != '0'):
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['codes'], errorCode, feedback)
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            raise ExchangeError(feedback)
        return None
