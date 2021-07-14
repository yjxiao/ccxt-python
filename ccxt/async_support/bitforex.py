# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.precise import Precise


class bitforex(Exchange):

    def describe(self):
        return self.deep_extend(super(bitforex, self).describe(), {
            'id': 'bitforex',
            'name': 'Bitforex',
            'countries': ['CN'],
            'version': 'v1',
            'has': {
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': True,
                'fetchMarkets': True,
                'fetchMyTrades': False,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': False,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchTrades': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
                '1M': '1month',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87295553-1160ec00-c50e-11ea-8ea0-df79276a9646.jpg',
                'api': 'https://api.bitforex.com',
                'www': 'https://www.bitforex.com',
                'doc': 'https://github.com/githubdev2020/API_Doc_en/wiki',
                'fees': 'https://help.bitforex.com/en_us/?cat=13',
                'referral': 'https://www.bitforex.com/en/invitationRegister?inviterId=1867438',
            },
            'api': {
                'public': {
                    'get': [
                        'api/v1/market/symbols',
                        'api/v1/market/ticker',
                        'api/v1/market/depth',
                        'api/v1/market/trades',
                        'api/v1/market/kline',
                    ],
                },
                'private': {
                    'post': [
                        'api/v1/fund/mainAccount',
                        'api/v1/fund/allAccount',
                        'api/v1/trade/placeOrder',
                        'api/v1/trade/placeMultiOrder',
                        'api/v1/trade/cancelOrder',
                        'api/v1/trade/cancelMultiOrder',
                        'api/v1/trade/orderInfo',
                        'api/v1/trade/multiOrderInfo',
                        'api/v1/trade/orderInfos',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.1 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': True,
                    'deposit': {},
                    'withdraw': {
                        'BTC': 0.0005,
                        'ETH': 0.01,
                        'BCH': 0.0001,
                        'LTC': 0.001,
                        'ETC': 0.005,
                        'USDT': 5,
                        'CMCT': 30,
                        'AION': 3,
                        'LVT': 0,
                        'DATA': 40,
                        'RHP': 50,
                        'NEO': 0,
                        'AIDOC': 10,
                        'BQT': 2,
                        'R': 2,
                        'DPY': 0.8,
                        'GTC': 40,
                        'AGI': 30,
                        'DENT': 100,
                        'SAN': 1,
                        'SPANK': 8,
                        'AID': 5,
                        'OMG': 0.1,
                        'BFT': 5,
                        'SHOW': 150,
                        'TRX': 20,
                        'ABYSS': 10,
                        'THM': 25,
                        'ZIL': 20,
                        'PPT': 0.2,
                        'WTC': 0.4,
                        'LRC': 7,
                        'BNT': 1,
                        'CTXC': 1,
                        'MITH': 20,
                        'TRUE': 4,
                        'LYM': 10,
                        'VEE': 100,
                        'AUTO': 200,
                        'REN': 50,
                        'TIO': 2.5,
                        'NGC': 1.5,
                        'PST': 10,
                        'CRE': 200,
                        'IPC': 5,
                        'PTT': 1000,
                        'XMCT': 20,
                        'ATMI': 40,
                        'TERN': 40,
                        'XLM': 0.01,
                        'ODE': 15,
                        'FTM': 100,
                        'RTE': 100,
                        'DCC': 100,
                        'IMT': 500,
                        'GOT': 3,
                        'EGT': 500,
                        'DACC': 1000,
                        'UBEX': 500,
                        'ABL': 100,
                        'OLT': 100,
                        'DAV': 40,
                        'THRT': 10,
                        'RMESH': 3,
                        'UPP': 20,
                        'SDT': 0,
                        'SHR': 10,
                        'MTV': 3,
                        'ESS': 100,
                        'MET': 3,
                        'TTC': 20,
                        'LXT': 10,
                        'XCLP': 100,
                        'LUK': 100,
                        'UBC': 100,
                        'DTX': 10,
                        'BEAT': 20,
                        'DEED': 2,
                        'BGX': 3000,
                        'PRL': 20,
                        'ELY': 50,
                        'CARD': 300,
                        'SQR': 15,
                        'VRA': 400,
                        'BWX': 3500,
                        'MAS': 75,
                        'FLP': 0.6,
                        'UNC': 300,
                        'CRNC': 15,
                        'MFG': 70,
                        'ZXC': 70,
                        'TRT': 30,
                        'ZIX': 35,
                        'XRA': 10,
                        'AMO': 1600,
                        'IPG': 3,
                        'uDoo': 50,
                        'URB': 30,
                        'ARCONA': 3,
                        'CRAD': 5,
                        'NOBS': 1000,
                        'ADF': 2,
                        'ELF': 5,
                        'LX': 20,
                        'PATH': 15,
                        'SILK': 120,
                        'SKYFT': 50,
                        'EDN': 50,
                        'ADE': 50,
                        'EDR': 10,
                        'TIME': 0.25,
                        'SPRK': 20,
                        'QTUM': 0.01,
                        'BF': 5,
                        'ZPR': 100,
                        'HYB': 10,
                        'CAN': 30,
                        'CEL': 10,
                        'ATS': 50,
                        'KCASH': 1,
                        'ACT': 0.01,
                        'MT': 300,
                        'DXT': 30,
                        'WAB': 4000,
                        'HYDRO': 400,
                        'LQD': 5,
                        'OPTC': 200,
                        'EQUAD': 80,
                        'LATX': 50,
                        'LEDU': 100,
                        'RIT': 70,
                        'ACDC': 500,
                        'FSN': 2,
                    },
                },
            },
            'commonCurrencies': {
                'ACE': 'ACE Entertainment',
                'CAPP': 'Crypto Application Token',
                'CREDIT': 'TerraCredit',
                'CTC': 'Culture Ticket Chain',
                'GOT': 'GoNetwork',
                'HBC': 'Hybrid Bank Cash',
                'IQ': 'IQ.Cash',
                'MIR': 'MIR COIN',
                'UOS': 'UOS Network',
            },
            'exceptions': {
                '4004': OrderNotFound,
                '1013': AuthenticationError,
                '1016': AuthenticationError,
                '1017': PermissionDenied,  # {"code":"1017","success":false,"time":1602670594367,"message":"IP not allow"}
                '1019': BadSymbol,  # {"code":"1019","success":false,"time":1607087743778,"message":"Symbol Invalid"}
                '3002': InsufficientFunds,
                '4002': InvalidOrder,  # {"success":false,"code":"4002","message":"Price unreasonable"}
                '4003': InvalidOrder,  # {"success":false,"code":"4003","message":"amount too small"}
                '10204': DDoSProtection,
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetApiV1MarketSymbols(params)
        data = response['data']
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = self.safe_string(market, 'symbol')
            symbolParts = id.split('-')
            baseId = symbolParts[2]
            quoteId = symbolParts[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            active = True
            precision = {
                'amount': self.safe_integer(market, 'amountPrecision'),
                'price': self.safe_integer(market, 'pricePrecision'),
            }
            limits = {
                'amount': {
                    'min': self.safe_number(market, 'minOrderAmount'),
                    'max': None,
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
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
                'limits': limits,
                'info': market,
            })
        return result

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(trade, 'time')
        id = self.safe_string(trade, 'tid')
        orderId = None
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        sideId = self.safe_integer(trade, 'direction')
        side = self.parse_side(sideId)
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'order': orderId,
            'fee': None,
            'takerOrMaker': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['size'] = limit
        market = self.market(symbol)
        response = await self.publicGetApiV1MarketTrades(self.extend(request, params))
        return self.parse_trades(response['data'], market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostApiV1FundAllAccount(params)
        data = response['data']
        result = {'info': response}
        for i in range(0, len(data)):
            balance = data[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['used'] = self.safe_string(balance, 'frozen')
            account['free'] = self.safe_string(balance, 'active')
            account['total'] = self.safe_string(balance, 'fix')
            result[code] = account
        return self.parse_balance(result, False)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetApiV1MarketTicker(self.extend(request, params))
        data = response['data']
        timestamp = self.safe_integer(data, 'date')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(data, 'high'),
            'low': self.safe_number(data, 'low'),
            'bid': self.safe_number(data, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(data, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': self.safe_number(data, 'last'),
            'last': self.safe_number(data, 'last'),
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_number(data, 'vol'),
            'quoteVolume': None,
            'info': response,
        }

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     {
        #         "close":0.02505143,
        #         "currencyVol":0,
        #         "high":0.02506422,
        #         "low":0.02505143,
        #         "open":0.02506095,
        #         "time":1591508940000,
        #         "vol":51.1869
        #     }
        #
        return [
            self.safe_integer(ohlcv, 'time'),
            self.safe_number(ohlcv, 'open'),
            self.safe_number(ohlcv, 'high'),
            self.safe_number(ohlcv, 'low'),
            self.safe_number(ohlcv, 'close'),
            self.safe_number(ohlcv, 'vol'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'ktype': self.timeframes[timeframe],
        }
        if limit is not None:
            request['size'] = limit  # default 1, max 600
        response = await self.publicGetApiV1MarketKline(self.extend(request, params))
        #
        #     {
        #         "data":[
        #             {"close":0.02505143,"currencyVol":0,"high":0.02506422,"low":0.02505143,"open":0.02506095,"time":1591508940000,"vol":51.1869},
        #             {"close":0.02503914,"currencyVol":0,"high":0.02506687,"low":0.02503914,"open":0.02505358,"time":1591509000000,"vol":9.1082},
        #             {"close":0.02505172,"currencyVol":0,"high":0.02507466,"low":0.02503895,"open":0.02506371,"time":1591509060000,"vol":63.7431},
        #         ],
        #         "success":true,
        #         "time":1591509427131
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        marketId = self.market_id(symbol)
        request = {
            'symbol': marketId,
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetApiV1MarketDepth(self.extend(request, params))
        data = self.safe_value(response, 'data')
        timestamp = self.safe_integer(response, 'time')
        return self.parse_order_book(data, symbol, timestamp, 'bids', 'asks', 'price', 'amount')

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'open',
            '2': 'closed',
            '3': 'canceled',
            '4': 'canceled',
        }
        return statuses[status] if (status in statuses) else status

    def parse_side(self, sideId):
        if sideId == 1:
            return 'buy'
        elif sideId == 2:
            return 'sell'
        else:
            return None

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'orderId')
        timestamp = self.safe_number(order, 'createTime')
        lastTradeTimestamp = self.safe_number(order, 'lastTime')
        symbol = market['symbol']
        sideId = self.safe_integer(order, 'tradeType')
        side = self.parse_side(sideId)
        type = None
        price = self.safe_number(order, 'orderPrice')
        average = self.safe_number(order, 'avgPrice')
        amount = self.safe_number(order, 'orderAmount')
        filled = self.safe_number(order, 'dealAmount')
        status = self.parse_order_status(self.safe_string(order, 'orderState'))
        feeSide = 'base' if (side == 'buy') else 'quote'
        feeCurrency = market[feeSide]
        fee = {
            'cost': self.safe_number(order, 'tradeFee'),
            'currency': feeCurrency,
        }
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
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
            'status': status,
            'fee': fee,
            'trades': None,
        })

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'orderId': id,
        }
        response = await self.privatePostApiV1TradeOrderInfo(self.extend(request, params))
        order = self.parse_order(response['data'], market)
        return order

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'state': 0,
        }
        response = await self.privatePostApiV1TradeOrderInfos(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
            'state': 1,
        }
        response = await self.privatePostApiV1TradeOrderInfos(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        sideId = None
        if side == 'buy':
            sideId = 1
        elif side == 'sell':
            sideId = 2
        request = {
            'symbol': self.market_id(symbol),
            'price': price,
            'amount': amount,
            'tradeType': sideId,
        }
        response = await self.privatePostApiV1TradePlaceOrder(self.extend(request, params))
        data = response['data']
        return {
            'info': response,
            'id': self.safe_string(data, 'orderId'),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'orderId': id,
        }
        if symbol is not None:
            request['symbol'] = self.market_id(symbol)
        results = await self.privatePostApiV1TradeCancelOrder(self.extend(request, params))
        success = results['success']
        returnVal = {'info': results, 'success': success}
        return returnVal

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            payload = self.urlencode({'accessKey': self.apiKey})
            query['nonce'] = self.milliseconds()
            if query:
                payload += '&' + self.urlencode(self.keysort(query))
            # message = '/' + 'api/' + self.version + '/' + path + '?' + payload
            message = '/' + path + '?' + payload
            signature = self.hmac(self.encode(message), self.encode(self.secret))
            body = payload + '&signData=' + signature
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            feedback = self.id + ' ' + body
            success = self.safe_value(response, 'success')
            if success is not None:
                if not success:
                    code = self.safe_string(response, 'code')
                    self.throw_exactly_matched_exception(self.exceptions, code, feedback)
                    raise ExchangeError(feedback)
