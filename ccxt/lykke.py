# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math


class lykke (Exchange):

    def describe(self):
        return self.deep_extend(super(lykke, self).describe(), {
            'id': 'lykke',
            'name': 'Lykke',
            'countries': ['CH'],
            'version': 'v1',
            'rateLimit': 200,
            'has': {
                'CORS': False,
                'fetchOHLCV': False,
                'fetchTrades': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrder': True,
                'fetchOrders': True,
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/34487620-3139a7b0-efe6-11e7-90f5-e520cef74451.jpg',
                'api': {
                    'mobile': 'https://public-api.lykke.com/api',
                    'public': 'https://hft-api.lykke.com/api',
                    'private': 'https://hft-api.lykke.com/api',
                    'test': {
                        'mobile': 'https://public-api.lykke.com/api',
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
                        'Market/{market}',
                        'Trades/{AssetPairId}',
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
            'commonCurrencies': {
                'XPD': 'Lykke XPD',
            },
        })

    def parse_trade(self, trade, market):
        #
        #  public fetchTrades
        #
        #   {
        #     "id": "d5983ab8-e9ec-48c9-bdd0-1b18f8e80a71",
        #     "assetPairId": "BTCUSD",
        #     "dateTime": "2019-05-15T06:52:02.147Z",
        #     "volume": 0.00019681,
        #     "index": 0,
        #     "price": 8023.333,
        #     "action": "Buy"
        #   }
        #
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'AssetPairId')
            market = self.safe_value(self.markets_by_id, marketId)
        if market:
            symbol = market['symbol']
        id = self.safe_string(trade, 'id')
        timestamp = self.parse8601(self.safe_string(trade, 'dateTime'))
        side = self.safe_string_lower(trade, 'action')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'volume')
        cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'order': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100
        request = {
            'AssetPairId': market['id'],
            'skip': 0,
            'take': limit,
        }
        response = self.mobileGetTradesAssetPairId(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetWallets(params)
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'AssetId')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_float(balance, 'Balance')
            account['used'] = self.safe_float(balance, 'Reserved')
            result[code] = account
        return self.parse_balance(result)

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostOrdersIdCancel({'id': id})

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
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
        result = getattr(self, method)(self.extend(query, params))
        return {
            'id': None,
            'info': result,
        }

    def fetch_markets(self, params={}):
        markets = self.publicGetAssetPairs()
        #
        #     [{               Id: "AEBTC",
        #                      Name: "AE/BTC",
        #                  Accuracy:  6,
        #          InvertedAccuracy:  8,
        #               BaseAssetId: "6f75280b-a005-4016-a3d8-03dc644e8912",
        #            QuotingAssetId: "BTC",
        #                 MinVolume:  0.4,
        #         MinInvertedVolume:  0.0001                                 },
        #       {               Id: "AEETH",
        #                      Name: "AE/ETH",
        #                  Accuracy:  6,
        #          InvertedAccuracy:  8,
        #               BaseAssetId: "6f75280b-a005-4016-a3d8-03dc644e8912",
        #            QuotingAssetId: "ETH",
        #                 MinVolume:  0.4,
        #         MinInvertedVolume:  0.001                                  }]
        #
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'Id')
            name = self.safe_string(market, 'Name')
            baseId, quoteId = name.split('/')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'Accuracy'),
                'price': self.safe_integer(market, 'InvertedAccuracy'),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'active': True,
                'info': market,
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
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        close = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'volume24H'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        ticker = self.mobileGetMarketMarket(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def parse_order_status(self, status):
        statuses = {
            'Pending': 'open',
            'InOrderBook': 'open',
            'Processing': 'open',
            'Matched': 'closed',
            'Cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'Status'))
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'AssetPairId')
            market = self.safe_value(self.markets_by_id, marketId)
        if market:
            symbol = market['symbol']
        lastTradeTimestamp = self.parse8601(self.safe_string(order, 'LastMatchTime'))
        timestamp = None
        if ('Registered' in list(order.keys())) and(order['Registered']):
            timestamp = self.parse8601(order['Registered'])
        elif ('CreatedAt' in list(order.keys())) and(order['CreatedAt']):
            timestamp = self.parse8601(order['CreatedAt'])
        price = self.safe_float(order, 'Price')
        amount = self.safe_float(order, 'Volume')
        remaining = self.safe_float(order, 'RemainingVolume')
        filled = amount - remaining
        cost = filled * price
        id = self.safe_string(order, 'Id')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
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

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateGetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.privateGetOrders(params)
        return self.parse_orders(response, None, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'status': 'InOrderBook',
        }
        response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response, None, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'status': 'Matched',
        }
        response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response, None, since, limit)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        response = self.publicGetOrderBooksAssetPairId(self.extend({
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
        price = self.safe_float(bidask, priceKey)
        amount = self.safe_float(bidask, amountKey)
        if amount < 0:
            amount = -amount
        return [price, amount]

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'mobile':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'public':
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
