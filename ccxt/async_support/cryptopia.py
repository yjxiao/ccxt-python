# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import base64
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import OrderNotCached
from ccxt.base.errors import InvalidNonce


class cryptopia (Exchange):

    def describe(self):
        return self.deep_extend(super(cryptopia, self).describe(), {
            'id': 'cryptopia',
            'name': 'Cryptopia',
            'rateLimit': 1500,
            'countries': ['NZ'],  # New Zealand
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchClosedOrders': 'emulated',
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
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
                'api': {
                    'public': 'https://www.cryptopia.co.nz/api',
                    'private': 'https://www.cryptopia.co.nz/api',
                    'web': 'https://www.cryptopia.co.nz',
                },
                'www': 'https://www.cryptopia.co.nz',
                'referral': 'https://www.cryptopia.co.nz/Register?referrer=kroitor',
                'doc': [
                    'https://support.cryptopia.co.nz/csm?id=kb_article&sys_id=a75703dcdbb9130084ed147a3a9619bc',
                    'https://support.cryptopia.co.nz/csm?id=kb_article&sys_id=40e9c310dbf9130084ed147a3a9619eb',
                ],
            },
            'timeframes': {
                '15m': 15,
                '30m': 30,
                '1h': 60,
                '2h': 120,
                '4h': 240,
                '12h': 720,
                '1d': 1440,
                '1w': 10080,
            },
            'api': {
                'web': {
                    'get': [
                        'Exchange/GetTradePairChart',
                    ],
                },
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
                'BEAN': 'BITB',  # rebranding, see issue  #3380
                'BLZ': 'BlazeCoin',
                'BTG': 'Bitgem',
                'CAN': 'CanYa',
                'CAT': 'Catcoin',
                'CC': 'CCX',
                'CMT': 'Comet',
                'EPC': 'ExperienceCoin',
                'FCN': 'Facilecoin',
                'FUEL': 'FC2',  # FuelCoin != FUEL
                'HAV': 'Havecoin',
                'KARM': 'KARMA',
                'LBTC': 'LiteBitcoin',
                'LDC': 'LADACoin',
                'MARKS': 'Bitmark',
                'NET': 'NetCoin',
                'PLC': 'Polcoin',
                'RED': 'RedCoin',
                'STC': 'StopTrumpCoin',
                'QBT': 'Cubits',
                'WRC': 'WarCoin',
            },
            'options': {
                'fetchTickersErrors': True,
            },
        })

    async def fetch_markets(self):
        response = await self.publicGetGetTradePairs()
        result = []
        markets = response['Data']
        for i in range(0, len(markets)):
            market = markets[i]
            numericId = market['Id']
            # symbol = market['Label']
            baseId = market['Symbol']
            quoteId = market['BaseSymbol']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            id = baseId + '_' + quoteId
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
                'numericId': numericId,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'maker': market['TradeFee'] / 100,
                'taker': market['TradeFee'] / 100,
                'active': active,
                'precision': precision,
                'limits': limits,
            })
        self.options['marketsByLabel'] = self.index_by(result, 'label')
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        response = await self.publicGetGetMarketOrdersId(self.extend({
            'id': self.market_id(symbol),
        }, params))
        orderbook = response['Data']
        return self.parse_order_book(orderbook, None, 'Buy', 'Sell', 'Price', 'Volume')

    async def fetch_ohlcv(self, symbol, timeframe='15m', since=None, limit=None, params={}):
        dataRange = 0
        if since is not None:
            dataRanges = [
                86400,
                172800,
                604800,
                1209600,
                2592000,
                7776000,
                15552000,
            ]
            numDataRanges = len(dataRanges)
            now = self.seconds()
            sinceSeconds = int(since / 1000)
            for i in range(1, numDataRanges):
                if (now - sinceSeconds) > dataRanges[i]:
                    dataRange = i
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'tradePairId': market['numericId'],
            'dataRange': dataRange,
            'dataGroup': self.timeframes[timeframe],
        }
        response = await self.webGetExchangeGetTradePairChart(self.extend(request, params))
        candles = response['Candle']
        volumes = response['Volume']
        for i in range(0, len(candles)):
            candles[i].append(volumes[i]['basev'])
        return self.parse_ohlcvs(candles, market, timeframe, since, limit)

    def join_market_ids(self, ids, glue='-'):
        result = str(ids[0])
        for i in range(1, len(ids)):
            result += glue + str(ids[i])
        return result

    async def fetch_order_books(self, symbols=None, params={}):
        await self.load_markets()
        if symbols is None:
            raise ExchangeError(self.id + ' fetchOrderBooks requires the symbols argument as of May 2018(up to 5 symbols at max)')
        numSymbols = len(symbols)
        if numSymbols > 5:
            raise ExchangeError(self.id + ' fetchOrderBooks accepts 5 symbols at max')
        ids = self.join_market_ids(self.market_ids(symbols))
        response = await self.publicGetGetMarketOrderGroupsIds(self.extend({
            'ids': ids,
        }, params))
        orderbooks = response['Data']
        result = {}
        for i in range(0, len(orderbooks)):
            orderbook = orderbooks[i]
            id = self.safe_string(orderbook, 'Market')
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            result[symbol] = self.parse_order_book(orderbook, None, 'Buy', 'Sell', 'Price', 'Volume')
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
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

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetGetMarketId(self.extend({
            'id': market['id'],
        }, params))
        ticker = response['Data']
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetGetMarkets(params)
        result = {}
        tickers = response['Data']
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker['Label'].replace('/', '_')
            recognized = (id in list(self.markets_by_id.keys()))
            if not recognized:
                if self.options['fetchTickersErrors']:
                    raise ExchangeError(self.id + ' fetchTickers() returned unrecognized pair id ' + str(id))
            else:
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
        if market is None:
            marketId = self.safe_string(trade, 'Market')
            marketId = marketId.replace('/', '_')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        symbol = None
        fee = None
        if market is not None:
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

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
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
        response = await self.publicGetGetMarketHistoryIdHours(self.extend(request, params))
        trades = response['Data']
        return self.parse_trades(trades, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['Market'] = market['id']
        if limit is not None:
            request['Count'] = limit  # default 100
        response = await self.privatePostGetTradeHistory(self.extend(request, params))
        return self.parse_trades(response['Data'], market, since, limit)

    async def fetch_currencies(self, params={}):
        response = await self.publicGetGetCurrencies(params)
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

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetBalance(params)
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

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        market = self.market(symbol)
        # price = float(price)
        # amount = float(amount)
        request = {
            'Market': market['id'],
            'Type': self.capitalize(side),
            # 'Rate': self.price_to_precision(symbol, price),
            # 'Amount': self.amount_to_precision(symbol, amount),
            'Rate': price,
            'Amount': amount,
        }
        response = await self.privatePostSubmitTrade(self.extend(request, params))
        if not response:
            raise ExchangeError(self.id + ' createOrder returned unknown error: ' + self.json(response))
        id = None
        filled = 0.0
        status = 'open'
        if 'Data' in response:
            if 'OrderId' in response['Data']:
                if response['Data']['OrderId']:
                    id = str(response['Data']['OrderId'])
                else:
                    filled = amount
                    status = 'closed'
        order = {
            'id': id,
            'timestamp': None,
            'datetime': None,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': price * amount,
            'amount': amount,
            'remaining': amount - filled,
            'filled': filled,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }
        if id:
            self.orders[id] = order
        return self.extend({'info': response}, order)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = None
        try:
            response = await self.privatePostCancelTrade(self.extend({
                'Type': 'Trade',
                'OrderId': id,
            }, params))
            # We do not know if it is indeed canceled, but cryptopia lacks any
            # reasonable method to get information on executed or canceled order.
            if id in self.orders:
                self.orders[id]['status'] = 'canceled'
        except Exception as e:
            if self.last_json_response:
                message = self.safe_string(self.last_json_response, 'Error')
                if message:
                    if message.find('does not exist') >= 0:
                        raise OrderNotFound(self.id + ' cancelOrder() error: ' + self.last_http_response)
            raise e
        return self.parse_order(response)

    def parse_order(self, order, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        elif 'Market' in order:
            id = order['Market']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                if id in self.options['marketsByLabel']:
                    market = self.options['marketsByLabel'][id]
                    symbol = market['symbol']
        timestamp = self.safe_string(order, 'TimeStamp')
        if timestamp is not None:
            timestamp = self.parse8601(order['TimeStamp'])
        datetime = None
        if timestamp:
            datetime = self.iso8601(timestamp)
        amount = self.safe_float(order, 'Amount')
        remaining = self.safe_float(order, 'Remaining')
        filled = None
        if amount is not None and remaining is not None:
            filled = amount - remaining
        id = self.safe_value(order, 'OrderId')
        if id is not None:
            id = str(id)
        side = self.safe_string(order, 'Type')
        if side is not None:
            side = side.lower()
        return {
            'id': id,
            'info': self.omit(order, 'status'),
            'timestamp': timestamp,
            'datetime': datetime,
            'lastTradeTimestamp': None,
            'status': self.safe_string(order, 'status'),
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': self.safe_float(order, 'Rate'),
            'cost': self.safe_float(order, 'Total'),
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
        }

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {
            # 'Market': market['id'],
            # 'TradePairId': market['id'],  # Cryptopia identifier(not required if 'Market' supplied)
            # 'Count': 100,  # default = 100
        }
        if symbol is not None:
            market = self.market(symbol)
            request['Market'] = market['id']
        response = await self.privatePostGetOpenOrders(self.extend(request, params))
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
                    if (symbol is None) or (order['symbol'] == symbol):
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

    async def fetch_order(self, id, symbol=None, params={}):
        id = str(id)
        orders = await self.fetch_orders(symbol, None, None, params)
        for i in range(0, len(orders)):
            if orders[i]['id'] == id:
                return orders[i]
        raise OrderNotCached(self.id + ' order ' + id + ' not found in cached .orders, fetchOrder requires .orders(de)serialization implemented for self method to work properly')

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, params)
        result = []
        for i in range(0, len(orders)):
            if orders[i]['status'] == 'open':
                result.append(orders[i])
        return result

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, params)
        result = []
        for i in range(0, len(orders)):
            if orders[i]['status'] == 'closed':
                result.append(orders[i])
        return result

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        response = await self.privatePostGetDepositAddress(self.extend({
            'Currency': currency['id'],
        }, params))
        address = self.safe_string(response['Data'], 'BaseAddress')
        if not address:
            address = self.safe_string(response['Data'], 'Address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'info': response,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        self.check_address(address)
        request = {
            'Currency': currency['id'],
            'Amount': amount,
            'Address': address,  # Address must exist in you AddressBook in security settings
        }
        if tag:
            request['PaymentId'] = tag
        response = await self.privatePostSubmitWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': response['Data'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
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
        else:
            if query:
                url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def nonce(self):
        return self.milliseconds()

    def handle_errors(self, code, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        fixedJSONString = self.sanitize_broken_json_string(body)
        if fixedJSONString[0] == '{':
            response = json.loads(fixedJSONString)
            if 'Success' in response:
                success = self.safe_value(response, 'Success')
                if success is not None:
                    if not success:
                        error = self.safe_string(response, 'Error')
                        feedback = self.id
                        if isinstance(error, basestring):
                            feedback = feedback + ' ' + error
                            if error.find('Invalid trade amount') >= 0:
                                raise InvalidOrder(feedback)
                            if error.find('does not exist') >= 0:
                                raise OrderNotFound(feedback)
                            if error.find('Insufficient Funds') >= 0:
                                raise InsufficientFunds(feedback)
                            if error.find('Nonce has already been used') >= 0:
                                raise InvalidNonce(feedback)
                        else:
                            feedback = feedback + ' ' + fixedJSONString
                        raise ExchangeError(feedback)

    def sanitize_broken_json_string(self, jsonString):
        # sometimes cryptopia will return a unicode symbol before actual JSON string.
        indexOfBracket = jsonString.find('{')
        if indexOfBracket >= 0:
            return jsonString[indexOfBracket:]
        return jsonString

    def parse_json(self, response, responseBody, url, method):
        return super(cryptopia, self).parseJson(response, self.sanitize_broken_json_string(responseBody), url, method)
