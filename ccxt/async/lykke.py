# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
import math


class lykke (Exchange):

    def describe(self):
        return self.deep_extend(super(lykke, self).describe(), {
            'id': 'lykke',
            'name': 'Lykke',
            'countries': 'CH',
            'version': 'v1',
            'rateLimit': 200,
            'has': {
                'CORS': False,
                'fetchOHLCV': False,
                'fetchTrades': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrders': True,
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/34487620-3139a7b0-efe6-11e7-90f5-e520cef74451.jpg',
                'api': {
                    'mobile': 'https://api.lykkex.com/api',
                    'public': 'https://hft-api.lykke.com/api',
                    'private': 'https://hft-api.lykke.com/api',
                    'test': {
                        'mobile': 'https://api.lykkex.com/api',
                        'public': 'https://hft-service-dev.lykkex.net/api',
                        'private': 'https://hft-service-dev.lykkex.net/api',
                    },
                },
                'www': 'https://www.lykke.com',
                'doc': [
                    'https://hft-api.lykke.com/swagger/ui/',
                    'https://www.lykke.com/lykke_api',
                ],
                'fees': 'https://www.lykke.com/trading-conditions',
            },
            'api': {
                'mobile': {
                    'get': [
                        'AllAssetPairRates/{market}',
                    ],
                },
                'public': {
                    'get': [
                        'AssetPairs',
                        'AssetPairs/{id}',
                        'IsAlive',
                        'OrderBooks',
                        'OrderBooks/{AssetPairId}',
                    ],
                },
                'private': {
                    'get': [
                        'Orders',
                        'Orders/{id}',
                        'Wallets',
                    ],
                    'post': [
                        'Orders/limit',
                        'Orders/market',
                        'Orders/{id}/Cancel',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.0,  # as of 7 Feb 2018, see https://github.com/ccxt/ccxt/issues/1863
                    'taker': 0.0,  # https://www.lykke.com/cp/wallet-fees-and-limits
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.001,
                    },
                    'deposit': {
                        'BTC': 0,
                    },
                },
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privateGetWallets()
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = balance['AssetId']
            total = balance['Balance']
            used = balance['Reserved']
            free = total - used
            result[currency] = {
                'free': free,
                'used': used,
                'total': total,
            }
        return self.parse_balance(result)

    async def cancel_order(self, id, symbol=None, params={}):
        return await self.privatePostOrdersIdCancel({'id': id})

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        query = {
            'AssetPairId': market['id'],
            'OrderAction': self.capitalize(side),
            'Volume': amount,
        }
        if type == 'market':
            query['Asset'] = market['base'] if (side == 'buy') else market['quote']
        elif type == 'limit':
            query['Price'] = price
        method = 'privatePostOrders' + self.capitalize(type)
        result = await getattr(self, method)(self.extend(query, params))
        return {
            'id': None,
            'info': result,
        }

    async def fetch_markets(self):
        markets = await self.publicGetAssetPairs()
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['Id']
            base = market['BaseAssetId']
            quote = market['QuotingAssetId']
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = market['Name']
            precision = {
                'amount': market['Accuracy'],
                'price': market['InvertedAccuracy'],
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'active': True,
                'info': market,
                'lot': math.pow(10, -precision['amount']),
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': math.pow(10, precision['amount']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': math.pow(10, precision['price']),
                    },
                },
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        ticker = ticker['Result']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': float(ticker['Rate']['Bid']),
            'bidVolume': None,
            'ask': float(ticker['Rate']['Ask']),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': None,
            'last': None,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.mobileGetAllAssetPairRatesMarket(self.extend({
            'market': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_order_status(self, status):
        if status == 'Pending':
            return 'open'
        elif status == 'InOrderBook':
            return 'open'
        elif status == 'Processing':
            return 'open'
        elif status == 'Matched':
            return 'closed'
        elif status == 'Cancelled':
            return 'canceled'
        elif status == 'NotEnoughFunds':
            return 'NotEnoughFunds'
        elif status == 'NoLiquidity':
            return 'NoLiquidity'
        elif status == 'UnknownAsset':
            return 'UnknownAsset'
        elif status == 'LeadToNegativeSpread':
            return 'LeadToNegativeSpread'
        return status

    def parse_order(self, order, market=None):
        status = self.parse_order_status(order['Status'])
        symbol = None
        if not market:
            if 'AssetPairId' in order:
                if order['AssetPairId'] in self.markets_by_id:
                    market = self.markets_by_id[order['AssetPairId']]
        if market:
            symbol = market['symbol']
        timestamp = None
        if 'LastMatchTime' in order:
            if order['LastMatchTime']:
                timestamp = self.parse8601(order['LastMatchTime'])
        elif 'Registered' in order:
            if order['Registered']:
                timestamp = self.parse8601(order['Registered'])
        elif 'CreatedAt' in order:
            if order['CreatedAt']:
                timestamp = self.parse8601(order['CreatedAt'])
        price = self.safe_float(order, 'Price')
        amount = self.safe_float(order, 'Volume')
        remaining = self.safe_float(order, 'RemainingVolume')
        filled = amount - remaining
        cost = filled * price
        result = {
            'info': order,
            'id': order['Id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
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

    async def fetch_order(self, id, symbol=None, params={}):
        response = await self.privateGetOrdersId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        response = await self.privateGetOrders()
        return self.parse_orders(response, None, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        response = await self.privateGetOrders(self.extend({
            'status': 'InOrderBook',
        }, params))
        return self.parse_orders(response, None, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        response = await self.privateGetOrders(self.extend({
            'status': 'Matched',
        }, params))
        return self.parse_orders(response, None, since, limit)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        response = await self.publicGetOrderBooksAssetPairId(self.extend({
            'AssetPairId': self.market_id(symbol),
        }, params))
        orderbook = {
            'timestamp': None,
            'bids': [],
            'asks': [],
        }
        timestamp = None
        for i in range(0, len(response)):
            side = response[i]
            if side['IsBuy']:
                orderbook['bids'] = self.array_concat(orderbook['bids'], side['Prices'])
            else:
                orderbook['asks'] = self.array_concat(orderbook['asks'], side['Prices'])
            sideTimestamp = self.parse8601(side['Timestamp'])
            timestamp = sideTimestamp if (timestamp is None) else max(timestamp, sideTimestamp)
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'Price', 'Volume')

    def parse_bid_ask(self, bidask, priceKey=0, amountKey=1):
        price = float(bidask[priceKey])
        amount = float(bidask[amountKey])
        if amount < 0:
            amount = -amount
        return [price, amount]

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            self.check_required_credentials()
            headers = {
                'api-key': self.apiKey,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
            if method == 'POST':
                if params:
                    body = self.json(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
