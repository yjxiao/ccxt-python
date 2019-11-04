# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support as ccxt


class poloniex(ccxt.poloniex):

    def describe(self):
        return self.deep_extend(super(poloniex, self).describe(), {
            'has': {
                'fetchWsTicker': True,
                'fetchWsOrderBook': True,
            },
            'urls': {
                'api': {
                    'wss': 'wss://api2.poloniex.com/',
                },
            },
        })

    def get_ws_message_hash(self, client, response):
        channelId = str(response[0])
        length = len(response)
        if length <= 2:
            return
        if channelId == '1002':
            return channelId + str(response[2][0])
        else:
            return channelId

    def handle_ws_ticker(self, response):
        data = response[2]
        market = self.safe_value(self.options['marketsByNumericId'], str(data[0]))
        symbol = self.safe_string(market, 'symbol')
        return {
            'info': response,
            'symbol': symbol,
            'last': float(data[1]),
            'ask': float(data[2]),
            'bid': float(data[3]),
            'change': float(data[4]),
            'baseVolume': float(data[5]),
            'quoteVolume': float(data[6]),
            'active': False if data[7] else True,
            'high': float(data[8]),
            'low': float(data[9]),
        }

    async def fetch_ws_ticker(self, symbol):
        await self.load_markets()
        self.markets_by_numeric_id()
        market = self.market(symbol)
        numericId = str(market['info']['id'])
        url = self.urls['api']['websocket']['public']
        return await self.WsTickerMessage(url, '1002' + numericId, {
            'command': 'subscribe',
            'channel': 1002,
        })

    def markets_by_numeric_id(self):
        if self.options['marketsByNumericId'] is None:
            keys = list(self.markets.keys())
            self.options['marketsByNumericId'] = {}
            for i in range(0, len(keys)):
                key = keys[i]
                market = self.markets[key]
                numericId = str(market['info']['id'])
                self.options['marketsByNumericId'][numericId] = market

    async def fetch_ws_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        self.markets_by_numeric_id()
        market = self.market(symbol)
        numericId = str(market['info']['id'])
        url = self.urls['api']['websocket']['public']
        return await self.WsOrderBookMessage(url, numericId, {
            'command': 'subscribe',
            'channel': numericId,
        })

    def handle_ws_order_book(self, orderBook):
        # TODO: handle incremental trades too
        data = orderBook[2]
        deltas = []
        for i in range(0, len(data)):
            delta = data[i]
            if delta[0] == 'i':
                rawBook = delta[1]['orderBook']
                bids = rawBook[1]
                asks = rawBook[0]
                delta = {
                    'bids': self.parse_bid_ask(bids),
                    'asks': self.parse_bid_ask(asks),
                    'nonce': None,
                    'timestamp': None,
                    'datetime': None,
                }
                deltas.append(delta)
            elif delta[0] == 'o':
                price = float(delta[2])
                amount = float(delta[3])
                operation = 'delete' if (amount == 0) else 'add'
                side = 'bids' if delta[1] else 'asks'
                delta = [None, operation, side, price, amount]
                deltas.append(delta)
        market = self.safe_value(self.options['marketsByNumericId'], str(orderBook[0]))
        symbol = self.safe_string(market, 'symbol')
        # if not (symbol in list(self.orderBooks.keys())):
        #     self.orderBooks[symbol] = IncrementalOrderBook(deltas.pop(0))
        # }
        incrementalBook = self.orderBooks[symbol]
        incrementalBook.update(deltas)
        incrementalBook.orderBook['nonce'] = orderBook[1]
        return incrementalBook.orderBook

    def parse_bid_ask(self, bidasks):
        prices = list(bidasks.keys())
        result = []
        for i in range(0, len(prices)):
            price = prices[i]
            amount = bidasks[price]
            result.append([float(price), float(amount)])
        return result

    def handle_ws_dropped(self, client, response, messageHash):
        if messageHash is not None and int(messageHash) < 1000:
            self.handle_ws_order_book(response)
