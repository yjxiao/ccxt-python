# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import InvalidNonce


class kucoin (Exchange):

    def describe(self):
        return self.deep_extend(super(kucoin, self).describe(), {
            'id': 'kucoin',
            'name': 'Kucoin',
            'countries': 'HK',  # Hong Kong
            'version': 'v1',
            'rateLimit': 2000,
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': False,
                'cancelOrders': True,
                'createMarketOrder': False,
                'fetchDepositAddress': True,
                'fetchTickers': True,
                'fetchOHLCV': True,  # see the method implementation below
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'fetchCurrencies': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': 1,
                '5m': 5,
                '15m': 15,
                '30m': 30,
                '1h': 60,
                '8h': 480,
                '1d': 'D',
                '1w': 'W',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/33795655-b3c46e48-dcf6-11e7-8abe-dc4588ba7901.jpg',
                'api': {
                    'public': 'https://api.kucoin.com',
                    'private': 'https://api.kucoin.com',
                    'kitchen': 'https://kitchen.kucoin.com',
                    'kitchen-2': 'https://kitchen-2.kucoin.com',
                },
                'www': 'https://kucoin.com',
                'doc': 'https://kucoinapidocs.docs.apiary.io',
                'fees': 'https://news.kucoin.com/en/fee',
            },
            'api': {
                'kitchen': {
                    'get': [
                        'open/chart/history',
                    ],
                },
                'public': {
                    'get': [
                        'open/chart/config',
                        'open/chart/history',
                        'open/chart/symbol',
                        'open/currencies',
                        'open/deal-orders',
                        'open/kline',
                        'open/lang-list',
                        'open/orders',
                        'open/orders-buy',
                        'open/orders-sell',
                        'open/tick',
                        'market/open/coin-info',
                        'market/open/coins',
                        'market/open/coins-trending',
                        'market/open/symbols',
                    ],
                },
                'private': {
                    'get': [
                        'account/balance',
                        'account/{coin}/wallet/address',
                        'account/{coin}/wallet/records',
                        'account/{coin}/balance',
                        'account/promotion/info',
                        'account/promotion/sum',
                        'deal-orders',
                        'order/active',
                        'order/active-map',
                        'order/dealt',
                        'order/detail',
                        'referrer/descendant/count',
                        'user/info',
                    ],
                    'post': [
                        'account/{coin}/withdraw/apply',
                        'account/{coin}/withdraw/cancel',
                        'account/promotion/draw',
                        'cancel-order',
                        'order',
                        'order/cancel-all',
                        'user/change-lang',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.001,
                    'taker': 0.001,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'KCS': 2.0,
                        'BTC': 0.0005,
                        'USDT': 10.0,
                        'ETH': 0.01,
                        'LTC': 0.001,
                        'NEO': 0.0,
                        'GAS': 0.0,
                        'KNC': 0.5,
                        'BTM': 5.0,
                        'QTUM': 0.1,
                        'EOS': 0.5,
                        'CVC': 3.0,
                        'OMG': 0.1,
                        'PAY': 0.5,
                        'SNT': 20.0,
                        'BHC': 1.0,
                        'HSR': 0.01,
                        'WTC': 0.1,
                        'VEN': 2.0,
                        'MTH': 10.0,
                        'RPX': 1.0,
                        'REQ': 20.0,
                        'EVX': 0.5,
                        'MOD': 0.5,
                        'NEBL': 0.1,
                        'DGB': 0.5,
                        'CAG': 2.0,
                        'CFD': 0.5,
                        'RDN': 0.5,
                        'UKG': 5.0,
                        'BCPT': 5.0,
                        'PPT': 0.1,
                        'BCH': 0.0005,
                        'STX': 2.0,
                        'NULS': 1.0,
                        'GVT': 0.1,
                        'HST': 2.0,
                        'PURA': 0.5,
                        'SUB': 2.0,
                        'QSP': 5.0,
                        'POWR': 1.0,
                        'FLIXX': 10.0,
                        'LEND': 20.0,
                        'AMB': 3.0,
                        'RHOC': 2.0,
                        'R': 2.0,
                        'DENT': 50.0,
                        'DRGN': 1.0,
                        'ACT': 0.1,
                    },
                    'deposit': {},
                },
            },
            # exchange-specific options
            'options': {
                'timeDifference': 0,  # the difference between system clock and Kucoin clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
            },
        })

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def load_time_difference(self):
        before = self.milliseconds()
        response = self.publicGetOpenTick()
        after = self.milliseconds()
        self.options['timeDifference'] = int((self.sum(before, after) / 2) - response['timestamp'])
        return self.options['timeDifference']

    def fetch_markets(self):
        response = self.publicGetMarketOpenSymbols()
        if self.options['adjustForTimeDifference']:
            self.load_time_difference()
        markets = response['data']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['symbol']
            base = market['coinType']
            quote = market['coinTypePair']
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': 8,
            }
            active = market['trading']
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'active': active,
                'taker': self.safe_float(market, 'feeRate'),
                'maker': self.safe_float(market, 'feeRate'),
                'info': market,
                'lot': math.pow(10, -precision['amount']),
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privateGetAccountCoinWalletAddress(self.extend({
            'coin': currency['id'],
        }, params))
        data = response['data']
        address = self.safe_string(data, 'address')
        tag = self.safe_string(data, 'userOid')
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'status': 'ok',
            'info': response,
        }

    def fetch_currencies(self, params={}):
        response = self.publicGetMarketOpenCoins(params)
        currencies = response['data']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['coin']
            # todo: will need to rethink the fees
            # to add support for multiple withdrawal/deposit methods and
            # differentiated fees for each particular method
            code = self.common_currency_code(id)
            precision = currency['tradePrecision']
            deposit = currency['enableDeposit']
            withdraw = currency['enableWithdraw']
            active = (deposit and withdraw)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': currency['name'],
                'active': active,
                'status': 'ok',
                'fee': currency['withdrawMinFee'],  # todo: redesign
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['withdrawMinAmount'],
                        'max': math.pow(10, precision),
                    },
                },
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccountBalance(self.extend({
            'limit': 20,  # default 12, max 20
            'page': 1,
        }, params))
        balances = response['data']
        result = {'info': balances}
        indexed = self.index_by(balances, 'coinType')
        keys = list(indexed.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            currency = self.common_currency_code(id)
            account = self.account()
            balance = indexed[id]
            used = float(balance['freezeBalance'])
            free = float(balance['balance'])
            total = self.sum(free, used)
            account['free'] = free
            account['used'] = used
            account['total'] = total
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenOrders(self.extend({
            'symbol': market['id'],
        }, params))
        orderbook = response['data']
        return self.parse_order_book(orderbook, None, 'BUY', 'SELL')

    def parse_order(self, order, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            symbol = order['coinType'] + '/' + order['coinTypePair']
        timestamp = self.safe_value(order, 'createdAt')
        price = self.safe_float(order, 'price')
        if price is None:
            price = self.safe_float(order, 'dealPrice')
        if price is None:
            price = self.safe_float(order, 'dealPriceAverage')
        if price is None:
            price = self.safe_float(order, 'orderPrice')
        remaining = self.safe_float(order, 'pendingAmount')
        status = self.safe_value(order, 'status')
        filled = self.safe_float(order, 'dealAmount')
        if status is None:
            if remaining is not None:
                if remaining > 0:
                    status = 'open'
                else:
                    status = 'closed'
        if filled is None:
            if status is not None:
                if status == 'closed':
                    filled = self.safe_float(order, 'amount')
        amount = self.safe_float(order, 'amount')
        cost = self.safe_float(order, 'dealValue')
        if cost is None:
            cost = self.safe_float(order, 'dealValueTotal')
        if filled is not None:
            if price is not None:
                if cost is None:
                    cost = price * filled
            if amount is None:
                if remaining is not None:
                    amount = self.sum(filled, remaining)
            elif remaining is None:
                remaining = amount - filled
        if (status == 'open') and(cost is None):
            cost = price * amount
        side = self.safe_value(order, 'direction')
        if side is None:
            side = order['type']
        if side is not None:
            side = side.lower()
        feeCurrency = None
        if market:
            feeCurrency = market['quote'] if (side == 'sell') else market['base']
        else:
            feeCurrencyField = 'coinTypePair' if (side == 'sell') else 'coinType'
            feeCurrency = self.safe_string(order, feeCurrencyField)
            if feeCurrency is not None:
                if feeCurrency in self.currencies_by_id:
                    feeCurrency = self.currencies_by_id[feeCurrency]['code']
        feeCost = self.safe_float(order, 'fee')
        fee = {
            'cost': self.safe_float(order, 'feeTotal', feeCost),
            'rate': self.safe_float(order, 'feeRate'),
            'currency': feeCurrency,
        }
        # todo: parse order trades and fill fees from 'datas'
        # do not confuse trades with orders
        orderId = self.safe_string(order, 'orderOid')
        if orderId is None:
            orderId = self.safe_string(order, 'oid')
        result = {
            'info': order,
            'id': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }
        return result

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol argument')
        orderType = self.safe_value(params, 'type')
        if orderType is None:
            raise ExchangeError(self.id + ' fetchOrder requires a type parameter("BUY" or "SELL")')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': orderType,
            'orderOid': id,
        }
        response = self.privateGetOrderDetail(self.extend(request, params))
        order = response['data']
        if not order:
            raise OrderNotFound(self.id + ' ' + self.json(response))
        return self.parse_order(response['data'], market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.privateGetOrderActiveMap(self.extend(request, params))
        orders = self.array_concat(response['data']['SELL'], response['data']['BUY'])
        result = []
        for i in range(0, len(orders)):
            result.append(self.extend(orders[i], {'status': 'open'}))
        return self.parse_orders(result, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {}
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['since'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetOrderDealt(self.extend(request, params))
        orders = response['data']['datas']
        result = []
        for i in range(0, len(orders)):
            result.append(self.extend(orders[i], {'status': 'closed'}))
        return self.parse_orders(result, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        base = market['base']
        order = {
            'symbol': market['id'],
            'type': side.upper(),
            'price': self.price_to_precision(symbol, price),
            'amount': self.truncate(amount, self.currencies[base]['precision']),
        }
        response = self.privatePostOrder(self.extend(order, params))
        return {
            'info': response,
            'id': self.safe_string(response['data'], 'orderOid'),
        }

    def cancel_orders(self, symbol=None, params={}):
        # https://kucoinapidocs.docs.apiary.io/#reference/0/trading/cancel-all-orders
        # docs say symbol is required, but it seems to be optional
        # you can cancel all orders, or filter by symbol or type or both
        request = {}
        if symbol:
            self.load_markets()
            market = self.market(symbol)
            request['symbol'] = market['id']
        if 'type' in params:
            request['type'] = params['type'].upper()
            params = self.omit(params, 'type')
        response = self.privatePostOrderCancelAll(self.extend(request, params))
        return response

    def cancel_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' cancelOrder requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'orderOid': id,
        }
        if 'type' in params:
            request['type'] = params['type'].upper()
            params = self.omit(params, 'type')
        else:
            raise ExchangeError(self.id + ' cancelOrder requires parameter type=["BUY"|"SELL"]')
        response = self.privatePostCancelOrder(self.extend(request, params))
        return response

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['datetime']
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            symbol = ticker['coinType'] + '/' + ticker['coinTypePair']
        # TNC coin doesn't have changerate for some reason
        change = self.safe_float(ticker, 'changeRate')
        if change is not None:
            change *= 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'ask': self.safe_float(ticker, 'sell'),
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': self.safe_float(ticker, 'lastDealPrice'),
            'change': change,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': self.safe_float(ticker, 'volValue'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        response = self.publicGetMarketOpenSymbols(params)
        tickers = response['data']
        result = {}
        for t in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[t])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenTick(self.extend({
            'symbol': market['id'],
        }, params))
        ticker = response['data']
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        id = None
        order = None
        info = trade
        timestamp = None
        type = None
        side = None
        price = None
        cost = None
        amount = None
        fee = None
        if isinstance(trade, list):
            timestamp = trade[0]
            type = 'limit'
            if trade[1] == 'BUY':
                side = 'buy'
            elif trade[1] == 'SELL':
                side = 'sell'
            price = trade[2]
            amount = trade[3]
        else:
            timestamp = self.safe_value(trade, 'createdAt')
            order = self.safe_string(trade, 'orderOid')
            if order is None:
                order = self.safe_string(trade, 'oid')
            side = trade['dealDirection'].lower()
            price = self.safe_float(trade, 'dealPrice')
            amount = self.safe_float(trade, 'amount')
            cost = self.safe_float(trade, 'dealValue')
            feeCurrency = None
            if 'coinType' in trade:
                feeCurrency = self.safe_string(trade, 'coinType')
                if feeCurrency is not None:
                    if feeCurrency in self.currencies_by_id:
                        feeCurrency = self.currencies_by_id[feeCurrency]['code']
            fee = {
                'cost': self.safe_float(trade, 'fee'),
                'currency': feeCurrency,
            }
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'order': order,
            'info': info,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenDealOrders(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit:
            request['limit'] = limit
        response = self.privateGetDealOrders(self.extend(request, params))
        return self.parse_trades(response['data']['datas'], market, since, limit)

    def parse_trading_view_ohlcvs(self, ohlcvs, market=None, timeframe='1m', since=None, limit=None):
        result = []
        for i in range(0, len(ohlcvs['t'])):
            result.append([
                ohlcvs['t'][i] * 1000,
                ohlcvs['o'][i],
                ohlcvs['h'][i],
                ohlcvs['l'][i],
                ohlcvs['c'][i],
                ohlcvs['v'][i],
            ])
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        end = self.seconds()
        resolution = self.timeframes[timeframe]
        # convert 'resolution' to minutes in order to calculate 'from' later
        minutes = resolution
        if minutes == 'D':
            if limit is None:
                limit = 30  # 30 days, 1 month
            minutes = 1440
        elif minutes == 'W':
            if limit is None:
                limit = 52  # 52 weeks, 1 year
            minutes = 10080
        elif limit is None:
            # last 1440 periods, whatever the duration of the period is
            # for 1m it equals 1 day(24 hours)
            # for 5m it equals 5 days
            # ...
            limit = 1440
        start = end - limit * minutes * 60
        # if 'since' has been supplied by user
        if since is not None:
            start = int(since / 1000)  # convert milliseconds to seconds
            end = min(end, self.sum(start, limit * minutes * 60))
        request = {
            'symbol': market['id'],
            'resolution': resolution,
            'from': start,
            'to': end,
        }
        response = self.publicGetOpenChartHistory(self.extend(request, params))
        return self.parse_trading_view_ohlcvs(response, market, timeframe, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privatePostAccountCoinWithdrawApply(self.extend({
            'coin': currency['id'],
            'amount': amount,
            'address': address,
        }, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        endpoint = '/' + self.version + '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + endpoint
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            # their nonce is always a calibrated synched milliseconds-timestamp
            nonce = self.nonce()
            queryString = ''
            nonce = str(nonce)
            if query:
                queryString = self.rawencode(self.keysort(query))
                url += '?' + queryString
                if method != 'GET':
                    body = queryString
            auth = endpoint + '/' + nonce + '/' + queryString
            payload = base64.b64encode(self.encode(auth))
            # payload should be "encoded" as returned from stringToBase64
            signature = self.hmac(payload, self.encode(self.secret), hashlib.sha256)
            headers = {
                'KC-API-KEY': self.apiKey,
                'KC-API-NONCE': nonce,
                'KC-API-SIGNATURE': signature,
            }
        else:
            if query:
                url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def throw_exception_on_error(self, response):
        #
        # API endpoints return the following formats
        #     {success: False, code: "ERROR", msg: "Min price:100.0"}
        #     {success: True,  code: "OK",    msg: "Operation succeeded."}
        #
        # Web OHLCV endpoint returns self:
        #     {s: "ok", o: [], h: [], l: [], c: [], v: []}
        #
        # This particular method handles API responses only
        #
        if not('success' in list(response.keys())):
            return
        if response['success'] is True:
            return  # not an error
        if not('code' in list(response.keys())) or not('msg' in list(response.keys())):
            raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
        code = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg')
        feedback = self.id + ' ' + self.json(response)
        if code == 'UNAUTH':
            if message == 'Invalid nonce':
                raise InvalidNonce(feedback)
            raise AuthenticationError(feedback)
        elif code == 'ERROR':
            if message.find('The precision of amount') >= 0:
                raise InvalidOrder(feedback)  # amount violates precision.amount
            if message.find('Min amount each order') >= 0:
                raise InvalidOrder(feedback)  # amount < limits.amount.min
            if message.find('Min price:') >= 0:
                raise InvalidOrder(feedback)  # price < limits.price.min
            if message.find('The precision of price') >= 0:
                raise InvalidOrder(feedback)  # price violates precision.price
        elif code == 'NO_BALANCE':
            if message.find('Insufficient balance') >= 0:
                raise InsufficientFunds(feedback)
        raise ExchangeError(self.id + ': unknown response: ' + self.json(response))

    def handle_errors(self, code, reason, url, method, headers, body, response=None):
        if response is not None:
            # JS callchain parses body beforehand
            self.throw_exception_on_error(response)
        elif body and(body[0] == '{'):
            # Python/PHP callchains don't have json available at self step
            self.throw_exception_on_error(json.loads(body))
