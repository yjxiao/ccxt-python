# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.precise import Precise


class whitebit(Exchange):

    def describe(self):
        return self.deep_extend(super(whitebit, self).describe(), {
            'id': 'whitebit',
            'name': 'WhiteBit',
            'version': 'v2',
            'countries': ['EE'],
            'rateLimit': 500,
            'has': {
                'cancelOrder': None,
                'CORS': None,
                'createDepositAddress': None,
                'createLimitOrder': None,
                'createMarketOrder': None,
                'createOrder': None,
                'deposit': None,
                'editOrder': None,
                'fetchBalance': None,
                'fetchBidsAsks': None,
                'fetchCurrencies': True,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOrderBook': True,
                'fetchStatus': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTradingFees': True,
                'privateAPI': None,
                'publicAPI': True,
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/66732963-8eb7dd00-ee66-11e9-849b-10d9282bb9e0.jpg',
                'api': {
                    'web': 'https://whitebit.com/',
                    'publicV2': 'https://whitebit.com/api/v2/public',
                    'publicV1': 'https://whitebit.com/api/v1/public',
                },
                'www': 'https://www.whitebit.com',
                'doc': 'https://documenter.getpostman.com/view/7473075/Szzj8dgv?version=latest',
                'fees': 'https://whitebit.com/fee-schedule',
                'referral': 'https://whitebit.com/referral/d9bdf40e-28f2-4b52-b2f9-cd1415d82963',
            },
            'api': {
                'web': {
                    'get': [
                        'v1/healthcheck',
                    ],
                },
                'publicV1': {
                    'get': [
                        'markets',
                        'tickers',
                        'ticker',
                        'symbols',
                        'depth/result',
                        'history',
                        'kline',
                    ],
                },
                'publicV2': {
                    'get': [
                        'markets',
                        'ticker',
                        'assets',
                        'fee',
                        'depth/{market}',
                        'trades/{market}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': self.parse_number('0.001'),
                    'maker': self.parse_number('0.001'),
                },
            },
            'options': {
                'fetchTradesMethod': 'fetchTradesV1',
            },
            'exceptions': {
                'exact': {
                    '503': ExchangeNotAvailable,  # {"response":null,"status":503,"errors":{"message":[""]},"notification":null,"warning":null,"_token":null}
                },
                'broad': {
                    'Market is not available': BadSymbol,  # {"success":false,"message":{"market":["Market is not available"]},"result":[]}
                },
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicV2GetMarkets(params)
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result":[
        #             {
        #                 "name":"BTC_USD",
        #                 "moneyPrec":"2",
        #                 "stock":"BTC",
        #                 "money":"USD",
        #                 "stockPrec":"6",
        #                 "feePrec":"4",
        #                 "minAmount":"0.001",
        #                 "tradesEnabled":true,
        #                 "minTotal":"0.001"
        #             }
        #         ]
        #     }
        #
        markets = self.safe_value(response, 'result')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'name')
            baseId = self.safe_string(market, 'stock')
            quoteId = self.safe_string(market, 'money')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            active = self.safe_value(market, 'tradesEnabled')
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'type': 'spot',
                'spot': True,
                'active': active,
                'precision': {
                    'amount': self.safe_integer(market, 'stockPrec'),
                    'price': self.safe_integer(market, 'moneyPrec'),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_number(market, 'minAmount'),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': self.safe_number(market, 'minTotal'),
                        'max': None,
                    },
                },
            }
            result.append(entry)
        return result

    def fetch_currencies(self, params={}):
        response = self.publicV2GetAssets(params)
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result":{
        #             "BTC":{
        #                 "id":"4f37bc79-f612-4a63-9a81-d37f7f9ff622",
        #                 "lastUpdateTimestamp":"2019-10-12T04:40:05.000Z",
        #                 "name":"Bitcoin",
        #                 "canWithdraw":true,
        #                 "canDeposit":true,
        #                 "minWithdrawal":"0.001",
        #                 "maxWithdrawal":"0",
        #                 "makerFee":"0.1",
        #                 "takerFee":"0.1"
        #             }
        #         }
        #     }
        #
        currencies = self.safe_value(response, 'result')
        ids = list(currencies.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            currency = currencies[id]
            # breaks down in Python due to utf8 encoding issues on the exchange side
            # name = self.safe_string(currency, 'name')
            canDeposit = self.safe_value(currency, 'canDeposit', True)
            canWithdraw = self.safe_value(currency, 'canWithdraw', True)
            active = canDeposit and canWithdraw
            code = self.safe_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,  # the original payload
                'name': None,  # see the comment above
                'active': active,
                'fee': None,
                'precision': None,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_number(currency, 'minWithdrawal'),
                        'max': self.safe_number(currency, 'maxWithdrawal'),
                    },
                },
            }
        return result

    def fetch_trading_fees(self, params={}):
        response = self.publicV2GetFee(params)
        fees = self.safe_value(response, 'result')
        return {
            'maker': self.safe_number(fees, 'makerFee'),
            'taker': self.safe_number(fees, 'takerFee'),
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicV1GetTicker(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result": {
        #             "bid":"0.021979",
        #             "ask":"0.021996",
        #             "open":"0.02182",
        #             "high":"0.022039",
        #             "low":"0.02161",
        #             "last":"0.021987",
        #             "volume":"2810.267",
        #             "deal":"61.383565474",
        #             "change":"0.76",
        #         },
        #     }
        #
        ticker = self.safe_value(response, 'result', {})
        return self.parse_ticker(ticker, market)

    def parse_ticker(self, ticker, market=None):
        #
        # fetchTicker
        #
        #     {
        #         "bid":"0.021979",
        #         "ask":"0.021996",
        #         "open":"0.02182",
        #         "high":"0.022039",
        #         "low":"0.02161",
        #         "last":"0.021987",
        #         "volume":"2810.267",
        #         "deal":"61.383565474",
        #         "change":"0.76",
        #     }
        #
        # fetchTickers v1
        #
        #     {
        #         "at":1571022144,
        #         "ticker": {
        #             "bid":"0.022024",
        #             "ask":"0.022042",
        #             "low":"0.02161",
        #             "high":"0.022062",
        #             "last":"0.022036",
        #             "vol":"2813.503",
        #             "deal":"61.457279261",
        #             "change":"0.95"
        #         }
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'at', self.milliseconds())
        ticker = self.safe_value(ticker, 'ticker', ticker)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_number(ticker, 'last')
        percentage = self.safe_number(ticker, 'change')
        change = None
        if percentage is not None:
            change = self.number_to_string(percentage * 0.01)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_number(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'volume'),
            'quoteVolume': self.safe_number(ticker, 'deal'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicV1GetTickers(params)
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result": {
        #             "ETH_BTC": {
        #                 "at":1571022144,
        #                 "ticker": {
        #                     "bid":"0.022024",
        #                     "ask":"0.022042",
        #                     "low":"0.02161",
        #                     "high":"0.022062",
        #                     "last":"0.022036",
        #                     "vol":"2813.503",
        #                     "deal":"61.457279261",
        #                     "change":"0.95"
        #                 }
        #             },
        #         },
        #     }
        #
        data = self.safe_value(response, 'result')
        marketIds = list(data.keys())
        result = {}
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.safe_market(marketId)
            ticker = self.parse_ticker(data[marketId], market)
            symbol = ticker['symbol']
            result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 50, maximum = 100
        response = self.publicV2GetDepthMarket(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result":{
        #             "lastUpdateTimestamp":"2019-10-14T03:15:47.000Z",
        #             "asks":[
        #                 ["0.02204","2.03"],
        #                 ["0.022041","2.492"],
        #                 ["0.022042","2.254"],
        #             ],
        #             "bids":[
        #                 ["0.022018","2.327"],
        #                 ["0.022017","1.336"],
        #                 ["0.022015","2.089"],
        #             ],
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        timestamp = self.parse8601(self.safe_string(result, 'lastUpdateTimestamp'))
        return self.parse_order_book(result, symbol, timestamp)

    def fetch_trades_v1(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'lastId': 1,  # todo add since
        }
        if limit is not None:
            request['limit'] = limit  # default = 50, maximum = 10000
        response = self.publicV1GetHistory(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result":[
        #             {
        #                 "id":11887426,
        #                 "type":"buy",
        #                 "time":1571023057.413769,
        #                 "amount":"0.171",
        #                 "price":"0.022052"
        #             }
        #         ],
        #     }
        #
        result = self.safe_value(response, 'result', [])
        return self.parse_trades(result, market, since, limit)

    def fetch_trades_v2(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 50, maximum = 10000
        response = self.publicV2GetTradesMarket(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result": [
        #             {
        #                 "tradeId":11903347,
        #                 "price":"0.022044",
        #                 "volume":"0.029",
        #                 "time":"2019-10-14T06:30:57.000Z",
        #                 "isBuyerMaker":false
        #             },
        #         ],
        #     }
        #
        result = self.safe_value(response, 'result', [])
        return self.parse_trades(result, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        method = self.safe_string(self.options, 'fetchTradesMethod', 'fetchTradesV2')
        return getattr(self, method)(symbol, since, limit, params)

    def parse_trade(self, trade, market=None):
        #
        # fetchTradesV1
        #
        #     {
        #         "id":11887426,
        #         "type":"buy",
        #         "time":1571023057.413769,
        #         "amount":"0.171",
        #         "price":"0.022052"
        #     }
        #
        # fetchTradesV2
        #
        #     {
        #         "tradeId":11903347,
        #         "price":"0.022044",
        #         "volume":"0.029",
        #         "time":"2019-10-14T06:30:57.000Z",
        #         "isBuyerMaker":false
        #     }
        #
        timestamp = self.safe_value(trade, 'time')
        if isinstance(timestamp, basestring):
            timestamp = self.parse8601(timestamp)
        else:
            timestamp = int(timestamp * 1000)
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string_2(trade, 'amount', 'volume')
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        id = self.safe_string_2(trade, 'id', 'tradeId')
        side = self.safe_string(trade, 'type')
        if side is None:
            isBuyerMaker = self.safe_value(trade, 'isBuyerMaker')
            side = 'buy' if isBuyerMaker else 'sell'
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
            'cost': cost,
            'fee': None,
        }

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'interval': self.timeframes[timeframe],
        }
        if since is not None:
            maxLimit = 1440
            if limit is None:
                limit = maxLimit
            limit = min(limit, maxLimit)
            start = int(since / 1000)
            duration = self.parse_timeframe(timeframe)
            end = self.sum(start, duration * limit)
            request['start'] = start
            request['end'] = end
        if limit is not None:
            request['limit'] = limit  # max 1440
        response = self.publicV1GetKline(self.extend(request, params))
        #
        #     {
        #         "success":true,
        #         "message":"",
        #         "result":[
        #             [1591488000,"0.025025","0.025025","0.025029","0.025023","6.181","0.154686629"],
        #             [1591488060,"0.025028","0.025033","0.025035","0.025026","8.067","0.201921167"],
        #             [1591488120,"0.025034","0.02505","0.02505","0.025034","20.089","0.503114696"],
        #         ]
        #     }
        #
        result = self.safe_value(response, 'result', [])
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         1591488000,
        #         "0.025025",
        #         "0.025025",
        #         "0.025029",
        #         "0.025023",
        #         "6.181",
        #         "0.154686629"
        #     ]
        #
        return [
            self.safe_timestamp(ohlcv, 0),  # timestamp
            self.safe_number(ohlcv, 1),  # open
            self.safe_number(ohlcv, 3),  # high
            self.safe_number(ohlcv, 4),  # low
            self.safe_number(ohlcv, 2),  # close
            self.safe_number(ohlcv, 5),  # volume
        ]

    def fetch_status(self, params={}):
        response = self.webGetV1Healthcheck(params)
        status = self.safe_integer(response, 'status')
        formattedStatus = 'ok'
        if status == 503:
            formattedStatus = 'maintenance'
        self.status = self.extend(self.status, {
            'status': formattedStatus,
            'updated': self.milliseconds(),
        })
        return self.status

    def sign(self, path, api='publicV1', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        if query:
            url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if (code == 418) or (code == 429):
            raise DDoSProtection(self.id + ' ' + str(code) + ' ' + reason + ' ' + body)
        if code == 404:
            raise ExchangeError(self.id + ' ' + str(code) + ' endpoint not found')
        if response is not None:
            success = self.safe_value(response, 'success')
            if not success:
                feedback = self.id + ' ' + body
                status = self.safe_string(response, 'status')
                if isinstance(status, basestring):
                    self.throw_exactly_matched_exception(self.exceptions['exact'], status, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
                raise ExchangeError(feedback)
