# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.base.types import Balances, Int, Order, OrderBook, Str, Trade
from ccxt.async_support.base.ws.client import Client
from typing import List
from ccxt.base.errors import BadRequest
from ccxt.base.errors import NetworkError
from ccxt.base.precise import Precise


class bingx(ccxt.async_support.bingx):

    def describe(self):
        return self.deep_extend(super(bingx, self).describe(), {
            'has': {
                'ws': True,
                'watchTrades': True,
                'watchOrderBook': True,
                'watchOHLCV': True,
                'watchOrders': True,
                'watchMyTrades': True,
                'watchTicker': False,
                'watchTickers': False,
                'watchBalance': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'spot': 'wss://open-api-ws.bingx.com/market',
                        'swap': 'wss://open-api-swap.bingx.com/swap-market',
                    },
                },
            },
            'options': {
                'ws': {
                    'gunzip': True,
                },
                'swap': {
                    'timeframes': {
                        '1m': '1m',
                        '3m': '3m',
                        '5m': '5m',
                        '15m': '15m',
                        '30m': '30m',
                        '1h': '1h',
                        '2h': '2h',
                        '4h': '4h',
                        '6h': '6h',
                        '12h': '12h',
                        '1d': '1d',
                        '3d': '3d',
                        '1w': '1w',
                        '1M': '1M',
                    },
                },
                'spot': {
                    'timeframes': {
                        '1m': '1min',
                        '5m': '5min',
                        '15m': '15min',
                        '30m': '30min',
                        '1h': '60min',
                        '1d': '1day',
                    },
                },
                'watchBalance': {
                    'fetchBalanceSnapshot': True,  # needed to be True to keep track of used and free balance
                    'awaitBalanceSnapshot': False,  # whether to wait for the balance snapshot before providing updates
                },
            },
            'streaming': {
                'keepAlive': 1800000,  # 30 minutes
            },
        })

    async def watch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        watches information on multiple trades made in a market
        :see: https://bingx-api.github.io/docs/#/spot/socket/market.html#Subscribe%20to%20tick-by-tick
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/market.html#Subscribe%20the%20Latest%20Trade%20Detail
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of [order structures]{@link https://docs.ccxt.com/#/?id=order-structure
        """
        await self.load_markets()
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('watchTrades', market, params)
        url = self.safe_value(self.urls['api']['ws'], marketType)
        if url is None:
            raise BadRequest(self.id + ' watchTrades is not supported for ' + marketType + ' markets.')
        messageHash = market['id'] + '@trade'
        uuid = self.uuid()
        request = {
            'id': uuid,
            'dataType': messageHash,
        }
        if marketType == 'swap':
            request['reqType'] = 'sub'
        trades = await self.watch(url, messageHash, self.extend(request, query), messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client: Client, message):
        #
        # spot
        # first snapshot
        #
        #    {
        #      "id": "d83b78ce-98be-4dc2-b847-12fe471b5bc5",
        #      "code": 0,
        #      "msg": "SUCCESS",
        #      "timestamp": 1690214699854
        #    }
        #
        # subsequent updates
        #
        #     {
        #         "code": 0,
        #         "data": {
        #           "E": 1690214529432,
        #           "T": 1690214529386,
        #           "e": "trade",
        #           "m": True,
        #           "p": "29110.19",
        #           "q": "0.1868",
        #           "s": "BTC-USDT",
        #           "t": "57903921"
        #         },
        #         "dataType": "BTC-USDT@trade",
        #         "success": True
        #     }
        #
        #
        # swap
        # first snapshot
        #
        #    {
        #        "id": "2aed93b1-6e1e-4038-aeba-f5eeaec2ca48",
        #        "code": 0,
        #        "msg": '',
        #        "dataType": '',
        #        "data": null
        #    }
        #
        # subsequent updates
        #
        #
        #    {
        #        "code": 0,
        #        "dataType": "BTC-USDT@trade",
        #        "data": [
        #            {
        #                "q": "0.0421",
        #                "p": "29023.5",
        #                "T": 1690221401344,
        #                "m": False,
        #                "s": "BTC-USDT"
        #            },
        #            ...
        #        ]
        #    }
        #
        data = self.safe_value(message, 'data', [])
        messageHash = self.safe_string(message, 'dataType')
        marketId = messageHash.split('@')[0]
        isSwap = client.url.find('swap') >= 0
        marketType = 'swap' if isSwap else 'spot'
        market = self.safe_market(marketId, None, None, marketType)
        symbol = market['symbol']
        trades = None
        if isinstance(data, list):
            trades = self.parse_trades(data, market)
        else:
            trades = [self.parse_trade(data, market)]
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        for j in range(0, len(trades)):
            stored.append(trades[j])
        client.resolve(stored, messageHash)

    async def watch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://bingx-api.github.io/docs/#/spot/socket/market.html#Subscribe%20Market%20Depth%20Data
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/market.html#Subscribe%20Market%20Depth%20Data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('watchOrderBook', market, params)
        if limit is None:
            limit = 100
        else:
            if marketType == 'swap':
                if (limit != 5) and (limit != 10) and (limit != 20) and (limit != 50) and (limit != 100):
                    raise BadRequest(self.id + ' watchOrderBook()(swap) only supports limit 5, 10, 20, 50, and 100')
            elif marketType == 'spot':
                if (limit != 20) and (limit != 100):
                    raise BadRequest(self.id + ' watchOrderBook()(spot) only supports limit 20, and 100')
        url = self.safe_value(self.urls['api']['ws'], marketType)
        if url is None:
            raise BadRequest(self.id + ' watchOrderBook is not supported for ' + marketType + ' markets.')
        messageHash = market['id'] + '@depth' + str(limit)
        uuid = self.uuid()
        request = {
            'id': uuid,
            'dataType': messageHash,
        }
        if marketType == 'swap':
            request['reqType'] = 'sub'
        orderbook = await self.watch(url, messageHash, self.deep_extend(request, query), messageHash)
        return orderbook.limit()

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_order_book(self, client: Client, message):
        #
        # spot
        #
        #
        #    {
        #        "code": 0,
        #        "dataType": "BTC-USDT@depth20",
        #        "data": {
        #          "bids": [
        #            ['28852.9', "34.2621"],
        #            ...
        #          ],
        #          "asks": [
        #            ['28864.9', "23.4079"],
        #            ...
        #          ]
        #        },
        #        "dataType": "BTC-USDT@depth20",
        #        "success": True
        #    }
        #
        # swap
        #
        #
        #    {
        #        "code": 0,
        #        "dataType": "BTC-USDT@depth20",
        #        "data": {
        #          "bids": [
        #            ['28852.9', "34.2621"],
        #            ...
        #          ],
        #          "asks": [
        #            ['28864.9', "23.4079"],
        #            ...
        #          ]
        #        }
        #    }
        #
        data = self.safe_value(message, 'data', [])
        messageHash = self.safe_string(message, 'dataType')
        marketId = messageHash.split('@')[0]
        isSwap = client.url.find('swap') >= 0
        marketType = 'swap' if isSwap else 'spot'
        market = self.safe_market(marketId, None, None, marketType)
        symbol = market['symbol']
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            orderbook = self.order_book()
        snapshot = self.parse_order_book(data, symbol, None, 'bids', 'asks', 0, 1)
        orderbook.reset(snapshot)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def parse_ws_ohlcv(self, ohlcv, market=None) -> list:
        #
        #    {
        #        "c": "28909.0",
        #        "o": "28915.4",
        #        "h": "28915.4",
        #        "l": "28896.1",
        #        "v": "27.6919",
        #        "T": 1696687499999,
        #        "t": 1696687440000
        #    }
        #
        # for spot, opening-time(t) is used instead of closing-time(T), to be compatible with fetchOHLCV
        # for swap,(T) is the opening time
        timestamp = 't' if (market['spot']) else 'T'
        return [
            self.safe_integer(ohlcv, timestamp),
            self.safe_number(ohlcv, 'o'),
            self.safe_number(ohlcv, 'h'),
            self.safe_number(ohlcv, 'l'),
            self.safe_number(ohlcv, 'c'),
            self.safe_number(ohlcv, 'v'),
        ]

    def handle_ohlcv(self, client: Client, message):
        #
        # spot
        #
        #   {
        #       "code": 0,
        #       "data": {
        #         "E": 1696687498608,
        #         "K": {
        #           "T": 1696687499999,
        #           "c": "27917.829",
        #           "h": "27918.427",
        #           "i": "1min",
        #           "l": "27917.7",
        #           "n": 262,
        #           "o": "27917.91",
        #           "q": "25715.359197",
        #           "s": "BTC-USDT",
        #           "t": 1696687440000,
        #           "v": "0.921100"
        #         },
        #         "e": "kline",
        #         "s": "BTC-USDT"
        #       },
        #       "dataType": "BTC-USDT@kline_1min",
        #       "success": True
        #   }
        #
        # swap
        #    {
        #        "code": 0,
        #        "dataType": "BTC-USDT@kline_1m",
        #        "s": "BTC-USDT",
        #        "data": [
        #            {
        #            "c": "28909.0",
        #            "o": "28915.4",
        #            "h": "28915.4",
        #            "l": "28896.1",
        #            "v": "27.6919",
        #            "T": 1690907580000
        #            }
        #        ]
        #    }
        #
        data = self.safe_value(message, 'data', [])
        candles = None
        if isinstance(data, list):
            candles = data
        else:
            candles = [self.safe_value(data, 'K', [])]
        messageHash = self.safe_string(message, 'dataType')
        timeframeId = messageHash.split('_')[1]
        marketId = messageHash.split('@')[0]
        isSwap = client.url.find('swap') >= 0
        marketType = 'swap' if isSwap else 'spot'
        market = self.safe_market(marketId, None, None, marketType)
        symbol = market['symbol']
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframeId)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframeId] = stored
        for i in range(0, len(candles)):
            candle = candles[i]
            parsed = self.parse_ws_ohlcv(candle, market)
            stored.append(parsed)
        client.resolve(stored, messageHash)

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Int = None, limit: Int = None, params={}) -> List[list]:
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :see: https://bingx-api.github.io/docs/#/spot/socket/market.html#K%E7%BA%BF%20Streams
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/market.html#Subscribe%20K-Line%20Data
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('watchOHLCV', market, params)
        url = self.safe_value(self.urls['api']['ws'], marketType)
        if url is None:
            raise BadRequest(self.id + ' watchOHLCV is not supported for ' + marketType + ' markets.')
        options = self.safe_value(self.options, marketType, {})
        timeframes = self.safe_value(options, 'timeframes', {})
        interval = self.safe_string(timeframes, timeframe, timeframe)
        messageHash = market['id'] + '@kline_' + interval
        uuid = self.uuid()
        request = {
            'id': uuid,
            'dataType': messageHash,
        }
        if marketType == 'swap':
            request['reqType'] = 'sub'
        ohlcv = await self.watch(url, messageHash, self.extend(request, query), messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    async def watch_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        :see: https://bingx-api.github.io/docs/#/spot/socket/account.html#Subscription%20order%20update%20data
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/account.html#Account%20balance%20and%20position%20update%20push
        watches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        await self.authenticate()
        type = None
        market = None
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        type, params = self.handle_market_type_and_params('watchOrders', market, params)
        isSpot = (type == 'spot')
        spotHash = 'spot:private'
        swapHash = 'swap:private'
        subscriptionHash = spotHash if isSpot else swapHash
        spotMessageHash = 'spot:order'
        swapMessageHash = 'swap:order'
        messageHash = spotMessageHash if isSpot else swapMessageHash
        if market is not None:
            messageHash += ':' + symbol
        url = self.urls['api']['ws'][type] + '?listenKey=' + self.options['listenKey']
        request = None
        uuid = self.uuid()
        if isSpot:
            request = {
                'id': uuid,
                'dataType': 'spot.executionReport',
            }
        orders = await self.watch(url, messageHash, request, subscriptionHash)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    async def watch_my_trades(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        :see: https://bingx-api.github.io/docs/#/spot/socket/account.html#Subscription%20order%20update%20data
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/account.html#Account%20balance%20and%20position%20update%20push
        watches information on multiple trades made by the user
        :param str symbol: unified market symbol of the market trades were made in
        :param int [since]: the earliest time in ms to trades orders for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of [trade structures]{@link https://docs.ccxt.com/#/?id=trade-structure
        """
        await self.load_markets()
        await self.authenticate()
        type = None
        market = None
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        type, params = self.handle_market_type_and_params('watchOrders', market, params)
        isSpot = (type == 'spot')
        spotSubHash = 'spot:private'
        swapSubHash = 'swap:private'
        subscriptionHash = spotSubHash if isSpot else swapSubHash
        spotMessageHash = 'spot:mytrades'
        swapMessageHash = 'swap:mytrades'
        messageHash = spotMessageHash if isSpot else swapMessageHash
        if market is not None:
            messageHash += ':' + symbol
        url = self.urls['api']['ws'][type] + '?listenKey=' + self.options['listenKey']
        request = None
        uuid = self.uuid()
        if isSpot:
            request = {
                'id': uuid,
                'dataType': 'spot.executionReport',
            }
        trades = await self.watch(url, messageHash, request, subscriptionHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    async def watch_balance(self, params={}) -> Balances:
        """
        :see: https://bingx-api.github.io/docs/#/spot/socket/account.html#Subscription%20order%20update%20data
        :see: https://bingx-api.github.io/docs/#/swapV2/socket/account.html#Account%20balance%20and%20position%20update%20push
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/#/?id=balance-structure>`
        """
        await self.load_markets()
        await self.authenticate()
        type = None
        type, params = self.handle_market_type_and_params('watchBalance', None, params)
        isSpot = (type == 'spot')
        spotSubHash = 'spot:balance'
        swapSubHash = 'swap:private'
        spotMessageHash = 'spot:balance'
        swapMessageHash = 'swap:balance'
        messageHash = spotMessageHash if isSpot else swapMessageHash
        subscriptionHash = spotSubHash if isSpot else swapSubHash
        url = self.urls['api']['ws'][type] + '?listenKey=' + self.options['listenKey']
        request = None
        uuid = self.uuid()
        if type == 'spot':
            request = {
                'id': uuid,
                'dataType': 'ACCOUNT_UPDATE',
            }
        client = self.client(url)
        self.set_balance_cache(client, type, subscriptionHash, params)
        fetchBalanceSnapshot = None
        awaitBalanceSnapshot = None
        fetchBalanceSnapshot, params = self.handle_option_and_params(params, 'watchBalance', 'fetchBalanceSnapshot', True)
        awaitBalanceSnapshot, params = self.handle_option_and_params(params, 'watchBalance', 'awaitBalanceSnapshot', False)
        if fetchBalanceSnapshot and awaitBalanceSnapshot:
            await client.future(type + ':fetchBalanceSnapshot')
        return await self.watch(url, messageHash, request, subscriptionHash)

    def set_balance_cache(self, client: Client, type, subscriptionHash, params):
        if subscriptionHash in client.subscriptions:
            return None
        fetchBalanceSnapshot = self.handle_option_and_params(params, 'watchBalance', 'fetchBalanceSnapshot', True)
        if fetchBalanceSnapshot:
            messageHash = type + ':fetchBalanceSnapshot'
            if not (messageHash in client.futures):
                client.future(messageHash)
                self.spawn(self.load_balance_snapshot, client, messageHash, type)
        else:
            self.balance[type] = {}

    async def load_balance_snapshot(self, client, messageHash, type):
        response = await self.fetch_balance({'type': type})
        self.balance[type] = self.extend(response, self.safe_value(self.balance, type, {}))
        # don't remove the future from the .futures cache
        future = client.futures[messageHash]
        future.resolve()
        client.resolve(self.balance[type], type + ':balance')

    def handle_error_message(self, client, message):
        #
        # {code: 100400, msg: '', timestamp: 1696245808833}
        #
        # {
        #     "code": 100500,
        #     "id": "9cd37d32-da98-440b-bd04-37e7dbcf51ad",
        #     "msg": '',
        #     "timestamp": 1696245842307
        # }
        code = self.safe_string(message, 'code')
        try:
            if code is not None:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
        except Exception as e:
            client.reject(e)
        return True

    async def authenticate(self, params={}):
        time = self.milliseconds()
        listenKey = self.safe_string(self.options, 'listenKey')
        if listenKey is None:
            response = await self.userAuthPrivatePostUserDataStream()
            self.options['listenKey'] = self.safe_string(response, 'listenKey')
            self.options['lastAuthenticatedTime'] = time
            return
        lastAuthenticatedTime = self.safe_integer(self.options, 'lastAuthenticatedTime', 0)
        listenKeyRefreshRate = self.safe_integer(self.options, 'listenKeyRefreshRate', 3600000)  # 1 hour
        if time - lastAuthenticatedTime > listenKeyRefreshRate:
            response = await self.userAuthPrivatePostUserDataStream({'listenKey': listenKey})  # self.extend the expiry
            self.options['listenKey'] = self.safe_string(response, 'listenKey')
            self.options['lastAuthenticatedTime'] = time

    async def pong(self, client, message):
        #
        # spot
        # {
        #     "ping": "5963ba3db76049b2870f9a686b2ebaac",
        #     "time": "2023-10-02T18:51:55.089+0800"
        # }
        # swap
        # Ping
        #
        try:
            if message == 'Ping':
                await client.send('Pong')
            else:
                ping = self.safe_string(message, 'ping')
                time = self.safe_string(message, 'time')
                await client.send({
                    'pong': ping,
                    'time': time,
                })
        except Exception as e:
            error = NetworkError(self.id + ' pong failed with error ' + self.json(e))
            client.reset(error)

    def handle_order(self, client, message):
        #
        #     {
        #         "code": 0,
        #         "dataType": "spot.executionReport",
        #         "data": {
        #            "e": "executionReport",
        #            "E": 1694680212947,
        #            "s": "LTC-USDT",
        #            "S": "BUY",
        #            "o": "LIMIT",
        #            "q": 0.1,
        #            "p": 50,
        #            "x": "NEW",
        #            "X": "PENDING",
        #            "i": 1702238305204043800,
        #            "l": 0,
        #            "z": 0,
        #            "L": 0,
        #            "n": 0,
        #            "N": "",
        #            "T": 0,
        #            "t": 0,
        #            "O": 1694680212676,
        #            "Z": 0,
        #            "Y": 0,
        #            "Q": 0,
        #            "m": False
        #         }
        #      }
        #
        #      {
        #         "code": 0,
        #         "dataType": "spot.executionReport",
        #         "data": {
        #           "e": "executionReport",
        #           "E": 1694681809302,
        #           "s": "LTC-USDT",
        #           "S": "BUY",
        #           "o": "MARKET",
        #           "q": 0,
        #           "p": 62.29,
        #           "x": "TRADE",
        #           "X": "FILLED",
        #           "i": "1702245001712369664",
        #           "l": 0.0802,
        #           "z": 0.0802,
        #           "L": 62.308,
        #           "n": -0.0000802,
        #           "N": "LTC",
        #           "T": 1694681809256,
        #           "t": 38259147,
        #           "O": 1694681809248,
        #           "Z": 4.9971016,
        #           "Y": 4.9971016,
        #           "Q": 5,
        #           "m": False
        #         }
        #       }
        # swap
        #    {
        #        "e": "ORDER_TRADE_UPDATE",
        #        "E": 1696843635475,
        #        "o": {
        #           "s": "LTC-USDT",
        #           "c": "",
        #           "i": "1711312357852147712",
        #           "S": "BUY",
        #           "o": "MARKET",
        #           "q": "0.10000000",
        #           "p": "64.35010000",
        #           "ap": "64.36000000",
        #           "x": "TRADE",
        #           "X": "FILLED",
        #           "N": "USDT",
        #           "n": "-0.00321800",
        #           "T": 0,
        #           "wt": "MARK_PRICE",
        #           "ps": "LONG",
        #           "rp": "0.00000000",
        #           "z": "0.10000000"
        #        }
        #    }
        #
        isSpot = ('dataType' in message)
        data = self.safe_value_2(message, 'data', 'o', {})
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        stored = self.orders
        parsedOrder = self.parse_order(data)
        stored.append(parsedOrder)
        symbol = parsedOrder['symbol']
        spotHash = 'spot:order'
        swapHash = 'swap:order'
        messageHash = spotHash if (isSpot) else swapHash
        client.resolve(stored, messageHash)
        client.resolve(stored, messageHash + ':' + symbol)

    def handle_my_trades(self, client: Client, message):
        #
        #
        #      {
        #         "code": 0,
        #         "dataType": "spot.executionReport",
        #         "data": {
        #           "e": "executionReport",
        #           "E": 1694681809302,
        #           "s": "LTC-USDT",
        #           "S": "BUY",
        #           "o": "MARKET",
        #           "q": 0,
        #           "p": 62.29,
        #           "x": "TRADE",
        #           "X": "FILLED",
        #           "i": "1702245001712369664",
        #           "l": 0.0802,
        #           "z": 0.0802,
        #           "L": 62.308,
        #           "n": -0.0000802,
        #           "N": "LTC",
        #           "T": 1694681809256,
        #           "t": 38259147,
        #           "O": 1694681809248,
        #           "Z": 4.9971016,
        #           "Y": 4.9971016,
        #           "Q": 5,
        #           "m": False
        #         }
        #       }
        #
        #  swap
        #    {
        #        "e": "ORDER_TRADE_UPDATE",
        #        "E": 1696843635475,
        #        "o": {
        #           "s": "LTC-USDT",
        #           "c": "",
        #           "i": "1711312357852147712",
        #           "S": "BUY",
        #           "o": "MARKET",
        #           "q": "0.10000000",
        #           "p": "64.35010000",
        #           "ap": "64.36000000",
        #           "x": "TRADE",
        #           "X": "FILLED",
        #           "N": "USDT",
        #           "n": "-0.00321800",
        #           "T": 0,
        #           "wt": "MARK_PRICE",
        #           "ps": "LONG",
        #           "rp": "0.00000000",
        #           "z": "0.10000000"
        #        }
        #    }
        #
        isSpot = ('dataType' in message)
        result = self.safe_value_2(message, 'data', 'o', {})
        cachedTrades = self.myTrades
        if cachedTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            cachedTrades = ArrayCacheBySymbolById(limit)
            self.myTrades = cachedTrades
        parsed = self.parse_trade(result)
        symbol = parsed['symbol']
        spotHash = 'spot:mytrades'
        swapHash = 'swap:mytrades'
        messageHash = spotHash if isSpot else swapHash
        cachedTrades.append(parsed)
        client.resolve(cachedTrades, messageHash)
        client.resolve(cachedTrades, messageHash + ':' + symbol)

    def handle_balance(self, client: Client, message):
        # spot
        #     {
        #         "e":"ACCOUNT_UPDATE",
        #         "E":1696242817000,
        #         "T":1696242817142,
        #         "a":{
        #            "B":[
        #               {
        #                  "a":"USDT",
        #                  "bc":"-1.00000000000000000000",
        #                  "cw":"86.59497382000000050000",
        #                  "wb":"86.59497382000000050000"
        #               }
        #            ],
        #            "m":"ASSET_TRANSFER"
        #         }
        #     }
        # swap
        #     {
        #         "e":"ACCOUNT_UPDATE",
        #         "E":1696244249320,
        #         "a":{
        #            "m":"WITHDRAW",
        #            "B":[
        #               {
        #                  "a":"USDT",
        #                  "wb":"49.81083984",
        #                  "cw":"49.81083984",
        #                  "bc":"-1.00000000"
        #               }
        #            ],
        #            "P":[
        #            ]
        #         }
        #     }
        #
        a = self.safe_value(message, 'a', {})
        data = self.safe_value(a, 'B', [])
        timestamp = self.safe_integer_2(message, 'T', 'E')
        type = 'swap' if ('P' in a) else 'spot'
        self.balance[type]['info'] = data
        self.balance[type]['timestamp'] = timestamp
        self.balance[type]['datetime'] = self.iso8601(timestamp)
        for i in range(0, len(data)):
            balance = data[i]
            currencyId = self.safe_string(balance, 'a')
            code = self.safe_currency_code(currencyId)
            account = self.balance[type][code] if (code in self.balance[type]) else self.account()
            account['free'] = self.safe_string(balance, 'wb')
            balanceChange = self.safe_string(balance, 'bc')
            if account['used'] is not None:
                account['used'] = Precise.string_sub(self.safe_string(account, 'used'), balanceChange)
            self.balance[type][code] = account
        self.balance[type] = self.safe_balance(self.balance[type])
        client.resolve(self.balance[type], type + ':balance')

    def handle_message(self, client: Client, message):
        if not self.handle_error_message(client, message):
            return
        # public subscriptions
        if (message == 'Ping') or ('ping' in message):
            self.spawn(self.pong, client, message)
            return
        dataType = self.safe_string(message, 'dataType', '')
        if dataType.find('@depth') >= 0:
            self.handle_order_book(client, message)
            return
        if dataType.find('@trade') >= 0:
            self.handle_trades(client, message)
            return
        if dataType.find('@kline') >= 0:
            self.handle_ohlcv(client, message)
            return
        if dataType.find('executionReport') >= 0:
            data = self.safe_value(message, 'data', {})
            type = self.safe_string(data, 'x')
            if type == 'TRADE':
                self.handle_my_trades(client, message)
            self.handle_order(client, message)
            return
        e = self.safe_string(message, 'e')
        if e == 'ACCOUNT_UPDATE':
            self.handle_balance(client, message)
        if e == 'ORDER_TRADE_UPDATE':
            self.handle_order(client, message)
            data = self.safe_value(message, 'o', {})
            type = self.safe_string(data, 'x')
            status = self.safe_string(data, 'X')
            if (type == 'TRADE') and (status == 'FILLED'):
                self.handle_my_trades(client, message)
