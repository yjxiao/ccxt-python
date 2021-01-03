# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheBySymbolById
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class bitfinex(Exchange, ccxt.bitfinex):

    def describe(self):
        return self.deep_extend(super(bitfinex, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': False,
                'watchOrderBook': True,
                'watchTrades': True,
                'watchBalance': False,  # for now
                'watchOHLCV': False,  # missing on the exchange side in v1
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://api-pub.bitfinex.com/ws/1',
                        'private': 'wss://api.bitfinex.com/ws/1',
                    },
                },
            },
            'options': {
                'watchOrderBook': {
                    'prec': 'P0',
                    'freq': 'F0',
                },
                'ordersLimit': 1000,
            },
        })

    async def subscribe(self, channel, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        url = self.urls['api']['ws']['public']
        messageHash = channel + ':' + marketId
        # channel = 'trades'
        request = {
            'event': 'subscribe',
            'channel': channel,
            'symbol': marketId,
            'messageHash': messageHash,
        }
        return await self.watch(url, messageHash, self.deep_extend(request, params), messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        future = self.subscribe('trades', symbol, params)
        return await self.after(future, self.filter_by_since_limit, since, limit, 'timestamp', True)

    async def watch_ticker(self, symbol, params={}):
        return await self.subscribe('ticker', symbol, params)

    def handle_trades(self, client, message, subscription):
        #
        # initial snapshot
        #
        #     [
        #         2,
        #         [
        #             [null, 1580565020, 9374.9, 0.005],
        #             [null, 1580565004, 9374.9, 0.005],
        #             [null, 1580565003, 9374.9, 0.005],
        #         ]
        #     ]
        #
        # when a trade does not have an id yet
        #
        #     # channel id, update type, seq, time, price, amount
        #     [2, 'te', '28462857-BTCUSD', 1580565041, 9374.9, 0.005],
        #
        # when a trade already has an id
        #
        #     # channel id, update type, seq, trade id, time, price, amount
        #     [2, 'tu', '28462857-BTCUSD', 413357662, 1580565041, 9374.9, 0.005]
        #
        channel = self.safe_value(subscription, 'channel')
        marketId = self.safe_string(subscription, 'pair')
        messageHash = channel + ':' + marketId
        tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
            data = self.safe_value(message, 1)
            stored = self.safe_value(self.trades, symbol)
            if stored is None:
                stored = ArrayCache(tradesLimit)
                self.trades[symbol] = stored
            if isinstance(data, list):
                trades = self.parse_trades(data, market)
                for i in range(0, len(trades)):
                    stored.append(trades[i])
            else:
                second = self.safe_string(message, 1)
                if second != 'tu':
                    return
                trade = self.parse_trade(message, market)
                stored.append(trade)
            client.resolve(stored, messageHash)
        return message

    def parse_trade(self, trade, market=None):
        #
        # snapshot trade
        #
        #     # null, time, price, amount
        #     [null, 1580565020, 9374.9, 0.005],
        #
        # when a trade does not have an id yet
        #
        #     # channel id, update type, seq, time, price, amount
        #     [2, 'te', '28462857-BTCUSD', 1580565041, 9374.9, 0.005],
        #
        # when a trade already has an id
        #
        #     # channel id, update type, seq, trade id, time, price, amount
        #     [2, 'tu', '28462857-BTCUSD', 413357662, 1580565041, 9374.9, 0.005]
        #
        if not isinstance(trade, list):
            return super(bitfinex, self).parse_trade(trade, market)
        tradeLength = len(trade)
        event = self.safe_string(trade, 1)
        id = None
        if event == 'tu':
            id = self.safe_string(trade, tradeLength - 4)
        timestamp = self.safe_timestamp(trade, tradeLength - 3)
        price = self.safe_float(trade, tradeLength - 2)
        amount = self.safe_float(trade, tradeLength - 1)
        side = None
        if amount is not None:
            side = 'buy' if (amount > 0) else 'sell'
            amount = abs(amount)
        cost = None
        if (price is not None) and (amount is not None):
            cost = price * amount
        seq = self.safe_string(trade, 2)
        parts = seq.split('-')
        marketId = self.safe_string(parts, 1)
        if marketId is not None:
            marketId = marketId.replace('t', '')
        symbol = self.safe_symbol(marketId, market)
        takerOrMaker = None
        orderId = None
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def handle_ticker(self, client, message, subscription):
        #
        #     [
        #         2,             # 0 CHANNEL_ID integer Channel ID
        #         236.62,        # 1 BID float Price of last highest bid
        #         9.0029,        # 2 BID_SIZE float Size of the last highest bid
        #         236.88,        # 3 ASK float Price of last lowest ask
        #         7.1138,        # 4 ASK_SIZE float Size of the last lowest ask
        #         -1.02,         # 5 DAILY_CHANGE float Amount that the last price has changed since yesterday
        #         0,             # 6 DAILY_CHANGE_PERC float Amount that the price has changed expressed in percentage terms
        #         236.52,        # 7 LAST_PRICE float Price of the last trade.
        #         5191.36754297,  # 8 VOLUME float Daily volume
        #         250.01,        # 9 HIGH float Daily high
        #         220.05,        # 10 LOW float Daily low
        #     ]
        #
        timestamp = self.milliseconds()
        marketId = self.safe_string(subscription, 'pair')
        symbol = self.safe_symbol(marketId)
        channel = 'ticker'
        messageHash = channel + ':' + marketId
        last = self.safe_float(message, 7)
        change = self.safe_float(message, 5)
        open = None
        if (last is not None) and (change is not None):
            open = last - change
        result = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(message, 9),
            'low': self.safe_float(message, 10),
            'bid': self.safe_float(message, 1),
            'bidVolume': None,
            'ask': self.safe_float(message, 3),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': self.safe_float(message, 6),
            'average': None,
            'baseVolume': self.safe_float(message, 8),
            'quoteVolume': None,
            'info': message,
        }
        self.tickers[symbol] = result
        client.resolve(result, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        if limit is not None:
            if (limit != 25) and (limit != 100):
                raise ExchangeError(self.id + ' watchOrderBook limit argument must be None, 25 or 100')
        options = self.safe_value(self.options, 'watchOrderBook', {})
        prec = self.safe_string(options, 'prec', 'P0')
        freq = self.safe_string(options, 'freq', 'F0')
        request = {
            # 'event': 'subscribe',  # added in subscribe()
            # 'channel': channel,  # added in subscribe()
            # 'symbol': marketId,  # added in subscribe()
            'prec': prec,  # string, level of price aggregation, 'P0', 'P1', 'P2', 'P3', 'P4', default P0
            'freq': freq,  # string, frequency of updates 'F0' = realtime, 'F1' = 2 seconds, default is 'F0'
            'len': limit,  # string, number of price points, '25', '100', default = '25'
        }
        future = self.subscribe('book', symbol, self.deep_extend(request, params))
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def handle_order_book(self, client, message, subscription):
        #
        # first message(snapshot)
        #
        #     [
        #         18691,  # channel id
        #         [
        #             [7364.8, 10, 4.354802],  # price, count, size > 0 = bid
        #             [7364.7, 1, 0.00288831],
        #             [7364.3, 12, 0.048],
        #             [7364.9, 3, -0.42028976],  # price, count, size < 0 = ask
        #             [7365, 1, -0.25],
        #             [7365.5, 1, -0.00371937],
        #         ]
        #     ]
        #
        # subsequent updates
        #
        #     [
        #         30,     # channel id
        #         9339.9,  # price
        #         0,      # count
        #         -1,     # size > 0 = bid, size < 0 = ask
        #     ]
        #
        marketId = self.safe_string(subscription, 'pair')
        symbol = self.safe_symbol(marketId)
        channel = 'book'
        messageHash = channel + ':' + marketId
        prec = self.safe_string(subscription, 'prec', 'P0')
        isRaw = (prec == 'R0')
        # if it is an initial snapshot
        if isinstance(message[1], list):
            limit = self.safe_integer(subscription, 'len')
            if isRaw:
                # raw order books
                self.orderbooks[symbol] = self.indexed_order_book({}, limit)
            else:
                # P0, P1, P2, P3, P4
                self.orderbooks[symbol] = self.counted_order_book({}, limit)
            orderbook = self.orderbooks[symbol]
            if isRaw:
                deltas = message[1]
                for i in range(0, len(deltas)):
                    delta = deltas[i]
                    id = self.safe_string(delta, 0)
                    price = self.safe_float(delta, 1)
                    size = -delta[2] if (delta[2] < 0) else delta[2]
                    side = 'asks' if (delta[2] < 0) else 'bids'
                    bookside = orderbook[side]
                    bookside.store(price, size, id)
            else:
                deltas = message[1]
                for i in range(0, len(deltas)):
                    delta = deltas[i]
                    size = -delta[2] if (delta[2] < 0) else delta[2]
                    side = 'asks' if (delta[2] < 0) else 'bids'
                    bookside = orderbook[side]
                    bookside.store(delta[0], size, delta[1])
            client.resolve(orderbook, messageHash)
        else:
            orderbook = self.orderbooks[symbol]
            if isRaw:
                id = self.safe_string(message, 1)
                price = self.safe_float(message, 2)
                size = -message[3] if (message[3] < 0) else message[3]
                side = 'asks' if (message[3] < 0) else 'bids'
                bookside = orderbook[side]
                # price = 0 means that you have to remove the order from your book
                amount = size if (price > 0) else 0
                bookside.store(price, amount, id)
            else:
                size = -message[3] if (message[3] < 0) else message[3]
                side = 'asks' if (message[3] < 0) else 'bids'
                bookside = orderbook[side]
                bookside.store(message[1], size, message[2])
            client.resolve(orderbook, messageHash)

    def handle_heartbeat(self, client, message):
        #
        # every second(approx) if no other updates are sent
        #
        #     {"event": "heartbeat"}
        #
        event = self.safe_string(message, 'event')
        client.resolve(message, event)

    def handle_system_status(self, client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified as handleStatus for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         event: 'info',
        #         version: 2,
        #         serverId: 'e293377e-7bb7-427e-b28c-5db045b2c1d1',
        #         platform: {status: 1},  # 1 for operative, 0 for maintenance
        #     }
        #
        return message

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         event: 'subscribed',
        #         channel: 'book',
        #         chanId: 67473,
        #         symbol: 'tBTCUSD',
        #         prec: 'P0',
        #         freq: 'F0',
        #         len: '25',
        #         pair: 'BTCUSD'
        #     }
        #
        channelId = self.safe_string(message, 'chanId')
        client.subscriptions[channelId] = message
        return message

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']['private']
        client = self.client(url)
        future = client.future('authenticated')
        method = 'auth'
        authenticated = self.safe_value(client.subscriptions, method)
        if authenticated is None:
            nonce = self.milliseconds()
            payload = 'AUTH' + str(nonce)
            signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha384, 'hex')
            request = {
                'apiKey': self.apiKey,
                'authSig': signature,
                'authNonce': nonce,
                'authPayload': payload,
                'event': method,
                'filter': [
                    'trading',
                    'wallet',
                ],
            }
            self.spawn(self.watch, url, method, request, 1)
        return await future

    def handle_authentication_message(self, client, message):
        status = self.safe_string(message, 'status')
        if status == 'OK':
            # we resolve the future here permanently so authentication only happens once
            future = self.safe_value(client.futures, 'authenticated')
            future.resolve(True)
        else:
            error = AuthenticationError(self.json(message))
            client.reject(error, 'authenticated')
            # allows further authentication attempts
            method = self.safe_string(message, 'event')
            if method in client.subscriptions:
                del client.subscriptions[method]

    async def watch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        url = self.urls['api']['ws']['private']
        future = self.authenticate()
        return await self.after_dropped(future, self.watch, url, id, None, 1)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        future = self.authenticate()
        url = self.urls['api']['ws']['private']
        watching = self.after_dropped(future, self.watch, url, 'os', None, 1)
        # purgeOrders here
        return await self.after(watching, self.filter_by_symbol_since_limit, symbol, since, limit)

    def handle_orders(self, client, message):
        #
        # order snapshot
        #
        #     [
        #         0,
        #         'os',
        #         [
        #             [
        #                 45287766631,
        #                 'ETHUST',
        #                 -0.07,
        #                 -0.07,
        #                 'EXCHANGE LIMIT',
        #                 'ACTIVE',
        #                 210,
        #                 0,
        #                 '2020-05-16T13:17:46Z',
        #                 0,
        #                 0,
        #                 0
        #             ]
        #         ]
        #     ]
        #
        # order cancel
        #
        #     [
        #         0,
        #         'oc',
        #         [
        #             45287766631,
        #             'ETHUST',
        #             -0.07,
        #             -0.07,
        #             'EXCHANGE LIMIT',
        #             'CANCELED',
        #             210,
        #             0,
        #             '2020-05-16T13:17:46Z',
        #             0,
        #             0,
        #             0,
        #         ]
        #     ]
        #
        data = self.safe_value(message, 2, [])
        messageType = self.safe_string(message, 1)
        if messageType == 'os':
            for i in range(0, len(data)):
                value = data[i]
                self.handle_order(client, value)
        else:
            self.handle_order(client, data)
        if self.orders is not None:
            client.resolve(self.orders, 'os')

    def parse_ws_order_status(self, status):
        statuses = {
            'ACTIVE': 'open',
            'CANCELED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def handle_order(self, client, order):
        # [45287766631,
        #     'ETHUST',
        #     -0.07,
        #     -0.07,
        #     'EXCHANGE LIMIT',
        #     'CANCELED',
        #     210,
        #     0,
        #     '2020-05-16T13:17:46Z',
        #     0,
        #     0,
        #     0]
        id = self.safe_string(order, 0)
        marketId = self.safe_string(order, 1)
        symbol = self.safe_symbol(marketId)
        amount = self.safe_float(order, 2)
        remaining = self.safe_float(order, 3)
        side = 'buy'
        if amount < 0:
            amount = abs(amount)
            remaining = abs(remaining)
            side = 'sell'
        type = self.safe_string(order, 4)
        if type.find('LIMIT') > -1:
            type = 'limit'
        elif type.find('MARKET') > -1:
            type = 'market'
        status = self.parse_ws_order_status(self.safe_string(order, 5))
        price = self.safe_float(order, 6)
        rawDatetime = self.safe_string(order, 8)
        timestamp = self.parse8601(rawDatetime)
        parsed = {
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'stopPrice': None,
            'average': None,
            'amount': amount,
            'remaining': remaining,
            'filled': amount - remaining,
            'status': status,
            'fee': None,
            'cost': None,
            'trades': None,
        }
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        orders.append(parsed)
        client.resolve(parsed, id)
        return parsed

    def handle_message(self, client, message):
        if isinstance(message, list):
            channelId = self.safe_string(message, 0)
            #
            #     [
            #         1231,
            #         'hb',
            #     ]
            #
            if message[1] == 'hb':
                return message  # skip heartbeats within subscription channels for now
            subscription = self.safe_value(client.subscriptions, channelId, {})
            channel = self.safe_string(subscription, 'channel')
            name = self.safe_string(message, 1)
            methods = {
                'book': self.handle_order_book,
                # 'ohlc': self.handleOHLCV,
                'ticker': self.handle_ticker,
                'trades': self.handle_trades,
                'os': self.handle_orders,
                'on': self.handle_orders,
                'oc': self.handle_orders,
            }
            method = self.safe_value_2(methods, channel, name)
            if method is None:
                return message
            else:
                return method(client, message, subscription)
        else:
            # todo add bitfinex handleErrorMessage
            #
            #     {
            #         event: 'info',
            #         version: 2,
            #         serverId: 'e293377e-7bb7-427e-b28c-5db045b2c1d1',
            #         platform: {status: 1},  # 1 for operative, 0 for maintenance
            #     }
            #
            event = self.safe_string(message, 'event')
            if event is not None:
                methods = {
                    'info': self.handle_system_status,
                    # 'book': 'handleOrderBook',
                    'subscribed': self.handle_subscription_status,
                    'auth': self.handle_authentication_message,
                }
                method = self.safe_value(methods, event)
                if method is None:
                    return message
                else:
                    return method(client, message)
