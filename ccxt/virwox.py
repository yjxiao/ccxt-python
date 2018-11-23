# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import json
from ccxt.base.errors import ExchangeError


class virwox (Exchange):

    def describe(self):
        return self.deep_extend(super(virwox, self).describe(), {
            'id': 'virwox',
            'name': 'VirWoX',
            'countries': ['AT', 'EU'],
            'rateLimit': 1000,
            'has': {
                'CORS': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766894-6da9d360-5eea-11e7-90aa-41f2711b7405.jpg',
                'api': {
                    'public': 'http://api.virwox.com/api/json.php',
                    'private': 'https://www.virwox.com/api/trading.php',
                },
                'www': 'https://www.virwox.com',
                'doc': 'https://www.virwox.com/developers.php',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
                'login': True,
                'password': True,
            },
            'api': {
                'public': {
                    'get': [
                        'getInstruments',
                        'getBestPrices',
                        'getMarketDepth',
                        'estimateMarketOrder',
                        'getTradedPriceVolume',
                        'getRawTradeData',
                        'getStatistics',
                        'getTerminalList',
                        'getGridList',
                        'getGridStatistics',
                    ],
                    'post': [
                        'getInstruments',
                        'getBestPrices',
                        'getMarketDepth',
                        'estimateMarketOrder',
                        'getTradedPriceVolume',
                        'getRawTradeData',
                        'getStatistics',
                        'getTerminalList',
                        'getGridList',
                        'getGridStatistics',
                    ],
                },
                'private': {
                    'get': [
                        'cancelOrder',
                        'getBalances',
                        'getCommissionDiscount',
                        'getOrders',
                        'getTransactions',
                        'placeOrder',
                    ],
                    'post': [
                        'cancelOrder',
                        'getBalances',
                        'getCommissionDiscount',
                        'getOrders',
                        'getTransactions',
                        'placeOrder',
                    ],
                },
            },
        })

    def fetch_markets(self, params={}):
        markets = self.publicGetGetInstruments()
        keys = list(markets['result'].keys())
        result = []
        for p in range(0, len(keys)):
            market = markets['result'][keys[p]]
            id = market['instrumentID']
            symbol = market['symbol']
            base = market['longCurrency']
            quote = market['shortCurrency']
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
        response = self.privatePostGetBalances()
        balances = response['result']['accountList']
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            total = balance['balance']
            account = {
                'free': total,
                'used': 0.0,
                'total': total,
            }
            result[currency] = account
        return self.parse_balance(result)

    def fetch_market_price(self, symbol, params={}):
        self.load_markets()
        response = self.publicPostGetBestPrices(self.extend({
            'symbols': [symbol],
        }, params))
        result = response['result']
        return {
            'bid': self.safe_float(result[0], 'bestBuyPrice'),
            'ask': self.safe_float(result[0], 'bestSellPrice'),
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbols': [symbol],
        }
        if limit is not None:
            request['buyDepth'] = limit  # 100
            request['sellDepth'] = limit  # 100
        response = self.publicPostGetMarketDepth(self.extend(request, params))
        orderbook = response['result'][0]
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'price', 'volume')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        end = self.milliseconds()
        start = end - 86400000
        response = self.publicGetGetTradedPriceVolume(self.extend({
            'instrument': symbol,
            'endDate': self.ymdhms(end),
            'startDate': self.ymdhms(start),
            'HLOC': 1,
        }, params))
        tickers = response['result']['priceVolumeList']
        keys = list(tickers.keys())
        length = len(keys)
        lastKey = keys[length - 1]
        ticker = tickers[lastKey]
        timestamp = self.milliseconds()
        close = self.safe_float(ticker, 'close')
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
            'open': self.safe_float(ticker, 'open'),
            'close': close,
            'last': close,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'longVolume'),
            'quoteVolume': self.safe_float(ticker, 'shortVolume'),
            'info': ticker,
        }

    def parse_trade(self, trade, symbol=None):
        sec = self.safe_integer(trade, 'time')
        timestamp = sec * 1000
        return {
            'id': trade['tid'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'symbol': symbol,
            'type': None,
            'side': None,
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'vol'),
            'fee': None,
            'info': trade,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetGetRawTradeData(self.extend({
            'instrument': symbol,
            'timespan': 3600,
        }, params))
        result = response['result']
        trades = result['data']
        return self.parse_trades(trades, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        order = {
            'instrument': market['symbol'],
            'orderType': side.upper(),
            'amount': amount,
        }
        if type == 'limit':
            order['price'] = price
        response = self.privatePostPlaceOrder(self.extend(order, params))
        return {
            'info': response,
            'id': str(response['result']['orderID']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostCancelOrder(self.extend({
            'orderID': id,
        }, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        auth = {}
        if api == 'private':
            self.check_required_credentials()
            auth['key'] = self.apiKey
            auth['user'] = self.login
            auth['pass'] = self.password
        nonce = self.nonce()
        if method == 'GET':
            url += '?' + self.urlencode(self.extend({
                'method': path,
                'id': nonce,
            }, auth, params))
        else:
            headers = {'Content-Type': 'application/json'}
            body = self.json({
                'method': path,
                'params': self.extend(auth, params),
                'id': nonce,
            })
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response=None):
        if code == 200:
            if (body[0] == '{') or (body[0] == '['):
                response = json.loads(body)
                if 'result' in response:
                    result = response['result']
                    if 'errorCode' in result:
                        errorCode = result['errorCode']
                        if errorCode != 'OK':
                            raise ExchangeError(self.id + ' error returned: ' + body)
                else:
                    raise ExchangeError(self.id + ' malformed response: no result in response: ' + body)
            else:
                # if not a JSON response
                raise ExchangeError(self.id + ' returned a non-JSON reply: ' + body)
