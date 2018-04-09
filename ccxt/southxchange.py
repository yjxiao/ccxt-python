# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError


class southxchange (Exchange):

    def describe(self):
        return self.deep_extend(super(southxchange, self).describe(), {
            'id': 'southxchange',
            'name': 'SouthXchange',
            'countries': 'AR',  # Argentina
            'rateLimit': 1000,
            'has': {
                'CORS': True,
                'createDepositAddres': True,
                'fetchOpenOrders': True,
                'fetchTickers': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27838912-4f94ec8a-60f6-11e7-9e5d-bbf9bd50a559.jpg',
                'api': 'https://www.southxchange.com/api',
                'www': 'https://www.southxchange.com',
                'doc': 'https://www.southxchange.com/Home/Api',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'price/{symbol}',
                        'prices',
                        'book/{symbol}',
                        'trades/{symbol}',
                    ],
                },
                'private': {
                    'post': [
                        'cancelMarketOrders',
                        'cancelOrder',
                        'generatenewaddress',
                        'listOrders',
                        'listBalances',
                        'placeOrder',
                        'withdraw',
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
            },
            'commonCurrencies': {
                'SMT': 'SmartNode',
            },
        })

    def fetch_markets(self):
        markets = self.publicGetMarkets()
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            baseId = market[0]
            quoteId = market[1]
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            id = symbol
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        balances = self.privatePostListBalances()
        if not balances:
            raise ExchangeError(self.id + ' fetchBalance got an unrecognized response')
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            currencyId = balance['Currency']
            uppercase = currencyId.upper()
            currency = self.currencies_by_id[uppercase]
            code = currency['code']
            free = float(balance['Available'])
            used = float(balance['Unconfirmed'])
            total = self.sum(free, used)
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetBookSymbol(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook, None, 'BuyOrders', 'SellOrders', 'Price', 'Amount')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'Last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'Variation24Hr'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume24Hr'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetPrices(params)
        tickers = self.index_by(response, 'Market')
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetPriceSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = trade['At'] * 1000
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': None,
            'order': None,
            'type': None,
            'side': trade['Type'],
            'price': trade['Price'],
            'amount': trade['Amount'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTradesSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order(self, order, market=None):
        status = 'open'
        symbol = order['ListingCurrency'] + '/' + order['ReferenceCurrency']
        timestamp = None
        price = float(order['LimitPrice'])
        amount = self.safe_float(order, 'OriginalAmount')
        remaining = self.safe_float(order, 'Amount')
        filled = None
        cost = None
        if amount is not None:
            cost = price * amount
            if remaining is not None:
                filled = amount - remaining
        orderType = order['Type'].lower()
        result = {
            'info': order,
            'id': str(order['Code']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': orderType,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostListOrders()
        return self.parse_orders(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        order = {
            'listingCurrency': market['base'],
            'referenceCurrency': market['quote'],
            'type': side,
            'amount': amount,
        }
        if type == 'limit':
            order['limitPrice'] = price
        response = self.privatePostPlaceOrder(self.extend(order, params))
        return {
            'info': response,
            'id': str(response),
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privatePostCancelOrder(self.extend({
            'orderCode': id,
        }, params))

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privatePostGeneratenewaddress(self.extend({
            'currency': currency['id'],
        }, params))
        parts = response.split('|')
        numParts = len(parts)
        address = parts[0]
        self.check_address(address)
        tag = None
        if numParts > 1:
            tag = parts[1]
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'status': 'ok',
            'info': response,
        }

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        request = {
            'currency': currency,
            'address': address,
            'amount': amount,
        }
        if tag is not None:
            request['address'] = address + '|' + tag
        response = self.privatePostWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            query = self.extend({
                'key': self.apiKey,
                'nonce': nonce,
            }, query)
            body = self.json(query)
            headers = {
                'Content-Type': 'application/json',
                'Hash': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
