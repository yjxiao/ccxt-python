# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt


class binance(ccxtpro.Exchange, ccxt.binance):

    def describe(self):
        return self.deep_extend(super(binance, self).describe(), {
            'has': {
                'fetchWsOrderBook': True,
                'fetchWsOHLCV': True,
                'fetchWsTrades': True,
            },
            'urls': {
                'api': {
                    # 'ws': 'wss://stream.binance.com:9443/ws',
                    # 'ws': 'wss://echo.websocket.org/',
                    'ws': 'ws://127.0.0.1:8080',
                },
            },
            'options': {
                'marketsByLowerCaseId': {},
            },
        })

    async def load_markets(self, reload=False, params={}):
        markets = await super(binance, self).load_markets(reload, params)
        marketsByLowercaseId = self.safe_value(self.options, 'marketsByLowercaseId')
        if (marketsByLowercaseId is None) or reload:
            marketsByLowercaseId = {}
            for i in range(0, len(self.symbols)):
                symbol = self.symbols[i]
                lowercaseId = self.markets[symbol]['id'].lower()
                self.markets[symbol]['lowercaseId'] = lowercaseId
                marketsByLowercaseId[lowercaseId] = self.markets[symbol]
            self.options['marketsByLowercaseId'] = marketsByLowercaseId
        return markets

    async def fetch_ws_trades(self, symbol):
        #     await self.load_markets()
        #     market = self.market(symbol)
        #     url = self.urls['api']['ws'] + market['id'].lower() + '@trade'
        #     return await self.WsTradesMessage(url, url)
        raise NotImplemented(self.id + ' fetchWsTrades not implemented yet')

    def handle_ws_trades(self, response):
        #     parsed = self.parse_trade(response)
        #     parsed['symbol'] = self.parseSymbol(response)
        #     return parsed
        raise NotImplemented(self.id + ' handleWsTrades not implemented yet')

    async def fetch_ws_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        #     await self.load_markets()
        #     interval = self.timeframes[timeframe]
        #     market = self.market(symbol)
        #     url = self.urls['api']['ws'] + market['id'].lower() + '@kline_' + interval
        #     return await self.WsOHLCVMessage(url, url)
        raise NotImplemented(self.id + ' fetchWsOHLCV not implemented yet')

    def handle_ws_ohlcv(self, ohlcv):
        #     data = ohlcv['k']
        #     timestamp = self.safe_integer(data, 'T')
        #     open = self.safe_float(data, 'o')
        #     high = self.safe_float(data, 'h')
        #     close = self.safe_float(data, 'l')
        #     low = self.safe_float(data, 'c')
        #     volume = self.safe_float(data, 'v')
        #     return [timestamp, open, high, close, low, volume]
        raise NotImplemented(self.id + ' handleWsOHLCV not implemented yet ' + self.json(ohlcv))

    async def fetch_ws_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        # self should be executed much later
        # orderbook = await self.fetch_order_book(symbol, limit, params)
        # request = {}
        name = 'depth'
        stream = market['lowercaseId'] + '@' + name
        url = self.urls['api']['ws']  # + '/' + stream
        requestId = self.nonce()
        request = {
            'method': 'SUBSCRIBE',
            'params': [
                stream,
            ],
            'id': requestId,
        }
        messageHash = stream
        future = self.sendWsMessage(url, messageHash, self.extend(request, params), messageHash)
        client = self.clients[url]
        client['futures'][requestId] = future
        return future

    def handle_ws_order_book(self, client, message):
        #
        # initial snapshot is fetched with ccxt's fetchOrderBook
        # the feed does not include a snapshot, just the deltas
        #
        #     {
        #         "e": "depthUpdate",  # Event type
        #         "E": 123456789,  # Event time
        #         "s": "BNBBTC",  # Symbol
        #         "U": 157,  # First update ID in event
        #         "u": 160,  # Final update ID in event
        #         "b": [ # bids
        #             ["0.0024", "10"],  # price, size
        #         ],
        #         "a": [ # asks
        #             ["0.0026", "100"],  # price, size
        #         ]
        #     }
        #
        deltas = []
        nonce = message['u']
        for i in range(0, len(message['b'])):
            bid = message['b'][i]
            deltas.append([nonce, 'absolute', 'bids', float(bid[0]), float(bid[1])])
        for i in range(0, len(message['a'])):
            asks = message['a'][i]
            deltas.append([nonce, 'absolute', 'asks', float(asks[0]), float(asks[1])])
        symbol = self.parseSymbol(message)
        incrementalBook = self.orderbooks[symbol]
        incrementalBook.update(deltas)
        timestamp = self.safe_integer(message, 'E')
        incrementalBook.message['timestamp'] = timestamp
        incrementalBook.message['datetime'] = self.iso8601(timestamp)
        incrementalBook.message['nonce'] = message['u']
        return incrementalBook.orderBook

    def sign_ws_message(self, client, messageHash, message, params={}):
        # todo: binance signWsMessage not implemented yet
        return message

    def handle_ws_subscription_status(self, client, message):
        #
        # todo: answer the question whether handleWsSubscriptionStatus should be renamed
        # and unified as handleWsResponse for any usage pattern that
        # involves an identified request/response sequence
        #
        #     {
        #         "result": None,
        #         "id": 1574649734450
        #     }
        #
        channelId = self.safe_string(message, 'channelID')
        self.options['subscriptionStatusByChannelId'][channelId] = message
        requestId = self.safe_string(message, 'reqid')
        if client.futures[requestId]:
            del client.futures[requestId]

    def handle_ws_message(self, client, message):
        print(message)
        #
        # keys = list(client.futures.keys())
        # for i in range(0, len(keys)):
        #     key = keys[i]
        #     self.rejectWsFuture()
        # }
        #
        # --------------------------------------------------------------------
        #
        # print(new Date(), json.dumps(message, None, 4))
        # print('---------------------------------------------------------')
        # if isinstance(message, list):
        #     channelId = str(message[0])
        #     subscriptionStatus = self.safe_value(self.options['subscriptionStatusByChannelId'], channelId, {})
        #     subscription = self.safe_value(subscriptionStatus, 'subscription', {})
        #     name = self.safe_string(subscription, 'name')
        #     methods = {
        #         'book': 'handleWsOrderBook',
        #         'ohlc': 'handleWsOHLCV',
        #         'ticker': 'handleWsTicker',
        #         'trade': 'handleWsTrades',
        #     }
        #     method = self.safe_string(methods, name)
        #     if method is None:
        #         return message
        #     else:
        #         return getattr(self, method)(client, message)
        #     }
        # else:
        #     if self.handleWsErrors(client, message):
        #         event = self.safe_string(message, 'event')
        #         methods = {
        #             'heartbeat': 'handleWsHeartbeat',
        #             'systemStatus': 'handleWsSystemStatus',
        #             'subscriptionStatus': 'handleWsSubscriptionStatus',
        #         }
        #         method = self.safe_string(methods, event)
        #         if method is None:
        #             return message
        #         else:
        #             return getattr(self, method)(client, message)
        #         }
        #     }
        # }
