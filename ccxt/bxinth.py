# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class bxinth (Exchange):

    def describe(self):
        return self.deep_extend(super(bxinth, self).describe(), {
            'id': 'bxinth',
            'name': 'BX.in.th',
            'countries': ['TH'],  # Thailand
            'rateLimit': 1500,
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOpenOrders': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766412-567b1eb4-5ed7-11e7-94a8-ff6a3884f6c5.jpg',
                'api': 'https://bx.in.th/api',
                'www': 'https://bx.in.th',
                'doc': 'https://bx.in.th/info/api',
            },
            'api': {
                'public': {
                    'get': [
                        '',  # ticker
                        'options',
                        'optionbook',
                        'orderbook',
                        'pairing',
                        'trade',
                        'tradehistory',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'biller',
                        'billgroup',
                        'billpay',
                        'cancel',
                        'deposit',
                        'getorders',
                        'history',
                        'option-issue',
                        'option-bid',
                        'option-sell',
                        'option-myissue',
                        'option-mybid',
                        'option-myoptions',
                        'option-exercise',
                        'option-cancel',
                        'option-history',
                        'order',
                        'withdrawal',
                        'withdrawal-history',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                },
            },
            'commonCurrencies': {
                'DAS': 'DASH',
                'DOG': 'DOGE',
                'LEO': 'LeoCoin',
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetPairing(params)
        keys = list(response.keys())
        result = []
        for i in range(0, len(keys)):
            key = keys[i]
            market = response[key]
            id = self.safe_string(market, 'pairing_id')
            baseId = self.safe_string(market, 'secondary_currency')
            quoteId = self.safe_string(market, 'primary_currency')
            active = self.safe_value(market, 'active')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalance(params)
        balances = self.safe_value(response, 'balance', {})
        result = {'info': balances}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.common_currency_code(currencyId)
            balance = self.safe_value(balances, currencyId, {})
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['total'] = self.safe_float(balance, 'total')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pairing': self.market_id(symbol),
        }
        response = self.publicGetOrderbook(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last_price')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker['orderbook']['bids'], 'highbid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker['orderbook']['asks'], 'highbid'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'change'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume_24hours'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGet(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            ticker = response[id]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        id = market['id']
        request = {
            'pairing': id,
        }
        response = self.publicGet(self.extend(request, params))
        ticker = self.safe_value(response, id)
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        date = self.safe_string(trade, 'trade_date')
        timestamp = None
        if date is not None:
            timestamp = self.parse8601(date + '+07:00')  # Thailand UTC+7 offset
        id = self.safe_string(trade, 'trade_id')
        orderId = self.safe_string(trade, 'order_id')
        type = None
        side = self.safe_string(trade, 'trade_type')
        price = self.safe_float(trade, 'rate')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        return {
            'id': id,
            'info': trade,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pairing': market['id'],
        }
        response = self.publicGetTrade(self.extend(request, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'pairing': self.market_id(symbol),
            'type': side,
            'amount': amount,
            'rate': price,
        }
        response = self.privatePostOrder(self.extend(request, params))
        id = self.safe_string(response, 'order_id')
        return {
            'info': response,
            'id': id,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        pairing = None  # TODO fixme
        request = {
            'order_id': id,
            'pairing': pairing,
        }
        return self.privatePostCancel(self.extend(request, params))

    def parse_order(self, order, market=None):
        side = self.safe_string(order, 'order_type')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'pairing_id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'date'))
        price = self.safe_float(order, 'rate')
        amount = self.safe_float(order, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        id = self.safe_string(order, 'order_id')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pairing'] = market['id']
        response = self.privatePostGetorders(self.extend(request, params))
        orders = self.parse_orders(response['orders'], market, since, limit)
        return self.filter_by_symbol(orders, symbol)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if path:
            url += path + '/'
        if params:
            url += '?' + self.urlencode(params)
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            auth = self.apiKey + str(nonce) + self.secret
            signature = self.hash(self.encode(auth), 'sha256')
            body = self.urlencode(self.extend({
                'key': self.apiKey,
                'nonce': nonce,
                'signature': signature,
                # twofa: self.twofa,
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'public':
            return response
        if 'success' in response:
            if response['success']:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))
