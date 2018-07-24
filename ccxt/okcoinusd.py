# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection


class okcoinusd (Exchange):

    def describe(self):
        return self.deep_extend(super(okcoinusd, self).describe(), {
            'id': 'okcoinusd',
            'name': 'OKCoin USD',
            'countries': ['CN', 'US'],
            'version': 'v1',
            'rateLimit': 1000,  # up to 3000 requests per 5 minutes ≈ 600 requests per minute ≈ 10 requests per second ≈ 100 ms
            'has': {
                'CORS': False,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
                'futures': False,
            },
            'extension': '.do',  # appended to endpoint URL
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': '1day',
                '3d': '3day',
                '1w': '1week',
            },
            'api': {
                'web': {
                    'get': [
                        'spot/markets/currencies',
                        'spot/markets/products',
                        'spot/markets/tickers',
                    ],
                },
                'public': {
                    'get': [
                        'depth',
                        'exchange_rate',
                        'future_depth',
                        'future_estimated_price',
                        'future_hold_amount',
                        'future_index',
                        'future_kline',
                        'future_price_limit',
                        'future_ticker',
                        'future_trades',
                        'kline',
                        'otcs',
                        'ticker',
                        'tickers',
                        'trades',
                    ],
                },
                'private': {
                    'post': [
                        'account_records',
                        'batch_trade',
                        'borrow_money',
                        'borrow_order_info',
                        'borrows_info',
                        'cancel_borrow',
                        'cancel_order',
                        'cancel_otc_order',
                        'cancel_withdraw',
                        'funds_transfer',
                        'future_batch_trade',
                        'future_cancel',
                        'future_devolve',
                        'future_explosive',
                        'future_order_info',
                        'future_orders_info',
                        'future_position',
                        'future_position_4fix',
                        'future_trade',
                        'future_trades_history',
                        'future_userinfo',
                        'future_userinfo_4fix',
                        'lend_depth',
                        'order_fee',
                        'order_history',
                        'order_info',
                        'orders_info',
                        'otc_order_history',
                        'otc_order_info',
                        'repayment',
                        'submit_otc_order',
                        'trade',
                        'trade_history',
                        'trade_otc_order',
                        'wallet_info',
                        'withdraw',
                        'withdraw_info',
                        'unrepayments_info',
                        'userinfo',
                    ],
                },
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766791-89ffb502-5ee5-11e7-8a5b-c5950b68ac65.jpg',
                'api': {
                    'web': 'https://www.okcoin.com/v2',
                    'public': 'https://www.okcoin.com/api',
                    'private': 'https://www.okcoin.com/api',
                },
                'www': 'https://www.okcoin.com',
                'doc': [
                    'https://www.okcoin.com/rest_getStarted.html',
                    'https://www.npmjs.com/package/okcoin.com',
                ],
            },
            'fees': {
                'trading': {
                    'taker': 0.002,
                    'maker': 0.002,
                },
            },
            'exceptions': {
                # see https://github.com/okcoin-okex/API-docs-OKEx.com/blob/master/API-For-Spot-EN/Error%20Code%20For%20Spot.md
                '10000': ExchangeError,  # "Required field, can not be null"
                '10001': DDoSProtection,  # "Request frequency too high to exceed the limit allowed"
                '10005': AuthenticationError,  # "'SecretKey' does not exist"
                '10006': AuthenticationError,  # "'Api_key' does not exist"
                '10007': AuthenticationError,  # "Signature does not match"
                '1002': InsufficientFunds,  # "The transaction amount exceed the balance"
                '1003': InvalidOrder,  # "The transaction amount is less than the minimum requirement"
                '1004': InvalidOrder,  # "The transaction amount is less than 0"
                '1013': InvalidOrder,  # no contract type(PR-1101)
                '1027': InvalidOrder,  # createLimitBuyOrder(symbol, 0, 0): Incorrect parameter may exceeded limits
                '1050': InvalidOrder,  # returned when trying to cancel an order that was filled or canceled previously
                '1217': InvalidOrder,  # "Order was sent at ±5% of the current market price. Please resend"
                '10014': InvalidOrder,  # "Order price must be between 0 and 1,000,000"
                '1009': OrderNotFound,  # for spot markets, cancelling closed order
                '1019': OrderNotFound,  # order closed?("Undo order failed")
                '1051': OrderNotFound,  # for spot markets, cancelling "just closed" order
                '10009': OrderNotFound,  # for spot markets, "Order does not exist"
                '20015': OrderNotFound,  # for future markets
                '10008': ExchangeError,  # Illegal URL parameter
            },
            'options': {
                'marketBuyPrice': False,
                'defaultContractType': 'this_week',  # next_week, quarter
                'warnOnFetchOHLCVLimitArgument': True,
                'fiats': ['USD', 'CNY'],
                'futures': {
                    'BCH': True,
                    'BTC': True,
                    'BTG': True,
                    'EOS': True,
                    'ETC': True,
                    'ETH': True,
                    'LTC': True,
                    'NEO': True,
                    'QTUM': True,
                    'USDT': True,
                    'XUC': True,
                },
            },
        })

    def fetch_markets(self):
        response = self.webGetSpotMarketsProducts()
        markets = response['data']
        result = []
        for i in range(0, len(markets)):
            id = markets[i]['symbol']
            baseId, quoteId = id.split('_')
            baseIdUppercase = baseId.upper()
            quoteIdUppercase = quoteId.upper()
            base = self.common_currency_code(baseIdUppercase)
            quote = self.common_currency_code(quoteIdUppercase)
            symbol = base + '/' + quote
            precision = {
                'amount': markets[i]['maxSizeDigit'],
                'price': markets[i]['maxPriceDigit'],
            }
            lot = math.pow(10, -precision['amount'])
            minAmount = markets[i]['minTradeSize']
            minPrice = math.pow(10, -precision['price'])
            active = (markets[i]['online'] != 0)
            baseNumericId = markets[i]['baseCurrency']
            quoteNumericId = markets[i]['quoteCurrency']
            market = self.extend(self.fees['trading'], {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'baseNumericId': baseNumericId,
                'quoteNumericId': quoteNumericId,
                'info': markets[i],
                'type': 'spot',
                'spot': True,
                'future': False,
                'lot': lot,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': minAmount,
                        'max': None,
                    },
                    'price': {
                        'min': minPrice,
                        'max': None,
                    },
                    'cost': {
                        'min': minAmount * minPrice,
                        'max': None,
                    },
                },
            })
            result.append(market)
            if (self.has['futures']) and(market['base'] in list(self.options['futures'].keys())):
                fiats = self.options['fiats']
                for j in range(0, len(fiats)):
                    fiat = fiats[j]
                    lowercaseFiat = fiat.lower()
                    result.append(self.extend(market, {
                        'quote': fiat,
                        'symbol': market['base'] + '/' + fiat,
                        'id': market['base'].lower() + '_' + lowercaseFiat,
                        'quoteId': lowercaseFiat,
                        'type': 'future',
                        'spot': False,
                        'future': True,
                    }))
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        if market['future']:
            method += 'Future'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        method += 'Depth'
        orderbook = getattr(self, method)(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        #
        #     {             buy:   "48.777300",
        #                 change:   "-1.244500",
        #       changePercentage:   "-2.47%",
        #                  close:   "49.064000",
        #            createdDate:    1531704852254,
        #             currencyId:    527,
        #                dayHigh:   "51.012500",
        #                 dayLow:   "48.124200",
        #                   high:   "51.012500",
        #                inflows:   "0",
        #                   last:   "49.064000",
        #                    low:   "48.124200",
        #             marketFrom:    627,
        #                   name: {},
        #                   open:   "50.308500",
        #               outflows:   "0",
        #              productId:    527,
        #                   sell:   "49.064000",
        #                 symbol:   "zec_okb",
        #                 volume:   "1049.092535"   }
        #
        timestamp = self.safe_integer_2(ticker, 'timestamp', 'createdDate')
        symbol = None
        if market is None:
            if 'symbol' in ticker:
                marketId = ticker['symbol']
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        open = self.safe_float(ticker, 'open')
        change = self.safe_float(ticker, 'change')
        percentage = self.safe_float(ticker, 'changePercentage')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float_2(ticker, 'vol', 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {
            'symbol': market['id'],
        }
        if market['future']:
            method += 'Future'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        method += 'Ticker'
        response = getattr(self, method)(self.extend(request, params))
        ticker = self.safe_value(response, 'ticker')
        if ticker is None:
            raise ExchangeError(self.id + ' fetchTicker returned an empty response: ' + self.json(response))
        timestamp = self.safe_integer(response, 'date')
        if timestamp is not None:
            timestamp *= 1000
            ticker = self.extend(ticker, {'timestamp': timestamp})
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': trade['date_ms'],
            'datetime': self.iso8601(trade['date_ms']),
            'symbol': symbol,
            'id': str(trade['tid']),
            'order': None,
            'type': None,
            'side': trade['type'],
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {
            'symbol': market['id'],
        }
        if market['future']:
            method += 'Future'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        method += 'Trades'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        numElements = len(ohlcv)
        volumeIndex = 6 if (numElements > 6) else 5
        return [
            ohlcv[0],  # timestamp
            ohlcv[1],  # Open
            ohlcv[2],  # High
            ohlcv[3],  # Low
            ohlcv[4],  # Close
            # ohlcv[5],  # quote volume
            # ohlcv[6],  # base volume
            ohlcv[volumeIndex],  # okex will return base volume in the 7th element for future markets
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {
            'symbol': market['id'],
            'type': self.timeframes[timeframe],
        }
        if market['future']:
            method += 'Future'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        method += 'Kline'
        if limit is not None:
            if self.options['warnOnFetchOHLCVLimitArgument']:
                raise ExchangeError(self.id + ' fetchOHLCV counts "limit" candles from current time backwards, therefore the "limit" argument for ' + self.id + ' is disabled. Set ' + self.id + '.options["warnOnFetchOHLCVLimitArgument"] = False to suppress self warning message.')
            request['size'] = int(limit)  # max is 1440 candles
        if since is not None:
            request['since'] = since
        else:
            request['since'] = self.milliseconds() - 86400000  # last 24 hours
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostUserinfo()
        balances = response['info']['funds']
        result = {'info': response}
        freeIds = list(balances['free'].keys())
        freezedIds = list(balances['freezed'].keys())
        ids = self.array_concat(freeIds, freezedIds)
        for i in range(0, len(ids)):
            id = ids[i]
            code = id.upper()
            if id in self.currencies_by_id:
                code = self.currencies_by_id[id]['code']
            else:
                code = self.common_currency_code(code)
            account = self.account()
            account['free'] = self.safe_float(balances['free'], id, 0.0)
            account['used'] = self.safe_float(balances['freezed'], id, 0.0)
            account['total'] = self.sum(account['free'], account['used'])
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        order = {
            'symbol': market['id'],
            'type': side,
        }
        if market['future']:
            method += 'Future'
            order = self.extend(order, {
                'contract_type': self.options['defaultContractType'],  # self_week, next_week, quarter
                'match_price': 0,  # match best counter party price? 0 or 1, ignores price if 1
                'lever_rate': 10,  # leverage rate value: 10 or 20(10 by default)
                'price': price,
                'amount': amount,
            })
        else:
            if type == 'limit':
                order['price'] = price
                order['amount'] = amount
            else:
                order['type'] += '_market'
                if side == 'buy':
                    if self.options['marketBuyPrice']:
                        if price is None:
                            # eslint-disable-next-line quotes
                            raise ExchangeError(self.id + " market buy orders require a price argument(the amount you want to spend or the cost of the order) when self.options['marketBuyPrice'] is True.")
                        order['price'] = price
                    else:
                        order['price'] = self.safe_float(params, 'cost')
                        if not order['price']:
                            # eslint-disable-next-line quotes
                            raise ExchangeError(self.id + " market buy orders require an additional cost parameter, cost = price * amount. If you want to pass the cost of the market order(the amount you want to spend) in the price argument(the default " + self.id + " behaviour), set self.options['marketBuyPrice'] = True. It will effectively suppress self warning exception as well.")
                else:
                    order['amount'] = amount
        params = self.omit(params, 'cost')
        method += 'Trade'
        response = getattr(self, method)(self.extend(order, params))
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': str(response['order_id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        method = 'privatePost'
        if market['future']:
            method += 'FutureCancel'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        else:
            method += 'CancelOrder'
        response = getattr(self, method)(self.extend(request, params))
        return response

    def parse_order_status(self, status):
        if status == -1:
            return 'canceled'
        if status == 0:
            return 'open'
        if status == 1:
            return 'open'
        if status == 2:
            return 'closed'
        if status == 3:
            return 'open'
        if status == 4:
            return 'canceled'
        return status

    def parse_order_side(self, side):
        if side == 1:
            return 'buy'  # open long position
        if side == 2:
            return 'sell'  # open short position
        if side == 3:
            return 'sell'  # liquidate long position
        if side == 4:
            return 'buy'  # liquidate short position
        return side

    def parse_order(self, order, market=None):
        side = None
        type = None
        if 'type' in order:
            if (order['type'] == 'buy') or (order['type'] == 'sell'):
                side = order['type']
                type = 'limit'
            elif order['type'] == 'buy_market':
                side = 'buy'
                type = 'market'
            elif order['type'] == 'sell_market':
                side = 'sell'
                type = 'market'
            else:
                side = self.parse_order_side(order['type'])
                if ('contract_name' in list(order.keys())) or ('lever_rate' in list(order.keys())):
                    type = 'margin'
        status = self.parse_order_status(order['status'])
        symbol = None
        if market is None:
            if 'symbol' in order:
                if order['symbol'] in self.markets_by_id:
                    market = self.markets_by_id[order['symbol']]
        if market:
            symbol = market['symbol']
        timestamp = None
        createDateField = self.get_create_date_field()
        if createDateField in order:
            timestamp = order[createDateField]
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'deal_amount')
        remaining = amount - filled
        if type == 'market':
            remaining = 0
        average = self.safe_float(order, 'avg_price')
        # https://github.com/ccxt/ccxt/issues/2452
        average = self.safe_float(order, 'price_avg', average)
        cost = average * filled
        result = {
            'info': order,
            'id': str(order['order_id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': order['price'],
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def get_create_date_field(self):
        # needed for derived exchanges
        # allcoin typo create_data instead of create_date
        return 'create_date'

    def get_orders_field(self):
        # needed for derived exchanges
        # allcoin typo order instead of orders(expected based on their API docs)
        return 'orders'

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        request = {
            'order_id': id,
            'symbol': market['id'],
            # 'status': 0,  # 0 for unfilled orders, 1 for filled orders
            # 'current_page': 1,  # current page number
            # 'page_length': 200,  # number of orders returned per page, maximum 200
        }
        if market['future']:
            method += 'Future'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
        method += 'OrderInfo'
        response = getattr(self, method)(self.extend(request, params))
        ordersField = self.get_orders_field()
        numOrders = len(response[ordersField])
        if numOrders > 0:
            return self.parse_order(response[ordersField][0])
        raise OrderNotFound(self.id + ' order ' + id + ' not found')

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        request = {
            'symbol': market['id'],
        }
        order_id_in_params = ('order_id' in list(params.keys()))
        if market['future']:
            method += 'FutureOrdersInfo'
            request['contract_type'] = self.options['defaultContractType']  # self_week, next_week, quarter
            if not order_id_in_params:
                raise ExchangeError(self.id + ' fetchOrders() requires order_id param for futures market ' + symbol + '(a string of one or more order ids, comma-separated)')
        else:
            status = None
            if 'type' in params:
                status = params['type']
            elif 'status' in params:
                status = params['status']
            else:
                name = 'type' if order_id_in_params else 'status'
                raise ExchangeError(self.id + ' fetchOrders() requires ' + name + ' param for spot market ' + symbol + '(0 - for unfilled orders, 1 - for filled/canceled orders)')
            if order_id_in_params:
                method += 'OrdersInfo'
                request = self.extend(request, {
                    'type': status,
                    'order_id': params['order_id'],
                })
            else:
                method += 'OrderHistory'
                request = self.extend(request, {
                    'status': status,
                    'current_page': 1,  # current page number
                    'page_length': 200,  # number of orders returned per page, maximum 200
                })
            params = self.omit(params, ['type', 'status'])
        response = getattr(self, method)(self.extend(request, params))
        ordersField = self.get_orders_field()
        return self.parse_orders(response[ordersField], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        open = 0  # 0 for unfilled orders, 1 for filled orders
        return self.fetch_orders(symbol, since, limit, self.extend({
            'status': open,
        }, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        closed = 1  # 0 for unfilled orders, 1 for filled orders
        orders = self.fetch_orders(symbol, since, limit, self.extend({
            'status': closed,
        }, params))
        return orders

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        # if amount < 0.01:
        #     raise ExchangeError(self.id + ' withdraw() requires amount > 0.01')
        # for some reason they require to supply a pair of currencies for withdrawing one currency
        currencyId = currency['id'] + '_usd'
        request = {
            'symbol': currencyId,
            'withdraw_address': address,
            'withdraw_amount': amount,
            'target': 'address',  # or 'okcn', 'okcom', 'okex'
        }
        query = params
        if 'chargefee' in query:
            request['chargefee'] = query['chargefee']
            query = self.omit(query, 'chargefee')
        else:
            raise ExchangeError(self.id + ' withdraw() requires a `chargefee` parameter')
        if self.password:
            request['trade_pwd'] = self.password
        elif 'password' in query:
            request['trade_pwd'] = query['password']
            query = self.omit(query, 'password')
        elif 'trade_pwd' in query:
            request['trade_pwd'] = query['trade_pwd']
            query = self.omit(query, 'trade_pwd')
        passwordInRequest = ('trade_pwd' in list(request.keys()))
        if not passwordInRequest:
            raise ExchangeError(self.id + ' withdraw() requires self.password set on the exchange instance or a password / trade_pwd parameter')
        response = self.privatePostWithdraw(self.extend(request, query))
        return {
            'info': response,
            'id': self.safe_string(response, 'withdraw_id'),
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/'
        if api != 'web':
            url += self.version + '/'
        url += path
        if api != 'web':
            url += self.extension
        if api == 'private':
            self.check_required_credentials()
            query = self.keysort(self.extend({
                'api_key': self.apiKey,
            }, params))
            # secret key must be at the end of query
            queryString = self.rawencode(query) + '&secret_key=' + self.secret
            query['sign'] = self.hash(self.encode(queryString)).upper()
            body = self.urlencode(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        else:
            if params:
                url += '?' + self.urlencode(params)
        url = self.urls['api'][api] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if len(body) < 2:
            return  # fallback to default error handler
        if body[0] == '{':
            response = json.loads(body)
            if 'error_code' in response:
                error = self.safe_string(response, 'error_code')
                message = self.id + ' ' + self.json(response)
                if error in self.exceptions:
                    ExceptionClass = self.exceptions[error]
                    raise ExceptionClass(message)
                else:
                    raise ExchangeError(message)
            if 'result' in response:
                if not response['result']:
                    raise ExchangeError(self.id + ' ' + self.json(response))
