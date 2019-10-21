# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import base64
import hashlib


class bl3p (Exchange):

    def describe(self):
        return self.deep_extend(super(bl3p, self).describe(), {
            'id': 'bl3p',
            'name': 'BL3P',
            'countries': ['NL', 'EU'],  # Netherlands, EU
            'rateLimit': 1000,
            'version': '1',
            'comment': 'An exchange market by BitonicNL',
            'has': {
                'CORS': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28501752-60c21b82-6feb-11e7-818b-055ee6d0e754.jpg',
                'api': 'https://api.bl3p.eu',
                'www': [
                    'https://bl3p.eu',
                    'https://bitonic.nl',
                ],
                'doc': [
                    'https://github.com/BitonicNL/bl3p-api/tree/master/docs',
                    'https://bl3p.eu/api',
                    'https://bitonic.nl/en/api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        '{market}/ticker',
                        '{market}/orderbook',
                        '{market}/trades',
                    ],
                },
                'private': {
                    'post': [
                        '{market}/money/depth/full',
                        '{market}/money/order/add',
                        '{market}/money/order/cancel',
                        '{market}/money/order/result',
                        '{market}/money/orders',
                        '{market}/money/orders/history',
                        '{market}/money/trades/fetch',
                        'GENMKT/money/info',
                        'GENMKT/money/deposit_address',
                        'GENMKT/money/new_deposit_address',
                        'GENMKT/money/wallet/history',
                        'GENMKT/money/withdraw',
                    ],
                },
            },
            'markets': {
                'BTC/EUR': {'id': 'BTCEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'BTC', 'quoteId': 'EUR', 'maker': 0.0025, 'taker': 0.0025},
                'LTC/EUR': {'id': 'LTCEUR', 'symbol': 'LTC/EUR', 'base': 'LTC', 'quote': 'EUR', 'baseId': 'LTC', 'quoteId': 'EUR', 'maker': 0.0025, 'taker': 0.0025},
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGENMKTMoneyInfo(params)
        data = self.safe_value(response, 'data', {})
        wallets = self.safe_value(data, 'wallets')
        result = {'info': data}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            currencyId = currency['id']
            wallet = self.safe_value(wallets, currencyId, {})
            available = self.safe_value(wallet, 'available', {})
            balance = self.safe_value(wallet, 'balance', {})
            account = self.account()
            account['free'] = self.safe_float(available, 'value')
            account['total'] = self.safe_float(balance, 'value')
            result[code] = account
        return self.parse_balance(result)

    def parse_bid_ask(self, bidask, priceKey=0, amountKey=1):
        return [
            bidask[priceKey] / 100000.0,
            bidask[amountKey] / 100000000.0,
        ]

    async def fetch_order_book(self, symbol, limit=None, params={}):
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetMarketOrderbook(self.extend(request, params))
        orderbook = self.safe_value(response, 'data')
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price_int', 'amount_int')

    async def fetch_ticker(self, symbol, params={}):
        request = {
            'market': self.market_id(symbol),
        }
        ticker = await self.publicGetMarketTicker(self.extend(request, params))
        timestamp = self.safe_timestamp(ticker, 'timestamp')
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
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker['volume'], '24h'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        id = self.safe_string(trade, 'trade_id')
        timestamp = self.safe_integer(trade, 'date')
        price = self.safe_float(trade, 'price_int')
        if price is not None:
            price /= 100000.0
        amount = self.safe_float(trade, 'amount_int')
        if amount is not None:
            amount /= 100000000.0
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = await self.publicGetMarketTrades(self.extend({
            'market': market['id'],
        }, params))
        result = self.parse_trades(response['data']['trades'], market, since, limit)
        return result

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        market = self.market(symbol)
        order = {
            'market': market['id'],
            'amount_int': int(amount * 100000000),
            'fee_currency': market['quote'],
            'type': 'bid' if (side == 'buy') else 'ask',
        }
        if type == 'limit':
            order['price_int'] = int(price * 100000.0)
        response = await self.privatePostMarketMoneyOrderAdd(self.extend(order, params))
        orderId = self.safe_string(response['data'], 'order_id')
        return {
            'info': response,
            'id': orderId,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'order_id': id,
        }
        return await self.privatePostMarketMoneyOrderCancel(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        url = self.urls['api'] + '/' + self.version + '/' + request
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({'nonce': nonce}, query))
            secret = base64.b64decode(self.secret)
            # eslint-disable-next-line quotes
            auth = request + "\0" + body
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Rest-Key': self.apiKey,
                'Rest-Sign': self.decode(signature),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
