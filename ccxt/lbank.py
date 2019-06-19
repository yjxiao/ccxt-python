# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import DDoSProtection


class lbank (Exchange):

    def describe(self):
        return self.deep_extend(super(lbank, self).describe(), {
            'id': 'lbank',
            'name': 'LBank',
            'countries': ['CN'],
            'version': 'v1',
            'has': {
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': False,  # status 0 API doesn't work
                'fetchClosedOrders': True,
            },
            'timeframes': {
                '1m': 'minute1',
                '5m': 'minute5',
                '15m': 'minute15',
                '30m': 'minute30',
                '1h': 'hour1',
                '2h': 'hour2',
                '4h': 'hour4',
                '6h': 'hour6',
                '8h': 'hour8',
                '12h': 'hour12',
                '1d': 'day1',
                '1w': 'week1',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38063602-9605e28a-3302-11e8-81be-64b1e53c4cfb.jpg',
                'api': 'https://api.lbank.info',
                'www': 'https://www.lbank.info',
                'doc': 'https://github.com/LBank-exchange/lbank-official-api-docs',
                'fees': 'https://lbankinfo.zendesk.com/hc/zh-cn/articles/115002295114--%E8%B4%B9%E7%8E%87%E8%AF%B4%E6%98%8E',
                'referral': 'https://www.lbex.io/sign-up.html?icode=7QCY&lang=en-US',
            },
            'api': {
                'public': {
                    'get': [
                        'currencyPairs',
                        'ticker',
                        'depth',
                        'trades',
                        'kline',
                        'accuracy',
                    ],
                },
                'private': {
                    'post': [
                        'user_info',
                        'create_order',
                        'cancel_order',
                        'orders_info',
                        'orders_info_history',
                        'withdraw',
                        'withdrawCancel',
                        'withdraws',
                        'withdrawConfigs',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': None,
                        'ZEC': 0.01,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        # 'QTUM': amount => max(0.01, amount * (0.1 / 100)),
                        'VEN': 10.0,
                        'BCH': 0.0002,
                        'SC': 50.0,
                        'BTM': 20.0,
                        'NAS': 1.0,
                        'EOS': 1.0,
                        'XWC': 5.0,
                        'BTS': 1.0,
                        'INK': 10.0,
                        'BOT': 3.0,
                        'YOYOW': 15.0,
                        'TGC': 10.0,
                        'NEO': 0.0,
                        'CMT': 20.0,
                        'SEER': 2000.0,
                        'FIL': None,
                        'BTG': None,
                    },
                },
            },
            'commonCurrencies': {
                'VET_ERC20': 'VEN',
            },
            'options': {
                'cacheSecretAsPem': True,
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetAccuracy(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = market['symbol']
            parts = id.split('_')
            baseId = None
            quoteId = None
            numParts = len(parts)
            # lbank will return symbols like "vet_erc20_usdt"
            if numParts > 2:
                baseId = parts[0] + '_' + parts[1]
                quoteId = parts[2]
            else:
                baseId = parts[0]
                quoteId = parts[1]
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'quantityAccuracy'),
                'price': self.safe_integer(market, 'priceAccuracy'),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': math.pow(10, precision['price']),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': id,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(ticker, 'symbol')
            if marketId in self.markets_by_id:
                market = self.marketsById[marketId]
                symbol = market['symbol']
            else:
                parts = marketId.split('_')
                baseId = None
                quoteId = None
                numParts = len(parts)
                # lbank will return symbols like "vet_erc20_usdt"
                if numParts > 2:
                    baseId = parts[0] + '_' + parts[1]
                    quoteId = parts[2]
                else:
                    baseId = parts[0]
                    quoteId = parts[1]
                base = self.common_currency_code(baseId.upper())
                quote = self.common_currency_code(quoteId.upper())
                symbol = base + '/' + quote
        timestamp = self.safe_integer(ticker, 'timestamp')
        info = ticker
        ticker = info['ticker']
        last = self.safe_float(ticker, 'latest')
        percentage = self.safe_float(ticker, 'change')
        relativeChange = percentage / 100
        open = last / self.sum(1, relativeChange)
        change = last - open
        average = self.sum(last, open) / 2
        if market is not None:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': self.safe_float(ticker, 'turnover'),
            'info': info,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        request = {
            'symbol': 'all',
        }
        response = self.publicGetTicker(self.extend(request, params))
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_order_book(self, symbol, limit=60, params={}):
        self.load_markets()
        size = 60
        if limit is not None:
            size = min(limit, size)
        request = {
            'symbol': self.market_id(symbol),
            'size': size,
        }
        response = self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(trade, 'date_ms')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = self.cost_to_precision(symbol, price * amount)
                cost = float(cost)
        id = self.safe_string(trade, 'tid')
        type = None
        side = self.safe_string(trade, 'type')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': None,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': self.safe_value(trade, 'info', trade),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'size': 100,
        }
        if since is not None:
            request['time'] = int(since)
        if limit is not None:
            request['size'] = limit
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0] * 1000,
            ohlcv[1],
            ohlcv[2],
            ohlcv[3],
            ohlcv[4],
            ohlcv[5],
        ]

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        if since is None:
            raise ExchangeError(self.id + ' fetchOHLCV requires a `since` argument')
        if limit is None:
            raise ExchangeError(self.id + ' fetchOHLCV requires a `limit` argument')
        request = {
            'symbol': market['id'],
            'type': self.timeframes[timeframe],
            'size': limit,
            'time': int(since / 1000),
        }
        response = self.publicGetKline(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostUserInfo(params)
        result = {'info': response}
        info = self.safe_value(response, 'info', {})
        free = self.safe_value(info, 'free', {})
        freeze = self.safe_value(info, 'freeze', {})
        ids = list(self.extend(free, freeze).keys())
        for i in range(0, len(ids)):
            id = ids[i]
            code = self.common_currency_code(id.upper())
            account = self.account()
            account['free'] = self.safe_float(free, id)
            account['used'] = self.safe_float(freeze, id)
            result[code] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            '-1': 'cancelled',  # cancelled
            '0': 'open',  # not traded
            '1': 'open',  # partial deal
            '2': 'closed',  # complete deal
            '4': 'closed',  # disposal processing
        }
        return self.safe_string(statuses, status)

    def parse_order(self, order, market=None):
        symbol = None
        responseMarket = self.safe_value(self.marketsById, order['symbol'])
        if responseMarket is not None:
            symbol = responseMarket['symbol']
        elif market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'create_time')
        # Limit Order Request Returns: Order Price
        # Market Order Returns: cny amount of market order
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount', 0.0)
        filled = self.safe_float(order, 'deal_amount', 0.0)
        av_price = self.safe_float(order, 'avg_price')
        cost = None
        if av_price is not None:
            cost = filled * av_price
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'order_id')
        type = self.safe_string(order, 'order_type')
        side = self.safe_string(order, 'type')
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = amount - filled
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': self.safe_value(order, 'info', order),
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        order = {
            'symbol': market['id'],
            'type': side,
            'amount': amount,
        }
        if type == 'market':
            order['type'] += '_market'
        else:
            order['price'] = price
        response = self.privatePostCreateOrder(self.extend(order, params))
        order = self.omit(order, 'type')
        order['order_id'] = response['order_id']
        order['type'] = side
        order['order_type'] = type
        order['create_time'] = self.milliseconds()
        order['info'] = response
        order = self.parse_order(order, market)
        id = order['id']
        self.orders[id] = order
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = self.privatePostCancelOrder(self.extend(request, params))
        return response

    def fetch_order(self, id, symbol=None, params={}):
        # Id can be a list of ids delimited by a comma
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = self.privatePostOrdersInfo(self.extend(request, params))
        orders = self.parse_orders(response['orders'], market)
        numOrders = len(orders)
        if numOrders == 1:
            return orders[0]
        else:
            return orders

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        if limit is None:
            limit = 100
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'current_page': 1,
            'page_length': limit,
        }
        response = self.privatePostOrdersInfoHistory(self.extend(request, params))
        return self.parse_orders(response['orders'], None, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        closed = self.filter_by(orders, 'status', 'closed')
        canceled = self.filter_by(orders, 'status', 'cancelled')  # cancelled orders may be partially filled
        allOrders = self.array_concat(closed, canceled)
        return self.filter_by_symbol_since_limit(allOrders, symbol, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        # mark and fee are optional params, mark is a note and must be less than 255 characters
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'assetCode': currency['id'],
            'amount': amount,
            'account': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostWithdraw(self.extend(request, params))
        return {
            'id': response['id'],
            'info': response,
        }

    def convert_secret_to_pem(self, secret):
        lineLength = 64
        secretLength = len(secret) - 0
        numLines = int(secretLength / lineLength)
        numLines = self.sum(numLines, 1)
        pem = "-----BEGIN PRIVATE KEY-----\n"  # eslint-disable-line
        for i in range(0, numLines):
            start = i * lineLength
            end = self.sum(start, lineLength)
            pem += self.secret[start:end] + "\n"  # eslint-disable-line
        return pem + '-----END PRIVATE KEY-----'

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        # Every endpoint ends with ".do"
        url += '.do'
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.keysort(self.extend({
                'api_key': self.apiKey,
            }, params))
            queryString = self.rawencode(query)
            message = self.hash(self.encode(queryString)).upper()
            cacheSecretAsPem = self.safe_value(self.options, 'cacheSecretAsPem', True)
            pem = None
            if cacheSecretAsPem:
                pem = self.safe_value(self.options, 'pem')
                if pem is None:
                    pem = self.convert_secret_to_pem(self.secret)
                    self.options['pem'] = pem
            else:
                pem = self.convert_secret_to_pem(self.secret)
            sign = self.binaryToBase64(self.rsa(message, pem, 'RS256'))
            query['sign'] = sign
            body = self.urlencode(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        success = self.safe_string(response, 'result')
        if success == 'false':
            errorCode = self.safe_string(response, 'error_code')
            message = self.safe_string({
                '10000': 'Internal error',
                '10001': 'The required parameters can not be empty',
                '10002': 'verification failed',
                '10003': 'Illegal parameters',
                '10004': 'User requests are too frequent',
                '10005': 'Key does not exist',
                '10006': 'user does not exist',
                '10007': 'Invalid signature',
                '10008': 'This currency pair is not supported',
                '10009': 'Limit orders can not be missing orders and the number of orders',
                '10010': 'Order price or order quantity must be greater than 0',
                '10011': 'Market orders can not be missing the amount of the order',
                '10012': 'market sell orders can not be missing orders',
                '10013': 'is less than the minimum trading position 0.001',
                '10014': 'Account number is not enough',
                '10015': 'The order type is wrong',
                '10016': 'Account balance is not enough',
                '10017': 'Abnormal server',
                '10018': 'order inquiry can not be more than 50 less than one',
                '10019': 'withdrawal orders can not be more than 3 less than one',
                '10020': 'less than the minimum amount of the transaction limit of 0.001',
                '10022': 'Insufficient key authority',
            }, errorCode, self.json(response))
            ErrorClass = self.safe_value({
                '10002': AuthenticationError,
                '10004': DDoSProtection,
                '10005': AuthenticationError,
                '10006': AuthenticationError,
                '10007': AuthenticationError,
                '10009': InvalidOrder,
                '10010': InvalidOrder,
                '10011': InvalidOrder,
                '10012': InvalidOrder,
                '10013': InvalidOrder,
                '10014': InvalidOrder,
                '10015': InvalidOrder,
                '10016': InvalidOrder,
                '10022': AuthenticationError,
            }, errorCode, ExchangeError)
            raise ErrorClass(message)
        return response
