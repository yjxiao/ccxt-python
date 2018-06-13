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
from ccxt.base.errors import NullResponse
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import NotSupported


class cex (Exchange):

    def describe(self):
        return self.deep_extend(super(cex, self).describe(), {
            'id': 'cex',
            'name': 'CEX.IO',
            'countries': ['GB', 'EU', 'CY', 'RU'],
            'rateLimit': 1500,
            'has': {
                'CORS': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchDepositAddress': True,
            },
            'timeframes': {
                '1m': '1m',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766442-8ddc33b0-5ed8-11e7-8b98-f786aef0f3c9.jpg',
                'api': 'https://cex.io/api',
                'www': 'https://cex.io',
                'doc': 'https://cex.io/cex-api',
                'fees': [
                    'https://cex.io/fee-schedule',
                    'https://cex.io/limits-commissions',
                ],
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        'currency_limits/',
                        'last_price/{pair}/',
                        'last_prices/{currencies}/',
                        'ohlcv/hd/{yyyymmdd}/{pair}',
                        'order_book/{pair}/',
                        'ticker/{pair}/',
                        'tickers/{currencies}/',
                        'trade_history/{pair}/',
                    ],
                    'post': [
                        'convert/{pair}',
                        'price_stats/{pair}',
                    ],
                },
                'private': {
                    'post': [
                        'active_orders_status/',
                        'archived_orders/{pair}/',
                        'balance/',
                        'cancel_order/',
                        'cancel_orders/{pair}/',
                        'cancel_replace_order/{pair}/',
                        'close_position/{pair}/',
                        'get_address/',
                        'get_myfee/',
                        'get_order/',
                        'get_order_tx/',
                        'open_orders/{pair}/',
                        'open_orders/',
                        'open_position/{pair}/',
                        'open_positions/{pair}/',
                        'place_order/{pair}/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.16 / 100,
                    'taker': 0.25 / 100,
                },
                'funding': {
                    'withdraw': {
                        # 'USD': None,
                        # 'EUR': None,
                        # 'RUB': None,
                        # 'GBP': None,
                        'BTC': 0.001,
                        'ETH': 0.01,
                        'BCH': 0.001,
                        'DASH': 0.01,
                        'BTG': 0.001,
                        'ZEC': 0.001,
                        'XRP': 0.02,
                    },
                    'deposit': {
                        # 'USD': amount => amount * 0.035 + 0.25,
                        # 'EUR': amount => amount * 0.035 + 0.24,
                        # 'RUB': amount => amount * 0.05 + 15.57,
                        # 'GBP': amount => amount * 0.035 + 0.2,
                        'BTC': 0.0,
                        'ETH': 0.0,
                        'BCH': 0.0,
                        'DASH': 0.0,
                        'BTG': 0.0,
                        'ZEC': 0.0,
                        'XRP': 0.0,
                        'XLM': 0.0,
                    },
                },
            },
            'options': {
                'fetchOHLCVWarning': True,
            },
        })

    async def fetch_markets(self):
        markets = await self.publicGetCurrencyLimits()
        result = []
        for p in range(0, len(markets['data']['pairs'])):
            market = markets['data']['pairs'][p]
            id = market['symbol1'] + '/' + market['symbol2']
            symbol = id
            base, quote = symbol.split('/')
            result.append({
                'id': id,
                'info': market,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'lot': market['minLotSize'],
                'precision': {
                    'price': self.precision_from_string(market['minPrice']),
                    'amount': -1 * math.log10(market['minLotSize']),
                },
                'limits': {
                    'amount': {
                        'min': market['minLotSize'],
                        'max': market['maxLotSize'],
                    },
                    'price': {
                        'min': self.safe_float(market, 'minPrice'),
                        'max': self.safe_float(market, 'maxPrice'),
                    },
                    'cost': {
                        'min': market['minLotSizeS2'],
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostBalance()
        result = {'info': response}
        ommited = ['username', 'timestamp']
        balances = self.omit(response, ommited)
        currencies = list(balances.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            if currency in balances:
                account = {
                    'free': self.safe_float(balances[currency], 'available', 0.0),
                    'used': self.safe_float(balances[currency], 'orders', 0.0),
                    'total': 0.0,
                }
                account['total'] = self.sum(account['free'], account['used'])
                result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        if limit is not None:
            request['depth'] = limit
        orderbook = await self.publicGetOrderBookPair(self.extend(request, params))
        timestamp = orderbook['timestamp'] * 1000
        return self.parse_order_book(orderbook, timestamp)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0] * 1000,
            ohlcv[1],
            ohlcv[2],
            ohlcv[3],
            ohlcv[4],
            ohlcv[5],
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if not since:
            since = self.milliseconds() - 86400000  # yesterday
        else:
            if self.options['fetchOHLCVWarning']:
                raise ExchangeError(self.id + " fetchOHLCV warning: CEX can return historical candles for a certain date only, self might produce an empty or null reply. Set exchange.options['fetchOHLCVWarning'] = False or add({'options': {'fetchOHLCVWarning': False}}) to constructor params to suppress self warning message.")
        ymd = self.ymd(since)
        ymd = ymd.split('-')
        ymd = ''.join(ymd)
        request = {
            'pair': market['id'],
            'yyyymmdd': ymd,
        }
        try:
            response = await self.publicGetOhlcvHdYyyymmddPair(self.extend(request, params))
            key = 'data' + self.timeframes[timeframe]
            ohlcvs = json.loads(response[key])
            return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)
        except Exception as e:
            if isinstance(e, NullResponse):
                return []

    def parse_ticker(self, ticker, market=None):
        timestamp = None
        iso8601 = None
        if 'timestamp' in ticker:
            timestamp = int(ticker['timestamp']) * 1000
            iso8601 = self.iso8601(timestamp)
        volume = self.safe_float(ticker, 'volume')
        high = self.safe_float(ticker, 'high')
        low = self.safe_float(ticker, 'low')
        bid = self.safe_float(ticker, 'bid')
        ask = self.safe_float(ticker, 'ask')
        last = self.safe_float(ticker, 'last')
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': iso8601,
            'high': high,
            'low': low,
            'bid': bid,
            'bidVolume': None,
            'ask': ask,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': volume,
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        currencies = list(self.currencies.keys())
        response = await self.publicGetTickersCurrencies(self.extend({
            'currencies': '/'.join(currencies),
        }, params))
        tickers = response['data']
        result = {}
        for t in range(0, len(tickers)):
            ticker = tickers[t]
            symbol = ticker['pair'].replace(':', '/')
            market = self.markets[symbol]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetTickerPair(self.extend({
            'pair': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = int(trade['date']) * 1000
        return {
            'info': trade,
            'id': trade['tid'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': self.safe_float(trade, 'price'),
            'amount': self.safe_float(trade, 'amount'),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetTradeHistoryPair(self.extend({
            'pair': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        order = {
            'pair': self.market_id(symbol),
            'type': side,
            'amount': amount,
        }
        if type == 'limit':
            order['price'] = price
        else:
            # for market buy CEX.io requires the amount of quote currency to spend
            if side == 'buy':
                if not price:
                    raise InvalidOrder('For market buy orders ' + self.id + " requires the amount of quote currency to spend, to calculate proper costs call createOrder(symbol, 'market', 'buy', amount, price)")
                order['amount'] = amount * price
            order['order_type'] = type
        response = await self.privatePostPlaceOrderPair(self.extend(order, params))
        return {
            'info': response,
            'id': response['id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostCancelOrder({'id': id})

    def parse_order(self, order, market=None):
        # Depending on the call, 'time' can be a unix int, unix string or ISO string
        # Yes, really
        timestamp = order['time']
        if isinstance(order['time'], basestring) and order['time'].find('T') >= 0:
            # ISO8601 string
            timestamp = self.parse8601(timestamp)
        else:
            # either integer or string integer
            timestamp = int(timestamp)
        symbol = None
        if not market:
            symbol = order['symbol1'] + '/' + order['symbol2']
            if symbol in self.markets:
                market = self.market(symbol)
        status = order['status']
        if status == 'a':
            status = 'open'  # the unified status
        elif status == 'cd':
            status = 'canceled'
        elif status == 'c':
            status = 'canceled'
        elif status == 'd':
            status = 'closed'
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        remaining = self.safe_float(order, 'pending')
        if not remaining:
            remaining = self.safe_float(order, 'remains')
        filled = amount - remaining
        fee = None
        cost = None
        if market:
            symbol = market['symbol']
            cost = self.safe_float(order, 'ta:' + market['quote'])
            if cost is None:
                cost = self.safe_float(order, 'tta:' + market['quote'])
            baseFee = 'fa:' + market['base']
            baseTakerFee = 'tfa:' + market['base']
            quoteFee = 'fa:' + market['quote']
            quoteTakerFee = 'tfa:' + market['quote']
            feeRate = self.safe_float(order, 'tradingFeeMaker')
            if not feeRate:
                feeRate = self.safe_float(order, 'tradingFeeTaker', feeRate)
            if feeRate:
                feeRate /= 100.0  # convert to mathematically-correct percentage coefficients: 1.0 = 100%
            if (baseFee in list(order.keys())) or (baseTakerFee in list(order.keys())):
                baseFeeCost = self.safe_float(order, baseFee)
                if baseFeeCost is None:
                    baseFeeCost = self.safe_float(order, baseTakerFee)
                fee = {
                    'currency': market['base'],
                    'rate': feeRate,
                    'cost': baseFeeCost,
                }
            elif (quoteFee in list(order.keys())) or (quoteTakerFee in list(order.keys())):
                quoteFeeCost = self.safe_float(order, quoteFee)
                if quoteFeeCost is None:
                    quoteFeeCost = self.safe_float(order, quoteTakerFee)
                fee = {
                    'currency': market['quote'],
                    'rate': feeRate,
                    'cost': quoteFeeCost,
                }
        if not cost:
            cost = price * filled
        return {
            'id': order['id'],
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': order['type'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': fee,
            'info': order,
        }

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        method = 'privatePostOpenOrders'
        market = None
        if symbol:
            market = self.market(symbol)
            request['pair'] = market['id']
            method += 'Pair'
        orders = await getattr(self, method)(self.extend(request, params))
        for i in range(0, len(orders)):
            orders[i] = self.extend(orders[i], {'status': 'open'})
        return self.parse_orders(orders, market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        method = 'privatePostArchivedOrdersPair'
        if symbol is None:
            raise NotSupported(self.id + ' fetchClosedOrders requires a symbol argument')
        market = self.market(symbol)
        request = {'pair': market['id']}
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privatePostGetOrder(self.extend({
            'id': str(id),
        }, params))
        return self.parse_order(response)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + self.uid + self.apiKey
            signature = self.hmac(self.encode(auth), self.encode(self.secret))
            body = self.urlencode(self.extend({
                'key': self.apiKey,
                'signature': signature.upper(),
                'nonce': nonce,
            }, query))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if not response:
            raise NullResponse(self.id + ' returned ' + self.json(response))
        elif response is True:
            return response
        elif 'e' in response:
            if 'ok' in response:
                if response['ok'] == 'ok':
                    return response
            raise ExchangeError(self.id + ' ' + self.json(response))
        elif 'error' in response:
            if response['error']:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response

    async def fetch_deposit_address(self, code, params={}):
        if code == 'XRP':
            # https://github.com/ccxt/ccxt/pull/2327#issuecomment-375204856
            raise NotSupported(self.id + ' fetchDepositAddress does not support XRP addresses yet(awaiting docs from CEX.io)')
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = await self.privatePostGetAddress(self.extend(request, params))
        address = self.safe_string(response, 'data')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'status': 'ok',
            'info': response,
        }
