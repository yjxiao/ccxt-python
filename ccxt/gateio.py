# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection


class gateio(Exchange):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'id': 'gateio',
            'name': 'Gate.io',
            'countries': ['CN'],
            'version': '2',
            'rateLimit': 1000,
            'pro': True,
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createDepositAddress': True,
                'createMarketOrder': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': False,
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchDeposits': True,
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchOrderTrades': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTransactions': True,
                'fetchWithdrawals': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': 60,
                '5m': 300,
                '10m': 600,
                '15m': 900,
                '30m': 1800,
                '1h': 3600,
                '2h': 7200,
                '4h': 14400,
                '6h': 21600,
                '12h': 43200,
                '1d': 86400,
                '1w': 604800,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31784029-0313c702-b509-11e7-9ccc-bc0da6a0e435.jpg',
                'api': {
                    'public': 'https://data.gate.io/api',
                    'private': 'https://data.gate.io/api',
                },
                'www': 'https://gate.io/',
                'doc': 'https://gate.io/api2',
                'fees': [
                    'https://gate.io/fee',
                    'https://support.gate.io/hc/en-us/articles/115003577673',
                ],
                'referral': 'https://www.gate.io/signup/2436035',
            },
            'api': {
                'public': {
                    'get': [
                        'candlestick2/{id}',
                        'pairs',
                        'coininfo',
                        'marketinfo',
                        'marketlist',
                        'coininfo',
                        'tickers',
                        'ticker/{id}',
                        'orderBook/{id}',
                        'trade/{id}',
                        'tradeHistory/{id}',
                        'tradeHistory/{id}/{tid}',
                    ],
                },
                'private': {
                    'post': [
                        'balances',
                        'depositAddress',
                        'newAddress',
                        'depositsWithdrawals',
                        'buy',
                        'sell',
                        'cancelOrder',
                        'cancelAllOrders',
                        'getOrder',
                        'openOrders',
                        'tradeHistory',
                        'feelist',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.002,
                    'taker': 0.002,
                },
            },
            'exceptions': {
                'exact': {
                    '4': DDoSProtection,
                    '5': AuthenticationError,  # {result: "false", code:  5, message: "Error: invalid key or sign, please re-generate it from your account"}
                    '6': AuthenticationError,  # {result: 'false', code: 6, message: 'Error: invalid data  '}
                    '7': NotSupported,
                    '8': NotSupported,
                    '9': NotSupported,
                    '15': DDoSProtection,
                    '16': OrderNotFound,
                    '17': OrderNotFound,
                    '20': InvalidOrder,
                    '21': InsufficientFunds,
                },
                # https://gate.io/api2#errCode
                'errorCodeNames': {
                    '1': 'Invalid request',
                    '2': 'Invalid version',
                    '3': 'Invalid request',
                    '4': 'Too many attempts',
                    '5': 'Invalid sign',
                    '6': 'Invalid sign',
                    '7': 'Currency is not supported',
                    '8': 'Currency is not supported',
                    '9': 'Currency is not supported',
                    '10': 'Verified failed',
                    '11': 'Obtaining address failed',
                    '12': 'Empty params',
                    '13': 'Internal error, please report to administrator',
                    '14': 'Invalid user',
                    '15': 'Cancel order too fast, please wait 1 min and try again',
                    '16': 'Invalid order id or order is already closed',
                    '17': 'Invalid orderid',
                    '18': 'Invalid amount',
                    '19': 'Not permitted or trade is disabled',
                    '20': 'Your order size is too small',
                    '21': 'You don\'t have enough fund',
                },
            },
            'options': {
                'fetchTradesMethod': 'public_get_tradehistory_id',  # 'public_get_tradehistory_id_tid'
                'limits': {
                    'cost': {
                        'min': {
                            'BTC': 0.0001,
                            'ETH': 0.001,
                            'USDT': 1,
                        },
                    },
                },
            },
            'commonCurrencies': {
                'BTCBEAR': 'BEAR',
                'BTCBULL': 'BULL',
            },
        })

    def fetch_currencies(self, params={}):
        response = self.publicGetCoininfo(params)
        #
        #     {
        #         "result":"true",
        #         "coins":[
        #             {
        #                 "CNYX":{
        #                     "delisted":0,
        #                     "withdraw_disabled":1,
        #                     "withdraw_delayed":0,
        #                     "deposit_disabled":0,
        #                     "trade_disabled":0
        #                 }
        #             },
        #             {
        #                 "USDT_ETH":{
        #                     "delisted":0,
        #                     "withdraw_disabled":1,
        #                     "withdraw_delayed":0,
        #                     "deposit_disabled":0,
        #                     "trade_disabled":1
        #                 }
        #             }
        #         ]
        #     }
        #
        coins = self.safe_value(response, 'coins')
        if not coins:
            raise ExchangeError(self.id + ' fetchCurrencies got an unrecognized response')
        result = {}
        for i in range(0, len(coins)):
            coin = coins[i]
            ids = list(coin.keys())
            for j in range(0, len(ids)):
                id = ids[j]
                currency = coin[id]
                code = self.safe_currency_code(id)
                delisted = self.safe_value(currency, 'delisted', 0)
                withdrawDisabled = self.safe_value(currency, 'withdraw_disabled', 0)
                depositDisabled = self.safe_value(currency, 'deposit_disabled', 0)
                tradeDisabled = self.safe_value(currency, 'trade_disabled', 0)
                listed = (delisted == 0)
                withdrawEnabled = (withdrawDisabled == 0)
                depositEnabled = (depositDisabled == 0)
                tradeEnabled = (tradeDisabled == 0)
                active = listed and withdrawEnabled and depositEnabled and tradeEnabled
                result[code] = {
                    'id': id,
                    'code': code,
                    'active': active,
                    'info': currency,
                    'name': None,
                    'fee': None,
                    'precision': None,
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

    def fetch_markets(self, params={}):
        response = self.publicGetMarketinfo(params)
        #
        #     {
        #         "result":"true",
        #         "pairs":[
        #             {
        #                 "usdt_cnyx":{
        #                     "decimal_places":3,
        #                     "amount_decimal_places":3,
        #                     "min_amount":1,
        #                     "min_amount_a":1,
        #                     "min_amount_b":3,
        #                     "fee":0.02,
        #                     "trade_disabled":0,
        #                     "buy_disabled":0,
        #                     "sell_disabled":0
        #                 }
        #             },
        #         ]
        #     }
        #
        markets = self.safe_value(response, 'pairs')
        if not markets:
            raise ExchangeError(self.id + ' fetchMarkets got an unrecognized response')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            keys = list(market.keys())
            id = self.safe_string(keys, 0)
            details = market[id]
            # all of their symbols are separated with an underscore
            # but not boe_eth_eth(BOE_ETH/ETH) which has two underscores
            # https://github.com/ccxt/ccxt/issues/4894
            parts = id.split('_')
            numParts = len(parts)
            baseId = parts[0]
            quoteId = parts[1]
            if numParts > 2:
                baseId = parts[0] + '_' + parts[1]
                quoteId = parts[2]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(details, 'amount_decimal_places'),
                'price': self.safe_integer(details, 'decimal_places'),
            }
            amountLimits = {
                'min': self.safe_float(details, 'min_amount'),
                'max': None,
            }
            priceLimits = {
                'min': math.pow(10, -precision['price']),
                'max': None,
            }
            defaultCost = amountLimits['min'] * priceLimits['min']
            minCost = self.safe_float(self.options['limits']['cost']['min'], quote, defaultCost)
            costLimits = {
                'min': minCost,
                'max': None,
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            disabled = self.safe_value(details, 'trade_disabled')
            active = not disabled
            uppercaseId = id.upper()
            fee = self.safe_float(details, 'fee')
            result.append({
                'id': id,
                'uppercaseId': uppercaseId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'maker': fee / 100,
                'taker': fee / 100,
                'precision': precision,
                'limits': limits,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalances(params)
        result = {'info': response}
        available = self.safe_value(response, 'available', {})
        if isinstance(available, list):
            available = {}
        locked = self.safe_value(response, 'locked', {})
        currencyIds = list(available.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(available, currencyId)
            account['used'] = self.safe_float(locked, currencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        response = self.publicGetOrderBookId(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_ohlcv(self, ohlcv, market=None):
        # they return [Timestamp, Volume, Close, High, Low, Open]
        return [
            self.safe_integer(ohlcv, 0),  # t
            self.safe_float(ohlcv, 5),  # o
            self.safe_float(ohlcv, 3),  # h
            self.safe_float(ohlcv, 4),  # l
            self.safe_float(ohlcv, 2),  # c
            self.safe_float(ohlcv, 1),  # v
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
            'group_sec': self.timeframes[timeframe],
        }
        # max limit = 1001
        if limit is not None:
            periodDurationInSeconds = self.parse_timeframe(timeframe)
            hours = int((periodDurationInSeconds * limit) / 3600)
            request['range_hour'] = max(0, hours - 1)
        response = self.publicGetCandlestick2Id(self.extend(request, params))
        #
        #     {
        #         "elapsed": "15ms",
        #         "result": "true",
        #         "data": [
        #             ["1553930820000", "1.005299", "4081.05", "4086.18", "4081.05", "4086.18"],
        #             ["1553930880000", "0.110923277", "4095.2", "4095.23", "4091.15", "4091.15"],
        #             ...
        #             ["1553934420000", "0", "4089.42", "4089.42", "4089.42", "4089.42"],
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'percentChange')
        open = None
        change = None
        average = None
        if (last is not None) and (percentage is not None):
            relativeChange = percentage / 100
            open = last / self.sum(1, relativeChange)
            change = last - open
            average = self.sum(last, open) / 2
        open = self.safe_float(ticker, 'open', open)
        change = self.safe_float(ticker, 'change', change)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float_2(ticker, 'high24hr', 'high'),
            'low': self.safe_float_2(ticker, 'low24hr', 'low'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'quoteVolume'),  # gateio has them reversed
            'quoteVolume': self.safe_float(ticker, 'baseVolume'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTickers(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            baseId, quoteId = id.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            symbol = base + '/' + quote
            market = None
            if symbol in self.markets:
                market = self.markets[symbol]
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
            result[symbol] = self.parse_ticker(response[id], market)
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetTickerId(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        # {
        #     "tradeID": 3175762,
        #     "date": "2017-08-25 07:24:28",
        #     "type": "sell",
        #     "rate": 29011,
        #     "amount": 0.0019,
        #     "total": 55.1209,
        #     "fee": "0",
        #     "fee_coin": "btc",
        #     "gt_fee":"0",
        #     "point_fee":"0.1213",
        # },
        timestamp = self.safe_timestamp_2(trade, 'timestamp', 'time_unix')
        timestamp = self.safe_timestamp(trade, 'time', timestamp)
        id = self.safe_string_2(trade, 'tradeID', 'id')
        # take either of orderid or orderId
        orderId = self.safe_string_2(trade, 'orderid', 'orderNumber')
        price = self.safe_float_2(trade, 'rate', 'price')
        amount = self.safe_float(trade, 'amount')
        type = self.safe_string(trade, 'type')
        takerOrMaker = self.safe_string(trade, 'role')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        fee = None
        feeCurrency = self.safe_currency_code(self.safe_string(trade, 'fee_coin'))
        feeCost = self.safe_float(trade, 'point_fee')
        if (feeCost is None) or (feeCost == 0):
            feeCost = self.safe_float(trade, 'gt_fee')
            if (feeCost is None) or (feeCost == 0):
                feeCost = self.safe_float(trade, 'fee')
            else:
                feeCurrency = self.safe_currency_code('GT')
        else:
            feeCurrency = self.safe_currency_code('POINT')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': None,
            'side': type,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        method = self.safe_string(self.options, 'fetchTradesMethod', 'public_get_tradehistory_id')
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        response = self.privatePostOpenOrders(params)
        return self.parse_orders(response['orders'], None, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderNumber': id,
            'currencyPair': self.market_id(symbol),
        }
        response = self.privatePostGetOrder(self.extend(request, params))
        return self.parse_order(response['order'])

    def parse_order_status(self, status):
        statuses = {
            'cancelled': 'canceled',
            # 'closed': 'closed',  # these two statuses aren't actually needed
            # 'open': 'open',  # as they are mapped one-to-one
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #        "fee": "0 ZEC",
        #         "code": 0,
        #         "rate": "0.0055",
        #         "side": 2,
        #         "type": "buy",
        #         "ctime": 1586460839.138,
        #         "market": "ZEC_BTC",
        #         "result": "true",
        #         "status": "open",
        #         "iceberg": "0",
        #         "message": "Success",
        #         "feeValue": "0",
        #         "filledRate": "0.005500000",
        #         "leftAmount": "0.60607456",
        #         "feeCurrency": "ZEC",
        #         "orderNumber": 10755887009,
        #         "filledAmount": "0",
        #         "feePercentage": 0.002,
        #         "initialAmount": "0.60607456"
        #     }
        #
        #     {
        #         'amount': '0.00000000',
        #         'currencyPair': 'xlm_usdt',
        #         'fee': '0.0113766632239302 USDT',
        #         'feeCurrency': 'USDT',
        #         'feePercentage': 0.18,
        #         'feeValue': '0.0113766632239302',
        #         'filledAmount': '30.14004987',
        #         'filledRate': 0.2097,
        #         'initialAmount': '30.14004987',
        #         'initialRate': '0.2097',
        #         'left': 0,
        #         'orderNumber': '998307286',
        #         'rate': '0.2097',
        #         'status': 'closed',
        #         'timestamp': 1531158583,
        #         'type': 'sell'
        #     }
        #
        #     {
        #         "orderNumber": 10802237760,
        #         "orderType": 1,
        #         "type": "buy",
        #         "rate": "0.54250000",
        #         "amount": "45.55638518",
        #         "total": "24.71433896",
        #         "initialRate": "0.54250000",
        #         "initialAmount": "45.55638518",
        #         "filledRate": "0.54250000",
        #         "filledAmount": "0",
        #         "currencyPair": "nano_usdt",
        #         "timestamp": 1586556143,
        #         "status": "open"
        #     }
        #
        id = self.safe_string_2(order, 'orderNumber', 'id')
        symbol = None
        marketId = self.safe_string(order, 'currencyPair')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_timestamp_2(order, 'timestamp', 'ctime')
        lastTradeTimestamp = self.safe_timestamp(order, 'mtime')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        side = self.safe_string(order, 'type')
        # handling for order.update messages
        if side == '1':
            side = 'sell'
        elif side == '2':
            side = 'buy'
        price = self.safe_float_2(order, 'initialRate', 'rate')
        average = self.safe_float(order, 'filledRate')
        amount = self.safe_float_2(order, 'initialAmount', 'amount')
        filled = self.safe_float(order, 'filledAmount')
        # In the order status response, self field has a different name.
        remaining = self.safe_float_2(order, 'leftAmount', 'left')
        if remaining is None:
            remaining = amount - filled
        feeCost = self.safe_float(order, 'feeValue')
        feeCurrencyId = self.safe_string(order, 'feeCurrency')
        feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
        feeRate = self.safe_float(order, 'feePercentage')
        if feeRate is not None:
            feeRate = feeRate / 100
        return {
            'id': id,
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': lastTradeTimestamp,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'average': average,
            'trades': None,
            'fee': {
                'cost': feeCost,
                'currency': feeCurrencyCode,
                'rate': feeRate,
            },
            'info': order,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        market = self.market(symbol)
        request = {
            'currencyPair': market['id'],
            'rate': price,
            'amount': amount,
        }
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_order(self.extend({
            'status': 'open',
            'type': side,
            'initialAmount': amount,
        }, response), market)

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires symbol argument')
        self.load_markets()
        request = {
            'orderNumber': id,
            'currencyPair': self.market_id(symbol),
        }
        return self.privatePostCancelOrder(self.extend(request, params))

    def query_deposit_address(self, method, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        method = 'privatePost' + method + 'Address'
        request = {
            'currency': currency['id'],
        }
        response = getattr(self, method)(self.extend(request, params))
        address = self.safe_string(response, 'addr')
        tag = None
        if (address is not None) and (address.find('address') >= 0):
            raise InvalidAddress(self.id + ' queryDepositAddress ' + address)
        if code == 'XRP':
            parts = address.split(' ')
            address = parts[0]
            tag = parts[1]
        return {
            'currency': currency,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def create_deposit_address(self, code, params={}):
        return self.query_deposit_address('New', code, params)

    def fetch_deposit_address(self, code, params={}):
        return self.query_deposit_address('Deposit', code, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostOpenOrders(params)
        return self.parse_orders(response['orders'], market, since, limit)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currencyPair': market['id'],
            'orderNumber': id,
        }
        response = self.privatePostTradeHistory(self.extend(request, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currencyPair': market['id'],
        }
        response = self.privatePostTradeHistory(self.extend(request, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'amount': amount,
            'address': address,  # Address must exist in you AddressBook in security settings
        }
        if tag is not None:
            request['address'] += ' ' + tag
        response = self.privatePostWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        prefix = (api + '/') if (api == 'private') else ''
        url = self.urls['api'][api] + self.version + '/1/' + prefix + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            request = {'nonce': nonce}
            body = self.urlencode(self.extend(request, query))
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Key': self.apiKey,
                'Sign': signature,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def fetch_transactions_by_type(self, type=None, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        if since is not None:
            request['start'] = since
        response = self.privatePostDepositsWithdrawals(self.extend(request, params))
        transactions = None
        if type is None:
            deposits = self.safe_value(response, 'deposits', [])
            withdrawals = self.safe_value(response, 'withdraws', [])
            transactions = self.array_concat(deposits, withdrawals)
        else:
            transactions = self.safe_value(response, type, [])
        currency = None
        if code is not None:
            currency = self.currency(code)
        return self.parse_transactions(transactions, currency, since, limit)

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type(None, code, since, limit, params)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('deposits', code, since, limit, params)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('withdraws', code, since, limit, params)

    def parse_transaction(self, transaction, currency=None):
        #
        # deposit
        #
        #     {
        #         'id': 'd16520849',
        #         'currency': 'NEO',
        #         'address': False,
        #         'amount': '1',
        #         'txid': '01acf6b8ce4d24a....',
        #         'timestamp': '1553125968',
        #         'status': 'DONE',
        #         'type': 'deposit'
        #     }
        #
        # withdrawal
        #
        #     {
        #         'id': 'w5864259',
        #         'currency': 'ETH',
        #         'address': '0x72632f462....',
        #         'amount': '0.4947',
        #         'txid': '0x111167d120f736....',
        #         'timestamp': '1553123688',
        #         'status': 'DONE',
        #         'type': 'withdrawal'
        #     }
        #
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        id = self.safe_string(transaction, 'id')
        txid = self.safe_string(transaction, 'txid')
        amount = self.safe_float(transaction, 'amount')
        address = self.safe_string(transaction, 'address')
        if address == 'false':
            address = None
        timestamp = self.safe_timestamp(transaction, 'timestamp')
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        type = self.parse_transaction_type(id[0])
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'currency': code,
            'amount': amount,
            'address': address,
            'tag': None,
            'status': status,
            'type': type,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'fee': None,
        }

    def parse_transaction_status(self, status):
        statuses = {
            'PEND': 'pending',
            'REQUEST': 'pending',
            'DMOVE': 'pending',
            'CANCEL': 'failed',
            'DONE': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction_type(self, type):
        types = {
            'd': 'deposit',
            'w': 'withdrawal',
        }
        return self.safe_string(types, type, type)

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        resultString = self.safe_string(response, 'result', '')
        if resultString != 'false':
            return
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'message', body)
        if errorCode is not None:
            feedback = self.safe_string(self.exceptions['errorCodeNames'], errorCode, message)
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
