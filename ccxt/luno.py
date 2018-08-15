# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
from ccxt.base.errors import ExchangeError


class luno (Exchange):

    def describe(self):
        return self.deep_extend(super(luno, self).describe(), {
            'id': 'luno',
            'name': 'luno',
            'countries': ['GB', 'SG', 'ZA'],
            'rateLimit': 10000,
            'version': '1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchTradingFees': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766607-8c1a69d8-5ede-11e7-930c-540b5eb9be24.jpg',
                'api': 'https://api.mybitx.com/api',
                'www': 'https://www.luno.com',
                'doc': [
                    'https://www.luno.com/en/api',
                    'https://npmjs.org/package/bitx',
                    'https://github.com/bausmeier/node-bitx',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'orderbook',
                        'orderbook_top',
                        'ticker',
                        'tickers',
                        'trades',
                    ],
                },
                'private': {
                    'get': [
                        'accounts/{id}/pending',
                        'accounts/{id}/transactions',
                        'balance',
                        'fee_info',
                        'funding_address',
                        'listorders',
                        'listtrades',
                        'orders/{id}',
                        'quotes/{id}',
                        'withdrawals',
                        'withdrawals/{id}',
                    ],
                    'post': [
                        'accounts',
                        'postorder',
                        'marketorder',
                        'stoporder',
                        'funding_address',
                        'withdrawals',
                        'send',
                        'quotes',
                        'oauth2/grant',
                    ],
                    'put': [
                        'quotes/{id}',
                    ],
                    'delete': [
                        'quotes/{id}',
                        'withdrawals/{id}',
                    ],
                },
            },
        })

    def fetch_markets(self):
        markets = self.publicGetTickers()
        result = []
        for p in range(0, len(markets['tickers'])):
            market = markets['tickers'][p]
            id = market['pair']
            base = id[0:3]
            quote = id[3:6]
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
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
        response = self.privateGetBalance()
        wallets = response['balance']
        result = {'info': response}
        for b in range(0, len(wallets)):
            wallet = wallets[b]
            currency = self.common_currency_code(wallet['asset'])
            reserved = float(wallet['reserved'])
            unconfirmed = float(wallet['unconfirmed'])
            balance = float(wallet['balance'])
            account = {
                'free': 0.0,
                'used': self.sum(reserved, unconfirmed),
                'total': self.sum(balance, unconfirmed),
            }
            account['free'] = account['total'] - account['used']
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        method = 'publicGetOrderbook'
        if limit is not None:
            if limit <= 100:
                method += 'Top'  # get just the top of the orderbook when limit is low
        orderbook = getattr(self, method)(self.extend({
            'pair': self.market_id(symbol),
        }, params))
        timestamp = orderbook['timestamp']
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'volume')

    def parse_order(self, order, market=None):
        timestamp = order['creation_timestamp']
        status = 'open' if (order['state'] == 'PENDING') else 'closed'
        side = 'sell' if (order['type'] == 'ASK') else 'buy'
        if market is None:
            market = self.find_market(order['pair'])
        symbol = market['symbol']
        price = self.safe_float(order, 'limit_price')
        amount = self.safe_float(order, 'limit_volume')
        quoteFee = self.safe_float(order, 'fee_counter')
        baseFee = self.safe_float(order, 'fee_base')
        filled = self.safe_float(order, 'base')
        cost = self.safe_float(order, 'counter')
        remaining = None
        if amount is not None:
            if filled is not None:
                remaining = max(0, amount - filled)
        fee = {'currency': None}
        if quoteFee:
            fee['side'] = 'quote'
            fee['cost'] = quoteFee
        else:
            fee['side'] = 'base'
            fee['cost'] = baseFee
        return {
            'id': order['order_id'],
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': filled,
            'cost': cost,
            'remaining': remaining,
            'trades': None,
            'fee': fee,
            'info': order,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetOrdersId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response)

    def fetch_orders_by_state(self, state=None, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if state is not None:
            request['state'] = state
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = self.privateGetListorders(self.extend(request, params))
        orders = self.safe_value(response, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_state(None, symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_state('PENDING', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_state('COMPLETE', symbol, since, limit, params)

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['timestamp']
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last_trade')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'rolling_24_hour_volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTickers(params)
        tickers = self.index_by(response['tickers'], 'pair')
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetTicker(self.extend({
            'pair': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        side = 'buy' if (trade['is_buy']) else 'sell'
        return {
            'info': trade,
            'id': None,
            'order': None,
            'timestamp': trade['timestamp'],
            'datetime': self.iso8601(trade['timestamp']),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'volume'),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if since is not None:
            request['since'] = since
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def fetch_trading_fees(self, params={}):
        self.load_markets()
        response = self.privateGetFeeInfo(params)
        return {
            'info': response,
            'maker': self.safe_float(response, 'maker_fee'),
            'taker': self.safe_float(response, 'taker_fee'),
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        method = 'privatePost'
        order = {'pair': self.market_id(symbol)}
        if type == 'market':
            method += 'Marketorder'
            order['type'] = side.upper()
            if side == 'buy':
                order['counter_volume'] = amount
            else:
                order['base_volume'] = amount
        else:
            method += 'Postorder'
            order['volume'] = amount
            order['price'] = price
            if side == 'buy':
                order['type'] = 'BID'
            else:
                order['type'] = 'ASK'
        response = getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': response['order_id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privatePostStoporder({'order_id': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if query:
            url += '?' + self.urlencode(query)
        if api == 'private':
            self.check_required_credentials()
            auth = self.encode(self.apiKey + ':' + self.secret)
            auth = base64.b64encode(auth)
            headers = {'Authorization': 'Basic ' + self.decode(auth)}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'error' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
