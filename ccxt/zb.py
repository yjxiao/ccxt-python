# -*- coding: utf-8 -*-

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError


class zb (Exchange):

    def describe(self):
        return self.deep_extend(super(zb, self).describe(), {
            'id': 'zb',
            'name': 'ZB',
            'countries': 'CN',
            'rateLimit': 1000,
            'version': 'v1',
            'hasCORS': False,
            # old metainfo interface
            'hasFetchOrder': True,
            'hasFetchTickers': True,
            'hasWithdraw': True,
            'hasFetchOHLCV': True,
            # new metainfo interface
            'has': {
                'CORS': False,
                'fetchOHLCV': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': '1day',
                '3d': '3day',
                '1w': '1week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/32859187-cd5214f0-ca5e-11e7-967d-96568e2e2bd1.jpg',
                'api': {
                    'public': 'http://api.zb.com/data',  # no https for public API
                    'private': 'https://trade.zb.com/api',
                },
                'www': 'https://trade.zb.com/api',
                'doc': 'https://www.zb.com/i/developer',
                'fees': 'https://www.zb.com/i/rate',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'ticker',
                        'depth',
                        'trades',
                        'kline',
                    ],
                },
                'private': {
                    'post': [
                        'order',
                        'cancelOrder',
                        'getOrder',
                        'getOrders',
                        'getOrdersNew',
                        'getOrdersIgnoreTradeType',
                        'getUnfinishedOrdersIgnoreTradeType',
                        'getAccountInfo',
                        'getUserAddress',
                        'getWithdrawAddress',
                        'getWithdrawRecord',
                        'getChargeRecord',
                        'getCnyWithdrawRecord',
                        'getCnyChargeRecord',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'BTC': 0.0001,
                        'BCH': 0.0006,
                        'LTC': 0.005,
                        'ETH': 0.01,
                        'ETC': 0.01,
                        'BTS': 3,
                        'EOS': 1,
                        'QTUM': 0.01,
                        'HSR': 0.001,
                        'XRP': 0.1,
                        'USDT': '0.1%',
                        'QCASH': 5,
                        'DASH': 0.002,
                        'BCD': 0,
                        'UBTC': 0,
                        'SBTC': 0,
                        'INK': 20,
                        'TV': 0.1,
                        'BTH': 0,
                        'BCX': 0,
                        'LBTC': 0,
                        'CHAT': 20,
                        'bitCNY': 20,
                        'HLC': 20,
                        'BTP': 0,
                        'BCW': 0,
                    },
                },
                'trading': {
                },
            },
        })

    def get_trading_fee_from_base_quote(self, base, quote):
        # base: quote
        fees = {
            'BTC': {'USDT': 0.0},
            'BCH': {'BTC': 0.001, 'USDT': 0.001},
            'LTC': {'BTC': 0.001, 'USDT': 0.0},
            'ETH': {'BTC': 0.001, 'USDT': 0.0},
            'ETC': {'BTC': 0.001, 'USDT': 0.0},
            'BTS': {'BTC': 0.001, 'USDT': 0.001},
            'EOS': {'BTC': 0.001, 'USDT': 0.001},
            'HSR': {'BTC': 0.001, 'USDT': 0.001},
            'QTUM': {'BTC': 0.001, 'USDT': 0.001},
            'USDT': {'BTC': 0.0},
        }
        if base in fees:
            quoteFees = fees[base]
            if quote in quoteFees:
                return quoteFees[quote]
        return None

    def fetch_markets(self):
        markets = self.publicGetMarkets()
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            fee = self.get_trading_fee_from_base_quote(base, quote)
            precision = {
                'amount': market['amountScale'],
                'price': market['priceScale'],
            }
            lot = math.pow(10, -precision['amount'])
            result.append({
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'info': market,
                'maker': fee,
                'taker': fee,
                'lot': lot,
                'active': True,
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
                        'min': 0,
                        'max': None,
                    },
                },
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetAccountInfo()
        balances = response['result']['coins']
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = balance['key']
            if currency in self.currencies:
                currency = self.currencies[currency]['code']
            account = self.account()
            account['free'] = float(balance['available'])
            account['used'] = float(balance['freez'])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def get_market_field_name(self):
        return 'market'

    def fetch_order_book(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        orderbook = self.publicGetDepth(self.extend(request, params))
        timestamp = self.milliseconds()
        bids = None
        asks = None
        if 'bids' in orderbook:
            bids = orderbook['bids']
        if 'asks' in orderbook:
            asks = orderbook['asks']
        result = {
            'bids': bids,
            'asks': asks,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        if result['bids']:
            result['bids'] = self.sort_by(result['bids'], 0, True)
        if result['asks']:
            result['asks'] = self.sort_by(result['asks'], 0)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = self.publicGetTicker(self.extend(request, params))
        ticker = response['ticker']
        timestamp = self.milliseconds()
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']),
            'low': float(ticker['low']),
            'bid': float(ticker['buy']),
            'ask': float(ticker['sell']),
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': float(ticker['last']),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': float(ticker['vol']),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [ohlcv[0],
                ohlcv[1],
                ohlcv[2],
                ohlcv[3],
                ohlcv[4],
                ohlcv[5]]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'type': self.timeframes[timeframe],
        }
        request['limit'] = limit if (limit) else 1000  # default == max ==  1000

        # Set since = 0 to traverse records from the beginning.
        if not (since is None) and (since >= 0):
            # The length of the 'since' parameter
            # passed to the API must be exactly 13 bytes.
            str_since = str(since)
            if len(str_since) < 13:
                str_since = "{0}{1}".format("0" * (13 - len(str_since)), str_since)
            request['since'] = str_since
        response = self.publicGetKline(self.extend(request, params))
        return self.parse_ohlcvs(response["data"], market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = trade['date'] * 1000
        side = 'buy' if (trade['trade_type'] == 'bid') else 'sell'
        return {
            'info': trade,
            'id': str(trade['tid']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': float(trade['price']),
            'amount': float(trade['amount']),
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        paramString = '&price=' + str(price)
        paramString += '&amount=' + str(amount)
        tradeType = '1' if (side == 'buy') else '0'
        paramString += '&tradeType=' + tradeType
        paramString += '&currency=' + self.market_id(symbol)
        response = self.privatePostOrder(paramString)
        return {
            'info': response,
            'id': response['id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        paramString = '&id=' + str(id)
        if 'currency' in params:
            paramString += '&currency=' + params['currency']
        return self.privatePostCancelOrder(paramString)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        paramString = '&id=' + str(id)
        if 'currency' in params:
            paramString += '&currency=' + params['currency']
        return self.privatePostGetOrder(paramString)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.version + '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            auth = 'accesskey=' + self.apiKey
            auth += '&' + 'method=' + path
            secret = self.hash(self.encode(self.secret), 'sha1')
            signature = self.hmac(self.encode(auth), self.encode(secret), hashlib.md5)
            suffix = 'sign=' + signature + '&reqTime=' + str(nonce)
            url += '/' + path + '?' + auth + '&' + suffix
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            # {"result":false,"message":}
            if 'result' in response:
                success = self.safe_value(response, 'result', False)
                if isinstance(success, basestring):
                    if (success == 'true') or (success == '1'):
                        success = True
                    else:
                        success = False
                if not success:
                    raise ExchangeError(self.id + ' ' + self.json(response))

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'private':
            if 'code' in response:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
