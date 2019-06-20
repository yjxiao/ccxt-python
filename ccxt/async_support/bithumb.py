# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import ExchangeNotAvailable


class bithumb (Exchange):

    def describe(self):
        return self.deep_extend(super(bithumb, self).describe(), {
            'id': 'bithumb',
            'name': 'Bithumb',
            'countries': ['KR'],  # South Korea
            'rateLimit': 500,
            'has': {
                'CORS': True,
                'fetchTickers': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30597177-ea800172-9d5e-11e7-804c-b9d4fa9b56b0.jpg',
                'api': {
                    'public': 'https://api.bithumb.com/public',
                    'private': 'https://api.bithumb.com',
                },
                'www': 'https://www.bithumb.com',
                'doc': 'https://apidocs.bithumb.com',
            },
            'api': {
                'public': {
                    'get': [
                        'ticker/{currency}',
                        'ticker/all',
                        'orderbook/{currency}',
                        'orderbook/all',
                        'transaction_history/{currency}',
                        'transaction_history/all',
                    ],
                },
                'private': {
                    'post': [
                        'info/account',
                        'info/balance',
                        'info/wallet_address',
                        'info/ticker',
                        'info/orders',
                        'info/user_transactions',
                        'trade/place',
                        'info/order_detail',
                        'trade/cancel',
                        'trade/btc_withdrawal',
                        'trade/krw_deposit',
                        'trade/krw_withdrawal',
                        'trade/market_buy',
                        'trade/market_sell',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.15 / 100,
                    'taker': 0.15 / 100,
                },
            },
            'exceptions': {
                'Bad Request(SSL)': BadRequest,
                'Bad Request(Bad Method)': BadRequest,
                'Bad Request.(Auth Data)': AuthenticationError,  # {"status": "5100", "message": "Bad Request.(Auth Data)"}
                'Not Member': AuthenticationError,
                'Invalid Apikey': AuthenticationError,  # {"status":"5300","message":"Invalid Apikey"}
                'Method Not Allowed.(Access IP)': PermissionDenied,
                'Method Not Allowed.(BTC Adress)': InvalidAddress,
                'Method Not Allowed.(Access)': PermissionDenied,
                'Database Fail': ExchangeNotAvailable,
                'Invalid Parameter': BadRequest,
                '5600': ExchangeError,
                'Unknown Error': ExchangeError,
                'After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions': ExchangeError,  # {"status":"5100","message":"After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions"}
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetTickerAll(params)
        data = self.safe_value(response, 'data')
        currencyIds = list(data.keys())
        result = []
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            if currencyId == 'date':
                continue
            market = data[currencyId]
            base = currencyId
            quote = 'KRW'
            symbol = currencyId + '/' + quote
            active = True
            if isinstance(market, list):
                numElements = len(market)
                if numElements == 0:
                    active = False
            result.append({
                'id': currencyId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'info': market,
                'active': active,
                'precision': {
                    'amount': None,
                    'price': None,
                },
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        request = {
            'currency': 'ALL',
        }
        response = await self.privatePostInfoBalance(self.extend(request, params))
        result = {'info': response}
        balances = self.safe_value(response, 'data')
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            account = self.account()
            currency = self.currency(code)
            currencyId = currency['id']
            account['total'] = self.safe_float(balances, 'total_' + currencyId)
            account['used'] = self.safe_float(balances, 'in_use_' + currencyId)
            account['free'] = self.safe_float(balances, 'available_' + currencyId)
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        if limit is not None:
            request['count'] = limit  # max = 50
        response = await self.publicGetOrderbookCurrency(self.extend(request, params))
        orderbook = self.safe_value(response, 'data')
        timestamp = self.safe_integer(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'quantity')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'date')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        open = self.safe_float(ticker, 'opening_price')
        close = self.safe_float(ticker, 'closing_price')
        change = None
        percentage = None
        average = None
        if (close is not None) and(open is not None):
            change = close - open
            if open > 0:
                percentage = change / open * 100
            average = self.sum(open, close) / 2
        vwap = self.safe_float(ticker, 'average_price')
        baseVolume = self.safe_float(ticker, 'volume_1day')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'max_price'),
            'low': self.safe_float(ticker, 'min_price'),
            'bid': self.safe_float(ticker, 'buy_price'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell_price'),
            'askVolume': None,
            'vwap': vwap,
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': baseVolume,
            'quoteVolume': baseVolume * vwap,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTickerAll(params)
        result = {}
        timestamp = self.safe_integer(response['data'], 'date')
        tickers = self.omit(response['data'], 'date')
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            ticker = tickers[id]
            isArray = isinstance(ticker, list)
            if not isArray:
                ticker['date'] = timestamp
                result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        response = await self.publicGetTickerCurrency(self.extend(request, params))
        return self.parse_ticker(response['data'], market)

    def parse_trade(self, trade, market=None):
        # a workaround for their bug in date format, hours are not 0-padded
        parts = trade['transaction_date'].split(' ')
        transaction_date = parts[0]
        transaction_time = parts[1]
        if len(transaction_time) < 8:
            transaction_time = '0' + transaction_time
        timestamp = self.parse8601(transaction_date + ' ' + transaction_time)
        timestamp -= 9 * 3600000  # they report UTC + 9 hours(server in list(Korean timezone.keys()))
        type = None
        side = self.safe_string(trade, 'type')
        side = 'sell' if (side == 'ask') else 'buy'
        id = self.safe_string(trade, 'cont_no')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'units_traded')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['base'],
        }
        if limit is None:
            request['count'] = limit  # default 20, max 100
        response = await self.publicGetTransactionHistoryCurrency(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = None
        method = 'privatePostTrade'
        if type == 'limit':
            request = {
                'order_currency': market['id'],
                'Payment_currency': market['quote'],
                'units': amount,
                'price': price,
                'type': 'bid' if (side == 'buy') else 'ask',
            }
            method += 'Place'
        elif type == 'market':
            request = {
                'currency': market['id'],
                'units': amount,
            }
            method += 'Market' + self.capitalize(side)
        response = await getattr(self, method)(self.extend(request, params))
        id = self.safe_string(response, 'order_id')
        return {
            'info': response,
            'id': id,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        side_in_params = ('side' in list(params.keys()))
        if not side_in_params:
            raise ExchangeError(self.id + ' cancelOrder requires a `side` parameter(sell or buy) and a `currency` parameter')
        currency = self.safe_string(params, 'currency')
        if currency is None:
            raise ExchangeError(self.id + ' cancelOrder requires a `currency` parameter(a currency id)')
        side = 'bid' if (params['side'] == 'buy') else 'ask'
        params = self.omit(params, ['side', 'currency'])
        request = {
            'order_id': id,
            'type': side,
            'currency': currency,
        }
        return await self.privatePostTradeCancel(self.extend(request, params))

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'units': amount,
            'address': address,
            'currency': currency['id'],
        }
        if currency == 'XRP' or currency == 'XMR':
            destination = self.safe_string(params, 'destination')
            if (tag is None) and(destination is None):
                raise ExchangeError(self.id + ' ' + code + ' withdraw() requires a tag argument or an extra destination param')
            elif tag is not None:
                request['destination'] = tag
        response = await self.privatePostTradeBtcWithdrawal(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        endpoint = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + endpoint
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'endpoint': endpoint,
            }, query))
            nonce = str(self.nonce())
            auth = endpoint + "\0" + body + "\0" + nonce  # eslint-disable-line quotes
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            signature64 = self.decode(base64.b64encode(self.encode(signature)))
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Api-Key': self.apiKey,
                'Api-Sign': str(signature64),
                'Api-Nonce': nonce,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None:
            return  # fallback to default error handler
        if 'status' in response:
            #
            #     {"status":"5100","message":"After May 23th, recent_transactions is no longer, hence users will not be able to connect to recent_transactions"}
            #
            status = self.safe_string(response, 'status')
            message = self.safe_string(response, 'message')
            if status is not None:
                if status == '0000':
                    return  # no error
                feedback = self.id + ' ' + self.json(response)
                exceptions = self.exceptions
                if status in exceptions:
                    raise exceptions[status](feedback)
                elif message in exceptions:
                    raise exceptions[message](feedback)
                else:
                    raise ExchangeError(feedback)

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'status' in response:
            if response['status'] == '0000':
                return response
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
