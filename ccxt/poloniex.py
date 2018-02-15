# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OrderNotCached
from ccxt.base.errors import CancelPending
from ccxt.base.errors import ExchangeNotAvailable


class poloniex (Exchange):

    def describe(self):
        return self.deep_extend(super(poloniex, self).describe(), {
            'id': 'poloniex',
            'name': 'Poloniex',
            'countries': 'US',
            'rateLimit': 1000,  # up to 6 calls per second
            'has': {
                'createDepositAddress': True,
                'fetchDepositAddress': True,
                'CORS': False,
                'editOrder': True,
                'createMarketOrder': False,
                'fetchOHLCV': True,
                'fetchMyTrades': True,
                'fetchOrder': 'emulated',
                'fetchOrders': 'emulated',
                'fetchOpenOrders': True,
                'fetchClosedOrders': 'emulated',
                'fetchTickers': True,
                'fetchCurrencies': True,
                'withdraw': True,
            },
            'timeframes': {
                '5m': 300,
                '15m': 900,
                '30m': 1800,
                '2h': 7200,
                '4h': 14400,
                '1d': 86400,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766817-e9456312-5ee6-11e7-9b3c-b628ca5626a5.jpg',
                'api': {
                    'public': 'https://poloniex.com/public',
                    'private': 'https://poloniex.com/tradingApi',
                },
                'www': 'https://poloniex.com',
                'doc': [
                    'https://poloniex.com/support/api/',
                    'http://pastebin.com/dMX7mZE0',
                ],
                'fees': 'https://poloniex.com/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'return24hVolume',
                        'returnChartData',
                        'returnCurrencies',
                        'returnLoanOrders',
                        'returnOrderBook',
                        'returnTicker',
                        'returnTradeHistory',
                    ],
                },
                'private': {
                    'post': [
                        'buy',
                        'cancelLoanOffer',
                        'cancelOrder',
                        'closeMarginPosition',
                        'createLoanOffer',
                        'generateNewAddress',
                        'getMarginPosition',
                        'marginBuy',
                        'marginSell',
                        'moveOrder',
                        'returnActiveLoans',
                        'returnAvailableAccountBalances',
                        'returnBalances',
                        'returnCompleteBalances',
                        'returnDepositAddresses',
                        'returnDepositsWithdrawals',
                        'returnFeeInfo',
                        'returnLendingHistory',
                        'returnMarginAccountSummary',
                        'returnOpenLoanOffers',
                        'returnOpenOrders',
                        'returnOrderTrades',
                        'returnTradableBalances',
                        'returnTradeHistory',
                        'sell',
                        'toggleAutoRenew',
                        'transferBalance',
                        'withdraw',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.0015,
                    'taker': 0.0025,
                },
                'funding': {},
            },
            'limits': {
                'amount': {
                    'min': 0.00000001,
                    'max': 1000000000,
                },
                'price': {
                    'min': 0.00000001,
                    'max': 1000000000,
                },
                'cost': {
                    'min': 0.00000000,
                    'max': 1000000000,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = float(self.cost_to_precision(symbol, amount * rate))
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(self.fee_to_precision(symbol, cost)),
        }

    def common_currency_code(self, currency):
        if currency == 'BTM':
            return 'Bitmark'
        if currency == 'STR':
            return 'XLM'
        return currency

    def currency_id(self, currency):
        if currency == 'Bitmark':
            return 'BTM'
        if currency == 'XLM':
            return 'STR'
        return currency

    def parse_ohlcv(self, ohlcv, market=None, timeframe='5m', since=None, limit=None):
        return [
            ohlcv['date'] * 1000,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['volume'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if not since:
            since = 0
        request = {
            'currencyPair': market['id'],
            'period': self.timeframes[timeframe],
            'start': int(since / 1000),
        }
        if limit is not None:
            request['end'] = self.sum(request['start'], limit * self.timeframes[timeframe])
        response = self.publicGetReturnChartData(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_markets(self):
        markets = self.publicGetReturnTicker()
        keys = list(markets.keys())
        result = []
        for p in range(0, len(keys)):
            id = keys[p]
            market = markets[id]
            quote, base = id.split('_')
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            result.append(self.extend(self.fees['trading'], {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'active': True,
                'lot': self.limits['amount']['min'],
                'info': market,
            }))
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        balances = self.privatePostReturnCompleteBalances(self.extend({
            'account': 'all',
        }, params))
        result = {'info': balances}
        currencies = list(balances.keys())
        for c in range(0, len(currencies)):
            id = currencies[c]
            balance = balances[id]
            currency = self.common_currency_code(id)
            account = {
                'free': float(balance['available']),
                'used': float(balance['onOrders']),
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def fetch_fees(self, params={}):
        self.load_markets()
        fees = self.privatePostReturnFeeInfo()
        return {
            'info': fees,
            'maker': float(fees['makerFee']),
            'taker': float(fees['takerFee']),
            'withdraw': {},
            'deposit': {},
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'currencyPair': self.market_id(symbol),
        }
        if limit is not None:
            request['depth'] = limit  # 100
        orderbook = self.publicGetReturnOrderBook(self.extend(request, params))
        return self.parse_order_book(orderbook)

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

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetReturnTicker(params)
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_currencies(self, params={}):
        currencies = self.publicGetReturnCurrencies(params)
        ids = list(currencies.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            currency = currencies[id]
            # todo: will need to rethink the fees
            # to add support for multiple withdrawal/deposit methods and
            # differentiated fees for each particular method
            precision = 8  # default precision, todo: fix "magic constants"
            code = self.common_currency_code(id)
            active = (currency['delisted'] == 0)
            status = 'disabled' if (currency['disabled']) else 'ok'
            if status != 'ok':
                active = False
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': currency['name'],
                'active': active,
                'status': status,
                'fee': currency['txFee'],  # todo: redesign
                'precision': precision,
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
                        'min': currency['txFee'],
                        'max': math.pow(10, precision),
                    },
                },
            }
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        tickers = self.publicGetReturnTicker(params)
        ticker = tickers[market['id']]
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['date'])
        symbol = None
        base = None
        quote = None
        if (not market) and('currencyPair' in list(trade.keys())):
            currencyPair = trade['currencyPair']
            if currencyPair in self.markets_by_id:
                market = self.markets_by_id[currencyPair]
            else:
                parts = currencyPair.split('_')
                quote = parts[0]
                base = parts[1]
                symbol = base + '/' + quote
        if market:
            symbol = market['symbol']
            base = market['base']
            quote = market['quote']
        side = trade['type']
        fee = None
        cost = self.safe_float(trade, 'total')
        amount = float(trade['amount'])
        if 'fee' in trade:
            rate = float(trade['fee'])
            feeCost = None
            currency = None
            if side == 'buy':
                currency = base
                feeCost = amount * rate
            else:
                currency = quote
                if cost is not None:
                    feeCost = cost * rate
            fee = {
                'type': None,
                'rate': rate,
                'cost': feeCost,
                'currency': currency,
            }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': self.safe_string(trade, 'tradeID'),
            'order': self.safe_string(trade, 'orderNumber'),
            'type': 'limit',
            'side': side,
            'price': float(trade['rate']),
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currencyPair': market['id'],
        }
        if since is not None:
            request['start'] = int(since / 1000)
            request['end'] = self.seconds()  # last 50000 trades by default
        trades = self.publicGetReturnTradeHistory(self.extend(request, params))
        return self.parse_trades(trades, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol:
            market = self.market(symbol)
        pair = market['id'] if market else 'all'
        request = {'currencyPair': pair}
        if since is not None:
            request['start'] = int(since / 1000)
            request['end'] = self.seconds()
        # limit is disabled(does not really work as expected)
        # if limit:
        #     request['limit'] = int(limit)
        response = self.privatePostReturnTradeHistory(self.extend(request, params))
        result = []
        if market:
            result = self.parse_trades(response, market)
        else:
            if response:
                ids = list(response.keys())
                for i in range(0, len(ids)):
                    id = ids[i]
                    market = None
                    if id in self.markets_by_id:
                        market = self.markets_by_id[id]
                    trades = self.parse_trades(response[id], market)
                    for j in range(0, len(trades)):
                        result.append(trades[j])
        return self.filter_by_since_limit(result, since, limit)

    def parse_order(self, order, market=None):
        timestamp = self.safe_integer(order, 'timestamp')
        if not timestamp:
            timestamp = self.parse8601(order['date'])
        trades = None
        if 'resultingTrades' in order:
            trades = self.parse_trades(order['resultingTrades'], market)
        symbol = None
        if market:
            symbol = market['symbol']
        price = self.safe_float(order, 'price')
        cost = self.safe_float(order, 'total', 0.0)
        remaining = self.safe_float(order, 'amount')
        amount = self.safe_float(order, 'startingAmount', remaining)
        filled = None
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
        if filled is None:
            if trades is not None:
                filled = 0
                cost = 0
                for i in range(0, len(trades)):
                    trade = trades[i]
                    tradeAmount = trade['amount']
                    tradePrice = trade['price']
                    filled = self.sum(filled, tradeAmount)
                    cost += tradePrice * tradeAmount
        return {
            'info': order,
            'id': order['orderNumber'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'status': order['status'],
            'symbol': symbol,
            'type': order['type'],
            'side': order['side'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': None,
        }

    def parse_open_orders(self, orders, market, result=[]):
        for i in range(0, len(orders)):
            order = orders[i]
            extended = self.extend(order, {
                'status': 'open',
                'type': 'limit',
                'side': order['type'],
                'price': order['rate'],
            })
            result.append(self.parse_order(extended, market))
        return result

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol:
            market = self.market(symbol)
        pair = market['id'] if market else 'all'
        response = self.privatePostReturnOpenOrders(self.extend({
            'currencyPair': pair,
        }))
        openOrders = []
        if market:
            openOrders = self.parse_open_orders(response, market, openOrders)
        else:
            marketIds = list(response.keys())
            for i in range(0, len(marketIds)):
                marketId = marketIds[i]
                orders = response[marketId]
                m = self.markets_by_id[marketId]
                openOrders = self.parse_open_orders(orders, m, openOrders)
        for j in range(0, len(openOrders)):
            self.orders[openOrders[j]['id']] = openOrders[j]
        openOrdersIndexedById = self.index_by(openOrders, 'id')
        cachedOrderIds = list(self.orders.keys())
        result = []
        for k in range(0, len(cachedOrderIds)):
            id = cachedOrderIds[k]
            if id in openOrdersIndexedById:
                self.orders[id] = self.extend(self.orders[id], openOrdersIndexedById[id])
            else:
                order = self.orders[id]
                if order['status'] == 'open':
                    order = self.extend(order, {
                        'status': 'closed',
                        'cost': None,
                        'filled': order['amount'],
                        'remaining': 0.0,
                    })
                    if order['cost'] is None:
                        if order['filled'] is not None:
                            order['cost'] = order['filled'] * order['price']
                    self.orders[id] = order
            order = self.orders[id]
            if market:
                if order['symbol'] == symbol:
                    result.append(order)
            else:
                result.append(order)
        return self.filter_by_since_limit(result, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        since = self.safe_value(params, 'since')
        limit = self.safe_value(params, 'limit')
        request = self.omit(params, ['since', 'limit'])
        orders = self.fetch_orders(symbol, since, limit, request)
        for i in range(0, len(orders)):
            if orders[i]['id'] == id:
                return orders[i]
        raise OrderNotCached(self.id + ' order id ' + str(id) + ' is not in "open" state and not found in cache')

    def filter_orders_by_status(self, orders, status):
        result = []
        for i in range(0, len(orders)):
            if orders[i]['status'] == status:
                result.append(orders[i])
        return result

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_orders_by_status(orders, 'open')

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_orders_by_status(orders, 'closed')

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        method = 'privatePost' + self.capitalize(side)
        market = self.market(symbol)
        price = float(price)
        amount = float(amount)
        response = getattr(self, method)(self.extend({
            'currencyPair': market['id'],
            'rate': self.price_to_precision(symbol, price),
            'amount': self.amount_to_precision(symbol, amount),
        }, params))
        timestamp = self.milliseconds()
        order = self.parse_order(self.extend({
            'timestamp': timestamp,
            'status': 'open',
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
        }, response), market)
        id = order['id']
        self.orders[id] = order
        return self.extend({'info': response}, order)

    def edit_order(self, id, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        price = float(price)
        request = {
            'orderNumber': id,
            'rate': self.price_to_precision(symbol, price),
        }
        if amount is not None:
            amount = float(amount)
            request['amount'] = self.amount_to_precision(symbol, amount)
        response = self.privatePostMoveOrder(self.extend(request, params))
        result = None
        if id in self.orders:
            self.orders[id]['status'] = 'canceled'
            newid = response['orderNumber']
            self.orders[newid] = self.extend(self.orders[id], {
                'id': newid,
                'price': price,
                'status': 'open',
            })
            if amount is not None:
                self.orders[newid]['amount'] = amount
            result = self.extend(self.orders[newid], {'info': response})
        else:
            market = None
            if symbol:
                market = self.market(symbol)
            result = self.parse_order(response, market)
            self.orders[result['id']] = result
        return result

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = None
        try:
            response = self.privatePostCancelOrder(self.extend({
                'orderNumber': id,
            }, params))
        except Exception as e:
            if isinstance(e, CancelPending):
                # A request to cancel the order has been sent already.
                # If we then attempt to cancel the order the second time
                # before the first request is processed the exchange will
                # raise a CancelPending exception. Poloniex won't show the
                # order in the list of active(open) orders and the cached
                # order will be marked as 'closed'(see  #1801 for details).
                # To avoid that we proactively mark the order as 'canceled'
                # here. If for some reason the order does not get canceled
                # and still appears in the active list then the order cache
                # will eventually get back in sync on a call to `fetchOrder`.
                if id in self.orders:
                    self.orders[id]['status'] = 'canceled'
            raise e
        if id in self.orders:
            self.orders[id]['status'] = 'canceled'
        return response

    def fetch_order_status(self, id, symbol=None):
        self.load_markets()
        orders = self.fetch_open_orders(symbol)
        indexed = self.index_by(orders, 'id')
        return 'open' if (id in list(indexed.keys())) else 'closed'

    def fetch_order_trades(self, id, symbol=None, params={}):
        self.load_markets()
        trades = self.privatePostReturnOrderTrades(self.extend({
            'orderNumber': id,
        }, params))
        return self.parse_trades(trades)

    def create_deposit_address(self, currency, params={}):
        currencyId = self.currency_id(currency)
        response = self.privatePostGenerateNewAddress({
            'currency': currencyId,
        })
        address = None
        if response['success'] == 1:
            address = self.safe_string(response, 'response')
        if not address:
            raise ExchangeError(self.id + ' createDepositAddress failed: ' + self.last_http_response)
        return {
            'currency': currency,
            'address': address,
            'status': 'ok',
            'info': response,
        }

    def fetch_deposit_address(self, currency, params={}):
        response = self.privatePostReturnDepositAddresses()
        currencyId = self.currency_id(currency)
        address = self.safe_string(response, currencyId)
        status = 'ok' if address else 'none'
        return {
            'currency': currency,
            'address': address,
            'status': status,
            'info': response,
        }

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.load_markets()
        currencyId = self.currency_id(currency)
        request = {
            'currency': currencyId,
            'amount': amount,
            'address': address,
        }
        if tag:
            request['paymentId'] = tag
        result = self.privatePostWithdraw(self.extend(request, params))
        return {
            'info': result,
            'id': result['response'],
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        query = self.extend({'command': path}, params)
        if api == 'public':
            url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query['nonce'] = self.nonce()
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if body[0] == '{':
            response = json.loads(body)
            if 'error' in response:
                error = response['error']
                feedback = self.id + ' ' + self.json(response)
                if error == 'Invalid order number, or you are not the person who placed the order.':
                    raise OrderNotFound(feedback)
                elif error.find('Total must be at least') >= 0:
                    raise InvalidOrder(feedback)
                elif error.find('Not enough') >= 0:
                    raise InsufficientFunds(feedback)
                elif error.find('Nonce must be greater') >= 0:
                    raise ExchangeNotAvailable(feedback)
                elif error.find('You have already called cancelOrder or moveOrder on self order.') >= 0:
                    raise CancelPending(feedback)
                else:
                    raise ExchangeError(self.id + ': unknown error: ' + self.json(response))
