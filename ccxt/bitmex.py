# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable


class bitmex (Exchange):

    def describe(self):
        return self.deep_extend(super(bitmex, self).describe(), {
            'id': 'bitmex',
            'name': 'BitMEX',
            'countries': ['SC'],  # Seychelles
            'version': 'v1',
            'userAgent': None,
            'rateLimit': 2000,
            'has': {
                'CORS': False,
                'fetchOHLCV': True,
                'withdraw': True,
                'editOrder': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '1h': '1h',
                '1d': '1d',
            },
            'urls': {
                'test': 'https://testnet.bitmex.com',
                'logo': 'https://user-images.githubusercontent.com/1294454/27766319-f653c6e6-5ed4-11e7-933d-f0bc3699ae8f.jpg',
                'api': 'https://www.bitmex.com',
                'www': 'https://www.bitmex.com',
                'doc': [
                    'https://www.bitmex.com/app/apiOverview',
                    'https://github.com/BitMEX/api-connectors/tree/master/official-http',
                ],
                'fees': 'https://www.bitmex.com/app/fees',
                'referral': 'https://www.bitmex.com/register/rm3C16',
            },
            'api': {
                'public': {
                    'get': [
                        'announcement',
                        'announcement/urgent',
                        'funding',
                        'instrument',
                        'instrument/active',
                        'instrument/activeAndIndices',
                        'instrument/activeIntervals',
                        'instrument/compositeIndex',
                        'instrument/indices',
                        'insurance',
                        'leaderboard',
                        'liquidation',
                        'orderBook',
                        'orderBook/L2',
                        'quote',
                        'quote/bucketed',
                        'schema',
                        'schema/websocketHelp',
                        'settlement',
                        'stats',
                        'stats/history',
                        'trade',
                        'trade/bucketed',
                    ],
                },
                'private': {
                    'get': [
                        'apiKey',
                        'chat',
                        'chat/channels',
                        'chat/connected',
                        'execution',
                        'execution/tradeHistory',
                        'notification',
                        'order',
                        'position',
                        'user',
                        'user/affiliateStatus',
                        'user/checkReferralCode',
                        'user/commission',
                        'user/depositAddress',
                        'user/margin',
                        'user/minWithdrawalFee',
                        'user/wallet',
                        'user/walletHistory',
                        'user/walletSummary',
                    ],
                    'post': [
                        'apiKey',
                        'apiKey/disable',
                        'apiKey/enable',
                        'chat',
                        'order',
                        'order/bulk',
                        'order/cancelAllAfter',
                        'order/closePosition',
                        'position/isolate',
                        'position/leverage',
                        'position/riskLimit',
                        'position/transferMargin',
                        'user/cancelWithdrawal',
                        'user/confirmEmail',
                        'user/confirmEnableTFA',
                        'user/confirmWithdrawal',
                        'user/disableTFA',
                        'user/logout',
                        'user/logoutAll',
                        'user/preferences',
                        'user/requestEnableTFA',
                        'user/requestWithdrawal',
                    ],
                    'put': [
                        'order',
                        'order/bulk',
                        'user',
                    ],
                    'delete': [
                        'apiKey',
                        'order',
                        'order/all',
                    ],
                },
            },
            'exceptions': {
                'exact': {
                    'Invalid API Key.': AuthenticationError,
                    'Access Denied': PermissionDenied,
                    'Duplicate clOrdID': InvalidOrder,
                    'Signature not valid': AuthenticationError,
                    'orderQty is invalid': InvalidOrder,
                    'Invalid price': InvalidOrder,
                    'Invalid stopPx for ordType': InvalidOrder,
                },
                'broad': {
                    'overloaded': ExchangeNotAvailable,
                    'Account has insufficient Available Balance': InsufficientFunds,
                },
            },
            'options': {
                # https://blog.bitmex.com/api_announcement/deprecation-of-api-nonce-header/
                # https://github.com/ccxt/ccxt/issues/4789
                'api-expires': 5,  # in seconds
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetInstrumentActiveAndIndices(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            active = (market['state'] != 'Unlisted')
            id = market['symbol']
            baseId = market['underlying']
            quoteId = market['quoteCurrency']
            basequote = baseId + quoteId
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            swap = (id == basequote)
            # 'positionCurrency' may be empty("", as Bitmex currently returns for ETHUSD)
            # so let's take the quote currency first and then adjust if needed
            positionId = self.safe_string_2(market, 'positionCurrency', 'quoteCurrency')
            type = None
            future = False
            prediction = False
            position = self.common_currency_code(positionId)
            symbol = id
            if swap:
                type = 'swap'
                symbol = base + '/' + quote
            elif id.find('B_') >= 0:
                prediction = True
                type = 'prediction'
            else:
                future = True
                type = 'future'
            precision = {
                'amount': None,
                'price': None,
            }
            lotSize = self.safe_float(market, 'lotSize')
            tickSize = self.safe_float(market, 'tickSize')
            if lotSize is not None:
                precision['amount'] = self.precision_from_string(self.truncate_to_string(lotSize, 16))
            if tickSize is not None:
                precision['price'] = self.precision_from_string(self.truncate_to_string(tickSize, 16))
            limits = {
                'amount': {
                    'min': None,
                    'max': None,
                },
                'price': {
                    'min': tickSize,
                    'max': self.safe_float(market, 'maxPrice'),
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            limitField = 'cost' if (position == quote) else 'amount'
            limits[limitField] = {
                'min': lotSize,
                'max': self.safe_float(market, 'maxOrderQty'),
            }
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
                'taker': market['takerFee'],
                'maker': market['makerFee'],
                'type': type,
                'spot': False,
                'swap': swap,
                'future': future,
                'prediction': prediction,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        request = {'currency': 'all'}
        response = self.privateGetUserMargin(self.extend(request, params))
        result = {'info': response}
        for b in range(0, len(response)):
            balance = response[b]
            currencyId = self.safe_string(balance, 'currency')
            currencyId = currencyId.upper()
            code = self.common_currency_code(currencyId)
            account = {
                'free': balance['availableMargin'],
                'used': 0.0,
                'total': balance['marginBalance'],
            }
            if code == 'BTC':
                account['free'] = account['free'] * 0.00000001
                account['total'] = account['total'] * 0.00000001
            account['used'] = account['total'] - account['free']
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['depth'] = limit
        orderbook = self.publicGetOrderBookL2(self.extend(request, params))
        result = {
            'bids': [],
            'asks': [],
            'timestamp': None,
            'datetime': None,
            'nonce': None,
        }
        for o in range(0, len(orderbook)):
            order = orderbook[o]
            side = 'asks' if (order['side'] == 'Sell') else 'bids'
            amount = self.safe_float(order, 'size')
            price = self.safe_float(order, 'price')
            # https://github.com/ccxt/ccxt/issues/4926
            # https://github.com/ccxt/ccxt/issues/4927
            # the exchange sometimes returns null price in the orderbook
            if price is not None:
                result[side].append([price, amount])
        result['bids'] = self.sort_by(result['bids'], 0, True)
        result['asks'] = self.sort_by(result['asks'], 0)
        return result

    def fetch_order(self, id, symbol=None, params={}):
        filter = {'filter': {'orderID': id}}
        result = self.fetch_orders(symbol, None, None, self.deep_extend(filter, params))
        numResults = len(result)
        if numResults == 1:
            return result[0]
        raise OrderNotFound(self.id + ': The order ' + id + ' not found.')

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startTime'] = self.iso8601(since)
        if limit is not None:
            request['count'] = limit
        request = self.deep_extend(request, params)
        # why the hassle? urlencode in python is kinda broken for nested dicts.
        # E.g. self.urlencode({"filter": {"open": True}}) will return "filter={'open':+True}"
        # Bitmex doesn't like that. Hence resorting to self hack.
        if 'filter' in request:
            request['filter'] = self.json(request['filter'])
        response = self.privateGetOrder(request)
        return self.parse_orders(response, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        filter_params = {'filter': {'open': True}}
        return self.fetch_orders(symbol, since, limit, self.deep_extend(filter_params, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        # Bitmex barfs if you set 'open': False in the filter...
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startTime'] = self.iso8601(since)
        if limit is not None:
            request['count'] = limit
        request = self.deep_extend(request, params)
        # why the hassle? urlencode in python is kinda broken for nested dicts.
        # E.g. self.urlencode({"filter": {"open": True}}) will return "filter={'open':+True}"
        # Bitmex doesn't like that. Hence resorting to self hack.
        if 'filter' in request:
            request['filter'] = self.json(request['filter'])
        response = self.privateGetExecutionTradeHistory(request)
        #
        #     [
        #         {
        #             "execID": "string",
        #             "orderID": "string",
        #             "clOrdID": "string",
        #             "clOrdLinkID": "string",
        #             "account": 0,
        #             "symbol": "string",
        #             "side": "string",
        #             "lastQty": 0,
        #             "lastPx": 0,
        #             "underlyingLastPx": 0,
        #             "lastMkt": "string",
        #             "lastLiquidityInd": "string",
        #             "simpleOrderQty": 0,
        #             "orderQty": 0,
        #             "price": 0,
        #             "displayQty": 0,
        #             "stopPx": 0,
        #             "pegOffsetValue": 0,
        #             "pegPriceType": "string",
        #             "currency": "string",
        #             "settlCurrency": "string",
        #             "execType": "string",
        #             "ordType": "string",
        #             "timeInForce": "string",
        #             "execInst": "string",
        #             "contingencyType": "string",
        #             "exDestination": "string",
        #             "ordStatus": "string",
        #             "triggered": "string",
        #             "workingIndicator": True,
        #             "ordRejReason": "string",
        #             "simpleLeavesQty": 0,
        #             "leavesQty": 0,
        #             "simpleCumQty": 0,
        #             "cumQty": 0,
        #             "avgPx": 0,
        #             "commission": 0,
        #             "tradePublishIndicator": "string",
        #             "multiLegReportingType": "string",
        #             "text": "string",
        #             "trdMatchID": "string",
        #             "execCost": 0,
        #             "execComm": 0,
        #             "homeNotional": 0,
        #             "foreignNotional": 0,
        #             "transactTime": "2019-03-05T12:47:02.762Z",
        #             "timestamp": "2019-03-05T12:47:02.762Z"
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        if not market['active']:
            raise ExchangeError(self.id + ': symbol ' + symbol + ' is delisted')
        tickers = self.fetch_tickers([symbol], params)
        ticker = self.safe_value(tickers, symbol)
        if ticker is None:
            raise ExchangeError(self.id + ' ticker symbol ' + symbol + ' not found')
        return ticker

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetInstrumentActiveAndIndices(params)
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = self.safe_string(ticker, 'symbol')
            if symbol is not None:
                result[symbol] = ticker
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     {                        symbol: "ETHH19",
        #                           rootSymbol: "ETH",
        #                                state: "Open",
        #                                  typ: "FFCCSX",
        #                              listing: "2018-12-17T04:00:00.000Z",
        #                                front: "2019-02-22T12:00:00.000Z",
        #                               expiry: "2019-03-29T12:00:00.000Z",
        #                               settle: "2019-03-29T12:00:00.000Z",
        #                       relistInterval:  null,
        #                           inverseLeg: "",
        #                              sellLeg: "",
        #                               buyLeg: "",
        #                     optionStrikePcnt:  null,
        #                    optionStrikeRound:  null,
        #                    optionStrikePrice:  null,
        #                     optionMultiplier:  null,
        #                     positionCurrency: "ETH",
        #                           underlying: "ETH",
        #                        quoteCurrency: "XBT",
        #                     underlyingSymbol: "ETHXBT=",
        #                            reference: "BMEX",
        #                      referenceSymbol: ".BETHXBT30M",
        #                         calcInterval:  null,
        #                      publishInterval:  null,
        #                          publishTime:  null,
        #                          maxOrderQty:  100000000,
        #                             maxPrice:  10,
        #                              lotSize:  1,
        #                             tickSize:  0.00001,
        #                           multiplier:  100000000,
        #                        settlCurrency: "XBt",
        #       underlyingToPositionMultiplier:  1,
        #         underlyingToSettleMultiplier:  null,
        #              quoteToSettleMultiplier:  100000000,
        #                             isQuanto:  False,
        #                            isInverse:  False,
        #                           initMargin:  0.02,
        #                          maintMargin:  0.01,
        #                            riskLimit:  5000000000,
        #                             riskStep:  5000000000,
        #                                limit:  null,
        #                               capped:  False,
        #                                taxed:  True,
        #                           deleverage:  True,
        #                             makerFee:  -0.0005,
        #                             takerFee:  0.0025,
        #                        settlementFee:  0,
        #                         insuranceFee:  0,
        #                    fundingBaseSymbol: "",
        #                   fundingQuoteSymbol: "",
        #                 fundingPremiumSymbol: "",
        #                     fundingTimestamp:  null,
        #                      fundingInterval:  null,
        #                          fundingRate:  null,
        #                indicativeFundingRate:  null,
        #                   rebalanceTimestamp:  null,
        #                    rebalanceInterval:  null,
        #                     openingTimestamp: "2019-02-13T08:00:00.000Z",
        #                     closingTimestamp: "2019-02-13T09:00:00.000Z",
        #                      sessionInterval: "2000-01-01T01:00:00.000Z",
        #                       prevClosePrice:  0.03347,
        #                       limitDownPrice:  null,
        #                         limitUpPrice:  null,
        #               bankruptLimitDownPrice:  null,
        #                 bankruptLimitUpPrice:  null,
        #                      prevTotalVolume:  1386531,
        #                          totalVolume:  1387062,
        #                               volume:  531,
        #                            volume24h:  17118,
        #                    prevTotalTurnover:  4741294246000,
        #                        totalTurnover:  4743103466000,
        #                             turnover:  1809220000,
        #                          turnover24h:  57919845000,
        #                      homeNotional24h:  17118,
        #                   foreignNotional24h:  579.19845,
        #                         prevPrice24h:  0.03349,
        #                                 vwap:  0.03383564,
        #                            highPrice:  0.03458,
        #                             lowPrice:  0.03329,
        #                            lastPrice:  0.03406,
        #                   lastPriceProtected:  0.03406,
        #                    lastTickDirection: "ZeroMinusTick",
        #                       lastChangePcnt:  0.017,
        #                             bidPrice:  0.03406,
        #                             midPrice:  0.034065,
        #                             askPrice:  0.03407,
        #                       impactBidPrice:  0.03406,
        #                       impactMidPrice:  0.034065,
        #                       impactAskPrice:  0.03407,
        #                         hasLiquidity:  True,
        #                         openInterest:  83679,
        #                            openValue:  285010674000,
        #                           fairMethod: "ImpactMidPrice",
        #                        fairBasisRate:  0,
        #                            fairBasis:  0,
        #                            fairPrice:  0.03406,
        #                           markMethod: "FairPrice",
        #                            markPrice:  0.03406,
        #                    indicativeTaxRate:  0,
        #                indicativeSettlePrice:  0.03406,
        #                optionUnderlyingPrice:  null,
        #                         settledPrice:  null,
        #                            timestamp: "2019-02-13T08:40:30.000Z",
        #     }
        #
        symbol = None
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_value(self.markets_by_id, marketId, market)
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(ticker, 'timestamp'))
        open = self.safe_float(ticker, 'prevPrice24h')
        last = self.safe_float(ticker, 'lastPrice')
        change = None
        percentage = None
        if last is not None and open is not None:
            change = last - open
            if open > 0:
                percentage = change / open * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highPrice'),
            'low': self.safe_float(ticker, 'lowPrice'),
            'bid': self.safe_float(ticker, 'bidPrice'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'askPrice'),
            'askVolume': None,
            'vwap': self.safe_float(ticker, 'vwap'),
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': self.sum(open, last) / 2,
            'baseVolume': self.safe_float(ticker, 'homeNotional24h'),
            'quoteVolume': self.safe_float(ticker, 'foreignNotional24h'),
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['timestamp'])
        return [
            timestamp,
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'volume'),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        # send JSON key/value pairs, such as {"key": "value"}
        # filter by individual fields and do advanced queries on timestamps
        # filter = {'key': 'value'}
        # send a bare series(e.g. XBU) to nearest expiring contract in that series
        # you can also send a timeframe, e.g. XBU:monthly
        # timeframes: daily, weekly, monthly, quarterly, and biquarterly
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'binSize': self.timeframes[timeframe],
            'partial': True,     # True == include yet-incomplete current bins
            # 'filter': filter,  # filter by individual fields and do advanced queries
            # 'columns': [],    # will return all columns if omitted
            # 'start': 0,       # starting point for results(wtf?)
            # 'reverse': False,  # True == newest first
            # 'endTime': '',    # ending date filter for results
        }
        if limit is not None:
            request['count'] = limit  # default 100, max 500
        # if since is not set, they will return candles starting from 2017-01-01
        if since is not None:
            ymdhms = self.ymdhms(since)
            request['startTime'] = ymdhms  # starting date filter for results
        response = self.publicGetTradeBucketed(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         timestamp: '2018-08-28T00:00:02.735Z',
        #         symbol: 'XBTUSD',
        #         side: 'Buy',
        #         size: 2000,
        #         price: 6906.5,
        #         tickDirection: 'PlusTick',
        #         trdMatchID: 'b9a42432-0a46-6a2f-5ecc-c32e9ca4baf8',
        #         grossValue: 28958000,
        #         homeNotional: 0.28958,
        #         foreignNotional: 2000
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "execID": "string",
        #         "orderID": "string",
        #         "clOrdID": "string",
        #         "clOrdLinkID": "string",
        #         "account": 0,
        #         "symbol": "string",
        #         "side": "string",
        #         "lastQty": 0,
        #         "lastPx": 0,
        #         "underlyingLastPx": 0,
        #         "lastMkt": "string",
        #         "lastLiquidityInd": "string",
        #         "simpleOrderQty": 0,
        #         "orderQty": 0,
        #         "price": 0,
        #         "displayQty": 0,
        #         "stopPx": 0,
        #         "pegOffsetValue": 0,
        #         "pegPriceType": "string",
        #         "currency": "string",
        #         "settlCurrency": "string",
        #         "execType": "string",
        #         "ordType": "string",
        #         "timeInForce": "string",
        #         "execInst": "string",
        #         "contingencyType": "string",
        #         "exDestination": "string",
        #         "ordStatus": "string",
        #         "triggered": "string",
        #         "workingIndicator": True,
        #         "ordRejReason": "string",
        #         "simpleLeavesQty": 0,
        #         "leavesQty": 0,
        #         "simpleCumQty": 0,
        #         "cumQty": 0,
        #         "avgPx": 0,
        #         "commission": 0,
        #         "tradePublishIndicator": "string",
        #         "multiLegReportingType": "string",
        #         "text": "string",
        #         "trdMatchID": "string",
        #         "execCost": 0,
        #         "execComm": 0,
        #         "homeNotional": 0,
        #         "foreignNotional": 0,
        #         "transactTime": "2019-03-05T12:47:02.762Z",
        #         "timestamp": "2019-03-05T12:47:02.762Z"
        #     }
        #
        timestamp = self.parse8601(self.safe_string(trade, 'timestamp'))
        price = self.safe_float(trade, 'price')
        amount = self.safe_float_2(trade, 'size', 'lastQty')
        id = self.safe_string(trade, 'trdMatchID')
        order = self.safe_string(trade, 'orderID')
        side = self.safe_string(trade, 'side').lower()
        # price * amount doesn't work for all symbols(e.g. XBT, ETH)
        cost = self.safe_float(trade, 'execCost')
        if cost is not None:
            cost = abs(cost) / 100000000
        fee = None
        if 'execComm' in trade:
            feeCost = self.safe_float(trade, 'execComm')
            feeCost = feeCost / 100000000
            currencyId = self.safe_string(trade, 'currency')
            currencyId = currencyId.upper()
            feeCurrency = self.common_currency_code(currencyId)
            feeRate = self.safe_float(trade, 'commission')
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
                'rate': feeRate,
            }
        takerOrMaker = None
        if fee is not None:
            takerOrMaker = fee['cost'] < 'maker' if 0 else 'taker'
        symbol = None
        marketId = self.safe_string(trade, 'symbol')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                symbol = marketId
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': order,
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'fee': fee,
        }

    def parse_order_status(self, status):
        statuses = {
            'New': 'open',
            'PartiallyFilled': 'open',
            'Filled': 'closed',
            'DoneForDay': 'open',
            'Canceled': 'canceled',
            'PendingCancel': 'open',
            'PendingNew': 'open',
            'Rejected': 'rejected',
            'Expired': 'expired',
            'Stopped': 'open',
            'Untriggered': 'open',
            'Triggered': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'ordStatus'))
        symbol = None
        if market is not None:
            symbol = market['symbol']
        else:
            id = order['symbol']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'timestamp'))
        lastTradeTimestamp = self.parse8601(self.safe_string(order, 'transactTime'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'orderQty')
        filled = self.safe_float(order, 'cumQty', 0.0)
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = max(amount - filled, 0.0)
        average = self.safe_float(order, 'avgPx')
        cost = None
        if filled is not None:
            if average is not None:
                cost = average * filled
            elif price is not None:
                cost = price * filled
        result = {
            'info': order,
            'id': str(order['orderID']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': order['ordType'].lower(),
            'side': order['side'].lower(),
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = self.iso8601(since)
        if limit is not None:
            request['count'] = limit
        response = self.publicGetTrade(self.extend(request, params))
        #
        #     [
        #         {
        #             timestamp: '2018-08-28T00:00:02.735Z',
        #             symbol: 'XBTUSD',
        #             side: 'Buy',
        #             size: 2000,
        #             price: 6906.5,
        #             tickDirection: 'PlusTick',
        #             trdMatchID: 'b9a42432-0a46-6a2f-5ecc-c32e9ca4baf8',
        #             grossValue: 28958000,
        #             homeNotional: 0.28958,
        #             foreignNotional: 2000
        #         },
        #         {
        #             timestamp: '2018-08-28T00:00:03.778Z',
        #             symbol: 'XBTUSD',
        #             side: 'Sell',
        #             size: 1000,
        #             price: 6906,
        #             tickDirection: 'MinusTick',
        #             trdMatchID: '0d4f1682-5270-a800-569b-4a0eb92db97c',
        #             grossValue: 14480000,
        #             homeNotional: 0.1448,
        #             foreignNotional: 1000
        #         },
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
            'side': self.capitalize(side),
            'orderQty': amount,
            'ordType': self.capitalize(type),
        }
        if price is not None:
            request['price'] = price
        response = self.privatePostOrder(self.extend(request, params))
        order = self.parse_order(response)
        id = order['id']
        self.orders[id] = order
        return self.extend({'info': response}, order)

    def edit_order(self, id, symbol, type, side, amount=None, price=None, params={}):
        self.load_markets()
        request = {
            'orderID': id,
        }
        if amount is not None:
            request['orderQty'] = amount
        if price is not None:
            request['price'] = price
        response = self.privatePutOrder(self.extend(request, params))
        order = self.parse_order(response)
        self.orders[order['id']] = order
        return self.extend({'info': response}, order)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateDeleteOrder(self.extend({'orderID': id}, params))
        order = response[0]
        error = self.safe_string(order, 'error')
        if error is not None:
            if error.find('Unable to cancel order due to existing state') >= 0:
                raise OrderNotFound(self.id + ' cancelOrder() failed: ' + error)
        order = self.parse_order(order)
        self.orders[order['id']] = order
        return self.extend({'info': response}, order)

    def is_fiat(self, currency):
        if currency == 'EUR':
            return True
        if currency == 'PLN':
            return True
        return False

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        # currency = self.currency(code)
        if code != 'BTC':
            raise ExchangeError(self.id + ' supoprts BTC withdrawals only, other currencies coming soon...')
        request = {
            'currency': 'XBt',  # temporarily
            'amount': amount,
            'address': address,
            # 'otpToken': '123456',  # requires if two-factor auth(OTP) is enabled
            # 'fee': 0.001,  # bitcoin network fee
        }
        response = self.privatePostUserRequestWithdrawal(self.extend(request, params))
        return {
            'info': response,
            'id': response['transactID'],
        }

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if code == 429:
            raise DDoSProtection(self.id + ' ' + body)
        if code >= 400:
            if body:
                if body[0] == '{':
                    error = self.safe_value(response, 'error', {})
                    message = self.safe_string(error, 'message')
                    feedback = self.id + ' ' + body
                    exact = self.exceptions['exact']
                    if message in exact:
                        raise exact[message](feedback)
                    broad = self.exceptions['broad']
                    broadKey = self.findBroadlyMatchedKey(broad, message)
                    if broadKey is not None:
                        raise broad[broadKey](feedback)
                    if code == 400:
                        raise BadRequest(feedback)
                    raise ExchangeError(feedback)  # unknown message

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = '/api/' + self.version + '/' + path
        if method == 'GET':
            if params:
                query += '?' + self.urlencode(params)
        else:
            format = self.safe_string(params, '_format')
            if format is not None:
                query += '?' + self.urlencode({'_format': format})
                params = self.omit(params, '_format')
        url = self.urls['api'] + query
        if api == 'private':
            self.check_required_credentials()
            auth = method + query
            expires = self.safe_integer(self.options, 'api-expires')
            headers = {
                'Content-Type': 'application/json',
                'api-key': self.apiKey,
            }
            expires = self.sum(self.seconds(), expires)
            expires = str(expires)
            auth += expires
            headers['api-expires'] = expires
            if method == 'POST' or method == 'PUT' or method == 'DELETE':
                if params:
                    body = self.json(params)
                    auth += body
            headers['api-signature'] = self.hmac(self.encode(auth), self.encode(self.secret))
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
