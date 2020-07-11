# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired


class ice3x(Exchange):

    def describe(self):
        return self.deep_extend(super(ice3x, self).describe(), {
            'id': 'ice3x',
            'name': 'ICE3X',
            'countries': ['ZA'],  # South Africa
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'fetchCurrencies': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'fetchDepositAddress': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38012176-11616c32-3269-11e8-9f05-e65cf885bb15.jpg',
                'api': 'https://ice3x.com/api',
                'www': 'https://ice3x.com',  # 'https://ice3x.co.za',
                'doc': 'https://ice3x.co.za/ice-cubed-bitcoin-exchange-api-documentation-1-june-2017',
                'fees': [
                    'https://help.ice3.com/support/solutions/articles/11000033293-trading-fees',
                    'https://help.ice3.com/support/solutions/articles/11000033288-fees-explained',
                    'https://help.ice3.com/support/solutions/articles/11000008131-what-are-your-fiat-deposit-and-withdrawal-fees-',
                    'https://help.ice3.com/support/solutions/articles/11000033289-deposit-fees',
                ],
                'referral': 'https://ice3x.com?ref=14341802',
            },
            'api': {
                'public': {
                    'get': [
                        'currency/list',
                        'currency/info',
                        'pair/list',
                        'pair/info',
                        'stats/marketdepthfull',
                        'stats/marketdepthbtcav',
                        'stats/marketdepth',
                        'orderbook/info',
                        'trade/list',
                        'trade/info',
                    ],
                },
                'private': {
                    'post': [
                        'balance/list',
                        'balance/info',
                        'order/new',
                        'order/cancel',
                        'order/list',
                        'order/info',
                        'trade/list',
                        'trade/info',
                        'transaction/list',
                        'transaction/info',
                        'invoice/list',
                        'invoice/info',
                        'invoice/pdf',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.005,
                    'taker': 0.005,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    async def fetch_currencies(self, params={}):
        response = await self.publicGetCurrencyList(params)
        currencies = response['response']['entities']
        precision = self.precision['amount']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = self.safe_string(currency, 'currency_id')
            currencyId = self.safe_string(currency, 'iso')
            code = self.safe_currency_code(currencyId)
            result[code] = {
                'id': id,
                'code': code,
                'name': currency['name'],
                'active': True,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': currency,
                'fee': None,
            }
        return result

    async def fetch_markets(self, params={}):
        if self.currencies_by_id is None:
            self.currencies = await self.fetch_currencies()
            self.currencies_by_id = self.index_by(self.currencies, 'id')
        response = await self.publicGetPairList(params)
        markets = self.safe_value(response['response'], 'entities')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'pair_id')
            baseId = self.safe_string(market, 'currency_id_from')
            quoteId = self.safe_string(market, 'currency_id_to')
            baseCurrency = self.currencies_by_id[baseId]
            quoteCurrency = self.currencies_by_id[quoteId]
            base = baseCurrency['code']
            quote = quoteCurrency['code']
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
                'precision': self.precision,
                'limits': self.limits,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = market['symbol']
        last = self.safe_float(ticker, 'last_price')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'max'),
            'low': self.safe_float(ticker, 'min'),
            'bid': self.safe_float(ticker, 'max_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'min_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_float(ticker, 'avg'),
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'vol'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair_id': market['id'],
        }
        response = await self.publicGetStatsMarketdepthfull(self.extend(request, params))
        ticker = self.safe_value(response['response'], 'entity')
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetStatsMarketdepthfull(params)
        tickers = self.safe_value(response['response'], 'entities')
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            marketId = self.safe_string(ticker, 'pair_id')
            market = self.safe_value(self.marketsById, marketId)
            if market is not None:
                symbol = market['symbol']
                result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair_id': self.market_id(symbol),
        }
        if limit is not None:
            type = self.safe_string(params, 'type')
            if (type != 'ask') and (type != 'bid'):
                # eslint-disable-next-line quotes
                raise ArgumentsRequired(self.id + " fetchOrderBook requires an exchange-specific extra 'type' param('bid' or 'ask') when used with a limit")
            else:
                request['items_per_page'] = limit
        response = await self.publicGetOrderbookInfo(self.extend(request, params))
        orderbook = self.safe_value(response['response'], 'entities')
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'created')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'volume')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        fee = None
        feeCost = self.safe_float(trade, 'fee')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': market['quote'],
            }
        type = 'limit'
        side = self.safe_string(trade, 'type')
        id = self.safe_string(trade, 'trade_id')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair_id': market['id'],
        }
        response = await self.publicGetTradeList(self.extend(request, params))
        trades = self.safe_value(response['response'], 'entities')
        return self.parse_trades(trades, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostBalanceList(params)
        result = {'info': response}
        balances = self.safe_value(response['response'], 'entities', [])
        for i in range(0, len(balances)):
            balance = balances[i]
            # currency ids are numeric strings
            currencyId = self.safe_string(balance, 'currency_id')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_float(balance, 'balance')
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        pairId = self.safe_integer(order, 'pair_id')
        symbol = None
        if pairId and not market and (pairId in self.marketsById):
            market = self.marketsById[pairId]
            symbol = market['symbol']
        timestamp = self.safe_timestamp(order, 'created')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'volume')
        status = self.safe_integer(order, 'active')
        remaining = self.safe_float(order, 'remaining')
        filled = None
        if status == 1:
            status = 'open'
        else:
            status = 'closed'
            remaining = 0
            filled = amount
        fee = None
        feeCost = self.safe_float(order, 'fee')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
            }
            if market is not None:
                fee['currency'] = market['quote']
        return {
            'id': self.safe_string(order, 'order_id'),
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': self.safeStrin(order, 'type'),
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': fee,
            'info': order,
            'average': None,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair_id': market['id'],
            'type': side,
            'amount': amount,
            'price': price,
        }
        response = await self.privatePostOrderNew(self.extend(request, params))
        order = self.parse_order({
            'order_id': response['response']['entity']['order_id'],
            'created': self.seconds(),
            'active': 1,
            'type': side,
            'price': price,
            'volume': amount,
            'remaining': amount,
            'info': response,
        }, market)
        id = order['id']
        self.orders[id] = order
        return order

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'order_id': id,
        }
        return await self.privatePostOrderCancel(self.extend(request, params))

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order _id': id,
        }
        response = await self.privatePostOrderInfo(self.extend(request, params))
        order = self.safe_value(response['response'], 'entity')
        return self.parse_order(order)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        response = await self.privatePostOrderList(params)
        orders = self.safe_value(response['response'], 'entities')
        return self.parse_orders(orders, None, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair_id': market['id'],
        }
        if limit is not None:
            request['items_per_page'] = limit
        if since is not None:
            request['date_from'] = int(since / 1000)
        response = await self.privatePostTradeList(self.extend(request, params))
        trades = self.safe_value(response['response'], 'entities')
        return self.parse_trades(trades, market, since, limit)

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'currency_id': currency['id'],
        }
        response = await self.privatePostBalanceInfo(self.extend(request, params))
        balance = self.safe_value(response['response'], 'entity')
        address = self.safe_string(balance, 'address')
        status = 'ok' if address else 'none'
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'status': status,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'nonce': self.nonce(),
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        errors = self.safe_value(response, 'errors')
        data = self.safe_value(response, 'response')
        if errors or not data:
            authErrorKeys = ['Key', 'user_id', 'Sign']
            for i in range(0, len(authErrorKeys)):
                errorKey = authErrorKeys[i]
                errorMessage = self.safe_string(errors, errorKey)
                if not errorMessage:
                    continue
                if errorKey == 'user_id' and errorMessage.find('authorization') < 0:
                    continue
                raise AuthenticationError(errorMessage)
            raise ExchangeError(self.json(errors))
        return response
