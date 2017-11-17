# -*- coding: utf-8 -*-

from ccxt.hitbtc import hitbtc
import base64
from ccxt.base.errors import ExchangeError


class hitbtc2 (hitbtc):

    def describe(self):
        return self.deep_extend(super(hitbtc2, self).describe(), {
            'id': 'hitbtc2',
            'name': 'HitBTC v2',
            'countries': 'HK',  # Hong Kong
            'rateLimit': 1500,
            'version': '2',
            'hasCORS': True,
            # older metainfo interface
            'hasFetchOHLCV': True,
            'hasFetchTickers': True,
            'hasFetchOrder': True,
            'hasFetchOrders': False,
            'hasFetchOpenOrders': True,
            'hasFetchClosedOrders': True,
            'hasWithdraw': True,
            # new metainfo interface
            'has': {
                'fetchOHLCV': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': 'M1',
                '3m': 'M3',
                '5m': 'M5',
                '15m': 'M15',
                '30m': 'M30',  # default
                '1h': 'H1',
                '4h': 'H4',
                '1d': 'D1',
                '1w': 'D7',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766555-8eaec20e-5edc-11e7-9c5b-6dc69fc42f5e.jpg',
                'api': 'https://api.hitbtc.com',
                'www': 'https://hitbtc.com',
                'doc': 'https://api.hitbtc.com',
            },
            'api': {
                'public': {
                    'get': [
                        'symbol',  # Available Currency Symbols
                        'symbol/{symbol}',  # Get symbol info
                        'currency',  # Available Currencies
                        'currency/{currency}',  # Get currency info
                        'ticker',  # Ticker list for all symbols
                        'ticker/{symbol}',  # Ticker for symbol
                        'trades/{symbol}',  # Trades
                        'orderbook/{symbol}',  # Orderbook
                        'candles/{symbol}',  # Candles
                    ],
                },
                'private': {
                    'get': [
                        'order',  # List your current open orders
                        'order/{clientOrderId}',  # Get a single order by clientOrderId
                        'trading/balance',  # Get trading balance
                        'trading/fee/{symbol}',  # Get trading fee rate
                        'history/trades',  # Get historical trades
                        'history/order',  # Get historical orders
                        'history/order/{id}/trades',  # Get historical trades by specified order
                        'account/balance',  # Get main acccount balance
                        'account/transactions',  # Get account transactions
                        'account/transactions/{id}',  # Get account transaction by id
                        'account/crypto/address/{currency}',  # Get deposit crypro address
                    ],
                    'post': [
                        'order',  # Create new order
                        'account/crypto/withdraw',  # Withdraw crypro
                        'account/crypto/address/{currency}',  # Create new deposit crypro address
                        'account/transfer',  # Transfer amount to trading
                    ],
                    'put': [
                        'order/{clientOrderId}',  # Create new order
                        'account/crypto/withdraw/{id}',  # Commit withdraw crypro
                    ],
                    'delete': [
                        'order',  # Cancel all open orders
                        'order/{clientOrderId}',  # Cancel order
                        'account/crypto/withdraw/{id}',  # Rollback withdraw crypro
                    ],
                    'patch': [
                        'order/{clientOrderId}',  # Cancel Replace order
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': -0.01 / 100,
                    'taker': 0.1 / 100,
                },
            },
        })

    def common_currency_code(self, currency):
        if currency == 'XBT':
            return 'BTC'
        if currency == 'DRK':
            return 'DASH'
        if currency == 'CAT':
            return 'BitClave'
        return currency

    def fetch_markets(self):
        markets = self.publicGetSymbol()
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['id']
            base = market['baseCurrency']
            quote = market['quoteCurrency']
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            lot = float(market['quantityIncrement'])
            step = float(market['tickSize'])
            precision = {
                'price': self.precision_from_string(market['tickSize']),
                'amount': self.precision_from_string(market['quantityIncrement']),
            }
            result.append(self.extend(self.fees['trading'], {
                'info': market,
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'lot': lot,
                'step': step,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': lot,
                        'max': None,
                    },
                    'price': {
                        'min': step,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            }))
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        type = self.safe_string(params, 'type', 'trading')
        method = 'privateGet' + self.capitalize(type) + 'Balance'
        balances = getattr(self, method)()
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            code = balance['currency']
            currency = self.common_currency_code(code)
            account = {
                'free': float(balance['available']),
                'used': float(balance['reserved']),
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['timestamp'])
        return [
            timestamp,
            float(ohlcv['open']),
            float(ohlcv['max']),
            float(ohlcv['min']),
            float(ohlcv['close']),
            float(ohlcv['volumeQuote']),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        if limit:
            request['limit'] = limit
        response = self.publicGetCandlesSymbol(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_order_book(self, symbol, params={}):
        self.load_markets()
        orderbook = self.publicGetOrderbookSymbol(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook, None, 'bid', 'ask', 'price', 'size')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.parse8601(ticker['timestamp'])
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'ask': self.safe_float(ticker, 'ask'),
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': self.safe_float(ticker, 'close'),
            'first': None,
            'last': self.safe_float(ticker, 'last'),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'volumeQuote'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTicker(params)
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker['symbol']
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetTickerSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        if 'message' in ticker:
            raise ExchangeError(self.id + ' ' + ticker['message'])
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['timestamp'])
        return {
            'info': trade,
            'id': str(trade['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['side'],
            'price': float(trade['price']),
            'amount': float(trade['quantity']),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTradesSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_trades(response, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        clientOrderId = self.milliseconds()
        amount = float(amount)
        order = {
            'clientOrderId': str(clientOrderId),
            'symbol': market['id'],
            'side': side,
            'quantity': self.amount_to_precision(symbol, amount),
            'type': type,
        }
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        else:
            order['timeInForce'] = 'FOK'
        response = self.privatePostOrder(self.extend(order, params))
        return {
            'info': response,
            'id': response['clientOrderId'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privateDeleteOrderClientOrderId(self.extend({
            'clientOrderId': id,
        }, params))

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(order['updatedAt'])
        if not market:
            market = self.markets_by_id[order['symbol']]
        symbol = market['symbol']
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'cumQuantity')
        status = order['status']
        if status == 'new':
            status = 'open'
        elif status == 'suspended':
            status = 'open'
        elif status == 'partiallyFilled':
            status = 'open'
        elif status == 'filled':
            status = 'closed'
        remaining = None
        if amount and filled:
            remaining = amount - filled
        return {
            'id': str(order['clientOrderId']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'status': order['status'],
            'symbol': symbol,
            'type': order['type'],
            'side': order['side'],
            'price': self.safe_float(order, 'price'),
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
            'info': order,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetOrder(self.extend({
            'client_order_id': id,
        }, params))
        return self.parse_order(response['orders'][0])

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol:
            market = self.market(symbol)
            request['symbol'] = market['symbol']
        response = self.privateGetOrder(self.extend(request, params))
        return self.parse_orders(response, market)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if limit:
            request['limit'] = limit
        if since:
            request['from'] = self.iso8601(since)
        response = self.privateGetHistoryOrder(self.extend(request, params))
        return self.parse_orders(response, market)

    def withdraw(self, currency, amount, address, params={}):
        self.load_markets()
        amount = float(amount)
        response = self.privatePostAccountCryptoWithdraw(self.extend({
            'currency': currency,
            'amount': str(amount),
            'address': address,
        }, params))
        return {
            'info': response,
            'id': response['id'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/api' + '/' + self.version + '/'
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            url += api + '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            url += self.implode_params(path, params)
            if method != 'GET':
                if query:
                    body = self.json(query)
            payload = self.encode(self.apiKey + ':' + self.secret)
            auth = base64.b64encode(payload)
            headers = {
                'Authorization': "Basic " + self.decode(auth),
                'Content-Type': 'application/json',
            }
        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'error' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
