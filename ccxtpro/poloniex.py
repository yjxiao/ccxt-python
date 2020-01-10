# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt
import hashlib


class poloniex(ccxtpro.Exchange, ccxt.poloniex):

    def describe(self):
        return self.deep_extend(super(poloniex, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchOrderBook': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api2.poloniex.com',
                },
            },
        })

    def handle_tickers(self, client, response):
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

    async def watch_balance(self, params={}):
        await self.load_markets()
        self.balance = await self.fetchBalance(params)
        channelId = '1000'
        subscribe = {
            'command': 'subscribe',
            'channel': channelId,
        }
        messageHash = channelId + ':b:e'
        url = self.urls['api']['ws']
        return await self.watch(url, messageHash, subscribe, channelId)

    async def watch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        # rewrite
        raise NotImplemented(self.id + 'watchTickers not implemented yet')
        # market = self.market(symbol)
        # numericId = str(market['info']['id'])
        # url = self.urls['api']['websocket']['public']
        # return await self.WsTickerMessage(url, '1002' + numericId, {
        #     'command': 'subscribe',
        #     'channel': 1002,
        # })

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

    async def watch_trades(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        numericId = self.safe_string(market, 'numericId')
        messageHash = 'trades:' + numericId
        url = self.urls['api']['ws']
        subscribe = {
            'command': 'subscribe',
            'channel': numericId,
        }
        return await self.watch(url, messageHash, subscribe, numericId)

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
        future = self.watch(url, messageHash, subscribe, numericId)
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def limit_order_book(self, orderbook, symbol, limit=None, params={}):
        return orderbook.limit(limit)

    async def watch_heartbeat(self, params={}):
        await self.load_markets()
        channelId = '1010'
        url = self.urls['api']['ws']
        return await self.watch(url, channelId)

    def sign_message(self, client, messageHash, message, params={}):
        if messageHash.find('1000') == 0:
            throwOnError = False
            if self.check_required_credentials(throwOnError):
                nonce = self.nonce()
                payload = self.urlencode({'nonce': nonce})
                signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha512)
                message = self.extend(message, {
                    'key': self.apiKey,
                    'payload': payload,
                    'sign': signature,
                })
        return message

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
                orderbookUpdatesCount += 1
            elif delta[0] == 'o':
                orderbook = self.orderbooks[symbol]
                side = 'bids' if delta[1] else 'asks'
                bookside = orderbook[side]
                price = float(delta[2])
                amount = float(delta[3])
                bookside.store(price, amount)
                orderbookUpdatesCount += 1
            elif delta[0] == 't':
                # todo: add max limit to the dequeue of trades, unshift and push
                trade = self.handle_trade(client, delta, market)
                self.trades.append(trade)
                tradesCount += 1
        if orderbookUpdatesCount:
            # resolve the orderbook future
            messageHash = 'orderbook:' + marketId
            orderbook = self.orderbooks[symbol]
            # the .limit() operation will be moved to the watchOrderBook
            client.resolve(orderbook, messageHash)
        if tradesCount:
            # resolve the trades future
            messageHash = 'trades:' + marketId
            # todo: incremental trades
            client.resolve(self.trades, messageHash)

    def handle_account_notifications(self, client, message):
        # not implemented yet
        # raise NotImplemented(self.id + 'watchTickers not implemented yet')
        return message

    def handle_message(self, client, message):
        channelId = self.safe_string(message, 0)
        market = self.safe_value(self.options['marketsByNumericId'], channelId)
        if market is None:
            methods = {
                # '<numericId>': 'handleOrderBookAndTrades',  # Price Aggregated Book
                '1000': self.handle_account_notifications,  # Beta
                '1002': self.handle_tickers,  # Ticker Data
                # '1003': None,  # 24 Hour Exchange Volume
                '1010': self.handle_heartbeat,
            }
            method = self.safe_value(methods, channelId)
            if method is None:
                return message
            else:
                method(client, message)
        else:
            return self.handle_order_book_and_trades(client, message)
