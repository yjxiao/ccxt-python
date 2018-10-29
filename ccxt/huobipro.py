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
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import ExchangeNotAvailable


class huobipro (Exchange):

    def describe(self):
        return self.deep_extend(super(huobipro, self).describe(), {
            'id': 'huobipro',
            'name': 'Huobi Pro',
            'countries': ['CN'],
            'rateLimit': 2000,
            'userAgent': self.userAgents['chrome39'],
            'version': 'v1',
            'accounts': None,
            'accountsById': None,
            'hostname': 'api.huobi.pro',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchDepositAddress': True,
                'fetchOHLCV': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchTradingLimits': True,
                'fetchMyTrades': True,
                'withdraw': True,
                'fetchCurrencies': True,
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
                'api': {
                    'market': 'https://api.huobi.pro',
                    'public': 'https://api.huobi.pro',
                    'private': 'https://api.huobi.pro',
                    'zendesk': 'https://huobiglobal.zendesk.com/hc/en-us/articles',
                },
                'www': 'https://www.huobi.pro',
                'referral': 'https://www.huobi.br.com/en-us/topic/invited/?invite_code=rwrd3',
                'doc': 'https://github.com/huobiapi/API_Docs/wiki/REST_api_reference',
                'fees': 'https://www.huobi.pro/about/fee/',
            },
            'api': {
                'zendesk': {
                    'get': [
                        '360000400491-Trade-Limits',
                    ],
                },
                'market': {
                    'get': [
                        'history/kline',  # 获取K线数据
                        'detail/merged',  # 获取聚合行情(Ticker)
                        'depth',  # 获取 Market Depth 数据
                        'trade',  # 获取 Trade Detail 数据
                        'history/trade',  # 批量获取最近的交易记录
                        'detail',  # 获取 Market Detail 24小时成交量数据
                        'tickers',
                    ],
                },
                'public': {
                    'get': [
                        'common/symbols',  # 查询系统支持的所有交易对
                        'common/currencys',  # 查询系统支持的所有币种
                        'common/timestamp',  # 查询系统当前时间
                        'common/exchange',  # order limits
                        'settings/currencys',  # ?language=en-US
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
                        'query/deposit-withdraw',
                        'margin/loan-orders',  # 借贷订单
                        'margin/accounts/balance',  # 借贷账户详情
                        'points/actions',
                        'points/orders',
                        'subuser/aggregate-balance',
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
                        'dw/transfer-in/margin',  # 现货账户划入至借贷账户
                        'dw/transfer-out/margin',  # 借贷账户划出至现货账户
                        'margin/orders',  # 申请借贷
                        'margin/orders/{id}/repay',  # 归还借贷
                        'subuser/transfer',
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
                'account-frozen-balance-insufficient-error': InsufficientFunds,  # {"status":"error","err-code":"account-frozen-balance-insufficient-error","err-msg":"trade account balance is not enough, left: `0.0027`","data":null}
                'invalid-amount': InvalidOrder,  # eg "Paramemter `amount` is invalid."
                'order-limitorder-amount-min-error': InvalidOrder,  # limit order amount error, min: `0.001`
                'order-marketorder-amount-min-error': InvalidOrder,  # market order amount error, min: `0.01`
                'order-limitorder-price-min-error': InvalidOrder,  # limit order price error
                'order-limitorder-price-max-error': InvalidOrder,  # limit order price error
                'order-orderstate-error': OrderNotFound,  # canceling an already canceled order
                'order-queryorder-invalid': OrderNotFound,  # querying a non-existent order
                'order-update-error': ExchangeNotAvailable,  # undocumented error
                'api-signature-check-failed': AuthenticationError,
                'api-signature-not-valid': AuthenticationError,  # {"status":"error","err-code":"api-signature-not-valid","err-msg":"Signature not valid: Incorrect Access key [Access key错误]","data":null}
            },
            'options': {
                'createMarketBuyOrderRequiresPrice': True,
                'fetchMarketsMethod': 'publicGetCommonSymbols',
                'fetchBalanceMethod': 'privateGetAccountAccountsIdBalance',
                'createOrderMethod': 'privatePostOrderOrdersPlace',
                'language': 'en-US',
            },
        })

    def fetch_trading_limits(self, symbols=None, params={}):
        # self method should not be called directly, use loadTradingLimits() instead
        #  by default it will try load withdrawal fees of all currencies(with separate requests)
        #  however if you define symbols = ['ETH/BTC', 'LTC/BTC'] in args it will only load those
        self.load_markets()
        if symbols is None:
            symbols = self.symbols
        result = {}
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            result[symbol] = self.fetch_trading_limits_by_id(self.market_id(symbol), params)
        return result

    def fetch_trading_limits_by_id(self, id, params={}):
        request = {
            'symbol': id,
        }
        response = self.publicGetCommonExchange(self.extend(request, params))
        #
        #     {status:   "ok",
        #         data: {                                 symbol: "aidocbtc",
        #                              'buy-limit-must-less-than':  1.1,
        #                          'sell-limit-must-greater-than':  0.9,
        #                         'limit-order-must-greater-than':  1,
        #                            'limit-order-must-less-than':  5000000,
        #                    'market-buy-order-must-greater-than':  0.0001,
        #                       'market-buy-order-must-less-than':  100,
        #                   'market-sell-order-must-greater-than':  1,
        #                      'market-sell-order-must-less-than':  500000,
        #                       'circuit-break-when-greater-than':  10000,
        #                          'circuit-break-when-less-than':  10,
        #                 'market-sell-order-rate-must-less-than':  0.1,
        #                  'market-buy-order-rate-must-less-than':  0.1        }}
        #
        return self.parse_trading_limits(self.safe_value(response, 'data', {}))

    def parse_trading_limits(self, limits, symbol=None, params={}):
        #
        #   {                                 symbol: "aidocbtc",
        #                  'buy-limit-must-less-than':  1.1,
        #              'sell-limit-must-greater-than':  0.9,
        #             'limit-order-must-greater-than':  1,
        #                'limit-order-must-less-than':  5000000,
        #        'market-buy-order-must-greater-than':  0.0001,
        #           'market-buy-order-must-less-than':  100,
        #       'market-sell-order-must-greater-than':  1,
        #          'market-sell-order-must-less-than':  500000,
        #           'circuit-break-when-greater-than':  10000,
        #              'circuit-break-when-less-than':  10,
        #     'market-sell-order-rate-must-less-than':  0.1,
        #      'market-buy-order-rate-must-less-than':  0.1        }
        #
        return {
            'info': limits,
            'limits': {
                'amount': {
                    'min': self.safe_float(limits, 'limit-order-must-greater-than'),
                    'max': self.safe_float(limits, 'limit-order-must-less-than'),
                },
            },
        }

    def fetch_markets(self):
        method = self.options['fetchMarketsMethod']
        response = getattr(self, method)()
        markets = response['data']
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
            maker = 0 if (base == 'OMG') else 0.2 / 100
            taker = 0 if (base == 'OMG') else 0.2 / 100
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'taker': taker,
                'maker': maker,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
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

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'ts')
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
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
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
            orderbook = response['tick']
            result = self.parse_order_book(orderbook, orderbook['ts'])
            result['nonce'] = orderbook['version']
            return result
        raise ExchangeError(self.id + ' fetchOrderBook() returned unrecognized response: ' + self.json(response))

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.marketGetDetailMerged(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(response['tick'], market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.marketGetTickers(params)
        tickers = response['data']
        timestamp = self.safe_integer(response, 'ts')
        result = {}
        for i in range(0, len(tickers)):
            marketId = self.safe_string(tickers[i], 'symbol')
            market = self.safe_value(self.markets_by_id, marketId)
            symbol = marketId
            if market is not None:
                symbol = market['symbol']
                ticker = self.parse_ticker(tickers[i], market)
                ticker['timestamp'] = timestamp
                ticker['datetime'] = self.iso8601(timestamp)
                result[symbol] = ticker
        return result

    def parse_trade(self, trade, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'symbol')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer_2(trade, 'ts', 'created-at')
        order = self.safe_string(trade, 'order-id')
        side = self.safe_string(trade, 'direction')
        type = self.safe_string(trade, 'type')
        if type is not None:
            typeParts = type.split('-')
            side = typeParts[0]
            type = typeParts[1]
        price = self.safe_float(trade, 'price')
        amount = self.safe_float_2(trade, 'filled-amount', 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        fee = None
        feeCost = self.safe_float(trade, 'filled-fees')
        feeCurrency = None
        if market is not None:
            feeCurrency = market['base'] if (side == 'buy') else market['quote']
        filledPoints = self.safe_float(trade, 'filled-points')
        if filledPoints is not None:
            if (feeCost is None) or (feeCost == 0.0):
                feeCost = filledPoints
                feeCurrency = self.common_currency_code('HBPOINT')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
            }
        return {
            'info': trade,
            'id': self.safe_string(trade, 'id'),
            'order': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.privateGetOrderMatchresults(params)
        trades = self.parse_trades(response['data'], None, since, limit)
        if symbol is not None:
            market = self.market(symbol)
            trades = self.filter_by_symbol(trades, market['symbol'])
        return trades

    def fetch_trades(self, symbol, since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['size'] = limit
        response = self.marketGetHistoryTrade(self.extend(request, params))
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

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'period': self.timeframes[timeframe],
        }
        if limit is not None:
            request['size'] = limit
        response = self.marketGetHistoryKline(self.extend(request, params))
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

    def fetch_currencies(self, params={}):
        response = self.publicGetSettingsCurrencys(self.extend({
            'language': self.options['language'],
        }, params))
        currencies = response['data']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            #
            #  {                    name: "ctxc",
            #              'display-name': "CTXC",
            #        'withdraw-precision':  8,
            #             'currency-type': "eth",
            #        'currency-partition': "pro",
            #             'support-sites':  null,
            #                'otc-enable':  0,
            #        'deposit-min-amount': "2",
            #       'withdraw-min-amount': "4",
            #            'show-precision': "8",
            #                      weight: "2988",
            #                     visible:  True,
            #              'deposit-desc': "Please don’t deposit any other digital assets except CTXC t…",
            #             'withdraw-desc': "Minimum withdrawal amount: 4 CTXC. not >_<not For security reason…",
            #           'deposit-enabled':  True,
            #          'withdraw-enabled':  True,
            #    'currency-addr-with-tag':  False,
            #             'fast-confirms':  15,
            #             'safe-confirms':  30                                                             }
            #
            id = self.safe_value(currency, 'name')
            precision = self.safe_integer(currency, 'withdraw-precision')
            code = self.common_currency_code(id.upper())
            active = currency['visible'] and currency['deposit-enabled'] and currency['withdraw-enabled']
            result[code] = {
                'id': id,
                'code': code,
                'type': 'crypto',
                # 'payin': currency['deposit-enabled'],
                # 'payout': currency['withdraw-enabled'],
                # 'transfer': None,
                'name': currency['display-name'],
                'active': active,
                'fee': None,  # todo need to fetch from fee endpoint
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
                    'deposit': {
                        'min': self.safe_float(currency, 'deposit-min-amount'),
                        'max': math.pow(10, precision),
                    },
                    'withdraw': {
                        'min': self.safe_float(currency, 'withdraw-min-amount'),
                        'max': math.pow(10, precision),
                    },
                },
                'info': currency,
            }
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        self.load_accounts()
        method = self.options['fetchBalanceMethod']
        response = getattr(self, method)(self.extend({
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

    def fetch_orders_by_states(self, states, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'states': states,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = self.privateGetOrderOrders(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states('pre-submitted,submitted,partial-filled,filled,partial-canceled,canceled', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states('pre-submitted,submitted,partial-filled', symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_states('filled,partial-canceled,canceled', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetOrderOrdersId(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response['data'])

    def parse_order_status(self, status):
        statuses = {
            'partial-filled': 'open',
            'partial-canceled': 'canceled',
            'filled': 'closed',
            'canceled': 'canceled',
            'submitted': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        side = None
        type = None
        status = None
        if 'type' in order:
            orderType = order['type'].split('-')
            side = orderType[0]
            type = orderType[1]
            status = self.parse_order_status(self.safe_string(order, 'state'))
        symbol = None
        if market is None:
            if 'symbol' in order:
                if order['symbol'] in self.markets_by_id:
                    marketId = order['symbol']
                    market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'created-at')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'field-amount')  # typo in their API, filled amount
        price = self.safe_float(order, 'price')
        cost = self.safe_float(order, 'field-cash-amount')  # same typo
        remaining = None
        average = None
        if filled is not None:
            average = 0
            if amount is not None:
                remaining = amount - filled
            # if cost is defined and filled is not zero
            if (cost is not None) and(filled > 0):
                average = cost / filled
        result = {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
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
        request = {
            'account-id': self.accounts[0]['id'],
            'amount': self.amount_to_precision(symbol, amount),
            'symbol': market['id'],
            'type': side + '-' + type,
        }
        if self.options['createMarketBuyOrderRequiresPrice']:
            if (type == 'market') and(side == 'buy'):
                if price is None:
                    raise InvalidOrder(self.id + " market buy order requires price argument to calculate cost(total amount of quote currency to spend for buying, amount * price). To switch off self warning exception and specify cost in the amount argument, set .options['createMarketBuyOrderRequiresPrice'] = False. Make sure you know what you're doing.")
                else:
                    request['amount'] = self.price_to_precision(symbol, float(amount) * float(price))
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        method = self.options['createOrderMethod']
        response = getattr(self, method)(self.extend(request, params))
        timestamp = self.milliseconds()
        return {
            'info': response,
            'id': response['data'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
        }

    def cancel_order(self, id, symbol=None, params={}):
        response = self.privatePostOrderOrdersIdSubmitcancel({'id': id})
        #
        #     response = {
        #         'status': 'ok',
        #         'data': '10138899000',
        #     }
        #
        return self.extend(self.parse_order(response), {
            'id': id,
            'status': 'canceled',
        })

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
            'address': address,
            'info': response,
        }

    def currency_to_precision(self, currency, fee):
        return self.decimal_to_precision(fee, 0, self.currencies[currency]['precision'])

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        rate = market[takerOrMaker]
        cost = amount * rate
        key = 'quote'
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(self.currency_to_precision(market[key], cost)),
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        self.check_address(address)
        currency = self.currency(code)
        request = {
            'address': address,  # only supports existing addresses in your withdraw address list
            'amount': amount,
            'currency': currency['id'].lower(),
        }
        if tag is not None:
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
        elif (api == 'public') or (api == 'private'):
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
        url = self.urls['api'][api] + url
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
                    exceptions = self.exceptions
                    if code in exceptions:
                        raise exceptions[code](feedback)
                    raise ExchangeError(feedback)
