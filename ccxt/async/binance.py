# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection


class binance (Exchange):

    def describe(self):
        return self.deep_extend(super(binance, self).describe(), {
            'id': 'binance',
            'name': 'Binance',
            'countries': 'JP',  # Japan
            'rateLimit': 500,
            # new metainfo interface
            'has': {
                'fetchDepositAddress': True,
                'CORS': False,
                'fetchBidsAsks': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg',
                'api': {
                    'web': 'https://www.binance.com',
                    'wapi': 'https://api.binance.com/wapi/v3',
                    'public': 'https://api.binance.com/api/v1',
                    'private': 'https://api.binance.com/api/v3',
                    'v3': 'https://api.binance.com/api/v3',
                    'v1': 'https://api.binance.com/api/v1',
                },
                'www': 'https://www.binance.com',
                'doc': 'https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md',
                'fees': [
                    'https://binance.zendesk.com/hc/en-us/articles/115000429332',
                    'https://support.binance.com/hc/en-us/articles/115000583311',
                ],
            },
            'api': {
                'web': {
                    'get': [
                        'exchange/public/product',
                    ],
                },
                'wapi': {
                    'post': [
                        'withdraw',
                    ],
                    'get': [
                        'depositHistory',
                        'withdrawHistory',
                        'depositAddress',
                        'accountStatus',
                        'systemStatus',
                    ],
                },
                'v3': {
                    'get': [
                        'ticker/price',
                        'ticker/bookTicker',
                    ],
                },
                'public': {
                    'get': [
                        'exchangeInfo',
                        'ping',
                        'time',
                        'depth',
                        'aggTrades',
                        'klines',
                        'ticker/24hr',
                        'ticker/allPrices',
                        'ticker/allBookTickers',
                        'ticker/price',
                        'ticker/bookTicker',
                    ],
                },
                'private': {
                    'get': [
                        'order',
                        'openOrders',
                        'allOrders',
                        'account',
                        'myTrades',
                    ],
                    'post': [
                        'order',
                        'order/test',
                    ],
                    'delete': [
                        'order',
                    ],
                },
                'v1': {
                    'put': ['userDataStream'],
                    'post': ['userDataStream'],
                    'delete': ['userDataStream'],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'ADA': 1.0,
                        'ADX': 4.7,
                        'AION': 1.9,
                        'AMB': 11.4,
                        'APPC': 6.5,
                        'ARK': 0.1,
                        'ARN': 3.1,
                        'AST': 10.0,
                        'BAT': 18.0,
                        'BCD': 1.0,
                        'BCH': 0.001,
                        'BCPT': 10.2,
                        'BCX': 1.0,
                        'BNB': 0.7,
                        'BNT': 1.5,
                        'BQX': 1.6,
                        'BRD': 6.4,
                        'BTC': 0.001,
                        'BTG': 0.001,
                        'BTM': 5.0,
                        'BTS': 1.0,
                        'CDT': 67.0,
                        'CMT': 37.0,
                        'CND': 47.0,
                        'CTR': 5.4,
                        'DASH': 0.002,
                        'DGD': 0.06,
                        'DLT': 11.7,
                        'DNT': 51.0,
                        'EDO': 2.5,
                        'ELF': 6.5,
                        'ENG': 2.1,
                        'ENJ': 42.0,
                        'EOS': 1.0,
                        'ETC': 0.01,
                        'ETF': 1.0,
                        'ETH': 0.01,
                        'EVX': 2.5,
                        'FUEL': 45.0,
                        'FUN': 85.0,
                        'GAS': 0,
                        'GTO': 20.0,
                        'GVT': 0.53,
                        'GXS': 0.3,
                        'HCC': 0.0005,
                        'HSR': 0.0001,
                        'ICN': 3.5,
                        'ICX': 1.3,
                        'INS': 1.5,
                        'IOTA': 0.5,
                        'KMD': 0.002,
                        'KNC': 2.6,
                        'LEND': 54.0,
                        'LINK': 12.8,
                        'LLT': 54.0,
                        'LRC': 9.1,
                        'LSK': 0.1,
                        'LTC': 0.01,
                        'LUN': 0.29,
                        'MANA': 74.0,
                        'MCO': 0.86,
                        'MDA': 4.7,
                        'MOD': 2.0,
                        'MTH': 34.0,
                        'MTL': 1.9,
                        'NAV': 0.2,
                        'NEBL': 0.01,
                        'NEO': 0.0,
                        'NULS': 2.1,
                        'OAX': 8.3,
                        'OMG': 0.57,
                        'OST': 17.0,
                        'POE': 88.0,
                        'POWR': 8.6,
                        'PPT': 0.25,
                        'QSP': 21.0,
                        'QTUM': 0.01,
                        'RCN': 35.0,
                        'RDN': 2.2,
                        'REQ': 18.1,
                        'RLC': 4.1,
                        'SALT': 1.3,
                        'SBTC': 1.0,
                        'SNGLS': 42,
                        'SNM': 29.0,
                        'SNT': 32.0,
                        'STORJ': 5.9,
                        'STRAT': 0.1,
                        'SUB': 7.4,
                        'TNB': 82.0,
                        'TNT': 47.0,
                        'TRIG': 6.7,
                        'TRX': 129.0,
                        'USDT': 23.0,
                        'VEN': 1.8,
                        'VIB': 28.0,
                        'VIBE': 7.2,
                        'WABI': 3.5,
                        'WAVES': 0.002,
                        'WINGS': 9.3,
                        'WTC': 0.5,
                        'XLM': 0.01,
                        'XMR': 0.04,
                        'XRP': 0.25,
                        'XVG': 0.1,
                        'XZC': 0.02,
                        'YOYOW': 39.0,
                        'ZEC': 0.005,
                        'ZRX': 5.7,
                    },
                    'deposit': {
                        'ARK': 0,
                        'AST': 0,
                        'BCH': 0,
                        'BNB': 0,
                        'BNT': 0,
                        'BQX': 0,
                        'BTC': 0,
                        'BTG': 0,
                        'CTR': 0,
                        'DASH': 0,
                        'DNT': 0,
                        'ENG': 0,
                        'ENJ': 0,
                        'EOS': 0,
                        'ETC': 0,
                        'ETH': 0,
                        'EVX': 0,
                        'FUN': 0,
                        'GAS': 0,
                        'HSR': 0,
                        'ICN': 0,
                        'IOTA': 0,
                        'KNC': 0,
                        'LINK': 0,
                        'LRC': 0,
                        'LTC': 0,
                        'MCO': 0,
                        'MDA': 0,
                        'MOD': 0,
                        'MTH': 0,
                        'MTL': 0,
                        'NEO': 0,
                        'OAX': 0,
                        'OMG': 0,
                        'POWR': 0,
                        'QTUM': 0,
                        'REQ': 0,
                        'SALT': 0,
                        'SNGLS': 0,
                        'SNM': 0,
                        'SNT': 0,
                        'STORJ': 0,
                        'STRAT': 0,
                        'SUB': 0,
                        'TRX': 0,
                        'USDT': 0,
                        'VIB': 0,
                        'WTC': 0,
                        'XRP': 0,
                        'XVG': 0,
                        'YOYOW': 0,
                        'ZRX': 0,
                    },
                },
            },
            # exchange-specific options
            'options': {
                'recvWindow': 5 * 1000,  # 5 sec, binance default
                'timeDifference': 0,  # the difference between system clock and Binance clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
            },
        })

    def milliseconds(self):
        return super(binance, self).milliseconds() - self.options['timeDifference']

    async def load_time_difference(self):
        before = self.milliseconds()
        response = await self.publicGetTime()
        after = self.milliseconds()
        self.options['timeDifference'] = int((before + after) / 2 - response['serverTime'])
        return self.options['timeDifference']

    async def fetch_markets(self):
        response = await self.publicGetExchangeInfo()
        if self.options['adjustForTimeDifference']:
            await self.load_time_difference()
        markets = response['symbols']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['symbol']
            # "123456" is a "test symbol/market"
            if id == '123456':
                continue
            baseId = market['baseAsset']
            quoteId = market['quoteAsset']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            filters = self.index_by(market['filters'], 'filterType')
            precision = {
                'base': market['baseAssetPrecision'],
                'quote': market['quotePrecision'],
                'amount': market['baseAssetPrecision'],
                'price': market['quotePrecision'],
            }
            active = (market['status'] == 'TRADING')
            # lot size is deprecated as of 2018.02.06
            lot = -1 * math.log10(precision['amount'])
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'lot': lot,  # lot size is deprecated as of 2018.02.06
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': lot,
                        'max': None,
                    },
                },
            }
            if 'PRICE_FILTER' in filters:
                filter = filters['PRICE_FILTER']
                entry['precision']['price'] = self.precision_from_string(filter['tickSize'])
                entry['limits']['price'] = {
                    'min': float(filter['minPrice']),
                    'max': float(filter['maxPrice']),
                }
            if 'LOT_SIZE' in filters:
                filter = filters['LOT_SIZE']
                entry['precision']['amount'] = self.precision_from_string(filter['stepSize'])
                entry['lot'] = float(filter['stepSize'])  # lot size is deprecated as of 2018.02.06
                entry['limits']['amount'] = {
                    'min': float(filter['minQty']),
                    'max': float(filter['maxQty']),
                }
            if 'MIN_NOTIONAL' in filters:
                entry['limits']['cost']['min'] = float(filters['MIN_NOTIONAL']['minNotional'])
            result.append(entry)
        return result

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

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccount(params)
        result = {'info': response}
        balances = response['balances']
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = balance['asset']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            account = {
                'free': float(balance['free']),
                'used': float(balance['locked']),
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = maximum = 100
        orderbook = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'closeTime')
        if timestamp is None:
            timestamp = self.milliseconds()
        symbol = ticker['symbol']
        if not market:
            if symbol in self.markets_by_id:
                market = self.markets_by_id[symbol]
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highPrice'),
            'low': self.safe_float(ticker, 'lowPrice'),
            'bid': self.safe_float(ticker, 'bidPrice'),
            'bidVolume': self.safe_float(ticker, 'bidQty'),
            'ask': self.safe_float(ticker, 'askPrice'),
            'askVolume': self.safe_float(ticker, 'askQty'),
            'vwap': self.safe_float(ticker, 'weightedAvgPrice'),
            'open': self.safe_float(ticker, 'openPrice'),
            'close': self.safe_float(ticker, 'prevClosePrice'),
            'first': None,
            'last': self.safe_float(ticker, 'lastPrice'),
            'change': self.safe_float(ticker, 'priceChange'),
            'percentage': self.safe_float(ticker, 'priceChangePercent'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTicker24hr(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(response, market)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            tickers.append(self.parse_ticker(rawTickers[i]))
        tickersBySymbol = self.index_by(tickers, 'symbol')
        # return all of them if no symbols were passed in the first argument
        if symbols is None:
            return tickersBySymbol
        # otherwise filter by symbol
        result = {}
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            if symbol in tickersBySymbol:
                result[symbol] = tickersBySymbol[symbol]
        return result

    async def fetch_bid_asks(self, symbols=None, params={}):
        await self.load_markets()
        rawTickers = await self.publicGetTickerBookTicker(params)
        return self.parse_tickers(rawTickers, symbols)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        rawTickers = await self.publicGetTicker24hr(params)
        return self.parse_tickers(rawTickers, symbols)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0],
            float(ohlcv[1]),
            float(ohlcv[2]),
            float(ohlcv[3]),
            float(ohlcv[4]),
            float(ohlcv[5]),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'interval': self.timeframes[timeframe],
        }
        request['limit'] = limit if (limit) else 500  # default == max == 500
        if since is not None:
            request['startTime'] = since
        response = await self.publicGetKlines(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestampField = 'T' if ('T' in list(trade.keys())) else 'time'
        timestamp = trade[timestampField]
        priceField = 'p' if ('p' in list(trade.keys())) else 'price'
        price = float(trade[priceField])
        amountField = 'q' if ('q' in list(trade.keys())) else 'qty'
        amount = float(trade[amountField])
        idField = 'a' if ('a' in list(trade.keys())) else 'id'
        id = str(trade[idField])
        side = None
        order = None
        if 'orderId' in trade:
            order = str(trade['orderId'])
        if 'm' in trade:
            side = 'sell' if trade['m'] else 'buy'  # self is reversed intentionally
        else:
            side = 'buy' if (trade['isBuyer']) else 'sell'  # self is a True side
        fee = None
        if 'commission' in trade:
            fee = {
                'cost': float(trade['commission']),
                'currency': self.common_currency_code(trade['commissionAsset']),
            }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': id,
            'order': order,
            'type': None,
            'side': side,
            'price': price,
            'cost': price * amount,
            'amount': amount,
            'fee': fee,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = since
            request['endTime'] = since + 3600000
        if limit is not None:
            request['limit'] = limit
        # 'fromId': 123,    # ID to get aggregate trades from INCLUSIVE.
        # 'startTime': 456,  # Timestamp in ms to get aggregate trades from INCLUSIVE.
        # 'endTime': 789,   # Timestamp in ms to get aggregate trades until INCLUSIVE.
        # 'limit': 500,     # default = maximum = 500
        response = await self.publicGetAggTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        if status == 'NEW':
            return 'open'
        if status == 'PARTIALLY_FILLED':
            return 'open'
        if status == 'FILLED':
            return 'closed'
        if status == 'CANCELED':
            return 'canceled'
        return status.lower()

    def parse_order(self, order, market=None):
        status = self.safe_value(order, 'status')
        if status is not None:
            status = self.parse_order_status(status)
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            id = order['symbol']
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
        timestamp = None
        if 'time' in order:
            timestamp = order['time']
        elif 'transactTime' in order:
            timestamp = order['transactTime']
        else:
            raise ExchangeError(self.id + ' malformed order: ' + self.json(order))
        price = float(order['price'])
        amount = float(order['origQty'])
        filled = self.safe_float(order, 'executedQty', 0.0)
        remaining = max(amount - filled, 0.0)
        cost = None
        if price is not None:
            if filled is not None:
                cost = price * filled
        result = {
            'info': order,
            'id': str(order['orderId']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': order['type'].lower(),
            'side': order['side'].lower(),
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        order = {
            'symbol': market['id'],
            'quantity': self.amount_to_string(symbol, amount),
            'type': type.upper(),
            'side': side.upper(),
        }
        if type == 'limit':
            order = self.extend(order, {
                'price': self.price_to_precision(symbol, price),
                'timeInForce': 'GTC',  # 'GTC' = Good To Cancel(default), 'IOC' = Immediate Or Cancel
            })
        response = await self.privatePostOrder(self.extend(order, params))
        return self.parse_order(response)

    async def fetch_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol param')
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privateGetOrder(self.extend({
            'symbol': market['id'],
            'orderId': int(id),
        }, params))
        return self.parse_order(response, market)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol param')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit:
            request['limit'] = limit
        response = await self.privateGetAllOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        # if not symbol:
        #     raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol param')
        await self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = await self.privateGetOpenOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = await self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    async def cancel_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' cancelOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privateDeleteOrder(self.extend({
            'symbol': market['id'],
            'orderId': int(id),
            # 'origClientOrderId': id,
        }, params))
        return response

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchMyTrades requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit:
            request['limit'] = limit
        response = await self.privateGetMyTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def common_currency_code(self, currency):
        currencies = {
            'YOYO': 'YOYOW',
            'BCC': 'BCH',
            'NANO': 'XRB',
        }
        if currency in currencies:
            return currencies[currency]
        return currency

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        response = await self.wapiGetDepositAddress(self.extend({
            'asset': currency['id'],
        }, params))
        if 'success' in response:
            if response['success']:
                address = self.safe_string(response, 'address')
                tag = self.safe_string(response, 'addressTag')
                return {
                    'currency': code,
                    'address': address,
                    'tag': tag,
                    'status': 'ok',
                    'info': response,
                }
        raise ExchangeError(self.id + ' fetchDepositAddress failed: ' + self.last_http_response)

    async def withdraw(self, code, amount, address, tag=None, params={}):
        currency = self.currency(code)
        name = address[0:20]
        request = {
            'asset': currency['id'],
            'address': address,
            'amount': float(amount),
            'name': name,
        }
        if tag:
            request['addressTag'] = tag
        response = await self.wapiPostWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'id'),
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        if api == 'wapi':
            url += '.html'
        # v1 special case for userDataStream
        if path == 'userDataStream':
            body = self.urlencode(params)
            headers = {
                'X-MBX-APIKEY': self.apiKey,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        elif (api == 'private') or (api == 'wapi'):
            self.check_required_credentials()
            query = self.urlencode(self.extend({
                'timestamp': self.milliseconds(),
                'recvWindow': self.options['recvWindow'],
            }, params))
            signature = self.hmac(self.encode(query), self.encode(self.secret))
            query += '&' + 'signature=' + signature
            headers = {
                'X-MBX-APIKEY': self.apiKey,
            }
            if (method == 'GET') or (api == 'wapi'):
                url += '?' + query
            else:
                body = query
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if code >= 400:
            if (code == 418) or (code == 429):
                raise DDoSProtection(self.id + ' ' + str(code) + ' ' + reason + ' ' + body)
            if body.find('Price * QTY is zero or less') >= 0:
                raise InvalidOrder(self.id + ' order cost = amount * price is zero or less ' + body)
            if body.find('MIN_NOTIONAL') >= 0:
                raise InvalidOrder(self.id + ' order cost = amount * price is too small ' + body)
            if body.find('LOT_SIZE') >= 0:
                raise InvalidOrder(self.id + ' order amount should be evenly divisible by lot size, use self.amount_to_lots(symbol, amount) ' + body)
            if body.find('PRICE_FILTER') >= 0:
                raise InvalidOrder(self.id + ' order price exceeds allowed price precision or invalid, use self.price_to_precision(symbol, amount) ' + body)
            if body.find('Order does not exist') >= 0:
                raise OrderNotFound(self.id + ' ' + body)
        if isinstance(body, basestring):
            if len(body) > 0:
                if body[0] == '{':
                    response = json.loads(body)
                    error = self.safe_value(response, 'code')
                    if error is not None:
                        if error == -2010:
                            raise InsufficientFunds(self.id + ' ' + self.json(response))
                        elif error == -2011:
                            raise OrderNotFound(self.id + ' ' + self.json(response))
                        elif error == -1013:  # Invalid quantity
                            raise InvalidOrder(self.id + ' ' + self.json(response))
