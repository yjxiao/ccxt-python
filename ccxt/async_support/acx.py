# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import json
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound


class acx (Exchange):

    def describe(self):
        return self.deep_extend(super(acx, self).describe(), {
            'id': 'acx',
            'name': 'ACX',
            'countries': ['AU'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'withdraw': True,
                'fetchOrder': True,
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

    async def fetch_markets(self):
        markets = await self.publicGetMarkets()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
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
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
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
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetMembersMe()
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

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 300
        orderbook = await self.publicGetDepth(self.extend(request, params))
        timestamp = orderbook['timestamp'] * 1000
        return self.parse_order_book(orderbook, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['at'] * 1000
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

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
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

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTickersMarket(self.extend({
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

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTrades(self.extend({
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

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500  # default is 30
        request = {
            'market': market['id'],
            'period': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['timestamp'] = since
        response = await self.publicGetK(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_order(self, order, market=None):
        symbol = None
        if market is not None:
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
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': order['ord_type'],
            'side': order['side'],
            'price': self.safe_float(order, 'price'),
            'amount': self.safe_float(order, 'volume'),
            'filled': self.safe_float(order, 'executed_volume'),
            'remaining': self.safe_float(order, 'remaining_volume'),
            'trades': None,
            'fee': None,
            'info': order,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privateGetOrder(self.extend({
            'id': int(id),
        }, params))
        return self.parse_order(response)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        order = {
            'market': self.market_id(symbol),
            'side': side,
            'volume': str(amount),
            'ord_type': type,
        }
        if type == 'limit':
            order['price'] = str(price)
        response = await self.privatePostOrders(self.extend(order, params))
        market = self.markets_by_id[response['market']]
        return self.parse_order(response, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        result = await self.privatePostOrderDelete({'id': id})
        order = self.parse_order(result)
        status = order['status']
        if status == 'closed' or status == 'canceled':
            raise OrderNotFound(self.id + ' ' + self.json(order))
        return order

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        # they have XRP but no docs on memo/tag
        request = {
            'currency': currency['id'],
            'sum': amount,
            'address': address,
        }
        result = await self.privatePostWithdraw(self.extend(request, params))
        # withdrawal response is undocumented
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
            signed = self.hmac(self.encode(auth), self.encode(self.secret))
            suffix = query + '&signature=' + signed
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
