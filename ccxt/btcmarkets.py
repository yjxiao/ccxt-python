# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import base64
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.decimal_to_precision import ROUND


class btcmarkets(Exchange):

    def describe(self):
        return self.deep_extend(super(btcmarkets, self).describe(), {
            'id': 'btcmarkets',
            'name': 'BTC Markets',
            'countries': ['AU'],  # Australia
            'rateLimit': 1000,  # market data cached for 1 second(trades cached for 2 seconds)
            'has': {
                'cancelOrder': True,
                'cancelOrders': True,
                'CORS': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': 'emulated',
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTransactions': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/89731817-b3fb8480-da52-11ea-817f-783b08aaf32b.jpg',
                'api': {
                    'public': 'https://api.btcmarkets.net',
                    'private': 'https://api.btcmarkets.net',
                    'privateV3': 'https://api.btcmarkets.net/v3',
                    'web': 'https://btcmarkets.net/data',
                },
                'www': 'https://btcmarkets.net',
                'doc': [
                    'https://api.btcmarkets.net/doc/v3#section/API-client-libraries',
                    'https://github.com/BTCMarkets/API',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'market/{id}/tick',
                        'market/{id}/orderbook',
                        'market/{id}/trades',
                        'v2/market/{id}/tickByTime/{timeframe}',
                        'v2/market/{id}/trades',
                        'v2/market/active',
                        'v3/markets',
                        'v3/markets/{marketId}/ticker',
                        'v3/markets/{marketId}/trades',
                        'v3/markets/{marketId}/orderbook',
                        'v3/markets/{marketId}/candles',
                        'v3/markets/tickers',
                        'v3/markets/orderbooks',
                        'v3/time',
                    ],
                },
                'private': {
                    'get': [
                        'account/balance',
                        'account/{id}/tradingfee',
                        'fundtransfer/history',
                        'v2/order/open',
                        'v2/order/open/{id}',
                        'v2/order/history/{instrument}/{currency}/',
                        'v2/order/trade/history/{id}',
                        'v2/transaction/history/{currency}',
                    ],
                    'post': [
                        'fundtransfer/withdrawCrypto',
                        'fundtransfer/withdrawEFT',
                        'order/create',
                        'order/cancel',
                        'order/history',
                        'order/open',
                        'order/trade/history',
                        'order/createBatch',  # they promise it's coming soon...
                        'order/detail',
                    ],
                },
                'privateV3': {
                    'get': [
                        'orders',
                        'orders/{id}',
                        'batchorders/{ids}',
                        'trades',
                        'trades/{id}',
                        'withdrawals',
                        'withdrawals/{id}',
                        'deposits',
                        'deposits/{id}',
                        'transfers',
                        'transfers/{id}',
                        'addresses',
                        'withdrawal-fees',
                        'assets',
                        'accounts/me/trading-fees',
                        'accounts/me/withdrawal-limits',
                        'accounts/me/balances',
                        'accounts/me/transactions',
                        'reports/{id}',
                    ],
                    'post': [
                        'orders',
                        'batchorders',
                        'withdrawals',
                        'reports',
                    ],
                    'delete': [
                        'orders',
                        'orders/{id}',
                        'batchorders/{ids}',
                    ],
                    'put': [
                        'orders/{id}',
                    ],
                },
                'web': {
                    'get': [
                        'market/BTCMarkets/{id}/tickByTime',
                    ],
                },
            },
            'timeframes': {
                '1m': 'minute',
                '1h': 'hour',
                '1d': 'day',
            },
            'exceptions': {
                '3': InvalidOrder,
                '6': DDoSProtection,
            },
            'fees': {
                'percentage': True,
                'tierBased': True,
                'maker': -0.05 / 100,
                'taker': 0.20 / 100,
            },
            'options': {
                'fees': {
                    'AUD': {
                        'maker': 0.85 / 100,
                        'taker': 0.85 / 100,
                    },
                },
            },
        })

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            request['since'] = since
        response = self.privateGetFundtransferHistory(self.extend(request, params))
        transactions = response['fundTransfers']
        return self.parse_transactions(transactions, None, since, limit)

    def parse_transaction_status(self, status):
        # todo: find more statuses
        statuses = {
            'Complete': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        #     {
        #         status: 'Complete',
        #         fundTransferId: 1904311906,
        #         description: 'ETH withdraw from [me@email.com] to Address: 0xF123aa44FadEa913a7da99cc2eE202Db684Ce0e3 amount: 8.28965701 fee: 0.00000000',
        #         creationTime: 1529418358525,
        #         currency: 'ETH',
        #         amount: 828965701,
        #         fee: 0,
        #         transferType: 'WITHDRAW',
        #         errorMessage: null,
        #         lastUpdate: 1529418376754,
        #         cryptoPaymentDetail: {
        #             address: '0xF123aa44FadEa913a7da99cc2eE202Db684Ce0e3',
        #             txId: '0x8fe483b6f9523559b9ebffb29624f98e86227d2660d4a1fd4785d45e51c662c2'
        #         }
        #     }
        #
        #     {
        #         status: 'Complete',
        #         fundTransferId: 494077500,
        #         description: 'BITCOIN Deposit, B 0.1000',
        #         creationTime: 1501077601015,
        #         currency: 'BTC',
        #         amount: 10000000,
        #         fee: 0,
        #         transferType: 'DEPOSIT',
        #         errorMessage: null,
        #         lastUpdate: 1501077601133,
        #         cryptoPaymentDetail: null
        #     }
        #
        #     {
        #         "fee": 0,
        #         "amount": 56,
        #         "status": "Complete",
        #         "currency": "BCHABC",
        #         "lastUpdate": 1542339164044,
        #         "description": "BitcoinCashABC Deposit, P 0.00000056",
        #         "creationTime": 1542339164003,
        #         "errorMessage": null,
        #         "transferType": "DEPOSIT",
        #         "fundTransferId": 2527326972,
        #         "cryptoPaymentDetail": null
        #     }
        #
        timestamp = self.safe_integer(transaction, 'creationTime')
        lastUpdate = self.safe_integer(transaction, 'lastUpdate')
        transferType = self.safe_string(transaction, 'transferType')
        cryptoPaymentDetail = self.safe_value(transaction, 'cryptoPaymentDetail', {})
        address = self.safe_string(cryptoPaymentDetail, 'address')
        txid = self.safe_string(cryptoPaymentDetail, 'txId')
        type = None
        if transferType == 'DEPOSIT':
            type = 'deposit'
        elif transferType == 'WITHDRAW':
            type = 'withdrawal'
        else:
            type = transferType
        fee = self.safe_float(transaction, 'fee')
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        ccy = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(ccy)
        # for some currencies the exchange requires the amount to be scaled, like BTC, ETH, BCH
        # values in other currencies may have to be treated "as is", without scaling, like XRP
        # https://github.com/ccxt/ccxt/issues/7413
        amount = self.safe_value(transaction, 'amount')
        if amount is not None:
            if isinstance(amount, basestring):
                amount = self.safe_float(transaction, 'amount')
            else:
                amount = amount / 100000000
        return {
            'id': self.safe_string(transaction, 'fundTransferId'),
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': None,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': lastUpdate,
            'fee': {
                'currency': code,
                'cost': fee,
            },
            'info': transaction,
        }

    def fetch_markets(self, params={}):
        response = self.publicGetV3Markets(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            baseId = self.safe_string(market, 'baseAssetName')
            quoteId = self.safe_string(market, 'quoteAssetName')
            id = self.safe_string(market, 'marketId')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            fees = self.safe_value(self.safe_value(self.options, 'fees', {}), quote, self.fees)
            pricePrecision = self.safe_float(market, 'priceDecimals')
            amountPrecision = self.safe_float(market, 'amountDecimals')
            minAmount = self.safe_float(market, 'minOrderAmount')
            maxAmount = self.safe_float(market, 'maxOrderAmount')
            minPrice = None
            if quote == 'AUD':
                minPrice = math.pow(10, -pricePrecision)
            precision = {
                'amount': amountPrecision,
                'price': pricePrecision,
            }
            limits = {
                'amount': {
                    'min': minAmount,
                    'max': maxAmount,
                },
                'price': {
                    'min': minPrice,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            result.append({
                'info': market,
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': None,
                'maker': fees['maker'],
                'taker': fees['taker'],
                'limits': limits,
                'precision': precision,
            })
        return result

    def fetch_time(self, params={}):
        response = self.publicGetV3Time(params)
        #
        #     {
        #         "timestamp": "2019-09-01T18:34:27.045000Z"
        #     }
        #
        return self.parse8601(self.safe_string(response, 'timestamp'))

    def fetch_balance(self, params={}):
        self.load_markets()
        balances = self.privateGetAccountBalance(params)
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            multiplier = 100000000
            total = self.safe_float(balance, 'balance')
            if total is not None:
                total /= multiplier
            used = self.safe_float(balance, 'pendingFunds')
            if used is not None:
                used /= multiplier
            account = self.account()
            account['used'] = used
            account['total'] = total
            result[code] = account
        return self.parse_balance(result)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     {
        #         "timestamp":1572307200000,
        #         "open":1962218,
        #         "high":1974850,
        #         "low":1962208,
        #         "close":1974850,
        #         "volume":305211315,
        #     }
        #
        multiplier = 100000000  # for price and volume
        keys = ['open', 'high', 'low', 'close', 'volume']
        result = [
            self.safe_integer(ohlcv, 'timestamp'),
        ]
        for i in range(0, len(keys)):
            key = keys[i]
            value = self.safe_float(ohlcv, key)
            if value is not None:
                value = value / multiplier
            result.append(value)
        return result

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
            'timeframe': self.timeframes[timeframe],
            # set to True to see candles more recent than the timestamp in the
            # since parameter, if a since parameter is used, default is False
            'indexForward': True,
            # set to True to see the earliest candles first in the list of
            # returned candles in chronological order, default is False
            'sortForward': True,
        }
        if since is not None:
            request['since'] = since
        if limit is not None:
            request['limit'] = limit  # default is 3000
        response = self.publicGetV2MarketIdTickByTimeTimeframe(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "paging":{
        #             "newer":"/v2/market/ETH/BTC/tickByTime/day?indexForward=true&since=1572307200000",
        #             "older":"/v2/market/ETH/BTC/tickByTime/day?since=1457827200000"
        #         },
        #         "ticks":[
        #             {"timestamp":1572307200000,"open":1962218,"high":1974850,"low":1962208,"close":1974850,"volume":305211315},
        #             {"timestamp":1572220800000,"open":1924700,"high":1951276,"low":1909328,"close":1951276,"volume":1086067595},
        #             {"timestamp":1572134400000,"open":1962155,"high":1962734,"low":1900905,"close":1930243,"volume":790141098},
        #         ],
        #     }
        #
        ticks = self.safe_value(response, 'ticks', [])
        return self.parse_ohlcvs(ticks, market, timeframe, since, limit)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.publicGetMarketIdOrderbook(self.extend(request, params))
        timestamp = self.safe_timestamp(response, 'timestamp')
        return self.parse_order_book(response, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'timestamp')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'bestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'bestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume24h'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.publicGetMarketIdTick(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'tid')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        return {
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            # 'since': 59868345231,
            'id': market['id'],
        }
        response = self.publicGetMarketIdTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        multiplier = 100000000  # for price and volume
        orderSide = 'Bid' if (side == 'buy') else 'Ask'
        request = self.ordered({
            'currency': market['quote'],
        })
        request['currency'] = market['quote']
        request['instrument'] = market['base']
        request['price'] = int(self.decimal_to_precision(price * multiplier, ROUND, 0))
        request['volume'] = int(self.decimal_to_precision(amount * multiplier, ROUND, 0))
        request['orderSide'] = orderSide
        request['ordertype'] = self.capitalize(type)
        request['clientRequestId'] = str(self.nonce())
        response = self.privatePostOrderCreate(self.extend(request, params))
        id = self.safe_string(response, 'id')
        return {
            'info': response,
            'id': id,
        }

    def cancel_orders(self, ids, symbol=None, params={}):
        self.load_markets()
        for i in range(0, len(ids)):
            ids[i] = int(ids[i])
        request = {
            'orderIds': ids,
        }
        return self.privatePostOrderCancel(self.extend(request, params))

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.cancel_orders([id])

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        currency = None
        cost = None
        if market['quote'] == 'AUD':
            currency = market['quote']
            cost = float(self.cost_to_precision(symbol, amount * price))
        else:
            currency = market['base']
            cost = float(self.amount_to_precision(symbol, amount))
        return {
            'type': takerOrMaker,
            'currency': currency,
            'rate': rate,
            'cost': float(self.fee_to_precision(symbol, rate * cost)),
        }

    def parse_my_trade(self, trade, market):
        multiplier = 100000000
        timestamp = self.safe_integer(trade, 'creationTime')
        side = self.safe_float(trade, 'side')
        side = 'buy' if (side == 'Bid') else 'sell'
        # BTCMarkets always charge in AUD for AUD-related transactions.
        feeCurrencyCode = None
        symbol = None
        if market is not None:
            feeCurrencyCode = market['quote'] if (market['quote'] == 'AUD') else market['base']
            symbol = market['symbol']
        id = self.safe_string(trade, 'id')
        price = self.safe_float(trade, 'price')
        if price is not None:
            price /= multiplier
        amount = self.safe_float(trade, 'volume')
        if amount is not None:
            amount /= multiplier
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCost /= multiplier
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        orderId = self.safe_string(trade, 'orderId')
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': orderId,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': {
                'currency': feeCurrencyCode,
                'cost': feeCost,
            },
            'takerOrMaker': None,
        }

    def parse_my_trades(self, trades, market=None, since=None, limit=None):
        result = []
        for i in range(0, len(trades)):
            trade = self.parse_my_trade(trades[i], market)
            result.append(trade)
        return result

    def parse_order(self, order, market=None):
        multiplier = 100000000
        side = 'buy' if (order['orderSide'] == 'Bid') else 'sell'
        type = 'limit' if (order['ordertype'] == 'Limit') else 'market'
        timestamp = self.safe_integer(order, 'creationTime')
        if market is None:
            market = self.market(order['instrument'] + '/' + order['currency'])
        status = 'open'
        if order['status'] == 'Failed' or order['status'] == 'Cancelled' or order['status'] == 'Partially Cancelled' or order['status'] == 'Error':
            status = 'canceled'
        elif order['status'] == 'Fully Matched' or order['status'] == 'Partially Matched':
            status = 'closed'
        price = self.safe_float(order, 'price') / multiplier
        amount = self.safe_float(order, 'volume') / multiplier
        remaining = self.safe_float(order, 'openVolume', 0.0) / multiplier
        filled = amount - remaining
        trades = self.parse_my_trades(order['trades'], market)
        numTrades = len(trades)
        cost = filled * price
        average = None
        lastTradeTimestamp = None
        if numTrades > 0:
            cost = 0
            for i in range(0, numTrades):
                trade = trades[i]
                cost = self.sum(cost, trade['cost'])
            if filled > 0:
                average = cost / filled
            lastTradeTimestamp = trades[numTrades - 1]['timestamp']
        id = self.safe_string(order, 'id')
        clientOrderId = self.safe_string(order, 'clientRequestId')
        return {
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': market['symbol'],
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'average': average,
            'status': status,
            'trades': trades,
            'fee': None,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        ids = [int(id)]
        request = {
            'orderIds': ids,
        }
        response = self.privatePostOrderDetail(self.extend(request, params))
        numOrders = len(response['orders'])
        if numOrders < 1:
            raise OrderNotFound(self.id + ' No matching order found: ' + id)
        order = response['orders'][0]
        return self.parse_order(order)

    def create_paginated_request(self, market, since=None, limit=None):
        limit = 100 if (limit is None) else limit
        since = 0 if (since is None) else since
        request = self.ordered({
            'currency': market['quoteId'],
            'instrument': market['baseId'],
            'limit': limit,
            'since': since,
        })
        return request

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ': fetchOrders requires a `symbol` argument.')
        self.load_markets()
        market = self.market(symbol)
        request = self.create_paginated_request(market, since, limit)
        response = self.privatePostOrderHistory(self.extend(request, params))
        return self.parse_orders(response['orders'], market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ': fetchOpenOrders requires a `symbol` argument.')
        self.load_markets()
        market = self.market(symbol)
        request = self.create_paginated_request(market, since, limit)
        response = self.privatePostOrderOpen(self.extend(request, params))
        return self.parse_orders(response['orders'], market)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ': fetchMyTrades requires a `symbol` argument.')
        self.load_markets()
        market = self.market(symbol)
        request = self.create_paginated_request(market, since, limit)
        response = self.privatePostOrderTradeHistory(self.extend(request, params))
        return self.parse_my_trades(response['trades'], market)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        uri = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + uri
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = None
            headers = {
                'apikey': self.apiKey,
                'timestamp': nonce,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/json'
                auth = uri + "\n" + nonce + "\n"  # eslint-disable-line quotes
                body = self.json(params)
                auth += body
            else:
                query = self.keysort(self.omit(params, self.extract_params(path)))
                queryString = ''
                if query:
                    queryString = self.urlencode(query)
                    url += '?' + queryString
                    queryString += "\n"  # eslint-disable-line quotes
                auth = uri + "\n" + queryString + nonce + "\n"  # eslint-disable-line quotes
            secret = base64.b64decode(self.secret)
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
            headers['signature'] = self.decode(signature)
        elif api == 'privateV3':
            self.check_required_credentials()
            nonce = str(self.nonce())
            secret = base64.b64decode(self.secret)  # or stringToBase64
            pathWithLeadingSlash = '/v3/' + path
            auth = method + pathWithLeadingSlash + nonce
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
            if method == 'GET':
                if params:
                    url += '?' + self.urlencode(params)
            else:
                body = self.json(params)
            headers = {
                'Accept': 'application/json',
                'Accept-Charset': 'UTF-8',
                'Content-Type': 'application/json',
                'BM-AUTH-APIKEY': self.apiKey,
                'BM-AUTH-TIMESTAMP': nonce,
                'BM-AUTH-SIGNATURE': signature,
            }
        else:
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if 'success' in response:
            if not response['success']:
                error = self.safe_string(response, 'errorCode')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, error, feedback)
                raise ExchangeError(feedback)
