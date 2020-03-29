# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange


class vaultoro(Exchange):

    def describe(self):
        return self.deep_extend(super(vaultoro, self).describe(), {
            'id': 'vaultoro',
            'name': 'Vaultoro',
            'countries': ['CH'],
            'rateLimit': 1000,
            'version': '1',
            'has': {
                'CORS': True,
                'fetchMarkets': True,
                'fetchOrderBook': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchTrades': True,
                'fetchTicker': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766880-f205e870-5ee9-11e7-8fe2-0d5b15880752.jpg',
                'api': 'https://api.vaultoro.com',
                'www': 'https://www.vaultoro.com',
                'doc': 'https://api.vaultoro.com',
            },
            'commonCurrencies': {
                'GLD': 'Gold',
            },
            'api': {
                'public': {
                    'get': [
                        'bidandask',
                        'buyorders',
                        'latest',
                        'latesttrades',
                        'markets',
                        'orderbook',
                        'sellorders',
                        'transactions/day',
                        'transactions/hour',
                        'transactions/month',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                        'mytrades',
                        'orders',
                    ],
                    'post': [
                        'buy/{symbol}/{type}',
                        'cancel/{id}',
                        'sell/{symbol}/{type}',
                        'withdraw',
                    ],
                },
            },
        })

    def fetch_markets(self, params={}):
        result = []
        response = self.publicGetMarkets(params)
        market = self.safe_value(response, 'data')
        baseId = self.safe_string(market, 'MarketCurrency')
        quoteId = self.safe_string(market, 'BaseCurrency')
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        symbol = base + '/' + quote
        id = self.safe_string(market, 'MarketName')
        result.append({
            'id': id,
            'symbol': symbol,
            'base': base,
            'quote': quote,
            'baseId': baseId,
            'quoteId': quoteId,
            'info': market,
            'active': None,
            'precision': self.precision,
            'limits': self.limits,
        })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalance(params)
        balances = self.safe_value(response, 'data')
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'cash')
            account['used'] = self.safe_float(balance, 'reserved')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        response = self.publicGetOrderbook(params)
        orderbook = {
            'bids': response['data'][0]['b'],
            'asks': response['data'][1]['s'],
        }
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'Gold_Price', 'Gold_Amount')

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string(trade, 'Time'))
        symbol = None
        if market is not None:
            symbol = market['symbol']
        price = self.safe_float(trade, 'Gold_Price')
        amount = self.safe_float(trade, 'Gold_Amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        return {
            'id': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTransactionsDay(params)
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost' + self.capitalize(side) + 'SymbolType'
        request = {
            'symbol': market['quoteId'].lower(),
            'type': type,
            'gld': amount,
            'price': price or 1,
        }
        response = getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': response['data']['Order_ID'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        return self.privatePostCancelId(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if api == 'public':
            url += path
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            url += self.version + '/' + self.implode_params(path, params)
            query = self.extend({
                'nonce': nonce,
                'apikey': self.apiKey,
            }, self.omit(params, self.extract_params(path)))
            url += '?' + self.urlencode(query)
            headers = {
                'Content-Type': 'application/json',
                'X-Signature': self.hmac(self.encode(url), self.encode(self.secret)),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
