# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import InvalidNonce


class bitbay (Exchange):

    def describe(self):
        return self.deep_extend(super(bitbay, self).describe(), {
            'id': 'bitbay',
            'name': 'BitBay',
            'countries': ['MT', 'EU'],  # Malta
            'rateLimit': 1000,
            'has': {
                'CORS': True,
                'withdraw': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'referral': 'https://auth.bitbay.net/ref/jHlbB4mIkdS1',
                'logo': 'https://user-images.githubusercontent.com/1294454/27766132-978a7bd8-5ece-11e7-9540-bc96d1e9bbb8.jpg',
                'www': 'https://bitbay.net',
                'api': {
                    'public': 'https://bitbay.net/API/Public',
                    'private': 'https://bitbay.net/API/Trading/tradingApi.php',
                    'v1_01Public': 'https://api.bitbay.net/rest',
                    'v1_01Private': 'https://api.bitbay.net/rest',
                },
                'doc': [
                    'https://bitbay.net/public-api',
                    'https://bitbay.net/en/private-api',
                    'https://bitbay.net/account/tab-api',
                    'https://github.com/BitBayNet/API',
                    'https://docs.bitbay.net/v1.0.1-en/reference',
                ],
                'fees': 'https://bitbay.net/en/fees',
            },
            'api': {
                'public': {
                    'get': [
                        '{id}/all',
                        '{id}/market',
                        '{id}/orderbook',
                        '{id}/ticker',
                        '{id}/trades',
                    ],
                },
                'private': {
                    'post': [
                        'info',
                        'trade',
                        'cancel',
                        'orderbook',
                        'orders',
                        'transfer',
                        'withdraw',
                        'history',
                        'transactions',
                    ],
                },
                'v1_01Public': {
                    'get': [
                        'trading/ticker',
                        'trading/ticker/{symbol}',
                        'trading/stats',
                        'trading/orderbook/{symbol}',
                        'trading/transactions/{symbol}',
                        'trading/candle/history/{symbol}/{resolution}',
                    ],
                },
                'v1_01Private': {
                    'get': [
                        'payments/withdrawal/{detailId}',
                        'payments/deposit/{detailId}',
                        'trading/offer',
                        'trading/config/{symbol}',
                        'trading/history/transactions',
                        'balances/BITBAY/history',
                        'balances/BITBAY/balance',
                        'fiat_cantor/rate/{baseId}/{quoteId}',
                        'fiat_cantor/history',
                    ],
                    'post': [
                        'trading/offer/{symbol}',
                        'trading/config/{symbol}',
                        'balances/BITBAY/balance',
                        'balances/BITBAY/balance/transfer/{source}/{destination}',
                        'fiat_cantor/exchange',
                    ],
                    'delete': [
                        'trading/offer/{symbol}/{id}/{side}/{price}',
                    ],
                    'put': [
                        'balances/BITBAY/balance/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.3 / 100,
                    'taker': 0.0043,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.0009,
                        'LTC': 0.005,
                        'ETH': 0.00126,
                        'LSK': 0.2,
                        'BCH': 0.0006,
                        'GAME': 0.005,
                        'DASH': 0.001,
                        'BTG': 0.0008,
                        'PLN': 4,
                        'EUR': 1.5,
                    },
                },
            },
            'exceptions': {
                '400': ExchangeError,  # At least one parameter wasn't set
                '401': InvalidOrder,  # Invalid order type
                '402': InvalidOrder,  # No orders with specified currencies
                '403': InvalidOrder,  # Invalid payment currency name
                '404': InvalidOrder,  # Error. Wrong transaction type
                '405': InvalidOrder,  # Order with self id doesn't exist
                '406': InsufficientFunds,  # No enough money or crypto
                # code 407 not specified are not specified in their docs
                '408': InvalidOrder,  # Invalid currency name
                '501': AuthenticationError,  # Invalid public key
                '502': AuthenticationError,  # Invalid sign
                '503': InvalidNonce,  # Invalid moment parameter. Request time doesn't match current server time
                '504': ExchangeError,  # Invalid method
                '505': AuthenticationError,  # Key has no permission for self action
                '506': AuthenticationError,  # Account locked. Please contact with customer service
                # codes 507 and 508 are not specified in their docs
                '509': ExchangeError,  # The BIC/SWIFT is required for self currency
                '510': ExchangeError,  # Invalid market name
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.v1_01PublicGetTradingTicker(params)
        #
        #     {
        #         status: 'Ok',
        #         items: {
        #             'BSV-USD': {
        #                 market: {
        #                     code: 'BSV-USD',
        #                     first: {currency: 'BSV', minOffer: '0.00035', scale: 8},
        #                     second: {currency: 'USD', minOffer: '5', scale: 2}
        #                 },
        #                 time: '1557569762154',
        #                 highestBid: '52.31',
        #                 lowestAsk: '62.99',
        #                 rate: '63',
        #                 previousRate: '51.21',
        #             },
        #         },
        #     }
        #
        result = []
        items = self.safe_value(response, 'items')
        keys = list(items.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            item = items[key]
            market = self.safe_value(item, 'market', {})
            first = self.safe_value(market, 'first', {})
            second = self.safe_value(market, 'second', {})
            baseId = self.safe_string(first, 'currency')
            quoteId = self.safe_string(second, 'currency')
            id = baseId + quoteId
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(first, 'scale'),
                'price': self.safe_integer(second, 'scale'),
            }
            # todo: check that the limits have ben interpreted correctly
            # todo: parse the fees page
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'active': None,
                'fee': None,
                'limits': {
                    'amount': {
                        'min': self.safe_float(first, 'minOffer'),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': self.safe_float(second, 'minOffer'),
                        'max': None,
                    },
                },
                'info': item,
            })
        return result

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        markets = [self.market_id(symbol)] if symbol else []
        request = {
            'markets': markets,
        }
        response = await self.v1_01PrivateGetTradingHistoryTransactions(self.extend({'query': self.json(request)}, params))
        #
        #     {
        #         status: 'Ok',
        #         totalRows: '67',
        #         items: [
        #             {
        #                 id: 'b54659a0-51b5-42a0-80eb-2ac5357ccee2',
        #                 market: 'BTC-EUR',
        #                 time: '1541697096247',
        #                 amount: '0.00003',
        #                 rate: '4341.44',
        #                 initializedBy: 'Sell',
        #                 wasTaker: False,
        #                 userAction: 'Buy',
        #                 offerId: 'bd19804a-6f89-4a69-adb8-eb078900d006',
        #                 commissionValue: null
        #             },
        #         ]
        #     }
        #
        items = self.safe_value(response, 'items')
        result = self.parse_trades(items, None, since, limit)
        if symbol is None:
            return result
        return self.filter_by_symbol(result, symbol)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostInfo(params)
        balances = self.safe_value(response, 'balances')
        if balances is None:
            raise ExchangeError(self.id + ' empty balance response ' + self.json(response))
        result = {'info': response}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            # rewrite with safeCurrencyCode, traverse by currency ids
            currencyId = self.currencyId(code)
            balance = self.safe_value(balances, currencyId)
            if balance is not None:
                account = self.account()
                account['free'] = self.safe_float(balance, 'available')
                account['used'] = self.safe_float(balance, 'locked')
                result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        orderbook = await self.publicGetIdOrderbook(self.extend(request, params))
        return self.parse_order_book(orderbook)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        ticker = await self.publicGetIdTicker(self.extend(request, params))
        timestamp = self.milliseconds()
        baseVolume = self.safe_float(ticker, 'volume')
        vwap = self.safe_float(ticker, 'vwap')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'max'),
            'low': self.safe_float(ticker, 'min'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_float(ticker, 'average'),
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        if 'tid' in trade:
            return self.parse_public_trade(trade, market)
        else:
            return self.parse_my_trade(trade, market)

    def parse_my_trade(self, trade, market):
        #
        #     {
        #         id: '5b6780e2-5bac-4ac7-88f4-b49b5957d33a',
        #         market: 'BTC-EUR',
        #         time: '1520719374684',
        #         amount: '0.3',
        #         rate: '7502',
        #         initializedBy: 'Sell',
        #         wasTaker: True,
        #         userAction: 'Sell',
        #         offerId: 'd093b0aa-b9c9-4a52-b3e2-673443a6188b',
        #         commissionValue: null
        #     }
        #
        timestamp = self.safe_integer(trade, 'time')
        userAction = self.safe_string(trade, 'userAction')
        side = 'buy' if (userAction == 'Buy') else 'sell'
        wasTaker = self.safe_value(trade, 'wasTaker')
        takerOrMaker = 'taker' if wasTaker else 'maker'
        price = self.safe_float(trade, 'rate')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        commissionValue = self.safe_float(trade, 'commissionValue')
        fee = None
        if commissionValue is not None:
            # it always seems to be null so don't know what currency to use
            fee = {
                'currency': None,
                'cost': commissionValue,
            }
        marketId = self.safe_string(trade, 'market')
        order = self.safe_string(trade, 'offerId')
        # todo: check self logic
        type = 'limit' if order else 'market'
        return {
            'id': self.safe_string(trade, 'id'),
            'order': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': self.find_symbol(marketId.replace('-', '')),
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'takerOrMaker': takerOrMaker,
            'fee': fee,
            'info': trade,
        }

    def parse_public_trade(self, trade, market=None):
        #
        #     {
        #         "date":1459608665,
        #         "price":0.02722571,
        #         "type":"sell",
        #         "amount":1.08112001,
        #         "tid":"0"
        #     }
        #
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is not None:
            timestamp *= 1000
        id = self.safe_string(trade, 'tid')
        type = None
        side = self.safe_string(trade, 'type')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
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
            'id': market['id'],
        }
        response = await self.publicGetIdTrades(self.extend(request, params))
        #
        #     [
        #         {
        #             "date":1459608665,
        #             "price":0.02722571,
        #             "type":"sell",
        #             "amount":1.08112001,
        #             "tid":"0"
        #         },
        #         {
        #             "date":1459698930,
        #             "price":0.029,
        #             "type":"buy",
        #             "amount":0.444188,
        #             "tid":"1"
        #         },
        #         {
        #             "date":1459726670,
        #             "price":0.029,
        #             "type":"buy",
        #             "amount":0.25459599,
        #             "tid":"2"
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        market = self.market(symbol)
        request = {
            'type': side,
            'currency': market['baseId'],
            'amount': amount,
            'payment_currency': market['quoteId'],
            'rate': price,
        }
        return await self.privatePostTrade(self.extend(request, params))

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'id': id,
        }
        return await self.privatePostCancel(self.extend(request, params))

    def is_fiat(self, currency):
        fiatCurrencies = {
            'USD': True,
            'EUR': True,
            'PLN': True,
        }
        return self.safe_value(fiatCurrencies, currency, False)

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        method = None
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'quantity': amount,
        }
        if self.is_fiat(code):
            method = 'privatePostWithdraw'
            # request['account'] = params['account']  # they demand an account number
            # request['express'] = params['express']  # whatever it means, they don't explain
            # request['bic'] = ''
        else:
            method = 'privatePostTransfer'
            if tag is not None:
                address += '?dt=' + str(tag)
            request['address'] = address
        response = await getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            query = self.omit(params, self.extract_params(path))
            url += '/' + self.implode_params(path, params) + '.json'
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'v1_01Public':
            query = self.omit(params, self.extract_params(path))
            url += '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'v1_01Private':
            self.check_required_credentials()
            query = self.omit(params, self.extract_params(path))
            url += '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
            nonce = self.milliseconds()
            payload = self.apiKey + nonce
            if body is not None:
                body = self.json(body)
            headers = {
                'Request-Timestamp': nonce,
                'Operation-Id': self.uuid(),
                'API-Key': self.apiKey,
                'API-Hash': self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha512),
                'Content-Type': 'application/json',
            }
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'method': path,
                'moment': self.nonce(),
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'API-Key': self.apiKey,
                'API-Hash': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None:
            return  # fallback to default error handler
        if 'code' in response:
            #
            # bitbay returns the integer 'success': 1 key from their private API
            # or an integer 'code' value from 0 to 510 and an error message
            #
            #      {'success': 1, ...}
            #      {'code': 502, 'message': 'Invalid sign'}
            #      {'code': 0, 'message': 'offer funds not exceeding minimums'}
            #
            #      400 At least one parameter wasn't set
            #      401 Invalid order type
            #      402 No orders with specified currencies
            #      403 Invalid payment currency name
            #      404 Error. Wrong transaction type
            #      405 Order with self id doesn't exist
            #      406 No enough money or crypto
            #      408 Invalid currency name
            #      501 Invalid public key
            #      502 Invalid sign
            #      503 Invalid moment parameter. Request time doesn't match current server time
            #      504 Invalid method
            #      505 Key has no permission for self action
            #      506 Account locked. Please contact with customer service
            #      509 The BIC/SWIFT is required for self currency
            #      510 Invalid market name
            #
            code = self.safe_string(response, 'code')  # always an integer
            feedback = self.id + ' ' + body
            exceptions = self.exceptions
            if code in self.exceptions:
                raise exceptions[code](feedback)
            else:
                raise ExchangeError(feedback)
