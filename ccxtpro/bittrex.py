# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxtpro
import ccxt.async_support as ccxt
import hashlib
import json
from ccxt.base.errors import AuthenticationError


class bittrex(ccxtpro.Exchange, ccxt.bittrex):

    def describe(self):
        return self.deep_extend(super(bittrex, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchBalance': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://socket.bittrex.com/signalr/connect',
                    'signalr': 'https://socket.bittrex.com/signalr',
                },
            },
            'api': {
                'signalr': {
                    'get': [
                        'negotiate',
                        'start',
                    ],
                },
            },
            'options': {
                'hub': 'c2',
            },
        })

    def create_signal_r_query(self, params={}):
        hub = self.safe_string(self.options, 'hub', 'c2')
        hubs = [
            {'name': hub},
        ]
        ms = self.milliseconds()
        return self.extend({
            'transport': 'webSockets',
            'connectionData': self.json(hubs),
            'clientProtocol': 1.5,
            '_': ms,  # no cache
            'tid': self.sum(ms % 10, 1),  # random
        }, params)

    async def negotiate(self, params={}):
        client = self.client(self.urls['api']['ws'])
        messageHash = 'negotiate'
        future = self.safe_value(client.subscriptions, messageHash)
        if future is None:
            future = client.future(messageHash)
            client.subscriptions[messageHash] = future
            request = self.create_signal_r_query(params)
            response = await self.signalrGetNegotiate(self.extend(request, params))
            #
            #     {
            #         Url: '/signalr/v1.1/signalr',
            #         ConnectionToken: 'lT/sa19+FcrEb4W53On2v+Pcc3d4lVCHV5/WJtmQw1RQNQMpm7K78w/WnvfTN2EgwQopTUiFX1dioHN7Bd1p8jAbfdxrqf5xHAMntJfOrw1tON0O',
            #         ConnectionId: 'a2afb0f7-346f-4f32-b7c7-01e04584b86a',
            #         KeepAliveTimeout: 20,
            #         DisconnectTimeout: 30,
            #         ConnectionTimeout: 110,
            #         TryWebSockets: True,
            #         ProtocolVersion: '1.5',
            #         TransportConnectTimeout: 5,
            #         LongPollDelay: 0
            #     }
            #
            result = {
                'request': request,
                'response': response,
            }
            client.resolve(result, messageHash)
        return await future

    async def start(self, negotiation, params={}):
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        request = self.create_signal_r_query(self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        }))
        return await self.signalrGetStart(request)

    async def authenticate(self, params={}):
        self.check_required_credentials()
        future = self.negotiate()
        return await self.after_async(future, self.get_auth_context, params)

    async def get_auth_context(self, negotiation, params={}):
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        method = 'GetAuthContext'
        client = self.client(url)
        authenticate = self.safe_value(client.subscriptions, method, {})
        future = self.safe_value(authenticate, 'future')
        if future is None:
            future = client.future('authenticated')
            requestId = str(self.milliseconds())
            hub = self.safe_string(self.options, 'hub', 'c2')
            request = {
                'H': hub,
                'M': method,  # request method
                'A': [self.apiKey],  # arguments
                'I': requestId,  # invocation request id
            }
            subscription = {
                'id': requestId,
                'method': self.handle_get_auth_context,
                'negotiation': negotiation,
                'future': future,
            }
            self.spawn(self.watch, url, requestId, request, method, subscription)
        return await future

    def handle_get_auth_context(self, client, message, subscription):
        #
        #     {
        #         'R': '7d10e6b583484659918821072c83a5b6ce488e03cb744d86a2cc820bad466f1f',
        #         'I': '1579474528471'
        #     }
        #
        # print(self.iso8601(self.milliseconds()), 'handleGetAuthContext')
        negotiation = self.safe_value(subscription, 'negotiation', {})
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        challenge = self.safe_string(message, 'R')
        signature = self.hmac(self.encode(challenge), self.encode(self.secret), hashlib.sha512)
        requestId = str(self.milliseconds())
        hub = self.safe_string(self.options, 'hub', 'c2')
        method = 'Authenticate'
        request = {
            'H': hub,
            'M': method,  # request method
            'A': [self.apiKey, signature],  # arguments
            'I': requestId,  # invocation request id
        }
        authenticateSubscription = {
            'id': requestId,
            'method': self.handle_authenticate,
            'negotiation': negotiation,
        }
        self.spawn(self.watch, url, requestId, request, requestId, authenticateSubscription)
        return message

    def handle_authenticate(self, client, message, subscription):
        #
        #     {'R': True, 'I': '1579474528821'}
        #
        R = self.safe_value(message, 'R')
        if R:
            client.resolve(subscription['negotiation'], 'authenticated')
        else:
            error = AuthenticationError('Authentication failed')
            client.reject(error, 'authenticated')
            authSubscriptionHash = 'GetAuthContext'
            if authSubscriptionHash in client.subscriptions:
                del client.subscriptions[authSubscriptionHash]
        return message

    async def subscribe_to_user_deltas(self, negotiation, params={}):
        await self.load_markets()
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        requestId = str(self.milliseconds())
        method = 'SubscribeToUserDeltas'
        messageHash = 'balance'
        subscribeHash = method
        hub = self.safe_string(self.options, 'hub', 'c2')
        request = {
            'H': hub,
            'M': method,
            'A': [],  # arguments
            'I': requestId,  # invocation request id
        }
        subscription = {
            'id': requestId,
            'params': params,
            'method': self.handle_subscribe_to_user_deltas,
            'negotiation': negotiation,
        }
        return await self.watch(url, messageHash, request, subscribeHash, subscription)

    async def watch_balance(self, params={}):
        await self.load_markets()
        future = self.authenticate()
        return await self.after_async(future, self.subscribe_to_user_deltas, params)

    async def subscribe_to_exchange_deltas(self, negotiation, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
            # 'tid': self.milliseconds() % 10,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        requestId = str(self.milliseconds())
        method = 'SubscribeToExchangeDeltas'
        messageHash = 'orderbook' + ':' + symbol
        subscribeHash = method + ':' + symbol
        marketId = market['id']
        hub = self.safe_string(self.options, 'hub', 'c2')
        request = {
            'H': hub,
            'M': method,
            'A': [marketId],  # arguments
            'I': requestId,  # invocation request id
        }
        subscription = {
            'id': requestId,
            'symbol': symbol,
            'limit': limit,
            'params': params,
            'method': self.handle_subscribe_to_exchange_deltas,
            'negotiation': negotiation,
        }
        future = self.watch(url, messageHash, request, subscribeHash, subscription)
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    async def watch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        future = self.negotiate()
        return await self.after_async(future, self.subscribe_to_exchange_deltas, symbol, limit, params)

    def limit_order_book(self, orderbook, symbol, limit=None, params={}):
        return orderbook.limit(limit)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 'R')
        amount = self.safe_float(delta, 'Q')
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_exchange_delta(self, client, message):
        #
        #     {
        #         'M': 'BTC-ETH',
        #         'N': 2322248,
        #         'Z': [],
        #         'S': [
        #             {'TY': 0, 'R': 0.01938852, 'Q': 29.32758526},
        #             {'TY': 1, 'R': 0.02322822, 'Q': 0}
        #         ],
        #         'f': []
        #     }
        #
        marketId = self.safe_string(message, 'M')
        market = None
        symbol = None
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
        #
        # https://bittrex.github.io/api/v1-1#socket-connections
        #
        #     1 Drop existing websocket connections and flush accumulated data and state(e.g. market nonces).
        #     2 Re-establish websocket connection.
        #     3 Subscribe to BTC-ETH market deltas, cache received data keyed by nonce.
        #     4 Query BTC-ETH market state.
        #     5 Apply cached deltas sequentially, starting with nonces greater than that received in step 4.
        #
        if (symbol is not None) and (symbol in self.orderbooks):
            orderbook = self.orderbooks[symbol]
            if orderbook['nonce'] is not None:
                self.handle_order_book_message(client, message, orderbook)
                name = 'orderbook'
                messageHash = name + ':' + symbol
                client.resolve(orderbook, messageHash)
            else:
                orderbook.cache.append(message)

    def handle_order_book_message(self, client, message, orderbook):
        #
        #     {
        #         'M': 'BTC-ETH',
        #         'N': 2322248,
        #         'Z': [],
        #         'S': [
        #             {'TY': 0, 'R': 0.01938852, 'Q': 29.32758526},
        #             {'TY': 1, 'R': 0.02322822, 'Q': 0}
        #         ],
        #         'f': []
        #     }
        #
        nonce = self.safe_integer(message, 'N')
        # print(new Date(), 'handleOrderBookMessage', nonce, orderbook['nonce'])
        if nonce > orderbook['nonce']:
            self.handle_deltas(orderbook['asks'], self.safe_value(message, 'S', []))
            self.handle_deltas(orderbook['bids'], self.safe_value(message, 'Z', []))
            orderbook['nonce'] = nonce
        return orderbook

    def handle_balance_delta(self, client, message):
        #
        #     {
        #         N: 4,  # nonce
        #         d: {
        #             U: '2832c5c6-ac7a-493e-bc16-ebca06c73670',  # uuid
        #             W: 334126,  # account id(wallet)
        #             c: 'BTC',  # currency
        #             b: 0.0181687,  # balance
        #             a: 0.0081687,  # available
        #             z: 0,  # pending
        #             p: '1cL5M4HjjoGWMA4jgHC5v6GqcjfxeeNMy',  # address
        #             r: False,  # requested
        #             u: 1579561864940,  # last updated timestamp
        #             h: null,  # autosell
        #         },
        #     }
        #
        # print(new Date(), 'handleBalanceDelta', message)
        d = self.safe_value(message, 'd')
        account = self.account()
        account['free'] = self.safe_float(d, 'a')
        account['total'] = self.safe_float(d, 'b')
        code = self.safe_currency_code(self.safe_string(d, 'c'))
        result = {}
        result[code] = account
        self.balance = self.deep_extend(self.balance, result)
        self.balance = self.parse_balance(self.balance)
        client.resolve(self.balance, 'balance')
        return message

    async def fetch_balance_snapshot(self, client, message, subscription):
        # print(new Date(), 'fetchBalanceSnapshot')
        # todo: self is a synch blocking call in ccxt.php - make it async
        response = await self.fetchBalance()
        self.balance = self.deep_extend(self.balance, response)
        # messageHash = self.safe_string(subscription, 'messageHash')
        client.resolve(self.balance, 'balance')

    async def fetch_balance_state(self, params={}):
        # print(new Date(), 'fetchBalanceState')
        await self.load_markets()
        future = self.authenticate()
        return await self.after_async(future, self.query_balance_state, params)

    async def query_balance_state(self, negotiation, params={}):
        #
        # This method does not work as expected.
        #
        # In general Bittrex API docs do not mention how to get the current
        # state or a snapshot of balances of all coins over WS. The docs only
        # specify how to 'Authenticate'(that works fine) which subscribes
        # the user being authenticated to balance and order deltas by default.
        #
        # Investigating the WS message log in the browser on the
        # balance page on Bittrex's website shows a request to
        # QueryBalanceState over WS sent in the very beginning.
        # However, in case of WS in the browser on the Bittrex website
        # there is no 'Authenticate' message, therefore the Bittrex website
        # uses a different authentication mechanism(presumably, involving
        # HTTP headers and Cookies upon the SignalR negotiation handshake).
        #
        # An attempt to replicate the same request to QueryBalanceState
        # over WS here has failed – the WS server responds to that request
        # with an empty message containing just the request id, without
        # the actual snapshot result(no field called R in the SignalR message).
        #
        # The issue experienced is 100% identical to
        #
        #     https://github.com/Bittrex/bittrex.github.io/issues/23
        #
        #     2020-01-20T16:20:52.133Z connecting to wss://socket.bittrex.com/signalr/connect?transport=webSockets&connectionData=%5B%7B%22name%22%3A%22c2%22%7D%5D&clientProtocol=1.5&_=1579537250704&tid=4&connectionToken=ycjp5vmHhq3%2BZ5yyAgSejQyUOQR%2Bj3aWrwoqBH3Tu4MWk0y84QjuCo4tp6PHPwrVqQf96jE7QRIZ3SwTcpMf5pdS40Vkxr3e4AjUdrRfFuoaidSh
        #     2020-01-20T16:20:52.469Z onUpgrade
        #     2020-01-20T16:20:52.471Z onOpen
        #     2020-01-20T16:20:52.471Z sending {
        #         H: 'c2',
        #         M: 'GetAuthContext',
        #         A: ['247febd8422c4b1dbdcd8a4ca9a6d15b'],
        #         I: '1579537252133'
        #     }
        #     2020-01-20T16:20:52.584Z handleSystemStatus {C: 'd-4F618038-L,0|LC0f,0|LC0g,1', S: 1, M: []}
        #     2020-01-20T16:20:52.938Z onMessage {
        #         R: '99d0f9052ee442eba5736169517ef9a67ecf08c83a364295a647c989c32737f4',
        #         I: '1579537252133'
        #     }
        #     2020-01-20T16:20:52.943Z sending {
        #         H: 'c2',
        #         M: 'Authenticate',
        #         A: [
        #             '247febd8422c4b1dbdcd8a4ca9a6d15b',
        #             '7935676d6c995f0435ec1cab48a8d02e3b4d1f786f941abba8aedbe2e088db0f023c15cee132dc6db50dd674e4ebf5a417de9ed59645b5668314846bbea8ec57'
        #         ],
        #         I: '1579537252943'
        #     }
        #     2020-01-20T16:20:56.216Z onMessage {R: True, I: '1579537252943'}
        #     2020-01-20T16:20:56.217Z sending {H: 'c2', M: 'SubscribeToUserDeltas', A: [], I: '1579537256217'}
        #     2020-01-20T16:20:57.035Z onMessage {R: True, I: '1579537256217'}
        #     2020-01-20T16:20:57.037Z sending {H: 'c2', M: 'QueryBalanceState', A: [], I: '1579537257037'}
        #     2020-01-20T16:20:57.772Z onMessage {I: '1579537257037'}
        #                                                  ↑
        #                                                  |
        #                       :( no 'R' here ------------+
        #
        # The last message in the sequence above has no resulting 'R' field
        # which is present in the WebInspector and should contain the snapshot.
        # Since the balance snapshot is returned and observed in WebInspector
        # self is not caused by low balances. Apparently, a 'Query*' over WS
        # requires a different authentication sequence that involves
        # headers and cookies from reCaptcha and Cloudflare.
        #
        # print(new Date(), 'queryBalanceState')
        #
        await self.load_markets()
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        method = 'QueryBalanceState'
        requestId = str(self.milliseconds())
        hub = self.safe_string(self.options, 'hub', 'c2')
        request = {
            'H': hub,
            'M': method,
            'A': [],  # arguments
            'I': requestId,  # invocation request id
        }
        subscription = {
            'id': requestId,
            'method': self.handle_balance_state,
        }
        future = self.watch(url, requestId, request, requestId, subscription)
        return await self.after(future, self.limit_order_book, params)

    def handle_balance_state(self, client, message, subscription):
        # print(new Date(), 'handleBalanceState')
        R = self.safe_string(message, 'R')
        # if R is not None:
        #     #
        #     #     {
        #     #         N: 2,
        #     #         y: {
        #     #             USDT: {
        #     #                 U: '2832c5c6-ac7a-493e-bc16-ebca06c73670',
        #     #                 W: 334126,
        #     #                 c: 'USDT',
        #     #                 b: 0.00002077,
        #     #                 a: 0.00002077,
        #     #                 z: 0,
        #     #                 p: null,
        #     #                 r: False,
        #     #                 u: 978307200000,
        #     #                 h: null
        #     #             },
        #     #             BTC: {
        #     #                 U: '2832c5c6-ac7a-493e-bc16-ebca06c73670',
        #     #                 W: 334126,
        #     #                 c: 'BTC',
        #     #                 b: 0.00000736,
        #     #                 a: 0.00000736,
        #     #                 z: 0,
        #     #                 p: '1cL5M4HjjoGWMA4jgHC5v6GqcjfxeeNMy',
        #     #                 r: False,
        #     #                 u: 978307200000,
        #     #                 h: null
        #     #             },
        #     #         }
        #     #     }
        #     #
        #     response = json.loads(self.inflate(R))
        # }
        return R

    async def fetch_exchange_state(self, symbol, limit=None, params={}):
        await self.load_markets()
        future = self.negotiate()
        return await self.after_async(future, self.query_exchange_state, symbol, limit, params)

    async def query_exchange_state(self, negotiation, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        connectionToken = self.safe_string(negotiation['response'], 'ConnectionToken')
        query = self.extend(negotiation['request'], {
            'connectionToken': connectionToken,
        })
        url = self.urls['api']['ws'] + '?' + self.urlencode(query)
        method = 'QueryExchangeState'
        requestId = str(self.milliseconds())
        marketId = market['id']
        hub = self.safe_string(self.options, 'hub', 'c2')
        request = {
            'H': hub,
            'M': method,
            'A': [marketId],  # arguments
            'I': requestId,  # invocation request id
        }
        subscription = {
            'id': requestId,
            'method': self.handle_exchange_state,
        }
        future = self.watch(url, requestId, request, requestId, subscription)
        return await self.after(future, self.limit_order_book, symbol, limit, params)

    def handle_exchange_state(self, client, message, subscription):
        R = json.loads(self.inflate(self.safe_value(message, 'R')))
        #
        #     {
        #         'M': 'BTC-ETH',
        #         'N': 2571953,
        #         'Z': [ # bids
        #             {'Q': 2.38619729, 'R': 0.01964739},
        #             {'Q': 6, 'R': 0.01964738},
        #             {'Q': 0.0257, 'R': 0.01964736},
        #         ],
        #         'S': [ # asks
        #             {'Q': 1.84253634, 'R': 0.01965675},
        #             {'Q': 3.61380271, 'R': 0.01965677},
        #             {'Q': 5.6518, 'R': 0.01965678},
        #         ],
        #         'f': [ # last fills
        #             {
        #                 'I': 49355896,
        #                 'T': 1579380036860,
        #                 'Q': 0.06966562,
        #                 'P': 0.01964993,
        #                 't': 0.0013689245564066,
        #                 'F': 'FILL',
        #                 'OT': 'SELL',
        #                 'U': '421c649f-82fa-437b-b8f2-2a6a55bbecbc'
        #             },
        #         ]
        #     }
        #
        marketId = self.safe_string(R, 'M')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
            orderbook = self.safe_value(self.orderbooks, symbol)
            if orderbook is not None:
                snapshot = self.parse_order_book(R, None, 'Z', 'S', 'R', 'Q')
                snapshot['nonce'] = self.safe_integer(R, 'N')
                orderbook.reset(snapshot)
                # unroll the accumulated deltas
                messages = orderbook.cache
                for i in range(0, len(messages)):
                    message = messages[i]
                    self.handle_order_book_message(client, message, orderbook)
                self.orderbooks[symbol] = orderbook
                messageHash = 'orderbook:' + symbol
                client.resolve(orderbook, messageHash)
                requestId = self.safe_string(subscription, 'id')
                client.resolve(orderbook, requestId)

    def handle_subscribe_to_user_deltas(self, client, message, subscription):
        # print(new Date(), 'handleSubscribeToUserDeltas')
        # fetch the snapshot in a separate async call
        self.spawn(self.fetch_balance_snapshot, client, message, subscription)
        # the two lines below may work when bittrex fixes the snapshots
        # params = self.safe_value(subscription, 'params')
        # self.spawn(self.fetch_balance_state, params)

    def handle_subscribe_to_exchange_deltas(self, client, message, subscription):
        symbol = self.safe_string(subscription, 'symbol')
        limit = self.safe_string(subscription, 'limit')
        params = self.safe_string(subscription, 'params')
        if symbol in self.orderbooks:
            del self.orderbooks[symbol]
        self.orderbooks[symbol] = self.order_book({}, limit)
        # fetch the snapshot in a separate async call
        self.spawn(self.fetch_exchange_state, symbol, limit, params)

    def handle_subscription_status(self, client, message):
        #
        #     {'R': True, I: '1579299273251'}
        #
        I = self.safe_string(message, 'I')  # noqa: E741
        subscription = self.safe_value(client.subscriptions, I)
        if subscription is None:
            subscriptionsById = self.index_by(client.subscriptions, 'id')
            subscription = self.safe_value(subscriptionsById, I, {})
        else:
            # clear if subscriptionHash == requestId(one-time request)
            del client.subscriptions[I]
        method = self.safe_value(subscription, 'method')
        if method is None:
            client.resolve(message, I)
        else:
            method(client, message, subscription)
        return message

    def handle_system_status(self, client, message):
        # send signalR protocol start() call
        future = self.negotiate()
        self.spawn(self.after_async, future, self.start)
        # print(new Date(), 'handleSystemStatus', message)
        return message

    def handle_heartbeat(self, client, message):
        #
        # every 20 seconds(approx) if no other updates are sent
        #
        #     {}
        #
        # print(new Date(), 'heartbeat')
        client.resolve(message, 'heartbeat')

    def handle_order_delta(self, client, message):
        return message

    def handle_message(self, client, message):
        methods = {
            'uE': self.handle_exchange_delta,
            'uO': self.handle_order_delta,
            'uB': self.handle_balance_delta,
        }
        M = self.safe_value(message, 'M', [])
        for i in range(0, len(M)):
            methodType = self.safe_value(M[i], 'M')
            method = self.safe_value(methods, methodType)
            if method is not None:
                A = self.safe_value(M[i], 'A', [])
                for k in range(0, len(A)):
                    update = json.loads(self.inflate(A[k]))
                    method(client, update)
        # resolve invocations by request id
        if 'I' in message:
            self.handle_subscription_status(client, message)
        if 'S' in message:
            self.handle_system_status(client, message)
        keys = list(message.keys())
        numKeys = len(keys)
        if numKeys < 1:
            self.handle_heartbeat(client, message)

    def sign_message(self, client, messageHash, message, params={}):
        # todo: implement signMessage() if needed
        return message

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if api == 'signalr':
            url = self.implode_params(self.urls['api'][api], {
                'hostname': self.hostname,
            }) + '/' + path
            if params:
                url += '?' + self.urlencode(params)
            return {'url': url, 'method': method, 'body': body, 'headers': headers}
        else:
            return super(bittrex, self).sign(path, api, method, params, headers, body)
