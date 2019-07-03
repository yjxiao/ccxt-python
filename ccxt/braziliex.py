# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder


class braziliex (Exchange):

    def describe(self):
        return self.deep_extend(super(braziliex, self).describe(), {
            'id': 'braziliex',
            'name': 'Braziliex',
            'countries': ['BR'],
            'rateLimit': 1000,
            'has': {
                'fetchCurrencies': True,
                'fetchTickers': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
                'fetchDepositAddress': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/34703593-c4498674-f504-11e7-8d14-ff8e44fb78c1.jpg',
                'api': 'https://braziliex.com/api/v1',
                'www': 'https://braziliex.com/',
                'doc': 'https://braziliex.com/exchange/api.php',
                'fees': 'https://braziliex.com/exchange/fees.php',
                'referral': 'https://braziliex.com/?ref=5FE61AB6F6D67DA885BC98BA27223465',
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'ticker',
                        'ticker/{market}',
                        'orderbook/{market}',
                        'tradehistory/{market}',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'complete_balance',
                        'open_orders',
                        'trade_history',
                        'deposit_address',
                        'sell',
                        'buy',
                        'cancel_order',
                    ],
                },
            },
            'commonCurrencies': {
                'EPC': 'Epacoin',
                'ABC': 'Anti Bureaucracy Coin',
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
            'options': {
                'fetchCurrencies': {
                    'expires': 1000,  # 1 second
                },
            },
        })

    def fetch_currencies_from_cache(self, params={}):
        # self method is now redundant
        # currencies are now fetched before markets
        options = self.safe_value(self.options, 'fetchCurrencies', {})
        timestamp = self.safe_integer(options, 'timestamp')
        expires = self.safe_integer(options, 'expires', 1000)
        now = self.milliseconds()
        if (timestamp is None) or ((now - timestamp) > expires):
            response = self.publicGetCurrencies(params)
            self.options['fetchCurrencies'] = self.extend(options, {
                'response': response,
                'timestamp': now,
            })
        return self.safe_value(self.options['fetchCurrencies'], 'response')

    def fetch_currencies(self, params={}):
        response = self.fetch_currencies_from_cache(params)
        #
        #     {
        #         brl: {
        #             name: "Real",
        #             withdrawal_txFee:  0.0075,
        #             txWithdrawalFee:  9,
        #             MinWithdrawal:  30,
        #             minConf:  1,
        #             minDeposit:  0,
        #             txDepositFee:  0,
        #             txDepositPercentageFee:  0,
        #             minAmountTradeFIAT:  5,
        #             minAmountTradeBTC:  0.0001,
        #             minAmountTradeUSDT:  0.0001,
        #             decimal:  8,
        #             decimal_withdrawal:  8,
        #             active:  1,
        #             dev_active:  1,
        #             under_maintenance:  0,
        #             order: "010",
        #             is_withdrawal_active:  1,
        #             is_deposit_active:  1,
        #             is_token_erc20:  0,
        #             is_fiat:  1,
        #             gateway:  0,
        #         },
        #         btc: {
        #             name: "Bitcoin",
        #             txWithdrawalMinFee:  0.000125,
        #             txWithdrawalFee:  0.00015625,
        #             MinWithdrawal:  0.0005,
        #             minConf:  1,
        #             minDeposit:  0,
        #             txDepositFee:  0,
        #             txDepositPercentageFee:  0,
        #             minAmountTradeFIAT:  5,
        #             minAmountTradeBTC:  0.0001,
        #             minAmountTradeUSDT:  0.0001,
        #             decimal:  8,
        #             decimal_withdrawal:  8,
        #             active:  1,
        #             dev_active:  1,
        #             under_maintenance:  0,
        #             order: "011",
        #             is_withdrawal_active:  1,
        #             is_deposit_active:  1,
        #             is_token_erc20:  0,
        #             is_fiat:  0,
        #             gateway:  1,
        #         }
        #     }
        #
        self.options['currencies'] = {
            'timestamp': self.milliseconds(),
            'response': response,
        }
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            currency = response[id]
            precision = self.safe_integer(currency, 'decimal')
            code = self.safeCurrencyCode(id)
            active = self.safe_integer(currency, 'active') == 1
            maintenance = self.safe_integer(currency, 'under_maintenance')
            if maintenance != 0:
                active = False
            canWithdraw = self.safe_integer(currency, 'is_withdrawal_active') == 1
            canDeposit = self.safe_integer(currency, 'is_deposit_active') == 1
            if not canWithdraw or not canDeposit:
                active = False
            result[code] = {
                'id': id,
                'code': code,
                'name': currency['name'],
                'active': active,
                'precision': precision,
                'funding': {
                    'withdraw': {
                        'active': canWithdraw,
                        'fee': self.safe_float(currency, 'txWithdrawalFee'),
                    },
                    'deposit': {
                        'active': canDeposit,
                        'fee': self.safe_float(currency, 'txDepositFee'),
                    },
                },
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision),
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
                    'withdraw': {
                        'min': self.safe_float(currency, 'MinWithdrawal'),
                        'max': math.pow(10, precision),
                    },
                    'deposit': {
                        'min': self.safe_float(currency, 'minDeposit'),
                        'max': None,
                    },
                },
                'info': currency,
            }
        return result

    def fetch_markets(self, params={}):
        currencies = self.fetch_currencies_from_cache(params)
        response = self.publicGetTicker()
        #
        #     {
        #         btc_brl: {
        #             active: 1,
        #             market: 'btc_brl',
        #             last: 14648,
        #             percentChange: -0.95,
        #             baseVolume24: 27.856,
        #             quoteVolume24: 409328.039,
        #             baseVolume: 27.856,
        #             quoteVolume: 409328.039,
        #             highestBid24: 14790,
        #             lowestAsk24: 14450.01,
        #             highestBid: 14450.37,
        #             lowestAsk: 14699.98
        #         },
        #         ...
        #     }
        #
        ids = list(response.keys())
        result = []
        for i in range(0, len(ids)):
            id = ids[i]
            market = response[id]
            baseId, quoteId = id.split('_')
            uppercaseBaseId = baseId.upper()
            uppercaseQuoteId = quoteId.upper()
            base = self.safeCurrencyCode(uppercaseBaseId)
            quote = self.safeCurrencyCode(uppercaseQuoteId)
            symbol = base + '/' + quote
            baseCurrency = self.safe_value(currencies, baseId, {})
            quoteCurrency = self.safe_value(currencies, quoteId, {})
            quoteIsFiat = self.safe_integer(quoteCurrency, 'is_fiat', 0)
            minCost = None
            if quoteIsFiat:
                minCost = self.safe_float(baseCurrency, 'minAmountTradeFIAT')
            else:
                minCost = self.safe_float(baseCurrency, 'minAmountTrade' + uppercaseQuoteId)
            isActive = self.safe_integer(market, 'active')
            active = (isActive == 1)
            precision = {
                'amount': 8,
                'price': 8,
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
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
                        'min': minCost,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highestBid24'),
            'low': self.safe_float(ticker, 'lowestAsk24'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'percentChange'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'baseVolume24'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume24'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.publicGetTickerMarket(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetTicker(params)
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            marketId = ids[i]
            market = self.markets_by_id[marketId]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(response[marketId], market)
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'market': self.market_id(symbol),
        }
        response = self.publicGetOrderbookMarket(self.extend(request, params))
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'amount')

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string_2(trade, 'date_exec', 'date'))
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        cost = self.safe_float(trade, 'total')
        orderId = self.safe_string(trade, 'order_number')
        type = 'limit'
        side = self.safe_string(trade, 'type')
        id = self.safe_string(trade, '_id')
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': type,
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
        request = {
            'market': market['id'],
        }
        response = self.publicGetTradehistoryMarket(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        balances = self.privatePostCompleteBalance(params)
        result = {'info': balances}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            balance = balances[currencyId]
            code = self.safeCurrencyCode(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['total'] = self.safe_float(balance, 'total')
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'market')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'timestamp')
        if timestamp is None:
            timestamp = self.parse8601(self.safe_string(order, 'date'))
        price = self.safe_float(order, 'price')
        cost = self.safe_float(order, 'total', 0.0)
        amount = self.safe_float(order, 'amount')
        filledPercentage = self.safe_float(order, 'progress')
        filled = amount * filledPercentage
        remaining = float(self.amount_to_precision(symbol, amount - filled))
        info = order
        if 'info' in info:
            info = order['info']
        id = self.safe_string(order, 'order_number')
        fee = self.safe_value(order, 'fee')  # propagated from createOrder
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': 'open',
            'symbol': symbol,
            'type': 'limit',
            'side': order['type'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': fee,
            'info': info,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost' + self.capitalize(side)
        request = {
            'market': market['id'],
            # 'price': self.price_to_precision(symbol, price),
            # 'amount': self.amount_to_precision(symbol, amount),
            'price': price,
            'amount': amount,
        }
        response = getattr(self, method)(self.extend(request, params))
        success = self.safe_integer(response, 'success')
        if success != 1:
            raise InvalidOrder(self.id + ' ' + self.json(response))
        parts = response['message'].split(' / ')
        parts = parts[1:]
        feeParts = parts[5].split(' ')
        order = self.parse_order({
            'timestamp': self.milliseconds(),
            'order_number': response['order_number'],
            'type': parts[0].lower(),
            'market': parts[0].lower(),
            'amount': parts[2].split(' ')[1],
            'price': parts[3].split(' ')[1],
            'total': parts[4].split(' ')[1],
            'fee': {
                'cost': float(feeParts[1]),
                'currency': feeParts[2],
            },
            'progress': '0.0',
            'info': response,
        }, market)
        id = order['id']
        self.orders[id] = order
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_number': id,
            'market': market['id'],
        }
        return self.privatePostCancelOrder(self.extend(request, params))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.privatePostOpenOrders(self.extend(request, params))
        return self.parse_orders(response['order_open'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = self.privatePostTradeHistory(self.extend(request, params))
        return self.parse_trades(response['trade_history'], market, since, limit)

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privatePostDepositAddress(self.extend(request, params))
        address = self.safe_string(response, 'deposit_address')
        self.check_address(address)
        tag = self.safe_string(response, 'payment_id')
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + api
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            url += '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.extend({
                'command': path,
                'nonce': self.nonce(),
            }, query)
            body = self.urlencode(query)
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.decode(signature),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if (isinstance(response, basestring)) and len((response) < 1):
            raise ExchangeError(self.id + ' returned empty response')
        if 'success' in response:
            success = self.safe_integer(response, 'success')
            if success == 0:
                message = self.safe_string(response, 'message')
                if message == 'Invalid APIKey':
                    raise AuthenticationError(message)
                raise ExchangeError(message)
        return response
