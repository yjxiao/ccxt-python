# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class itbit (Exchange):

    def describe(self):
        return self.deep_extend(super(itbit, self).describe(), {
            'id': 'itbit',
            'name': 'itBit',
            'countries': 'US',
            'rateLimit': 2000,
            'version': 'v1',
            'has': {
                'CORS': True,
                'createMarketOrder': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27822159-66153620-60ad-11e7-89e7-005f6d7f3de0.jpg',
                'api': 'https://api.itbit.com',
                'www': 'https://www.itbit.com',
                'doc': [
                    'https://api.itbit.com/docs',
                    'https://www.itbit.com/api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'markets/{symbol}/ticker',
                        'markets/{symbol}/order_book',
                        'markets/{symbol}/trades',
                    ],
                },
                'private': {
                    'get': [
                        'wallets',
                        'wallets/{walletId}',
                        'wallets/{walletId}/balances/{currencyCode}',
                        'wallets/{walletId}/funding_history',
                        'wallets/{walletId}/trades',
                        'wallets/{walletId}/orders',
                        'wallets/{walletId}/orders/{id}',
                    ],
                    'post': [
                        'wallet_transfers',
                        'wallets',
                        'wallets/{walletId}/cryptocurrency_deposits',
                        'wallets/{walletId}/cryptocurrency_withdrawals',
                        'wallets/{walletId}/orders',
                        'wire_withdrawal',
                    ],
                    'delete': [
                        'wallets/{walletId}/orders/{id}',
                    ],
                },
            },
            'markets': {
                'BTC/USD': {'id': 'XBTUSD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD'},
                'BTC/SGD': {'id': 'XBTSGD', 'symbol': 'BTC/SGD', 'base': 'BTC', 'quote': 'SGD'},
                'BTC/EUR': {'id': 'XBTEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR'},
            },
            'fees': {
                'trading': {
                    'maker': 0,
                    'taker': 0.2 / 100,
                },
            },
        })

    def fetch_order_book(self, symbol, limit=None, params={}):
        orderbook = self.publicGetMarketsSymbolOrderBook(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        ticker = self.publicGetMarketsSymbolTicker(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        serverTimeUTC = ('serverTimeUTC' in list(ticker.keys()))
        if not serverTimeUTC:
            raise ExchangeError(self.id + ' fetchTicker returned a bad response: ' + self.json(ticker))
        timestamp = self.parse8601(ticker['serverTimeUTC'])
        vwap = self.safe_float(ticker, 'vwap24h')
        baseVolume = self.safe_float(ticker, 'volume24h')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24h'),
            'low': self.safe_float(ticker, 'low24h'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_float(ticker, 'openToday'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = self.parse8601(trade['timestamp'])
        id = str(trade['matchNumber'])
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': id,
            'order': id,
            'type': None,
            'side': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetMarketsSymbolTrades(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_trades(response['recentTrades'], market, since, limit)

    def fetch_balance(self, params={}):
        response = self.fetch_wallets()
        balances = response[0]['balances']
        result = {'info': response}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            account = {
                'free': float(balance['availableBalance']),
                'used': 0.0,
                'total': float(balance['totalBalance']),
            }
            account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    def fetch_wallets(self, params={}):
        if not self.userId:
            raise AuthenticationError(self.id + ' fetchWallets requires userId in API settings')
        request = {
            'userId': self.userId,
        }
        return self.privateGetWallets(self.extend(request, params))

    def fetch_wallet(self, walletId, params={}):
        wallet = {
            'walletId': walletId,
        }
        return self.privateGetWalletsWalletId(self.extend(wallet, params))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders(symbol, since, limit, self.extend({
            'status': 'open',
        }, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders(symbol, since, limit, self.extend({
            'status': 'filled',
        }, params))

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        walletIdInParams = ('walletId' in list(params.keys()))
        if not walletIdInParams:
            raise ExchangeError(self.id + ' fetchOrders requires a walletId parameter')
        walletId = params['walletId']
        response = self.privateGetWalletsWalletIdOrders(self.extend({
            'walletId': walletId,
        }, params))
        orders = self.parse_orders(response, None, since, limit)
        return orders

    def parse_order(self, order, market=None):
        side = order['side']
        type = order['type']
        symbol = self.markets_by_id[order['instrument']]['symbol']
        timestamp = self.parse8601(order['createdTime'])
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'amountFilled')
        remaining = amount - filled
        fee = None
        price = self.safe_float(order, 'price')
        cost = price * self.safe_float(order, 'volumeWeightedAveragePrice')
        return {
            'id': order['id'],
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': order['status'],
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
            # 'trades': self.parse_trades(order['trades'], market),
        }

    def nonce(self):
        return self.milliseconds()

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        walletIdInParams = ('walletId' in list(params.keys()))
        if not walletIdInParams:
            raise ExchangeError(self.id + ' createOrder requires a walletId parameter')
        amount = str(amount)
        price = str(price)
        market = self.market(symbol)
        order = {
            'side': side,
            'type': type,
            'currency': market['id'].replace(market['quote'], ''),
            'amount': amount,
            'display': amount,
            'price': price,
            'instrument': market['id'],
        }
        response = self.privatePostWalletsWalletIdOrders(self.extend(order, params))
        return {
            'info': response,
            'id': response['id'],
        }

    def fetch_order(self, id, symbol=None, params={}):
        walletIdInParams = ('walletId' in list(params.keys()))
        if not walletIdInParams:
            raise ExchangeError(self.id + ' fetchOrder requires a walletId parameter')
        return self.privateGetWalletsWalletIdOrdersId(self.extend({
            'id': id,
        }, params))

    def cancel_order(self, id, symbol=None, params={}):
        walletIdInParams = ('walletId' in list(params.keys()))
        if not walletIdInParams:
            raise ExchangeError(self.id + ' cancelOrder requires a walletId parameter')
        return self.privateDeleteWalletsWalletIdOrdersId(self.extend({
            'id': id,
        }, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET' and query:
            url += '?' + self.urlencode(query)
        if method == 'POST' and query:
            body = self.json(query)
        else:
            body = ''
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            timestamp = nonce
            auth = [method, url, body, nonce, timestamp]
            message = nonce + self.json(auth).replace('\\/', '/')
            hash = self.hash(self.encode(message), 'sha256', 'binary')
            binhash = self.binary_concat(url, hash)
            signature = self.hmac(binhash, self.encode(self.secret), hashlib.sha512, 'base64')
            headers = {
                'Authorization': self.apiKey + ':' + signature,
                'Content-Type': 'application/json',
                'X-Auth-Timestamp': timestamp,
                'X-Auth-Nonce': nonce,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'code' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
