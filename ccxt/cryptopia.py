# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OrderNotCached


class cryptopia (Exchange):

    def describe(self):
        return self.deep_extend(super(cryptopia, self).describe(), {
            'id': 'cryptopia',
            'name': 'Cryptopia',
            'rateLimit': 1500,
            'countries': 'NZ',  # New Zealand
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchClosedOrders': 'emulated',
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchMyTrades': True,
                'fetchOrder': 'emulated',
                'fetchOrderBooks': True,
                'fetchOrders': 'emulated',
                'fetchOpenOrders': True,
                'fetchTickers': True,
                'deposit': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/29484394-7b4ea6e2-84c6-11e7-83e5-1fccf4b2dc81.jpg',
                'api': 'https://www.cryptopia.co.nz/api',
                'www': 'https://www.cryptopia.co.nz',
                'doc': [
                    'https://www.cryptopia.co.nz/Forum/Category/45',
                    'https://www.cryptopia.co.nz/Forum/Thread/255',
                    'https://www.cryptopia.co.nz/Forum/Thread/256',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'GetCurrencies',
                        'GetTradePairs',
                        'GetMarkets',
                        'GetMarkets/{id}',
                        'GetMarkets/{hours}',
                        'GetMarkets/{id}/{hours}',
                        'GetMarket/{id}',
                        'GetMarket/{id}/{hours}',
                        'GetMarketHistory/{id}',
                        'GetMarketHistory/{id}/{hours}',
                        'GetMarketOrders/{id}',
                        'GetMarketOrders/{id}/{count}',
                        'GetMarketOrderGroups/{ids}',
                        'GetMarketOrderGroups/{ids}/{count}',
                    ],
                },
                'private': {
                    'post': [
                        'CancelTrade',
                        'GetBalance',
                        'GetDepositAddress',
                        'GetOpenOrders',
                        'GetTradeHistory',
                        'GetTransactions',
                        'SubmitTip',
                        'SubmitTrade',
                        'SubmitTransfer',
                        'SubmitWithdraw',
                    ],
                },
            },
            'commonCurrencies': {
                'ACC': 'AdCoin',
                'BAT': 'BatCoin',
                'BLZ': 'BlazeCoin',
                'BTG': 'Bitgem',
                'CC': 'CCX',
                'CMT': 'Comet',
                'FCN': 'Facilecoin',
                'FUEL': 'FC2',  # FuelCoin != FUEL
                'HAV': 'Havecoin',
                'LDC': 'LADACoin',
                'MARKS': 'Bitmark',
                'NET': 'NetCoin',
                'QBT': 'Cubits',
                'WRC': 'WarCoin',
            },
        })

    def fetch_markets(self):
        response = self.publicGetGetTradePairs()
        result = []
        markets = response['Data']
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['Id']
            symbol = market['Label']
            baseId = market['Symbol']
            quoteId = market['BaseSymbol']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': 8,
            }
            lot = market['MinimumTrade']
            priceLimits = {
                'min': market['MinimumPrice'],
                'max': market['MaximumPrice'],
            }
            amountLimits = {
                'min': lot,
                'max': market['MaximumTrade'],
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': {
                    'min': market['MinimumBaseTrade'],
                    'max': None,
                },
            }
            active = market['Status'] == 'OK'
            result.append({
                'id': id,
                'symbol': symbol,
                'label': market['Label'],
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'maker': market['TradeFee'] / 100,
                'taker': market['TradeFee'] / 100,
                'lot': limits['amount']['min'],
                'active': active,
                'precision': precision,
                'limits': limits,
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        response = self.publicGetGetMarketOrdersId(self.extend({
            'id': self.market_id(symbol),
        }, params))
        orderbook = response['Data']
        return self.parse_order_book(orderbook, None, 'Buy', 'Sell', 'Price', 'Volume')

    def join_market_ids(self, ids, glue='-'):
        result = str(ids[0])
        for i in range(1, len(ids)):
            result += glue + str(ids[i])
        return result

    def fetch_order_books(self, symbols=None, params={}):
        self.load_markets()
        ids = None
        if not symbols:
            numIds = len(self.ids)
            # max URL length is 2083 characters, including http schema, hostname, tld, etc...
            if numIds > 2048:
                raise ExchangeError(self.id + ' has ' + str(numIds) + ' symbols exceeding max URL length, you are required to specify a list of symbols in the first argument to fetchOrderBooks')
            ids = self.join_market_ids(self.ids)
        else:
            ids = self.join_market_ids(self.market_ids(symbols))
        response = self.publicGetGetMarketOrderGroupsIds(self.extend({
            'ids': ids,
        }, params))
        orderbooks = response['Data']
        result = {}
        for i in range(0, len(orderbooks)):
            orderbook = orderbooks[i]
            id = self.safe_integer(orderbook, 'TradePairId')
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            result[symbol] = self.parse_order_book(orderbook, None, 'Buy', 'Sell', 'Price', 'Volume')
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        open = self.safe_float(ticker, 'Open')
        last = self.safe_float(ticker, 'LastPrice')
        change = last - open
        baseVolume = self.safe_float(ticker, 'Volume')
        quoteVolume = self.safe_float(ticker, 'BaseVolume')
        vwap = None
        if quoteVolume is not None:
            if baseVolume is not None:
                if baseVolume > 0:
                    vwap = quoteVolume / baseVolume
        return {
            'symbol': symbol,
            'info': ticker,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'BidPrice'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'AskPrice'),
            'askVolume': None,
            'vwap': vwap,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': self.safe_float(ticker, 'Change'),
            'average': self.sum(last, open) / 2,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetGetMarketId(self.extend({
            'id': market['id'],
        }, params))
        ticker = response['Data']
        return self.parse_ticker(ticker, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetGetMarkets(params)
        result = {}
        tickers = response['Data']
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker['TradePairId']
            recognized = (id in list(self.markets_by_id.keys()))
            if not recognized:
                raise ExchangeError(self.id + ' fetchTickers() returned unrecognized pair id ' + str(id))
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    def parse_trade(self, trade, market=None):
        timestamp = None
        if 'Timestamp' in trade:
            timestamp = trade['Timestamp'] * 1000
        elif 'TimeStamp' in trade:
            timestamp = self.parse8601(trade['TimeStamp'])
        price = self.safe_float(trade, 'Price')
        if not price:
            price = self.safe_float(trade, 'Rate')
        cost = self.safe_float(trade, 'Total')
        id = self.safe_string(trade, 'TradeId')
        if not market:
            if 'TradePairId' in trade:
                if trade['TradePairId'] in self.markets_by_id:
                    market = self.markets_by_id[trade['TradePairId']]
        symbol = None
        fee = None
        if market:
            symbol = market['symbol']
            if 'Fee' in trade:
                fee = {
                    'currency': market['quote'],
                    'cost': trade['Fee'],
                }
        return {
            'id': id,
            'info': trade,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': trade['Type'].lower(),
            'price': price,
            'cost': cost,
            'amount': trade['Amount'],
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        hours = 24  # the default
        if since is not None:
            elapsed = self.milliseconds() - since
            hour = 1000 * 60 * 60
            hours = int(int(math.ceil(elapsed / hour)))
        request = {
            'id': market['id'],
            'hours': hours,
        }
        response = self.publicGetGetMarketHistoryIdHours(self.extend(request, params))
        trades = response['Data']
        return self.parse_trades(trades, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol:
            market = self.market(symbol)
            request['TradePairId'] = market['id']
        if limit is not None:
            request['Count'] = limit  # default 100
        response = self.privatePostGetTradeHistory(self.extend(request, params))
        return self.parse_trades(response['Data'], market, since, limit)

    def fetch_currencies(self, params={}):
        response = self.publicGetGetCurrencies(params)
        currencies = response['Data']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['Symbol']
            # todo: will need to rethink the fees
            # to add support for multiple withdrawal/deposit methods and
            # differentiated fees for each particular method
            precision = 8  # default precision, todo: fix "magic constants"
            code = self.common_currency_code(id)
            active = (currency['ListingStatus'] == 'Active')
            status = currency['Status'].lower()
            if status != 'ok':
                active = False
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': currency['Name'],
                'active': active,
                'status': status,
                'fee': currency['WithdrawFee'],
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
                        'min': currency['MinBaseTrade'],
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['MinWithdraw'],
                        'max': currency['MaxWithdraw'],
                    },
                },
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetBalance()
        balances = response['Data']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            code = balance['Symbol']
            currency = self.common_currency_code(code)
            account = {
                'free': balance['Available'],
                'used': 0.0,
                'total': balance['Total'],
            }
            account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        # price = float(price)
        # amount = float(amount)
        request = {
            'TradePairId': market['id'],
            'Type': self.capitalize(side),
            # 'Rate': self.price_to_precision(symbol, price),
            # 'Amount': self.amount_to_precision(symbol, amount),
            'Rate': price,
            'Amount': amount,
        }
        response = self.privatePostSubmitTrade(self.extend(request, params))
        if not response:
            raise ExchangeError(self.id + ' createOrder returned unknown error: ' + self.json(response))
        id = None
        filled = 0.0
        if 'Data' in response:
            if 'OrderId' in response['Data']:
                if response['Data']['OrderId']:
                    id = str(response['Data']['OrderId'])
            if 'FilledOrders' in response['Data']:
                filledOrders = response['Data']['FilledOrders']
                filledOrdersLength = len(filledOrders)
                if filledOrdersLength:
                    filled = None
        timestamp = self.milliseconds()
        order = {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': 'open',
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': price * amount,
            'amount': amount,
            'remaining': amount,
            'filled': filled,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }
        if id:
            self.orders[id] = order
        return self.extend({'info': response}, order)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = None
        try:
            response = self.privatePostCancelTrade(self.extend({
                'Type': 'Trade',
                'OrderId': id,
            }, params))
            if id in self.orders:
                self.orders[id]['status'] = 'canceled'
        except Exception as e:
            if self.last_json_response:
                message = self.safe_string(self.last_json_response, 'Error')
                if message:
                    if message.find('does not exist') >= 0:
                        raise OrderNotFound(self.id + ' cancelOrder() error: ' + self.last_http_response)
            raise e
        return response

    def parse_order(self, order, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        elif 'Market' in order:
            id = order['Market']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                if not('marketsByLabel' in list(self.options.keys())):
                    self.options['marketsByLabel'] = self.index_by(self.markets, 'label')
                if id in self.options['marketsByLabel']:
                    market = self.options['marketsByLabel'][id]
                    symbol = market['symbol']
        timestamp = self.parse8601(order['TimeStamp'])
        amount = self.safe_float(order, 'Amount')
        remaining = self.safe_float(order, 'Remaining')
        filled = amount - remaining
        return {
            'id': str(order['OrderId']),
            'info': self.omit(order, 'status'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': order['status'],
            'symbol': symbol,
            'type': 'limit',
            'side': order['Type'].lower(),
            'price': self.safe_float(order, 'Rate'),
            'cost': self.safe_float(order, 'Total'),
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {
            # 'Market': market['id'],
            # 'TradePairId': market['id'],  # Cryptopia identifier(not required if 'Market' supplied)
            # 'Count': 100,  # default = 100
        }
        if symbol is not None:
            market = self.market(symbol)
            request['TradePairId'] = market['id']
        response = self.privatePostGetOpenOrders(self.extend(request, params))
        orders = []
        for i in range(0, len(response['Data'])):
            orders.append(self.extend(response['Data'][i], {'status': 'open'}))
        openOrders = self.parse_orders(orders, market)
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
                    self.orders[id] = self.extend(order, {
                        'status': 'closed',
                        'cost': order['amount'] * order['price'],
                        'filled': order['amount'],
                        'remaining': 0.0,
                    })
            order = self.orders[id]
            if (symbol is None) or (order['symbol'] == symbol):
                result.append(order)
        return self.filter_by_since_limit(result, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        id = str(id)
        orders = self.fetch_orders(symbol, None, None, params)
        for i in range(0, len(orders)):
            if orders[i]['id'] == id:
                return orders[i]
        raise OrderNotCached(self.id + ' order ' + id + ' not found in cached .orders, fetchOrder requires .orders(de)serialization implemented for self method to work properly')

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        result = []
        for i in range(0, len(orders)):
            if orders[i]['status'] == 'open':
                result.append(orders[i])
        return result

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        result = []
        for i in range(0, len(orders)):
            if orders[i]['status'] == 'closed':
                result.append(orders[i])
        return result

    def fetch_deposit_address(self, code, params={}):
        currency = self.currency(code)
        response = self.privatePostGetDepositAddress(self.extend({
            'Currency': currency['id'],
        }, params))
        address = self.safe_string(response['Data'], 'BaseAddress')
        if not address:
            address = self.safe_string(response['Data'], 'Address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'status': 'ok',
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        currency = self.currency(code)
        self.check_address(address)
        request = {
            'Currency': currency['id'],
            'Amount': amount,
            'Address': address,  # Address must exist in you AddressBook in security settings
        }
        if tag:
            request['PaymentId'] = tag
        response = self.privatePostSubmitWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': response['Data'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            body = self.json(query, {'convertArraysToObjects': True})
            hash = self.hash(self.encode(body), 'md5', 'base64')
            secret = base64.b64decode(self.secret)
            uri = self.encode_uri_component(url)
            lowercase = uri.lower()
            hash = self.binary_to_string(hash)
            payload = self.apiKey + method + lowercase + nonce + hash
            signature = self.hmac(self.encode(payload), secret, hashlib.sha256, 'base64')
            auth = 'amx ' + self.apiKey + ':' + self.binary_to_string(signature) + ':' + nonce
            headers = {
                'Content-Type': 'application/json',
                'Authorization': auth,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if response:
            if 'Success' in response:
                if response['Success']:
                    return response
                elif 'Error' in response:
                    if response['Error'] == 'Insufficient Funds.':
                        raise InsufficientFunds(self.id + ' ' + self.json(response))
        raise ExchangeError(self.id + ' ' + self.json(response))
