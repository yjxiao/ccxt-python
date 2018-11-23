# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce


class bigone (Exchange):

    def describe(self):
        return self.deep_extend(super(bigone, self).describe(), {
            'id': 'bigone',
            'name': 'BigONE',
            'countries': ['GB'],
            'version': 'v2',
            'has': {
                'fetchTickers': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'fetchDepositAddress': True,
                'withdraw': True,
                'fetchOHLCV': False,
                'createMarketOrder': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/42803606-27c2b5ec-89af-11e8-8d15-9c8c245e8b2c.jpg',
                'api': {
                    'public': 'https://big.one/api/v2',
                    'private': 'https://big.one/api/v2/viewer',
                },
                'www': 'https://big.one',
                'doc': 'https://open.big.one/docs/api.html',
                'fees': 'https://help.big.one/hc/en-us/articles/115001933374-BigONE-Fee-Policy',
                'referral': 'https://b1.run/users/new?code=D3LLBVFT',
            },
            'api': {
                'public': {
                    'get': [
                        'ping',  # timestamp in nanoseconds
                        'markets',
                        'markets/{symbol}/depth',
                        'markets/{symbol}/trades',
                        'markets/{symbol}/ticker',
                        'orders',
                        'orders/{id}',
                        'tickers',
                        'trades',
                    ],
                },
                'private': {
                    'get': [
                        'accounts',
                        'orders',
                        'orders/{order_id}',
                        'trades',
                        'withdrawals',
                        'deposits',
                    ],
                    'post': [
                        'orders',
                        'orders/{order_id}/cancel',
                        'orders/cancel_all',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    # HARDCODING IS DEPRECATED THE FEES BELOW ARE TO BE REMOVED SOON
                    'withdraw': {
                        'BTC': 0.002,
                        'ETH': 0.01,
                        'EOS': 0.01,
                        'ZEC': 0.002,
                        'LTC': 0.01,
                        'QTUM': 0.01,
                        # 'INK': 0.01 QTUM,
                        # 'BOT': 0.01 QTUM,
                        'ETC': 0.01,
                        'GAS': 0.0,
                        'BTS': 1.0,
                        'GXS': 0.1,
                        'BITCNY': 1.0,
                    },
                },
            },
            'exceptions': {
                'codes': {
                    '401': AuthenticationError,
                    '10030': InvalidNonce,  # {"message":"invalid nonce, nonce should be a 19bits number","code":10030}
                },
                'detail': {
                    'Internal server error': ExchangeNotAvailable,
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarkets()
        markets = response['data']
        result = []
        self.options['marketsByUuid'] = {}
        for i in range(0, len(markets)):
            #
            #      {      uuid:   "550b34db-696e-4434-a126-196f827d9172",
            #        quoteScale:    3,
            #        quoteAsset: {  uuid: "17082d1c-0195-4fb6-8779-2cdbcb9eeb3c",
            #                      symbol: "USDT",
            #                        name: "TetherUS"                              },
            #              name:   "BTC-USDT",
            #         baseScale:    5,
            #         baseAsset: {  uuid: "0df9c3c3-255a-46d7-ab82-dedae169fba9",
            #                      symbol: "BTC",
            #                        name: "Bitcoin"                               }  }}
            #
            market = markets[i]
            id = market['name']
            uuid = market['uuid']
            baseId = market['baseAsset']['symbol']
            quoteId = market['quoteAsset']['symbol']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': market['baseScale'],
                'price': market['quoteScale'],
            }
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
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
                'info': market,
            }
            self.options['marketsByUuid'][uuid] = entry
            result.append(entry)
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     [
        #         {
        #             "volume": "190.4925000000000000",
        #             "open": "0.0777371200000000",
        #             "market_uuid": "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        #             "market_id": "ETH-BTC",
        #             "low": "0.0742925600000000",
        #             "high": "0.0789150000000000",
        #             "daily_change_perc": "-0.3789180767180466680525339760",
        #             "daily_change": "-0.0002945600000000",
        #             "close": "0.0774425600000000",  # last price
        #             "bid": {
        #                 "price": "0.0764777900000000",
        #                 "amount": "6.4248000000000000"
        #             },
        #             "ask": {
        #                 "price": "0.0774425600000000",
        #                 "amount": "1.1741000000000000"
        #             }
        #         }
        #     ]
        #
        if market is None:
            marketId = self.safe_string(ticker, 'market_id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.milliseconds()
        close = self.safe_float(ticker, 'close')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker['bid'], 'price'),
            'bidVolume': self.safe_float(ticker['bid'], 'amount'),
            'ask': self.safe_float(ticker['ask'], 'price'),
            'askVolume': self.safe_float(ticker['ask'], 'amount'),
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': close,
            'last': close,
            'previousClose': None,
            'change': self.safe_float(ticker, 'daily_change'),
            'percentage': self.safe_float(ticker, 'daily_change_perc'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetMarketsSymbolTicker(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(response['data'], market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTickers(params)
        tickers = response['data']
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        response = await self.publicGetMarketsSymbolDepth(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_order_book(response['data'], None, 'bids', 'asks', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        #
        #     {  node: { taker_side: "ASK",
        #                       price: "0.0694071600000000",
        #                 market_uuid: "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        #                   market_id: "ETH-BTC",
        #                 inserted_at: "2018-07-14T09:22:06Z",
        #                          id: "19913306",
        #                      amount: "0.8800000000000000"                    },
        #       cursor:   "Y3Vyc29yOnYxOjE5OTEzMzA2"                              }
        #
        node = trade['node']
        timestamp = self.parse8601(node['inserted_at'])
        price = self.safe_float(node, 'price')
        amount = self.safe_float(node, 'amount')
        if market is None:
            marketId = self.safe_string(node, 'market_id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        cost = self.cost_to_precision(symbol, price * amount)
        side = None
        if node['taker_side'] == 'ASK':
            side = 'sell'
        else:
            side = 'buy'
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(node, 'id'),
            'order': None,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'cost': float(cost),
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['first'] = limit
        response = await self.publicGetMarketsSymbolTrades(self.extend(request, params))
        #
        #     {data: {page_info: {     start_cursor: "Y3Vyc29yOnYxOjE5OTEzMzA2",
        #                            has_previous_page:  True,
        #                                has_next_page:  False,
        #                                   end_cursor: "Y3Vyc29yOnYxOjIwMDU0NzIw"  },
        #                   edges: [{  node: { taker_side: "ASK",
        #                                              price: "0.0694071600000000",
        #                                        market_uuid: "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        #                                          market_id: "ETH-BTC",
        #                                        inserted_at: "2018-07-14T09:22:06Z",
        #                                                 id: "19913306",
        #                                             amount: "0.8800000000000000"                    },
        #                              cursor:   "Y3Vyc29yOnYxOjE5OTEzMzA2"                              },
        #                            {  node: { taker_side: "ASK",
        #                                              price: "0.0694071600000000",
        #                                        market_uuid: "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        #                                          market_id: "ETH-BTC",
        #                                        inserted_at: "2018-07-14T09:22:07Z",
        #                                                 id: "19913307",
        #                                             amount: "0.3759000000000000"                    },
        #                              cursor:   "Y3Vyc29yOnYxOjE5OTEzMzA3"                              },
        #                            {  node: { taker_side: "ASK",
        #                                              price: "0.0694071600000000",
        #                                        market_uuid: "38dd30bf-76c2-4777-ae2a-a3222433eef3",
        #                                          market_id: "ETH-BTC",
        #                                        inserted_at: "2018-07-14T09:22:08Z",
        #                                                 id: "19913321",
        #                                             amount: "0.2197000000000000"                    },
        #                              cursor:   "Y3Vyc29yOnYxOjE5OTEzMzIx"                              },
        #
        return self.parse_trades(response['data']['edges'], market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccounts(params)
        #
        #     {data: [{locked_balance: "0",
        #                        balance: "0",
        #                     asset_uuid: "04479958-d7bb-40e4-b153-48bd63f2f77f",
        #                       asset_id: "NKC"                                   },
        #               {locked_balance: "0",
        #                        balance: "0",
        #                     asset_uuid: "04c8da0e-44fd-4d71-aeb0-8f4d54a4a907",
        #                       asset_id: "UBTC"                                  },
        #               {locked_balance: "0",
        #                        balance: "0",
        #                     asset_uuid: "05bc0d34-4809-4a39-a3c8-3a1851c8d224",
        #                       asset_id: "READ"                                  },
        #
        result = {'info': response}
        balances = response['data']
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['asset_id']
            code = self.common_currency_code(currencyId)
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            total = self.safe_float(balance, 'balance')
            used = self.safe_float(balance, 'locked_balance')
            free = None
            if total is not None and used is not None:
                free = total - used
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        #
        #     {
        #       "id": 10,
        #       "market_uuid": "d2185614-50c3-4588-b146-b8afe7534da6",
        #       "market_uuid": "BTC-EOS",  # not sure which one is correct
        #       "market_id": "BTC-EOS",   # not sure which one is correct
        #       "price": "10.00",
        #       "amount": "10.00",
        #       "filled_amount": "9.0",
        #       "avg_deal_price": "12.0",
        #       "side": "ASK",
        #       "state": "FILLED"
        #     }
        #
        id = self.safe_string(order, 'id')
        if market is None:
            marketId = self.safe_string(order, 'market_id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                marketUuid = self.safe_string(order, 'market_uuid')
                if marketUuid in self.options['marketsByUuid']:
                    market = self.options['marketsByUuid'][marketUuid]
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(self.safe_string(order, 'inserted_at'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'filled_amount')
        remaining = max(0, amount - filled)
        status = self.parse_order_status(self.safe_string(order, 'state'))
        side = self.safe_string(order, 'side')
        if side == 'BID':
            side = 'buy'
        else:
            side = 'sell'
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        side = 'BID' if (side == 'buy') else 'ASK'
        request = {
            'market_id': market['id'],  # market uuid d2185614-50c3-4588-b146-b8afe7534da6, required
            'side': side,  # order side one of "ASK"/"BID", required
            'amount': self.amount_to_precision(symbol, amount),  # order amount, string, required
            'price': self.price_to_precision(symbol, price),  # order price, string, required
        }
        response = await self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #       "data":
        #         {
        #           "id": 10,
        #           "market_uuid": "BTC-EOS",
        #           "price": "10.00",
        #           "amount": "10.00",
        #           "filled_amount": "9.0",
        #           "avg_deal_price": "12.0",
        #           "side": "ASK",
        #           "state": "FILLED"
        #         }
        #     }
        #
        order = self.safe_value(response, 'data')
        return self.parse_order(order, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {'order_id': id}
        response = await self.privatePostOrdersOrderIdCancel(self.extend(request, params))
        #
        #     {
        #       "data":
        #         {
        #           "id": 10,
        #           "market_uuid": "BTC-EOS",
        #           "price": "10.00",
        #           "amount": "10.00",
        #           "filled_amount": "9.0",
        #           "avg_deal_price": "12.0",
        #           "side": "ASK",
        #           "state": "FILLED"
        #         }
        #     }
        #
        order = response['data']
        return self.parse_order(order)

    async def cancel_all_orders(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.privatePostOrdersOrderIdCancel(params)
        #
        #     [
        #         {
        #             "id": 10,
        #             "market_uuid": "d2185614-50c3-4588-b146-b8afe7534da6",
        #             "price": "10.00",
        #             "amount": "10.00",
        #             "filled_amount": "9.0",
        #             "avg_deal_price": "12.0",
        #             "side": "ASK",
        #             "state": "FILLED"
        #         },
        #         {
        #             ...
        #         },
        #     ]
        #
        return self.parse_orders(response)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {'order_id': id}
        response = await self.privateGetOrdersOrderId(self.extend(request, params))
        #
        #     {
        #       "data":
        #         {
        #           "id": 10,
        #           "market_uuid": "BTC-EOS",
        #           "price": "10.00",
        #           "amount": "10.00",
        #           "filled_amount": "9.0",
        #           "avg_deal_price": "12.0",
        #           "side": "ASK",
        #           "state": "FILLED"
        #         }
        #     }
        #
        order = self.safe_value(response, 'data')
        return self.parse_order(order)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        # NAME      DESCRIPTION                                           EXAMPLE         REQUIRED
        # market_id market id                                             ETH-BTC         True
        # after     ask for the server to return orders after the cursor  dGVzdGN1cmVzZQo False
        # before    ask for the server to return orders before the cursor dGVzdGN1cmVzZQo False
        # first     slicing count                                         20              False
        # last      slicing count                                         20              False
        # side      order side one of                                     "ASK"/"BID"     False
        # state     order state one of                      "CANCELED"/"FILLED"/"PENDING" False
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market_id': market['id'],
        }
        if limit is not None:
            request['first'] = limit
        response = await self.privateGetOrders(self.extend(request, params))
        #
        #     {
        #          "data": {
        #              "edges": [
        #                  {
        #                      "node": {
        #                          "id": 10,
        #                          "market_id": "ETH-BTC",
        #                          "price": "10.00",
        #                          "amount": "10.00",
        #                          "filled_amount": "9.0",
        #                          "avg_deal_price": "12.0",
        #                          "side": "ASK",
        #                          "state": "FILLED"
        #                      },
        #                      "cursor": "dGVzdGN1cmVzZQo="
        #                  }
        #              ],
        #              "page_info": {
        #                  "end_cursor": "dGVzdGN1cmVzZQo=",
        #                  "start_cursor": "dGVzdGN1cmVzZQo=",
        #                  "has_next_page": True,
        #                  "has_previous_page": False
        #              }
        #          }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        orders = self.safe_value(data, 'edges', [])
        result = []
        for i in range(0, len(orders)):
            result.append(self.parse_order(orders[i]['node'], market))
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'PENDING': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
        }
        return self.safe_string(statuses, status)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders(symbol, since, limit, self.extend({
            'state': 'PENDING',
        }, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders(symbol, since, limit, self.extend({
            'state': 'FILLED',
        }, params))

    def nonce(self):
        return self.microseconds() * 1000

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            request = {
                'type': 'OpenAPI',
                'sub': self.apiKey,
                'nonce': nonce,
            }
            jwt = self.jwt(request, self.secret)
            headers = {
                'Authorization': 'Bearer ' + jwt,
            }
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            elif method == 'POST':
                headers['Content-Type'] = 'application/json'
                body = self.json(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response=None):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            #
            #      {"errors":{"detail":"Internal server error"}}
            #      {"errors":[{"message":"invalid nonce, nonce should be a 19bits number","code":10030}],"data":null}
            #
            error = self.safe_value(response, 'error')
            errors = self.safe_value(response, 'errors')
            data = self.safe_value(response, 'data')
            if error is not None or errors is not None or data is None:
                feedback = self.id + ' ' + self.json(response)
                code = None
                if error is not None:
                    code = self.safe_integer(error, 'code')
                exceptions = self.exceptions['codes']
                if errors is not None:
                    if isinstance(errors, list):
                        code = self.safe_string(errors[0], 'code')
                    else:
                        code = self.safe_string(errors, 'detail')
                        exceptions = self.exceptions['detail']
                if code in exceptions:
                    raise exceptions[code](feedback)
                else:
                    raise ExchangeError(feedback)
