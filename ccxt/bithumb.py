# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import DECIMAL_PLACES
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS


class bithumb(Exchange):

    def describe(self):
        return self.deep_extend(super(bithumb, self).describe(), {
            'id': 'bithumb',
            'name': 'Bithumb',
            'countries': ['KR'],  # South Korea
            'rateLimit': 500,
            'has': {
                'cancelOrder': True,
                'CORS': True,
                'createMarketOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30597177-ea800172-9d5e-11e7-804c-b9d4fa9b56b0.jpg',
                'api': {
                    'public': 'https://api.bithumb.com/public',
                    'private': 'https://api.bithumb.com',
                },
                'www': 'https://www.bithumb.com',
                'doc': 'https://apidocs.bithumb.com',
                'fees': 'https://en.bithumb.com/customer_support/info_fee',
            },
            'api': {
                'public': {
                    'get': [
                        'ticker/{currency}',
                        'ticker/all',
                        'orderbook/{currency}',
                        'orderbook/all',
                        'transaction_history/{currency}',
                        'transaction_history/all',
                        'candlestick/{currency}/{interval}',
                    ],
                },
                'private': {
                    'post': [
                        'info/account',
                        'info/balance',
                        'info/wallet_address',
                        'info/ticker',
                        'info/orders',
                        'info/user_transactions',
                        'info/order_detail',
                        'trade/place',
                        'trade/cancel',
                        'trade/btc_withdrawal',
                        'trade/krw_deposit',
                        'trade/krw_withdrawal',
                        'trade/market_buy',
                        'trade/market_sell',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.25 / 100,
                    'taker': 0.25 / 100,
                },
            },
            'precisionMode': SIGNIFICANT_DIGITS,
            'exceptions': {
                'Bad Request(SSL)': BadRequest,
                'Bad Request(Bad Method)': BadRequest,
                'Bad Request.(Auth Data)': AuthenticationError,  # {"status": "5100", "message": "Bad Request.(Auth Data)"}
                'Not Member': AuthenticationError,
                'Invalid Apikey': AuthenticationError,  # {"status":"5300","message":"Invalid Apikey"}
                'Method Not Allowed.(Access IP)': PermissionDenied,
                'Method Not Allowed.(BTC Adress)': InvalidAddress,
                'Method Not Allowed.(Access)': PermissionDenied,
                'Database Fail': ExchangeNotAvailable,
                'Invalid Parameter': BadRequest,
                '5600': ExchangeError,
                'Unknown Error': ExchangeError,
                'After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions': ExchangeError,  # {"status":"5100","message":"After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions"}
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '10m': '10m',
                '30m': '30m',
                '1h': '1h',
                '6h': '6h',
                '12h': '12h',
                '1d': '24h',
            },
        })

    def amount_to_precision(self, symbol, amount):
        return self.decimal_to_precision(amount, TRUNCATE, self.markets[symbol]['precision']['amount'], DECIMAL_PLACES)

    def fetch_markets(self, params={}):
        response = self.publicGetTickerAll(params)
        data = self.safe_value(response, 'data')
        currencyIds = list(data.keys())
        result = []
        quote = self.safe_currency_code('KRW')
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            if currencyId == 'date':
                continue
            market = data[currencyId]
            base = self.safe_currency_code(currencyId)
            symbol = currencyId + '/' + quote
            active = True
            if isinstance(market, list):
                numElements = len(market)
                if numElements == 0:
                    active = False
            result.append({
                'id': currencyId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'info': market,
                'active': active,
                'precision': {
                    'amount': 4,
                    'price': 4,
                },
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
                        'min': 500,
                        'max': 5000000000,
                    },
                },
                'baseId': None,
                'quoteId': None,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        request = {
            'currency': 'ALL',
        }
        response = self.privatePostInfoBalance(self.extend(request, params))
        result = {'info': response}
        balances = self.safe_value(response, 'data')
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            account = self.account()
            currency = self.currency(code)
            lowerCurrencyId = self.safe_string_lower(currency, 'id')
            account['total'] = self.safe_float(balances, 'total_' + lowerCurrencyId)
            account['used'] = self.safe_float(balances, 'in_use_' + lowerCurrencyId)
            account['free'] = self.safe_float(balances, 'available_' + lowerCurrencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        if limit is not None:
            request['count'] = limit  # default 30, max 30
        response = self.publicGetOrderbookCurrency(self.extend(request, params))
        #
        #     {
        #         "status":"0000",
        #         "data":{
        #             "timestamp":"1587621553942",
        #             "payment_currency":"KRW",
        #             "order_currency":"BTC",
        #             "bids":[
        #                 {"price":"8652000","quantity":"0.0043"},
        #                 {"price":"8651000","quantity":"0.0049"},
        #                 {"price":"8650000","quantity":"8.4791"},
        #             ],
        #             "asks":[
        #                 {"price":"8654000","quantity":"0.119"},
        #                 {"price":"8655000","quantity":"0.254"},
        #                 {"price":"8658000","quantity":"0.119"},
        #             ]
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(data, 'timestamp')
        return self.parse_order_book(data, timestamp, 'bids', 'asks', 'price', 'quantity')

    def parse_ticker(self, ticker, market=None):
        #
        # fetchTicker, fetchTickers
        #
        #     {
        #         "opening_price":"227100",
        #         "closing_price":"228400",
        #         "min_price":"222300",
        #         "max_price":"230000",
        #         "units_traded":"82618.56075337",
        #         "acc_trade_value":"18767376138.6031",
        #         "prev_closing_price":"227100",
        #         "units_traded_24H":"151871.13484676",
        #         "acc_trade_value_24H":"34247610416.8974",
        #         "fluctate_24H":"8700",
        #         "fluctate_rate_24H":"3.96",
        #         "date":"1587710327264",  # fetchTickers inject self
        #     }
        #
        timestamp = self.safe_integer(ticker, 'date')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        open = self.safe_float(ticker, 'opening_price')
        close = self.safe_float(ticker, 'closing_price')
        change = None
        percentage = None
        average = None
        if (close is not None) and (open is not None):
            change = close - open
            if open > 0:
                percentage = change / open * 100
            average = self.sum(open, close) / 2
        baseVolume = self.safe_float(ticker, 'units_traded_24H')
        quoteVolume = self.safe_float(ticker, 'acc_trade_value_24H')
        vwap = self.vwap(baseVolume, quoteVolume)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'max_price'),
            'low': self.safe_float(ticker, 'min_price'),
            'bid': self.safe_float(ticker, 'buy_price'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell_price'),
            'askVolume': None,
            'vwap': vwap,
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTickerAll(params)
        #
        #     {
        #         "status":"0000",
        #         "data":{
        #             "BTC":{
        #                 "opening_price":"9045000",
        #                 "closing_price":"9132000",
        #                 "min_price":"8938000",
        #                 "max_price":"9168000",
        #                 "units_traded":"4619.79967497",
        #                 "acc_trade_value":"42021363832.5187",
        #                 "prev_closing_price":"9041000",
        #                 "units_traded_24H":"8793.5045804",
        #                 "acc_trade_value_24H":"78933458515.4962",
        #                 "fluctate_24H":"530000",
        #                 "fluctate_rate_24H":"6.16"
        #             },
        #             "date":"1587710878669"
        #         }
        #     }
        #
        result = {}
        data = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(data, 'date')
        tickers = self.omit(data, 'date')
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            ticker = tickers[id]
            isArray = isinstance(ticker, list)
            if not isArray:
                ticker['date'] = timestamp
                result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        response = self.publicGetTickerCurrency(self.extend(request, params))
        #
        #     {
        #         "status":"0000",
        #         "data":{
        #             "opening_price":"227100",
        #             "closing_price":"228400",
        #             "min_price":"222300",
        #             "max_price":"230000",
        #             "units_traded":"82618.56075337",
        #             "acc_trade_value":"18767376138.6031",
        #             "prev_closing_price":"227100",
        #             "units_traded_24H":"151871.13484676",
        #             "acc_trade_value_24H":"34247610416.8974",
        #             "fluctate_24H":"8700",
        #             "fluctate_rate_24H":"3.96",
        #             "date":"1587710327264"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_ticker(data, market)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         1576823400000,  # 기준 시간
        #         '8284000',  # 시가
        #         '8286000',  # 종가
        #         '8289000',  # 고가
        #         '8276000',  # 저가
        #         '15.41503692'  # 거래량
        #     ]
        #
        return [
            self.safe_integer(ohlcv, 0),
            self.safe_float(ohlcv, 1),
            self.safe_float(ohlcv, 3),
            self.safe_float(ohlcv, 4),
            self.safe_float(ohlcv, 2),
            self.safe_float(ohlcv, 5),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
            'interval': self.timeframes[timeframe],
        }
        response = self.publicGetCandlestickCurrencyInterval(self.extend(request, params))
        #
        #     {
        #         'status': '0000',
        #         'data': {
        #             [
        #                 1576823400000,  # 기준 시간
        #                 '8284000',  # 시가
        #                 '8286000',  # 종가
        #                 '8289000',  # 고가
        #                 '8276000',  # 저가
        #                 '15.41503692'  # 거래량
        #             ],
        #             [
        #                 1576824000000,  # 기준 시간
        #                 '8284000',  # 시가
        #                 '8281000',  # 종가
        #                 '8289000',  # 고가
        #                 '8275000',  # 저가
        #                 '6.19584467'  # 거래량
        #             ],
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "transaction_date":"2020-04-23 22:21:46",
        #         "type":"ask",
        #         "units_traded":"0.0125",
        #         "price":"8667000",
        #         "total":"108337"
        #     }
        #
        # fetchOrder(private)
        #
        #     {
        #         "transaction_date": "1572497603902030",
        #         "price": "8601000",
        #         "units": "0.005",
        #         "fee_currency": "KRW",
        #         "fee": "107.51",
        #         "total": "43005"
        #     }
        #
        # a workaround for their bug in date format, hours are not 0-padded
        timestamp = None
        transactionDatetime = self.safe_string(trade, 'transaction_date')
        if transactionDatetime is not None:
            parts = transactionDatetime.split(' ')
            numParts = len(parts)
            if numParts > 1:
                transactionDate = parts[0]
                transactionTime = parts[1]
                if len(transactionTime) < 8:
                    transactionTime = '0' + transactionTime
                timestamp = self.parse8601(transactionDate + ' ' + transactionTime)
            else:
                timestamp = self.safe_integer_product(trade, 'transaction_date', 0.001)
        if timestamp is not None:
            timestamp -= 9 * 3600000  # they report UTC + 9 hours, server in Korean timezone
        type = None
        side = self.safe_string(trade, 'type')
        side = 'sell' if (side == 'ask') else 'buy'
        id = self.safe_string(trade, 'cont_no')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        price = self.safe_float(trade, 'price')
        amount = self.safe_float_2(trade, 'units_traded', 'units')
        cost = self.safe_float(trade, 'total')
        if cost is None:
            if amount is not None:
                if price is not None:
                    cost = price * amount
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'fee_currency')
            feeCurrencyCode = self.common_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        if limit is None:
            request['count'] = limit  # default 20, max 100
        response = self.publicGetTransactionHistoryCurrency(self.extend(request, params))
        #
        #     {
        #         "status":"0000",
        #         "data":[
        #             {
        #                 "transaction_date":"2020-04-23 22:21:46",
        #                 "type":"ask",
        #                 "units_traded":"0.0125",
        #                 "price":"8667000",
        #                 "total":"108337"
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_currency': market['id'],
            'payment_currency': market['quote'],
            'units': amount,
        }
        method = 'privatePostTradePlace'
        if type == 'limit':
            request['price'] = price
            request['type'] = 'bid' if (side == 'buy') else 'ask'
        else:
            method = 'privatePostTradeMarket' + self.capitalize(side)
        response = getattr(self, method)(self.extend(request, params))
        id = self.safe_string(response, 'order_id')
        if id is None:
            raise InvalidOrder(self.id + ' createOrder did not return an order id')
        return {
            'info': response,
            'symbol': symbol,
            'type': type,
            'side': side,
            'id': id,
        }

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'count': 1,
            'order_currency': market['base'],
            'payment_currency': market['quote'],
        }
        response = self.privatePostInfoOrderDetail(self.extend(request, params))
        #
        #     {
        #         "status": "0000",
        #         "data": {
        #             order_date: '1603161798539254',
        #             type: 'ask',
        #             order_status: 'Cancel',
        #             order_currency: 'BTC',
        #             payment_currency: 'KRW',
        #             watch_price: '0',
        #             order_price: '13344000',
        #             order_qty: '0.0125',
        #             cancel_date: '1603161803809993',
        #             cancel_type: '사용자취소',
        #             contract: [
        #                 {
        #                     transaction_date: '1603161799976383',
        #                     price: '13344000',
        #                     units: '0.0015',
        #                     fee_currency: 'KRW',
        #                     fee: '0',
        #                     total: '20016'
        #                 }
        #             ],
        #         }
        #     }
        #
        data = self.safe_value(response, 'data')
        return self.parse_order(self.extend(data, {'order_id': id}), market)

    def parse_order_status(self, status):
        statuses = {
            'Pending': 'open',
            'Completed': 'closed',
            'Cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #
        # fetchOrder
        #
        #     {
        #         "transaction_date": "1572497603668315",
        #         "type": "bid",
        #         "order_status": "Completed",
        #         "order_currency": "BTC",
        #         "payment_currency": "KRW",
        #         "order_price": "8601000",
        #         "order_qty": "0.007",
        #         "cancel_date": "",
        #         "cancel_type": "",
        #         "contract": [
        #             {
        #                 "transaction_date": "1572497603902030",
        #                 "price": "8601000",
        #                 "units": "0.005",
        #                 "fee_currency": "KRW",
        #                 "fee": "107.51",
        #                 "total": "43005"
        #             },
        #         ]
        #     }
        #
        #     {
        #         order_date: '1603161798539254',
        #         type: 'ask',
        #         order_status: 'Cancel',
        #         order_currency: 'BTC',
        #         payment_currency: 'KRW',
        #         watch_price: '0',
        #         order_price: '13344000',
        #         order_qty: '0.0125',
        #         cancel_date: '1603161803809993',
        #         cancel_type: '사용자취소',
        #         contract: [
        #             {
        #                 transaction_date: '1603161799976383',
        #                 price: '13344000',
        #                 units: '0.0015',
        #                 fee_currency: 'KRW',
        #                 fee: '0',
        #                 total: '20016'
        #             }
        #         ],
        #     }
        #
        # fetchOpenOrders
        #
        #     {
        #         "order_currency": "BTC",
        #         "payment_currency": "KRW",
        #         "order_id": "C0101000007408440032",
        #         "order_date": "1571728739360570",
        #         "type": "bid",
        #         "units": "5.0",
        #         "units_remaining": "5.0",
        #         "price": "501000",
        #     }
        #
        timestamp = self.safe_integer_product(order, 'order_date', 0.001)
        sideProperty = self.safe_value_2(order, 'type', 'side')
        side = 'buy' if (sideProperty == 'bid') else 'sell'
        status = self.parse_order_status(self.safe_string(order, 'order_status'))
        price = self.safe_float_2(order, 'order_price', 'price')
        type = 'limit'
        if price == 0:
            price = None
            type = 'market'
        amount = self.safe_float_2(order, 'order_qty', 'units')
        remaining = self.safe_float(order, 'units_remaining')
        if remaining is None:
            if status == 'closed':
                remaining = 0
            elif status != 'canceled':
                remaining = amount
        symbol = None
        baseId = self.safe_string(order, 'order_currency')
        quoteId = self.safe_string(order, 'payment_currency')
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        if (base is not None) and (quote is not None):
            symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        filled = None
        cost = None
        average = None
        id = self.safe_string(order, 'order_id')
        rawTrades = self.safe_value(order, 'contract')
        trades = None
        fee = None
        fees = None
        feesByCurrency = None
        if rawTrades is not None:
            trades = self.parse_trades(rawTrades, market, None, None, {
                'side': side,
                'symbol': symbol,
                'order': id,
            })
            filled = 0
            feesByCurrency = {}
            for i in range(0, len(trades)):
                trade = trades[i]
                filled = self.sum(filled, trade['amount'])
                cost = self.sum(cost, trade['cost'])
                tradeFee = trade['fee']
                feeCurrency = tradeFee['currency']
                if feeCurrency in feesByCurrency:
                    feesByCurrency[feeCurrency] = {
                        'currency': feeCurrency,
                        'cost': self.sum(feesByCurrency[feeCurrency]['cost'], tradeFee['cost']),
                    }
                else:
                    feesByCurrency[feeCurrency] = {
                        'currency': feeCurrency,
                        'cost': tradeFee['cost'],
                    }
            feeCurrencies = list(feesByCurrency.keys())
            feeCurrenciesLength = len(feeCurrencies)
            if feeCurrenciesLength > 1:
                fees = []
                for i in range(0, len(feeCurrencies)):
                    feeCurrency = feeCurrencies[i]
                    fees.append(feesByCurrency[feeCurrency])
            else:
                fee = self.safe_value(feesByCurrency, feeCurrencies[0])
            if filled != 0:
                average = cost / filled
        if amount is not None:
            if (filled is None) and (remaining is not None):
                filled = max(0, amount - remaining)
            if (remaining is None) and (filled is not None):
                remaining = max(0, amount - filled)
        result = {
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
            'fee': None,
            'trades': trades,
        }
        if fee is not None:
            result['fee'] = fee
        elif fees is not None:
            result['fees'] = fees
        return result

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        request = {
            'count': limit,
            'order_currency': market['base'],
            'payment_currency': market['quote'],
        }
        if since is not None:
            request['after'] = since
        response = self.privatePostInfoOrders(self.extend(request, params))
        #
        #     {
        #         "status": "0000",
        #         "data": [
        #             {
        #                 "order_currency": "BTC",
        #                 "payment_currency": "KRW",
        #                 "order_id": "C0101000007408440032",
        #                 "order_date": "1571728739360570",
        #                 "type": "bid",
        #                 "units": "5.0",
        #                 "units_remaining": "5.0",
        #                 "price": "501000",
        #             }
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_orders(data, market, since, limit)

    def cancel_order(self, id, symbol=None, params={}):
        side_in_params = ('side' in params)
        if not side_in_params:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a `symbol` argument and a `side` parameter(sell or buy)')
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a `symbol` argument and a `side` parameter(sell or buy)')
        market = self.market(symbol)
        side = 'bid' if (params['side'] == 'buy') else 'ask'
        params = self.omit(params, ['side', 'currency'])
        # https://github.com/ccxt/ccxt/issues/6771
        request = {
            'order_id': id,
            'type': side,
            'order_currency': market['base'],
            'payment_currency': market['quote'],
        }
        return self.privatePostTradeCancel(self.extend(request, params))

    def cancel_unified_order(self, order, params={}):
        request = {
            'side': order['side'],
        }
        return self.cancel_order(order['id'], order['symbol'], self.extend(request, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'units': amount,
            'address': address,
            'currency': currency['id'],
        }
        if currency == 'XRP' or currency == 'XMR':
            destination = self.safe_string(params, 'destination')
            if (tag is None) and (destination is None):
                raise ArgumentsRequired(self.id + ' ' + code + ' withdraw() requires a tag argument or an extra destination param')
            elif tag is not None:
                request['destination'] = tag
        response = self.privatePostTradeBtcWithdrawal(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        endpoint = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + endpoint
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'endpoint': endpoint,
            }, query))
            nonce = str(self.nonce())
            auth = endpoint + "\0" + body + "\0" + nonce  # eslint-disable-line quotes
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            signature64 = self.decode(self.string_to_base64(signature))
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Api-Key': self.apiKey,
                'Api-Sign': signature64,
                'Api-Nonce': nonce,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if 'status' in response:
            #
            #     {"status":"5100","message":"After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions"}
            #
            status = self.safe_string(response, 'status')
            message = self.safe_string(response, 'message')
            if status is not None:
                if status == '0000':
                    return  # no error
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, status, feedback)
                self.throw_exactly_matched_exception(self.exceptions, message, feedback)
                raise ExchangeError(feedback)

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'status' in response:
            if response['status'] == '0000':
                return response
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
