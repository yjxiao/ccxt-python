# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class quadrigacx (Exchange):

    def describe(self):
        return self.deep_extend(super(quadrigacx, self).describe(), {
            'id': 'quadrigacx',
            'name': 'QuadrigaCX',
            'countries': ['CA'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'fetchDepositAddress': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchMyTrades': True,
                'CORS': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766825-98a6d0de-5ee7-11e7-9fa4-38e11a2c6f52.jpg',
                'api': 'https://api.quadrigacx.com',
                'www': 'https://www.quadrigacx.com',
                'doc': 'https://www.quadrigacx.com/api_info',
                'referral': 'https://www.quadrigacx.com/?ref=laiqgbp6juewva44finhtmrk',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'order_book',
                        'ticker',
                        'transactions',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'bitcoin_deposit_address',
                        'bitcoin_withdrawal',
                        'bitcoincash_deposit_address',
                        'bitcoincash_withdrawal',
                        'bitcoingold_deposit_address',
                        'bitcoingold_withdrawal',
                        'buy',
                        'cancel_order',
                        'ether_deposit_address',
                        'ether_withdrawal',
                        'litecoin_deposit_address',
                        'litecoin_withdrawal',
                        'lookup_order',
                        'open_orders',
                        'sell',
                        'user_transactions',
                    ],
                },
            },
            'markets': {
                'BTC/CAD': {'id': 'btc_cad', 'symbol': 'BTC/CAD', 'base': 'BTC', 'quote': 'CAD', 'baseId': 'btc', 'quoteId': 'cad', 'maker': 0.005, 'taker': 0.005},
                'BTC/USD': {'id': 'btc_usd', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'btc', 'quoteId': 'usd', 'maker': 0.005, 'taker': 0.005},
                'ETH/BTC': {'id': 'eth_btc', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'eth', 'quoteId': 'btc', 'maker': 0.002, 'taker': 0.002},
                'ETH/CAD': {'id': 'eth_cad', 'symbol': 'ETH/CAD', 'base': 'ETH', 'quote': 'CAD', 'baseId': 'eth', 'quoteId': 'cad', 'maker': 0.005, 'taker': 0.005},
                'LTC/CAD': {'id': 'ltc_cad', 'symbol': 'LTC/CAD', 'base': 'LTC', 'quote': 'CAD', 'baseId': 'ltc', 'quoteId': 'cad', 'maker': 0.005, 'taker': 0.005},
                'LTC/BTC': {'id': 'ltc_btc', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC', 'baseId': 'ltc', 'quoteId': 'btc', 'maker': 0.005, 'taker': 0.005},
                'BCH/CAD': {'id': 'bch_cad', 'symbol': 'BCH/CAD', 'base': 'BCH', 'quote': 'CAD', 'baseId': 'bch', 'quoteId': 'cad', 'maker': 0.005, 'taker': 0.005},
                'BCH/BTC': {'id': 'bch_btc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bch', 'quoteId': 'btc', 'maker': 0.005, 'taker': 0.005},
                'BTG/CAD': {'id': 'btg_cad', 'symbol': 'BTG/CAD', 'base': 'BTG', 'quote': 'CAD', 'baseId': 'btg', 'quoteId': 'cad', 'maker': 0.005, 'taker': 0.005},
                'BTG/BTC': {'id': 'btg_btc', 'symbol': 'BTG/BTC', 'base': 'BTG', 'quote': 'BTC', 'baseId': 'btg', 'quoteId': 'btc', 'maker': 0.005, 'taker': 0.005},
            },
            'exceptions': {
                '101': AuthenticationError,
            },
        })

    async def fetch_balance(self, params={}):
        balances = await self.privatePostBalance()
        result = {'info': balances}
        currencyIds = list(self.currencies_by_id.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            currency = self.currencies_by_id[currencyId]
            code = currency['code']
            result[code] = {
                'free': self.safe_float(balances, currencyId + '_available'),
                'used': self.safe_float(balances, currencyId + '_reserved'),
                'total': self.safe_float(balances, currencyId + '_balance'),
            }
        return self.parse_balance(result)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['book'] = market['id']
        if limit is not None:
            request['limit'] = limit
        response = await self.privatePostUserTransactions(self.extend(request, params))
        trades = self.filter_by(response, 'type', 2)
        return self.parse_trades(trades, market, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        request = {
            'id': id,
        }
        response = await self.privatePostLookupOrder(self.extend(request, params))
        return self.parse_orders(response)

    def parse_order_status(self, status):
        statuses = {
            '-1': 'canceled',
            '0': 'open',
            '1': 'open',
            '2': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        price = self.safe_float(order, 'price')
        amount = None
        filled = None
        remaining = self.safe_float(order, 'amount')
        cost = None
        symbol = None
        marketId = self.safe_string(order, 'book')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        else:
            baseId, quoteId = marketId.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
        side = self.safe_string(order, 'type')
        if side == '0':
            side = 'buy'
        else:
            side = 'sell'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.parse8601(self.safe_string(order, 'created'))
        lastTradeTimestamp = self.parse8601(self.safe_string(order, 'updated'))
        type = 'market' if (price == 0.0) else 'limit'
        if market is not None:
            symbol = market['symbol']
        if status == 'closed':
            amount = remaining
            filled = remaining
            remaining = 0
        if (type == 'limit') and(price is not None):
            if filled is not None:
                cost = price * filled
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'average': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        orderbook = await self.publicGetOrderBook(self.extend({
            'book': self.market_id(symbol),
        }, params))
        timestamp = int(orderbook['timestamp']) * 1000
        return self.parse_order_book(orderbook, timestamp)

    async def fetch_tickers(self, symbols=None, params={}):
        response = await self.publicGetTicker(self.extend({
            'book': 'all',
        }, params))
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                baseId, quoteId = id.split('_')
                base = baseId.upper()
                quote = quoteId.upper()
                base = self.common_currency_code(base)
                quote = self.common_currency_code(base)
                symbol = base + '/' + quote
                market = {
                    'symbol': symbol,
                }
            result[symbol] = self.parse_ticker(response[id], market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTicker(self.extend({
            'book': market['id'],
        }, params))
        return self.parse_ticker(response, market)

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = int(ticker['timestamp']) * 1000
        vwap = self.safe_float(ticker, 'vwap')
        baseVolume = self.safe_float(ticker, 'volume')
        quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': None,
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

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {"amount":"2.26252009","date":"1541355778","price":"0.03300000","tid":3701722,"side":"sell"}
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "datetime": "2018-01-01T00:00:00",  # date and time
        #         "id": 123,  # unique identifier(only for trades)
        #         "type": 2,  # transaction type(0 - deposit 1 - withdrawal 2 - trade)
        #         "method": "...",  # deposit or withdrawal method
        #         "(minor currency code)" – the minor currency amount
        #         "(major currency code)" – the major currency amount
        #         "order_id": "...",  # a 64 character long hexadecimal string representing the order that was fully or partially filled(only for trades)
        #         "fee": 123.45,  # transaction fee
        #         "rate": 54.321,  # rate per btc(only for trades)
        #     }
        #
        id = self.safe_string_2(trade, 'tid', 'id')
        timestamp = self.parse8601(self.safe_string(trade, 'datetime'))
        if timestamp is None:
            timestamp = self.safe_integer(trade, 'date')
            if timestamp is not None:
                timestamp *= 1000
        symbol = None
        omitted = self.omit(trade, ['datetime', 'id', 'type', 'method', 'order_id', 'fee', 'rate'])
        keys = list(omitted.keys())
        rate = self.safe_float(trade, 'rate')
        for i in range(0, len(keys)):
            marketId = keys[i]
            floatValue = self.safe_float(trade, marketId)
            if floatValue == rate:
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
                else:
                    currencyIds = marketId.split('_')
                    numCurrencyIds = len(currencyIds)
                    if numCurrencyIds == 2:
                        baseId = currencyIds[0]
                        quoteId = currencyIds[1]
                        base = baseId.upper()
                        quote = quoteId.upper()
                        base = self.common_currency_code(base)
                        quote = self.common_currency_code(base)
                        symbol = base + '/' + quote
        orderId = self.safe_string(trade, 'order_id')
        side = self.safe_string(trade, 'side')
        price = self.safe_float(trade, 'price', rate)
        amount = self.safe_float(trade, 'amount')
        cost = None
        if market is not None:
            symbol = market['symbol']
            baseId = market['baseId']
            quoteId = market['quoteId']
            if amount is None:
                amount = self.safe_float(trade, baseId)
                if amount is not None:
                    amount = abs(amount)
            cost = self.safe_float(trade, quoteId)
            if cost is not None:
                cost = abs(cost)
            if side is None:
                if self.safe_float(trade, market['base']) > 0:
                    side = 'buy'
                else:
                    side = 'sell'
        if cost is None:
            if price is not None:
                if amount is not None:
                    cost = amount * price
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            feeCurrency = None
            if market is not None:
                feeCurrency = market['base'] if (side == 'buy') else market['quote']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = await self.publicGetTransactions(self.extend({
            'book': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        method = 'privatePost' + self.capitalize(side)
        order = {
            'amount': amount,
            'book': self.market_id(symbol),
        }
        if type == 'limit':
            order['price'] = price
        response = await getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': str(response['id']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        return await self.privatePostCancelOrder(self.extend({
            'id': id,
        }, params))

    async def fetch_deposit_address(self, code, params={}):
        method = 'privatePost' + self.get_currency_name(code) + 'DepositAddress'
        response = await getattr(self, method)(params)
        # [E|e]rror
        if response.find('rror') >= 0:
            raise ExchangeError(self.id + ' ' + response)
        self.check_address(response)
        return {
            'currency': code,
            'address': response,
            'tag': None,
            'info': response,
        }

    def get_currency_name(self, code):
        currencies = {
            'ETH': 'Ether',
            'BTC': 'Bitcoin',
            'LTC': 'Litecoin',
            'BCH': 'Bitcoincash',
            'BTG': 'Bitcoingold',
        }
        return currencies[code]

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        request = {
            'amount': amount,
            'address': address,
        }
        method = 'privatePost' + self.get_currency_name(code) + 'Withdrawal'
        response = await getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            request = ''.join([str(nonce), self.uid, self.apiKey])
            signature = self.hmac(self.encode(request), self.encode(self.secret))
            query = self.extend({
                'key': self.apiKey,
                'nonce': nonce,
                'signature': signature,
            }, params)
            body = self.json(query)
            headers = {
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, statusCode, statusText, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            error = self.safe_value(response, 'error')
            if error is not None:
                #
                # {"error":{"code":101,"message":"Invalid API Code or Invalid Signature"}}
                #
                code = self.safe_string(error, 'code')
                feedback = self.id + ' ' + self.json(response)
                exceptions = self.exceptions
                if code in exceptions:
                    raise exceptions[code](feedback)
                else:
                    raise ExchangeError(self.id + ' unknown "error" value: ' + self.json(response))
