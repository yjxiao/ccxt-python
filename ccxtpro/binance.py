# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange


class binance(Exchange):

    def describe(self):
        return self.deep_extend(super(binance, self).describe(), {
            'has': {
                'fetchWsOrderBook': True,
                'fetchWsOHLCV': True,
                'fetchWsTrades': True,
            },
            'urls': {
                'api': {
                    'wss': 'wss://stream.binance.com:9443/ws/',
                },
            },
        })

    def get_ws_message_hash(self, client, response):
        return client.url

    async def fetch_ws_trades(self, symbol):
        await self.load_markets()
        market = self.market(symbol)
        url = self.urls['api']['websocket']['public'] + market['id'].lower() + '@trade'
        return await self.WsTradesMessage(url, url)

    def handle_ws_trades(self, response):
        parsed = self.parse_trade(response)
        parsed['symbol'] = self.parse_symbol(response)
        return parsed

    async def fetch_ws_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        interval = self.timeframes[timeframe]
        market = self.market(symbol)
        url = self.urls['api']['websocket']['public'] + market['id'].lower() + '@kline_' + interval
        return await self.WsOHLCVMessage(url, url)

    def handle_ws_ohlcv(self, ohlcv):
        data = ohlcv['k']
        timestamp = self.safe_integer(data, 'T')
        open = self.safe_float(data, 'o')
        high = self.safe_float(data, 'h')
        close = self.safe_float(data, 'l')
        low = self.safe_float(data, 'c')
        volume = self.safe_float(data, 'v')
        return [timestamp, open, high, close, low, volume]

    async def fetch_ws_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        url = self.urls['api']['websocket']['public'] + market['id'].lower() + '@depth'
        # if not (symbol in list(self.orderbooks.keys())):
        #     snapshot = await self.fetch_order_book(symbol, limit, params)
        #     self.orderbooks[symbol] = IncrementalOrderBook(snapshot)
        # }
        return await self.WsOrderBookMessage(url, url)

    def handle_ws_order_book(self, orderBook):
        deltas = []
        nonce = orderBook['u']
        for i in range(0, len(orderBook['b'])):
            bid = orderBook['b'][i]
            deltas.append([nonce, 'absolute', 'bids', float(bid[0]), float(bid[1])])
        for i in range(0, len(orderBook['a'])):
            asks = orderBook['a'][i]
            deltas.append([nonce, 'absolute', 'asks', float(asks[0]), float(asks[1])])
        symbol = self.parse_symbol(orderBook)
        incrementalBook = self.orderbooks[symbol]
        incrementalBook.update(deltas)
        timestamp = self.safe_integer(orderBook, 'E')
        incrementalBook.orderBook['timestamp'] = timestamp
        incrementalBook.orderBook['datetime'] = self.iso8601(timestamp)
        incrementalBook.orderBook['nonce'] = orderBook['u']
        return incrementalBook.orderBook

    def parse_symbol(self, message):
        return self.marketsById[message['s']]['symbol']

    def handle_ws_dropped(self, client, response, messageHash):
        orderBookHash = 'wss://stream.binance.com:9443/ws/ethbtc@depth'
        if messageHash is not None and messageHash.startsWith(orderBookHash):
            self.handle_ws_order_book(response)
