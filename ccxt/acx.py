# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import json
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound


class acx (Exchange):

    def describe(self):
        return self.deep_extend(super(acx, self).describe(), {
            'id': 'acx',
            'name': 'ACX',
            'countries': 'AU',
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1',
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '2h': '120',
                '4h': '240',
                '12h': '720',
                '1d': '1440',
                '3d': '4320',
                '1w': '10080',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30247614-1fe61c74-9621-11e7-9e8c-f1a627afa279.jpg',
                'extension': '.json',
                'api': 'https://acx.io/api',
                'www': 'https://acx.io',
                'doc': 'https://acx.io/documents/api_v2',
            },
            'api': {
                'public': {
                    'get': [
                        'depth',  # Get depth or specified market Both asks and bids are sorted from highest price to lowest.
                        'k_with_pending_trades',  # Get K data with pending trades, which are the trades not included in K data yet, because there's delay between trade generated and processed by K data generator
                        'k',  # Get OHLC(k line) of specific market
                        'markets',  # Get all available markets
                        'order_book',  # Get the order book of specified market
                        'order_book/{market}',
                        'tickers',  # Get ticker of all markets
                        'tickers/{market}',  # Get ticker of specific market
                        'timestamp',  # Get server current time, in seconds since Unix epoch
                        'trades',  # Get recent trades on market, each trade is included only once Trades are sorted in reverse creation order.
                        'trades/{market}',
                    ],
                },
                'private': {
                    'get': [
                        'members/me',  # Get your profile and accounts info
                        'deposits',  # Get your deposits history
                        'deposit',  # Get details of specific deposit
                        'deposit_address',  # Where to deposit The address field could be empty when a new address is generating(e.g. for bitcoin), you should try again later in that case.
                        'orders',  # Get your orders, results is paginated
                        'order',  # Get information of specified order
                        'trades/my',  # Get your executed trades Trades are sorted in reverse creation order.
                        'withdraws',  # Get your cryptocurrency withdraws
                        'withdraw',  # Get your cryptocurrency withdraw
                    ],
                    'post': [
                        'orders',  # Create a Sell/Buy order
                        'orders/multi',  # Create multiple sell/buy orders
                        'orders/clear',  # Cancel all my orders
                        'order/delete',  # Cancel an order
                        'withdraw',  # Create a withdraw
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': True,
                    'withdraw': {},  # There is only 1% fee on withdrawals to your bank account.
                },
            },
            'exceptions': {
                '2002': InsufficientFunds,
                '2003': OrderNotFound,
            },
        })

    def fetch_markets(self):
        markets = self.publicGetMarkets()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            id = market['id']
            symbol = market['name']
            base, quote = symbol.split('/')
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetMembersMe()
        balances = response['accounts']
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            uppercase = currency.upper()
            account = {
                'free': float(balance['balance']),
                'used': float(balance['locked']),
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[uppercase] = account
        return self.parse_balance(result)

    def perform_order_book_request(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is None:
            request['limit'] = limit  # default = 300
        orderbook = self.publicGetDepth(self.extend(request, params))
        # result['bids'] = self.sort_by(result['bids'], 0, True)
        # result['asks'] = self.sort_by(result['asks'], 0)
        return orderbook

    def parse_order_book_timestamp(self, orderbook, keys):
        return orderbook[keys['timestamp']] * 1000

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['at'] * 1000
        ticker = ticker['ticker']
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high', None),
            'low': self.safe_float(ticker, 'low', None),
            'bid': self.safe_float(ticker, 'buy', None),
            'ask': self.safe_float(ticker, 'sell', None),
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': self.safe_float(ticker, 'last', None),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol', None),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTickers(params)
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                base = id[0:3]
                quote = id[3:6]
                base = base.upper()
                quote = quote.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(quote)
                symbol = base + '/' + quote
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTickersMarket(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['created_at'])
        return {
            'id': str(trade['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'volume'),
            'cost': self.safe_float(trade, 'funds'),
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTrades(self.extend({
            'market': market['id'],
        }, params))
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

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if not limit:
            limit = 500  # default is 30
        request = {
            'market': market['id'],
            'period': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['timestamp'] = since
        response = self.publicGetK(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_order(self, order, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            marketId = order['market']
            symbol = self.markets_by_id[marketId]['symbol']
        timestamp = self.parse8601(order['created_at'])
        state = order['state']
        status = None
        if state == 'done':
            status = 'closed'
        elif state == 'wait':
            status = 'open'
        elif state == 'cancel':
            status = 'canceled'
        return {
            'id': str(order['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'status': status,
            'symbol': symbol,
            'type': order['ord_type'],
            'side': order['side'],
            'price': float(order['price']),
            'amount': float(order['volume']),
            'filled': float(order['executed_volume']),
            'remaining': float(order['remaining_volume']),
            'trades': None,
            'fee': None,
            'info': order,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        order = {
            'market': self.market_id(symbol),
            'side': side,
            'volume': str(amount),
            'ord_type': type,
        }
        if type == 'limit':
            order['price'] = str(price)
        response = self.privatePostOrders(self.extend(order, params))
        market = self.markets_by_id[response['market']]
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        result = self.privatePostOrderDelete({'id': id})
        order = self.parse_order(result)
        status = order['status']
        if status == 'closed' or status == 'canceled':
            raise OrderNotFound(self.id + ' ' + self.json(order))
        return order

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        result = self.privatePostWithdraw(self.extend({
            'currency': currency.lower(),
            'sum': amount,
            'address': address,
        }, params))
        return {
            'info': result,
            'id': None,
        }

    def nonce(self):
        return self.milliseconds()

    def encode_params(self, params):
        if 'orders' in params:
            orders = params['orders']
            query = self.urlencode(self.keysort(self.omit(params, 'orders')))
            for i in range(0, len(orders)):
                order = orders[i]
                keys = list(order.keys())
                for k in range(0, len(keys)):
                    key = keys[k]
                    value = order[key]
                    query += '&orders%5B%5D%5B' + key + '%5D=' + str(value)
            return query
        return self.urlencode(self.keysort(params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/api' + '/' + self.version + '/' + self.implode_params(path, params)
        if 'extension' in self.urls:
            request += self.urls['extension']
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + request
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            query = self.encode_params(self.extend({
                'access_key': self.apiKey,
                'tonce': nonce,
            }, params))
            auth = method + '|' + request + '|' + query
            signature = self.hmac(self.encode(auth), self.encode(self.secret))
            suffix = query + '&signature=' + signature
            if method == 'GET':
                url += '?' + suffix
            else:
                body = suffix
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if code == 400:
            response = json.loads(body)
            error = self.safe_value(response, 'error')
            errorCode = self.safe_string(error, 'code')
            feedback = self.id + ' ' + self.json(response)
            exceptions = self.exceptions
            if errorCode in exceptions:
                raise exceptions[errorCode](feedback)
            # fallback to default error handler
