# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound


class acx(Exchange):

    def describe(self):
        return self.deep_extend(super(acx, self).describe(), {
            'id': 'acx',
            'name': 'ACX',
            'countries': ['AU'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'cancelOrder': True,
                'CORS': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
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
            'commonCurrencies': {
                'PLA': 'Plair',
            },
            'exceptions': {
                '2002': InsufficientFunds,
                '2003': OrderNotFound,
            },
        })

    def fetch_markets(self, params={}):
        markets = self.publicGetMarkets(params)
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['id']
            symbol = market['name']
            baseId = self.safe_string(market, 'base_unit')
            quoteId = self.safe_string(market, 'quote_unit')
            if (baseId is None) or (quoteId is None):
                ids = symbol.split('/')
                baseId = ids[0].lower()
                quoteId = ids[1].lower()
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            # todo: find out their undocumented precision and limits
            precision = {
                'amount': 8,
                'price': 8,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'info': market,
                'active': None,
                'limits': self.limits,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetMembersMe(params)
        balances = self.safe_value(response, 'accounts')
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'balance')
            account['used'] = self.safe_float(balance, 'locked')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 300
        orderbook = self.publicGetDepth(self.extend(request, params))
        timestamp = self.safe_timestamp(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'at')
        ticker = ticker['ticker']
        symbol = None
        if market:
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
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTickers(params)
        ids = list(response.keys())
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
                base = self.safe_currency_code(base)
                quote = self.safe_currency_code(quote)
                symbol = base + '/' + quote
            result[symbol] = self.parse_ticker(response[id], market)
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicGetTickersMarket(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        id = self.safe_string(trade, 'tid')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'order': None,
            'takerOrMaker': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'volume'),
            'cost': self.safe_float(trade, 'funds'),
            'fee': None,
        }

    def fetch_time(self, params={}):
        response = self.publicGetTimestamp(params)
        #
        #     1594911427
        #
        return response * 1000

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        return [
            self.safe_timestamp(ohlcv, 0),
            self.safe_float(ohlcv, 1),
            self.safe_float(ohlcv, 2),
            self.safe_float(ohlcv, 3),
            self.safe_float(ohlcv, 4),
            self.safe_float(ohlcv, 5),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500  # default is 30
        request = {
            'market': market['id'],
            'period': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['timestamp'] = int(since / 1000)
        response = self.publicGetK(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'done': 'closed',
            'wait': 'open',
            'cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        marketId = self.safe_string(order, 'market')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        status = self.parse_order_status(self.safe_string(order, 'state'))
        type = self.safe_string(order, 'type')
        side = self.safe_string(order, 'side')
        id = self.safe_string(order, 'id')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': self.safe_float(order, 'price'),
            'stopPrice': None,
            'amount': self.safe_float(order, 'volume'),
            'filled': self.safe_float(order, 'executed_volume'),
            'remaining': self.safe_float(order, 'remaining_volume'),
            'trades': None,
            'fee': None,
            'info': order,
            'cost': None,
            'average': None,
        })

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': int(id),
        }
        response = self.privateGetOrder(self.extend(request, params))
        return self.parse_order(response)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'side': side,
            'volume': str(amount),
            'ord_type': type,
        }
        if type == 'limit':
            request['price'] = str(price)
        response = self.privatePostOrders(self.extend(request, params))
        marketId = self.safe_value(response, 'market')
        market = self.safe_value(self.markets_by_id, marketId)
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privatePostOrderDelete(self.extend(request, params))
        order = self.parse_order(response)
        status = order['status']
        if status == 'closed' or status == 'canceled':
            raise OrderNotFound(self.id + ' ' + self.json(order))
        return order

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        # they have XRP but no docs on memo/tag
        request = {
            'currency': currency['id'],
            'sum': amount,
            'address': address,
        }
        response = self.privatePostWithdraw(self.extend(request, params))
        # withdrawal response is undocumented
        return {
            'info': response,
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
        request = '/api/' + self.version + '/' + self.implode_params(path, params)
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
            signed = self.hmac(self.encode(auth), self.encode(self.secret))
            suffix = query + '&signature=' + signed
            if method == 'GET':
                url += '?' + suffix
            else:
                body = suffix
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if code == 400:
            error = self.safe_value(response, 'error')
            errorCode = self.safe_string(error, 'code')
            feedback = self.id + ' ' + self.json(response)
            self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
            # fallback to default error handler
