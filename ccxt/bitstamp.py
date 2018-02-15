# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported
from ccxt.base.errors import AuthenticationError


class bitstamp (Exchange):

    def describe(self):
        return self.deep_extend(super(bitstamp, self).describe(), {
            'id': 'bitstamp',
            'name': 'Bitstamp',
            'countries': 'GB',
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27786377-8c8ab57e-5fe9-11e7-8ea4-2b05b6bcceec.jpg',
                'api': 'https://www.bitstamp.net/api',
                'www': 'https://www.bitstamp.net',
                'doc': 'https://www.bitstamp.net/api',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'order_book/{pair}/',
                        'ticker_hour/{pair}/',
                        'ticker/{pair}/',
                        'transactions/{pair}/',
                        'trading-pairs-info/',
                    ],
                },
                'private': {
                    'post': [
                        'balance/',
                        'balance/{pair}/',
                        'bch_withdrawal/',
                        'bch_address/',
                        'user_transactions/',
                        'user_transactions/{pair}/',
                        'open_orders/all/',
                        'open_orders/{pair}/',
                        'order_status/',
                        'cancel_order/',
                        'buy/{pair}/',
                        'buy/market/{pair}/',
                        'sell/{pair}/',
                        'sell/market/{pair}/',
                        'ltc_withdrawal/',
                        'ltc_address/',
                        'eth_withdrawal/',
                        'eth_address/',
                        'xrp_withdrawal/',
                        'xrp_address/',
                        'transfer-to-main/',
                        'transfer-from-main/',
                        'withdrawal/open/',
                        'withdrawal/status/',
                        'withdrawal/cancel/',
                        'liquidation_address/new/',
                        'liquidation_address/info/',
                    ],
                },
                'v1': {
                    'post': [
                        'bitcoin_deposit_address/',
                        'unconfirmed_btc/',
                        'bitcoin_withdrawal/',
                        'ripple_withdrawal/',
                        'ripple_address/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                    'tiers': {
                        'taker': [
                            [0, 0.25 / 100],
                            [20000, 0.24 / 100],
                            [100000, 0.22 / 100],
                            [400000, 0.20 / 100],
                            [600000, 0.15 / 100],
                            [1000000, 0.14 / 100],
                            [2000000, 0.13 / 100],
                            [4000000, 0.12 / 100],
                            [20000000, 0.11 / 100],
                            [20000001, 0.10 / 100],
                        ],
                        'maker': [
                            [0, 0.25 / 100],
                            [20000, 0.24 / 100],
                            [100000, 0.22 / 100],
                            [400000, 0.20 / 100],
                            [600000, 0.15 / 100],
                            [1000000, 0.14 / 100],
                            [2000000, 0.13 / 100],
                            [4000000, 0.12 / 100],
                            [20000000, 0.11 / 100],
                            [20000001, 0.10 / 100],
                        ],
                    },
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0,
                        'BCH': 0,
                        'LTC': 0,
                        'ETH': 0,
                        'XRP': 0,
                        'USD': 25,
                        'EUR': 0.90,
                    },
                    'deposit': {
                        'BTC': 0,
                        'BCH': 0,
                        'LTC': 0,
                        'ETH': 0,
                        'XRP': 0,
                        'USD': 25,
                        'EUR': 0,
                    },
                },
            },
        })

    def fetch_markets(self):
        markets = self.publicGetTradingPairsInfo()
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            symbol = market['name']
            base, quote = symbol.split('/')
            baseId = base.lower()
            quoteId = quote.lower()
            symbolId = baseId + '_' + quoteId
            id = market['url_symbol']
            precision = {
                'amount': market['base_decimals'],
                'price': market['counter_decimals'],
            }
            parts = market['minimum_order'].split(' ')
            cost = parts[0]
            # cost, currency = market['minimum_order'].split(' ')
            active = (market['trading'] == 'Enabled')
            lot = math.pow(10, -precision['amount'])
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'symbolId': symbolId,
                'info': market,
                'lot': lot,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': lot,
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': float(cost),
                        'max': None,
                    },
                },
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetOrderBookPair(self.extend({
            'pair': self.market_id(symbol),
        }, params))
        timestamp = int(orderbook['timestamp']) * 1000
        return self.parse_order_book(orderbook, timestamp)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        ticker = self.publicGetTickerPair(self.extend({
            'pair': self.market_id(symbol),
        }, params))
        timestamp = int(ticker['timestamp']) * 1000
        vwap = float(ticker['vwap'])
        baseVolume = float(ticker['volume'])
        quoteVolume = baseVolume * vwap
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']),
            'low': float(ticker['low']),
            'bid': float(ticker['bid']),
            'ask': float(ticker['ask']),
            'vwap': vwap,
            'open': float(ticker['open']),
            'close': None,
            'first': None,
            'last': float(ticker['last']),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def get_market_from_trade(self, trade):
        trade = self.omit(trade, [
            'fee',
            'price',
            'datetime',
            'tid',
            'type',
            'order_id',
        ])
        currencyIds = list(trade.keys())
        numCurrencyIds = len(currencyIds)
        if numCurrencyIds == 2:
            marketId = currencyIds[0] + currencyIds[1]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
            marketId = currencyIds[1] + currencyIds[0]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
        return None

    def get_market_from_trades(self, trades):
        tradesBySymbol = self.index_by(trades, 'symbol')
        symbols = list(tradesBySymbol.keys())
        numSymbols = len(symbols)
        if numSymbols == 1:
            return self.markets[symbols[0]]
        return None

    def parse_trade(self, trade, market=None):
        timestamp = None
        symbol = None
        if 'date' in trade:
            timestamp = int(trade['date']) * 1000
        elif 'datetime' in trade:
            timestamp = self.parse8601(trade['datetime'])
        # only if overrided externally
        side = self.safe_string(trade, 'side')
        orderId = self.safe_string(trade, 'order_id')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        id = self.safe_string(trade, 'tid')
        id = self.safe_string(trade, 'id', id)
        if market is None:
            keys = list(trade.keys())
            for i in range(0, len(keys)):
                if keys[i].find('_') >= 0:
                    marketId = keys[i].replace('_', '')
                    if marketId in self.markets_by_id:
                        market = self.markets_by_id[marketId]
            # if the market is still not defined
            # try to deduce it from used keys
            if market is None:
                market = self.get_market_from_trade(trade)
        feeCost = self.safe_float(trade, 'fee')
        feeCurrency = None
        if market is not None:
            price = self.safe_float(trade, market['symbolId'], price)
            amount = self.safe_float(trade, market['baseId'], amount)
            feeCurrency = market['quote']
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'fee': {
                'cost': feeCost,
                'currency': feeCurrency,
            },
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTransactionsPair(self.extend({
            'pair': market['id'],
            'time': 'minute',
        }, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        balance = self.privatePostBalance()
        result = {'info': balance}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            lowercase = currency.lower()
            total = lowercase + '_balance'
            free = lowercase + '_available'
            used = lowercase + '_reserved'
            account = self.account()
            if free in balance:
                account['free'] = float(balance[free])
            if used in balance:
                account['used'] = float(balance[used])
            if total in balance:
                account['total'] = float(balance[total])
            result[currency] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        order = {
            'pair': self.market_id(symbol),
            'amount': amount,
        }
        if type == 'market':
            method += 'Market'
        else:
            order['price'] = price
        method += 'Pair'
        response = getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': response['id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privatePostCancelOrder({'id': id})

    def parse_order_status(self, order):
        if (order['status'] == 'Queue') or (order['status'] == 'Open'):
            return 'open'
        if order['status'] == 'Finished':
            return 'closed'
        return order['status']

    def fetch_order_status(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privatePostOrderStatus(self.extend({'id': id}, params))
        return self.parse_order_status(response)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostOrderStatus(self.extend({'id': id}, params))
        return self.parse_order(response, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        method = 'privatePostUserTransactions'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
            method += 'Pair'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = None
        iso8601 = None
        datetimeString = self.safe_string(order, 'datetime')
        if datetimeString is not None:
            timestamp = self.parse8601(datetimeString)
            iso8601 = self.iso8601(timestamp)
        symbol = None
        if market is None:
            if 'currency_pair' in order:
                marketId = order['currency_pair']
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        amount = self.safe_float(order, 'amount')
        filled = 0
        trades = []
        transactions = self.safe_value(order, 'transactions')
        if transactions is not None:
            if isinstance(transactions, list):
                for i in range(0, len(transactions)):
                    trade = self.parse_trade(self.extend({'order_id': id}, transactions[i]), market)
                    filled += trade['amount']
                    trades.append(trade)
        status = self.safe_string(order, 'status')
        if (status == 'In Queue') or (status == 'Open'):
            status = 'open'
        elif status == 'Finished':
            status = 'closed'
            if amount is None:
                amount = filled
        remaining = None
        if amount is not None:
            remaining = amount - filled
        price = self.safe_float(order, 'price')
        side = self.safe_string(order, 'type')
        if side is not None:
            side = 'sell' if (side == '1') else 'buy'
        fee = None
        cost = None
        if market is None:
            market = self.get_market_from_trades(trades)
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'datetime': iso8601,
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': fee,
            'info': order,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        market = None
        if symbol is not None:
            self.load_markets()
            market = self.market(symbol)
        orders = self.privatePostOpenOrdersAll()
        return self.parse_orders(orders, market, since, limit)

    def get_currency_name(self, code):
        if code == 'BTC':
            return 'bitcoin'
        return code.lower()

    def is_fiat(self, code):
        if code == 'USD':
            return True
        if code == 'EUR':
            return True
        return False

    def withdraw(self, code, amount, address, tag=None, params={}):
        isFiat = self.is_fiat(code)
        if isFiat:
            raise NotSupported(self.id + ' fiat withdraw() for ' + code + ' is not implemented yet')
        name = self.get_currency_name(code)
        request = {
            'amount': amount,
            'address': address,
        }
        v1 = (code == 'BTC')
        method = 'v1' if v1 else 'private'  # v1 or v2
        method += 'Post' + self.capitalize(name) + 'Withdrawal'
        query = params
        if code == 'XRP':
            if tag is not None:
                request['destination_tag'] = tag
                query = self.omit(params, 'destination_tag')
            else:
                raise ExchangeError(self.id + ' withdraw() requires a destination_tag param for ' + code)
        response = getattr(self, method)(self.extend(request, query))
        return {
            'info': response,
            'id': response['id'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if api != 'v1':
            url += self.version + '/'
        url += self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + self.uid + self.apiKey
            signature = self.encode(self.hmac(self.encode(auth), self.encode(self.secret)))
            query = self.extend({
                'key': self.apiKey,
                'signature': signature.upper(),
                'nonce': nonce,
            }, query)
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            status = self.safe_string(response, 'status')
            if status == 'error':
                code = self.safe_string(response, 'code')
                if code is not None:
                    if code == 'API0005':
                        raise AuthenticationError(self.id + ' invalid signature, use the uid for the main account if you have subaccounts')
                raise ExchangeError(self.id + ' ' + self.json(response))
