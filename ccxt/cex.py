# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
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
                'fetchOrders': True,
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
                'referral': 'https://cex.io/r/0/up105393824/0/',
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
                'createMarketBuyOrderRequiresPrice': True,
                'order': {
                    'status': {
                        'c': 'canceled',
                        'd': 'closed',
                        'cd': 'closed',
                        'a': 'open',
                    },
                },
            },
        })

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'limit': limit,
            'pair': market['id'],
            'dateFrom': since,
        }
        response = self.privatePostArchivedOrdersPair(self.extend(request, params))
        results = []
        for i in range(0, len(response)):
            # cancelled(unfilled):
            #    {id: '4005785516',
            #     type: 'sell',
            #     time: '2017-07-18T19:08:34.223Z',
            #     lastTxTime: '2017-07-18T19:08:34.396Z',
            #     lastTx: '4005785522',
            #     pos: null,
            #     status: 'c',
            #     symbol1: 'ETH',
            #     symbol2: 'GBP',
            #     amount: '0.20000000',
            #     price: '200.5625',
            #     remains: '0.20000000',
            #     'a:ETH:cds': '0.20000000',
            #     tradingFeeMaker: '0',
            #     tradingFeeTaker: '0.16',
            #     tradingFeeUserVolumeAmount: '10155061217',
            #     orderId: '4005785516'}
            # --
            # cancelled(partially filled buy):
            #    {id: '4084911657',
            #     type: 'buy',
            #     time: '2017-08-05T03:18:39.596Z',
            #     lastTxTime: '2019-03-19T17:37:46.404Z',
            #     lastTx: '8459265833',
            #     pos: null,
            #     status: 'cd',
            #     symbol1: 'BTC',
            #     symbol2: 'GBP',
            #     amount: '0.05000000',
            #     price: '2241.4692',
            #     tfacf: '1',
            #     remains: '0.03910535',
            #     'tfa:GBP': '0.04',
            #     'tta:GBP': '24.39',
            #     'a:BTC:cds': '0.01089465',
            #     'a:GBP:cds': '112.26',
            #     'f:GBP:cds': '0.04',
            #     tradingFeeMaker: '0',
            #     tradingFeeTaker: '0.16',
            #     tradingFeeUserVolumeAmount: '13336396963',
            #     orderId: '4084911657'}
            # --
            # cancelled(partially filled sell):
            #    {id: '4426728375',
            #     type: 'sell',
            #     time: '2017-09-22T00:24:20.126Z',
            #     lastTxTime: '2017-09-22T00:24:30.476Z',
            #     lastTx: '4426729543',
            #     pos: null,
            #     status: 'cd',
            #     symbol1: 'BCH',
            #     symbol2: 'BTC',
            #     amount: '0.10000000',
            #     price: '0.11757182',
            #     tfacf: '1',
            #     remains: '0.09935956',
            #     'tfa:BTC': '0.00000014',
            #     'tta:BTC': '0.00007537',
            #     'a:BCH:cds': '0.10000000',
            #     'a:BTC:cds': '0.00007537',
            #     'f:BTC:cds': '0.00000014',
            #     tradingFeeMaker: '0',
            #     tradingFeeTaker: '0.18',
            #     tradingFeeUserVolumeAmount: '3466715450',
            #     orderId: '4426728375'}
            # --
            # filled:
            #    {id: '5342275378',
            #     type: 'sell',
            #     time: '2018-01-04T00:28:12.992Z',
            #     lastTxTime: '2018-01-04T00:28:12.992Z',
            #     lastTx: '5342275393',
            #     pos: null,
            #     status: 'd',
            #     symbol1: 'BCH',
            #     symbol2: 'BTC',
            #     amount: '0.10000000',
            #     kind: 'api',
            #     price: '0.17',
            #     remains: '0.00000000',
            #     'tfa:BTC': '0.00003902',
            #     'tta:BTC': '0.01699999',
            #     'a:BCH:cds': '0.10000000',
            #     'a:BTC:cds': '0.01699999',
            #     'f:BTC:cds': '0.00003902',
            #     tradingFeeMaker: '0.15',
            #     tradingFeeTaker: '0.23',
            #     tradingFeeUserVolumeAmount: '1525951128',
            #     orderId: '5342275378'}
            # --
            # market order(buy):
            #    {"id": "6281946200",
            #     "pos": null,
            #     "time": "2018-05-23T11:55:43.467Z",
            #     "type": "buy",
            #     "amount": "0.00000000",
            #     "lastTx": "6281946210",
            #     "status": "d",
            #     "amount2": "20.00",
            #     "orderId": "6281946200",
            #     "remains": "0.00000000",
            #     "symbol1": "ETH",
            #     "symbol2": "EUR",
            #     "tfa:EUR": "0.05",
            #     "tta:EUR": "19.94",
            #     "a:ETH:cds": "0.03764100",
            #     "a:EUR:cds": "20.00",
            #     "f:EUR:cds": "0.05",
            #     "lastTxTime": "2018-05-23T11:55:43.467Z",
            #     "tradingFeeTaker": "0.25",
            #     "tradingFeeUserVolumeAmount": "55998097"}
            # --
            # market order(sell):
            #   {"id": "6282200948",
            #     "pos": null,
            #     "time": "2018-05-23T12:42:58.315Z",
            #     "type": "sell",
            #     "amount": "-0.05000000",
            #     "lastTx": "6282200958",
            #     "status": "d",
            #     "orderId": "6282200948",
            #     "remains": "0.00000000",
            #     "symbol1": "ETH",
            #     "symbol2": "EUR",
            #     "tfa:EUR": "0.07",
            #     "tta:EUR": "26.49",
            #     "a:ETH:cds": "0.05000000",
            #     "a:EUR:cds": "26.49",
            #     "f:EUR:cds": "0.07",
            #     "lastTxTime": "2018-05-23T12:42:58.315Z",
            #     "tradingFeeTaker": "0.25",
            #     "tradingFeeUserVolumeAmount": "56294576"}
            item = response[i]
            status = self.parse_order_status(self.safe_string(item, 'status'))
            baseId = item['symbol1']
            quoteId = item['symbol2']
            side = item['type']
            baseAmount = self.safe_float(item, 'a:' + baseId + ':cds')
            quoteAmount = self.safe_float(item, 'a:' + quoteId + ':cds')
            fee = self.safe_float(item, 'f:' + quoteId + ':cds')
            amount = self.safe_float(item, 'amount')
            price = self.safe_float(item, 'price')
            remaining = self.safe_float(item, 'remains')
            filled = amount - remaining
            orderAmount = None
            cost = None
            average = None
            type = None
            if not price:
                type = 'market'
                orderAmount = baseAmount
                cost = quoteAmount
                average = orderAmount / cost
            else:
                ta = self.safe_float(item, 'ta:' + quoteId, 0)
                tta = self.safe_float(item, 'tta:' + quoteId, 0)
                fa = self.safe_float(item, 'fa:' + quoteId, 0)
                tfa = self.safe_float(item, 'tfa:' + quoteId, 0)
                if side == 'sell':
                    cost = ta + tta + (fa + tfa)
                else:
                    cost = ta + tta - (fa + tfa)
                type = 'limit'
                orderAmount = amount
                average = cost / filled
            time = self.safe_string(item, 'time')
            lastTxTime = self.safe_string(item, 'lastTxTime')
            timestamp = self.parse8601(time)
            results.append({
                'id': item['id'],
                'timestamp': timestamp,
                'datetime': self.iso8601(timestamp),
                'lastUpdated': self.parse8601(lastTxTime),
                'status': status,
                'symbol': self.find_symbol(baseId + '/' + quoteId),
                'side': side,
                'price': price,
                'amount': orderAmount,
                'average': average,
                'type': type,
                'filled': filled,
                'cost': cost,
                'remaining': remaining,
                'fee': {
                    'cost': fee,
                    'currency': self.currencyId(quoteId),
                },
                'info': item,
            })
        return results

    def parse_order_status(self, status):
        return self.safe_string(self.options['order']['status'], status, status)

    def fetch_markets(self, params={}):
        response = self.publicGetCurrencyLimits(params)
        result = []
        markets = self.safe_value(response['data'], 'pairs')
        for i in range(0, len(markets)):
            market = markets[i]
            baseId = self.safe_string(market, 'symbol1')
            quoteId = self.safe_string(market, 'symbol2')
            id = baseId + '/' + quoteId
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'info': market,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': {
                    'price': self.precision_from_string(self.safe_string(market, 'minPrice')),
                    'amount': self.precision_from_string(self.safe_string(market, 'minLotSize')),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'minLotSize'),
                        'max': self.safe_float(market, 'maxLotSize'),
                    },
                    'price': {
                        'min': self.safe_float(market, 'minPrice'),
                        'max': self.safe_float(market, 'maxPrice'),
                    },
                    'cost': {
                        'min': self.safe_float(market, 'minLotSizeS2'),
                        'max': None,
                    },
                },
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalance(params)
        result = {'info': response}
        ommited = ['username', 'timestamp']
        balances = self.omit(response, ommited)
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            balance = self.safe_value(balances, currencyId, {})
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            # https://github.com/ccxt/ccxt/issues/5484
            account['used'] = self.safe_float(balance, 'orders', 0.0)
            code = self.safe_currency_code(currencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        if limit is not None:
            request['depth'] = limit
        response = self.publicGetOrderBookPair(self.extend(request, params))
        timestamp = response['timestamp'] * 1000
        return self.parse_order_book(response, timestamp)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0] * 1000,
            ohlcv[1],
            ohlcv[2],
            ohlcv[3],
            ohlcv[4],
            ohlcv[5],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if since is None:
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
            response = self.publicGetOhlcvHdYyyymmddPair(self.extend(request, params))
            key = 'data' + self.timeframes[timeframe]
            ohlcvs = json.loads(response[key])
            return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)
        except Exception as e:
            if isinstance(e, NullResponse):
                return []

    def parse_ticker(self, ticker, market=None):
        timestamp = None
        if 'timestamp' in ticker:
            timestamp = int(ticker['timestamp']) * 1000
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
            'datetime': self.iso8601(timestamp),
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

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        currencies = list(self.currencies.keys())
        request = {
            'currencies': '/'.join(currencies),
        }
        response = self.publicGetTickersCurrencies(self.extend(request, params))
        tickers = response['data']
        result = {}
        for t in range(0, len(tickers)):
            ticker = tickers[t]
            symbol = ticker['pair'].replace(':', '/')
            market = self.markets[symbol]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        ticker = self.publicGetTickerPair(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        id = self.safe_string(trade, 'tid')
        type = None
        side = self.safe_string(trade, 'type')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
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

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetTradeHistoryPair(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            # for market buy it requires the amount of quote currency to spend
            if side == 'buy':
                if self.options['createMarketBuyOrderRequiresPrice']:
                    if price is None:
                        raise InvalidOrder(self.id + " createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount, or, alternatively, add .options['createMarketBuyOrderRequiresPrice'] = False to supply the cost in the amount argument(the exchange-specific behaviour)")
                    else:
                        amount = amount * price
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
            'type': side,
            'amount': amount,
        }
        if type == 'limit':
            request['price'] = price
        else:
            request['order_type'] = type
        response = self.privatePostPlaceOrderPair(self.extend(request, params))
        return {
            'info': response,
            'id': response['id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        return self.privatePostCancelOrder(self.extend(request, params))

    def parse_order(self, order, market=None):
        # Depending on the call, 'time' can be a unix int, unix string or ISO string
        # Yes, really
        timestamp = self.safe_value(order, 'time')
        if isinstance(timestamp, basestring) and timestamp.find('T') >= 0:
            # ISO8601 string
            timestamp = self.parse8601(timestamp)
        else:
            # either integer or string integer
            timestamp = int(timestamp)
        symbol = None
        if market is None:
            baseId = self.safe_string(order, 'symbol1')
            quoteId = self.safe_string(order, 'symbol2')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            if symbol in self.markets:
                market = self.market(symbol)
        status = self.parse_order_status(self.safe_string(order, 'status'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        # sell orders can have a negative amount
        # https://github.com/ccxt/ccxt/issues/5338
        if amount is not None:
            amount = abs(amount)
        remaining = self.safe_float_2(order, 'pending', 'remains')
        filled = amount - remaining
        fee = None
        cost = None
        if market is not None:
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
                baseFeeCost = self.safe_float_2(order, baseFee, baseTakerFee)
                fee = {
                    'currency': market['base'],
                    'rate': feeRate,
                    'cost': baseFeeCost,
                }
            elif (quoteFee in list(order.keys())) or (quoteTakerFee in list(order.keys())):
                quoteFeeCost = self.safe_float_2(order, quoteFee, quoteTakerFee)
                fee = {
                    'currency': market['quote'],
                    'rate': feeRate,
                    'cost': quoteFeeCost,
                }
        if not cost:
            cost = price * filled
        side = order['type']
        trades = None
        orderId = order['id']
        if 'vtx' in order:
            trades = []
            for i in range(0, len(order['vtx'])):
                item = order['vtx'][i]
                tradeSide = self.safe_string(item, 'type')
                if item['type'] == 'cancel':
                    # looks like self might represent the cancelled part of an order
                    #   {id: '4426729543',
                    #     type: 'cancel',
                    #     time: '2017-09-22T00:24:30.476Z',
                    #     user: 'up106404164',
                    #     c: 'user:up106404164:a:BCH',
                    #     d: 'order:4426728375:a:BCH',
                    #     a: '0.09935956',
                    #     amount: '0.09935956',
                    #     balance: '0.42580261',
                    #     symbol: 'BCH',
                    #     order: '4426728375',
                    #     buy: null,
                    #     sell: null,
                    #     pair: null,
                    #     pos: null,
                    #     cs: '0.42580261',
                    #     ds: 0}
                    continue
                if not item['price']:
                    # self represents the order
                    #   {
                    #     "a": "0.47000000",
                    #     "c": "user:up106404164:a:EUR",
                    #     "d": "order:6065499239:a:EUR",
                    #     "cs": "1432.93",
                    #     "ds": "476.72",
                    #     "id": "6065499249",
                    #     "buy": null,
                    #     "pos": null,
                    #     "pair": null,
                    #     "sell": null,
                    #     "time": "2018-04-22T13:07:22.152Z",
                    #     "type": "buy",
                    #     "user": "up106404164",
                    #     "order": "6065499239",
                    #     "amount": "-715.97000000",
                    #     "symbol": "EUR",
                    #     "balance": "1432.93000000"}
                    continue
                # if item['type'] == 'costsNothing':
                #     print(item)
                # todo: deal with these
                if item['type'] == 'costsNothing':
                    continue
                # --
                # if side != tradeSide:
                #     raise Error(json.dumps(order, null, 2))
                # if orderId != item['order']:
                #     raise Error(json.dumps(order, null, 2))
                # --
                # partial buy trade
                #   {
                #     "a": "0.01589885",
                #     "c": "user:up106404164:a:BTC",
                #     "d": "order:6065499239:a:BTC",
                #     "cs": "0.36300000",
                #     "ds": 0,
                #     "id": "6067991213",
                #     "buy": "6065499239",
                #     "pos": null,
                #     "pair": null,
                #     "sell": "6067991206",
                #     "time": "2018-04-22T23:09:11.773Z",
                #     "type": "buy",
                #     "user": "up106404164",
                #     "order": "6065499239",
                #     "price": 7146.5,
                #     "amount": "0.01589885",
                #     "symbol": "BTC",
                #     "balance": "0.36300000",
                #     "symbol2": "EUR",
                #     "fee_amount": "0.19"}
                # --
                # trade with zero amount, but non-zero fee
                #   {
                #     "a": "0.00000000",
                #     "c": "user:up106404164:a:EUR",
                #     "d": "order:5840654423:a:EUR",
                #     "cs": 559744,
                #     "ds": 0,
                #     "id": "5840654429",
                #     "buy": "5807238573",
                #     "pos": null,
                #     "pair": null,
                #     "sell": "5840654423",
                #     "time": "2018-03-15T03:20:14.010Z",
                #     "type": "sell",
                #     "user": "up106404164",
                #     "order": "5840654423",
                #     "price": 730,
                #     "amount": "0.00000000",
                #     "symbol": "EUR",
                #     "balance": "5597.44000000",
                #     "symbol2": "BCH",
                #     "fee_amount": "0.01"}
                tradeTime = self.safe_string(item, 'time')
                tradeTimestamp = self.parse8601(tradeTime)
                tradeAmount = self.safe_float(item, 'amount')
                tradePrice = self.safe_float(item, 'price')
                absTradeAmount = tradeAmount < -tradeAmount if 0 else tradeAmount
                tradeCost = None
                if tradeSide == 'sell':
                    tradeCost = absTradeAmount
                    absTradeAmount = tradeCost / tradePrice
                else:
                    tradeCost = absTradeAmount * tradePrice
                trades.append({
                    'id': self.safe_string(item, 'id'),
                    'timestamp': tradeTimestamp,
                    'datetime': self.iso8601(tradeTimestamp),
                    'order': orderId,
                    'symbol': symbol,
                    'price': tradePrice,
                    'amount': absTradeAmount,
                    'cost': tradeCost,
                    'side': tradeSide,
                    'fee': {
                        'cost': self.safe_float(item, 'fee_amount'),
                        'currency': market['quote'],
                    },
                    'info': item,
                })
        return {
            'id': orderId,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': fee,
            'info': order,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        method = 'privatePostOpenOrders'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
            method += 'Pair'
        orders = getattr(self, method)(self.extend(request, params))
        for i in range(0, len(orders)):
            orders[i] = self.extend(orders[i], {'status': 'open'})
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        method = 'privatePostArchivedOrdersPair'
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchClosedOrders requires a symbol argument')
        market = self.market(symbol)
        request = {'pair': market['id']}
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': str(id),
        }
        response = self.privatePostGetOrderTx(self.extend(request, params))
        return self.parse_order(response['data'])

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
            body = self.json(self.extend({
                'key': self.apiKey,
                'signature': signature.upper(),
                'nonce': nonce,
            }, query))
            headers = {
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if isinstance(response, list):
            return response  # public endpoints may return []-arrays
        if not response:
            raise NullResponse(self.id + ' returned ' + self.json(response))
        elif response is True or response == 'true':
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

    def fetch_deposit_address(self, code, params={}):
        if code == 'XRP' or code == 'XLM':
            # https://github.com/ccxt/ccxt/pull/2327#issuecomment-375204856
            raise NotSupported(self.id + ' fetchDepositAddress does not support XRP and XLM addresses yet(awaiting docs from CEX.io)')
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privatePostGetAddress(self.extend(request, params))
        address = self.safe_string(response, 'data')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response,
        }
