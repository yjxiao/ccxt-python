# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.abstract.bitforex import ImplicitAPI
import hashlib
from ccxt.base.types import OrderSide
from ccxt.base.types import OrderType
from typing import Optional
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import AuthenticationError
from ccxt.base.decimal_to_precision import TICK_SIZE


class bitforex(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(bitforex, self).describe(), {
            'id': 'bitforex',
            'name': 'Bitforex',
            'countries': ['CN'],
            'rateLimit': 500,  # https://github.com/ccxt/ccxt/issues/5054
            'version': 'v1',
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': None,  # has but unimplemented
                'future': False,
                'option': False,
                'cancelOrder': True,
                'createOrder': True,
                'createStopLimitOrder': False,
                'createStopMarketOrder': False,
                'createStopOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchClosedOrders': True,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPositionMode': False,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchTrades': True,
                'fetchTransactionFees': False,
                'fetchTransfer': False,
                'fetchTransfers': False,
                'fetchWithdrawal': False,
                'fetchWithdrawals': False,
                'transfer': False,
                'withdraw': False,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
                '1M': '1month',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87295553-1160ec00-c50e-11ea-8ea0-df79276a9646.jpg',
                'api': {
                    'rest': 'https://api.bitforex.com',
                },
                'www': 'https://www.bitforex.com',
                'doc': 'https://github.com/githubdev2020/API_Doc_en/wiki',
                'fees': 'https://help.bitforex.com/en_us/?cat=13',
                'referral': 'https://www.bitforex.com/en/invitationRegister?inviterId=1867438',
            },
            'api': {
                'public': {
                    'get': {
                        '/api/v1/ping': 0.2,
                        '/api/v1/time': 0.2,
                        'api/v1/market/symbols': 20,
                        'api/v1/market/ticker': 4,
                        'api/v1/market/ticker-all': 4,
                        'api/v1/market/depth': 4,
                        'api/v1/market/depth-all': 4,
                        'api/v1/market/trades': 20,
                        'api/v1/market/kline': 20,
                    },
                },
                'private': {
                    'post': {
                        'api/v1/fund/mainAccount': 1,
                        'api/v1/fund/allAccount': 30,
                        'api/v1/trade/placeOrder': 1,
                        'api/v1/trade/placeMultiOrder': 10,
                        'api/v1/trade/cancelOrder': 1,
                        'api/v1/trade/cancelMultiOrder': 6.67,
                        'api/v1/trade/cancelAllOrder': 20,
                        'api/v1/trade/orderInfo': 1,
                        'api/v1/trade/multiOrderInfo': 10,
                        'api/v1/trade/orderInfos': 20,
                        'api/v1/trade/myTrades': 2,
                    },
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': self.parse_number('0.001'),
                    'taker': self.parse_number('0.001'),
                },
                'funding': {
                    'tierBased': False,
                    'percentage': True,
                    'deposit': {},
                    'withdraw': {},
                },
            },
            'commonCurrencies': {
                'BKC': 'Bank Coin',
                'CAPP': 'Crypto Application Token',
                'CREDIT': 'TerraCredit',
                'CTC': 'Culture Ticket Chain',
                'EWT': 'EcoWatt Token',
                'IQ': 'IQ.Cash',
                'MIR': 'MIR COIN',
                'NOIA': 'METANOIA',
                'TON': 'To The Moon',
            },
            'precisionMode': TICK_SIZE,
            'exceptions': {
                '1000': OrderNotFound,  # {"code":"1000","success":false,"time":1643047898676,"message":"The order does not exist or the status is wrong"}
                '1003': BadSymbol,  # {"success":false,"code":"1003","message":"Param Invalid:param invalid -symbol:symbol error"}
                '1013': AuthenticationError,
                '1016': AuthenticationError,
                '1017': PermissionDenied,  # {"code":"1017","success":false,"time":1602670594367,"message":"IP not allow"}
                '1019': BadSymbol,  # {"code":"1019","success":false,"time":1607087743778,"message":"Symbol Invalid"}
                '3002': InsufficientFunds,
                '4002': InvalidOrder,  # {"success":false,"code":"4002","message":"Price unreasonable"}
                '4003': InvalidOrder,  # {"success":false,"code":"4003","message":"amount too small"}
                '4004': OrderNotFound,
                '10204': DDoSProtection,
            },
        })

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bitforex
        :param dict [params]: extra parameters specific to the exchange api endpoint
        :returns dict[]: an array of objects representing market data
        """
        response = await self.publicGetApiV1MarketSymbols(params)
        #
        #    {
        #        "data": [
        #            {
        #                "amountPrecision":4,
        #                "minOrderAmount":3.0E-4,
        #                "pricePrecision":2,
        #                "symbol":"coin-usdt-btc"
        #            },
        #            ...
        #        ]
        #    }
        #
        data = response['data']
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = self.safe_string(market, 'symbol')
            symbolParts = id.split('-')
            baseId = symbolParts[2]
            quoteId = symbolParts[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            result.append({
                'id': id,
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
                'active': True,
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'expiry': None,
                'expiryDateTime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'amountPrecision'))),
                    'price': self.parse_number(self.parse_precision(self.safe_string(market, 'pricePrecision'))),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(market, 'minOrderAmount'),
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
                'info': market,
            })
        return result

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public) v1
        #
        #      {
        #          "price":57594.53,
        #          "amount":0.3172,
        #          "time":1637329685322,
        #          "direction":1,
        #          "tid":"1131019666"
        #      }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "symbol": "coin-usdt-babydoge",
        #         "tid": 7289,
        #         "orderId": "b6fe2b61-e5cb-4970-9bdc-8c7cd1fcb4d8",
        #         "price": "0.000007",
        #         "amount": "50000000",
        #         "tradeFee": "50000",
        #         "tradeFeeCurrency": "babydoge",
        #         "time": "1684750536460",
        #         "isBuyer": True,
        #         "isMaker": True,
        #         "isSelfTrade": True
        #     }
        #
        marketId = self.safe_string(trade, 'symbol')
        market = self.safe_market(marketId, market)
        timestamp = self.safe_integer(trade, 'time')
        id = self.safe_string(trade, 'tid')
        orderId = self.safe_string(trade, 'orderId')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        sideId = self.safe_integer(trade, 'direction')
        side = self.parse_side(sideId)
        if side is None:
            isBuyer = self.safe_value(trade, 'isBuyer')
            side = 'buy' if isBuyer else 'sell'
        takerOrMaker = None
        isMaker = self.safe_value(trade, 'isMaker')
        if isMaker is not None:
            takerOrMaker = 'maker' if (isMaker) else 'taker'
        fee = None
        feeCostString = self.safe_string(trade, 'tradeFee')
        if feeCostString is not None:
            feeCurrencyId = self.safe_string(trade, 'tradeFeeCurrency')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCostString,
                'currency': feeCurrencyCode,
            }
        return self.safe_trade({
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'order': orderId,
            'fee': fee,
            'takerOrMaker': takerOrMaker,
        }, market)

    async def fetch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns Trade[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['size'] = limit
        market = self.market(symbol)
        response = await self.publicGetApiV1MarketTrades(self.extend(request, params))
        #
        # {
        #  "data":
        #      [
        #          {
        #              "price":57594.53,
        #              "amount":0.3172,
        #              "time":1637329685322,
        #              "direction":1,
        #              "tid":"1131019666"
        #          }
        #      ],
        #  "success": True,
        #  "time": 1637329688475
        # }
        #
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all trades made by the user
        see https://apidoc.bitforex.com/#spot-account-trade
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns Trade[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#trade-structure>`
        """
        self.check_required_symbol('fetchMyTrades', symbol)
        await self.load_markets()
        request = {
            # 'symbol': market['id'],
            # 'orderId': orderId,
            # 'startTime': timestamp,
            # 'endTime': timestamp,
            # 'limit': limit,  # default 500, max 1000
        }
        market = self.market(symbol)
        request['symbol'] = market['id']
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            request['startTime'] = max(since - 1, 0)
        endTime = self.safe_integer_2(params, 'until', 'endTime')
        if endTime is not None:
            request['endTime'] = endTime
        params = self.omit(params, ['until'])
        response = await self.privatePostApiV1TradeMyTrades(self.extend(request, params))
        #
        #     {
        #         "data": [
        #             {
        #                 "symbol": "coin-usdt-babydoge",
        #                 "tid": 7289,
        #                 "orderId": "a262d030-11a5-40fd-a07c-7ba84aa68752",
        #                 "price": "0.000007",
        #                 "amount": "50000000",
        #                 "tradeFee": "0.35",
        #                 "tradeFeeCurrency": "usdt",
        #                 "time": "1684750536460",
        #                 "isBuyer": False,
        #                 "isMaker": False,
        #                 "isSelfTrade": True
        #             }
        #         ],
        #         "success": True,
        #         "time": 1685009320042
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def parse_balance(self, response):
        data = response['data']
        result = {'info': response}
        for i in range(0, len(data)):
            balance = data[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['used'] = self.safe_string(balance, 'frozen')
            account['free'] = self.safe_string(balance, 'active')
            account['total'] = self.safe_string(balance, 'fix')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: a `balance structure <https://github.com/ccxt/ccxt/wiki/Manual#balance-structure>`
        """
        await self.load_markets()
        response = await self.privatePostApiV1FundAllAccount(params)
        return self.parse_balance(response)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "buy":7.04E-7,
        #         "date":1643371198598,
        #         "high":7.48E-7,
        #         "last":7.28E-7,
        #         "low":7.10E-7,
        #         "sell":7.54E-7,
        #         "vol":9877287.2874
        #     }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.safe_integer(ticker, 'date')
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
            'baseVolume': self.safe_string(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol: str, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        await self.load_markets()
        market = self.markets[symbol]
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetApiV1MarketTickerAll(self.extend(request, params))
        ticker = self.safe_value(response, 'data')
        #
        #     {
        #         "data":{
        #             "buy":37082.83,
        #             "date":1643388686660,
        #             "high":37487.83,
        #             "last":37086.79,
        #             "low":35544.44,
        #             "sell":37090.52,
        #             "vol":690.9776
        #         },
        #         "success":true,
        #         "time":1643388686660
        #     }
        #
        return self.parse_ticker(ticker, market)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     {
        #         "close":0.02505143,
        #         "currencyVol":0,
        #         "high":0.02506422,
        #         "low":0.02505143,
        #         "open":0.02506095,
        #         "time":1591508940000,
        #         "vol":51.1869
        #     }
        #
        return [
            self.safe_integer(ohlcv, 'time'),
            self.safe_number(ohlcv, 'open'),
            self.safe_number(ohlcv, 'high'),
            self.safe_number(ohlcv, 'low'),
            self.safe_number(ohlcv, 'close'),
            self.safe_number(ohlcv, 'vol'),
        ]

    async def fetch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'ktype': self.safe_string(self.timeframes, timeframe, timeframe),
        }
        if limit is not None:
            request['size'] = limit  # default 1, max 600
        response = await self.publicGetApiV1MarketKline(self.extend(request, params))
        #
        #     {
        #         "data":[
        #             {"close":0.02505143,"currencyVol":0,"high":0.02506422,"low":0.02505143,"open":0.02506095,"time":1591508940000,"vol":51.1869},
        #             {"close":0.02503914,"currencyVol":0,"high":0.02506687,"low":0.02503914,"open":0.02505358,"time":1591509000000,"vol":9.1082},
        #             {"close":0.02505172,"currencyVol":0,"high":0.02507466,"low":0.02503895,"open":0.02506371,"time":1591509060000,"vol":63.7431},
        #         ],
        #         "success":true,
        #         "time":1591509427131
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    async def fetch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetApiV1MarketDepthAll(self.extend(request, params))
        data = self.safe_value(response, 'data')
        timestamp = self.safe_integer(response, 'time')
        return self.parse_order_book(data, market['symbol'], timestamp, 'bids', 'asks', 'price', 'amount')

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'open',
            '2': 'closed',
            '3': 'canceled',
            '4': 'canceled',
        }
        return statuses[status] if (status in statuses) else status

    def parse_side(self, sideId):
        if sideId == 1:
            return 'buy'
        elif sideId == 2:
            return 'sell'
        else:
            return None

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'orderId')
        timestamp = self.safe_number(order, 'createTime')
        lastTradeTimestamp = self.safe_number(order, 'lastTime')
        symbol = market['symbol']
        sideId = self.safe_integer(order, 'tradeType')
        side = self.parse_side(sideId)
        type = None
        price = self.safe_string(order, 'orderPrice')
        average = self.safe_string(order, 'avgPrice')
        amount = self.safe_string(order, 'orderAmount')
        filled = self.safe_string(order, 'dealAmount')
        status = self.parse_order_status(self.safe_string(order, 'orderState'))
        feeSide = 'base' if (side == 'buy') else 'quote'
        feeCurrency = market[feeSide]
        fee = {
            'cost': self.safe_number(order, 'tradeFee'),
            'currency': feeCurrency,
        }
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'cost': None,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': fee,
            'trades': None,
        }, market)

    async def fetch_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'orderId': id,
        }
        response = await self.privatePostApiV1TradeOrderInfo(self.extend(request, params))
        order = self.parse_order(response['data'], market)
        return order

    async def fetch_open_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of  open orders structures to retrieve
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns Order[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'state': 0,
        }
        response = await self.privatePostApiV1TradeOrderInfos(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    async def fetch_closed_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of  orde structures to retrieve
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns Order[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'state': 1,
        }
        response = await self.privatePostApiV1TradeOrderInfos(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    async def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float [price]: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: an `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        sideId = None
        if side == 'buy':
            sideId = 1
        elif side == 'sell':
            sideId = 2
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'price': price,
            'amount': amount,
            'tradeType': sideId,
        }
        response = await self.privatePostApiV1TradePlaceOrder(self.extend(request, params))
        data = response['data']
        return self.safe_order({
            'info': response,
            'id': self.safe_string(data, 'orderId'),
        }, market)

    async def cancel_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the bitforex api endpoint
        :returns dict: An `order structure <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        request = {
            'orderId': id,
        }
        if symbol is not None:
            request['symbol'] = self.market_id(symbol)
        results = await self.privatePostApiV1TradeCancelOrder(self.extend(request, params))
        success = results['success']
        returnVal = {'info': results, 'success': success}
        return returnVal

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']['rest'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            payload = self.urlencode({'accessKey': self.apiKey})
            query['nonce'] = self.milliseconds()
            if query:
                payload += '&' + self.urlencode(self.keysort(query))
            # message = '/' + 'api/' + self.version + '/' + path + '?' + payload
            message = '/' + path + '?' + payload
            signature = self.hmac(self.encode(message), self.encode(self.secret), hashlib.sha256)
            body = payload + '&signData=' + signature
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not isinstance(body, str):
            return None  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            feedback = self.id + ' ' + body
            success = self.safe_value(response, 'success')
            if success is not None:
                if not success:
                    codeInner = self.safe_string(response, 'code')
                    self.throw_exactly_matched_exception(self.exceptions, codeInner, feedback)
                    raise ExchangeError(feedback)
        return None
