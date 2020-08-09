# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection


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
                'InsufficientFund': InsufficientFunds,
                'InvalidPrice': InvalidOrder,
                'InvalidAmount': InvalidOrder,
                'MissingArgument': InvalidOrder,
                'OrderAlreadyCancelled': InvalidOrder,
                'OrderNotFound': OrderNotFound,
                'OrderStatusIsFinal': InvalidOrder,
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

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            request['after'] = since
        response = await self.privateV3GetTransfers(self.extend(request, params))
        return self.parse_transactions(response, None, since, limit)

    def parse_transaction_status(self, status):
        # todo: find more statuses
        statuses = {
            'Complete': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction_type(self, type):
        statuses = {
            'Withdraw': 'withdrawal',
            'Deposit': 'deposit',
        }
        return self.safe_string(statuses, type, type)

    def parse_transaction(self, transaction, currency=None):
        #    {
        #         "id": "6500230339",
        #         "assetName": "XRP",
        #         "amount": "500",
        #         "type": "Deposit",
        #         "creationTime": "2020-07-27T07:52:08.640000Z",
        #         "status": "Complete",
        #         "description": "RIPPLE Deposit, XRP 500",
        #         "fee": "0",
        #         "lastUpdate": "2020-07-27T07:52:08.665000Z",
        #         "paymentDetail": {
        #             "txId": "lsjflsjdfljsd",
        #             "address": "kjasfkjsdf?dt=873874545"
        #         }
        #    }
        #
        #    {
        #         "id": "500985282",
        #         "assetName": "BTC",
        #         "amount": "0.42570126",
        #         "type": "Withdraw",
        #         "creationTime": "2017-07-29T12:49:03.931000Z",
        #         "status": "Complete",
        #         "description": "BTC withdraw from [nick-btcmarkets@snowmonkey.co.uk] to Address: 1B9DsnSYQ54VMqFHVJYdGoLMCYzFwrQzsj amount: 0.42570126 fee: 0.00000000",
        #         "fee": "0.0005",
        #         "lastUpdate": "2017-07-29T12:52:20.676000Z",
        #         "paymentDetail": {
        #             "txId": "fkjdsfjsfljsdfl",
        #             "address": "a;daddjas;djas"
        #         }
        #    }
        #
        #    {
        #         "id": "505102262",
        #         "assetName": "XRP",
        #         "amount": "979.836",
        #         "type": "Deposit",
        #         "creationTime": "2017-07-31T08:50:01.053000Z",
        #         "status": "Complete",
        #         "description": "Ripple Deposit, X 979.8360",
        #         "fee": "0",
        #         "lastUpdate": "2017-07-31T08:50:01.290000Z"
        #     }
        timestamp = self.parse8601(self.safe_string(transaction, 'creationTime'))
        lastUpdate = self.parse8601(self.safe_string(transaction, 'lastUpdate'))
        transferType = self.parse_transaction_type(self.safe_string(transaction, 'type'))
        cryptoPaymentDetail = self.safe_value(transaction, 'paymentDetail', {})
        txid = self.safe_string(cryptoPaymentDetail, 'txId')
        address = self.safe_string(cryptoPaymentDetail, 'address')
        tag = None
        if address is not None:
            addressParts = address.split('?dt=')
            numParts = len(addressParts)
            if numParts > 1:
                address = addressParts[0]
                tag = addressParts[1]
        type = None
        if transferType == 'DEPOSIT':
            type = 'deposit'
        elif transferType == 'WITHDRAW':
            type = 'withdrawal'
        else:
            type = transferType
        fee = self.safe_float(transaction, 'fee')
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        ccy = self.safe_string(transaction, 'assetName')
        code = self.safe_currency_code(ccy)
        # todo: self logic is duplicated below
        amount = self.safe_float(transaction, 'amount')
        return {
            'id': self.safe_string(transaction, 'id'),
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,
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

    async def fetch_markets(self, params={}):
        response = await self.publicGetV3Markets(params)
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

    async def fetch_time(self, params={}):
        response = await self.publicGetV3Time(params)
        #
        #     {
        #         "timestamp": "2019-09-01T18:34:27.045000Z"
        #     }
        #
        return self.parse8601(self.safe_string(response, 'timestamp'))

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateV3GetAccountsMeBalances(params)
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'assetName')
            code = self.safe_currency_code(currencyId)
            total = self.safe_float(balance, 'balance')
            used = self.safe_float(balance, 'locked')
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

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
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
        response = await self.publicGetV2MarketIdTickByTimeTimeframe(self.extend(request, params))
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

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = await self.publicGetMarketIdOrderbook(self.extend(request, params))
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

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = await self.publicGetMarketIdTick(self.extend(request, params))
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

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            # 'since': 59868345231,
            'id': market['id'],
        }
        response = await self.publicGetMarketIdTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = self.ordered({
            'marketId': market['id'],
            'amount': self.price_to_precision(symbol, amount),
            'side': 'Bid' if (side == 'buy') else 'Ask',
            'clientOrderId': self.safe_value(params, 'clientOrderId'),
        })
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
            request['type'] = 'Limit'
        else:
            request['type'] = 'Market'
        # todo: add support for "Stop Limit" "Stop" "Take Profit" order types
        response = await self.privateV3PostOrders(self.extend(request, params))
        id = self.safe_string(response, 'orderId')
        return {
            'info': response,
            'id': id,
        }

    async def cancel_orders(self, ids, symbol=None, params={}):
        await self.load_markets()
        for i in range(0, len(ids)):
            ids[i] = int(ids[i])
        request = {
            'ids': ids,
        }
        return await self.privateV3DeleteBatchordersIds(self.extend(request, params))

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        return await self.privateV3DeleteOrdersId(self.extend(request, params))

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
        timestamp = self.parse8601(self.safe_string(trade, 'timestamp'))
        side = None
        if self.safe_string(trade, 'side') == 'Bid':
            side = 'buy'
        else:
            side = 'sell'
        marketId = self.safe_string(trade, 'marketId')
        symbol = self.lookup_symbol_from_market_id(marketId)
        market = self.market(symbol)
        # BTCMarkets always charge in AUD for AUD-related transactions.
        feeCurrencyCode = None
        if market is None:
            # happens for some markets like BCH-BTC
            baseId, quoteId = marketId.split('-')
            if quoteId == 'AUD':
                feeCurrencyCode = self.safe_currency_code(quoteId)
            else:
                feeCurrencyCode = self.safe_currency_code(baseId)
        else:
            if market['quote'] == 'AUD':
                feeCurrencyCode = market['quote']
            else:
                feeCurrencyCode = market['base']
        id = self.safe_string(trade, 'id')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        feeCost = self.safe_float(trade, 'fee')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        orderId = self.safe_string(trade, 'orderId')
        type = None
        if price is None:
            type = 'market'
        else:
            type = 'limit'
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': orderId,
            'symbol': symbol,
            'type': type,
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

    def parse_order_status(self, status):
        statuses = {
            'Accepted': 'open',
            'Placed': 'open',
            'Partially Matched': 'open',
            'Fully Matched': 'closed',
            'Cancelled': 'canceled',
            'Partially Cancelled': 'canceled',
            'Failed': 'rejected',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(self.safe_string(order, 'creationTime'))
        marketId = self.safe_string(order, 'marketId')
        symbol = self.lookup_symbol_from_market_id(marketId)
        side = None
        if self.safe_string(order, 'side') == 'Bid':
            side = 'buy'
        else:
            side = 'sell'
        type = self.safe_string_lower(order, 'type')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        remaining = self.safe_float(order, 'openAmount')
        filled = amount - remaining
        status = self.parse_order_status(self.safe_string(order, 'status'))
        cost = None
        if price is not None:
            if filled is not None:
                cost = price * filled
        return {
            'info': order,
            'id': self.safe_string(order, 'orderId'),
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'average': None,
            'status': status,
            'trades': None,
            'fee': None,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privateV3GetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'status': 'all',
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketId'] = market['id']
        if since is not None:
            request['after'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.privateV3GetOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'open'}
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketId'] = market['id']
        if since is not None:
            request['after'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.privateV3GetTrades(self.extend(request, params))
        return self.parse_my_trades(response, market, since, limit)

    def lookup_symbol_from_market_id(self, marketId):
        market = None
        symbol = None
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        return symbol

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
            pathWithLeadingSlash = '/v3' + uri
            if method != 'GET':
                body = self.json(params)
            else:
                query = self.keysort(self.omit(params, self.extract_params(path)))
                queryString = ''
                if query:
                    queryString = self.urlencode(query)
                    url += '?' + queryString
            auth = None
            if body:
                auth = method + pathWithLeadingSlash + nonce + body
            else:
                auth = method + pathWithLeadingSlash + nonce
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
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
        # v3 api errors
        if code >= 400:
            errorCode = self.safe_string(response, 'code')
            message = self.safe_string(response, 'message')
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
            self.throw_exactly_matched_exception(self.exceptions, message, feedback)
            raise ExchangeError(feedback)
