# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCacheBySymbolById
from ccxt.base.errors import ArgumentsRequired


class bitrue(ccxt.async_support.bitrue):

    def describe(self):
        return self.deep_extend(super(bitrue, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchTicker': False,
                'watchTickers': False,
                'watchTrades': False,
                'watchMyTrades': False,
                'watchOrders': True,
                'watchOrderBook': False,
                'watchOHLCV': False,
            },
            'urls': {
                'api': {
                    'open': 'https://open.bitrue.com',
                    'ws': {
                        'public': 'wss://ws.bitrue.com/market/ws',
                        'private': 'wss://wsapi.bitrue.com',
                    },
                },
            },
            'api': {
                'open': {
                    'private': {
                        'post': {
                            'poseidon/api/v1/listenKey': 1,
                        },
                        'put': {
                            'poseidon/api/v1/listenKey/{listenKey}': 1,
                        },
                        'delete': {
                            'poseidon/api/v1/listenKey/{listenKey}': 1,
                        },
                    },
                },
            },
            'options': {
                'listenKeyRefreshRate': 1800000,  # 30 mins
                'ws': {
                    'gunzip': True,
                },
            },
        })

    async def watch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        see https://github.com/Bitrue-exchange/Spot-official-api-docs#balance-update
        :param dict params: extra parameters specific to the bitrue api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        url = await self.authenticate()
        messageHash = 'balance'
        message = {
            'event': 'sub',
            'params': {
                'channel': 'user_balance_update',
            },
        }
        request = self.deep_extend(message, params)
        return await self.watch(url, messageHash, request, messageHash)

    def handle_balance(self, client, message):
        #
        #     {
        #         e: 'BALANCE',
        #         x: 'OutboundAccountPositionTradeEvent',
        #         E: 1657799510175,
        #         I: '302274978401288200',
        #         i: 1657799510175,
        #         B: [{
        #                 a: 'btc',
        #                 F: '0.0006000000000000',
        #                 T: 1657799510000,
        #                 f: '0.0006000000000000',
        #                 t: 0
        #             },
        #             {
        #                 a: 'usdt',
        #                 T: 0,
        #                 L: '0.0000000000000000',
        #                 l: '-11.8705317318000000',
        #                 t: 1657799510000
        #             }
        #         ],
        #         u: 1814396
        #     }
        #
        #     {
        #      e: 'BALANCE',
        #      x: 'OutboundAccountPositionOrderEvent',
        #      E: 1670051332478,
        #      I: '353662845694083072',
        #      i: 1670051332478,
        #      B: [
        #        {
        #          a: 'eth',
        #          F: '0.0400000000000000',
        #          T: 1670051332000,
        #          f: '-0.0100000000000000',
        #          L: '0.0100000000000000',
        #          l: '0.0100000000000000',
        #          t: 1670051332000
        #        }
        #      ],
        #      u: 2285311
        #    }
        #
        balances = self.safe_value(message, 'B', [])
        self.parse_ws_balances(balances)
        messageHash = 'balance'
        client.resolve(self.balance, messageHash)

    def parse_ws_balances(self, balances):
        #
        #    [{
        #         a: 'btc',
        #         F: '0.0006000000000000',
        #         T: 1657799510000,
        #         f: '0.0006000000000000',
        #         t: 0
        #     },
        #     {
        #         a: 'usdt',
        #         T: 0,
        #         L: '0.0000000000000000',
        #         l: '-11.8705317318000000',
        #         t: 1657799510000
        #     }]
        #
        self.balance['info'] = balances
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'a')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            free = self.safe_string(balance, 'F')
            used = self.safe_string(balance, 'L')
            balanceUpdateTime = self.safe_integer(balance, 'T', 0)
            lockBalanceUpdateTime = self.safe_integer(balance, 't', 0)
            updateFree = balanceUpdateTime != 0
            updateUsed = lockBalanceUpdateTime != 0
            if updateFree or updateUsed:
                if updateFree:
                    account['free'] = free
                if updateUsed:
                    account['used'] = used
                self.balance[code] = account
        self.balance = self.safe_balance(self.balance)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on user orders
        see https://github.com/Bitrue-exchange/Spot-official-api-docs#order-update
        :param [str] symbols: unified symbols of the market to watch the orders for
        :param int|None since: timestamp in ms of the earliest order
        :param int|None limit: the maximum amount of orders to return
        :param dict params: extra parameters specific to the bitrue api endpoint
        :returns dict: A dictionary of `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>` indexed by market symbols
        """
        await self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        url = await self.authenticate()
        messageHash = 'orders'
        message = {
            'event': 'sub',
            'params': {
                'channel': 'user_order_update',
            },
        }
        request = self.deep_extend(message, params)
        orders = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client, message):
        #
        #    {
        #        e: 'ORDER',
        #        i: 16122802798,
        #        E: 1657882521876,
        #        I: '302623154710888464',
        #        u: 1814396,
        #        s: 'btcusdt',
        #        S: 2,
        #        o: 1,
        #        q: '0.0005',
        #        p: '60000',
        #        X: 0,
        #        x: 1,
        #        z: '0',
        #        n: '0',
        #        N: 'usdt',
        #        O: 1657882521876,
        #        L: '0',
        #        l: '0',
        #        Y: '0'
        #    }
        #
        parsed = self.parse_ws_order(message)
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        orders.append(parsed)
        messageHash = 'orders'
        client.resolve(self.orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        #    {
        #        e: 'ORDER',
        #        i: 16122802798,
        #        E: 1657882521876,
        #        I: '302623154710888464',
        #        u: 1814396,
        #        s: 'btcusdt',
        #        S: 2,
        #        o: 1,
        #        q: '0.0005',
        #        p: '60000',
        #        X: 0,
        #        x: 1,
        #        z: '0',
        #        n: '0',
        #        N: 'usdt',
        #        O: 1657882521876,
        #        L: '0',
        #        l: '0',
        #        Y: '0'
        #    }
        #
        timestamp = self.safe_integer(order, 'E')
        marketId = self.safe_string_upper(order, 's')
        typeId = self.safe_string(order, 'o')
        sideId = self.safe_integer(order, 'S')
        # 1: buy
        # 2: sell
        side = 'buy' if (sideId == 1) else 'sell'
        statusId = self.safe_string(order, 'X')
        feeCurrencyId = self.safe_string(order, 'N')
        return self.safe_order({
            'info': order,
            'id': self.safe_string(order, 'i'),
            'clientOrderId': self.safe_string(order, 'c'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': self.safe_integer(order, 'T'),
            'symbol': self.safe_symbol(marketId, market),
            'type': self.parse_ws_order_type(typeId),
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': self.safe_string(order, 'p'),
            'triggerPrice': None,
            'amount': self.safe_string(order, 'q'),
            'cost': self.safe_string(order, 'Y'),
            'average': None,
            'filled': self.safe_string(order, 'z'),
            'remaining': None,
            'status': self.parse_ws_order_status(statusId),
            'fee': {
                'currency': self.safe_currency_code(feeCurrencyId),
                'cost': self.safe_number(order, 'n'),
            },
        }, market)

    async def watch_order_book(self, symbol, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' watchOrderBook() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = 'orderbook:' + symbol
        marketIdLowercase = market['id'].lower()
        channel = 'market_' + marketIdLowercase + '_simple_depth_step0'
        url = self.urls['api']['ws']['public']
        message = {
            'event': 'sub',
            'params': {
                'cb_id': marketIdLowercase,
                'channel': channel,
            },
        }
        request = self.deep_extend(message, params)
        return await self.watch(url, messageHash, request, messageHash)

    def handle_order_book(self, client, message):
        #
        #     {
        #         "channel": "market_ethbtc_simple_depth_step0",
        #         "ts": 1670056708670,
        #         "tick": {
        #             "buys": [
        #                 [
        #                     "0.075170",
        #                     "67.153"
        #                 ],
        #                 [
        #                     "0.075169",
        #                     "17.195"
        #                 ],
        #                 [
        #                     "0.075166",
        #                     "29.788"
        #                 ],
        #             ]
        #              "asks": [
        #                 [
        #                     "0.075171",
        #                     "0.256"
        #                 ],
        #                 [
        #                     "0.075172",
        #                     "0.160"
        #                 ],
        #             ]
        #         }
        #     }
        #
        channel = self.safe_string(message, 'channel')
        parts = channel.split('_')
        marketId = self.safe_string_upper(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        timestamp = self.safe_integer(message, 'ts')
        tick = self.safe_value(message, 'tick', {})
        orderbook = self.parse_order_book(tick, symbol, timestamp, 'buys', 'asks')
        self.orderbooks[symbol] = orderbook
        messageHash = 'orderbook:' + symbol
        client.resolve(orderbook, messageHash)

    def parse_ws_order_type(self, typeId):
        types = {
            '1': 'limit',
            '2': 'market',
            '3': 'limit',
        }
        return self.safe_string(types, typeId, typeId)

    def parse_ws_order_status(self, status):
        statuses = {
            '0': 'open',  # The order has not been accepted by the engine.
            '1': 'open',  # The order has been accepted by the engine.
            '2': 'closed',  # The order has been completed.
            '3': 'open',  # A part of the order has been filled.
            '4': 'canceled',  # The order has been canceled.
            '7': 'open',  # Stop order placed.
        }
        return self.safe_string(statuses, status, status)

    def handle_ping(self, client, message):
        self.spawn(self.pong, client, message)

    async def pong(self, client, message):
        #
        #     {
        #         "ping": 1670057540627
        #     }
        #
        time = self.safe_integer(message, 'ping')
        pong = {
            'pong': time,
        }
        await client.send(pong)

    def handle_message(self, client, message):
        if 'channel' in message:
            self.handle_order_book(client, message)
        elif 'ping' in message:
            self.handle_ping(client, message)
        else:
            event = self.safe_string(message, 'e')
            handlers = {
                'BALANCE': self.handle_balance,
                'ORDER': self.handle_order,
            }
            handler = self.safe_value(handlers, event)
            if handler is not None:
                handler(client, message)

    async def authenticate(self, params={}):
        listenKey = self.safe_value(self.options, 'listenKey')
        if listenKey is None:
            response = None
            try:
                response = await self.openPrivatePostPoseidonApiV1ListenKey(params)
            except Exception as error:
                self.options['listenKey'] = None
                self.options['listenKeyUrl'] = None
                return
            #
            #     {
            #         "msg": "succ",
            #         "code": 200,
            #         "data": {
            #             "listenKey": "7d1ec51340f499d85bb33b00a96ef680bda28869d5c3374a444c5ca4847d1bf0"
            #         }
            #     }
            #
            data = self.safe_value(response, 'data', {})
            key = self.safe_string(data, 'listenKey')
            self.options['listenKey'] = key
            self.options['listenKeyUrl'] = self.urls['api']['ws']['private'] + '/stream?listenKey=' + key
            refreshTimeout = self.safe_integer(self.options, 'listenKeyRefreshRate', 1800000)
            self.delay(refreshTimeout, self.keep_alive_listen_key)
        return self.options['listenKeyUrl']

    async def keep_alive_listen_key(self, params={}):
        listenKey = self.safe_string(self.options, 'listenKey')
        request = {
            'listenKey': listenKey,
        }
        try:
            await self.openPrivatePutPoseidonApiV1ListenKeyListenKey(self.extend(request, params))
            #
            # ಠ_ಠ
            #     {
            #         "msg": "succ",
            #         "code": "200"
            #     }
            #
        except Exception as error:
            self.options['listenKey'] = None
            self.options['listenKeyUrl'] = None
            return
        refreshTimeout = self.safe_integer(self.options, 'listenKeyRefreshRate', 1800000)
        self.delay(refreshTimeout, self.keep_alive_listen_key)
