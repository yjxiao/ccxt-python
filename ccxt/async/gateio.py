# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError


class gateio (Exchange):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'id': 'gateio',
            'name': 'Gate.io',
            'countries': 'CN',
            'version': '2',
            'rateLimit': 1000,
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': True,
                'withdraw': True,
                'createDepositAddress': True,
                'fetchDepositAddress': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31784029-0313c702-b509-11e7-9ccc-bc0da6a0e435.jpg',
                'api': {
                    'public': 'https://data.gate.io/api',
                    'private': 'https://data.gate.io/api',
                },
                'www': 'https://gate.io/',
                'doc': 'https://gate.io/api2',
                'fees': [
                    'https://gate.io/fee',
                    'https://support.gate.io/hc/en-us/articles/115003577673',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'pairs',
                        'marketinfo',
                        'marketlist',
                        'tickers',
                        'ticker/{id}',
                        'orderBook/{id}',
                        'trade/{id}',
                        'tradeHistory/{id}',
                        'tradeHistory/{id}/{tid}',
                    ],
                },
                'private': {
                    'post': [
                        'balances',
                        'depositAddress',
                        'newAddress',
                        'depositsWithdrawals',
                        'buy',
                        'sell',
                        'cancelOrder',
                        'cancelAllOrders',
                        'getOrder',
                        'openOrders',
                        'tradeHistory',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.002,
                    'taker': 0.002,
                },
            },
        })

    async def fetch_markets(self):
        response = await self.publicGetMarketinfo()
        markets = self.safe_value(response, 'pairs')
        if not markets:
            raise ExchangeError(self.id + ' fetchMarkets got an unrecognized response')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            keys = list(market.keys())
            id = keys[0]
            details = market[id]
            base, quote = id.split('_')
            base = base.upper()
            quote = quote.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': details['decimal_places'],
                'price': details['decimal_places'],
            }
            amountLimits = {
                'min': details['min_amount'],
                'max': None,
            }
            priceLimits = {
                'min': None,
                'max': None,
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'info': market,
                'maker': details['fee'] / 100,
                'taker': details['fee'] / 100,
                'precision': precision,
                'limits': limits,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balance = await self.privatePostBalances()
        result = {'info': balance}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            code = self.common_currency_code(currency)
            account = self.account()
            if 'available' in balance:
                if currency in balance['available']:
                    account['free'] = float(balance['available'][currency])
            if 'locked' in balance:
                if currency in balance['locked']:
                    account['used'] = float(balance['locked'][currency])
            account['total'] = self.sum(account['free'], account['used'])
            result[code] = account
        return self.parse_balance(result)

    async def perform_order_book_request(self, symbol, limit=None, params={}):
        await self.load_markets()
        orderbook = await self.publicGetOrderBookId(self.extend({
            'id': self.market_id(symbol),
        }, params))
        return orderbook

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high24hr']),
            'low': float(ticker['low24hr']),
            'bid': float(ticker['highestBid']),
            'ask': float(ticker['lowestAsk']),
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': float(ticker['last']),
            'change': float(ticker['percentChange']),
            'percentage': None,
            'average': None,
            'baseVolume': float(ticker['quoteVolume']),
            'quoteVolume': float(ticker['baseVolume']),
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
        result = {}
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            baseId, quoteId = id.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            ticker = tickers[id]
            market = None
            if symbol in self.markets:
                market = self.markets[symbol]
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetTickerId(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        # exchange reports local time(UTC+8)
        timestamp = self.parse8601(trade['date']) - 8 * 60 * 60 * 1000
        return {
            'id': trade['tradeID'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': trade['rate'],
            'amount': self.safe_float(trade, 'amount'),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTradeHistoryId(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        order = {
            'currencyPair': self.market_id(symbol),
            'rate': price,
            'amount': amount,
        }
        response = await getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': response['orderNumber'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostCancelOrder({'orderNumber': id})

    async def query_deposit_address(self, method, currency, params={}):
        method = 'privatePost' + method + 'Address'
        response = await getattr(self, method)(self.extend({
            'currency': currency,
        }, params))
        address = None
        if 'addr' in response:
            address = self.safe_string(response, 'addr')
        return {
            'currency': currency,
            'address': address,
            'status': 'ok' if (address is not None) else 'none',
            'info': response,
        }

    async def create_deposit_address(self, currency, params={}):
        return await self.query_deposit_address('New', currency, params)

    async def fetch_deposit_address(self, currency, params={}):
        return await self.query_deposit_address('Deposit', currency, params)

    async def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        response = await self.privatePostWithdraw(self.extend({
            'currency': currency.lower(),
            'amount': amount,
            'address': address,  # Address must exist in you AddressBook in security settings
        }, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        prefix = (api + '/') if (api == 'private') else ''
        url = self.urls['api'][api] + self.version + '/1/' + prefix + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            request = {'nonce': nonce}
            body = self.urlencode(self.extend(request, query))
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Key': self.apiKey,
                'Sign': signature,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'result' in response:
            if response['result'] != 'true':
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response
