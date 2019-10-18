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
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce


class yobit (Exchange):

    def describe(self):
        return self.deep_extend(super(yobit, self).describe(), {
            'id': 'yobit',
            'name': 'YoBit',
            'countries': ['RU'],
            'rateLimit': 3000,  # responses are cached every 2 seconds
            'version': '3',
            'has': {
                'CORS': False,
                'createDepositAddress': True,
                'createMarketOrder': False,
                'fetchClosedOrders': 'emulated',
                'fetchDepositAddress': True,
                'fetchDeposits': False,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBooks': True,
                'fetchOrders': 'emulated',
                'fetchTickers': True,
                'fetchTransactions': False,
                'fetchWithdrawals': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766910-cdcbfdae-5eea-11e7-9859-03fea873272d.jpg',
                'api': {
                    'public': 'https://yobit.net/api',
                    'private': 'https://yobit.net/tapi',
                },
                'www': 'https://www.yobit.net',
                'doc': 'https://www.yobit.net/en/api/',
                'fees': 'https://www.yobit.net/en/fees/',
            },
            'api': {
                'public': {
                    'get': [
                        'depth/{pair}',
                        'info',
                        'ticker/{pair}',
                        'trades/{pair}',
                    ],
                },
                'private': {
                    'post': [
                        'ActiveOrders',
                        'CancelOrder',
                        'GetDepositAddress',
                        'getInfo',
                        'OrderInfo',
                        'Trade',
                        'TradeHistory',
                        'WithdrawCoinsToAddress',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.002,
                    'taker': 0.002,
                },
                'funding': {
                    'withdraw': {},
                },
            },
            'commonCurrencies': {
                'AIR': 'AirCoin',
                'ANI': 'ANICoin',
                'ANT': 'AntsCoin',  # what is self, a coin for ants?
                'ATMCHA': 'ATM',
                'ASN': 'Ascension',
                'AST': 'Astral',
                'ATM': 'Autumncoin',
                'BCC': 'BCH',
                'BCS': 'BitcoinStake',
                'BLN': 'Bulleon',
                'BOT': 'BOTcoin',
                'BON': 'BONES',
                'BPC': 'BitcoinPremium',
                'BTS': 'Bitshares2',
                'CAT': 'BitClave',
                'CMT': 'CometCoin',
                'COV': 'Coven Coin',
                'COVX': 'COV',
                'CPC': 'Capricoin',
                'CS': 'CryptoSpots',
                'DCT': 'Discount',
                'DGD': 'DarkGoldCoin',
                'DIRT': 'DIRTY',
                'DROP': 'FaucetCoin',
                'DSH': 'DASH',
                'EKO': 'EkoCoin',
                'ENTER': 'ENTRC',
                'EPC': 'ExperienceCoin',
                'ESC': 'EdwardSnowden',
                'EUROPE': 'EUROP',
                'EXT': 'LifeExtension',
                'FUNK': 'FUNKCoin',
                'GCC': 'GlobalCryptocurrency',
                'GEN': 'Genstake',
                'GENE': 'Genesiscoin',
                'GOLD': 'GoldMint',
                'GOT': 'Giotto Coin',
                'HTML5': 'HTML',
                'HYPERX': 'HYPER',
                'ICN': 'iCoin',
                'INSANE': 'INSN',
                'JNT': 'JointCoin',
                'JPC': 'JupiterCoin',
                'KNC': 'KingN Coin',
                'LBTCX': 'LiteBitcoin',
                'LIZI': 'LiZi',
                'LOC': 'LocoCoin',
                'LOCX': 'LOC',
                'LUNYR': 'LUN',
                'LUN': 'LunarCoin',  # they just change the ticker if it is already taken
                'MDT': 'Midnight',
                'NAV': 'NavajoCoin',
                'NBT': 'NiceBytes',
                'OMG': 'OMGame',
                'PAC': '$PAC',
                'PLAY': 'PlayCoin',
                'PIVX': 'Darknet',
                'PRS': 'PRE',
                'PUTIN': 'PUT',
                'STK': 'StakeCoin',
                'SUB': 'Subscriptio',
                'PAY': 'EPAY',
                'PLC': 'Platin Coin',
                'RCN': 'RCoin',
                'REP': 'Republicoin',
                'RUR': 'RUB',
                'XIN': 'XINCoin',
            },
            'options': {
                # 'fetchTickersMaxLength': 2048,
                'fetchOrdersRequiresSymbol': True,
                'fetchTickersMaxLength': 512,
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
                    'Total transaction amount': ExchangeError,  # {"success": 0, "error": "Total transaction amount is less than minimal total: 0.00010000"}
                    'Insufficient funds': InsufficientFunds,
                    'invalid key': AuthenticationError,
                    'invalid nonce': InvalidNonce,  # {"success":0,"error":"invalid nonce(has already been used)"}'
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo(params)
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "funds":{
        #                 "ltc":22,
        #                 "nvc":423.998,
        #                 "ppc":10,
        #             },
        #             "funds_incl_orders":{
        #                 "ltc":32,
        #                 "nvc":523.998,
        #                 "ppc":20,
        #             },
        #             "rights":{
        #                 "info":1,
        #                 "trade":0,
        #                 "withdraw":0
        #             },
        #             "transaction_count":0,
        #             "open_orders":1,
        #             "server_time":1418654530
        #         }
        #     }
        #
        balances = self.safe_value(response, 'return', {})
        result = {'info': response}
        free = self.safe_value(balances, 'funds', {})
        total = self.safe_value(balances, 'funds_incl_orders', {})
        currencyIds = list(self.extend(free, total).keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(free, currencyId)
            account['total'] = self.safe_float(total, currencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_markets(self, params={}):
        response = self.publicGetInfo(params)
        markets = self.safe_value(response, 'pairs')
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'decimal_places'),
                'price': self.safe_integer(market, 'decimal_places'),
            }
            amountLimits = {
                'min': self.safe_float(market, 'min_amount'),
                'max': self.safe_float(market, 'max_amount'),
            }
            priceLimits = {
                'min': self.safe_float(market, 'min_price'),
                'max': self.safe_float(market, 'max_price'),
            }
            costLimits = {
                'min': self.safe_float(market, 'min_total'),
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            hidden = self.safe_integer(market, 'hidden')
            active = (hidden == 0)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'taker': market['fee'] / 100,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 150, max = 2000
        response = self.publicGetDepthPair(self.extend(request, params))
        market_id_in_reponse = (market['id'] in list(response.keys()))
        if not market_id_in_reponse:
            raise ExchangeError(self.id + ' ' + market['symbol'] + ' order book is empty or not available')
        orderbook = response[market['id']]
        return self.parse_order_book(orderbook)

    def fetch_order_books(self, symbols=None, params={}):
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
        response = self.publicGetDepthPair(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            result[symbol] = self.parse_order_book(response[id])
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #   {   high: 0.03497582,
        #         low: 0.03248474,
        #         avg: 0.03373028,
        #         vol: 120.11485715062999,
        #     vol_cur: 3572.24914074,
        #        last: 0.0337611,
        #         buy: 0.0337442,
        #        sell: 0.03377798,
        #     updated: 1537522009          }
        #
        timestamp = self.safe_timestamp(ticker, 'updated')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
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
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_float(ticker, 'avg'),
            'baseVolume': self.safe_float(ticker, 'vol_cur'),
            'quoteVolume': self.safe_float(ticker, 'vol'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        ids = self.ids
        if symbols is None:
            numIds = len(ids)
            ids = '-'.join(ids)
            maxLength = self.safe_integer(self.options, 'fetchTickersMaxLength', 2048)
            # max URL length is 2048 symbols, including http schema, hostname, tld, etc...
            if len(ids) > self.options['fetchTickersMaxLength']:
                raise ArgumentsRequired(self.id + ' has ' + str(numIds) + ' markets exceeding max URL length for self endpoint(' + str(maxLength) + ' characters), please, specify a list of symbols of interest in the first argument to fetchTickers')
        else:
            ids = self.market_ids(symbols)
            ids = '-'.join(ids)
        request = {
            'pair': ids,
        }
        tickers = self.publicGetTickerPair(self.extend(request, params))
        result = {}
        keys = list(tickers.keys())
        for k in range(0, len(keys)):
            id = keys[k]
            ticker = tickers[id]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

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
        price = self.safe_float_2(trade, 'rate', 'price')
        id = self.safe_string_2(trade, 'trade_id', 'tid')
        order = self.safe_string(trade, 'order_id')
        if 'pair' in trade:
            marketId = self.safe_string(trade, 'pair')
            market = self.safe_value(self.markets_by_id, marketId, market)
        symbol = None
        if market is not None:
            symbol = market['symbol']
        amount = self.safe_float(trade, 'amount')
        type = 'limit'  # all trades are still limit trades
        takerOrMaker = None
        fee = None
        feeCost = self.safe_float(trade, 'commission')
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
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        return {
            'id': id,
            'order': order,
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
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': side,
            'amount': self.amount_to_precision(symbol, amount),
            'rate': self.price_to_precision(symbol, price),
        }
        price = float(price)
        amount = float(amount)
        response = self.privatePostTrade(self.extend(request, params))
        id = None
        status = 'open'
        filled = 0.0
        remaining = amount
        if 'return' in response:
            id = self.safe_string(response['return'], 'order_id')
            if id == '0':
                id = self.safe_string(response['return'], 'init_order_id')
                status = 'closed'
            filled = self.safe_float(response['return'], 'received', 0.0)
            remaining = self.safe_float(response['return'], 'remains', amount)
        timestamp = self.milliseconds()
        order = {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': price * filled,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }
        self.orders[id] = order
        return self.extend({'info': response}, order)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': int(id),
        }
        response = self.privatePostCancelOrder(self.extend(request, params))
        if id in self.orders:
            self.orders[id]['status'] = 'canceled'
        return response

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'closed',
            '2': 'canceled',
            '3': 'open',  # or partially-filled and canceled? https://github.com/ccxt/ccxt/issues/1594
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_timestamp(order, 'timestamp_created')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'pair')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        remaining = self.safe_float(order, 'amount')
        amount = None
        price = self.safe_float(order, 'rate')
        filled = None
        cost = None
        if 'start_amount' in order:
            amount = self.safe_float(order, 'start_amount')
        else:
            if id in self.orders:
                amount = self.orders[id]['amount']
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
                cost = price * filled
        fee = None
        type = 'limit'
        side = self.safe_string(order, 'type')
        result = {
            'info': order,
            'id': id,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'status': status,
            'fee': fee,
        }
        return result

    def parse_orders(self, orders, market=None, since=None, limit=None, params={}):
        result = []
        ids = list(orders.keys())
        symbol = None
        if market is not None:
            symbol = market['symbol']
        for i in range(0, len(ids)):
            id = ids[i]
            order = self.extend({'id': id}, orders[id])
            result.append(self.extend(self.parse_order(order, market), params))
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': int(id),
        }
        response = self.privatePostOrderInfo(self.extend(request, params))
        id = str(id)
        newOrder = self.parse_order(self.extend({'id': id}, response['return'][id]))
        oldOrder = self.orders[id] if (id in list(self.orders.keys())) else {}
        self.orders[id] = self.extend(oldOrder, newOrder)
        return self.orders[id]

    def update_cached_orders(self, openOrders, symbol):
        # update local cache with open orders
        # self will add unseen orders and overwrite existing ones
        for j in range(0, len(openOrders)):
            id = openOrders[j]['id']
            self.orders[id] = openOrders[j]
        openOrdersIndexedById = self.index_by(openOrders, 'id')
        cachedOrderIds = list(self.orders.keys())
        for k in range(0, len(cachedOrderIds)):
            # match each cached order to an order in the open orders array
            # possible reasons why a cached order may be missing in the open orders array:
            # - order was closed or canceled -> update cache
            # - symbol mismatch(e.g. cached BTC/USDT, fetched ETH/USDT) -> skip
            cachedOrderId = cachedOrderIds[k]
            cachedOrder = self.orders[cachedOrderId]
            if not(cachedOrderId in list(openOrdersIndexedById.keys())):
                # cached order is not in open orders array
                # if we fetched orders by symbol and it doesn't match the cached order -> won't update the cached order
                if symbol is not None and symbol != cachedOrder['symbol']:
                    continue
                # cached order is absent from the list of open orders -> mark the cached order as closed
                if cachedOrder['status'] == 'open':
                    cachedOrder = self.extend(cachedOrder, {
                        'status': 'closed',  # likewise it might have been canceled externally(unnoticed by "us")
                        'cost': None,
                        'filled': cachedOrder['amount'],
                        'remaining': 0.0,
                    })
                    if cachedOrder['cost'] is None:
                        if cachedOrder['filled'] is not None:
                            cachedOrder['cost'] = cachedOrder['filled'] * cachedOrder['price']
                    self.orders[cachedOrderId] = cachedOrder
        return self.to_array(self.orders)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = self.privatePostActiveOrders(self.extend(request, params))
        # can only return 'open' orders(i.e. no way to fetch 'closed' orders)
        openOrders = []
        if 'return' in response:
            openOrders = self.parse_orders(response['return'], market)
        allOrders = self.update_cached_orders(openOrders, symbol)
        result = self.filter_by_symbol(allOrders, symbol)
        return self.filter_by_since_limit(result, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'open')

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a `symbol` argument')
        self.load_markets()
        market = self.market(symbol)
        # some derived classes use camelcase notation for request fields
        request = {
            # 'from': 123456789,  # trade ID, from which the display starts numerical 0(test result: liqui ignores self field)
            # 'count': 1000,  # the number of trades for display numerical, default = 1000
            # 'from_id': trade ID, from which the display starts numerical 0
            # 'end_id': trade ID on which the display ends numerical ∞
            # 'order': 'ASC',  # sorting, default = DESC(test result: liqui ignores self field, most recent trade always goes last)
            # 'since': 1234567890,  # UTC start time, default = 0(test result: liqui ignores self field)
            # 'end': 1234567890,  # UTC end time, default = ∞(test result: liqui ignores self field)
            'pair': market['id'],
        }
        if limit is not None:
            request['count'] = int(limit)
        if since is not None:
            request['since'] = int(since / 1000)
        response = self.privatePostTradeHistory(self.extend(request, params))
        trades = self.safe_value(response, 'return', {})
        ids = list(trades.keys())
        result = []
        for i in range(0, len(ids)):
            id = ids[i]
            trade = self.parse_trade(self.extend(trades[id], {
                'trade_id': id,
            }), market)
            result.append(trade)
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def create_deposit_address(self, code, params={}):
        request = {
            'need_new': 1,
        }
        response = self.fetch_deposit_address(code, self.extend(request, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response['info'],
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'coinName': currency['id'],
            'need_new': 0,
        }
        response = self.privatePostGetDepositAddress(self.extend(request, params))
        address = self.safe_string(response['return'], 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'coinName': currency['id'],
            'amount': amount,
            'address': address,
        }
        # no docs on the tag, yet...
        if tag is not None:
            raise ExchangeError(self.id + ' withdraw() does not support the tag argument yet due to a lack of docs on withdrawing with tag/memo on behalf of the exchange.')
        response = self.privatePostWithdrawCoinsToAddress(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = float(self.cost_to_precision(symbol, amount * rate))
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': cost,
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
            url += '/' + self.version + '/' + self.implode_params(path, params)
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
            # 1 - Liqui only returns the integer 'success' key from their private API
            #
            #     {"success": 1, ...} httpCode == 200
            #     {"success": 0, ...} httpCode == 200
            #
            # 2 - However, exchanges derived from Liqui, can return non-integers
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
                feedback = self.id + ' ' + self.json(response)
                exact = self.exceptions['exact']
                if code in exact:
                    raise exact[code](feedback)
                elif message in exact:
                    raise exact[message](feedback)
                broad = self.exceptions['broad']
                broadKey = self.findBroadlyMatchedKey(broad, message)
                if broadKey is not None:
                    raise broad[broadKey](feedback)
                raise ExchangeError(feedback)  # unknown message
