# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import OrderNotFound


class bitflyer(Exchange):

    def describe(self):
        return self.deep_extend(super(bitflyer, self).describe(), {
            'id': 'bitflyer',
            'name': 'bitFlyer',
            'countries': ['JP'],
            'version': 'v1',
            'rateLimit': 1000,  # their nonce-timestamp is in seconds...
            'hostname': 'bitflyer.com',  # or bitflyer.com
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': None,  # has but not fully implemented
                'future': None,  # has but not fully implemented
                'option': False,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': 'emulated',
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': 'emulated',
                'fetchOrder': 'emulated',
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPositions': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28051642-56154182-660e-11e7-9b0d-6042d1e6edd8.jpg',
                'api': 'https://api.{hostname}',
                'www': 'https://bitflyer.com',
                'doc': 'https://lightning.bitflyer.com/docs?lang=en',
            },
            'api': {
                'public': {
                    'get': [
                        'getmarkets/usa',  # new(wip)
                        'getmarkets/eu',  # new(wip)
                        'getmarkets',     # or 'markets'
                        'getboard',       # ...
                        'getticker',
                        'getexecutions',
                        'gethealth',
                        'getboardstate',
                        'getchats',
                    ],
                },
                'private': {
                    'get': [
                        'getpermissions',
                        'getbalance',
                        'getbalancehistory',
                        'getcollateral',
                        'getcollateralhistory',
                        'getcollateralaccounts',
                        'getaddresses',
                        'getcoinins',
                        'getcoinouts',
                        'getbankaccounts',
                        'getdeposits',
                        'getwithdrawals',
                        'getchildorders',
                        'getparentorders',
                        'getparentorder',
                        'getexecutions',
                        'getpositions',
                        'gettradingcommission',
                    ],
                    'post': [
                        'sendcoin',
                        'withdraw',
                        'sendchildorder',
                        'cancelchildorder',
                        'sendparentorder',
                        'cancelparentorder',
                        'cancelallchildorders',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.002'),
                    'taker': self.parse_number('0.002'),
                },
            },
        })

    def parse_expiry_date(self, expiry):
        day = expiry[0:2]
        monthName = expiry[2:5]
        year = expiry[5:9]
        months = {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12',
        }
        month = self.safe_string(months, monthName)
        return self.parse8601(year + '-' + month + '-' + day + 'T00:00:00Z')

    async def fetch_markets(self, params={}):
        jp_markets = await self.publicGetGetmarkets(params)
        #  #
        #     [
        #         # spot
        #         {
        #             "product_code": "BTC_JPY",
        #             "market_type": "Spot"
        #         },
        #         {
        #             "product_code": "BCH_BTC",
        #             "market_type": "Spot"
        #         },
        #         # forex swap
        #         {
        #             "product_code": "FX_BTC_JPY",
        #             "market_type": "FX"
        #         },
        #         # future
        #         {
        #             "product_code": "BTCJPY11FEB2022",
        #             "alias": "BTCJPY_MAT1WK",
        #             "market_type": "Futures"
        #         },
        #     ]
        #
        us_markets = await self.publicGetGetmarketsUsa(params)
        #
        #    {"product_code": "BTC_USD", "market_type": "Spot"},
        #    {"product_code": "BTC_JPY", "market_type": "Spot"}
        #
        eu_markets = await self.publicGetGetmarketsEu(params)
        #
        #    {"product_code": "BTC_EUR", "market_type": "Spot"},
        #    {"product_code": "BTC_JPY", "market_type": "Spot"}
        #
        markets = self.array_concat(jp_markets, us_markets)
        markets = self.array_concat(markets, eu_markets)
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'product_code')
            currencies = id.split('_')
            marketType = self.safe_string(market, 'market_type')
            swap = (marketType == 'FX')
            future = (marketType == 'Futures')
            spot = not swap and not future
            type = 'spot'
            settle = None
            baseId = None
            quoteId = None
            expiry = None
            if spot:
                baseId = self.safe_string(currencies, 0)
                quoteId = self.safe_string(currencies, 1)
            elif swap:
                type = 'swap'
                baseId = self.safe_string(currencies, 1)
                quoteId = self.safe_string(currencies, 2)
            elif future:
                alias = self.safe_string(market, 'alias')
                splitAlias = alias.split('_')
                currencyIds = self.safe_string(splitAlias, 0)
                baseId = currencyIds[0:-3]
                quoteId = currencyIds[-3:]
                splitId = id.split(currencyIds)
                expiryDate = self.safe_string(splitId, 1)
                expiry = self.parse_expiry_date(expiryDate)
                type = 'future'
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            taker = self.fees['trading']['taker']
            maker = self.fees['trading']['maker']
            contract = swap or future
            if contract:
                maker = 0.0
                taker = 0.0
                settle = 'JPY'
                symbol = symbol + ':' + settle
                if future:
                    symbol = symbol + '-' + self.yymmdd(expiry)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'settle': settle,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': type,
                'spot': spot,
                'margin': False,
                'swap': swap,
                'future': future,
                'option': False,
                'active': True,
                'contract': contract,
                'linear': None if spot else True,
                'inverse': None if spot else False,
                'taker': taker,
                'maker': maker,
                'contractSize': None,
                'expiry': expiry,
                'expiryDatetime': self.iso8601(expiry),
                'strike': None,
                'optionType': None,
                'precision': {
                    'price': None,
                    'amount': None,
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
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
            })
        return result

    def parse_balance(self, response):
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_string(balance, 'amount')
            account['free'] = self.safe_string(balance, 'available')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetGetbalance(params)
        #
        #     [
        #         {
        #             "currency_code": "JPY",
        #             "amount": 1024078,
        #             "available": 508000
        #         },
        #         {
        #             "currency_code": "BTC",
        #             "amount": 10.24,
        #             "available": 4.12
        #         },
        #         {
        #             "currency_code": "ETH",
        #             "amount": 20.48,
        #             "available": 16.38
        #         }
        #     ]
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
        }
        orderbook = await self.publicGetGetboard(self.extend(request, params))
        return self.parse_order_book(orderbook, symbol, None, 'bids', 'asks', 'price', 'size')

    def parse_ticker(self, ticker, market=None):
        symbol = self.safe_symbol(None, market)
        timestamp = self.parse8601(self.safe_string(ticker, 'timestamp'))
        last = self.safe_string(ticker, 'ltp')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_string(ticker, 'best_bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'best_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume_by_product'),
            'quoteVolume': None,
            'info': ticker,
        }, market, False)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        response = await self.publicGetGetticker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public) v1
        #
        #     {
        #          "id":2278466664,
        #          "side":"SELL",
        #          "price":56810.7,
        #          "size":0.08798,
        #          "exec_date":"2021-11-19T11:46:39.323",
        #          "buy_child_order_acceptance_id":"JRF20211119-114209-236525",
        #          "sell_child_order_acceptance_id":"JRF20211119-114639-236919"
        #      }
        #
        #      {
        #          "id":2278463423,
        #          "side":"BUY",
        #          "price":56757.83,
        #          "size":0.6003,"exec_date":"2021-11-19T11:28:00.523",
        #          "buy_child_order_acceptance_id":"JRF20211119-112800-236526",
        #          "sell_child_order_acceptance_id":"JRF20211119-112734-062017"
        #      }
        #
        #
        #
        side = self.safe_string_lower(trade, 'side')
        if side is not None:
            if len(side) < 1:
                side = None
        order = None
        if side is not None:
            id = side + '_child_order_acceptance_id'
            if id in trade:
                order = trade[id]
        if order is None:
            order = self.safe_string(trade, 'child_order_acceptance_id')
        timestamp = self.parse8601(self.safe_string(trade, 'exec_date'))
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'size')
        id = self.safe_string(trade, 'id')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': order,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': None,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        response = await self.publicGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_type': type.upper(),
            'side': side.upper(),
            'price': price,
            'size': amount,
        }
        result = await self.privatePostSendchildorder(self.extend(request, params))
        # {"status": - 200, "error_message": "Insufficient funds", "data": null}
        id = self.safe_string(result, 'child_order_acceptance_id')
        return {
            'info': result,
            'id': id,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a `symbol` argument')
        await self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_acceptance_id': id,
        }
        return await self.privatePostCancelchildorder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'ACTIVE': 'open',
            'COMPLETED': 'closed',
            'CANCELED': 'canceled',
            'EXPIRED': 'canceled',
            'REJECTED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(self.safe_string(order, 'child_order_date'))
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'size')
        filled = self.safe_string(order, 'executed_size')
        remaining = self.safe_string(order, 'outstanding_size')
        status = self.parse_order_status(self.safe_string(order, 'child_order_state'))
        type = self.safe_string_lower(order, 'child_order_type')
        side = self.safe_string_lower(order, 'side')
        marketId = self.safe_string(order, 'product_code')
        symbol = self.safe_symbol(marketId, market)
        fee = None
        feeCost = self.safe_number(order, 'total_commission')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
                'rate': None,
            }
        id = self.safe_string(order, 'child_order_acceptance_id')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
            'average': None,
            'trades': None,
        }, market)

    async def fetch_orders(self, symbol=None, since=None, limit=100, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
            'count': limit,
        }
        response = await self.privateGetGetchildorders(self.extend(request, params))
        orders = self.parse_orders(response, market, since, limit)
        if symbol is not None:
            orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    async def fetch_open_orders(self, symbol=None, since=None, limit=100, params={}):
        request = {
            'child_order_state': 'ACTIVE',
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=100, params={}):
        request = {
            'child_order_state': 'COMPLETED',
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a `symbol` argument')
        orders = await self.fetch_orders(symbol)
        ordersById = self.index_by(orders, 'id')
        if id in ordersById:
            return ordersById[id]
        raise OrderNotFound(self.id + ' No order found with id ' + id)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        response = await self.privateGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_positions(self, symbols=None, params={}):
        if symbols is None:
            raise ArgumentsRequired(self.id + ' fetchPositions() requires a `symbols` argument, exactly one symbol in an array')
        await self.load_markets()
        request = {
            'product_code': self.market_ids(symbols),
        }
        response = await self.privateGetpositions(self.extend(request, params))
        #
        #     [
        #         {
        #             "product_code": "FX_BTC_JPY",
        #             "side": "BUY",
        #             "price": 36000,
        #             "size": 10,
        #             "commission": 0,
        #             "swap_point_accumulate": -35,
        #             "require_collateral": 120000,
        #             "open_date": "2015-11-03T10:04:45.011",
        #             "leverage": 3,
        #             "pnl": 965,
        #             "sfd": -0.5
        #         }
        #     ]
        #
        # todo unify parsePosition/parsePositions
        return response

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        if code != 'JPY' and code != 'USD' and code != 'EUR':
            raise ExchangeError(self.id + ' allows withdrawing JPY, USD, EUR only, ' + code + ' is not supported')
        currency = self.currency(code)
        request = {
            'currency_code': currency['id'],
            'amount': amount,
            # 'bank_account_id': 1234,
        }
        response = await self.privatePostWithdraw(self.extend(request, params))
        id = self.safe_string(response, 'message_id')
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/'
        if api == 'private':
            request += 'me/'
        request += path
        if method == 'GET':
            if params:
                request += '?' + self.urlencode(params)
        baseUrl = self.implode_hostname(self.urls['api'])
        url = baseUrl + request
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = ''.join([nonce, method, request])
            if params:
                if method != 'GET':
                    body = self.json(params)
                    auth += body
            headers = {
                'ACCESS-KEY': self.apiKey,
                'ACCESS-TIMESTAMP': nonce,
                'ACCESS-SIGN': self.hmac(self.encode(auth), self.encode(self.secret)),
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
