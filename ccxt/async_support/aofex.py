# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.precise import Precise


class aofex(Exchange):

    def describe(self):
        return self.deep_extend(super(aofex, self).describe(), {
            'id': 'aofex',
            'name': 'AOFEX',
            'countries': ['GB'],
            'rateLimit': 1000,
            'hostname': 'openapi.aofex.com',
            'has': {
                'cancelAllOrders': True,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrder': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': None,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrderBook': True,
                'fetchOrderTrades': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTradingFee': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '6h': '6hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/77670271-056d1080-6f97-11ea-9ac2-4268e9ed0c1f.jpg',
                'api': {
                    'public': 'https://{hostname}/openApi',
                    'private': 'https://{hostname}/openApi',
                },
                'www': 'https://aofex.com',
                'doc': 'https://aofex.zendesk.com/hc/en-us/sections/360005576574-API',
                'fees': 'https://aofex.zendesk.com/hc/en-us/articles/360025814934-Fees-on-AOFEX',
                'referral': 'https://aofex.com/#/register?key=9763840',
            },
            'api': {
                'public': {
                    'get': [
                        'market/symbols',
                        'market/trade',
                        'market/depth',
                        'market/kline',
                        'market/precision',
                        'market/24kline',
                        'market/gears_depth',
                        'market/detail',
                    ],
                },
                'private': {
                    'get': [
                        'entrust/currentList',
                        'entrust/historyList',
                        'entrust/rate',
                        'wallet/list',
                        'entrust/detail',
                    ],
                    'post': [
                        'entrust/add',
                        'entrust/cancel',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.0019,
                    'taker': 0.002,
                },
            },
            'exceptions': {
                'exact': {
                    '20001': ExchangeError,  # request failure
                    '20401': PermissionDenied,  # no permission
                    '20500': ExchangeError,  # system error
                    '20501': BadSymbol,  # base symbol error
                    '20502': ExchangeError,  # base currency error
                    '20503': ExchangeError,  # base date error
                    '20504': InsufficientFunds,  # account frozen balance insufficient error
                    '20505': BadRequest,  # bad argument
                    '20506': AuthenticationError,  # api signature not valid
                    '20507': ExchangeError,  # gateway internal error
                    '20508': InvalidAddress,  # ad ethereum addresss
                    '20509': InsufficientFunds,  # order accountbalance error
                    '20510': InvalidOrder,  # order limitorder price error
                    '20511': InvalidOrder,  # order limitorder amount error
                    '20512': InvalidOrder,  # order orderprice precision error
                    '20513': InvalidOrder,  # order orderamount precision error
                    '20514': InvalidOrder,  # order marketorder amount error
                    '20515': InvalidOrder,  # order queryorder invalid
                    '20516': InvalidOrder,  # order orderstate error
                    '20517': InvalidOrder,  # order datelimit error
                    '50518': InvalidOrder,  # order update error
                    '20519': InvalidNonce,  # the nonce has been used
                    '20520': InvalidNonce,  # nonce expires, please verify server time
                    '20521': BadRequest,  # incomplete header parameters
                    '20522': ExchangeError,  # not getting the current user
                    '20523': AuthenticationError,  # please authenticate
                    '20524': PermissionDenied,  # btc account lockout
                    '20525': AuthenticationError,  # get API Key error
                    '20526': PermissionDenied,  # no query permission
                    '20527': PermissionDenied,  # no deal permission
                    '20528': PermissionDenied,  # no withdrawal permission
                    '20529': AuthenticationError,  # API Key expired
                    '20530': PermissionDenied,  # no permission
                },
                'broad': {
                },
            },
            'options': {
                'fetchBalance': {
                    'show_all': '0',  # '1' to show zero balances
                },
            },
            'commonCurrencies': {
                'CPC': 'Consensus Planet Coin',
                'HERO': 'Step Hero',  # conflict with Metahero
                'XBT': 'XBT',  # conflict with BTC
            },
        })

    async def fetch_markets(self, params={}):
        markets = await self.publicGetMarketSymbols(params)
        #
        #     {
        #         errno: 0,
        #         errmsg: 'success',
        #         result: [
        #             {
        #                 id: 2,
        #                 symbol: 'BTC-USDT',
        #                 base_currency: 'BTC',
        #                 quote_currency: 'USDT',
        #                 min_size: 0.00008,
        #                 max_size: 1300,
        #                 min_price: 1000,
        #                 max_price: 110000,
        #                 maker_fee: 1,
        #                 taker_fee: 1,
        #                 isHot: null,
        #                 isNew: null,
        #                 crown: null
        #             },
        #         ]
        #     }
        #
        precisions = await self.publicGetMarketPrecision()
        #
        #     {
        #         errno: 0,
        #         errmsg: 'success',
        #         result: {
        #             'MANA-USDT': {
        #                 amount: '2',
        #                 minQuantity: '32',
        #                 maxQuantity: '46000000',
        #                 price: '4',
        #                 minPrice: '0.003',
        #                 maxPrice: '0.35'
        #             },
        #         }
        #     }
        #
        precisions = self.safe_value(precisions, 'result', {})
        markets = self.safe_value(markets, 'result', [])
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'symbol')
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'quote_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            numericId = self.safe_integer(market, 'id')
            precision = self.safe_value(precisions, id, {})
            makerFeeString = self.safe_string(market, 'maker_fee')
            takerFeeString = self.safe_string(market, 'taker_fee')
            makerFee = self.parse_number(Precise.string_div(makerFeeString, '1000'))
            takerFee = self.parse_number(Precise.string_div(takerFeeString, '1000'))
            result.append({
                'id': id,
                'numericId': numericId,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'type': 'spot',
                'spot': True,
                'active': None,
                'maker': makerFee,
                'taker': takerFee,
                'precision': {
                    'amount': self.safe_integer(precision, 'amount'),
                    'price': self.safe_integer(precision, 'price'),
                },
                'limits': {
                    'amount': {
                        'min': self.safe_number(market, 'min_size'),
                        'max': self.safe_number(market, 'max_size'),
                    },
                    'price': {
                        'min': self.safe_number(market, 'min_price'),
                        'max': self.safe_number(market, 'max_price'),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': self.extend(market, precision),
            })
        return result

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     {
        #         id:  1584950100,
        #         amount: "329.196",
        #         count:  81,
        #         open: "0.021155",
        #         close: "0.021158",
        #         low: "0.021144",
        #         high: "0.021161",
        #         vol: "6.963557767"
        #     }
        #
        return [
            self.safe_timestamp(ohlcv, 'id'),
            self.safe_number(ohlcv, 'open'),
            self.safe_number(ohlcv, 'high'),
            self.safe_number(ohlcv, 'low'),
            self.safe_number(ohlcv, 'close'),
            self.safe_number(ohlcv, 'amount'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 150  # default 150, max 2000
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
            'size': limit,  # default 150, max 2000
        }
        response = await self.publicGetMarketKline(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: "success",
        #         result: {
        #             ts:  1584950139003,
        #             symbol: "ETH-BTC",
        #             period: "1min",
        #             data: [
        #                 {
        #                     id:  1584950100,
        #                     amount: "329.196",
        #                     count:  81,
        #                     open: "0.021155",
        #                     close: "0.021158",
        #                     low: "0.021144",
        #                     high: "0.021161",
        #                     vol: "6.963557767"
        #                 },
        #                 {
        #                     id:  1584950040,
        #                     amount: "513.265",
        #                     count:  151,
        #                     open: "0.021165",
        #                     close: "0.021155",
        #                     low: "0.021151",
        #                     high: "0.02118",
        #                     vol: "10.862806573"
        #                 },
        #             ]
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        data = self.safe_value(result, 'data', [])
        return self.parse_ohlcvs(data, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        options = self.safe_value(self.options, 'fetchBalance', {})
        showAll = self.safe_value(options, 'show_all', '0')
        request = {
            # 'currency': 'BTC',
            'show_all': showAll,  # required to show zero balances
        }
        response = await self.privateGetWalletList(self.extend(request, params))
        #
        #     {
        #         "errno": 0,
        #         "errmsg": "success",
        #         "result": [
        #             {"available": "0", "frozen": "0", "currency": "BTC"}
        #         ]
        #     }
        #
        result = {
            'info': response,
            'timestamp': None,
            'datetime': None,
        }
        balances = self.safe_value(response, 'result', [])
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'available')
            account['used'] = self.safe_string(balance, 'frozen')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_trading_fee(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.privateGetEntrustRate(self.extend(request, params))
        #
        #     {
        #         "errno":0,
        #         "errmsg":"success",
        #         "result": {
        #             "toFee":"0.002","fromFee":"0.002"
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        return {
            'info': response,
            'symbol': symbol,
            'maker': self.safe_number(result, 'fromFee'),
            'taker': self.safe_number(result, 'toFee'),
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        response = await self.publicGetMarketDepth(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: "success",
        #         result: {
        #             buyType: 1,
        #             sellType: 1,
        #             ts: 1584950701050,
        #             symbol: "ETH-BTC",
        #             asks: [
        #                 ["0.021227", "0.182"],
        #                 ["0.021249", "0.035"],
        #                 ["0.021253", "0.058"],
        #             ],
        #             bids: [
        #                 ["0.021207", "0.039"],
        #                 ["0.021203", "0.051"],
        #                 ["0.02117", "2.326"],
        #             ]
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        timestamp = self.safe_integer(result, 'ts')
        return self.parse_order_book(result, symbol, timestamp)

    def parse_ticker(self, ticker, market=None):
        #
        # fetchTicker
        #
        #     {
        #         id: 1584890087,
        #         amount: '150032.919',
        #         count: 134538,
        #         open: '0.021394',
        #         close: '0.021177',
        #         low: '0.021053',
        #         high: '0.021595',
        #         vol: '3201.72451442'
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'id')
        open = self.safe_number(ticker, 'open')
        last = self.safe_number(ticker, 'close')
        baseVolume = self.safe_number(ticker, 'amount')
        quoteVolume = self.safe_number(ticker, 'vol')
        return self.safe_ticker({
            'symbol': None,
            'timestamp': timestamp,
            'datetime': None,
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        request = {}
        if symbols is not None:
            ids = self.market_ids(symbols)
            request['symbol'] = ','.join(ids)
        response = await self.publicGetMarket24kline(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: "success",
        #         result: [
        #             {
        #                 symbol: "HB-AQ",
        #                 data: {
        #                     id:  1584893403,
        #                     amount: "4753751.243400354852648809",
        #                     count:  4724,
        #                     open: "6.3497",
        #                     close: "6.3318",
        #                     low: "6.011",
        #                     high: "6.5",
        #                     vol: "29538384.7873528796542891343493"
        #                 }
        #             },
        #         ]
        #     }
        #
        tickers = self.safe_value(response, 'result', [])
        result = {}
        for i in range(0, len(tickers)):
            marketId = self.safe_string(tickers[i], 'symbol')
            market = self.safe_market(marketId, None, '-')
            symbol = market['symbol']
            data = self.safe_value(tickers[i], 'data', {})
            result[symbol] = self.parse_ticker(data, market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetMarketDetail(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: 'success',
        #         result: {
        #             id: 1584890087,
        #             amount: '150032.919',
        #             count: 134538,
        #             open: '0.021394',
        #             close: '0.021177',
        #             low: '0.021053',
        #             high: '0.021595',
        #             vol: '3201.72451442'
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        return self.parse_ticker(result, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         id: 1584948803298490,
        #         amount: "2.737",
        #         price: "0.021209",
        #         direction: "sell",
        #         ts: 1584948803
        #     }
        #
        # fetchOrder trades
        #
        #     {
        #         "id":null,
        #         "ctime":"2020-03-23 20:07:17",
        #         "price":"123.9",
        #         "number":"0.010688626311541565",
        #         "total_price":"1.324320799999999903",
        #         "fee":"0.000021377252623083"
        #     }
        #
        id = self.safe_string(trade, 'id')
        ctime = self.parse8601(self.safe_string(trade, 'ctime'))
        timestamp = self.safe_timestamp(trade, 'ts', ctime) - 28800000  # 8 hours, adjust to UTC
        symbol = None
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        side = self.safe_string(trade, 'direction')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string_2(trade, 'amount', 'number')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.safe_number(trade, 'total_price')
        if cost is None:
            cost = self.parse_number(Precise.string_mul(priceString, amountString))
        feeCost = self.safe_number(trade, 'fee')
        fee = None
        if feeCost is not None:
            feeCurrencyCode = None
            if market is not None:
                if side == 'buy':
                    feeCurrencyCode = market['base']
                elif side == 'sell':
                    feeCurrencyCode = market['quote']
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
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
            'symbol': market['id'],
        }
        response = await self.publicGetMarketTrade(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: "success",
        #         result: {
        #             symbol: "ETH-BTC",
        #             ts: 1584948805439,
        #             data: [
        #                 {
        #                     id: 1584948803300883,
        #                     amount: "0.583",
        #                     price: "0.021209",
        #                     direction: "buy",
        #                     ts: 1584948803
        #                 },
        #                 {
        #                     id: 1584948803298490,
        #                     amount: "2.737",
        #                     price: "0.021209",
        #                     direction: "sell",
        #                     ts: 1584948803
        #                 },
        #             ]
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        data = self.safe_value(result, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            '1': 'open',
            '2': 'open',  # partially filled
            '3': 'closed',
            '4': 'canceled',  # canceling
            '5': 'canceled',  # partially canceled
            '6': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {order_sn: 'BM7442641584965237751ZMAKJ5'}
        #
        # fetchOpenOrders, fetchClosedOrders
        #
        #     {
        #         "order_sn": "BL74426415849672087836G48N1",
        #         "symbol": "ETH-USDT",
        #         "ctime": "2020-03-23 20:40:08",
        #         "type": 2,
        #         "side": "buy",
        #         "price": "90",  # None for market orders
        #         "number": "0.1",
        #         "total_price": "9.0",  # 0 for market orders
        #         "deal_number": null,
        #         "deal_price": null,
        #         "status": 1,
        #     }
        #
        # fetchOrder
        #
        #     {
        #         order_sn: 'BM7442641584965237751ZMAKJ5',
        #         symbol: 'ETH-USDT',
        #         ctime: '2020-03-23 20:07:17',
        #         type: 1,
        #         side: 'buy',
        #         price: '0',
        #         number: '10',
        #         total_price: '0',
        #         deal_number: '0.080718626311541565',
        #         deal_price: '123.890000000000000000',
        #         status: 3,
        #         # the trades field is injected by fetchOrder
        #         trades: [
        #             {
        #                 id: null,
        #                 ctime: '2020-03-23 20:07:17',
        #                 price: '123.9',
        #                 number: '0.010688626311541565',
        #                 total_price: '1.324320799999999903',
        #                 fee: '0.000021377252623083'
        #             }
        #         ]
        #     }
        #
        id = self.safe_string(order, 'order_sn')
        orderStatus = self.safe_string(order, 'status')
        status = self.parse_order_status(orderStatus)
        marketId = self.safe_string(order, 'symbol')
        market = self.safe_market(marketId, market, '-')
        timestamp = self.parse8601(self.safe_string(order, 'ctime'))
        if timestamp is not None:
            timestamp -= 28800000  # 8 hours, adjust to UTC
        orderType = self.safe_string(order, 'type')
        type = 'limit' if (orderType == '2') else 'market'
        side = self.safe_string(order, 'side')
        # amount = self.safe_number(order, 'number')
        # price = self.safe_number(order, 'price')
        price = None
        amount = None
        average = None
        number = self.safe_string(order, 'number')
        # total_price is just the price times the amount
        # but it doesn't tell us anything about the filled price
        if type == 'limit':
            amount = number
            price = self.safe_string(order, 'price')
        else:
            average = self.safe_string(order, 'deal_price')
            if side == 'buy':
                amount = self.safe_string(order, 'deal_number')
            else:
                amount = number
        # all orders except new orders and canceled orders
        rawTrades = self.safe_value(order, 'trades', [])
        filled = None
        if (type == 'limit') and (orderStatus == '3'):
            filled = amount
        return self.safe_order2({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': market['symbol'],
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': None,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'trades': rawTrades,
            'fee': None,
        })

    async def fetch_closed_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_sn': id,
        }
        response = await self.privateGetEntrustDetail(self.extend(request, params))
        #
        #     {
        #         "errno": 0,
        #         "errmsg": "success",
        #         "result": {
        #             "trades": [
        #                 {
        #                     "id":null,
        #                     "ctime":"2020-03-23 20:07:17",
        #                     "price":"123.9",
        #                     "number":"0.010688626311541565",
        #                     "total_price":"1.324320799999999903",
        #                     "fee":"0.000021377252623083"
        #                 },
        #             ],
        #             "entrust":{
        #                 "order_sn":"BM7442641584965237751ZMAKJ5",
        #                 "symbol":"ETH-USDT",
        #                 "ctime":"2020-03-23 20:07:17",
        #                 "type":1,
        #                 "side":"buy",
        #                 "price":"0",
        #                 "number":"10",
        #                 "total_price":"0",
        #                 "deal_number":"0.080718626311541565",
        #                 "deal_price":"123.890000000000000000",
        #                 "status":3
        #             }
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        trades = self.safe_value(result, 'trades', [])
        order = self.safe_value(result, 'entrust', {})
        order['trades'] = trades
        return self.parse_order(order)

    async def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        response = await self.fetch_closed_order(id, symbol, params)
        return self.safe_value(response, 'trades', [])

    async def fetch_orders_with_method(self, method, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            # 'from': 'BM7442641584965237751ZMAKJ5',  # query start order_sn
            'direct': 'prev',  # next
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if limit is not None:
            request['limit'] = limit  # default 20, max 100
        response = await getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "errno": 0,
        #         "errmsg": "success",
        #         "result": [
        #             {
        #                 "order_sn": "BL74426415849672087836G48N1",
        #                 "symbol": "ETH-USDT",
        #                 "ctime": "2020-03-23 20:40:08",
        #                 "type": 2,
        #                 "side": "buy",
        #                 "price": "90",
        #                 "number": "0.1",
        #                 "total_price": "9.0",
        #                 "deal_number": null,
        #                 "deal_price": null,
        #                 "status": 1,
        #             }
        #         ]
        #     }
        #
        result = self.safe_value(response, 'result', [])
        return self.parse_orders(result, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders_with_method('privateGetEntrustCurrentList', symbol, since, limit, params)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_orders_with_method('privateGetEntrustHistoryList', symbol, since, limit, params)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        orderType = side + '-' + type
        request = {
            'symbol': market['id'],
            'type': orderType,
        }
        if type == 'limit':
            request['amount'] = self.amount_to_precision(symbol, amount)
            request['price'] = self.price_to_precision(symbol, price)
        elif type == 'market':
            # for market buy it requires the amount of quote currency to spend
            if side == 'buy':
                createMarketBuyOrderRequiresPrice = self.safe_value(self.options, 'createMarketBuyOrderRequiresPrice', True)
                cost = amount
                if createMarketBuyOrderRequiresPrice:
                    if price is not None:
                        cost = amount * price
                    else:
                        raise InvalidOrder(self.id + " createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount, or, alternatively, add .options['createMarketBuyOrderRequiresPrice'] = False and supply the total cost value in the 'amount' argument")
                precision = market['precision']['price']
                request['amount'] = self.decimal_to_precision(cost, TRUNCATE, precision, self.precisionMode)
            else:
                request['amount'] = self.amount_to_precision(symbol, amount)
        response = await self.privatePostEntrustAdd(self.extend(request, params))
        #
        #     {
        #         errno: 0,
        #         errmsg: 'success',
        #         result: {order_sn: 'BM7442641584965237751ZMAKJ5'}
        #     }
        #
        result = self.safe_value(response, 'result', {})
        return self.parse_order(result, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_ids': id,
        }
        response = await self.privatePostEntrustCancel(self.extend(request, params))
        #
        #     {
        #         "errno": 0,
        #         "errmsg": "success",
        #         "result": {
        #             "success": ["avl12121", "bl3123123"],
        #             "failed": ["sd24564", "sdf6564564"]
        #         }
        #     }
        #
        result = self.safe_value(response, 'result', {})
        success = self.safe_value(result, 'success', [])
        if not self.in_array(id, success):
            raise OrderNotFound(self.id + ' order id ' + id + ' not found in successfully canceled orders: ' + self.json(response))
        timestamp = None
        return {
            'info': response,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': 'canceled',
            'symbol': symbol,
            'type': None,
            'side': None,
            'price': None,
            'cost': None,
            'average': None,
            'amount': None,
            'filled': None,
            'remaining': None,
            'trades': None,
            'fee': None,
            'clientOrderId': None,
        }

    async def cancel_all_orders(self, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelAllOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.privatePostEntrustCancel(self.extend(request, params))
        #
        #     {
        #         "errno": 0,
        #         "errmsg": "success",
        #         "result": {
        #             "success": ["avl12121", "bl3123123"],
        #             "failed": ["sd24564", "sdf6564564"]
        #         }
        #     }
        #
        return response

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.implode_hostname(self.urls['api'][api]) + '/' + path
        keys = list(params.keys())
        keysLength = len(keys)
        if api == 'public':
            if keysLength > 0:
                url += '?' + self.urlencode(params)
        else:
            nonce = str(self.nonce())
            uuid = self.uuid()
            randomString = uuid[0:5]
            nonceString = nonce + '_' + randomString
            auth = {}
            auth[self.apiKey] = self.apiKey
            auth[self.secret] = self.secret
            auth[nonceString] = nonceString
            for i in range(0, keysLength):
                key = keys[i]
                auth[key] = key + '=' + params[key]
            keysorted = self.keysort(auth)
            stringToSign = ''
            keys = list(keysorted.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                stringToSign += keysorted[key]
            signature = self.hash(self.encode(stringToSign), 'sha1')
            headers = {
                'Nonce': nonceString,
                'Token': self.apiKey,
                'Signature': signature,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                if keysLength > 0:
                    body = self.urlencode(params)
            else:
                if keysLength > 0:
                    url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        #
        #     {"errno":20501,"errmsg":"base symbol error"}
        #
        error = self.safe_string(response, 'errno')
        if (error is not None) and (error != '0'):
            message = self.safe_string(response, 'errmsg')
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['exact'], error, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
            raise ExchangeError(feedback)  # unknown message
