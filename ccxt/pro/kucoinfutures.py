# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.pro.base.exchange import Exchange
import ccxt.async_support
from ccxt.pro.base.cache import ArrayCache, ArrayCacheBySymbolById
from ccxt.base.errors import ExchangeError


class kucoinfutures(Exchange, ccxt.async_support.kucoinfutures):

    def describe(self):
        return self.deep_extend(super(kucoinfutures, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTrades': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchBalance': True,
            },
            'options': {
                'accountsByType': {
                    'swap': 'future',
                    'cross': 'margin',
                    # 'spot': ,
                    # 'margin': ,
                    # 'main': ,
                    # 'funding': ,
                    # 'future': ,
                    # 'mining': ,
                    # 'trade': ,
                    # 'contract': ,
                    # 'pool': ,
                },
                'tradesLimit': 1000,
                'watchOrderBook': {
                    'snapshotDelay': 20,
                    'maxRetries': 3,
                },
                'watchTicker': {
                    'name': 'contractMarket/tickerV2',  # market/ticker
                },
            },
            'streaming': {
                # kucoin does not support built-in ws protocol-level ping-pong
                # instead it requires a custom json-based text ping-pong
                # https://docs.kucoin.com/#ping
                'ping': self.ping,
            },
        })

    def negotiate(self, privateChannel, params={}):
        connectId = 'private' if privateChannel else 'public'
        urls = self.safe_value(self.options, 'urls', {})
        if connectId in urls:
            return urls[connectId]
        # we store an awaitable to the url
        # so that multiple calls don't asynchronously
        # fetch different urls and overwrite each other
        urls[connectId] = self.spawn(self.negotiate_helper, privateChannel, params)
        self.options['urls'] = urls
        return urls[connectId]

    async def negotiate_helper(self, privateChannel, params={}):
        response = None
        connectId = 'private' if privateChannel else 'public'
        if privateChannel:
            response = await self.futuresPrivatePostBulletPrivate(params)
            #
            #     {
            #         code: "200000",
            #         data: {
            #             instanceServers: [
            #                 {
            #                     pingInterval:  50000,
            #                     endpoint: "wss://push-private.kucoin.com/endpoint",
            #                     protocol: "websocket",
            #                     encrypt: True,
            #                     pingTimeout: 10000
            #                 }
            #             ],
            #             token: "2neAiuYvAU61ZDXANAGAsiL4-iAExhsBXZxftpOeh_55i3Ysy2q2LEsEWU64mdzUOPusi34M_wGoSf7iNyEWJ1UQy47YbpY4zVdzilNP-Bj3iXzrjjGlWtiYB9J6i9GjsxUuhPw3BlrzazF6ghq4Lzf7scStOz3KkxjwpsOBCH4=.WNQmhZQeUKIkh97KYgU0Lg=="
            #         }
            #     }
            #
        else:
            response = await self.futuresPublicPostBulletPublic(params)
        data = self.safe_value(response, 'data', {})
        instanceServers = self.safe_value(data, 'instanceServers', [])
        firstInstanceServer = self.safe_value(instanceServers, 0)
        pingInterval = self.safe_integer(firstInstanceServer, 'pingInterval')
        endpoint = self.safe_string(firstInstanceServer, 'endpoint')
        token = self.safe_string(data, 'token')
        result = endpoint + '?' + self.urlencode({
            'token': token,
            'privateChannel': privateChannel,
            'connectId': connectId,
        })
        client = self.client(result)
        client.keepAlive = pingInterval
        return result

    def request_id(self):
        requestId = self.sum(self.safe_integer(self.options, 'requestId', 0), 1)
        self.options['requestId'] = requestId
        return requestId

    async def subscribe(self, url, messageHash, subscriptionHash, subscription, params={}):
        requestId = str(self.request_id())
        request = {
            'id': requestId,
            'type': 'subscribe',
            'topic': subscriptionHash,
            'response': True,
        }
        message = self.extend(request, params)
        subscriptionRequest = {
            'id': requestId,
        }
        if subscription is None:
            subscription = subscriptionRequest
        else:
            subscription = self.extend(subscriptionRequest, subscription)
        return await self.watch(url, messageHash, message, subscriptionHash, subscription)

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        see https://docs.kucoin.com/futures/#get-real-time-symbol-ticker-v2
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the kucoinfutures api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = await self.negotiate(False)
        options = self.safe_value(self.options, 'watchTicker', {})
        channel = self.safe_string(options, 'name', 'contractMarket/tickerV2')
        topic = '/' + channel + ':' + market['id']
        messageHash = 'ticker:' + symbol
        return await self.subscribe(url, messageHash, topic, None, params)

    def handle_ticker(self, client, message):
        #
        # market/tickerV2
        #
        #    {
        #        type: 'message',
        #        topic: '/contractMarket/tickerV2:ADAUSDTM',
        #        subject: 'tickerV2',
        #        data: {
        #            symbol: 'ADAUSDTM',
        #            sequence: 1668007800439,
        #            bestBidSize: 178,
        #            bestBidPrice: '0.35959',
        #            bestAskPrice: '0.35981',
        #            ts: '1668141430037124460',
        #            bestAskSize: 134
        #        }
        #    }
        #
        data = self.safe_value(message, 'data', {})
        marketId = self.safe_value(data, 'symbol')
        market = self.safe_market(marketId, None, '-')
        ticker = self.parse_ticker(data, market)
        self.tickers[market['symbol']] = ticker
        messageHash = 'ticker:' + market['symbol']
        client.resolve(ticker, messageHash)
        return message

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        see https://docs.kucoin.com/futures/#execution-data
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the kucoinfutures api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        url = await self.negotiate(False)
        market = self.market(symbol)
        symbol = market['symbol']
        topic = '/contractMarket/execution:' + market['id']
        messageHash = 'trades:' + symbol
        trades = await self.subscribe(url, messageHash, topic, None, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trade(self, client, message):
        #
        #    {
        #        type: 'message',
        #        topic: '/contractMarket/execution:ADAUSDTM',
        #        subject: 'match',
        #        data: {
        #            makerUserId: '62286a4d720edf0001e81961',
        #            symbol: 'ADAUSDTM',
        #            sequence: 41320766,
        #            side: 'sell',
        #            size: 2,
        #            price: 0.35904,
        #            takerOrderId: '636dd9da9857ba00010cfa44',
        #            makerOrderId: '636dd9c8df149d0001e62bc8',
        #            takerUserId: '6180be22b6ab210001fa3371',
        #            tradeId: '636dd9da0000d400d477eca7',
        #            ts: 1668143578987357700
        #        }
        #    }
        #
        data = self.safe_value(message, 'data', {})
        trade = self.parse_trade(data)
        symbol = trade['symbol']
        trades = self.safe_value(self.trades, symbol)
        if trades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            trades = ArrayCache(limit)
            self.trades[symbol] = trades
        trades.append(trade)
        messageHash = 'trades:' + symbol
        client.resolve(trades, messageHash)
        return message

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
         *   1. After receiving the websocket Level 2 data flow, cache the data.
         *   2. Initiate a REST request to get the snapshot data of Level 2 order book.
         *   3. Playback the cached Level 2 data flow.
         *   4. Apply the new Level 2 data flow to the local snapshot to ensure that the sequence of the new Level 2 update lines up with the sequence of the previous Level 2 data. Discard all the message prior to that sequence, and then playback the change to snapshot.
         *   5. Update the level2 full data based on sequence according to the size. If the price is 0, ignore the messages and update the sequence. If the size=0, update the sequence and remove the price of which the size is 0 out of level 2. For other cases, please update the price.
         *   6. If the sequence of the newly pushed message does not line up to the sequence of the last message, you could pull through REST Level 2 message request to get the updated messages. Please note that the difference between the start and end parameters cannot exceed 500.
        see https://docs.kucoin.com/futures/#level-2-market-data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the kucoinfutures api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        if limit is not None:
            if (limit != 20) and (limit != 100):
                raise ExchangeError(self.id + " watchOrderBook 'limit' argument must be None, 20 or 100")
        await self.load_markets()
        url = await self.negotiate(False)
        market = self.market(symbol)
        symbol = market['symbol']
        topic = '/contractMarket/level2:' + market['id']
        messageHash = 'orderbook:' + symbol
        subscription = {
            'method': self.handle_order_book_subscription,
            'symbol': symbol,
            'limit': limit,
        }
        orderbook = await self.subscribe(url, messageHash, topic, subscription, params)
        return orderbook.limit()

    def handle_delta(self, orderbook, delta):
        orderbook['nonce'] = self.safe_integer(delta, 'sequence')
        timestamp = self.safe_integer(delta, 'timestamp')
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        change = self.safe_value(delta, 'change', {})
        splitChange = change.split(',')
        price = self.safe_number(splitChange, 0)
        side = self.safe_string(splitChange, 1)
        quantity = self.safe_number(splitChange, 2)
        type = 'bids' if (side == 'buy') else 'asks'
        value = [price, quantity]
        if type == 'bids':
            storedBids = orderbook['bids']
            storedBids.storeArray(value)
        else:
            storedAsks = orderbook['asks']
            storedAsks.storeArray(value)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book(self, client, message):
        #
        # initial snapshot is fetched with ccxt's fetchOrderBook
        # the feed does not include a snapshot, just the deltas
        #
        #    {
        #        type: 'message',
        #        topic: '/contractMarket/level2:ADAUSDTM',
        #        subject: 'level2',
        #        data: {
        #            sequence: 1668059586457,
        #            change: '0.34172,sell,456',  # type, side, quantity
        #            timestamp: 1668573023223
        #        }
        #    }
        #
        data = self.safe_value(message, 'data')
        topic = self.safe_string(message, 'topic')
        topicParts = topic.split(':')
        marketId = self.safe_string(topicParts, 1)
        symbol = self.safe_symbol(marketId, None, '-')
        messageHash = 'orderbook:' + symbol
        storedOrderBook = self.orderbooks[symbol]
        nonce = self.safe_integer(storedOrderBook, 'nonce')
        deltaEnd = self.safe_integer(data, 'sequence')
        if nonce is None:
            cacheLength = len(storedOrderBook.cache)
            topic = self.safe_string(message, 'topic')
            subscription = client.subscriptions[topic]
            limit = self.safe_integer(subscription, 'limit')
            snapshotDelay = self.handle_option('watchOrderBook', 'snapshotDelay', 5)
            if cacheLength == snapshotDelay:
                self.spawn(self.load_order_book, client, messageHash, symbol, limit)
            storedOrderBook.cache.append(data)
            return
        elif nonce >= deltaEnd:
            return
        self.handle_delta(storedOrderBook, data)
        client.resolve(storedOrderBook, messageHash)

    def get_cache_index(self, orderbook, cache):
        firstDelta = self.safe_value(cache, 0)
        nonce = self.safe_integer(orderbook, 'nonce')
        firstDeltaStart = self.safe_integer(firstDelta, 'sequence')
        if nonce < firstDeltaStart - 1:
            return -1
        for i in range(0, len(cache)):
            delta = cache[i]
            deltaStart = self.safe_integer(delta, 'sequence')
            if nonce < deltaStart - 1:
                return i
        return len(cache)

    def handle_order_book_subscription(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_integer(subscription, 'limit')
        self.orderbooks[symbol] = self.order_book({}, limit)
        # moved snapshot initialization to handleOrderBook to fix
        # https://github.com/ccxt/ccxt/issues/6820
        # the general idea is to fetch the snapshot after the first delta
        # but not before, because otherwise we cannot synchronize the feed

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         id: '1578090438322',
        #         type: 'ack'
        #     }
        #
        id = self.safe_string(message, 'id')
        subscriptionsById = self.index_by(client.subscriptions, 'id')
        subscription = self.safe_value(subscriptionsById, id, {})
        method = self.safe_value(subscription, 'method')
        if method is not None:
            method(client, message, subscription)
        return message

    def handle_system_status(self, client, message):
        #
        # todo: answer the question whether handleSystemStatus should be renamed
        # and unified as handleStatus for any usage pattern that
        # involves system status and maintenance updates
        #
        #     {
        #         id: '1578090234088',  # connectId
        #         type: 'welcome',
        #     }
        #
        return message

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple orders made by the user
        see https://docs.kucoin.com/futures/#trade-orders-according-to-the-market
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the kucoinfutures api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        url = await self.negotiate(True)
        topic = '/contractMarket/tradeOrders'
        request = {
            'privateChannel': True,
        }
        messageHash = 'orders'
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            messageHash = messageHash + ':' + symbol
        orders = await self.subscribe(url, messageHash, topic, None, self.extend(request, params))
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def parse_ws_order_status(self, status):
        statuses = {
            'open': 'open',
            'filled': 'closed',
            'match': 'open',
            'update': 'open',
            'canceled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_ws_order(self, order, market=None):
        #
        #     {
        #         'symbol': 'XCAD-USDT',
        #         'orderType': 'limit',
        #         'side': 'buy',
        #         'orderId': '6249167327218b000135e749',
        #         'type': 'canceled',
        #         'orderTime': 1648957043065280224,
        #         'size': '100.452',
        #         'filledSize': '0',
        #         'price': '2.9635',
        #         'clientOid': 'buy-XCAD-USDT-1648957043010159',
        #         'remainSize': '0',
        #         'status': 'done',
        #         'ts': 1648957054031001037
        #     }
        #
        id = self.safe_string(order, 'orderId')
        clientOrderId = self.safe_string(order, 'clientOid')
        orderType = self.safe_string_lower(order, 'orderType')
        price = self.safe_string(order, 'price')
        filled = self.safe_string(order, 'filledSize')
        amount = self.safe_string(order, 'size')
        rawType = self.safe_string(order, 'type')
        status = self.parse_ws_order_status(rawType)
        timestamp = self.safe_integer_product(order, 'orderTime', 0.000001)
        marketId = self.safe_string(order, 'symbol')
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        side = self.safe_string_lower(order, 'side')
        return self.safe_order({
            'info': order,
            'symbol': symbol,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'type': orderType,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'amount': amount,
            'cost': None,
            'average': None,
            'filled': filled,
            'remaining': None,
            'status': status,
            'fee': None,
            'trades': None,
        }, market)

    def handle_order(self, client, message):
        messageHash = 'orders'
        data = self.safe_value(message, 'data')
        parsed = self.parse_ws_order(data)
        symbol = self.safe_string(parsed, 'symbol')
        orderId = self.safe_string(parsed, 'id')
        if symbol is not None:
            if self.orders is None:
                limit = self.safe_integer(self.options, 'ordersLimit', 1000)
                self.orders = ArrayCacheBySymbolById(limit)
            cachedOrders = self.orders
            orders = self.safe_value(cachedOrders.hashmap, symbol, {})
            order = self.safe_value(orders, orderId)
            if order is not None:
                # todo add others to calculate average etc
                stopPrice = self.safe_value(order, 'stopPrice')
                if stopPrice is not None:
                    parsed['stopPrice'] = stopPrice
                if order['status'] == 'closed':
                    parsed['status'] = 'closed'
            cachedOrders.append(parsed)
            client.resolve(self.orders, messageHash)
            symbolSpecificMessageHash = messageHash + ':' + symbol
            client.resolve(self.orders, symbolSpecificMessageHash)

    async def watch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        see https://docs.kucoin.com/futures/#account-balance-events
        :param dict params: extra parameters specific to the kucoinfutures api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        url = await self.negotiate(True)
        topic = '/contractAccount/wallet'
        request = {
            'privateChannel': True,
        }
        subscription = {
            'method': self.handle_balance_subscription,
        }
        messageHash = 'balance'
        return await self.subscribe(url, messageHash, topic, subscription, self.extend(request, params))

    def handle_balance(self, client, message):
        #
        #    {
        #        id: '6375553193027a0001f6566f',
        #        type: 'message',
        #        topic: '/contractAccount/wallet',
        #        userId: '613a896885d8660006151f01',
        #        channelType: 'private',
        #        subject: 'availableBalance.change',
        #        data: {
        #            currency: 'USDT',
        #            holdBalance: '0.0000000000',
        #            availableBalance: '14.0350281903',
        #            timestamp: '1668633905657'
        #        }
        #    }
        #
        data = self.safe_value(message, 'data', {})
        self.balance['info'] = data
        currencyId = self.safe_string(data, 'currency')
        code = self.safe_currency_code(currencyId)
        account = self.account()
        account['free'] = self.safe_string(data, 'availableBalance')
        account['used'] = self.safe_string(data, 'holdBalance')
        self.balance[code] = account
        self.balance = self.safe_balance(self.balance)
        client.resolve(self.balance, 'balance')

    def handle_balance_subscription(self, client, message, subscription):
        self.spawn(self.fetch_balance_snapshot, client, message)

    async def fetch_balance_snapshot(self, client, message):
        await self.load_markets()
        self.check_required_credentials()
        messageHash = 'balance'
        selectedType = self.safe_string_2(self.options, 'watchBalance', 'defaultType', 'swap')  # spot, margin, main, funding, future, mining, trade, contract, pool
        params = {
            'type': selectedType,
        }
        snapshot = await self.fetch_balance(params)
        #
        #    {
        #        info: {
        #            code: '200000',
        #            data: {
        #                accountEquity: 0.0350281903,
        #                unrealisedPNL: 0,
        #                marginBalance: 0.0350281903,
        #                positionMargin: 0,
        #                orderMargin: 0,
        #                frozenFunds: 0,
        #                availableBalance: 0.0350281903,
        #                currency: 'USDT'
        #            }
        #        },
        #        timestamp: None,
        #        datetime: None,
        #        USDT: {
        #            free: 0.0350281903,
        #            used: 0,
        #            total: 0.0350281903
        #        },
        #        free: {
        #            USDT: 0.0350281903
        #        },
        #        used: {
        #            USDT: 0
        #        },
        #        total: {
        #            USDT: 0.0350281903
        #        }
        #    }
        #
        keys = list(snapshot.keys())
        for i in range(0, len(keys)):
            code = keys[i]
            if code != 'free' and code != 'used' and code != 'total' and code != 'timestamp' and code != 'datetime' and code != 'info':
                self.balance[code] = snapshot[code]
        self.balance['info'] = self.safe_value(snapshot, 'info', {})
        client.resolve(self.balance, messageHash)

    def handle_subject(self, client, message):
        #
        #    {
        #        type: 'message',
        #        topic: '/contractMarket/level2:ADAUSDTM',
        #        subject: 'level2',
        #        data: {
        #            sequence: 1668059586457,
        #            change: '0.34172,sell,456',  # type, side, quantity
        #            timestamp: 1668573023223
        #        }
        #    }
        #
        subject = self.safe_string(message, 'subject')
        methods = {
            'level2': self.handle_order_book,
            'tickerV2': self.handle_ticker,
            'availableBalance.change': self.handle_balance,
            'match': self.handle_trade,
            'orderChange': self.handle_order,
            'orderUpdated': self.handle_order,
        }
        method = self.safe_value(methods, subject)
        if method is None:
            return message
        else:
            return method(client, message)

    def ping(self, client):
        # kucoin does not support built-in ws protocol-level ping-pong
        # instead it requires a custom json-based text ping-pong
        # https://docs.kucoin.com/#ping
        id = str(self.request_id())
        return {
            'id': id,
            'type': 'ping',
        }

    def handle_pong(self, client, message):
        # https://docs.kucoin.com/#ping
        client.lastPong = self.milliseconds()
        return message

    def handle_error_message(self, client, message):
        return message

    def handle_message(self, client, message):
        if self.handle_error_message(client, message):
            type = self.safe_string(message, 'type')
            methods = {
                # 'heartbeat': self.handleHeartbeat,
                'welcome': self.handle_system_status,
                'ack': self.handle_subscription_status,
                'message': self.handle_subject,
                'pong': self.handle_pong,
            }
            method = self.safe_value(methods, type)
            if method is None:
                return message
            else:
                return method(client, message)
