# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.base.exchange import Exchange
import ccxt.async_support as ccxt
from ccxtpro.base.cache import ArrayCache, ArrayCacheBySymbolById
import hashlib


class poloniex(Exchange, ccxt.poloniex):

    def describe(self):
        return self.deep_extend(super(poloniex, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchTrades': True,
                'watchOrderBook': True,
                'watchBalance': False,  # not implemented yet
                'watchOHLCV': False,  # missing on the exchange side
            },
            'urls': {
                'api': {
                    'ws': 'wss://api2.poloniex.com',
                },
            },
            'options': {
                'tradesLimit': 1000,
                'symbolsByOrderId': {},
            },
        })

    def handle_tickers(self, client, message):
        #
        #     [
        #         1002,
        #         null,
        #         [
        #             50,               # currency pair id
        #             '0.00663930',     # last trade price
        #             '0.00663924',     # lowest ask
        #             '0.00663009',     # highest bid
        #             '0.01591824',     # percent change in last 24 hours
        #             '176.03923205',   # 24h base volume
        #             '26490.59208176',  # 24h quote volume
        #             0,                # is frozen
        #             '0.00678580',     # highest price
        #             '0.00648216'      # lowest price
        #         ]
        #     ]
        #
        channelId = self.safe_string(message, 0)
        subscribed = self.safe_value(message, 1)
        if subscribed:
            # skip subscription confirmation
            return
        ticker = self.safe_value(message, 2)
        numericId = self.safe_string(ticker, 0)
        market = self.safe_value(self.options['marketsByNumericId'], numericId)
        if market is None:
            # todo handle market not found, reject corresponging futures
            return
        symbol = self.safe_string(market, 'symbol')
        timestamp = self.milliseconds()
        open = None
        change = None
        average = None
        last = self.safe_float(ticker, 1)
        relativeChange = self.safe_float(ticker, 4)
        if relativeChange != -1:
            open = last / self.sum(1, relativeChange)
            change = last - open
            average = self.sum(last, open) / 2
        result = {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 8),
            'low': self.safe_float(ticker, 9),
            'bid': self.safe_float(ticker, 3),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 2),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': relativeChange * 100,
            'average': average,
            'baseVolume': self.safe_float(ticker, 6),
            'quoteVolume': self.safe_float(ticker, 5),
            'info': ticker,
        }
        self.tickers[symbol] = result
        messageHash = channelId + ':' + numericId
        client.resolve(result, messageHash)

    async def subscribe_private(self, messageHash, subscription):
        channelId = '1000'
        url = self.urls['api']['ws']
        client = self.client(url)
        if not (channelId in client.subscriptions):
            self.spawn(self.fetch_and_cache_open_orders)
        nonce = self.nonce()
        payload = self.urlencode({'nonce': nonce})
        signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha512)
        subscribe = {
            'command': 'subscribe',
            'channel': channelId,
            'key': self.apiKey,
            'payload': payload,
            'sign': signature,
        }
        return await self.watch(url, messageHash, subscribe, channelId, subscription)

    async def watch_balance(self, params={}):
        self.check_required_credentials()
        await self.load_markets()
        url = self.urls['api']['ws']
        client = self.client(url)
        messageHash = 'balance'
        channelId = '1000'
        existingSubscription = self.safe_value(client.subscriptions, channelId, {})
        fetchedBalance = self.safe_value(existingSubscription, 'fetchedBalance', False)
        if not fetchedBalance:
            self.balance = await self.fetch_balance()
            existingSubscription['fetchedBalance'] = True
        return await self.subscribe_private(messageHash, existingSubscription)

    async def fetch_and_cache_open_orders(self):
        # a cancel order update does not give us very much information
        # about an order, we cache the information before receiving cancel updates
        openOrders = await self.fetch_open_orders()
        orders = self.orders
        symbolsByOrderId = self.safe_value(self.options, 'symbolsByOrderId', {})
        if orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            orders = ArrayCacheBySymbolById(limit)
            self.orders = orders
        for i in range(0, len(openOrders)):
            openOrder = openOrders[i]
            orders.append(openOrder)
            symbolsByOrderId[openOrder.id] = openOrder.symbol
        self.options['symbolsByOrderId'] = symbolsByOrderId

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.check_required_credentials()
        await self.load_markets()
        messageHash = 'orders'
        if symbol:
            marketId = self.market_id(symbol)
            messageHash = messageHash + ':' + marketId
        orders = await self.subscribe_private(messageHash, {})
        if self.newUpdates:
            limit = orders.getLimit()
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.check_required_credentials()
        await self.load_markets()
        messageHash = 'myTrades'
        if symbol:
            marketId = self.market_id(symbol)
            messageHash = messageHash + ':' + marketId
        trades = await self.subscribe_private(messageHash, {})
        if self.newUpdates:
            limit = trades.getLimit()
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit)

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        numericId = self.safe_string(market, 'numericId')
        channelId = '1002'
        messageHash = channelId + ':' + numericId
        url = self.urls['api']['ws']
        subscribe = {
            'command': 'subscribe',
            'channel': channelId,
        }
        return await self.watch(url, messageHash, subscribe, channelId)

    async def watch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        channelId = '1002'
        messageHash = channelId
        url = self.urls['api']['ws']
        subscribe = {
            'command': 'subscribe',
            'channel': channelId,
        }
        tickers = await self.watch(url, messageHash, subscribe, channelId)
        return self.filter_by_array(tickers, 'symbol', symbols)

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
        currenciesByNumericId = self.safe_value(self.options, 'marketsByNumericId')
        if (currenciesByNumericId is None) or reload:
            currenciesByNumericId = {}
            keys = list(self.currencies.keys())
            for i in range(0, len(keys)):
                currency = self.currencies[keys[i]]
                numericId = self.safe_string(currency, 'numericId')
                currenciesByNumericId[numericId] = currency
            self.options['currenciesByNumericId'] = currenciesByNumericId
        return markets

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        numericId = self.safe_string(market, 'numericId')
        messageHash = 'trades:' + numericId
        url = self.urls['api']['ws']
        subscribe = {
            'command': 'subscribe',
            'channel': numericId,
        }
        trades = await self.watch(url, messageHash, subscribe, numericId)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        numericId = self.safe_string(market, 'numericId')
        messageHash = 'orderbook:' + numericId
        url = self.urls['api']['ws']
        subscribe = {
            'command': 'subscribe',
            'channel': numericId,
        }
        orderbook = await self.watch(url, messageHash, subscribe, numericId)
        return orderbook.limit(limit)

    async def watch_heartbeat(self, params={}):
        await self.load_markets()
        channelId = '1010'
        url = self.urls['api']['ws']
        return await self.watch(url, channelId)

    def handle_heartbeat(self, client, message):
        #
        # every second(approx) if no other updates are sent
        #
        #     [1010]
        #
        channelId = '1010'
        client.resolve(message, channelId)

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
        id = self.safe_string(trade, 1)
        isBuy = self.safe_integer(trade, 2)
        side = 'buy' if isBuy else 'sell'
        price = self.safe_float(trade, 3)
        amount = self.safe_float(trade, 4)
        timestamp = self.safe_timestamp(trade, 5)
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

    def handle_order_book_and_trades(self, client, message):
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
        #             ["t", "42706057", 1, "0.05567134", "0.00181421", 1522877119]  # trade, id, side(1 for buy, 0 for sell), price, size, timestamp
        #         ]
        #     ]
        #
        marketId = str(message[0])
        nonce = message[1]
        data = message[2]
        market = self.safe_value(self.options['marketsByNumericId'], marketId)
        symbol = self.safe_string(market, 'symbol')
        orderbookUpdatesCount = 0
        tradesCount = 0
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        for i in range(0, len(data)):
            delta = data[i]
            if delta[0] == 'i':
                snapshot = self.safe_value(delta[1], 'orderBook', [])
                sides = ['asks', 'bids']
                self.orderbooks[symbol] = self.order_book()
                orderbook = self.orderbooks[symbol]
                for j in range(0, len(snapshot)):
                    side = sides[j]
                    bookside = orderbook[side]
                    orders = snapshot[j]
                    prices = list(orders.keys())
                    for k in range(0, len(prices)):
                        price = prices[k]
                        amount = orders[price]
                        bookside.store(float(price), float(amount))
                orderbook['nonce'] = nonce
                orderbookUpdatesCount = self.sum(orderbookUpdatesCount, 1)
            elif delta[0] == 'o':
                orderbook = self.orderbooks[symbol]
                side = 'bids' if delta[1] else 'asks'
                bookside = orderbook[side]
                price = float(delta[2])
                amount = float(delta[3])
                bookside.store(price, amount)
                orderbookUpdatesCount = self.sum(orderbookUpdatesCount, 1)
                orderbook['nonce'] = nonce
            elif delta[0] == 't':
                trade = self.handle_trade(client, delta, market)
                stored.append(trade)
                tradesCount = self.sum(tradesCount, 1)
        if orderbookUpdatesCount:
            # resolve the orderbook future
            messageHash = 'orderbook:' + marketId
            orderbook = self.orderbooks[symbol]
            client.resolve(orderbook, messageHash)
        if tradesCount:
            # resolve the trades future
            messageHash = 'trades:' + marketId
            # todo: incremental trades
            client.resolve(stored, messageHash)

    def handle_account_notifications(self, client, message):
        # [
        #   1000,
        #   '',
        #   [
        #     [
        #       'p',
        #       898860801559,
        #       121,
        #       '48402.31639500',
        #       '0.00004133',
        #       '0',
        #       null
        #     ],
        #     ['b', 28, 'e', '-0.00004133'],
        #     ['b', 214, 'e', '1.99915833'],
        #     [
        #       't',
        #       42365437,
        #       '48431.17368463',
        #       '0.00004133',
        #       '0.00125000',
        #       0,
        #       898860801559,
        #       '0.00242155',
        #       '2021-03-06 20:01:23',
        #       null,
        #       '0.00004133'
        #     ]
        #   ]
        # ]
        data = self.safe_value(message, 2, [])
        # order is important here
        methods = {
            'b': [self.handle_balance],
            'p': [self.handle_order, self.handle_balance],
            'n': [self.handle_order, self.handle_balance],
            'o': [self.handle_order, self.handle_balance],
            't': [self.handle_my_trade, self.handle_order, self.handle_balance],
        }
        for i in range(0, len(data)):
            entry = data[i]
            type = self.safe_string(entry, 0)
            callbacks = self.safe_value(methods, type)
            if isinstance(callbacks, list):
                for j in range(0, len(callbacks)):
                    callback = callbacks[j]
                    callback(client, entry)

    def handle_balance(self, client, message):
        #
        # balance update
        # ['b', 28, 'e', '-0.00004133']
        # ['b', 214, 'e', '1.99915833']
        #
        # pending
        # ['p', 6083059, 148, '48402.31639500', '0.00004133', '0', null]
        #
        # new order
        # ["n", 148, 6083059, 1, "0.03000000", "2.00000000", "2018-09-08 04:54:09", "2.00000000", "12345"]
        # ["n", <currency pair id>, <order number>, <order type>, "<rate>", "<amount>", "<date>", "<original amount ordered>" "<clientOrderId>"]
        #
        # order change
        # ['o', 899641758820, '0.00000000', 'c', null, '0.00001971']
        # ['o', 6083059, '1.50000000', 'f', '12345']
        #
        # ["o", <order number>, "<new amount>", "<order type>", "<clientOrderId>"]
        #
        # trade update
        #
        # ["t", 12345, "0.03000000", "0.50000000", "0.00250000", 0, 6083059, "0.00000375", "2018-09-08 05:54:09", "12345", "0.015"]
        #
        # ["t", <trade ID>, "<rate>", "<amount>", "<fee multiplier>", <funding type>, <order number>, <total fee>, <date>, "<clientOrderId>", "<trade total>"]
        #
        subscription = self.safe_value(client.subscriptions, '1000', {})
        fetchedBalance = self.safe_value(subscription, 'fetchedBalance', False)
        # to avoid synchronisation issues
        if not fetchedBalance:
            return
        messageHash = 'balance'
        messageType = self.safe_string(message, 0)
        if messageType == 'b':
            balanceType = self.safe_string(message, 2)
            if balanceType != 'e':
                # no support for poloniex futures atm
                return
            numericId = self.safe_string(message, 1)
            currency = self.safe_value(self.options['currenciesByNumericId'], numericId)
            if currency is None:
                return
            code = currency['code']
            changeAmount = self.safe_float(message, 3)
            self.balance[code]['free'] = self.sum(self.balance[code]['free'], changeAmount)
            self.balance[code]['total'] = None
            self.balance = self.parse_balance(self.balance)
        elif (messageType == 'o') or (messageType == 'p') or (messageType == 't') or (messageType == 'n'):
            symbol = None
            orderId = None
            if (messageType == 'o') or (messageType == 'p'):
                orderId = self.safe_string(message, 1)
                orderType = self.safe_string(message, 3)
                if (messageType == 'o') and (orderType == 'f'):
                    # we use the trades for the fills and the order events for the cancels
                    return
            elif messageType == 't':
                orderId = self.safe_string(message, 6)
            elif messageType == 'n':
                orderId = self.safe_string(message, 2)
            symbolsByOrderId = self.safe_value(self.options, 'symbolsByOrderId')
            symbol = self.safe_string(symbolsByOrderId, orderId)
            if not (symbol in self.markets):
                return
            market = self.market(symbol)
            previousOrders = self.safe_value(self.orders.hashmap, symbol, {})
            previousOrder = self.safe_value(previousOrders, orderId)
            quote = market['quote']
            changeAmount = None
            if messageType == 'n':
                changeAmount = previousOrder['filled']
            elif messageType == 'o':
                changeAmount = self.safe_float(message, 5)
            else:
                changeAmount = previousOrder['amount']
            quoteAmount = changeAmount * previousOrder['price']
            base = market['base']
            baseAmount = changeAmount
            orderAmount = None
            orderCode = None
            if previousOrder['side'] == 'buy':
                orderAmount = quoteAmount
                orderCode = quote
            else:
                orderAmount = baseAmount
                orderCode = base
            preciseAmount = self.amount_to_precision(symbol, orderAmount)
            floatAmount = float(preciseAmount)
            if (messageType == 'o') or (messageType == 't') or (messageType == 'n'):
                self.balance[orderCode]['used'] = self.balance[orderCode]['used'] - floatAmount
            else:
                self.balance[orderCode]['used'] = self.sum(self.balance[orderCode]['used'], floatAmount)
            self.balance[orderCode]['total'] = None
            self.balance = self.parse_balance(self.balance)
        client.resolve(self.balance, messageHash)

    def handle_order(self, client, message):
        #
        # pending
        # ['p', 6083059, 148, '48402.31639500', '0.00004133', '0', null],
        # ["p", <order number>, <currency pair id>, "<rate>", "<amount>", "<order type>", "<clientOrderId>"]
        #
        # new order
        # ["n", 148, 6083059, 1, "0.03000000", "2.00000000", "2018-09-08 04:54:09", "2.00000000", "12345"]
        # ["n", <currency pair id>, <order number>, <order type>, "<rate>", "<amount>", "<date>", "<original amount ordered>" "<clientOrderId>"]
        #
        # order change
        # ['o', 899641758820, '0.00000000', 'c', null, '0.00001971']
        # ['o', 6083059, '1.50000000', 'f', '12345']
        # ["o", <order number>, "<new amount>", "c", "<clientOrderId>", "<canceledAmount>"]
        #
        # trade change
        # ["t", 12345, "0.03000000", "0.50000000", "0.00250000", 0, 6083059, "0.00000375", "2018-09-08 05:54:09", "12345", "0.015"]
        # ["t", <trade ID>, "<rate>", "<amount>", "<fee multiplier>", <funding type>, <order number>, <total fee>, <date>, "<clientOrderId>", "<trade total>"]
        #
        # in the case of an n update, as corresponding t update is not sent, the code accounts for self
        #
        orders = self.orders
        limit = self.safe_integer(self.options, 'ordersLimit', 1000)
        symbolsByOrderId = self.safe_value(self.options, 'symbolsByOrderId', {})
        if orders is None:
            orders = ArrayCacheBySymbolById(limit)
            self.orders = orders
        length = len(orders)
        type = self.safe_string(message, 0)
        symbol = None
        if type == 'p':
            orderId = self.safe_string(message, 1)
            numericId = self.safe_string(message, 2)
            market = self.safe_value(self.options['marketsByNumericId'], numericId)
            if market is None:
                return None
            symbol = market['symbol']
            symbolsByOrderId[orderId] = symbol
            price = self.safe_float(message, 3)
            amount = self.safe_float(message, 4)
            orderType = self.safe_integer(message, 5)
            side = 'buy' if orderType else 'sell'
            clientOrderId = self.safe_string(message, 6)
            if length == limit:
                first = orders[0]
                if first['id'] in symbolsByOrderId:
                    del symbolsByOrderId[first['id']]
            orders.append({
                'info': message,
                'symbol': symbol,
                'id': orderId,
                'clientOrderId': clientOrderId,
                'timestamp': None,
                'datetime': None,
                'lastTradeTimestamp': None,
                'type': 'limit',
                'timeInForce': None,
                'postOnly': None,
                'side': side,
                'price': price,
                'stopPrice': None,
                'amount': amount,
                'cost': None,
                'average': None,
                'filled': None,
                'remaining': amount,
                'status': 'open',
                'fee': None,
                'trades': None,
            })
        elif type == 'n':
            numericId = self.safe_string(message, 1)
            market = self.safe_value(self.options['marketsByNumericId'], numericId)
            if market is None:
                return None
            symbol = market['symbol']
            orderId = self.safe_string(message, 2)
            orderType = self.safe_integer(message, 3)
            side = 'buy' if orderType else 'sell'
            price = self.safe_float(message, 4)
            remaining = self.safe_float(message, 5)
            date = self.safe_string(message, 6)
            timestamp = self.parse8601(date)
            amount = self.safe_float(message, 7)
            clientOrderId = self.safe_string(message, 8)
            filled = None
            cost = None
            if (amount is not None) and (remaining is not None):
                filled = amount - remaining
                cost = filled * price
            if length == limit:
                first = orders[0]
                if first['id'] in symbolsByOrderId:
                    del symbolsByOrderId[first['id']]
            orders.append({
                'info': message,
                'symbol': symbol,
                'id': orderId,
                'clientOrderId': clientOrderId,
                'timestamp': timestamp,
                'datetime': self.iso8601(timestamp),
                'lastTradeTimestamp': None,
                'type': 'limit',
                'timeInForce': None,
                'postOnly': None,
                'side': side,
                'price': price,
                'stopPrice': None,
                'amount': amount,
                'cost': cost,
                'average': None,
                'filled': filled,
                'remaining': remaining,
                'status': 'open',
                'fee': None,
                'trades': None,
            })
        elif type == 'o':
            orderId = self.safe_string(message, 1)
            orderType = self.safe_string(message, 3)
            if (orderType == 'c') or (orderType == 'k'):
                symbol = self.safe_string(symbolsByOrderId, orderId)
                previousOrders = self.safe_value(orders.hashmap, symbol, {})
                previousOrder = self.safe_value(previousOrders, orderId)
                if previousOrder is not None:
                    previousOrder['status'] = 'canceled'
        elif type == 't':
            trade = self.parse_ws_trade(message)
            orderId = self.safe_string(trade, 'order')
            symbol = self.safe_string(symbolsByOrderId, orderId)
            previousOrders = self.safe_value(orders.hashmap, symbol, {})
            previousOrder = self.safe_value(previousOrders, orderId)
            if previousOrder['trades'] is None:
                previousOrder['trades'] = []
            previousOrder['trades'].append(trade)
            filled = previousOrder['filled']
            if filled is None:
                filled = trade['amount']
            else:
                filled = previousOrder['filled'] + trade['amount']
            if previousOrder['amount'] is not None:
                previousOrder['remaining'] = max(previousOrder['amount'] - filled, 0.0)
                if previousOrder['remaining'] == 0.0:
                    previousOrder['status'] = 'closed'
            previousOrder['filled'] = filled
            previousOrder['cost'] = filled * previousOrder['price']
            if previousOrder['fee'] is None:
                previousOrder['fee'] = {
                    'currency': trade['fee']['currency'],
                    'cost': trade['fee']['cost'],
                }
            else:
                previousOrder['fee']['cost'] = self.sum(previousOrder['fee']['cost'], trade['fee']['cost'])
        messageHash = 'orders'
        client.resolve(orders, messageHash)
        symbolSpecificMessageHash = messageHash + ':' + symbol
        client.resolve(orders, symbolSpecificMessageHash)

    def handle_my_trade(self, client, message):
        #
        # ["t", 12345, "0.03000000", "0.50000000", "0.00250000", 0, 6083059, "0.00000375", "2018-09-08 05:54:09", "12345", "0.015"]
        # ["t", <trade ID>, "<rate>", "<amount>", "<fee multiplier>", <funding type>, <order number>, <total fee>, <date>, "<clientOrderId>", "<trade total>"]
        #
        # in the case of an n update, as corresponding t update is not sent, the code accounts for self
        # so it is possible to miss myTrade updates
        #
        trades = self.myTrades
        if trades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            trades = ArrayCacheBySymbolById(limit)
        orders = self.orders
        if orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            orders = ArrayCacheBySymbolById(limit)
            self.orders = orders
        parsed = self.parse_ws_trade(message)
        trades.append(parsed)
        messageHash = 'myTrades'
        client.resolve(trades, messageHash)
        symbolSpecificMessageHash = messageHash + ':' + parsed['symbol']
        client.resolve(trades, symbolSpecificMessageHash)

    def parse_ws_trade(self, trade):
        orders = self.orders
        tradeId = self.safe_string(trade, 1)
        price = self.safe_float(trade, 2)
        amount = self.safe_float(trade, 3)
        feeRate = self.safe_float(trade, 4)
        order = self.safe_string(trade, 6)
        feeCost = self.safe_float(trade, 7)
        date = self.safe_string(trade, 8)
        cost = self.safe_float(trade, 10)
        timestamp = self.parse8601(date)
        symbolsByOrderId = self.safe_value(self.options, 'symbolsByOrderId', {})
        symbol = self.safe_string(symbolsByOrderId, order)
        previousOrders = self.safe_value(orders.hashmap, symbol, {})
        previousOrder = self.safe_value(previousOrders, order)
        market = self.market(symbol)
        side = self.safe_string(previousOrder, 'side')
        feeCurrency = None
        if side == 'buy':
            feeCurrency = market['base']
        else:
            feeCurrency = market['quote']
        fee = {
            'cost': feeCost,
            'rate': feeRate,
            'currency': feeCurrency,
        }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': order,
            'type': 'limit',
            'takerOrMaker': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def handle_message(self, client, message):
        channelId = self.safe_string(message, 0)
        methods = {
            # '<numericId>': 'handleOrderBookAndTrades',  # Price Aggregated Book
            '1000': self.handle_account_notifications,  # Beta
            '1002': self.handle_tickers,  # Ticker Data
            # '1003': None,  # 24 Hour Exchange Volume
            '1010': self.handle_heartbeat,
        }
        method = self.safe_value(methods, channelId)
        if method is None:
            market = self.safe_value(self.options['marketsByNumericId'], channelId)
            if market is None:
                return message
            else:
                return self.handle_order_book_and_trades(client, message)
        else:
            method(client, message)
