# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection


class gateio (Exchange):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'id': 'gateio',
            'name': 'Gate.io',
            'countries': 'CN',
            'version': '2',
            'rateLimit': 1000,
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': True,
                'withdraw': True,
                'createDepositAddress': True,
                'fetchDepositAddress': True,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchOrders': True,
                'fetchOrder': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31784029-0313c702-b509-11e7-9ccc-bc0da6a0e435.jpg',
                'api': {
                    'public': 'https://data.gate.io/api',
                    'private': 'https://data.gate.io/api',
                },
                'www': 'https://gate.io/',
                'doc': 'https://gate.io/api2',
                'fees': [
                    'https://gate.io/fee',
                    'https://support.gate.io/hc/en-us/articles/115003577673',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'pairs',
                        'marketinfo',
                        'marketlist',
                        'tickers',
                        'ticker/{id}',
                        'orderBook/{id}',
                        'trade/{id}',
                        'tradeHistory/{id}',
                        'tradeHistory/{id}/{tid}',
                    ],
                },
                'private': {
                    'post': [
                        'balances',
                        'depositAddress',
                        'newAddress',
                        'depositsWithdrawals',
                        'buy',
                        'sell',
                        'cancelOrder',
                        'cancelAllOrders',
                        'getOrder',
                        'openOrders',
                        'tradeHistory',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.002,
                    'taker': 0.002,
                },
            },
            'exceptions': {
                '4': DDoSProtection,
                '7': NotSupported,
                '8': NotSupported,
                '9': NotSupported,
                '15': DDoSProtection,
                '16': OrderNotFound,
                '17': OrderNotFound,
                '21': InsufficientFunds,
            },
            # https://gate.io/api2#errCode
            'errorCodeNames': {
                '1': 'Invalid request',
                '2': 'Invalid version',
                '3': 'Invalid request',
                '4': 'Too many attempts',
                '5': 'Invalid sign',
                '6': 'Invalid sign',
                '7': 'Currency is not supported',
                '8': 'Currency is not supported',
                '9': 'Currency is not supported',
                '10': 'Verified failed',
                '11': 'Obtaining address failed',
                '12': 'Empty params',
                '13': 'Internal error, please report to administrator',
                '14': 'Invalid user',
                '15': 'Cancel order too fast, please wait 1 min and try again',
                '16': 'Invalid order id or order is already closed',
                '17': 'Invalid orderid',
                '18': 'Invalid amount',
                '19': 'Not permitted or trade is disabled',
                '20': 'Your order size is too small',
                '21': 'You don\'t have enough fund',
            },
        })

    async def fetch_markets(self):
        response = await self.publicGetMarketinfo()
        markets = self.safe_value(response, 'pairs')
        if not markets:
            raise ExchangeError(self.id + ' fetchMarkets got an unrecognized response')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            keys = list(market.keys())
            id = keys[0]
            details = market[id]
            base, quote = id.split('_')
            base = base.upper()
            quote = quote.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': details['decimal_places'],
            }
            amountLimits = {
                'min': details['min_amount'],
                'max': None,
            }
            priceLimits = {
                'min': math.pow(10, -details['decimal_places']),
                'max': None,
            }
            costLimits = {
                'min': amountLimits['min'] * priceLimits['min'],
                'max': None,
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'info': market,
                'maker': details['fee'] / 100,
                'taker': details['fee'] / 100,
                'precision': precision,
                'limits': limits,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balance = await self.privatePostBalances()
        result = {'info': balance}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            code = self.common_currency_code(currency)
            account = self.account()
            if 'available' in balance:
                if currency in balance['available']:
                    account['free'] = float(balance['available'][currency])
            if 'locked' in balance:
                if currency in balance['locked']:
                    account['used'] = float(balance['locked'][currency])
            account['total'] = self.sum(account['free'], account['used'])
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        orderbook = await self.publicGetOrderBookId(self.extend({
            'id': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24hr'),
            'low': self.safe_float(ticker, 'low24hr'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'percentChange'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'quoteVolume'),
            'quoteVolume': self.safe_float(ticker, 'baseVolume'),
            'info': ticker,
        }

    def handle_errors(self, code, reason, url, method, headers, body):
        if len(body) <= 0:
            return
        if body[0] != '{':
            return
        jsonbodyParsed = json.loads(body)
        resultString = self.safe_string(jsonbodyParsed, 'result', '')
        if resultString != 'false':
            return
        errorCode = self.safe_string(jsonbodyParsed, 'code')
        if errorCode is not None:
            exceptions = self.exceptions
            errorCodeNames = self.errorCodeNames
            if errorCode in exceptions:
                message = ''
                if errorCode in errorCodeNames:
                    message = errorCodeNames[errorCode]
                else:
                    message = self.safe_string(jsonbodyParsed, 'message', '(unknown)')
                raise exceptions[errorCode](message)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
        result = {}
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            baseId, quoteId = id.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            ticker = tickers[id]
            market = None
            if symbol in self.markets:
                market = self.markets[symbol]
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetTickerId(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        # exchange reports local time(UTC+8)
        timestamp = self.parse8601(trade['date']) - 8 * 60 * 60 * 1000
        return {
            'id': trade['tradeID'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': self.safe_float(trade, 'rate'),
            'amount': self.safe_float(trade, 'amount'),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTradeHistoryId(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        response = await self.privatePostOpenOrders(params)
        return self.parse_orders(response['orders'], None, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privatePostGetOrder(self.extend({
            'orderNumber': id,
            'currencyPair': self.market_id(symbol),
        }, params))
        return self.parse_order(response['order'])

    def parse_order_status(self, status):
        statuses = {
            'cancelled': 'canceled',
            # 'closed': 'closed',  # these two statuses aren't actually needed
            # 'open': 'open',  # as they are mapped one-to-one
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'orderNumber')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'currencyPair')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        datetime = None
        timestamp = self.safe_integer(order, 'timestamp')
        if timestamp is not None:
            timestamp *= 1000
            datetime = self.iso8601(timestamp)
        status = self.safe_string(order, 'status')
        if status is not None:
            status = self.parse_order_status(status)
        side = self.safe_string(order, 'type')
        price = self.safe_float(order, 'filledRate')
        amount = self.safe_float(order, 'initialAmount')
        filled = self.safe_float(order, 'filledAmount')
        remaining = self.safe_float(order, 'leftAmount')
        if remaining is None:
            # In the order status response, self field has a different name.
            remaining = self.safe_float(order, 'left')
        feeCost = self.safe_float(order, 'feeValue')
        feeCurrency = self.safe_string(order, 'feeCurrency')
        if feeCurrency is not None:
            if feeCurrency in self.currencies_by_id:
                feeCurrency = self.currencies_by_id[feeCurrency]['code']
        return {
            'id': id,
            'datetime': datetime,
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': {
                'cost': feeCost,
                'currency': feeCurrency,
            },
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        market = self.market(symbol)
        order = {
            'currencyPair': market['id'],
            'rate': price,
            'amount': amount,
        }
        response = await getattr(self, method)(self.extend(order, params))
        return self.parse_order(self.extend({
            'status': 'open',
            'type': side,
            'initialAmount': amount,
        }, response), market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostCancelOrder({
            'orderNumber': id,
            'currencyPair': self.market_id(symbol),
        })

    async def query_deposit_address(self, method, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        method = 'privatePost' + method + 'Address'
        response = await getattr(self, method)(self.extend({
            'currency': currency['id'],
        }, params))
        address = self.safe_string(response, 'addr')
        tag = None
        if (address is not None) and(address.find('address') >= 0):
            raise InvalidAddress(self.id + ' queryDepositAddress ' + address)
        if code == 'XRP':
            parts = address.split('/', 2)
            address = parts[0]
            tag = parts[1]
        return {
            'currency': currency,
            'address': address,
            'tag': tag,
            'status': 'ok' if (address is not None) else 'none',
            'info': response,
        }

    async def create_deposit_address(self, code, params={}):
        return await self.query_deposit_address('New', code, params)

    async def fetch_deposit_address(self, code, params={}):
        return await self.query_deposit_address('Deposit', code, params)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostOpenOrders()
        return self.parse_orders(response['orders'], market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchMyTrades requires symbol param')
        await self.load_markets()
        market = self.market(symbol)
        id = market['id']
        response = self.privatePostTradeHistory(self.extend({'currencyPair': id}, params))
        return self.parse_trades(response['trades'], market, since, limit)

    async def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        response = await self.privatePostWithdraw(self.extend({
            'currency': currency.lower(),
            'amount': amount,
            'address': address,  # Address must exist in you AddressBook in security settings
        }, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        prefix = (api + '/') if (api == 'private') else ''
        url = self.urls['api'][api] + self.version + '/1/' + prefix + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            request = {'nonce': nonce}
            body = self.urlencode(self.extend(request, query))
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Key': self.apiKey,
                'Sign': signature,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'result' in response:
            result = response['result']
            message = self.id + ' ' + self.json(response)
            if result is None:
                raise ExchangeError(message)
            if isinstance(result, basestring):
                if result != 'true':
                    raise ExchangeError(message)
            elif not result:
                raise ExchangeError(message)
        return response
