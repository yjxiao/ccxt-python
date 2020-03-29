# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OnMaintenance


class coinone(Exchange):

    def describe(self):
        return self.deep_extend(super(coinone, self).describe(), {
            'id': 'coinone',
            'name': 'CoinOne',
            'countries': ['KR'],  # Korea
            'rateLimit': 667,
            'version': 'v2',
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': True,
                'fetchOrder': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38003300-adc12fba-323f-11e8-8525-725f53c4a659.jpg',
                'api': 'https://api.coinone.co.kr',
                'www': 'https://coinone.co.kr',
                'doc': 'https://doc.coinone.co.kr',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'orderbook/',
                        'trades/',
                        'ticker/',
                    ],
                },
                'private': {
                    'post': [
                        'account/btc_deposit_address/',
                        'account/balance/',
                        'account/daily_balance/',
                        'account/user_info/',
                        'account/virtual_account/',
                        'order/cancel_all/',
                        'order/cancel/',
                        'order/limit_buy/',
                        'order/limit_sell/',
                        'order/complete_orders/',
                        'order/limit_orders/',
                        'order/order_info/',
                        'transaction/auth_number/',
                        'transaction/history/',
                        'transaction/krw/history/',
                        'transaction/btc/',
                        'transaction/coin/',
                    ],
                },
            },
            'markets': {
                'BCH/KRW': {'id': 'bch', 'symbol': 'BCH/KRW', 'base': 'BCH', 'quote': 'KRW', 'baseId': 'bch', 'quoteId': 'krw'},
                'BTC/KRW': {'id': 'btc', 'symbol': 'BTC/KRW', 'base': 'BTC', 'quote': 'KRW', 'baseId': 'btc', 'quoteId': 'krw'},
                'BTG/KRW': {'id': 'btg', 'symbol': 'BTG/KRW', 'base': 'BTG', 'quote': 'KRW', 'baseId': 'btg', 'quoteId': 'krw'},
                'ETC/KRW': {'id': 'etc', 'symbol': 'ETC/KRW', 'base': 'ETC', 'quote': 'KRW', 'baseId': 'etc', 'quoteId': 'krw'},
                'ETH/KRW': {'id': 'eth', 'symbol': 'ETH/KRW', 'base': 'ETH', 'quote': 'KRW', 'baseId': 'eth', 'quoteId': 'krw'},
                'IOTA/KRW': {'id': 'iota', 'symbol': 'IOTA/KRW', 'base': 'IOTA', 'quote': 'KRW', 'baseId': 'iota', 'quoteId': 'krw'},
                'LTC/KRW': {'id': 'ltc', 'symbol': 'LTC/KRW', 'base': 'LTC', 'quote': 'KRW', 'baseId': 'ltc', 'quoteId': 'krw'},
                'OMG/KRW': {'id': 'omg', 'symbol': 'OMG/KRW', 'base': 'OMG', 'quote': 'KRW', 'baseId': 'omg', 'quoteId': 'krw'},
                'QTUM/KRW': {'id': 'qtum', 'symbol': 'QTUM/KRW', 'base': 'QTUM', 'quote': 'KRW', 'baseId': 'qtum', 'quoteId': 'krw'},
                'XRP/KRW': {'id': 'xrp', 'symbol': 'XRP/KRW', 'base': 'XRP', 'quote': 'KRW', 'baseId': 'xrp', 'quoteId': 'krw'},
                'EOS/KRW': {'id': 'eos', 'symbol': 'EOS/KRW', 'base': 'EOS', 'quote': 'KRW', 'baseId': 'eos', 'quoteId': 'krw'},
                'DATA/KRW': {'id': 'data', 'symbol': 'DATA/KRW', 'base': 'DATA', 'quote': 'KRW', 'baseId': 'data', 'quoteId': 'krw'},
                'ZIL/KRW': {'id': 'zil', 'symbol': 'ZIL/KRW', 'base': 'ZIL', 'quote': 'KRW', 'baseId': 'zil', 'quoteId': 'krw'},
                'KNC/KRW': {'id': 'knc', 'symbol': 'KNC/KRW', 'base': 'KNC', 'quote': 'KRW', 'baseId': 'knc', 'quoteId': 'krw'},
                'ZRX/KRW': {'id': 'zrx', 'symbol': 'ZRX/KRW', 'base': 'ZRX', 'quote': 'KRW', 'baseId': 'zrx', 'quoteId': 'krw'},
                'LUNA/KRW': {'id': 'luna', 'symbol': 'LUNA/KRW', 'base': 'LUNA', 'quote': 'KRW', 'baseId': 'luna', 'quoteId': 'krw'},
                'ATOM/KRW': {'id': 'atom', 'symbol': 'ATOM/KRW', 'base': 'ATOM', 'quote': 'KRW', 'baseId': 'atom', 'quoteId': 'krw'},
                'VNT/KRW': {'id': 'vnt', 'symbol': 'VNT/KRW', 'base': 'VNT', 'quote': 'KRW', 'baseId': 'vnt', 'quoteId': 'krw'},
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                    'tiers': {
                        'taker': [
                            [0, 0.001],
                            [100000000, 0.0009],
                            [1000000000, 0.0008],
                            [5000000000, 0.0007],
                            [10000000000, 0.0006],
                            [20000000000, 0.0005],
                            [30000000000, 0.0004],
                            [40000000000, 0.0003],
                            [50000000000, 0.0002],
                        ],
                        'maker': [
                            [0, 0.001],
                            [100000000, 0.0008],
                            [1000000000, 0.0006],
                            [5000000000, 0.0004],
                            [10000000000, 0.0002],
                            [20000000000, 0],
                            [30000000000, 0],
                            [40000000000, 0],
                            [50000000000, 0],
                        ],
                    },
                },
            },
            'exceptions': {
                '405': OnMaintenance,  # {"errorCode":"405","status":"maintenance","result":"error"}
                '104': OrderNotFound,
                '108': BadSymbol,  # {"errorCode":"108","errorMsg":"Unknown CryptoCurrency","result":"error"}
                '107': BadRequest,  # {"errorCode":"107","errorMsg":"Parameter error","result":"error"}
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostAccountBalance(params)
        result = {'info': response}
        balances = self.omit(response, [
            'errorCode',
            'result',
            'normalWallets',
        ])
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            balance = balances[currencyId]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'avail')
            account['total'] = self.safe_float(balance, 'balance')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = await self.publicGetOrderbook(self.extend(request, params))
        return self.parse_order_book(response, None, 'bid', 'ask', 'price', 'qty')

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        request = {
            'currency': 'all',
            'format': 'json',
        }
        response = await self.publicGetTicker(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = id
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
                ticker = response[id]
                result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
            'format': 'json',
        }
        response = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'last')
        previousClose = self.safe_float(ticker, 'yesterday_last')
        change = None
        if last is not None and previousClose is not None:
            change = previousClose - last
        symbol = market['symbol'] if (market is not None) else None
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
            'open': self.safe_float(ticker, 'first'),
            'close': last,
            'last': last,
            'previousClose': previousClose,
            'change': change,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'timestamp')
        symbol = market['symbol'] if (market is not None) else None
        is_ask = self.safe_string(trade, 'is_ask')
        side = None
        if is_ask == '1':
            side = 'sell'
        elif is_ask == '0':
            side = 'buy'
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'qty')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'id': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'symbol': symbol,
            'type': None,
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
            'currency': market['id'],
            'period': 'hour',
            'format': 'json',
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response['completeOrders'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        request = {
            'price': price,
            'currency': self.market_id(symbol),
            'qty': amount,
        }
        method = 'privatePostOrder' + self.capitalize(type) + self.capitalize(side)
        response = await getattr(self, method)(self.extend(request, params))
        id = self.safe_string(response, 'orderId')
        if id is not None:
            id = id.upper()
        timestamp = self.milliseconds()
        cost = price * amount
        order = {
            'info': response,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': cost,
            'average': None,
            'amount': amount,
            'filled': None,
            'remaining': amount,
            'status': 'open',
            'fee': None,
            'clientOrderId': None,
            'trades': None,
        }
        self.orders[id] = order
        return order

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        result = None
        market = None
        if symbol is None:
            if id in self.orders:
                market = self.market(self.orders[id]['symbol'])
            else:
                raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument for order ids missing in the .orders cache(the order was created with a different instance of self class or within a different run of self code).')
        else:
            market = self.market(symbol)
        try:
            request = {
                'order_id': id,
                'currency': market['id'],
            }
            response = await self.privatePostOrderOrderInfo(self.extend(request, params))
            result = self.parse_order(response)
            self.orders[id] = result
        except Exception as e:
            if isinstance(e, OrderNotFound):
                if id in self.orders:
                    self.orders[id]['status'] = 'canceled'
                    result = self.orders[id]
                else:
                    raise e
            else:
                raise e
        return result

    def parse_order_status(self, status):
        statuses = {
            'live': 'open',
            'partially_filled': 'open',
            'filled': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "index": "0",
        #         "orderId": "68665943-1eb5-4e4b-9d76-845fc54f5489",
        #         "timestamp": "1449037367",
        #         "price": "444000.0",
        #         "qty": "0.3456",
        #         "type": "ask",
        #         "feeRate": "-0.0015"
        #     }
        #
        info = self.safe_value(order, 'info')
        id = self.safe_string_upper(info, 'orderId')
        timestamp = self.safe_timestamp(info, 'timestamp')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        cost = None
        side = self.safe_string(info, 'type')
        if side.find('ask') >= 0:
            side = 'sell'
        else:
            side = 'buy'
        price = self.safe_float(info, 'price')
        amount = self.safe_float(info, 'qty')
        remaining = self.safe_float(info, 'remainQty')
        filled = None
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
            if price is not None:
                cost = price * amount
        currency = self.safe_string(info, 'currency')
        fee = {
            'currency': currency,
            'cost': self.safe_float(info, 'fee'),
            'rate': self.safe_float(info, 'feeRate'),
        }
        symbol = None
        if market is None:
            marketId = currency.lower()
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        return {
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'average': None,
            'trades': None,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        order = self.safe_value(self.orders, id)
        amount = None
        price = None
        side = None
        if order is None:
            if symbol is None:
                # eslint-disable-next-line quotes
                raise InvalidOrder(self.id + " cancelOrder could not find the order id " + id + " in orders cache. The order was probably created with a different instance of self class earlier. The `symbol` argument is missing. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
            price = self.safe_float(params, 'price')
            if price is None:
                # eslint-disable-next-line quotes
                raise InvalidOrder(self.id + " cancelOrder could not find the order id " + id + " in orders cache. The order was probably created with a different instance of self class earlier. The `price` parameter is missing. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
            amount = self.safe_float(params, 'qty')
            if amount is None:
                # eslint-disable-next-line quotes
                raise InvalidOrder(self.id + " cancelOrder could not find the order id " + id + " in orders cache. The order was probably created with a different instance of self class earlier. The `qty`(amount) parameter is missing. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
            side = self.safe_float(params, 'is_ask')
            if side is None:
                # eslint-disable-next-line quotes
                raise InvalidOrder(self.id + " cancelOrder could not find the order id " + id + " in orders cache. The order was probably created with a different instance of self class earlier. The `is_ask`(side) parameter is missing. To cancel the order, pass a symbol argument and {'price': 12345, 'qty': 1.2345, 'is_ask': 0} in the params argument of cancelOrder.")
        else:
            price = order['price']
            amount = order['amount']
            side = 0 if (order['side'] == 'buy') else 1
            symbol = order['symbol']
        request = {
            'order_id': id,
            'price': price,
            'qty': amount,
            'is_ask': side,
            'currency': self.market_id(symbol),
        }
        self.orders[id]['status'] = 'canceled'
        return await self.privatePostOrderCancel(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/'
        if api == 'public':
            url += request
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/' + request
            nonce = str(self.nonce())
            json = self.json(self.extend({
                'access_token': self.apiKey,
                'nonce': nonce,
            }, params))
            payload = base64.b64encode(self.encode(json))
            body = self.decode(payload)
            secret = self.secret.upper()
            signature = self.hmac(payload, self.encode(secret), hashlib.sha512)
            headers = {
                'content-type': 'application/json',
                'X-COINONE-PAYLOAD': payload,
                'X-COINONE-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'result' in response:
            result = response['result']
            if result != 'success':
                #
                #    { "errorCode": "405",  "status": "maintenance",  "result": "error"}
                #
                errorCode = self.safe_string(response, 'errorCode')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
                raise ExchangeError(feedback)
        else:
            raise ExchangeError(self.id + ' ' + body)
