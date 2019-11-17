# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support as ccxt


class poloniex(ccxt.poloniex):

    def describe(self):
        return self.deep_extend(super(poloniex, self).describe(), {
            'has': {
                'ws': True,
                'fetchWsTicker': True,
                'fetchWsOrderBook': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api2.poloniex.com/',
                },
            },
        })

    def get_ws_message_hash(self, client, response):
    #     channelId = str(response[0])
    #     length = len(response)
    #     if length <= 2:
    #         return
    #     }
    #     if channelId == '1002':
    #         return channelId + str(response[2][0])
    #     else:
    #         return channelId
    #     }

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

    async def fetch_ws_tickers(self, symbol):
        await self.load_markets()
        market = self.market(symbol)
        numericId = str(market['info']['id'])
        url = self.urls['api']['websocket']['public']
        return await self.WsTickerMessage(url, '1002' + numericId, {
            'command': 'subscribe',
            'channel': 1002,
        })

    async def load_markets(self, reload=False, params={}):
        markets = await super(poloniex, self).load_markets(reload, params)
        marketsByNumericId = self.safe_value(self.options, 'marketsByNumericId')
        if (marketsByNumericId is None) or reload:
            marketsByNumericId = {}
            for i in range(0, len(self.symbols)):
                symbol = self.symbols[i]
                market = self.markets[symbol]
                numericId = self.safe_string(market, 'numericId')
                marketsByNumericId[numericId] = market
            self.options['marketsByNumericId'] = marketsByNumericId
        return markets

    async def fetch_ws_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        numericId = self.safe_string(market, 'numericId')
        url = self.urls['api']['ws']
        orderbook = await self.sendWsMessage(url, numericId, {
            'command': 'subscribe',
            'channel': numericId,
        })
        return orderbook.limit(limit)

    def handle_ws_heartbeat(self, message):
        #
        # every second
        #
        #     [1010]
        #
        return message

    def handle_ws_order_book_and_trades(self, message):
        #
        # first response
        #
        #     [
        #         14,  # channelId == market['numericId']
        #         8767,  # nonce
        #         [
        #             [
        #                 "i",  # initial snapshot
        #                 {
        #                     "currencyPair": "BTC_BTS",
        #                     "orderBook": [
        #                         {"0.00001853": "2537.5637", "0.00001854": "1567238.172367"},  # asks, price, size
        #                         {"0.00001841": "3645.3647", "0.00001840": "1637.3647"}  # bids
        #                     ]
        #                 }
        #             ]
        #         ]
        #     ]
        #
        # subsequent updates
        #
        #     [
        #         14,
        #         8768,
        #         [
        #             ["o", 1, "0.00001823", "5534.6474"],  # orderbook delta, bids, price, size
        #             ["o", 0, "0.00001824", "6575.464"],  # orderbook delta, asks, price, size
        #             ["t", "42706057", 1, "0.05567134", "0.00181421", 1522877119]  # trade, id, sell, price, size, timestamp
        #         ]
        #     ]
        #
        # TODO: handle incremental trades too
        marketId = str(message[0])
        nonce = message[1]
        data = message[2]
        market = self.safe_value(self.options['marketsByNumericId'], marketId)
        symbol = self.safe_string(market, 'symbol')
        orderbookCount = 0
        tradesCount = 0
        for i in range(0, len(data)):
            delta = data[i]
            if delta[0] == 'i':
                snapshot = self.safe_value(delta[1], 'orderBook', [])
                sides = ['asks', 'bids']
                self.orderbooks[symbol] = self.orderbook()
                orderbook = self.orderbooks[symbol]
                for j in range(0, len(snapshot)):
                    side = sides[j]
                    bookside = orderbook[side]
                    orders = snapshot[j]
                    prices = list(orders.keys())
                    for k in range(0, len(prices)):
                        price = prices[k]
                        amount = float(orders[price])
                        bookside.store(price, amount)
                orderbook['nonce'] = nonce
                orderbookCount += 1
            elif delta[0] == 'o':
                orderbook = self.orderbooks[symbol]
                side = 'bids' if delta[1] else 'asks'
                bookside = orderbook[side]
                price = delta[2]
                amount = float(delta[3])
                bookside.store(price, amount)
                orderbookCount += 1
            elif delta[0] == 't':
                trade = self.parseWsTrade(delta)
                self.trades.append(trade)
                tradesCount += 1
        if orderbookCount:
            # resolve the orderbook future
        if tradesCount:
            # resolve the trades future

    def handle_ws_message(self, client, message):
        channelId = str(message[0])
        market = self.safe_value(self.options['marketsByNumericId'], channelId)
        if market is None:
            methods = {
                # '<numericId>': 'handleWsOrderBookAndTrades',  # Price Aggregated Book
                '1000': 'handleWsPrivateAccountNotifications',  #(Beta)
                '1002': 'handleWsTicker',  # Ticker Data
                # '1003': None,  # 24 Hour Exchange Volume
                '1010': 'handleWsHeartbeat',
            }
            method = self.safe_string(methods, channelId)
            if method is None:
                return message
            else:
                return getattr(self, method)(message)
        else:
            return self.handle_ws_order_book_and_trades(message)
        # if channelId in self.options['marketsByNumericId']:
        #     return self.handle_ws_order_book_and_trades(message)
        # else:
        #     methods = {
        #         # '<numericId>': 'handleWsOrderBookAndTrades',  # Price Aggregated Book
        #         '1000': 'handleWsPrivateAccountNotifications',  #(Beta)
        #         '1002': 'handleWsTicker',  # Ticker Data
        #         # '1003': None,  # 24 Hour Exchange Volume
        #         '1010': 'handleWsHeartbeat',
        #     }
        #     method = self.safe_string(methods, channelId)
        #     if method is None:
        #         return message
        #     else:
        #         return getattr(self, method)(message)
        #     }
        # }
