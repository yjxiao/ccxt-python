# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.ws.base.exchange import Exchange
from ccxt.rest.async_support import hitbtc as hitbtcRest
from ccxt.ws.base.cache import ArrayCache, ArrayCacheByTimestamp


class hitbtc(Exchange, hitbtcRest):

    def describe(self):
        return self.deep_extend(super(hitbtc, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': False,  # not available on exchange side
                'watchTrades': True,
                'watchOrderBook': True,
                'watchBalance': False,  # not implemented yet
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api.hitbtc.com/api/2/ws',
                },
            },
            'options': {
                'tradesLimit': 1000,
                'methods': {
                    'orderbook': 'subscribeOrderbook',
                    'ticker': 'subscribeTicker',
                    'trades': 'subscribeTrades',
                    'ohlcv': 'subscribeCandles',
                },
            },
        })

    async def watch_public(self, symbol, channel, timeframe=None, params={}):
        await self.load_markets()
        marketId = self.market_id(symbol)
        url = self.urls['api']['ws']
        messageHash = channel + ':' + marketId
        if timeframe is not None:
            messageHash += ':' + timeframe
        methods = self.safe_value(self.options, 'methods', {})
        method = self.safe_string(methods, channel, channel)
        requestId = self.nonce()
        subscribe = {
            'method': method,
            'params': {
                'symbol': marketId,
            },
            'id': requestId,
        }
        request = self.deep_extend(subscribe, params)
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        orderbook = await self.watch_public(symbol, 'orderbook', None, params)
        return orderbook.limit(limit)

    def handle_order_book_snapshot(self, client, message):
        #
        #     {
        #         jsonrpc: "2.0",
        #         method: "snapshotOrderbook",
        #         params: {
        #             ask: [
        #                 {price: "6927.75", size: "0.11991"},
        #                 {price: "6927.76", size: "0.06200"},
        #                 {price: "6927.85", size: "0.01000"},
        #             ],
        #             bid: [
        #                 {price: "6926.18", size: "0.16898"},
        #                 {price: "6926.17", size: "0.06200"},
        #                 {price: "6925.97", size: "0.00125"},
        #             ],
        #             symbol: "BTCUSD",
        #             sequence: 494854,
        #             timestamp: "2020-04-03T08:58:53.460Z"
        #         }
        #     }
        #
        params = self.safe_value(message, 'params', {})
        marketId = self.safe_string(params, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(params, 'timestamp'))
        nonce = self.safe_integer(params, 'sequence')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        snapshot = self.parse_order_book(params, symbol, timestamp, 'bid', 'ask', 'price', 'size')
        orderbook = self.order_book(snapshot)
        orderbook['nonce'] = nonce
        self.orderbooks[symbol] = orderbook
        messageHash = 'orderbook:' + marketId
        client.resolve(orderbook, messageHash)

    def handle_order_book_update(self, client, message):
        #
        #     {
        #         jsonrpc: "2.0",
        #         method: "updateOrderbook",
        #         params: {
        #             ask: [
        #                 {price: "6940.65", size: "0.00000"},
        #                 {price: "6940.66", size: "6.00000"},
        #                 {price: "6943.52", size: "0.04707"},
        #             ],
        #             bid: [
        #                 {price: "6938.40", size: "0.11991"},
        #                 {price: "6938.39", size: "0.00073"},
        #                 {price: "6936.65", size: "0.00000"},
        #             ],
        #             symbol: "BTCUSD",
        #             sequence: 497872,
        #             timestamp: "2020-04-03T09:03:56.685Z"
        #         }
        #     }
        #
        params = self.safe_value(message, 'params', {})
        marketId = self.safe_string(params, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        if symbol in self.orderbooks:
            timestamp = self.parse8601(self.safe_string(params, 'timestamp'))
            nonce = self.safe_integer(params, 'sequence')
            orderbook = self.orderbooks[symbol]
            asks = self.safe_value(params, 'ask', [])
            bids = self.safe_value(params, 'bid', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            orderbook['nonce'] = nonce
            self.orderbooks[symbol] = orderbook
            messageHash = 'orderbook:' + marketId
            client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 'price')
        amount = self.safe_float(delta, 'size')
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    async def watch_ticker(self, symbol, params={}):
        return await self.watch_public(symbol, 'ticker', None, params)

    def handle_ticker(self, client, message):
        #
        #     {
        #         jsonrpc: '2.0',
        #         method: 'ticker',
        #         params: {
        #             ask: '6983.22',
        #             bid: '6980.77',
        #             last: '6980.77',
        #             open: '6650.05',
        #             low: '6606.45',
        #             high: '7223.11',
        #             volume: '79264.33941',
        #             volumeQuote: '540183372.5134832',
        #             timestamp: '2020-04-03T10:02:18.943Z',
        #             symbol: 'BTCUSD'
        #         }
        #     }
        #
        params = self.safe_value(message, 'params')
        marketId = self.safe_value(params, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        result = self.parse_ticker(params, market)
        self.tickers[symbol] = result
        method = self.safe_value(message, 'method')
        messageHash = method + ':' + marketId
        client.resolve(result, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        trades = await self.watch_public(symbol, 'trades', None, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        #     {
        #         jsonrpc: '2.0',
        #         method: 'snapshotTrades',  # updateTrades
        #         params: {
        #             data: [
        #                 {
        #                     id: 814145791,
        #                     price: '6957.20',
        #                     quantity: '0.02779',
        #                     side: 'buy',
        #                     timestamp: '2020-04-03T10:28:20.032Z'
        #                 },
        #                 {
        #                     id: 814145792,
        #                     price: '6957.20',
        #                     quantity: '0.12918',
        #                     side: 'buy',
        #                     timestamp: '2020-04-03T10:28:20.039Z'
        #                 },
        #             ],
        #             symbol: 'BTCUSD'
        #         }
        #     }
        #
        params = self.safe_value(message, 'params', {})
        data = self.safe_value(params, 'data', [])
        marketId = self.safe_string(params, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        messageHash = 'trades:' + marketId
        tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            stored = ArrayCache(tradesLimit)
            self.trades[symbol] = stored
        if isinstance(data, list):
            trades = self.parse_trades(data, market)
            for i in range(0, len(trades)):
                stored.append(trades[i])
        else:
            trade = self.parse_trade(message, market)
            stored.append(trade)
        client.resolve(stored, messageHash)
        return message

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        # if limit is None:
        #     limit = 100
        # }
        period = self.timeframes[timeframe]
        request = {
            'params': {
                'period': period,
                # 'limit': limit,
            },
        }
        requestParams = self.deep_extend(request, params)
        ohlcv = await self.watch_public(symbol, 'ohlcv', period, requestParams)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #     {
        #         jsonrpc: '2.0',
        #         method: 'snapshotCandles',  # updateCandles
        #         params: {
        #             data: [
        #                 {
        #                     timestamp: '2020-04-05T00:06:00.000Z',
        #                     open: '6869.40',
        #                     close: '6867.16',
        #                     min: '6863.17',
        #                     max: '6869.4',
        #                     volume: '0.08947',
        #                     volumeQuote: '614.4195442'
        #                 },
        #                 {
        #                     timestamp: '2020-04-05T00:07:00.000Z',
        #                     open: '6867.54',
        #                     close: '6859.26',
        #                     min: '6858.85',
        #                     max: '6867.54',
        #                     volume: '1.7766',
        #                     volumeQuote: '12191.5880395'
        #                 },
        #             ],
        #             symbol: 'BTCUSD',
        #             period: 'M1'
        #         }
        #     }
        #
        params = self.safe_value(message, 'params', {})
        data = self.safe_value(params, 'data', [])
        marketId = self.safe_string(params, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        period = self.safe_string(params, 'period')
        timeframe = self.find_timeframe(period)
        messageHash = 'ohlcv:' + marketId + ':' + period
        for i in range(0, len(data)):
            candle = data[i]
            parsed = self.parse_ohlcv(candle, market)
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            stored = self.safe_value(self.ohlcvs[symbol], timeframe)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol][timeframe] = stored
            stored.append(parsed)
            client.resolve(stored, messageHash)
        return message

    def handle_notification(self, client, message):
        #
        #     {jsonrpc: '2.0', result: True, id: null}
        #
        return message

    def handle_message(self, client, message):
        methods = {
            'snapshotOrderbook': self.handle_order_book_snapshot,
            'updateOrderbook': self.handle_order_book_update,
            'ticker': self.handle_ticker,
            'snapshotTrades': self.handle_trades,
            'updateTrades': self.handle_trades,
            'snapshotCandles': self.handle_ohlcv,
            'updateCandles': self.handle_ohlcv,
        }
        event = self.safe_string(message, 'method')
        method = self.safe_value(methods, event)
        if method is None:
            self.handle_notification(client, message)
        else:
            method(client, message)
