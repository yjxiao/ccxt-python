# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.precise import Precise


class bitbns(Exchange):

    def describe(self):
        return self.deep_extend(super(bitbns, self).describe(), {
            'id': 'bitbns',
            'name': 'Bitbns',
            'countries': ['IN'],  # India
            'rateLimit': 1000,
            'certified': False,
            'pro': False,
            'version': 'v2',
            # new metainfo interface
            'has': {
                'spot': True,
                'margin': None,
                'swap': False,
                'future': False,
                'option': False,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchDeposits': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedPositions': False,
                'fetchLeverage': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOHLCV': None,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchStatus': True,
                'fetchTicker': 'emulated',
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchWithdrawals': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setPositionMode': False,
            },
            'timeframes': {
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/117201933-e7a6e780-adf5-11eb-9d80-98fc2a21c3d6.jpg',
                'api': {
                    'www': 'https://bitbns.com',
                    'v1': 'https://api.bitbns.com/api/trade/v1',
                    'v2': 'https://api.bitbns.com/api/trade/v2',
                },
                'www': 'https://bitbns.com',
                'referral': 'https://ref.bitbns.com/1090961',
                'doc': [
                    'https://bitbns.com/trade/#/api-trading/',
                ],
                'fees': 'https://bitbns.com/fees',
            },
            'api': {
                'www': {
                    'get': [
                        'order/fetchMarkets',
                        'order/fetchTickers',
                        'order/fetchOrderbook',
                        'order/getTickerWithVolume',
                        'exchangeData/ohlc',  # ?coin=${coin_name}&page=${page}
                        'exchangeData/orderBook',
                        'exchangeData/tradedetails',
                    ],
                },
                'v1': {
                    'get': [
                        'platform/status',
                        'tickers',
                        'orderbook/sell/{symbol}',
                        'orderbook/buy/{symbol}',
                    ],
                    'post': [
                        'currentCoinBalance/EVERYTHING',
                        'getApiUsageStatus/USAGE',
                        'getOrderSocketToken/USAGE',
                        'currentCoinBalance/{symbol}',
                        'orderStatus/{symbol}',
                        'depositHistory/{symbol}',
                        'withdrawHistory/{symbol}',
                        'withdrawHistoryAll/{symbol}',
                        'depositHistoryAll/{symbol}',
                        'listOpenOrders/{symbol}',
                        'listOpenStopOrders/{symbol}',
                        'getCoinAddress/{symbol}',
                        'placeSellOrder/{symbol}',
                        'placeBuyOrder/{symbol}',
                        'buyStopLoss/{symbol}',
                        'sellStopLoss/{symbol}',
                        'placeSellOrder/{symbol}',
                        'cancelOrder/{symbol}',
                        'cancelStopLossOrder/{symbol}',
                        'listExecutedOrders/{symbol}',
                        'placeMarketOrder/{symbol}',
                        'placeMarketOrderQnty/{symbol}',
                    ],
                },
                'v2': {
                    'post': [
                        'orders',
                        'cancel',
                        'getordersnew',
                        'marginOrders',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'feeSide': 'quote',
                    'tierBased': False,
                    'percentage': True,
                    'taker': self.parse_number('0.0025'),
                    'maker': self.parse_number('0.0025'),
                },
            },
            'exceptions': {
                'exact': {
                    '400': BadRequest,  # {"msg":"Invalid Request","status":-1,"code":400}
                    '409': BadSymbol,  # {"data":"","status":0,"error":"coin name not supplied or not yet supported","code":409}
                    '416': InsufficientFunds,  # {"data":"Oops ! Not sufficient currency to sell","status":0,"error":null,"code":416}
                    '417': OrderNotFound,  # {"data":[],"status":0,"error":"Nothing to show","code":417}
                },
                'broad': {},
            },
        })

    def fetch_status(self, params={}):
        response = self.v1GetPlatformStatus(params)
        #
        #     {
        #         "data":{
        #             "BTC":{"status":1},
        #             "ETH":{"status":1},
        #             "XRP":{"status":1},
        #         },
        #         "status":1,
        #         "error":null,
        #         "code":200
        #     }
        #
        status = self.safe_string(response, 'status')
        if status is not None:
            status = 'ok' if (status == '1') else 'maintenance'
            self.status = self.extend(self.status, {
                'status': status,
                'updated': self.milliseconds(),
            })
        return self.status

    def fetch_markets(self, params={}):
        response = self.wwwGetOrderFetchMarkets(params)
        #
        #     [
        #         {
        #             "id":"BTC",
        #             "symbol":"BTC/INR",
        #             "base":"BTC",
        #             "quote":"INR",
        #             "baseId":"BTC",
        #             "quoteId":"",
        #             "active":true,
        #             "limits":{
        #                 "amount":{"min":"0.00017376","max":20},
        #                 "price":{"min":2762353.2359999996,"max":6445490.883999999},
        #                 "cost":{"min":800,"max":128909817.67999998}
        #             },
        #             "precision":{
        #                 "amount":8,
        #                 "price":2
        #             },
        #             "info":{}
        #         },
        #     ]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'id')
            baseId = self.safe_string(market, 'base')
            quoteId = self.safe_string(market, 'quote')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            marketPrecision = self.safe_value(market, 'precision', {})
            marketLimits = self.safe_value(market, 'limits', {})
            amountLimits = self.safe_value(marketLimits, 'amount', {})
            priceLimits = self.safe_value(marketLimits, 'price', {})
            costLimits = self.safe_value(marketLimits, 'cost', {})
            usdt = (quoteId == 'USDT')
            # INR markets don't need a _INR prefix
            uppercaseId = (baseId + '_' + quoteId) if usdt else baseId
            result.append({
                'id': id,
                'uppercaseId': uppercaseId,
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
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'active': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.safe_integer(marketPrecision, 'amount'),
                    'price': self.safe_integer(marketPrecision, 'price'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(amountLimits, 'min'),
                        'max': self.safe_number(amountLimits, 'max'),
                    },
                    'price': {
                        'min': self.safe_number(priceLimits, 'min'),
                        'max': self.safe_number(priceLimits, 'max'),
                    },
                    'cost': {
                        'min': self.safe_number(costLimits, 'min'),
                        'max': self.safe_number(costLimits, 'max'),
                    },
                },
                'info': market,
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default 100, max 5000, see https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#order-book
        response = self.wwwGetOrderFetchOrderbook(self.extend(request, params))
        #
        #     {
        #         "bids":[
        #             [49352.04,0.843948],
        #             [49352.03,0.742048],
        #             [49349.78,0.686239],
        #         ],
        #         "asks":[
        #             [49443.59,0.065137],
        #             [49444.63,0.098211],
        #             [49449.01,0.066309],
        #         ],
        #         "timestamp":1619172786577,
        #         "datetime":"2021-04-23T10:13:06.577Z",
        #         "nonce":""
        #     }
        #
        timestamp = self.safe_integer(response, 'timestamp')
        return self.parse_order_book(response, timestamp)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "symbol":"BTC/INR",
        #         "info":{
        #             "highest_buy_bid":4368494.31,
        #             "lowest_sell_bid":4374835.09,
        #             "last_traded_price":4374835.09,
        #             "yes_price":4531016.27,
        #             "volume":{"max":"4569119.23","min":"4254552.13","volume":62.17722344}
        #         },
        #         "timestamp":1619100020845,
        #         "datetime":1619100020845,
        #         "high":"4569119.23",
        #         "low":"4254552.13",
        #         "bid":4368494.31,
        #         "bidVolume":"",
        #         "ask":4374835.09,
        #         "askVolume":"",
        #         "vwap":"",
        #         "open":4531016.27,
        #         "close":4374835.09,
        #         "last":4374835.09,
        #         "baseVolume":62.17722344,
        #         "quoteVolume":"",
        #         "previousClose":"",
        #         "change":-156181.1799999997,
        #         "percentage":-3.446934874943623,
        #         "average":4452925.68
        #     }
        #
        timestamp = self.safe_integer(ticker, 'timestamp')
        marketId = self.safe_string(ticker, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        last = self.safe_number(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'bid'),
            'bidVolume': self.safe_number(ticker, 'bidVolume'),
            'ask': self.safe_number(ticker, 'ask'),
            'askVolume': self.safe_number(ticker, 'askVolume'),
            'vwap': self.safe_number(ticker, 'vwap'),
            'open': self.safe_number(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': self.safe_number(ticker, 'previousClose'),  # previous day close
            'change': self.safe_number(ticker, 'change'),
            'percentage': self.safe_number(ticker, 'percentage'),
            'average': self.safe_number(ticker, 'average'),
            'baseVolume': self.safe_number(ticker, 'baseVolume'),
            'quoteVolume': self.safe_number(ticker, 'quoteVolume'),
            'info': ticker,
        }, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.wwwGetOrderFetchTickers(params)
        #
        #     {
        #         "BTC/INR":{
        #             "symbol":"BTC/INR",
        #             "info":{
        #                 "highest_buy_bid":4368494.31,
        #                 "lowest_sell_bid":4374835.09,
        #                 "last_traded_price":4374835.09,
        #                 "yes_price":4531016.27,
        #                 "volume":{"max":"4569119.23","min":"4254552.13","volume":62.17722344}
        #             },
        #             "timestamp":1619100020845,
        #             "datetime":1619100020845,
        #             "high":"4569119.23",
        #             "low":"4254552.13",
        #             "bid":4368494.31,
        #             "bidVolume":"",
        #             "ask":4374835.09,
        #             "askVolume":"",
        #             "vwap":"",
        #             "open":4531016.27,
        #             "close":4374835.09,
        #             "last":4374835.09,
        #             "baseVolume":62.17722344,
        #             "quoteVolume":"",
        #             "previousClose":"",
        #             "change":-156181.1799999997,
        #             "percentage":-3.446934874943623,
        #             "average":4452925.68
        #         }
        #     }
        #
        return self.parse_tickers(response, symbols)

    def parse_balance(self, response):
        timestamp = None
        result = {
            'info': response,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        data = self.safe_value(response, 'data', {})
        keys = list(data.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            parts = key.split('availableorder')
            numParts = len(parts)
            if numParts > 1:
                currencyId = self.safe_string(parts, 1)
                if currencyId != 'Money':
                    code = self.safe_currency_code(currencyId)
                    account = self.account()
                    account['free'] = self.safe_string(data, key)
                    account['used'] = self.safe_string(data, 'inorder' + currencyId)
                    result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.v1PostCurrentCoinBalanceEVERYTHING(params)
        #
        #     {
        #         "data":{
        #             "availableorderMoney":0,
        #             "availableorderBTC":0,
        #             "availableorderXRP":0,
        #             "inorderMoney":0,
        #             "inorderBTC":0,
        #             "inorderXRP":0,
        #             "inorderNEO":0,
        #         },
        #         "status":1,
        #         "error":null,
        #         "code":200
        #     }
        #
        return self.parse_balance(response)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            # 'PARTIALLY_FILLED': 'open',
            # 'FILLED': 'closed',
            # 'CANCELED': 'canceled',
            # 'PENDING_CANCEL': 'canceling',  # currently unused
            # 'REJECTED': 'rejected',
            # 'EXPIRED': 'expired',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "data":"Successfully placed bid to purchase currency",
        #         "status":1,
        #         "error":null,
        #         "id":5424475,
        #         "code":200
        #     }
        #
        # fetchOrder
        #
        #     {
        #         "entry_id":5424475,
        #         "btc":0.01,
        #         "rate":2000,
        #         "time":"2021-04-25T17:05:42.000Z",
        #         "type":0,
        #         "status":0,
        #         "total":0.01,
        #         "avg_cost":null,
        #         "side":"BUY",
        #         "amount":0.01,
        #         "remaining":0.01,
        #         "filled":0,
        #         "cost":null,
        #         "fee":0.05
        #     }
        #
        # fetchOpenOrders
        #
        #     {
        #         "entry_id":5424475,
        #         "btc":0.01,
        #         "rate":2000,
        #         "time":"2021-04-25T17:05:42.000Z",
        #         "type":0,
        #         "status":0
        #     }
        #
        id = self.safe_string_2(order, 'id', 'entry_id')
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.parse8601(self.safe_string(order, 'time'))
        price = self.safe_string(order, 'rate')
        amount = self.safe_string_2(order, 'amount', 'btc')
        filled = self.safe_string(order, 'filled')
        remaining = self.safe_string(order, 'remaining')
        average = self.safe_string(order, 'avg_cost')
        cost = self.safe_string(order, 'cost')
        type = self.safe_string_lower(order, 'type')
        if type == '0':
            type = 'limit'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        side = self.safe_string_lower(order, 'side')
        feeCost = self.safe_number(order, 'fee')
        fee = None
        if feeCost is not None:
            feeCurrencyCode = None
            fee = {
                'cost': feeCost,
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
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': None,
        }, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit' and type != 'market':
            raise ExchangeError(self.id + ' allows limit and market orders only')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'side': side.upper(),
            'symbol': market['uppercaseId'],
            'quantity': self.amount_to_precision(symbol, amount),
            # 'target_rate': self.price_to_precision(symbol, targetRate),
            # 't_rate': self.price_to_precision(symbol, stopPrice),
            # 'trail_rate': self.price_to_precision(symbol, trailRate),
            # To Place Simple Buy or Sell Order use rate
            # To Place Stoploss Buy or Sell Order use rate & t_rate
            # To Place Bracket Buy or Sell Order use rate , t_rate, target_rate & trail_rate
        }
        method = 'v2PostOrders'
        if type == 'limit':
            request['rate'] = self.price_to_precision(symbol, price)
        elif type == 'market':
            method = 'v1PostPlaceMarketOrderQntySymbol'
            request['market'] = market['quoteId']
        else:
            raise ExchangeError(self.id + ' allows limit and market orders only')
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "data":"Successfully placed bid to purchase currency",
        #         "status":1,
        #         "error":null,
        #         "id":5424475,
        #         "code":200
        #     }
        #
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        quoteSide = 'usdtcancelOrder' if (market['quoteId'] == 'USDT') else 'cancelOrder'
        request = {
            'entry_id': id,
            'symbol': market['uppercaseId'],
            'side': quoteSide,
        }
        response = self.v2PostCancel(self.extend(request, params))
        return self.parse_order(response, market)

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'entry_id': id,
        }
        response = self.v1PostOrderStatusSymbol(self.extend(request, params))
        #
        #     {
        #         "data":[
        #             {
        #                 "entry_id":5424475,
        #                 "btc":0.01,
        #                 "rate":2000,
        #                 "time":"2021-04-25T17:05:42.000Z",
        #                 "type":0,
        #                 "status":0,
        #                 "total":0.01,
        #                 "avg_cost":null,
        #                 "side":"BUY",
        #                 "amount":0.01,
        #                 "remaining":0.01,
        #                 "filled":0,
        #                 "cost":null,
        #                 "fee":0.05
        #             }
        #         ],
        #         "status":1,
        #         "error":null,
        #         "code":200
        #     }
        #
        data = self.safe_value(response, 'data', [])
        first = self.safe_value(data, 0)
        return self.parse_order(first, market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        quoteSide = 'usdtListOpenOrders' if (market['quoteId'] == 'USDT') else 'listOpenOrders'
        request = {
            'symbol': market['uppercaseId'],
            'side': quoteSide,
            'page': 0,
        }
        response = self.v2PostGetordersnew(self.extend(request, params))
        #
        #     {
        #         "data":[
        #             {
        #                 "entry_id":5424475,
        #                 "btc":0.01,
        #                 "rate":2000,
        #                 "time":"2021-04-25T17:05:42.000Z",
        #                 "type":0,
        #                 "status":0
        #             }
        #         ],
        #         "status":1,
        #         "error":null,
        #         "code":200
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_orders(data, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchMyTrades
        #
        #     {
        #         "type": "BTC Sell order executed",
        #         "typeI": 6,
        #         "crypto": 5000,
        #         "amount": 35.4,
        #         "rate": 709800,
        #         "date": "2020-05-22T15:05:34.000Z",
        #         "unit": "INR",
        #         "factor": 100000000,
        #         "fee": 0.09,
        #         "delh_btc": -5000,
        #         "delh_inr": 0,
        #         "del_btc": 0,
        #         "del_inr": 35.4,
        #         "id": "2938823"
        #     }
        #
        # fetchTrades
        #
        #     {
        #         "tradeId":"1909151",
        #         "price":"61904.6300",
        #         "quote_volume":1618.05,
        #         "base_volume":0.02607254,
        #         "timestamp":1634548602000,
        #         "type":"buy"
        #     }
        #
        market = self.safe_market(None, market)
        orderId = self.safe_string_2(trade, 'id', 'tradeId')
        timestamp = self.parse8601(self.safe_string(trade, 'date'))
        timestamp = self.safe_integer(trade, 'timestamp', timestamp)
        priceString = self.safe_string_2(trade, 'rate', 'price')
        amountString = self.safe_string(trade, 'amount')
        side = self.safe_string_lower(trade, 'type')
        if side is not None:
            if side.find('buy') >= 0:
                side = 'buy'
            elif side.find('sell') >= 0:
                side = 'sell'
        factor = self.safe_string(trade, 'factor')
        costString = None
        if factor is not None:
            amountString = Precise.string_div(amountString, factor)
        else:
            amountString = self.safe_string(trade, 'base_volume')
            costString = self.safe_string(trade, 'quote_volume')
        symbol = market['symbol']
        fee = None
        feeCostString = self.safe_string(trade, 'fee')
        if feeCostString is not None:
            feeCurrencyCode = market['quote']
            fee = {
                'cost': feeCostString,
                'currency': feeCurrencyCode,
            }
        return self.safe_trade({
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': orderId,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': costString,
            'fee': fee,
        }, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'page': 0,
        }
        if since is not None:
            request['since'] = self.iso8601(since)
        response = self.v1PostListExecutedOrdersSymbol(self.extend(request, params))
        #
        #     {
        #         "data": [
        #             {
        #                 "type": "BTC Sell order executed",
        #                 "typeI": 6,
        #                 "crypto": 5000,
        #                 "amount": 35.4,
        #                 "rate": 709800,
        #                 "date": "2020-05-22T15:05:34.000Z",
        #                 "unit": "INR",
        #                 "factor": 100000000,
        #                 "fee": 0.09,
        #                 "delh_btc": -5000,
        #                 "delh_inr": 0,
        #                 "del_btc": 0,
        #                 "del_inr": 35.4,
        #                 "id": "2938823"
        #             },
        #             {
        #                 "type": "BTC Sell order executed",
        #                 "typeI": 6,
        #                 "crypto": 195000,
        #                 "amount": 1380.58,
        #                 "rate": 709765.5,
        #                 "date": "2020-05-22T15:05:34.000Z",
        #                 "unit": "INR",
        #                 "factor": 100000000,
        #                 "fee": 3.47,
        #                 "delh_btc": -195000,
        #                 "delh_inr": 0,
        #                 "del_btc": 0,
        #                 "del_inr": 1380.58,
        #                 "id": "2938823"
        #             }
        #         ],
        #         "status": 1,
        #         "error": null,
        #         "code": 200
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchTrades() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
            'market': market['quoteId'],
        }
        response = self.wwwGetExchangeDataTradedetails(self.extend(request, params))
        #
        #     [
        #         {"tradeId":"1909151","price":"61904.6300","quote_volume":1618.05,"base_volume":0.02607254,"timestamp":1634548602000,"type":"buy"},
        #         {"tradeId":"1909153","price":"61893.9000","quote_volume":16384.42,"base_volume":0.26405767,"timestamp":1634548999000,"type":"sell"},
        #         {"tradeId":"1909155","price":"61853.1100","quote_volume":2304.37,"base_volume":0.03716263,"timestamp":1634549670000,"type":"sell"}
        #     }
        #
        return self.parse_trades(response, market, since, limit)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchDeposits() requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['id'],
            'page': 0,
        }
        response = self.v1PostDepositHistorySymbol(self.extend(request, params))
        #
        #     {
        #         "data":[
        #             {
        #                 "type":"USDT deposited",
        #                 "typeI":1,
        #                 "amount":100,
        #                 "date":"2021-04-24T14:56:04.000Z",
        #                 "unit":"USDT",
        #                 "factor":100,
        #                 "fee":0,
        #                 "delh_btc":0,
        #                 "delh_inr":0,
        #                 "rate":0,
        #                 "del_btc":10000,
        #                 "del_inr":0
        #             }
        #         ],
        #         "status":1,
        #         "error":null,
        #         "code":200
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_transactions(data, currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchWithdrawals() requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['id'],
            'page': 0,
        }
        response = self.v1PostWithdrawHistorySymbol(self.extend(request, params))
        #
        #     ...
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_transactions(data, currency, since, limit)

    def parse_transaction_status_by_type(self, status, type=None):
        statusesByType = {
            'deposit': {
                '0': 'pending',
                '1': 'ok',
            },
            'withdrawal': {
                '0': 'pending',  # Email Sent
                '1': 'canceled',  # Cancelled(different from 1 = ok in deposits)
                '2': 'pending',  # Awaiting Approval
                '3': 'failed',  # Rejected
                '4': 'pending',  # Processing
                '5': 'failed',  # Failure
                '6': 'ok',  # Completed
            },
        }
        statuses = self.safe_value(statusesByType, type, {})
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #     {
        #         "type":"USDT deposited",
        #         "typeI":1,
        #         "amount":100,
        #         "date":"2021-04-24T14:56:04.000Z",
        #         "unit":"USDT",
        #         "factor":100,
        #         "fee":0,
        #         "delh_btc":0,
        #         "delh_inr":0,
        #         "rate":0,
        #         "del_btc":10000,
        #         "del_inr":0
        #     }
        #
        # fetchWithdrawals
        #
        #     ...
        #
        currencyId = self.safe_string(transaction, 'unit')
        code = self.safe_currency_code(currencyId, currency)
        timestamp = self.parse8601(self.safe_string(transaction, 'date'))
        type = self.safe_string(transaction, 'type')
        status = None
        if type is not None:
            if type.find('deposit') >= 0:
                type = 'deposit'
                status = 'ok'
            elif type.find('withdraw') >= 0:
                type = 'withdrawal'
        # status = self.parse_transaction_status_by_type(self.safe_string(transaction, 'status'), type)
        amount = self.safe_number(transaction, 'amount')
        feeCost = self.safe_number(transaction, 'fee')
        fee = None
        if feeCost is not None:
            fee = {'currency': code, 'cost': feeCost}
        return {
            'info': transaction,
            'id': None,
            'txid': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'network': None,
            'address': None,
            'addressTo': None,
            'addressFrom': None,
            'tag': None,
            'tagTo': None,
            'tagFrom': None,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'internal': None,
            'fee': fee,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'symbol': currency['id'],
        }
        response = self.v1PostGetCoinAddressSymbol(self.extend(request, params))
        #
        #     {
        #         "data":{
        #             "token":"0x680dee9edfff0c397736e10b017cf6a0aee4ba31",
        #             "expiry":"2022-04-24 22:30:11"
        #         },
        #         "status":1,
        #         "error":null
        #     }
        #
        data = self.safe_value(response, 'data', {})
        address = self.safe_string(data, 'token')
        tag = self.safe_string(data, 'tag')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'network': None,
            'info': response,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='www', method='GET', params={}, headers=None, body=None):
        if not (api in self.urls['api']):
            raise ExchangeError(self.id + ' does not have a testnet/sandbox URL for ' + api + ' endpoints')
        if api != 'www':
            self.check_required_credentials()
            headers = {
                'X-BITBNS-APIKEY': self.apiKey,
            }
        baseUrl = self.implode_hostname(self.urls['api'][api])
        url = baseUrl + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        nonce = str(self.nonce())
        if method == 'GET':
            if query:
                url += '?' + self.urlencode(query)
        elif method == 'POST':
            if query:
                body = self.json(query)
            else:
                body = '{}'
            auth = {
                'timeStamp_nonce': nonce,
                'body': body,
            }
            payload = self.string_to_base64(self.json(auth))
            signature = self.hmac(payload, self.encode(self.secret), hashlib.sha512)
            headers['X-BITBNS-PAYLOAD'] = self.decode(payload)
            headers['X-BITBNS-SIGNATURE'] = signature
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        #
        #     {"msg":"Invalid Request","status":-1,"code":400}
        #     {"data":[],"status":0,"error":"Nothing to show","code":417}
        #
        code = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg')
        error = (code is not None) and (code != '200')
        if error or (message is not None):
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
            raise ExchangeError(feedback)  # unknown message
