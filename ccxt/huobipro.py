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
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InvalidOrder


class huobipro (Exchange):

    def describe(self):
        return self.deep_extend(super(huobipro, self).describe(), {
            'id': 'huobipro',
            'name': 'Huobi Pro',
            'countries': 'CN',
            'rateLimit': 2000,
            'userAgent': self.userAgents['chrome39'],
            'version': 'v1',
            'accounts': None,
            'accountsById': None,
            'hostname': 'api.huobipro.com',
            'has': {
                'CORS': False,
                'fetchLimits': True,
                'fetchOHCLV': True,
                'fetchOrders': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchDepositAddress': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '60min',
                '1d': '1day',
                '1w': '1week',
                '1M': '1mon',
                '1y': '1year',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766569-15aa7b9a-5edd-11e7-9e7f-44791f4ee49c.jpg',
                'api': 'https://api.huobipro.com',
                'www': 'https://www.huobipro.com',
                'doc': 'https://github.com/huobiapi/API_Docs/wiki/REST_api_reference',
                'fees': 'https://www.huobipro.com/about/fee/',
            },
            'api': {
                'market': {
                    'get': [
                        'history/kline',  # 获取K线数据
                        'detail/merged',  # 获取聚合行情(Ticker)
                        'depth',  # 获取 Market Depth 数据
                        'trade',  # 获取 Trade Detail 数据
                        'history/trade',  # 批量获取最近的交易记录
                        'detail',  # 获取 Market Detail 24小时成交量数据
                    ],
                },
                'public': {
                    'get': [
                        'common/symbols',  # 查询系统支持的所有交易对
                        'common/currencys',  # 查询系统支持的所有币种
                        'common/timestamp',  # 查询系统当前时间
                        'common/exchange',  # order limits
                    ],
                },
                'private': {
                    'get': [
                        'account/accounts',  # 查询当前用户的所有账户(即account-id)
                        'account/accounts/{id}/balance',  # 查询指定账户的余额
                        'order/orders/{id}',  # 查询某个订单详情
                        'order/orders/{id}/matchresults',  # 查询某个订单的成交明细
                        'order/orders',  # 查询当前委托、历史委托
                        'order/matchresults',  # 查询当前成交、历史成交
                        'dw/withdraw-virtual/addresses',  # 查询虚拟币提现地址
                        'dw/deposit-virtual/addresses',
                    ],
                    'post': [
                        'order/orders/place',  # 创建并执行一个新订单(一步下单， 推荐使用)
                        'order/orders',  # 创建一个新的订单请求 （仅创建订单，不执行下单）
                        'order/orders/{id}/place',  # 执行一个订单 （仅执行已创建的订单）
                        'order/orders/{id}/submitcancel',  # 申请撤销一个订单请求
                        'order/orders/batchcancel',  # 批量撤销订单
                        'dw/balance/transfer',  # 资产划转
                        'dw/withdraw/api/create',  # 申请提现虚拟币
                        'dw/withdraw-virtual/create',  # 申请提现虚拟币
                        'dw/withdraw-virtual/{id}/place',  # 确认申请虚拟币提现
                        'dw/withdraw-virtual/{id}/cancel',  # 申请取消提现虚拟币
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.002,
                    'taker': 0.002,
                },
            },
            'exceptions': {
                'order-limitorder-amount-min-error': InvalidOrder,  # limit order amount error, min: `0.001`
            },
        })

    def parse_markets(self, markets):
        numMarkets = len(markets)
        if numMarkets < 1:
            raise ExchangeError(self.id + ' publicGetCommonSymbols returned empty response: ' + self.json(markets))
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId = market['base-currency']
            quoteId = market['quote-currency']
            base = baseId.upper()
            quote = quoteId.upper()
            id = baseId + quoteId
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {
                'amount': market['amount-precision'],
                'price': market['price-precision'],
            }
            lot = math.pow(10, -precision['amount'])
            maker = 0 if (base == 'OMG') else 0.2 / 100
            taker = 0 if (base == 'OMG') else 0.2 / 100
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'lot': lot,
                'precision': precision,
                'taker': taker,
                'maker': maker,
                'limits': {
                    'amount': {
                        'min': lot,
                        'max': math.pow(10, precision['amount']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def fetch_limits(self, symbol, params={}):
        market = self.market(symbol)
        return self.publicGetCommonExchange(self.extend({
            'symbol': market['id'],
        }))

    def parse_limits(self, response, symbol=None, params={}):
        data = response['data']
        if data is None:
            return None
        return {
            'amount': {
                'min': data['limit-order-must-greater-than'],
                'max': data['limit-order-must-less-than'],
            },
        }

    def fetch_markets(self):
        response = self.publicGetCommonSymbols()
        return self.parse_markets(response['data'])

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = self.milliseconds()
        if 'ts' in ticker:
            timestamp = ticker['ts']
        bid = None
        ask = None
        bidVolume = None
        askVolume = None
        if 'bid' in ticker:
            if isinstance(ticker['bid'], list):
                bid = self.safe_float(ticker['bid'], 0)
                bidVolume = self.safe_float(ticker['bid'], 1)
        if 'ask' in ticker:
            if isinstance(ticker['ask'], list):
                ask = self.safe_float(ticker['ask'], 0)
                askVolume = self.safe_float(ticker['ask'], 1)
        open = self.safe_float(ticker, 'open')
        close = self.safe_float(ticker, 'close')
        change = None
        percentage = None
        average = None
        if (open is not None) and(close is not None):
            change = close - open
            average = self.sum(open, close) / 2
            if (close is not None) and(close > 0):
                percentage = (change / open) * 100
        baseVolume = self.safe_float(ticker, 'amount')
        quoteVolume = self.safe_float(ticker, 'vol')
        vwap = None
        if baseVolume is not None and quoteVolume is not None and baseVolume > 0:
            vwap = quoteVolume / baseVolume
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': ticker['high'],
            'low': ticker['low'],
            'bid': bid,
            'bidVolume': bidVolume,
            'ask': ask,
            'askVolume': askVolume,
            'vwap': vwap,
            'open': open,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.marketGetDepth(self.extend({
            'symbol': market['id'],
            'type': 'step0',
        }, params))
        if 'tick' in response:
            if not response['tick']:
                raise ExchangeError(self.id + ' fetchOrderBook() returned empty response: ' + self.json(response))
            return self.parse_order_book(response['tick'], response['tick']['ts'])
        raise ExchangeError(self.id + ' fetchOrderBook() returned unrecognized response: ' + self.json(response))

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.marketGetDetailMerged(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(response['tick'], market)

    def parse_trade(self, trade, market):
        timestamp = trade['ts']
        return {
            'info': trade,
            'id': str(trade['id']),
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['direction'],
            'price': trade['price'],
            'amount': trade['amount'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.marketGetHistoryTrade(self.extend({
            'symbol': market['id'],
            'size': 2000,
        }, params))
        data = response['data']
        result = []
        for i in range(0, len(data)):
            trades = data[i]['data']
            for j in range(0, len(trades)):
                trade = self.parse_trade(trades[j], market)
                result.append(trade)
        result = self.sort_by(result, 'timestamp')
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv['id'] * 1000,
            ohlcv['open'],
            ohlcv['high'],
            ohlcv['low'],
            ohlcv['close'],
            ohlcv['amount'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.marketGetHistoryKline(self.extend({
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
            'size': 2000,  # max = 2000
        }, params))
        return self.parse_ohlcvs(response['data'], market, timeframe, since, limit)

    def load_accounts(self, reload=False):
        if reload:
            self.accounts = self.fetch_accounts()
        else:
            if self.accounts:
                return self.accounts
            else:
                self.accounts = self.fetch_accounts()
                self.accountsById = self.index_by(self.accounts, 'id')
        return self.accounts

    def fetch_accounts(self):
        self.load_markets()
        response = self.privateGetAccountAccounts()
        return response['data']

    def fetch_balance(self, params={}):
        self.load_markets()
        self.load_accounts()
        response = self.privateGetAccountAccountsIdBalance(self.extend({
            'id': self.accounts[0]['id'],
        }, params))
        balances = response['data']['list']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            uppercase = balance['currency'].upper()
            currency = self.common_currency_code(uppercase)
            account = None
            if currency in result:
                account = result[currency]
            else:
                account = self.account()
            if balance['type'] == 'trade':
                account['free'] = float(balance['balance'])
            if balance['type'] == 'frozen':
                account['used'] = float(balance['balance'])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrders() requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        status = None
        if 'type' in params:
            status = params['type']
        elif 'status' in params:
            status = params['status']
        else:
            raise ExchangeError(self.id + ' fetchOrders() requires a type param or status param for spot market ' + symbol + '(0 or "open" for unfilled or partial filled orders, 1 or "closed" for filled orders)')
        if (status == 0) or (status == 'open'):
            status = 'pre-submitted,submitted,partial-filled'
        elif (status == 1) or (status == 'closed'):
            status = 'filled,partial-canceled,canceled'
        else:
            status = 'pre-submitted,submitted,partial-filled,filled,partial-canceled,canceled'
        response = self.privateGetOrderOrders(self.extend({
            'symbol': market['id'],
            'states': status,
        }))
        return self.parse_orders(response['data'], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        open = 0  # 0 for unfilled orders, 1 for filled orders
        return self.fetch_orders(symbol, None, None, self.extend({
            'status': open,
        }, params))

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetOrderOrdersId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response['data'])

    def parse_order_status(self, status):
        if status == 'partial-filled':
            return 'open'
        elif status == 'filled':
            return 'closed'
        elif status == 'canceled':
            return 'canceled'
        elif status == 'submitted':
            return 'open'
        return status

    def parse_order(self, order, market=None):
        side = None
        type = None
        status = None
        if 'type' in order:
            orderType = order['type'].split('-')
            side = orderType[0]
            type = orderType[1]
            status = self.parse_order_status(order['state'])
        symbol = None
        if not market:
            if 'symbol' in order:
                if order['symbol'] in self.markets_by_id:
                    marketId = order['symbol']
                    market = self.markets_by_id[marketId]
        if market:
            symbol = market['symbol']
        timestamp = order['created-at']
        amount = float(order['amount'])
        filled = float(order['field-amount'])
        remaining = amount - filled
        price = float(order['price'])
        cost = float(order['field-cash-amount'])
        average = 0
        if filled:
            average = float(cost / filled)
        result = {
            'info': order,
            'id': str(order['id']),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        self.load_accounts()
        market = self.market(symbol)
        order = {
            'account-id': self.accounts[0]['id'],
            'amount': self.amount_to_precision(symbol, amount),
            'symbol': market['id'],
            'type': side + '-' + type,
        }
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrderOrdersPlace(self.extend(order, params))
        return {
            'info': response,
            'id': response['data'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostOrderOrdersIdSubmitcancel({'id': id})

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privateGetDwDepositVirtualAddresses(self.extend({
            'currency': currency['id'].lower(),
        }, params))
        address = self.safe_string(response, 'data')
        self.check_address(address)
        return {
            'currency': code,
            'status': 'ok',
            'address': address,
            'info': response,
        }

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        cost = float(self.cost_to_precision(symbol, amount * rate))
        key = 'quote'
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

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        request = {
            'address': address,  # only supports existing addresses in your withdraw address list
            'amount': amount,
            'currency': currency.lower(),
        }
        if tag:
            request['addr-tag'] = tag  # only for XRP?
        response = self.privatePostDwWithdrawApiCreate(self.extend(request, params))
        id = None
        if 'data' in response:
            id = response['data']
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/'
        if api == 'market':
            url += api
        else:
            url += self.version
        url += '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            timestamp = self.ymdhms(self.milliseconds(), 'T')
            request = self.keysort(self.extend({
                'SignatureMethod': 'HmacSHA256',
                'SignatureVersion': '2',
                'AccessKeyId': self.apiKey,
                'Timestamp': timestamp,
            }, query))
            auth = self.urlencode(request)
            # unfortunately, PHP demands double quotes for the escaped newline symbol
            # eslint-disable-next-line quotes
            payload = "\n".join([method, self.hostname, url, auth])
            signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
            auth += '&' + self.urlencode({'Signature': signature})
            url += '?' + auth
            if method == 'POST':
                body = self.json(query)
                headers = {
                    'Content-Type': 'application/json',
                }
            else:
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
        else:
            if params:
                url += '?' + self.urlencode(params)
        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            if 'status' in response:
                #
                #     {"status":"error","err-code":"order-limitorder-amount-min-error","err-msg":"limit order amount error, min: `0.001`","data":null}
                #
                status = self.safe_string(response, 'status')
                if status == 'error':
                    code = self.safe_string(response, 'err-code')
                    feedback = self.id + ' ' + self.json(response)
                    message = self.safe_string(response, 'err-msg', feedback)
                    exceptions = self.exceptions
                    if code in exceptions:
                        raise exceptions[code](message)
                    raise ExchangeError(message)
