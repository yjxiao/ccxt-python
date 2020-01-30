# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol


class kraken(ccxtpro.Exchange, ccxt.kraken):

    def describe(self):
        return self.deep_extend(super(kraken, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchTrades': True,
                'watchOrderBook': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://ws.kraken.com',
                        'private': 'wss://ws-auth.kraken.com',
                        'beta': 'wss://beta-ws.kraken.com',
                    },
                },
            },
            'versions': {
                'ws': '0.2.0',
            },
            'options': {
                'tradesLimit': 1000,
            },
            'exceptions': {
                'ws': {
                    'exact': {
                        'Event(s) not found': BadRequest,
                    },
                    'broad': {
                        'Currency pair not in ISO 4217-A3 format': BadSymbol,
                    },
                },
            },
        })

    def handle_ticker(self, client, message):
        #
        #     [
        #         0,  # channelID
        #         {
        #             "a": ["5525.40000", 1, "1.000"],  # ask, wholeAskVolume, askVolume
        #             "b": ["5525.10000", 1, "1.000"],  # bid, wholeBidVolume, bidVolume
        #             "c": ["5525.10000", "0.00398963"],  # closing price, volume
        #             "h": ["5783.00000", "5783.00000"],  # high price today, high price 24h ago
        #             "l": ["5505.00000", "5505.00000"],  # low price today, low price 24h ago
        #             "o": ["5760.70000", "5763.40000"],  # open price today, open price 24h ago
        #             "p": ["5631.44067", "5653.78939"],  # vwap today, vwap 24h ago
        #             "t": [11493, 16267],  # number of trades today, 24 hours ago
        #             "v": ["2634.11501494", "3591.17907851"],  # volume today, volume 24 hours ago
        #         },
        #         "ticker",
        #         "XBT/USD"
        #     ]
        #
        wsName = message[3]
        name = 'ticker'
        messageHash = name + ':' + wsName
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        ticker = message[1]
        vwap = self.safe_float(ticker['p'], 0)
        quoteVolume = None
        baseVolume = self.safe_float(ticker['v'], 0)
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker['c'], 0)
        timestamp = self.milliseconds()
        result = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker['h'], 0),
            'low': self.safe_float(ticker['l'], 0),
            'bid': self.safe_float(ticker['b'], 0),
            'bidVolume': self.safe_float(ticker['b'], 2),
            'ask': self.safe_float(ticker['a'], 0),
            'askVolume': self.safe_float(ticker['a'], 2),
            'vwap': vwap,
            'open': self.safe_float(ticker['o'], 0),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }
        # todo: add support for multiple tickers(may be tricky)
        # kraken confirms multi-pair subscriptions separately one by one
        # trigger correct watchTickers calls upon receiving any of symbols
        self.tickers[symbol] = result
        client.resolve(result, messageHash)

    async def watch_balance(self, params={}):
        await self.load_markets()
        raise NotImplemented(self.id + ' watchBalance() not implemented yet')

    def handle_trades(self, client, message):
        #
        #     [
        #         0,  # channelID
        #         [ #     price        volume         time             side type misc
        #             ["5541.20000", "0.15850568", "1534614057.321597", "s", "l", ""],
        #             ["6060.00000", "0.02455000", "1534614057.324998", "b", "l", ""],
        #         ],
        #         "trade",
        #         "XBT/USD"
        #     ]
        #
        # todo: incremental trades – add max limit to the dequeue of trades, unshift and push
        #
        #     trade = self.handle_trade(client, delta, market)
        #     self.trades.append(trade)
        #     tradesCount += 1
        #
        wsName = self.safe_string(message, 3)
        name = self.safe_string(message, 2)
        messageHash = name + ':' + wsName
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol, [])
        trades = self.safe_value(message, 1, [])
        parsed = self.parse_trades(trades, market)
        for i in range(0, len(parsed)):
            stored.append(parsed[i])
            storedLength = len(stored)
            if storedLength > self.options['tradesLimit']:
                stored.pop(0)
        self.trades[symbol] = stored
        client.resolve(stored, messageHash)

    def handle_ohlcv(self, client, message):
        #
        #     [
        #         216,  # channelID
        #         [
        #             '1574454214.962096',  # Time, seconds since epoch
        #             '1574454240.000000',  # End timestamp of the interval
        #             '0.020970',  # Open price at midnight UTC
        #             '0.020970',  # Intraday high price
        #             '0.020970',  # Intraday low price
        #             '0.020970',  # Closing price at midnight UTC
        #             '0.020970',  # Volume weighted average price
        #             '0.08636138',  # Accumulated volume today
        #             1,  # Number of trades today
        #         ],
        #         'ohlc-1',  # Channel Name of subscription
        #         'ETH/XBT',  # Asset pair
        #     ]
        #
        wsName = message[3]
        name = 'ohlc'
        candle = message[1]
        # print(
        #     self.iso8601(int(float(candle[0]) * 1000)), '-',
        #     self.iso8601(int(float(candle[1]) * 1000)), ': [',
        #     float(candle[2]),
        #     float(candle[3]),
        #     float(candle[4]),
        #     float(candle[5]),
        #     float(candle[7]), ']'
        # )
        result = [
            int(float(candle[0]) * 1000),
            float(candle[2]),
            float(candle[3]),
            float(candle[4]),
            float(candle[5]),
            float(candle[7]),
        ]
        messageHash = name + ':' + wsName
        client.resolve(result, messageHash)

    def reqid(self):
        # their support said that reqid must be an int32, not documented
        reqid = self.sum(self.safe_integer(self.options, 'reqid', 0), 1)
        self.options['reqid'] = reqid
        return reqid

    async def watch_public(self, name, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        wsName = self.safe_value(market['info'], 'wsname')
        messageHash = name + ':' + wsName
        url = self.urls['api']['ws']['public']
        requestId = self.reqid()
        subscribe = {
            'event': 'subscribe',
            'reqid': requestId,
            'pair': [
                wsName,
            ],
            'subscription': {
                'name': name,
            },
        }
        request = self.deep_extend(subscribe, params)
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_ticker(self, symbol, params={}):
        return await self.watch_public('ticker', symbol, params)

    async def watch_trades(self, symbol, params={}):
        return await self.watch_public('trade', symbol, params)

    async def watch_order_book(self, symbol, limit=None, params={}):
        name = 'book'
        request = {}
        if limit is not None:
            request['subscription'] = {
                'depth': limit,  # default 10, valid options 10, 25, 100, 500, 1000
            }
        future = self.watch_public(name, symbol, self.extend(request, params))
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def limit_order_book(self, orderbook, symbol, limit=None, params={}):
        return orderbook.limit(limit)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        name = 'ohlc'
        request = {
            'subscription': {
                'interval': int(self.timeframes[timeframe]),
            },
        }
        return await self.watch_public(name, symbol, self.extend(request, params))

    async def load_markets(self, reload=False, params={}):
        markets = await super(kraken, self).load_markets(reload, params)
        marketsByWsName = self.safe_value(self.options, 'marketsByWsName')
        if (marketsByWsName is None) or reload:
            marketsByWsName = {}
            for i in range(0, len(self.symbols)):
                symbol = self.symbols[i]
                market = self.markets[symbol]
                if not market['darkpool']:
                    info = self.safe_value(market, 'info', {})
                    wsName = self.safe_string(info, 'wsname')
                    marketsByWsName[wsName] = market
            self.options['marketsByWsName'] = marketsByWsName
        return markets

    async def watch_heartbeat(self, params={}):
        await self.load_markets()
        event = 'heartbeat'
        url = self.urls['api']['ws']['public']
        return await self.watch(url, event)

    def handle_heartbeat(self, client, message):
        #
        # every second(approx) if no other updates are sent
        #
        #     {"event": "heartbeat"}
        #
        event = self.safe_string(message, 'event')
        client.resolve(message, event)

    def handle_trade(self, client, trade, market=None):
        #
        # public trades
        #
        #     [
        #         "t",  # trade
        #         "42706057",  # id
        #         1,  # 1 = buy, 0 = sell
        #         "0.05567134",  # price
        #         "0.00181421",  # amount
        #         1522877119,  # timestamp
        #     ]
        #
        id = str(trade[1])
        side = 'buy' if trade[2] else 'sell'
        price = float(trade[3])
        amount = float(trade[4])
        timestamp = trade[5] * 1000
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': None,
            'type': None,
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': None,
        }

    def handle_order_book(self, client, message):
        #
        # first message(snapshot)
        #
        #     [
        #         1234,  # channelID
        #         {
        #             "as": [
        #                 ["5541.30000", "2.50700000", "1534614248.123678"],
        #                 ["5541.80000", "0.33000000", "1534614098.345543"],
        #                 ["5542.70000", "0.64700000", "1534614244.654432"]
        #             ],
        #             "bs": [
        #                 ["5541.20000", "1.52900000", "1534614248.765567"],
        #                 ["5539.90000", "0.30000000", "1534614241.769870"],
        #                 ["5539.50000", "5.00000000", "1534613831.243486"]
        #             ]
        #         },
        #         "book-10",
        #         "XBT/USD"
        #     ]
        #
        # subsequent updates
        #
        #     [
        #         1234,
        #         { # optional
        #             "a": [
        #                 ["5541.30000", "2.50700000", "1534614248.456738"],
        #                 ["5542.50000", "0.40100000", "1534614248.456738"]
        #             ]
        #         },
        #         { # optional
        #             "b": [
        #                 ["5541.30000", "0.00000000", "1534614335.345903"]
        #             ]
        #         },
        #         "book-10",
        #         "XBT/USD"
        #     ]
        #
        messageLength = len(message)
        wsName = message[messageLength - 1]
        market = self.safe_value(self.options['marketsByWsName'], wsName)
        symbol = market['symbol']
        timestamp = None
        messageHash = 'book:' + wsName
        # if self is a snapshot
        if 'as' in message[1]:
            # todo get depth from marketsByWsName
            self.orderbooks[symbol] = self.order_book({}, 10)
            orderbook = self.orderbooks[symbol]
            sides = {
                'as': 'asks',
                'bs': 'bids',
            }
            keys = list(sides.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                side = sides[key]
                bookside = orderbook[side]
                deltas = self.safe_value(message[1], key, [])
                timestamp = self.handle_deltas(bookside, deltas, timestamp)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            # the .limit() operation will be moved to the watchOrderBook
            client.resolve(orderbook, messageHash)
        else:
            orderbook = self.orderbooks[symbol]
            # else, if self is an orderbook update
            a = None
            b = None
            if messageLength == 5:
                a = self.safe_value(message[1], 'a', [])
                b = self.safe_value(message[2], 'b', [])
            else:
                if 'a' in message[1]:
                    a = self.safe_value(message[1], 'a', [])
                else:
                    b = self.safe_value(message[1], 'b', [])
            if a is not None:
                timestamp = self.handle_deltas(orderbook['asks'], a, timestamp)
            if b is not None:
                timestamp = self.handle_deltas(orderbook['bids'], b, timestamp)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
            # the .limit() operation will be moved to the watchOrderBook
            client.resolve(orderbook, messageHash)

    def handle_deltas(self, bookside, deltas, timestamp):
        for j in range(0, len(deltas)):
            delta = deltas[j]
            price = float(delta[0])
            amount = float(delta[1])
            timestamp = max(timestamp or 0, int(float(delta[2]) * 1000))
            bookside.store(price, amount)
        return timestamp

    def handle_system_status(self, client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified as handleStatus for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         connectionID: 15527282728335292000,
        #         event: 'systemStatus',
        #         status: 'online',  # online|maintenance|(custom status tbd)
        #         version: '0.2.0'
        #     }
        #
        return message

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         channelID: 210,
        #         channelName: 'book-10',
        #         event: 'subscriptionStatus',
        #         reqid: 1574146735269,
        #         pair: 'ETH/XBT',
        #         status: 'subscribed',
        #         subscription: {depth: 10, name: 'book'}
        #     }
        #
        channelId = self.safe_string(message, 'channelID')
        client.subscriptions[channelId] = message
        # requestId = self.safe_string(message, 'reqid')
        # if requestId in client.futures:
        #     del client.futures[requestId]
        # }

    def handle_error_message(self, client, message):
        #
        #     {
        #         errorMessage: 'Currency pair not in ISO 4217-A3 format foobar',
        #         event: 'subscriptionStatus',
        #         pair: 'foobar',
        #         reqid: 1574146735269,
        #         status: 'error',
        #         subscription: {name: 'ticker'}
        #     }
        #
        errorMessage = self.safe_value(message, 'errorMessage')
        if errorMessage is not None:
            requestId = self.safe_value(message, 'reqid')
            if requestId is not None:
                broad = self.exceptions['ws']['broad']
                broadKey = self.find_broadly_matched_key(broad, errorMessage)
                exception = None
                if broadKey is None:
                    exception = ExchangeError(errorMessage)
                else:
                    exception = broad[broadKey](errorMessage)
                # print(requestId, exception)
                client.reject(exception, requestId)
                # raise exception
                return False
        return True

    def sign_message(self, client, messageHash, message, params={}):
        # todo: kraken signMessage not implemented yet
        return message

    def handle_message(self, client, message):
        if isinstance(message, list):
            # todo: move self branch and the 'method' property – to the client.subscriptions
            channelId = str(message[0])
            subscriptionStatus = self.safe_value(client.subscriptions, channelId, {})
            subscription = self.safe_value(subscriptionStatus, 'subscription', {})
            name = self.safe_string(subscription, 'name')
            methods = {
                'book': self.handle_order_book,
                'ohlc': self.handle_ohlcv,
                'ticker': self.handle_ticker,
                'trade': self.handle_trades,
            }
            method = self.safe_value(methods, name)
            if method is None:
                return message
            else:
                return method(client, message)
        else:
            if self.handle_error_message(client, message):
                event = self.safe_string(message, 'event')
                methods = {
                    'heartbeat': self.handle_heartbeat,
                    'systemStatus': self.handle_system_status,
                    'subscriptionStatus': self.handle_subscription_status,
                }
                method = self.safe_value(methods, event)
                if method is None:
                    return message
                else:
                    return method(client, message)
