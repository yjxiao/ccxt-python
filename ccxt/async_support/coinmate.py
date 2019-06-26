# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class coinmate (Exchange):

    def describe(self):
        return self.deep_extend(super(coinmate, self).describe(), {
            'id': 'coinmate',
            'name': 'CoinMate',
            'countries': ['GB', 'CZ', 'EU'],  # UK, Czech Republic
            'rateLimit': 1000,
            'has': {
                'CORS': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27811229-c1efb510-606c-11e7-9a36-84ba2ce412d8.jpg',
                'api': 'https://coinmate.io/api',
                'www': 'https://coinmate.io',
                'fees': 'https://coinmate.io/fees',
                'doc': [
                    'https://coinmate.docs.apiary.io',
                    'https://coinmate.io/developers',
                ],
                'referral': 'https://coinmate.io?referral=YTFkM1RsOWFObVpmY1ZjMGREQmpTRnBsWjJJNVp3PT0',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'orderBook',
                        'ticker',
                        'transactions',
                        'tradingPairs',
                    ],
                },
                'private': {
                    'post': [
                        'balances',
                        'bitcoinWithdrawal',
                        'bitcoinDepositAddresses',
                        'buyInstant',
                        'buyLimit',
                        'cancelOrder',
                        'cancelOrderWithInfo',
                        'createVoucher',
                        'openOrders',
                        'redeemVoucher',
                        'sellInstant',
                        'sellLimit',
                        'transactionHistory',
                        'unconfirmedBitcoinDeposits',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.05 / 100,
                    'taker': 0.15 / 100,
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetTradingPairs(params)
        #
        #     {
        #         "error":false,
        #         "errorMessage":null,
        #         "data": [
        #             {
        #                 "name":"BTC_EUR",
        #                 "firstCurrency":"BTC",
        #                 "secondCurrency":"EUR",
        #                 "priceDecimals":2,
        #                 "lotDecimals":8,
        #                 "minAmount":0.0002,
        #                 "tradesWebSocketChannelId":"trades-BTC_EUR",
        #                 "orderBookWebSocketChannelId":"order_book-BTC_EUR",
        #                 "tradeStatisticsWebSocketChannelId":"statistics-BTC_EUR"
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data')
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = self.safe_string(market, 'name')
            baseId = self.safe_string(market, 'firstCurrency')
            quoteId = self.safe_string(market, 'secondCurrency')
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
                'active': None,
                'info': market,
                'precision': {
                    'price': self.safe_integer(market, 'priceDecimals'),
                    'amount': self.safe_integer(market, 'lotDecimals'),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'minAmount'),
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
        response = await self.privatePostBalances(params)
        balances = self.safe_value(response, 'data')
        result = {'info': response}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.common_currency_code(currencyId)
            balance = self.safe_value(balances, currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['used'] = self.safe_float(balance, 'reserved')
            account['total'] = self.safe_float(balance, 'balance')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'currencyPair': self.market_id(symbol),
            'groupByPriceLimit': 'False',
        }
        response = await self.publicGetOrderBook(self.extend(request, params))
        orderbook = response['data']
        timestamp = self.safe_integer(orderbook, 'timestamp')
        if timestamp is not None:
            timestamp *= 1000
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'amount')

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'currencyPair': self.market_id(symbol),
        }
        response = await self.publicGetTicker(self.extend(request, params))
        ticker = self.safe_value(response, 'data')
        timestamp = self.safe_integer(ticker, 'timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
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
            'vwap': None,
            'askVolume': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'amount'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'currencyPair')
            if marketId in self.markets_by_id[marketId]:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        id = self.safe_string(trade, 'transactionId')
        timestamp = self.safe_integer(trade, 'timestamp')
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
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currencyPair': market['id'],
            'minutesIntoHistory': 10,
        }
        response = await self.publicGetTransactions(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        request = {
            'currencyPair': self.market_id(symbol),
        }
        if type == 'market':
            if side == 'buy':
                request['total'] = amount  # amount in fiat
            else:
                request['amount'] = amount  # amount in fiat
            method += 'Instant'
        else:
            request['amount'] = amount  # amount in crypto
            request['price'] = price
            method += self.capitalize(type)
        response = await getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': str(response['data']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        return await self.privatePostCancelOrder({'orderId': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + self.uid + self.apiKey
            signature = self.hmac(self.encode(auth), self.encode(self.secret))
            body = self.urlencode(self.extend({
                'clientId': self.uid,
                'nonce': nonce,
                'publicKey': self.apiKey,
                'signature': signature.upper(),
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'error' in response:
            if response['error']:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
