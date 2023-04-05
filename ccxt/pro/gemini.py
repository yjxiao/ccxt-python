# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.async_support.base.ws.client import Client
from typing import Optional
from ccxt.base.errors import ExchangeError


class gemini(ccxt.async_support.gemini):

    def describe(self):
        return self.deep_extend(super(gemini, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': False,
                'watchTicker': False,
                'watchTickers': False,
                'watchTrades': True,
                'watchMyTrades': False,
                'watchOrders': True,
                'watchOrderBook': True,
                'watchOHLCV': True,
            },
            'hostname': 'api.gemini.com',
            'urls': {
                'api': {
                    'ws': 'wss://api.gemini.com',
                },
                'test': {
                    'ws': 'wss://api.sandbox.gemini.com',
                },
            },
        })

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watch the list of most recent trades for a particular symbol
        see https://docs.gemini.com/websocket-api/#market-data-version-2
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the gemini api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'trades:' + market['symbol']
        marketId = market['id']
        request = {
            'type': 'subscribe',
            'subscriptions': [
                {
                    'name': 'l2',
                    'symbols': [
                        marketId.upper(),
                    ],
                },
            ],
        }
        subscribeHash = 'l2:' + market['symbol']
        url = self.urls['api']['ws'] + '/v2/marketdata'
        trades = await self.watch(url, messageHash, request, subscribeHash)
        if self.newUpdates:
            limit = trades.getLimit(market['symbol'], limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def parse_ws_trade(self, trade, market=None):
        #
        #     {
        #         type: 'trade',
        #         symbol: 'BTCUSD',
        #         event_id: 122258166738,
        #         timestamp: 1655330221424,
        #         price: '22269.14',
        #         quantity: '0.00004473',
        #         side: 'buy'
        #     }
        #
        timestamp = self.safe_integer(trade, 'timestamp')
        id = self.safe_string(trade, 'event_id')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'quantity')
        side = self.safe_string_lower(trade, 'side')
        marketId = self.safe_string_lower(trade, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        return self.safe_trade({
            'id': id,
            'order': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'cost': None,
            'amount': amountString,
            'fee': None,
        }, market)

    def handle_trade(self, client: Client, message):
        #
        #     {
        #         type: 'trade',
        #         symbol: 'BTCUSD',
        #         event_id: 122278173770,
        #         timestamp: 1655335880981,
        #         price: '22530.80',
        #         quantity: '0.04',
        #         side: 'buy'
        #     }
        #
        trade = self.parse_ws_trade(message)
        symbol = trade['symbol']
        tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            stored = ArrayCache(tradesLimit)
            self.trades[symbol] = stored
        stored.append(trade)
        messageHash = 'trades:' + symbol
        client.resolve(stored, messageHash)

    def handle_trades(self, client: Client, message):
        #
        #     {
        #         type: 'l2_updates',
        #         symbol: 'BTCUSD',
        #         changes: [
        #             ['buy', '22252.37', '0.02'],
        #             ['buy', '22251.61', '0.04'],
        #             ['buy', '22251.60', '0.04'],
        #             # some asks
        #         ],
        #         trades: [
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258166738, timestamp: 1655330221424, price: '22269.14', quantity: '0.00004473', side: 'buy'},
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258141090, timestamp: 1655330213216, price: '22250.00', quantity: '0.00704098', side: 'buy'},
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258118291, timestamp: 1655330206753, price: '22250.00', quantity: '0.03', side: 'buy'},
        #         ],
        #         auction_events: [
        #             {
        #                 type: 'auction_result',
        #                 symbol: 'BTCUSD',
        #                 time_ms: 1655323200000,
        #                 result: 'failure',
        #                 highest_bid_price: '21590.88',
        #                 lowest_ask_price: '21602.30',
        #                 collar_price: '21634.73'
        #             },
        #             {
        #                 type: 'auction_indicative',
        #                 symbol: 'BTCUSD',
        #                 time_ms: 1655323185000,
        #                 result: 'failure',
        #                 highest_bid_price: '21661.90',
        #                 lowest_ask_price: '21663.79',
        #                 collar_price: '21662.845'
        #             },
        #         ]
        #     }
        #
        marketId = self.safe_string_lower(message, 'symbol')
        market = self.safe_market(marketId)
        trades = self.safe_value(message, 'trades')
        if trades is not None:
            symbol = market['symbol']
            tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = self.safe_value(self.trades, symbol)
            if stored is None:
                stored = ArrayCache(tradesLimit)
                self.trades[symbol] = stored
            for i in range(0, len(trades)):
                trade = self.parse_ws_trade(trades[i], market)
                stored.append(trade)
            messageHash = 'trades:' + symbol
            client.resolve(stored, messageHash)

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        see https://docs.gemini.com/websocket-api/#candles-data-feed
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the gemini api endpoint
        :returns [[int]]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        timeframeId = self.safe_string(self.timeframes, timeframe, timeframe)
        request = {
            'type': 'subscribe',
            'subscriptions': [
                {
                    'name': 'candles_' + timeframeId,
                    'symbols': [
                        market['id'].upper(),
                    ],
                },
            ],
        }
        messageHash = 'ohlcv:' + market['symbol'] + ':' + timeframeId
        url = self.urls['api']['ws'] + '/v2/marketdata'
        ohlcv = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client: Client, message):
        #
        #     {
        #         "type": "candles_15m_updates",
        #         "symbol": "BTCUSD",
        #         "changes": [
        #             [
        #                 1561054500000,
        #                 9350.18,
        #                 9358.35,
        #                 9350.18,
        #                 9355.51,
        #                 2.07
        #             ],
        #             [
        #                 1561053600000,
        #                 9357.33,
        #                 9357.33,
        #                 9350.18,
        #                 9350.18,
        #                 1.5900161
        #             ]
        #             ...
        #         ]
        #     }
        #
        type = self.safe_string(message, 'type', '')
        timeframeId = type[8:]
        timeframeEndIndex = timeframeId.find('_')
        timeframeId = timeframeId[0:timeframeEndIndex]
        marketId = self.safe_string(message, 'symbol', '').lower()
        market = self.safe_market(marketId)
        symbol = self.safe_symbol(marketId, market)
        changes = self.safe_value(message, 'changes', [])
        timeframe = self.find_timeframe(timeframeId)
        ohlcvsBySymbol = self.safe_value(self.ohlcvs, symbol)
        if ohlcvsBySymbol is None:
            self.ohlcvs[symbol] = {}
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        changesLength = len(changes)
        # reverse order of array to store candles in ascending order
        for i in range(0, changesLength):
            index = changesLength - i - 1
            parsed = self.parse_ohlcv(changes[index], market)
            stored.append(parsed)
        messageHash = 'ohlcv:' + symbol + ':' + timeframeId
        client.resolve(stored, messageHash)
        return message

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        see https://docs.gemini.com/websocket-api/#market-data-version-2
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the gemini api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'orderbook:' + market['symbol']
        marketId = market['id']
        request = {
            'type': 'subscribe',
            'subscriptions': [
                {
                    'name': 'l2',
                    'symbols': [
                        marketId.upper(),
                    ],
                },
            ],
        }
        subscribeHash = 'l2:' + market['symbol']
        url = self.urls['api']['ws'] + '/v2/marketdata'
        orderbook = await self.watch(url, messageHash, request, subscribeHash)
        return orderbook.limit()

    def handle_order_book(self, client: Client, message):
        changes = self.safe_value(message, 'changes', [])
        marketId = self.safe_string_lower(message, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        messageHash = 'orderbook:' + symbol
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            orderbook = self.order_book()
        for i in range(0, len(changes)):
            delta = changes[i]
            price = self.safe_number(delta, 1)
            size = self.safe_number(delta, 2)
            side = 'bids' if (delta[0] == 'buy') else 'asks'
            bookside = orderbook[side]
            bookside.store(price, size)
            orderbook[side] = bookside
        orderbook['symbol'] = symbol
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    def handle_l2_updates(self, client: Client, message):
        #
        #     {
        #         type: 'l2_updates',
        #         symbol: 'BTCUSD',
        #         changes: [
        #             ['buy', '22252.37', '0.02'],
        #             ['buy', '22251.61', '0.04'],
        #             ['buy', '22251.60', '0.04'],
        #             # some asks
        #         ],
        #         trades: [
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258166738, timestamp: 1655330221424, price: '22269.14', quantity: '0.00004473', side: 'buy'},
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258141090, timestamp: 1655330213216, price: '22250.00', quantity: '0.00704098', side: 'buy'},
        #             {type: 'trade', symbol: 'BTCUSD', event_id: 122258118291, timestamp: 1655330206753, price: '22250.00', quantity: '0.03', side: 'buy'},
        #         ],
        #         auction_events: [
        #             {
        #                 type: 'auction_result',
        #                 symbol: 'BTCUSD',
        #                 time_ms: 1655323200000,
        #                 result: 'failure',
        #                 highest_bid_price: '21590.88',
        #                 lowest_ask_price: '21602.30',
        #                 collar_price: '21634.73'
        #             },
        #             {
        #                 type: 'auction_indicative',
        #                 symbol: 'BTCUSD',
        #                 time_ms: 1655323185000,
        #                 result: 'failure',
        #                 highest_bid_price: '21661.90',
        #                 lowest_ask_price: '21663.79',
        #                 collar_price: '21662.845'
        #             },
        #         ]
        #     }
        #
        self.handle_order_book(client, message)
        self.handle_trades(client, message)

    async def watch_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        watches information on multiple orders made by the user
        see https://docs.gemini.com/websocket-api/#order-events
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the gemini api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        url = self.urls['api']['ws'] + '/v1/order/events?eventTypeFilter=initial&eventTypeFilter=accepted&eventTypeFilter=rejected&eventTypeFilter=fill&eventTypeFilter=cancelled&eventTypeFilter=booked'
        await self.load_markets()
        authParams = {
            'url': url,
        }
        await self.authenticate(authParams)
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        messageHash = 'orders'
        orders = await self.watch(url, messageHash, None, messageHash)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_heartbeat(self, client: Client, message):
        #
        #     {
        #         type: 'heartbeat',
        #         timestampms: 1659740268958,
        #         sequence: 7,
        #         trace_id: '25b3d92476dd3a9a5c03c9bd9e0a0dba',
        #         socket_sequence: 7
        #     }
        #
        return message

    def handle_subscription(self, client: Client, message):
        #
        #     {
        #         type: 'subscription_ack',
        #         accountId: 19433282,
        #         subscriptionId: 'orderevents-websocket-25b3d92476dd3a9a5c03c9bd9e0a0dba',
        #         symbolFilter: [],
        #         apiSessionFilter: [],
        #         eventTypeFilter: []
        #     }
        #
        return message

    def handle_order(self, client: Client, message):
        #
        #     [
        #         {
        #             type: 'accepted',
        #             order_id: '134150423884',
        #             event_id: '134150423886',
        #             account_name: 'primary',
        #             client_order_id: '1659739406916',
        #             api_session: 'account-pnBFSS0XKGvDamX4uEIt',
        #             symbol: 'batbtc',
        #             side: 'sell',
        #             order_type: 'exchange limit',
        #             timestamp: '1659739407',
        #             timestampms: 1659739407576,
        #             is_live: True,
        #             is_cancelled: False,
        #             is_hidden: False,
        #             original_amount: '1',
        #             price: '1',
        #             socket_sequence: 139
        #         }
        #     ]
        #
        messageHash = 'orders'
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        orders = self.orders
        for i in range(0, len(message)):
            order = self.parse_ws_order(message[i])
            orders.append(order)
        client.resolve(self.orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        #     {
        #         type: 'accepted',
        #         order_id: '134150423884',
        #         event_id: '134150423886',
        #         account_name: 'primary',
        #         client_order_id: '1659739406916',
        #         api_session: 'account-pnBFSS0XKGvDamX4uEIt',
        #         symbol: 'batbtc',
        #         side: 'sell',
        #         order_type: 'exchange limit',
        #         timestamp: '1659739407',
        #         timestampms: 1659739407576,
        #         is_live: True,
        #         is_cancelled: False,
        #         is_hidden: False,
        #         original_amount: '1',
        #         price: '1',
        #         socket_sequence: 139
        #     }
        #
        timestamp = self.safe_number(order, 'timestampms')
        status = self.safe_string(order, 'type')
        marketId = self.safe_string(order, 'symbol')
        typeId = self.safe_string(order, 'order_type')
        behavior = self.safe_string(order, 'behavior')
        timeInForce = 'GTC'
        postOnly = False
        if behavior == 'immediate-or-cancel':
            timeInForce = 'IOC'
        elif behavior == 'fill-or-kill':
            timeInForce = 'FOK'
        elif behavior == 'maker-or-cancel':
            timeInForce = 'PO'
            postOnly = True
        return self.safe_order({
            'id': self.safe_string(order, 'order_id'),
            'clientOrderId': self.safe_string(order, 'client_order_id'),
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': self.parse_ws_order_status(status),
            'symbol': self.safe_symbol(marketId, market),
            'type': self.parse_ws_order_type(typeId),
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'side': self.safe_string(order, 'side'),
            'price': self.safe_number(order, 'price'),
            'stopPrice': None,
            'average': self.safe_number(order, 'avg_execution_price'),
            'cost': None,
            'amount': self.safe_number(order, 'original_amount'),
            'filled': self.safe_number(order, 'executed_amount'),
            'remaining': self.safe_number(order, 'remaining_amount'),
            'fee': None,
            'trades': None,
        }, market)

    def parse_ws_order_status(self, status):
        statuses = {
            'accepted': 'open',
            'booked': 'open',
            'fill': 'closed',
            'cancelled': 'canceled',
            'cancel_rejected': 'rejected',
            'rejected': 'rejected',
        }
        return self.safe_string(statuses, status, status)

    def parse_ws_order_type(self, type):
        types = {
            'exchange limit': 'limit',
            'market buy': 'market',
            'market sell': 'market',
        }
        return self.safe_string(types, type, type)

    def handle_error(self, client: Client, message):
        #
        #     {
        #         reason: 'NoValidTradingPairs',
        #         result: 'error'
        #     }
        #
        raise ExchangeError(self.json(message))

    def handle_message(self, client: Client, message):
        #
        #  public
        #     {
        #         type: 'trade',
        #         symbol: 'BTCUSD',
        #         event_id: 122278173770,
        #         timestamp: 1655335880981,
        #         price: '22530.80',
        #         quantity: '0.04',
        #         side: 'buy'
        #     }
        #
        #  private
        #     [
        #         {
        #             type: 'accepted',
        #             order_id: '134150423884',
        #             event_id: '134150423886',
        #             account_name: 'primary',
        #             client_order_id: '1659739406916',
        #             api_session: 'account-pnBFSS0XKGvDamX4uEIt',
        #             symbol: 'batbtc',
        #             side: 'sell',
        #             order_type: 'exchange limit',
        #             timestamp: '1659739407',
        #             timestampms: 1659739407576,
        #             is_live: True,
        #             is_cancelled: False,
        #             is_hidden: False,
        #             original_amount: '1',
        #             price: '1',
        #             socket_sequence: 139
        #         }
        #     ]
        #
        isArray = isinstance(message, list)
        if isArray:
            return self.handle_order(client, message)
        reason = self.safe_string(message, 'reason')
        if reason == 'error':
            self.handle_error(client, message)
        methods = {
            'l2_updates': self.handle_l2_updates,
            'trade': self.handle_trade,
            'subscription_ack': self.handle_subscription,
            'heartbeat': self.handle_heartbeat,
        }
        type = self.safe_string(message, 'type', '')
        if type.find('candles') >= 0:
            return self.handle_ohlcv(client, message)
        method = self.safe_value(methods, type)
        if method is not None:
            method(client, message)

    async def authenticate(self, params={}):
        url = self.safe_string(params, 'url')
        if (self.clients is not None) and (url in self.clients):
            return
        self.check_required_credentials()
        startIndex = len(self.urls['api']['ws'])
        urlParamsIndex = url.find('?')
        urlLength = len(url)
        endIndex = urlParamsIndex if (urlParamsIndex >= 0) else urlLength
        request = url[startIndex:endIndex]
        payload = {
            'request': request,
            'nonce': self.nonce(),
        }
        b64 = self.string_to_base64(self.json(payload))
        signature = self.hmac(b64, self.encode(self.secret), hashlib.sha384, 'hex')
        defaultOptions = {
            'ws': {
                'options': {
                    'headers': {},
                },
            },
        }
        self.options = self.extend(defaultOptions, self.options)
        originalHeaders = self.options['ws']['options']['headers']
        headers = {
            'X-GEMINI-APIKEY': self.apiKey,
            'X-GEMINI-PAYLOAD': b64,
            'X-GEMINI-SIGNATURE': signature,
        }
        self.options['ws']['options']['headers'] = headers
        self.client(url)
        self.options['ws']['options']['headers'] = originalHeaders
