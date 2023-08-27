# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.abstract.coinone import ImplicitAPI
import hashlib
from ccxt.base.types import OrderSide
from ccxt.base.types import OrderType
from typing import Optional
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OnMaintenance
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class coinone(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(coinone, self).describe(), {
            'id': 'coinone',
            'name': 'CoinOne',
            'countries': ['KR'],  # Korea
            # 'enableRateLimit': False,
            'rateLimit': 667,
            'version': 'v2',
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
                'createMarketOrder': False,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'createStopLimitOrder': False,
                'createStopMarketOrder': False,
                'createStopOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchClosedOrders': False,  # the endpoint that should return closed orders actually returns trades, https://github.com/ccxt/ccxt/pull/7067
                'fetchDepositAddresses': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'ws': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38003300-adc12fba-323f-11e8-8525-725f53c4a659.jpg',
                'api': {
                    'rest': 'https://api.coinone.co.kr',
                },
                'www': 'https://coinone.co.kr',
                'doc': 'https://doc.coinone.co.kr',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'orderbook/',
                        'trades/',
                        'ticker/',
                    ],
                },
                'private': {
                    'post': [
                        'account/deposit_address/',
                        'account/btc_deposit_address/',
                        'account/balance/',
                        'account/daily_balance/',
                        'account/user_info/',
                        'account/virtual_account/',
                        'order/cancel_all/',
                        'order/cancel/',
                        'order/limit_buy/',
                        'order/limit_sell/',
                        'order/complete_orders/',
                        'order/limit_orders/',
                        'order/query_order/',
                        'transaction/auth_number/',
                        'transaction/history/',
                        'transaction/krw/history/',
                        'transaction/btc/',
                        'transaction/coin/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.002,
                    'maker': 0.002,
                },
            },
            'precisionMode': TICK_SIZE,
            'exceptions': {
                '405': OnMaintenance,  # {"errorCode":"405","status":"maintenance","result":"error"}
                '104': OrderNotFound,  # {"errorCode":"104","errorMsg":"Order id is not exist","result":"error"}
                '108': BadSymbol,  # {"errorCode":"108","errorMsg":"Unknown CryptoCurrency","result":"error"}
                '107': BadRequest,  # {"errorCode":"107","errorMsg":"Parameter error","result":"error"}
            },
            'commonCurrencies': {
                'SOC': 'Soda Coin',
            },
        })

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for coinone
        :param dict [params]: extra parameters specific to the exchange api endpoint
        :returns dict[]: an array of objects representing market data
        """
        request = {
            'currency': 'all',
        }
        response = self.publicGetTicker(request)
        #
        #    {
        #        "result": "success",
        #        "errorCode": "0",
        #        "timestamp": "1643676668",
        #        "xec": {
        #          "currency": "xec",
        #          "first": "0.0914",
        #          "low": "0.0894",
        #          "high": "0.096",
        #          "last": "0.0937",
        #          "volume": "1673283662.9797",
        #          "yesterday_first": "0.0929",
        #          "yesterday_low": "0.0913",
        #          "yesterday_high": "0.0978",
        #          "yesterday_last": "0.0913",
        #          "yesterday_volume": "1167285865.4571"
        #        },
        #        ...
        #    }
        #
        result = []
        quoteId = 'krw'
        quote = self.safe_currency_code(quoteId)
        baseIds = list(response.keys())
        for i in range(0, len(baseIds)):
            baseId = baseIds[i]
            ticker = self.safe_value(response, baseId, {})
            currency = self.safe_value(ticker, 'currency')
            if currency is None:
                continue
            base = self.safe_currency_code(baseId)
            result.append({
                'id': baseId,
                'symbol': base + '/' + quote,
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
                    'amount': self.parse_number('1e-4'),
                    'price': self.parse_number('1e-4'),
                    'cost': self.parse_number('1e-8'),
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
                        'min': None,
                        'max': None,
                    },
                },
                'info': ticker,
            })
        return result

    def parse_balance(self, response):
        result = {'info': response}
        balances = self.omit(response, [
            'errorCode',
            'result',
            'normalWallets',
        ])
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            balance = balances[currencyId]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'avail')
            account['total'] = self.safe_string(balance, 'balance')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: a `balance structure <https://github.com/ccxt/ccxt/wiki/Manual#balance-structure>`
        """
        self.load_markets()
        response = self.privatePostAccountBalance(params)
        return self.parse_balance(response)

    def fetch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = self.publicGetOrderbook(self.extend(request, params))
        timestamp = self.safe_timestamp(response, 'timestamp')
        return self.parse_order_book(response, market['symbol'], timestamp, 'bid', 'ask', 'price', 'qty')

    def fetch_tickers(self, symbols: Optional[List[str]] = None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param str[]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: a dictionary of `ticker structures <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        request = {
            'currency': 'all',
            'format': 'json',
        }
        response = self.publicGetTicker(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        timestamp = self.safe_timestamp(response, 'timestamp')
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.safe_market(id)
            symbol = market['symbol']
            ticker = response[id]
            result[symbol] = self.parse_ticker(ticker, market)
            result[symbol]['timestamp'] = timestamp
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol: str, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "currency":"xec",
        #         "first":"0.1069",
        #         "low":"0.09",
        #         "high":"0.1069",
        #         "last":"0.0911",
        #         "volume":"4591217267.4974",
        #         "yesterday_first":"0.1128",
        #         "yesterday_low":"0.1035",
        #         "yesterday_high":"0.1167",
        #         "yesterday_last":"0.1069",
        #         "yesterday_volume":"4014832231.5102"
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'timestamp')
        open = self.safe_string(ticker, 'first')
        last = self.safe_string(ticker, 'last')
        previousClose = self.safe_string(ticker, 'yesterday_last')
        symbol = self.safe_symbol(None, market)
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': previousClose,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "timestamp": "1416893212",
        #         "price": "420000.0",
        #         "qty": "0.1",
        #         "is_ask": "1"
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "timestamp": "1416561032",
        #         "price": "419000.0",
        #         "type": "bid",
        #         "qty": "0.001",
        #         "feeRate": "-0.0015",
        #         "fee": "-0.0000015",
        #         "orderId": "E84A1AC2-8088-4FA0-B093-A3BCDB9B3C85"
        #     }
        #
        timestamp = self.safe_timestamp(trade, 'timestamp')
        market = self.safe_market(None, market)
        is_ask = self.safe_string(trade, 'is_ask')
        side = self.safe_string(trade, 'type')
        if is_ask is not None:
            if is_ask == '1':
                side = 'sell'
            elif is_ask == '0':
                side = 'buy'
        else:
            if side == 'ask':
                side = 'sell'
            elif side == 'bid':
                side = 'buy'
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'qty')
        orderId = self.safe_string(trade, 'orderId')
        feeCostString = self.safe_string(trade, 'fee')
        fee = None
        if feeCostString is not None:
            feeCostString = Precise.string_abs(feeCostString)
            feeRateString = self.safe_string(trade, 'feeRate')
            feeRateString = Precise.string_abs(feeRateString)
            feeCurrencyCode = market['quote'] if (side == 'sell') else market['base']
            fee = {
                'cost': feeCostString,
                'currency': feeCurrencyCode,
                'rate': feeRateString,
            }
        return self.safe_trade({
            'id': self.safe_string(trade, 'id'),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': orderId,
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': fee,
        }, market)

    def fetch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns Trade[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = self.publicGetTrades(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "timestamp": "1416895635",
        #         "currency": "btc",
        #         "completeOrders": [
        #             {
        #                 "timestamp": "1416893212",
        #                 "price": "420000.0",
        #                 "qty": "0.1",
        #                 "is_ask": "1"
        #             }
        #         ]
        #     }
        #
        completeOrders = self.safe_value(response, 'completeOrders', [])
        return self.parse_trades(completeOrders, market, since, limit)

    def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount, price=None, params={}):
        """
        create a trade order
        see https://doc.coinone.co.kr/#tag/Order-V2/operation/v2_order_limit_buy
        see https://doc.coinone.co.kr/#tag/Order-V2/operation/v2_order_limit_sell
        :param str symbol: unified symbol of the market to create an order in
        :param str type: must be 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float [price]: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: an `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        if type != 'limit':
            raise ExchangeError(self.id + ' createOrder() allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'price': price,
            'currency': market['id'],
            'qty': amount,
        }
        method = 'privatePostOrder' + self.capitalize(type) + self.capitalize(side)
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "8a82c561-40b4-4cb3-9bc0-9ac9ffc1d63b"
        #     }
        #
        return self.parse_order(response, market)

    def fetch_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'currency': market['id'],
        }
        response = self.privatePostOrderQueryOrder(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "0e3019f2-1e4d-11e9-9ec7-00e04c3600d7",
        #         "baseCurrency": "KRW",
        #         "targetCurrency": "BTC",
        #         "price": "10011000.0",
        #         "originalQty": "3.0",
        #         "executedQty": "0.62",
        #         "canceledQty": "1.125",
        #         "remainQty": "1.255",
        #         "status": "partially_filled",
        #         "side": "bid",
        #         "orderedAt": 1499340941,
        #         "updatedAt": 1499341142,
        #         "feeRate": "0.002",
        #         "fee": "0.00124",
        #         "averageExecutedPrice": "10011000.0"
        #     }
        #
        return self.parse_order(response, market)

    def parse_order_status(self, status):
        statuses = {
            'live': 'open',
            'partially_filled': 'open',
            'partially_canceled': 'open',
            'filled': 'closed',
            'canceled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "8a82c561-40b4-4cb3-9bc0-9ac9ffc1d63b"
        #     }
        #
        # fetchOrder
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "orderId": "0e3019f2-1e4d-11e9-9ec7-00e04c3600d7",
        #         "baseCurrency": "KRW",
        #         "targetCurrency": "BTC",
        #         "price": "10011000.0",
        #         "originalQty": "3.0",
        #         "executedQty": "0.62",
        #         "canceledQty": "1.125",
        #         "remainQty": "1.255",
        #         "status": "partially_filled",
        #         "side": "bid",
        #         "orderedAt": 1499340941,
        #         "updatedAt": 1499341142,
        #         "feeRate": "0.002",
        #         "fee": "0.00124",
        #         "averageExecutedPrice": "10011000.0"
        #     }
        #
        # fetchOpenOrders
        #
        #     {
        #         "index": "0",
        #         "orderId": "68665943-1eb5-4e4b-9d76-845fc54f5489",
        #         "timestamp": "1449037367",
        #         "price": "444000.0",
        #         "qty": "0.3456",
        #         "type": "ask",
        #         "feeRate": "-0.0015"
        #     }
        #
        id = self.safe_string(order, 'orderId')
        baseId = self.safe_string(order, 'baseCurrency')
        quoteId = self.safe_string(order, 'targetCurrency')
        base = self.safe_currency_code(baseId, market['base'])
        quote = self.safe_currency_code(quoteId, market['quote'])
        symbol = base + '/' + quote
        market = self.safe_market(symbol, market, '/')
        timestamp = self.safe_timestamp_2(order, 'timestamp', 'updatedAt')
        side = self.safe_string_2(order, 'type', 'side')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        remainingString = self.safe_string(order, 'remainQty')
        amountString = self.safe_string_2(order, 'originalQty', 'qty')
        status = self.safe_string(order, 'status')
        # https://github.com/ccxt/ccxt/pull/7067
        if status == 'live':
            if (remainingString is not None) and (amountString is not None):
                isLessThan = Precise.string_lt(remainingString, amountString)
                if isLessThan:
                    status = 'canceled'
        status = self.parse_order_status(status)
        fee = None
        feeCostString = self.safe_string(order, 'fee')
        if feeCostString is not None:
            feeCurrencyCode = quote if (side == 'sell') else base
            fee = {
                'cost': feeCostString,
                'rate': self.safe_string(order, 'feeRate'),
                'currency': feeCurrencyCode,
            }
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': self.safe_string(order, 'price'),
            'stopPrice': None,
            'triggerPrice': None,
            'cost': None,
            'average': self.safe_string(order, 'averageExecutedPrice'),
            'amount': amountString,
            'filled': self.safe_string(order, 'executedQty'),
            'remaining': remainingString,
            'status': status,
            'fee': fee,
            'trades': None,
        }, market)

    def fetch_open_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of  open orders structures to retrieve
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns Order[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        # The returned amount might not be same ordered amount. If an order is partially filled, the returned amount means the remaining amount.
        # For the same reason, the returned amount and remaining are always same, and the returned filled and cost are always zero.
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOpenOrders() allows fetching closed orders with a specific symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = self.privatePostOrderLimitOrders(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "limitOrders": [
        #             {
        #                 "index": "0",
        #                 "orderId": "68665943-1eb5-4e4b-9d76-845fc54f5489",
        #                 "timestamp": "1449037367",
        #                 "price": "444000.0",
        #                 "qty": "0.3456",
        #                 "type": "ask",
        #                 "feeRate": "-0.0015"
        #             }
        #         ]
        #     }
        #
        limitOrders = self.safe_value(response, 'limitOrders', [])
        return self.parse_orders(limitOrders, market, since, limit)

    def fetch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns Trade[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = self.privatePostOrderCompleteOrders(self.extend(request, params))
        #
        # despite the name of the endpoint it returns trades which may have a duplicate orderId
        # https://github.com/ccxt/ccxt/pull/7067
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0",
        #         "completeOrders": [
        #             {
        #                 "timestamp": "1416561032",
        #                 "price": "419000.0",
        #                 "type": "bid",
        #                 "qty": "0.001",
        #                 "feeRate": "-0.0015",
        #                 "fee": "-0.0000015",
        #                 "orderId": "E84A1AC2-8088-4FA0-B093-A3BCDB9B3C85"
        #             }
        #         ]
        #     }
        #
        completeOrders = self.safe_value(response, 'completeOrders', [])
        return self.parse_trades(completeOrders, market, since, limit)

    def cancel_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        if symbol is None:
            # eslint-disable-next-line quotes
            raise ArgumentsRequired(self.id + " cancelOrder() requires a symbol argument. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
        price = self.safe_number(params, 'price')
        qty = self.safe_number(params, 'qty')
        isAsk = self.safe_integer(params, 'is_ask')
        if (price is None) or (qty is None) or (isAsk is None):
            # eslint-disable-next-line quotes
            raise ArgumentsRequired(self.id + " cancelOrder() requires {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument.")
        self.load_markets()
        request = {
            'order_id': id,
            'price': price,
            'qty': qty,
            'is_ask': isAsk,
            'currency': self.market_id(symbol),
        }
        response = self.privatePostOrderCancel(self.extend(request, params))
        #
        #     {
        #         "result": "success",
        #         "errorCode": "0"
        #     }
        #
        return response

    def fetch_deposit_addresses(self, codes=None, params={}):
        """
        fetch deposit addresses for multiple currencies and chain types
        :param str[]|None codes: list of unified currency codes, default is None
        :param dict [params]: extra parameters specific to the coinone api endpoint
        :returns dict: a list of `address structures <https://github.com/ccxt/ccxt/wiki/Manual#address-structure>`
        """
        self.load_markets()
        response = self.privatePostAccountDepositAddress(params)
        #
        #     {
        #         result: 'success',
        #         errorCode: '0',
        #         walletAddress: {
        #             matic: null,
        #             btc: "mnobqu4i6qMCJWDpf5UimRmr8JCvZ8FLcN",
        #             xrp: null,
        #             xrp_tag: '-1',
        #             kava: null,
        #             kava_memo: null,
        #         }
        #     }
        #
        walletAddress = self.safe_value(response, 'walletAddress', {})
        keys = list(walletAddress.keys())
        result = {}
        for i in range(0, len(keys)):
            key = keys[i]
            value = walletAddress[key]
            if (not value) or (value == '-1'):
                continue
            parts = key.split('_')
            currencyId = self.safe_value(parts, 0)
            secondPart = self.safe_value(parts, 1)
            code = self.safe_currency_code(currencyId)
            depositAddress = self.safe_value(result, code)
            if depositAddress is None:
                depositAddress = {
                    'currency': code,
                    'address': None,
                    'tag': None,
                    'info': value,
                }
            address = self.safe_string(depositAddress, 'address', value)
            self.check_address(address)
            depositAddress['address'] = address
            depositAddress['info'] = address
            if (secondPart == 'tag' or secondPart == 'memo'):
                depositAddress['tag'] = value
                depositAddress['info'] = [address, value]
            result[code] = depositAddress
        return result

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api']['rest'] + '/'
        if api == 'public':
            url += request
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/' + request
            nonce = str(self.nonce())
            json = self.json(self.extend({
                'access_token': self.apiKey,
                'nonce': nonce,
            }, params))
            payload = self.string_to_base64(json)
            body = payload
            secret = self.secret.upper()
            signature = self.hmac(payload, self.encode(secret), hashlib.sha512)
            headers = {
                'Content-Type': 'application/json',
                'X-COINONE-PAYLOAD': payload,
                'X-COINONE-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return None
        if 'result' in response:
            result = response['result']
            if result != 'success':
                #
                #    { "errorCode": "405",  "status": "maintenance",  "result": "error"}
                #
                errorCode = self.safe_string(response, 'errorCode')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
                raise ExchangeError(feedback)
        else:
            raise ExchangeError(self.id + ' ' + body)
        return None
