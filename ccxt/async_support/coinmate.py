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
        response = await self.privatePostBalances()
        balances = response['data']
        result = {'info': balances}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            account = self.account()
            if currency in balances:
                account['free'] = balances[currency]['available']
                account['used'] = balances[currency]['reserved']
                account['total'] = balances[currency]['balance']
            result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        response = await self.publicGetOrderBook(self.extend({
            'currencyPair': self.market_id(symbol),
            'groupByPriceLimit': 'False',
        }, params))
        orderbook = response['data']
        timestamp = orderbook['timestamp'] * 1000
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'amount')

    async def fetch_ticker(self, symbol, params={}):
        response = await self.publicGetTicker(self.extend({
            'currencyPair': self.market_id(symbol),
        }, params))
        ticker = response['data']
        timestamp = ticker['timestamp'] * 1000
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
        if not market:
            market = self.markets_by_id[trade['currencyPair']]
        return {
            'id': trade['transactionId'],
            'info': trade,
            'timestamp': trade['timestamp'],
            'datetime': self.iso8601(trade['timestamp']),
            'symbol': market['symbol'],
            'type': None,
            'side': None,
            'price': trade['price'],
            'amount': trade['amount'],
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = await self.publicGetTransactions(self.extend({
            'currencyPair': market['id'],
            'minutesIntoHistory': 10,
        }, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        method = 'privatePost' + self.capitalize(side)
        order = {
            'currencyPair': self.market_id(symbol),
        }
        if type == 'market':
            if side == 'buy':
                order['total'] = amount  # amount in fiat
            else:
                order['amount'] = amount  # amount in fiat
            method += 'Instant'
        else:
            order['amount'] = amount  # amount in crypto
            order['price'] = price
            method += self.capitalize(type)
        response = await getattr(self, method)(self.extend(order, params))
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
