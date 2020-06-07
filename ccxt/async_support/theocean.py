# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OrderNotFillable
from ccxt.base.errors import NotSupported
from ccxt.base.errors import ExchangeNotAvailable


class theocean(Exchange):

    def describe(self):
        self.check_required_dependencies()
        return self.deep_extend(super(theocean, self).describe(), {
            'id': 'theocean',
            'name': 'The Ocean',
            'countries': ['US'],
            'rateLimit': 3000,
            'version': 'v1',
            'requiresWeb3': True,
            'timeframes': {
                '5m': '300',
                '15m': '900',
                '1h': '3600',
                '6h': '21600',
                '1d': '86400',
            },
            'has': {
                'cancelAllOrders': True,
                'CORS': False,  # ?
                'fetchClosedOrders': True,
                'fetchOHLCV': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/43103756-d56613ce-8ed7-11e8-924e-68f9d4bcacab.jpg',
                'api': 'https://api.theocean.trade',
                'www': 'https://theocean.trade',
                'doc': 'https://docs.theocean.trade',
                'fees': 'https://theocean.trade/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'fee_components',
                        'token_pairs',
                        'ticker',
                        'tickers',
                        'candlesticks',
                        'candlesticks/intervals',
                        'trade_history',
                        'order_book',
                        'order/{orderHash}',
                        'version',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                        'available_balance',
                        'order_history',
                        'order/unsigned',
                        'order/unsigned/market',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete': [
                        'order/{orderHash}',
                        'order',
                    ],
                },
            },
            'exceptions': {
                'exact': {
                    'Order not found': OrderNotFound,  # {"message":"Order not found","errors":...}
                },
                'broad': {
                    "Price can't exceed 8 digits in precision.": InvalidOrder,  # {"message":"Price can't exceed 8 digits in precision.","type":"paramPrice"}
                    'Order cannot be canceled': InvalidOrder,  # {"message":"Order cannot be canceled","type":"General error"}
                    'Greater than available wallet balance.': InsufficientFunds,
                    'Fillable amount under minimum': InvalidOrder,  # {"message":"Fillable amount under minimum WETH trade size.","type":"paramQuoteTokenAmount"}
                    'Fillable amount over maximum': InvalidOrder,  # {"message":"Fillable amount over maximum TUSD trade size.","type":"paramQuoteTokenAmount"}
                    "Schema validation failed for 'params'": BadRequest,  # # {"message":"Schema validation failed for 'params'"}
                    'Service Temporarily Unavailable': ExchangeNotAvailable,
                },
            },
            'options': {
                'decimals': {},
                'fetchOrderMethod': 'fetch_order_from_history',
            },
        })

    async def fetch_markets(self, params={}):
        markets = await self.publicGetTokenPairs(params)
        #
        #     [
        #       "baseToken": {
        #         "symbol": "ZRX",
        #         "address": "0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570",
        #         "name": "0x Protocol Token",
        #         "decimals": "18",
        #         "minAmount": "10000000000000000000",
        #         "maxAmount": "10000000000000000000000",
        #         "precision": "-8"
        #       },
        #       "quoteToken": {
        #         "symbol": "ETH",
        #         "address": "0xd0a1e359811322d97991e03f863a0c30c2cf029c",
        #         "name": "Ether Token",
        #         "decimals": "18",
        #         "minAmount": "20000000000000000",
        #         "maxAmount": "20000000000000000000",
        #         "precision": "-8"
        #       }
        #     ]
        #
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseToken = self.safe_value(market, 'baseToken', {})
            quoteToken = self.safe_value(market, 'quoteToken', {})
            baseId = self.safe_string(baseToken, 'address')
            quoteId = self.safe_string(quoteToken, 'address')
            base = self.safe_currency_code(self.safe_string(baseToken, 'symbol'))
            quote = self.safe_currency_code(self.safe_string(quoteToken, 'symbol'))
            symbol = base + '/' + quote
            id = baseId + '/' + quoteId
            baseDecimals = self.safe_integer(baseToken, 'decimals')
            quoteDecimals = self.safe_integer(quoteToken, 'decimals')
            self.options['decimals'][base] = baseDecimals
            self.options['decimals'][quote] = quoteDecimals
            precision = {
                'amount': -int(baseToken['precision']),
                'price': -int(quoteToken['precision']),
            }
            amountLimits = {
                'min': self.from_wei(self.safe_string(baseToken, 'minAmount'), baseDecimals),
                'max': self.from_wei(self.safe_string(baseToken, 'maxAmount'), baseDecimals),
            }
            priceLimits = {
                'min': None,
                'max': None,
            }
            costLimits = {
                'min': self.from_wei(self.safe_string(quoteToken, 'minAmount'), quoteDecimals),
                'max': self.from_wei(self.safe_string(quoteToken, 'maxAmount'), quoteDecimals),
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            active = True
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def parse_ohlcv(self, ohlcv, market=None, timeframe='5m', since=None, limit=None):
        #
        #     {
        #         "market_id":"ETH-BTC",
        #         "open":"0.02811",
        #         "close":"0.02811",
        #         "low":"0.02811",
        #         "high":"0.02811",
        #         "base_volume":"0.0005",
        #         "quote_volume":"0.000014055",
        #         "start_time":"2018-11-30T18:19:00.000Z",
        #         "end_time":"2018-11-30T18:20:00.000Z"
        #     }
        #
        baseDecimals = self.safe_integer(self.options['decimals'], market['base'], 18)
        return [
            self.safe_timestamp(ohlcv, 'startTime'),
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.from_wei(self.safe_string(ohlcv, 'baseVolume'), baseDecimals),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        if since is None:
            raise ArgumentsRequired(self.id + ' fetchOHLCV requires a since argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'baseTokenAddress': market['baseId'],
            'quoteTokenAddress': market['quoteId'],
            'interval': self.timeframes[timeframe],
            'startTime': int(since),
        }
        response = await self.publicGetCandlesticks(self.extend(request, params))
        #
        #     [
        #         {
        #             "high": "100.52",
        #             "low": "97.23",
        #             "open": "98.45",
        #             "close": "99.23",
        #             "baseVolume": "2400000000000000000000",
        #             "quoteVolume": "1200000000000000000000",
        #             "startTime": "1512929323784"
        #         },
        #         {
        #             "high": "100.52",
        #             "low": "97.23",
        #             "open": "98.45",
        #             "close": "99.23",
        #             "volume": "2400000000000000000000",
        #             "startTime": "1512929198980"
        #         }
        #     ]
        #
        return self.parse_ohlcvs(response, market)

    async def fetch_balance_by_code(self, code, params={}):
        if not self.walletAddress or (self.walletAddress.find('0x') != 0):
            raise InvalidAddress(self.id + ' fetchBalanceByCode() requires the .walletAddress to be a "0x"-prefixed hexstring like "0xbF2d65B3b2907214EEA3562f21B80f6Ed7220377"')
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'walletAddress': self.walletAddress.lower(),
            'tokenAddress': currency['id'],
        }
        response = await self.privateGetBalance(self.extend(request, params))
        #
        #     {"available":"0","committed":"0","total":"0"}
        #
        decimals = self.safe_integer(self.options['decimals'], code, 18)
        free = self.from_wei(self.safe_string(response, 'available'), decimals)
        used = self.from_wei(self.safe_string(response, 'committed'), decimals)
        total = self.from_wei(self.safe_string(response, 'total'), decimals)
        return {
            'free': free,
            'used': used,
            'total': total,
        }

    async def fetch_balance(self, params={}):
        if not self.walletAddress or (self.walletAddress.find('0x') != 0):
            raise InvalidAddress(self.id + ' fetchBalance() requires the .walletAddress to be a "0x"-prefixed hexstring like "0xbF2d65B3b2907214EEA3562f21B80f6Ed7220377"')
        codes = self.safe_value(self.options, 'fetchBalanceCurrencies')
        if codes is None:
            codes = self.safe_value(params, 'codes')
        if (codes is None) or (not isinstance(codes, list)):
            raise ExchangeError(self.id + ' fetchBalance() requires a `codes` parameter(an array of currency codes)')
        await self.load_markets()
        result = {}
        for i in range(0, len(codes)):
            code = codes[i]
            result[code] = await self.fetch_balance_by_code(code)
        return self.parse_balance(result)

    def parse_bid_ask(self, bidask, priceKey=0, amountKey=1, market=None):
        if market is None:
            raise ArgumentsRequired(self.id + ' parseBidAsk requires a market argument')
        price = float(bidask[priceKey])
        amountDecimals = self.safe_integer(self.options['decimals'], market['base'], 18)
        amount = self.from_wei(bidask[amountKey], 'ether', amountDecimals)
        return [price, amount]

    def parse_order_book(self, orderbook, timestamp=None, bidsKey='bids', asksKey='asks', priceKey=0, amountKey=1, market=None):
        result = {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'nonce': None,
        }
        sides = [bidsKey, asksKey]
        for i in range(0, len(sides)):
            side = sides[i]
            orders = []
            bidasks = self.safe_value(orderbook, side)
            for k in range(0, len(bidasks)):
                orders.append(self.parse_bid_ask(bidasks[k], priceKey, amountKey, market))
            result[side] = orders
        result[bidsKey] = self.sort_by(result[bidsKey], 0, True)
        result[asksKey] = self.sort_by(result[asksKey], 0)
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'baseTokenAddress': market['baseId'],
            'quoteTokenAddress': market['quoteId'],
        }
        if limit is not None:
            request['depth'] = limit
        response = await self.publicGetOrderBook(self.extend(request, params))
        #
        #     {
        #       "bids": [
        #         {orderHash: '0xe2b7f80198edb561cc66cd85cb8e5f420073cf1e5143193d8add8774bd8236c4',
        #           price: '30',
        #           availableAmount: '500000000000000000',
        #           creationTimestamp: '1547193525',
        #           expirationTimestampInSec: '1549789124'
        #         }
        #       ],
        #       "asks": [
        #         {orderHash: '0xe2b7f80198edb561cc66cd85cb8e5f420073cf1e5143193d8add8774bd8236c4',
        #           price: '30',
        #           availableAmount: '500000000000000000',
        #           creationTimestamp: '1547193525',
        #           expirationTimestampInSec: '1549789124'
        #         }
        #       ]
        #     }
        #
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'availableAmount', market)

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "bid": "0.00050915",
        #         "ask": "0.00054134",
        #         "last": "0.00052718",
        #         "volume": "3000000000000000000",
        #         "timestamp": "1512929327792"
        #     }
        #
        timestamp = int(self.safe_integer(ticker, 'timestamp') / 1000)
        symbol = None
        base = None
        if market is not None:
            symbol = market['symbol']
            base = market['base']
        baseDecimals = self.safe_integer(self.options['decimals'], base, 18)
        baseVolume = self.from_wei(self.safe_string(ticker, 'volume'), baseDecimals)
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_float(ticker, 'priceChange'),
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
        #
        #     [{
        #     "baseTokenAddress": "0xa8e9fa8f91e5ae138c74648c9c304f1c75003a8d",
        #     "quoteTokenAddress": "0xc00fd9820cd2898cc4c054b7bf142de637ad129a",
        #     "ticker": {
        #         "bid": "0.00050915",
        #         "ask": "0.00054134",
        #         "last": "0.00052718",
        #         "volume": "3000000000000000000",
        #         "timestamp": "1512929327792"
        #     }
        #     }]
        #
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            baseId = self.safe_string(ticker, 'baseTokenAddress')
            quoteId = self.safe_string(ticker, 'quoteTokenAddress')
            marketId = baseId + '/' + quoteId
            market = None
            symbol = marketId
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker['ticker'], market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'baseTokenAddress': market['baseId'],
            'quoteTokenAddress': market['quoteId'],
        }
        response = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades
        #
        #     {
        #         "id": "37212",
        #         "transactionHash": "0x5e6e75e1aa681b51b034296f62ac19be7460411a2ad94042dd8ba637e13eac0c",
        #         "amount": "300000000000000000",
        #         "price": "0.00052718",
        # ------- they also have a "confirmed" status here ↓ -----------------
        #         "status": "filled",  # filled | settled | failed
        #         "lastUpdated": "1520265048996"
        #     }
        #
        # parseOrder trades(timeline "actions", "fills")
        #
        #     {     action: "confirmed",
        #            amount: "1000000000000000000",
        #          intentID: "MARKET_INTENT:90jjw2s7gj90jjw2s7gkjjw2s7gl",
        #            txHash: "0x043488fdc3f995bf9e632a32424e41ed126de90f8cb340a1ff006c2a74ca8336",
        #       blockNumber: "8094822",
        #         timestamp: "1532261686"                                                          }
        #
        timestamp = self.safe_integer(trade, 'lastUpdated')
        if timestamp is not None:
            timestamp /= 1000
        price = self.safe_float(trade, 'price')
        id = self.safe_string(trade, 'id')
        side = self.safe_string(trade, 'side')
        symbol = None
        base = None
        if market is not None:
            symbol = market['symbol']
            base = market['base']
        baseDecimals = self.safe_integer(self.options['decimals'], base, 18)
        amount = self.from_wei(self.safe_string(trade, 'amount'), baseDecimals)
        cost = None
        if amount is not None and price is not None:
            cost = amount * price
        takerOrMaker = 'taker'
        return {
            'id': id,
            'order': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'baseTokenAddress': market['baseId'],
            'quoteTokenAddress': market['quoteId'],
        }
        response = await self.publicGetTradeHistory(self.extend(request, params))
        #
        #     [
        #       {
        #         "id": "37212",
        #         "transactionHash": "0x5e6e75e1aa681b51b034296f62ac19be7460411a2ad94042dd8ba637e13eac0c",
        #         "amount": "300000000000000000",
        #         "price": "0.00052718",
        #         "status": "filled",  # filled | settled | failed
        #         "lastUpdated": "1520265048996"
        #       }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        errorMessage = self.id + ' createOrder() requires `exchange.walletAddress` and `exchange.privateKey`. The .walletAddress should be a "0x"-prefixed hexstring like "0xbF2d65B3b2907214EEA3562f21B80f6Ed7220377". The .privateKey for that wallet should be a "0x"-prefixed hexstring like "0xe4f40d465efa94c98aec1a51f574329344c772c1bce33be07fa20a56795fdd09".'
        if not self.walletAddress or (self.walletAddress.find('0x') != 0):
            raise InvalidAddress(errorMessage)
        if not self.privateKey or (self.privateKey.find('0x') != 0):
            raise InvalidAddress(errorMessage)
        orderParams = await self.fetch_order_params_to_sign(symbol, type, side, amount, price, params)
        unsignedOrder = orderParams['unsignedZeroExOrder']
        if unsignedOrder is None:
            raise OrderNotFillable(self.id + ' ' + type + ' order to ' + side + ' ' + symbol + ' is not fillable at the moment')
        signedOrder = await self.sign_zero_ex_order_v2(unsignedOrder, self.privateKey)
        id = self.safe_string(signedOrder, 'orderHash')
        await self.post_signed_order(signedOrder, orderParams, params)
        order = await self.fetch_order(id)
        order['type'] = type
        return order

    async def fetch_order_params_to_sign(self, symbol, type, side, amount, price=None, params={}):
        if side != 'buy' and side != 'sell':
            raise ExchangeError(side + ' is not valid side param. Use \'buy\' or \'sell\'')
        if type != 'market' and type != 'limit':
            raise ExchangeError(type + ' is not valid type param. Use \'market\' or \'limit\'')
        if type == 'limit' and price is None:
            raise ExchangeError('Price is not provided for limit order')
        await self.load_markets()
        market = self.market(symbol)
        baseDecimals = self.safe_integer(self.options['decimals'], market['base'], 18)
        request = {
            'walletAddress': self.walletAddress.lower(),  # Your Wallet Address
            'baseTokenAddress': market['baseId'],  # Base token address
            'quoteTokenAddress': market['quoteId'],  # Quote token address
            'side': side,  # "buy" or "sell"
            'amount': self.to_wei(self.amount_to_precision(symbol, amount), baseDecimals),  # Base token amount in wei
        }
        method = None
        if type == 'limit':
            method = 'privateGetOrderUnsigned'
            request['price'] = self.price_to_precision(symbol, price)
        elif type == 'market':
            method = 'privateGetOrderUnsignedMarket'
        else:
            raise ExchangeError('Unsupported order type: ' + type)
        response = await getattr(self, method)(self.extend(request, params))
        return response

    async def post_signed_order(self, signedOrder, requestParams, params={}):
        request = requestParams
        request['signedZeroExOrder'] = signedOrder
        request = self.omit(request, 'unsignedZeroExOrder')
        response = await self.privatePostOrder(self.extend(request, params))
        return response

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderHash': id,
        }
        response = await self.privateDeleteOrderOrderHash(self.extend(request, params))
        #
        #     {
        #       "canceledOrder": {
        #         "orderHash": "0x3d6b287c1dc79262d2391ae2ca9d050fdbbab2c8b3180e4a46f9f321a7f1d7a9",
        #         "amount": "100000000000"
        #       }
        #     }
        #
        market = None
        if symbol is not None:
            market = self.market(symbol)
        return self.extend(self.parse_order(response['canceledOrder'], market), {
            'status': 'canceled',
        })

    async def cancel_all_orders(self, symbol=None, params={}):
        response = await self.privateDeleteOrder(params)
        #
        #     [{
        #       "canceledOrder": {
        #         "orderHash": "0x3d6b287c1dc79262d2391ae2ca9d050fdbbab2c8b3180e4a46f9f321a7f1d7a9",
        #         "amount": "100000000000"
        #       }
        #     }]
        #
        return response

    def parse_order(self, order, market=None):
        zeroExOrder = self.safe_value(order, 'zeroExOrder')
        id = self.safe_string(order, 'orderHash')
        if (id is None) and (zeroExOrder is not None):
            id = self.safe_string(zeroExOrder, 'orderHash')
        side = self.safe_string(order, 'side')
        type = self.safe_string(order, 'type')  # injected from outside
        timestamp = self.safe_integer(order, 'creationTimestamp')
        if timestamp != 'None':
            timestamp = int(timestamp / 1000)
        symbol = None
        baseId = self.safe_string(order, 'baseTokenAddress')
        quoteId = self.safe_string(order, 'quoteTokenAddress')
        marketId = None
        if baseId is not None and quoteId is not None:
            marketId = baseId + '/' + quoteId
        market = self.safe_value(self.markets_by_id, marketId, market)
        base = None
        if market is not None:
            symbol = market['symbol']
            base = market['base']
        baseDecimals = self.safe_integer(self.options['decimals'], base, 18)
        price = self.safe_float(order, 'price')
        filledAmount = self.from_wei(self.safe_string(order, 'filledAmount'), baseDecimals)
        settledAmount = self.from_wei(self.safe_string(order, 'settledAmount'), baseDecimals)
        confirmedAmount = self.from_wei(self.safe_string(order, 'confirmedAmount'), baseDecimals)
        failedAmount = self.from_wei(self.safe_string(order, 'failedAmount'), baseDecimals)
        deadAmount = self.from_wei(self.safe_string(order, 'deadAmount'), baseDecimals)
        prunedAmount = self.from_wei(self.safe_string(order, 'prunedAmount'), baseDecimals)
        amount = self.from_wei(self.safe_string(order, 'initialAmount'), baseDecimals)
        filled = self.sum(filledAmount, settledAmount, confirmedAmount)
        remaining = None
        lastTradeTimestamp = None
        timeline = self.safe_value(order, 'timeline')
        trades = None
        status = None
        if timeline is not None:
            numEvents = len(timeline)
            if numEvents > 0:
                timelineEventsGroupedByAction = self.group_by(timeline, 'action')
                if 'error' in timelineEventsGroupedByAction:
                    status = 'failed'
                if 'filled' in timelineEventsGroupedByAction:
                    fillEvents = self.safe_value(timelineEventsGroupedByAction, 'filled')
                    numFillEvents = len(fillEvents)
                    lastTradeTimestamp = self.safe_integer(fillEvents[numFillEvents - 1], 'timestamp')
                    lastTradeTimestamp = lastTradeTimestamp if (lastTradeTimestamp is not None) else lastTradeTimestamp
                    trades = []
                    for i in range(0, numFillEvents):
                        trade = self.parse_trade(self.extend(fillEvents[i], {
                            'price': price,
                        }), market)
                        trades.append(self.extend(trade, {
                            'order': id,
                            'type': type,
                            'side': side,
                        }))
        cost = None
        if filled is not None:
            if remaining is None:
                if amount is not None:
                    remaining = amount - filled
            if price is not None:
                cost = filled * price
        fee = None
        feeCost = self.safe_string(order, 'feeAmount')
        if feeCost is not None:
            feeOption = self.safe_string(order, 'feeOption')
            feeCurrency = None
            if feeOption == 'feeInNative':
                if market is not None:
                    feeCurrency = market['base']
            elif feeOption == 'feeInZRX':
                feeCurrency = 'ZRX'
            else:
                raise NotSupported(self.id + ' encountered an unsupported order fee option: ' + feeOption)
            feeDecimals = self.safe_integer(self.options['decimals'], feeCurrency, 18)
            fee = {
                'cost': self.from_wei(feeCost, feeDecimals),
                'currency': feeCurrency,
            }
        amountPrecision = market['precision']['amount'] if market else 8
        if remaining is not None:
            if status is None:
                status = 'open'
                rest = remaining - failedAmount - deadAmount - prunedAmount
                if rest < math.pow(10, -amountPrecision):
                    status = 'canceled' if (filled < amount) else 'closed'
        result = {
            'info': order,
            'id': id,
            'clientOrderId': None,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'status': status,
            'fee': fee,
            'trades': trades,
            'average': None,
        }
        return result

    async def fetch_open_order(self, id, symbol=None, params={}):
        method = self.options['fetchOrderMethod']
        return await getattr(self, method)(id, symbol, self.extend({
            'openAmount': 1,
        }, params))

    async def fetch_closed_order(self, id, symbol=None, params={}):
        method = self.options['fetchOrderMethod']
        return await getattr(self, method)(id, symbol, self.extend(params))

    async def fetch_order_from_history(self, id, symbol=None, params={}):
        request = {
            'orderHash': id,
        }
        orders = await self.fetch_orders(symbol, None, None, self.extend(request, params))
        ordersById = self.index_by(orders, 'id')
        if id in ordersById:
            return ordersById[id]
        raise OrderNotFound(self.id + ' could not find order ' + id + ' in order history')

    async def fetch_order_by_id(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderHash': id,
        }
        response = await self.publicGetOrderOrderHash(self.extend(request, params))
        #  {
        #   baseTokenAddress: '0xb18845c260f680d5b9d84649638813e342e4f8c9',
        #   quoteTokenAddress: '0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570',
        #   side: 'sell',
        #   price: '30',
        #   feeTokenAddress: '0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570',
        #   amount: '500000000000000000',
        #   created: '1547194003',
        #   expires: '1549786003',
        #   zeroExOrder: {
        #     salt: '71810414258284992779348693906799008280152689028521273772736250669496045815907',
        #     maker: '0xfa1a3371bcbfcf3deaa8a6f67784bfbe5b886d7f',
        #     taker: '0x77b18613579d49f252bd237ef113884eb37a7090',
        #     makerFee: '0',
        #     takerFee: '0',
        #     orderHash: '0x368540323af55868dd9ce6ac248e6a91d9b7595252ca061c4ada7612b09af1cf',
        #     feeRecipient: '0x88a64b5e882e5ad851bea5e7a3c8ba7c523fecbe',
        #     makerTokenAmount: '500000000000000000',
        #     takerTokenAmount: '14845250714350000000',
        #     makerTokenAddress: '0xb18845c260f680d5b9d84649638813e342e4f8c9',
        #     takerTokenAddress: '0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570',
        #     exchangeContractAddress: '0x35dd2932454449b14cee11a94d3674a936d5d7b2',
        #     expirationUnixTimestampSec: '1549789602'
        #   },
        #   feeAmount: '154749285650000000',
        #   feeOption: 'feeInNative',
        #   cancelAfter: '1549786003'
        #  }
        return self.parse_order(response)

    async def fetch_order(self, id, symbol=None, params={}):
        request = {
            'orderHash': id,
        }
        orders = await self.fetch_orders(symbol, None, None, self.extend(request, params))
        numOrders = len(orders)
        if numOrders != 1:
            raise OrderNotFound(self.id + ' order ' + id + ' not found')
        return orders[0]

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['baseTokenAddress'] = market['baseId']
            request['quoteTokenAddress'] = market['quoteId']
        if limit is not None:
            request['limit'] = limit
        response = await self.privateGetOrderHistory(self.extend(request, params))
        #
        #     [
        #       {
        #         "orderHash": "0x94629386298dee69ae63cd3e414336ae153b3f02cffb9ffc53ad71e166615618",
        #         "baseTokenAddress": "0x323b5d4c32345ced77393b3530b1eed0f346429d",
        #         "quoteTokenAddress": "0xef7fff64389b814a946f3e92105513705ca6b990",
        #         "side": "buy",
        #         "openAmount": "10000000000000000000",
        #         "filledAmount": "0",
        #         "reservedAmount": "0",
        #         "settledAmount": "0",
        #         "confirmedAmount": "0",
        #         "deadAmount": "0",
        #         "price": "0.00050915",
        #         "timeline": [
        #           {
        #             "action": "placed",
        #             "amount": "10000000000000000000",
        #             "timestamp": "1512929327792"
        #           }
        #         ]
        #       }
        #     ]
        #
        return self.parse_orders(response, None, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'openAmount': 1,  # returns open orders with remaining openAmount >= 1
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'openAmount': 0,  # returns closed orders with remaining openAmount == 0
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            timestamp = str(self.seconds())
            prehash = self.apiKey + timestamp + method
            if method == 'POST':
                body = self.json(query)
                prehash += body
            else:
                if query:
                    url += '?' + self.urlencode(query)
                prehash += self.json({})
            signature = self.hmac(self.encode(prehash), self.encode(self.secret), hashlib.sha256, 'base64')
            headers = {
                'TOX-ACCESS-KEY': self.apiKey,
                'TOX-ACCESS-SIGN': signature,
                'TOX-ACCESS-TIMESTAMP': timestamp,
                'Content-Type': 'application/json',
            }
        elif api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        # code 401 and plain body 'Authentication failed'(with single quotes)
        # self error is sent if you do not submit a proper Content-Type
        if body == "'Authentication failed'":
            raise AuthenticationError(self.id + ' ' + body)
        message = self.safe_string(response, 'message')
        if message is not None:
            #
            # {"message":"Schema validation failed for 'query'","errors":[{"name":"required","argument":"startTime","message":"requires property \"startTime\"","instance":{"baseTokenAddress":"0x6ff6c0ff1d68b964901f986d4c9fa3ac68346570","quoteTokenAddress":"0xd0a1e359811322d97991e03f863a0c30c2cf029c","interval":"300"},"property":"instance"}]}
            # {"message":"Logic validation failed for 'query'","errors":[{"message":"startTime should be between 0 and current date","type":"startTime"}]}
            # {"message":"Order not found","errors":[]}
            # {"message":"Orderbook exhausted for intent MARKET_INTENT:8yjjzd8b0e8yjjzd8b0fjjzd8b0g"}
            # {"message":"Intent validation failed.","errors":[{"message":"Greater than available wallet balance.","type":"walletBaseTokenAmount"}]}
            # {"message":"Schema validation failed for 'body'","errors":[{"name":"anyOf","argument":["[subschema 0]","[subschema 1]","[subschema 2]"],"message":"is not any of [subschema 0],[subschema 1],[subschema 2]","instance":{"signedTargetOrder":{"error":{"message":"Unsigned target order validation failed.","errors":[{"message":"Greater than available wallet balance.","type":"walletBaseTokenAmount"}]},"maker":"0x1709c02cd7327d391a39a7671af8a91a1ef8a47b","orderHash":"0xda007ea8b5eca71ac96fe4072f7c1209bb151d898a9cc89bbeaa594f0491ee49","ecSignature":{"v":27,"r":"0xb23ce6c4a7b5d51d77e2d00f6d1d472a3b2e72d5b2be1510cfeb122f9366b79e","s":"0x07d274e6d7a00b65fc3026c2f9019215b1e47a5ac4d1f05e03f90550d27109be"}}},"property":"instance"}]}
            # {"message":"Schema validation failed for 'params'","errors":[{"name":"pattern","argument":"^0x[0-9a-fA-F]{64}$","message":"does not match pattern \"^0x[0-9a-fA-F]{64}$\"","instance":"1","property":"instance.orderHash"}]}
            #
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
            raise ExchangeError(feedback)  # unknown message
