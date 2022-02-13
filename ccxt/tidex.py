# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.precise import Precise


class tidex(Exchange):

    def describe(self):
        return self.deep_extend(super(tidex, self).describe(), {
            'id': 'tidex',
            'name': 'Tidex',
            'countries': ['UK'],
            'rateLimit': 2000,
            'version': '3',
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createMarketOrder': None,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchCurrencies': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedPositions': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30781780-03149dc4-a12e-11e7-82bb-313b269d24d4.jpg',
                'api': {
                    'web': 'https://gate.tidex.com/api',
                    'public': 'https://api.tidex.com/api/3',
                    'private': 'https://api.tidex.com/tapi',
                },
                'www': 'https://tidex.com',
                'doc': 'https://tidex.com/exchange/public-api',
                'referral': 'https://tidex.com/exchange/?ref=57f5638d9cd7',
                'fees': [
                    'https://tidex.com/exchange/assets-spec',
                    'https://tidex.com/exchange/pairs-spec',
                ],
            },
            'api': {
                'web': {
                    'get': [
                        'currency',
                        'pairs',
                        'tickers',
                        'orders',
                        'ordershistory',
                        'trade-data',
                        'trade-data/{id}',
                    ],
                },
                'public': {
                    'get': [
                        'info',
                        'ticker/{pair}',
                        'depth/{pair}',
                        'trades/{pair}',
                    ],
                },
                'private': {
                    'post': [
                        'getInfoExt',
                        'getInfo',
                        'Trade',
                        'ActiveOrders',
                        'OrderInfo',
                        'CancelOrder',
                        'TradeHistory',
                        'getDepositAddress',
                        'createWithdraw',
                        'getWithdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'feeSide': 'get',
                    'tierBased': False,
                    'percentage': True,
                    'taker': self.parse_number('0.001'),
                    'maker': self.parse_number('0.001'),
                },
            },
            'commonCurrencies': {
                'DSH': 'DASH',
                'EMGO': 'MGO',
                'MGO': 'WMGO',
            },
            'exceptions': {
                'exact': {
                    '803': InvalidOrder,  # "Count could not be less than 0.001."(selling below minAmount)
                    '804': InvalidOrder,  # "Count could not be more than 10000."(buying above maxAmount)
                    '805': InvalidOrder,  # "price could not be less than X."(minPrice violation on buy & sell)
                    '806': InvalidOrder,  # "price could not be more than X."(maxPrice violation on buy & sell)
                    '807': InvalidOrder,  # "cost could not be less than X."(minCost violation on buy & sell)
                    '831': InsufficientFunds,  # "Not enougth X to create buy order."(buying with balance.quote < order.cost)
                    '832': InsufficientFunds,  # "Not enougth X to create sell order."(selling with balance.base < order.amount)
                    '833': OrderNotFound,  # "Order with id X was not found."(cancelling non-existent, closed and cancelled order)
                },
                'broad': {
                    'Invalid pair name': ExchangeError,  # {"success":0,"error":"Invalid pair name: btc_eth"}
                    'invalid api key': AuthenticationError,
                    'invalid sign': AuthenticationError,
                    'api key dont have trade permission': AuthenticationError,
                    'invalid parameter': InvalidOrder,
                    'invalid order': InvalidOrder,
                    'Requests too often': DDoSProtection,
                    'not available': ExchangeNotAvailable,
                    'data unavailable': ExchangeNotAvailable,
                    'external service unavailable': ExchangeNotAvailable,
                    'IP restricted': PermissionDenied,  # {"success":0,"code":0,"error":"IP restricted(223.xxx.xxx.xxx)"}
                },
            },
            'options': {
                'fetchTickersMaxLength': 2048,
            },
            'orders': {},  # orders cache / emulation
        })

    def fetch_currencies(self, params={}):
        response = self.webGetCurrency(params)
        #
        #     [
        #         {
        #             "id":2,
        #             "symbol":"BTC",
        #             "type":2,
        #             "name":"Bitcoin",
        #             "amountPoint":8,
        #             "depositEnable":true,
        #             "depositMinAmount":0.0005,
        #             "withdrawEnable":true,
        #             "withdrawFee":0.0004,
        #             "withdrawMinAmount":0.0005,
        #             "settings":{
        #                 "Blockchain":"https://blockchair.com/bitcoin/",
        #                 "TxUrl":"https://blockchair.com/bitcoin/transaction/{0}",
        #                 "AddrUrl":"https://blockchair.com/bitcoin/address/{0}",
        #                 "ConfirmationCount":3,
        #                 "NeedMemo":false
        #             },
        #             "visible":true,
        #             "isDelisted":false
        #         }
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'symbol')
            precision = self.safe_integer(currency, 'amountPoint')
            code = self.safe_currency_code(id)
            visible = self.safe_value(currency, 'visible')
            active = visible is True
            withdrawEnable = self.safe_value(currency, 'withdrawEnable', True)
            depositEnable = self.safe_value(currency, 'depositEnable', True)
            if not withdrawEnable or not depositEnable:
                active = False
            name = self.safe_string(currency, 'name')
            fee = self.safe_number(currency, 'withdrawFee')
            result[code] = {
                'id': id,
                'code': code,
                'name': name,
                'active': active,
                'deposit': depositEnable,
                'withdraw': withdrawEnable,
                'precision': precision,
                'funding': {
                    'withdraw': {
                        'active': withdrawEnable,
                        'fee': fee,
                    },
                    'deposit': {
                        'active': depositEnable,
                        'fee': self.parse_number('0'),
                    },
                },
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_number(currency, 'withdrawMinAmount'),
                        'max': None,
                    },
                    'deposit': {
                        'min': self.safe_number(currency, 'depositMinAmount'),
                        'max': None,
                    },
                },
                'info': currency,
            }
        return result

    def fetch_markets(self, params={}):
        response = self.publicGetInfo(params)
        #
        #     {
        #         "server_time":1615861869,
        #         "pairs":{
        #             "ltc_btc":{
        #                 "decimal_places":8,
        #                 "min_price":0.00000001,
        #                 "max_price":3.0,
        #                 "min_amount":0.001,
        #                 "max_amount":1000000.0,
        #                 "min_total":0.0001,
        #                 "hidden":0,
        #                 "fee":0.1,
        #             },
        #         },
        #     }
        #
        markets = response['pairs']
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            hidden = self.safe_integer(market, 'hidden')
            takerFeeString = self.safe_string(market, 'fee')
            takerFeeString = Precise.string_div(takerFeeString, '100')
            result.append({
                'id': id,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': (hidden == 0),
                'contract': False,
                'linear': None,
                'inverse': None,
                'taker': self.parse_number(takerFeeString),
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.safe_integer(market, 'decimal_places'),
                    'price': self.safe_integer(market, 'decimal_places'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(market, 'min_amount'),
                        'max': self.safe_number(market, 'max_amount'),
                    },
                    'price': {
                        'min': self.safe_number(market, 'min_price'),
                        'max': self.safe_number(market, 'max_price'),
                    },
                    'cost': {
                        'min': self.safe_number(market, 'min_total'),
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_balance(self, response):
        balances = self.safe_value(response, 'return')
        timestamp = self.safe_timestamp(balances, 'server_time')
        result = {
            'info': response,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        funds = self.safe_value(balances, 'funds', {})
        currencyIds = list(funds.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            balance = self.safe_value(funds, currencyId, {})
            account = self.account()
            account['free'] = self.safe_string(balance, 'value')
            account['used'] = self.safe_string(balance, 'inOrders')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfoExt(params)
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "funds":{
        #                 "btc":{"value":0.0000499885629956,"inOrders":0.0},
        #                 "eth":{"value":0.000000030741708,"inOrders":0.0},
        #                 "tdx":{"value":0.0000000155385356,"inOrders":0.0}
        #             },
        #             "rights":{
        #                 "info":true,
        #                 "trade":true,
        #                 "withdraw":false
        #             },
        #             "transaction_count":0,
        #             "open_orders":0,
        #             "server_time":1619436907
        #         },
        #         "stat":{
        #             "isSuccess":true,
        #             "serverTime":"00:00:00.0001157",
        #             "time":"00:00:00.0101364",
        #             "errors":null
        #         }
        #     }
        #
        return self.parse_balance(response)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 150, max = 2000
        response = self.publicGetDepthPair(self.extend(request, params))
        market_id_in_reponse = (market['id'] in response)
        if not market_id_in_reponse:
            raise ExchangeError(self.id + ' ' + market['symbol'] + ' order book is empty or not available')
        orderbook = response[market['id']]
        return self.parse_order_book(orderbook, symbol)

    def fetch_order_books(self, symbols=None, limit=None, params={}):
        self.load_markets()
        ids = None
        if symbols is None:
            ids = '-'.join(self.ids)
            # max URL length is 2083 symbols, including http schema, hostname, tld, etc...
            if len(ids) > 2048:
                numIds = len(self.ids)
                raise ExchangeError(self.id + ' has ' + str(numIds) + ' symbols exceeding max URL length, you are required to specify a list of symbols in the first argument to fetchOrderBooks')
        else:
            ids = self.market_ids(symbols)
            ids = '-'.join(ids)
        request = {
            'pair': ids,
        }
        if limit is not None:
            request['limit'] = limit  # default = 150, max = 2000
        response = self.publicGetDepthPair(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = self.safe_symbol(id)
            result[symbol] = self.parse_order_book(response[id])
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         high: 0.03497582,
        #         low: 0.03248474,
        #         avg: 0.03373028,
        #         vol: 120.11485715062999,
        #         vol_cur: 3572.24914074,
        #         last: 0.0337611,
        #         buy: 0.0337442,
        #         sell: 0.03377798,
        #         updated: 1537522009
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'updated')
        market = self.safe_market(None, market)
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': market['symbol'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_string(ticker, 'avg'),
            'baseVolume': self.safe_string(ticker, 'vol_cur'),
            'quoteVolume': self.safe_string(ticker, 'vol'),
            'info': ticker,
        }, market, False)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        ids = self.ids
        if symbols is None:
            numIds = len(ids)
            ids = '-'.join(ids)
            # max URL length is 2048 symbols, including http schema, hostname, tld, etc...
            if len(ids) > self.options['fetchTickersMaxLength']:
                maxLength = self.safe_integer(self.options, 'fetchTickersMaxLength', 2048)
                raise ArgumentsRequired(self.id + ' has ' + str(numIds) + ' markets exceeding max URL length for self endpoint(' + str(maxLength) + ' characters), please, specify a list of symbols of interest in the first argument to fetchTickers')
        else:
            ids = self.market_ids(symbols)
            ids = '-'.join(ids)
        request = {
            'pair': ids,
        }
        response = self.publicGetTickerPair(self.extend(request, params))
        result = {}
        keys = list(response.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            market = self.safe_market(id)
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(response[id], market)
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        tickers = self.fetch_tickers([symbol], params)
        return tickers[symbol]

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'timestamp')
        side = self.safe_string(trade, 'type')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        priceString = self.safe_string_2(trade, 'rate', 'price')
        id = self.safe_string_2(trade, 'trade_id', 'tid')
        orderId = self.safe_string(trade, 'order_id')
        marketId = self.safe_string(trade, 'pair')
        symbol = self.safe_symbol(marketId, market)
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        type = 'limit'  # all trades are still limit trades
        takerOrMaker = None
        fee = None
        feeCost = self.safe_number(trade, 'commission')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'commissionCurrency')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        isYourOrder = self.safe_value(trade, 'is_your_order')
        if isYourOrder is not None:
            takerOrMaker = 'taker'
            if isYourOrder:
                takerOrMaker = 'maker'
            if fee is None:
                fee = self.calculate_fee(symbol, type, side, amount, price, takerOrMaker)
        return {
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTradesPair(self.extend(request, params))
        if isinstance(response, list):
            numElements = len(response)
            if numElements == 0:
                return []
        return self.parse_trades(response[market['id']], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        amountString = str(amount)
        priceString = str(price)
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': side,
            'amount': self.amount_to_precision(symbol, amount),
            'rate': self.price_to_precision(symbol, price),
        }
        response = self.privatePostTrade(self.extend(request, params))
        id = None
        status = 'open'
        filledString = '0.0'
        remainingString = amountString
        returnResult = self.safe_value(response, 'return')
        if returnResult is not None:
            id = self.safe_string(returnResult, 'order_id')
            if id == '0':
                id = self.safe_string(returnResult, 'init_order_id')
                status = 'closed'
            filledString = self.safe_string(returnResult, 'received', filledString)
            remainingString = self.safe_string(returnResult, 'remains', amountString)
        timestamp = self.milliseconds()
        return self.safe_order({
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': priceString,
            'cost': None,
            'amount': amountString,
            'remaining': remainingString,
            'filled': filledString,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
            'info': response,
            'clientOrderId': None,
            'average': None,
            'trades': None,
        }, market)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': int(id),
        }
        return self.privatePostCancelOrder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'closed',
            '2': 'canceled',
            '3': 'canceled',  # or partially-filled and still open? https://github.com/ccxt/ccxt/issues/1594
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_timestamp(order, 'timestamp_created')
        marketId = self.safe_string(order, 'pair')
        symbol = self.safe_symbol(marketId, market)
        remaining = None
        amount = None
        price = self.safe_string(order, 'rate')
        if 'start_amount' in order:
            amount = self.safe_string(order, 'start_amount')
            remaining = self.safe_string(order, 'amount')
        else:
            remaining = self.safe_string(order, 'amount')
        fee = None
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'type': 'limit',
            'timeInForce': None,
            'postOnly': None,
            'side': self.safe_string(order, 'type'),
            'price': price,
            'stopPrice': None,
            'cost': None,
            'amount': amount,
            'remaining': remaining,
            'filled': None,
            'status': status,
            'fee': fee,
            'average': None,
            'trades': None,
        }, market)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': int(id),
        }
        response = self.privatePostOrderInfo(self.extend(request, params))
        id = str(id)
        result = self.safe_value(response, 'return', {})
        order = self.safe_value(result, id)
        return self.parse_order(self.extend({'id': id}, order))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = self.privatePostActiveOrders(self.extend(request, params))
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "1255468911":{
        #                 "status":0,
        #                 "pair":"spike_usdt",
        #                 "type":"sell",
        #                 "amount":35028.44256388,
        #                 "rate":0.00199989,
        #                 "timestamp_created":1602684432
        #             }
        #         },
        #         "stat":{
        #             "isSuccess":true,
        #             "serverTime":"00:00:00.0000826",
        #             "time":"00:00:00.0091423",
        #             "errors":null
        #         }
        #     }
        #
        # it can only return 'open' orders(i.e. no way to fetch 'closed' orders)
        orders = self.safe_value(response, 'return', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        # some derived classes use camelcase notation for request fields
        request = {
            # 'from': 123456789,  # trade ID, from which the display starts numerical 0(test result: liqui ignores self field)
            # 'count': 1000,  # the number of trades for display numerical, default = 1000
            # 'from_id': trade ID, from which the display starts numerical 0
            # 'end_id': trade ID on which the display ends numerical ∞
            # 'order': 'ASC',  # sorting, default = DESC(test result: liqui ignores self field, most recent trade always goes last)
            # 'since': 1234567890,  # UTC start time, default = 0(test result: liqui ignores self field)
            # 'end': 1234567890,  # UTC end time, default = ∞(test result: liqui ignores self field)
            # 'pair': 'eth_btc',  # default = all markets
        }
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        if limit is not None:
            request['count'] = int(limit)
        if since is not None:
            request['since'] = int(since / 1000)
        response = self.privatePostTradeHistory(self.extend(request, params))
        trades = self.safe_value(response, 'return', [])
        return self.parse_trades(trades, market, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
            'amount': float(amount),
            'address': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostCreateWithdraw(self.extend(request, params))
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "withdraw_id":1111,
        #             "withdraw_info":{
        #                 "id":1111,
        #                 "asset_id":1,
        #                 "asset":"BTC",
        #                 "amount":0.0093,
        #                 "fee":0.0007,
        #                 "create_time":1575128018,
        #                 "status":"Created",
        #                 "data":{
        #                     "address":"1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY",
        #                     "memo":"memo",
        #                     "tx":null,
        #                     "error":null
        #                 },
        #             "in_blockchain":false
        #             }
        #         }
        #     }
        #
        result = self.safe_value(response, 'return', {})
        return {
            'info': response,
            'id': self.safe_string(result, 'withdraw_id'),
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'nonce': nonce,
                'method': path,
            }, query))
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': signature,
            }
        elif api == 'public':
            url += '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            url += '/' + self.implode_params(path, params)
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                if query:
                    body = self.json(query)
                    headers = {
                        'Content-Type': 'application/json',
                    }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if 'success' in response:
            #
            # 1 - The exchange only returns the integer 'success' key from their private API
            #
            #     {"success": 1, ...} httpCode == 200
            #     {"success": 0, ...} httpCode == 200
            #
            # 2 - However, derived exchanges can return non-integers
            #
            #     It can be a numeric string
            #     {"sucesss": "1", ...}
            #     {"sucesss": "0", ...}, httpCode >= 200(can be 403, 502, etc)
            #
            #     Or just a string
            #     {"success": "true", ...}
            #     {"success": "false", ...}, httpCode >= 200
            #
            #     Or a boolean
            #     {"success": True, ...}
            #     {"success": False, ...}, httpCode >= 200
            #
            # 3 - Oversimplified, Python PEP8 forbids comparison operator(==) of different types
            #
            # 4 - We do not want to copy-paste and duplicate the code of self handler to other exchanges derived from Liqui
            #
            # To cover points 1, 2, 3 and 4 combined self handler should work like self:
            #
            success = self.safe_value(response, 'success', False)
            if isinstance(success, basestring):
                if (success == 'true') or (success == '1'):
                    success = True
                else:
                    success = False
            if not success:
                code = self.safe_string(response, 'code')
                message = self.safe_string(response, 'error')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
                raise ExchangeError(feedback)  # unknown message
