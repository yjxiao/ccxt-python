# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class flowbtc(Exchange):

    def describe(self):
        return self.deep_extend(super(flowbtc, self).describe(), {
            'id': 'flowbtc',
            'name': 'flowBTC',
            'countries': ['BR'],  # Brazil
            'version': 'v1',
            'rateLimit': 1000,
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchMarkets': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87443317-01c0d080-c5fe-11ea-95c2-9ebe1a8fafd9.jpg',
                'api': 'https://publicapi.flowbtc.com.br',
                'www': 'https://www.flowbtc.com.br',
                'doc': 'https://www.flowbtc.com.br/api.html',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'post': [
                        'GetTicker',
                        'GetTrades',
                        'GetTradesByDate',
                        'GetOrderBook',
                        'GetProductPairs',
                        'GetProducts',
                    ],
                },
                'private': {
                    'post': [
                        'CreateAccount',
                        'GetUserInfo',
                        'SetUserInfo',
                        'GetAccountInfo',
                        'GetAccountTrades',
                        'GetDepositAddresses',
                        'Withdraw',
                        'CreateOrder',
                        'ModifyOrder',
                        'CancelOrder',
                        'CancelAllOrders',
                        'GetAccountOpenOrders',
                        'GetOrderFee',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.0025,
                    'taker': 0.005,
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicPostGetProductPairs(params)
        markets = self.safe_value(response, 'productPairs')
        result = {}
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'name')
            baseId = self.safe_string(market, 'product1Label')
            quoteId = self.safe_string(market, 'product2Label')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            precision = {
                'amount': self.safe_integer(market, 'product1DecimalPlaces'),
                'price': self.safe_integer(market, 'product2DecimalPlaces'),
            }
            symbol = base + '/' + quote
            result[symbol] = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
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
                'info': market,
                'active': None,
            }
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetAccountInfo(params)
        balances = self.safe_value(response, 'currencies')
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['name']
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'balance')
            account['total'] = self.safe_float(balance, 'hold')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'productPair': market['id'],
        }
        response = await self.publicPostGetOrderBook(self.extend(request, params))
        return self.parse_order_book(response, None, 'bids', 'asks', 'px', 'qty')

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'productPair': market['id'],
        }
        ticker = await self.publicPostGetTicker(self.extend(request, params))
        timestamp = self.milliseconds()
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
            'baseVolume': self.safe_float(ticker, 'volume24hr'),
            'quoteVolume': self.safe_float(ticker, 'volume24hrProduct2'),
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = self.safe_timestamp(trade, 'unixtime')
        side = 'buy' if (trade['incomingOrderSide'] == 0) else 'sell'
        id = self.safe_string(trade, 'tid')
        price = self.safe_float(trade, 'px')
        amount = self.safe_float(trade, 'qty')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': id,
            'order': None,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'takerOrMaker': None,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'ins': market['id'],
            'startIndex': -1,
        }
        response = await self.publicPostGetTrades(self.extend(request, params))
        return self.parse_trades(response['trades'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        orderType = 1 if (type == 'market') else 0
        request = {
            'ins': self.market_id(symbol),
            'side': side,
            'orderType': orderType,
            'qty': amount,
            'px': self.price_to_precision(symbol, price),
        }
        response = await self.privatePostCreateOrder(self.extend(request, params))
        return {
            'info': response,
            'id': response['serverOrderId'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        if 'ins' in params:
            request = {
                'serverOrderId': id,
            }
            return await self.privatePostCancelOrder(self.extend(request, params))
        raise ExchangeError(self.id + ' requires `ins` symbol parameter for cancelling an order')

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            if params:
                body = self.json(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            auth = str(nonce) + self.uid + self.apiKey
            signature = self.hmac(self.encode(auth), self.encode(self.secret))
            body = self.json(self.extend({
                'apiKey': self.apiKey,
                'apiNonce': nonce,
                'apiSig': signature.upper(),
            }, params))
            headers = {
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'isAccepted' in response:
            if response['isAccepted']:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))
