# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import DDoSProtection


class coinnest (Exchange):

    def describe(self):
        return self.deep_extend(super(coinnest, self).describe(), {
            'id': 'coinnest',
            'name': 'coinnest',
            'countries': ['KR'],
            'rateLimit': 1000,
            'has': {
                'fetchOpenOrders': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38065728-7289ff5c-330d-11e8-9cc1-cf0cbcb606bc.jpg',
                'api': {
                    'public': 'https://api.coinnest.co.kr/api',
                    'private': 'https://api.coinnest.co.kr/api',
                    'web': 'https://www.coinnest.co.kr',
                },
                'www': 'https://www.coinnest.co.kr',
                'doc': 'https://www.coinnest.co.kr/doc/intro.html',
                'fees': [
                    'https://coinnesthelp.zendesk.com/hc/ko/articles/115002110252-%EA%B1%B0%EB%9E%98-%EC%88%98%EC%88%98%EB%A3%8C%EB%8A%94-%EC%96%BC%EB%A7%88%EC%9D%B8%EA%B0%80%EC%9A%94-',
                    'https://coinnesthelp.zendesk.com/hc/ko/articles/115002110272-%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8-%EC%88%98%EC%88%98%EB%A3%8C%EB%A5%BC-%EC%84%A0%ED%83%9D%ED%95%98%EB%8A%94-%EC%9D%B4%EC%9C%A0%EA%B0%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94-',
                ],
            },
            'api': {
                'web': {
                    'get': [
                        'coin/allcoin',
                    ],
                },
                'public': {
                    'get': [
                        'pub/ticker',
                        'pub/depth',
                        'pub/trades',
                    ],
                },
                'private': {
                    'post': [
                        'account/balance',
                        'trade/add',
                        'trade/cancel',
                        'trade/fetchtrust',
                        'trade/trust',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': '0.002',
                    },
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    async def fetch_markets(self):
        quote = 'KRW'
        quoteId = quote.lower()
        # todo: rewrite self for web endpoint
        coins = [
            'btc',
            'bch',
            'btg',
            'bcd',
            'ubtc',
            'btn',
            'kst',
            'ltc',
            'act',
            'eth',
            'etc',
            'ada',
            'qtum',
            'xlm',
            'neo',
            'gas',
            'rpx',
            'hsr',
            'knc',
            'tsl',
            'tron',
            'omg',
            'wtc',
            'mco',
            'storm',
            'gto',
            'pxs',
            'chat',
            'ink',
            'oc',
            'hlc',
            'ent',
            'qbt',
            'spc',
            'put',
        ]
        result = []
        for i in range(0, len(coins)):
            baseId = coins[i]
            id = baseId + '/' + quoteId
            base = self.common_currency_code(baseId.upper())
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'info': None,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['time'] * 1000
        symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetPubTicker(self.extend({
            'coin': market['baseId'],
        }, params))
        return self.parse_ticker(ticker, market)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        orderbook = await self.publicGetPubDepth(self.extend({
            'coin': market['baseId'],
        }, params))
        return self.parse_order_book(orderbook)

    def parse_trade(self, trade, market=None):
        timestamp = int(trade['date']) * 1000
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        symbol = market['symbol']
        cost = self.price_to_precision(symbol, amount * price)
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'tid'),
            'order': None,
            'type': 'limit',
            'side': trade['type'],
            'price': price,
            'amount': amount,
            'cost': float(cost),
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        trades = await self.publicGetPubTrades(self.extend({
            'coin': market['baseId'],
        }, params))
        return self.parse_trades(trades, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostAccountBalance(params)
        result = {'info': response}
        balancKeys = list(response.keys())
        for i in range(0, len(balancKeys)):
            key = balancKeys[i]
            parts = key.split('_')
            if len(parts) != 2:
                continue
            type = parts[1]
            if type != 'reserved' and type != 'balance':
                continue
            currency = parts[0].upper()
            currency = self.common_currency_code(currency)
            if not(currency in list(result.keys())):
                result[currency] = {
                    'free': 0.0,
                    'used': 0.0,
                    'total': 0.0,
                }
            type = (type == 'used' if 'reserved' else 'free')
            result[currency][type] = float(response[key])
            otherType = (type == 'free' if 'used' else 'used')
            if otherType in result[currency]:
                result[currency]['total'] = self.sum(result[currency]['free'], result[currency]['used'])
        return self.parse_balance(result)

    def parse_order(self, order, market):
        symbol = market['symbol']
        timestamp = int(order['time']) * 1000
        status = int(order['status'])
        # 1: newly created, 2: ready for dealing, 3: canceled, 4: completed.
        if status == 4:
            status = 'closed'
        elif status == 3:
            status = 'canceled'
        else:
            status = 'open'
        amount = self.safe_float(order, 'amount_total')
        remaining = self.safe_float(order, 'amount_over')
        filled = self.safe_value(order, 'deals')
        if filled:
            filled = self.safe_float(filled, 'sum_amount')
        else:
            filled = amount - remaining
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': order['type'],
            'price': self.safe_float(order, 'price'),
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': self.safe_value(order, 'info', order),
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostTradeAdd(self.extend({
            'coin': market['baseId'],
            'type': side,
            'number': amount,
            'price': price,
        }, params))
        order = {
            'id': response['id'],
            'time': self.seconds(),
            'type': side,
            'price': price,
            'amount_total': amount,
            'amount_over': amount,
            'info': response,
        }
        id = order['id']
        self.orders[id] = self.parse_order(order, market)
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostTradeCancel(self.extend({
            'id': id,
            'coin': market['baseId'],
        }, params))
        return response

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        order = await self.privatePostTradeFetchtrust(self.extend({
            'id': id,
            'coin': market['baseId'],
        }, params))
        return self.parse_order(order, market)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['baseId'],
        }
        if since:
            request['since'] = int(since / 1000)
        if limit:
            request['limit'] = limit
        response = await self.privatePostTradeTrust(self.extend(request, params))
        return self.parse_orders(response, market)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders(symbol, since, limit, self.extend({
            'type': '1',
        }, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        query = None
        if api == 'public':
            query = self.urlencode(params)
            if len(query):
                url += '?' + query
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend(params, {
                'key': self.apiKey,
                'nonce': self.nonce(),
            }))
            secret = self.hash(self.secret)
            body += '&signature=' + self.hmac(self.encode(body), self.encode(secret))
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        status = self.safe_string(response, 'status')
        if not response or response == 'nil' or status:
            ErrorClass = self.safe_value({
                '100': DDoSProtection,
                '101': DDoSProtection,
                '104': AuthenticationError,
                '105': AuthenticationError,
                '106': DDoSProtection,
            }, status, ExchangeError)
            message = self.safe_string(response, 'msg', self.json(response))
            raise ErrorClass(message)
        return response
