# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.async_support.base.ws.client import Client
from typing import Optional
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported


class wazirx(ccxt.async_support.wazirx):

    def describe(self):
        return self.deep_extend(super(wazirx, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchTicker': True,
                'watchTickers': True,
                'watchTrades': True,
                'watchMyTrades': True,
                'watchOrders': True,
                'watchOrderBook': True,
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://stream.wazirx.com/stream',
                },
            },
            'options': {
            },
            'streaming': {
            },
            'exceptions': {
            },
            'api': {
                'private': {
                    'post': {
                        'create_auth_token': 1,
                    },
                },
            },
        })

    async def watch_balance(self, params={}):
        """
        watch balance and get the amount of funds available for trading or funds locked in orders
        :see: https://docs.wazirx.com/#account-update
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict: a `balance structure <https://github.com/ccxt/ccxt/wiki/Manual#balance-structure>`
        """
        await self.load_markets()
        token = await self.authenticate(params)
        messageHash = 'balance'
        url = self.urls['api']['ws']
        subscribe = {
            'event': 'subscribe',
            'streams': ['outboundAccountPosition'],
            'auth_key': token,
        }
        request = self.deep_extend(subscribe, params)
        return await self.watch(url, messageHash, request, messageHash)

    def handle_balance(self, client: Client, message):
        #
        #     {
        #         "data":
        #         {
        #           "B": [
        #             {
        #               "a":"wrx",
        #               "b":"2043856.426455209",
        #               "l":"3001318.98"
        #             }
        #           ],
        #           "E":1631683058909
        #         },
        #         "stream":"outboundAccountPosition"
        #     }
        #
        data = self.safe_value(message, 'data', {})
        balances = self.safe_value(data, 'B', [])
        timestamp = self.safe_integer(data, 'E')
        self.balance['info'] = balances
        self.balance['timestamp'] = timestamp
        self.balance['datetime'] = self.iso8601(timestamp)
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'a')
            code = self.safe_currency_code(currencyId)
            available = self.safe_number(balance, 'b')
            locked = self.safe_number(balance, 'l')
            account = self.account()
            account['free'] = available
            account['used'] = locked
            self.balance[code] = account
        self.balance = self.safe_balance(self.balance)
        messageHash = 'balance'
        client.resolve(self.balance, messageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        # trade
        #     {
        #         "E": 1631681323000,  Event time
        #         "S": "buy",          Side
        #         "a": 26946138,       Buyer order ID
        #         "b": 26946169,       Seller order ID
        #         "m": True,           Is buyer maker?
        #         "p": "7.0",          Price
        #         "q": "15.0",         Quantity
        #         "s": "btcinr",       Symbol
        #         "t": 17376030        Trade ID
        #     }
        # ownTrade
        #     {
        #         "E": 1631683058000,
        #         "S": "ask",
        #         "U": "inr",
        #         "a": 114144050,
        #         "b": 114144121,
        #         "f": "0.2",
        #         "m": True,
        #         "o": 26946170,
        #         "p": "5.0",
        #         "q": "20.0",
        #         "s": "btcinr",
        #         "t": 17376032,
        #         "w": "100.0"
        #     }
        #
        timestamp = self.safe_integer(trade, 'E')
        marketId = self.safe_string(trade, 's')
        market = self.safe_market(marketId, market)
        feeCost = self.safe_string(trade, 'f')
        feeCurrencyId = self.safe_string(trade, 'U')
        isMaker = self.safe_value(trade, 'm') is True
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': self.safe_currency_code(feeCurrencyId),
                'rate': None,
            }
        return self.safe_trade({
            'id': self.safe_string(trade, 't'),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': self.safe_string_n(trade, ['o']),
            'type': None,
            'side': self.safe_string(trade, 'S'),
            'takerOrMaker': 'maker' if isMaker else 'taker',
            'price': self.safe_string(trade, 'p'),
            'amount': self.safe_string(trade, 'q'),
            'cost': None,
            'fee': fee,
        }, market)

    async def watch_ticker(self, symbol: str, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://docs.wazirx.com/#all-market-tickers-stream
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        url = self.urls['api']['ws']
        messageHash = 'ticker:' + market['symbol']
        subscribeHash = 'tickers'
        stream = '!' + 'ticker@arr'
        subscribe = {
            'event': 'subscribe',
            'streams': [stream],
        }
        request = self.deep_extend(subscribe, params)
        return await self.watch(url, messageHash, request, subscribeHash)

    async def watch_tickers(self, symbols: Optional[List[str]] = None, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list
        :see: https://docs.wazirx.com/#all-market-tickers-stream
        :param str[] symbols: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        await self.load_markets()
        symbols = self.market_symbols(symbols)
        url = self.urls['api']['ws']
        messageHash = 'tickers'
        stream = '!' + 'ticker@arr'
        subscribe = {
            'event': 'subscribe',
            'streams': [stream],
        }
        request = self.deep_extend(subscribe, params)
        tickers = await self.watch(url, messageHash, request, messageHash)
        return self.filter_by_array(tickers, 'symbol', symbols, False)

    def handle_ticker(self, client: Client, message):
        #
        #     {
        #         "data":
        #         [
        #           {
        #             "E":1631625534000,    # Event time
        #             "T":"SPOT",           # Type
        #             "U":"wrx",            # Quote unit
        #             "a":"0.0",            # Best sell price
        #             "b":"0.0",            # Best buy price
        #             "c":"5.0",            # Last price
        #             "h":"5.0",            # High price
        #             "l":"5.0",            # Low price
        #             "o":"5.0",            # Open price
        #             "q":"0.0",            # Quantity
        #             "s":"btcwrx",         # Symbol
        #             "u":"btc"             # Base unit
        #           }
        #         ],
        #         "stream":"not ticker@arr"
        #     }
        #
        data = self.safe_value(message, 'data', [])
        for i in range(0, len(data)):
            ticker = data[i]
            parsedTicker = self.parse_ws_ticker(ticker)
            symbol = parsedTicker['symbol']
            self.tickers[symbol] = parsedTicker
            messageHash = 'ticker:' + symbol
            client.resolve(parsedTicker, messageHash)
        client.resolve(self.tickers, 'tickers')

    def parse_ws_ticker(self, ticker, market=None):
        #
        #     {
        #         "E":1631625534000,    # Event time
        #         "T":"SPOT",           # Type
        #         "U":"wrx",            # Quote unit
        #         "a":"0.0",            # Best sell price
        #         "b":"0.0",            # Best buy price
        #         "c":"5.0",            # Last price
        #         "h":"5.0",            # High price
        #         "l":"5.0",            # Low price
        #         "o":"5.0",            # Open price
        #         "q":"0.0",            # Quantity
        #         "s":"btcwrx",         # Symbol
        #         "u":"btc"             # Base unit
        #     }
        #
        marketId = self.safe_string(ticker, 's')
        timestamp = self.safe_integer(ticker, 'E')
        return self.safe_ticker({
            'symbol': self.safe_symbol(marketId, market),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'h'),
            'low': self.safe_string(ticker, 'l'),
            'bid': self.safe_number(ticker, 'b'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'a'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_string(ticker, 'o'),
            'close': None,
            'last': self.safe_string(ticker, 'l'),
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_string(ticker, 'q'),
            'info': ticker,
        }, market)

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = market['id'] + '@trades'
        url = self.urls['api']['ws']
        message = {
            'event': 'subscribe',
            'streams': [messageHash],
        }
        request = self.extend(message, params)
        trades = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client: Client, message):
        #
        #     {
        #         "data": {
        #             "trades": [{
        #                 "E": 1631681323000,  Event time
        #                 "S": "buy",          Side
        #                 "a": 26946138,       Buyer order ID
        #                 "b": 26946169,       Seller order ID
        #                 "m": True,           Is buyer maker?
        #                 "p": "7.0",          Price
        #                 "q": "15.0",         Quantity
        #                 "s": "btcinr",       Symbol
        #                 "t": 17376030        Trade ID
        #             }]
        #         },
        #         "stream": "btcinr@trades"
        #     }
        #
        data = self.safe_value(message, 'data', {})
        rawTrades = self.safe_value(data, 'trades', [])
        messageHash = self.safe_string(message, 'stream')
        split = messageHash.split('@')
        marketId = self.safe_string(split, 0)
        market = self.safe_market(marketId)
        symbol = self.safe_symbol(marketId, market)
        trades = self.safe_value(self.trades, symbol)
        if trades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            trades = ArrayCache(limit)
            self.trades[symbol] = trades
        for i in range(0, len(rawTrades)):
            parsedTrade = self.parse_ws_trade(rawTrades[i], market)
            trades.append(parsedTrade)
        client.resolve(trades, messageHash)

    async def watch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watch trades by user
        :see: https://docs.wazirx.com/#trade-update
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        token = await self.authenticate(params)
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        url = self.urls['api']['ws']
        messageHash = 'myTrades'
        message = {
            'event': 'subscribe',
            'streams': ['ownTrade'],
            'auth_key': token,
        }
        request = self.deep_extend(message, params)
        trades = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']
        messageHash = 'ohlcv:' + symbol + ':' + timeframe
        stream = market['id'] + '@kline_' + timeframe
        message = {
            'event': 'subscribe',
            'streams': [stream],
        }
        request = self.deep_extend(message, params)
        ohlcv = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client: Client, message):
        #
        #     {
        #         "data": {
        #           "E":1631683058904,      Event time
        #           "s": "btcinr",          Symbol
        #           "t": 1638747660000,     Kline start time
        #           "T": 1638747719999,     Kline close time
        #           "i": "1m",              Interval
        #           "o": "0.0010",          Open price
        #           "c": "0.0020",          Close price
        #           "h": "0.0025",          High price
        #           "l": "0.0015",          Low price
        #           "v": "1000",            Base asset volume
        #         },
        #         "stream": "btcinr@kline_1m"
        #     }
        #
        data = self.safe_value(message, 'data', {})
        marketId = self.safe_string(data, 's')
        market = self.safe_market(marketId)
        symbol = self.safe_symbol(marketId, market)
        timeframe = self.safe_string(data, 'i')
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        parsed = self.parse_ws_ohlcv(data, market)
        stored.append(parsed)
        messageHash = 'ohlcv:' + symbol + ':' + timeframe
        client.resolve(stored, messageHash)

    def parse_ws_ohlcv(self, ohlcv, market=None) -> list:
        #
        #    {
        #        "E":1631683058904,      Event time
        #        "s": "btcinr",          Symbol
        #        "t": 1638747660000,     Kline start time
        #        "T": 1638747719999,     Kline close time
        #        "i": "1m",              Interval
        #        "o": "0.0010",          Open price
        #        "c": "0.0020",          Close price
        #        "h": "0.0025",          High price
        #        "l": "0.0015",          Low price
        #        "v": "1000",            Base asset volume
        #    }
        #
        return [
            self.safe_integer(ohlcv, 't'),
            self.safe_number(ohlcv, 'o'),
            self.safe_number(ohlcv, 'c'),
            self.safe_number(ohlcv, 'h'),
            self.safe_number(ohlcv, 'l'),
            self.safe_number(ohlcv, 'v'),
        ]

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://docs.wazirx.com/#depth-stream
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the wazirx api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws']
        messageHash = 'orderbook:' + symbol
        stream = market['id'] + '@depth'
        subscribe = {
            'event': 'subscribe',
            'streams': [stream],
        }
        request = self.deep_extend(subscribe, params)
        orderbook = await self.watch(url, messageHash, request, messageHash)
        return orderbook.limit()

    def handle_delta(self, bookside, delta):
        bidAsk = self.parse_bid_ask(delta, 0, 1)
        bookside.storeArray(bidAsk)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book(self, client: Client, message):
        #
        #     {
        #         "data": {
        #             "E": 1659475095000,
        #             "a": [
        #                 ["23051.0", "1.30141"],
        #             ],
        #             "b": [
        #                 ["22910.0", "1.30944"],
        #             ],
        #             "s": "btcusdt"
        #         },
        #         "stream": "btcusdt@depth"
        #     }
        #
        data = self.safe_value(message, 'data', {})
        timestamp = self.safe_integer(data, 'E')
        marketId = self.safe_string(data, 's')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        messageHash = 'orderbook:' + symbol
        currentOrderBook = self.safe_value(self.orderbooks, symbol)
        if currentOrderBook is None:
            snapshot = self.parse_order_book(data, symbol, timestamp, 'b', 'a')
            orderBook = self.order_book(snapshot)
            self.orderbooks[symbol] = orderBook
        else:
            asks = self.safe_value(data, 'a', [])
            bids = self.safe_value(data, 'b', [])
            self.handle_deltas(currentOrderBook['asks'], asks)
            self.handle_deltas(currentOrderBook['bids'], bids)
            currentOrderBook['nonce'] = timestamp
            currentOrderBook['timestamp'] = timestamp
            currentOrderBook['datetime'] = self.iso8601(timestamp)
            self.orderbooks[symbol] = currentOrderBook
        client.resolve(self.orderbooks[symbol], messageHash)

    async def watch_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        await self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        token = await self.authenticate(params)
        messageHash = 'orders'
        message = {
            'event': 'subscribe',
            'streams': ['orderUpdate'],
            'auth_key': token,
        }
        url = self.urls['api']['ws']
        request = self.deep_extend(message, params)
        orders = await self.watch(url, messageHash, request, messageHash, request)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client: Client, message):
        #
        #     {
        #         "data": {
        #             "E": 1631683058904,
        #             "O": 1631683058000,
        #             "S": "ask",
        #             "V": "70.0",
        #             "X": "wait",
        #             "i": 26946170,
        #             "m": True,
        #             "o": "sell",
        #             "p": "5.0",
        #             "q": "70.0",
        #             "s": "wrxinr",
        #             "v": "0.0"
        #         },
        #         "stream": "orderUpdate"
        #     }
        #
        order = self.safe_value(message, 'data', {})
        parsedOrder = self.parse_ws_order(order)
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        orders.append(parsedOrder)
        messageHash = 'orders'
        client.resolve(self.orders, messageHash)
        messageHash += ':' + parsedOrder['symbol']
        client.resolve(self.orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        #     {
        #         "E": 1631683058904,
        #         "O": 1631683058000,
        #         "S": "ask",
        #         "V": "70.0",
        #         "X": "wait",
        #         "i": 26946170,
        #         "m": True,
        #         "o": "sell",
        #         "p": "5.0",
        #         "q": "70.0",
        #         "s": "wrxinr",
        #         "v": "0.0"
        #     }
        #
        timestamp = self.safe_integer(order, 'O')
        marketId = self.safe_string(order, 's')
        status = self.safe_string(order, 'X')
        market = self.safe_market(marketId)
        return self.safe_order({
            'info': order,
            'id': self.safe_string(order, 'i'),
            'clientOrderId': self.safe_string(order, 'c'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'symbol': market['symbol'],
            'type': 'limit' if self.safe_value(order, 'm') else 'market',
            'timeInForce': None,
            'postOnly': None,
            'side': self.safe_string(order, 'o'),
            'price': self.safe_string(order, 'p'),
            'stopPrice': None,
            'triggerPrice': None,
            'amount': self.safe_string(order, 'V'),
            'filled': None,
            'remaining': self.safe_string(order, 'q'),
            'cost': None,
            'average': self.safe_string(order, 'v'),
            'status': self.parse_order_status(status),
            'fee': None,
            'trades': None,
        }, market)

    def handle_my_trades(self, client: Client, message):
        #
        #     {
        #         "data": {
        #             "E": 1631683058000,
        #             "S": "ask",
        #             "U": "usdt",
        #             "a": 114144050,
        #             "b": 114144121,
        #             "f": "0.2",
        #             "ga": '0.0',
        #             "gc": 'usdt',
        #             "m": True,
        #             "o": 26946170,
        #             "p": "5.0",
        #             "q": "20.0",
        #             "s": "btcusdt",
        #             "t": 17376032,
        #             "w": "100.0"
        #         },
        #         "stream": "ownTrade"
        #     }
        #
        trade = self.safe_value(message, 'data', {})
        messageHash = 'myTrades'
        myTrades = None
        if self.myTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            myTrades = ArrayCacheBySymbolById(limit)
            self.myTrades = myTrades
        else:
            myTrades = self.myTrades
        parsedTrade = self.parse_ws_trade(trade)
        myTrades.append(parsedTrade)
        client.resolve(myTrades, messageHash)

    def handle_connected(self, client: Client, message):
        #
        #     {
        #         data: {
        #             timeout_duration: 1800
        #         },
        #         event: 'connected'
        #     }
        #
        return message

    def handle_subscribed(self, client: Client, message):
        #
        #     {
        #         data: {
        #             streams: ['not ticker@arr']
        #         },
        #         event: 'subscribed',
        #         id: 0
        #     }
        #
        return message

    def handle_error(self, client: Client, message):
        #
        #     {
        #         "data": {
        #             "code": 400,
        #             "message": "Invalid request: streams must be an array"
        #         },
        #         "event": "error",
        #         "id": 0
        #     }
        #
        #     {
        #         message: 'HeartBeat message not received, closing the connection',
        #         status: 'error'
        #     }
        #
        raise ExchangeError(self.id + ' ' + self.json(message))

    def handle_message(self, client: Client, message):
        status = self.safe_string(message, 'status')
        if status == 'error':
            return self.handle_error(client, message)
        event = self.safe_string(message, 'event')
        eventHandlers = {
            'error': self.handle_error,
            'connected': self.handle_connected,
            'subscribed': self.handle_subscribed,
        }
        eventHandler = self.safe_value(eventHandlers, event)
        if eventHandler is not None:
            return eventHandler(client, message)
        stream = self.safe_string(message, 'stream', '')
        streamHandlers = {
            'ticker@arr': self.handle_ticker,
            '@depth': self.handle_order_book,
            '@kline': self.handle_ohlcv,
            '@trades': self.handle_trades,
            'outboundAccountPosition': self.handle_balance,
            'orderUpdate': self.handle_order,
            'ownTrade': self.handle_my_trades,
        }
        streams = list(streamHandlers.keys())
        for i in range(0, len(streams)):
            if self.in_array(streams[i], stream):
                handler = streamHandlers[streams[i]]
                return handler(client, message)
        raise NotSupported(self.id + ' self message type is not supported yet. Message: ' + self.json(message))

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']
        client = self.client(url)
        messageHash = 'authenticated'
        now = self.milliseconds()
        subscription = self.safe_value(client.subscriptions, messageHash)
        expires = self.safe_integer(subscription, 'expires')
        if subscription is None or now > expires:
            subscription = await self.privatePostCreateAuthToken()
            subscription['expires'] = now + self.safe_integer(subscription, 'timeout_duration') * 1000
            #
            #     {
            #         "auth_key": "Xx***dM",
            #         "timeout_duration": 900
            #     }
            #
            client.subscriptions[messageHash] = subscription
        return self.safe_string(subscription, 'auth_key')
