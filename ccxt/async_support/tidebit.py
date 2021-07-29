# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.precise import Precise


class tidebit(Exchange):

    def describe(self):
        return self.deep_extend(super(tidebit, self).describe(), {
            'id': 'tidebit',
            'name': 'TideBit',
            'countries': ['HK'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'cancelOrder': True,
                'CORS': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchMarkets': True,
                'fetchOHLCV': True,
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1',
                '5m': '5',
                '15m': '15',
                '30m': '30',
                '1h': '60',
                '2h': '120',
                '4h': '240',
                '12h': '720',
                '1d': '1440',
                '3d': '4320',
                '1w': '10080',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87460811-1e690280-c616-11ea-8652-69f187305add.jpg',
                'api': 'https://www.tidebit.com',
                'www': 'https://www.tidebit.com',
                'doc': [
                    'https://www.tidebit.com/documents/api/guide',
                    'https://www.tidebit.com/swagger/#/default',
                ],
                'referral': 'http://bit.ly/2IX0LrM',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'tickers',
                        'tickers/{market}',
                        'timestamp',
                        'trades',
                        'trades/{market}',
                        'order_book',
                        'order',
                        'k_with_pending_trades',
                        'k',
                        'depth',
                    ],
                    'post': [],
                },
                'private': {
                    'get': [
                        'addresses/{address}',
                        'deposits/history',
                        'deposits/get_deposit',
                        'deposits/deposit_address',
                        'historys/orders',
                        'historys/vouchers',
                        'historys/accounts',
                        'historys/snapshots',
                        'linkage/get_status',
                        'members/me',
                        'order',
                        'orders',
                        'partners/orders/{id}/trades',
                        'referral_commissions/get_undeposited',
                        'referral_commissions/get_graph_data',
                        'trades/my',
                        'withdraws/bind_account_list',
                        'withdraws/get_withdraw_account',
                        'withdraws/fetch_bind_info',
                    ],
                    'post': [
                        'deposits/deposit_cash',
                        'favorite_markets/update',
                        'order/delete',
                        'orders',
                        'orders/multi',
                        'orders/clear',
                        'referral_commissions/deposit',
                        'withdraws/apply',
                        'withdraws/bind_bank',
                        'withdraws/bind_address',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': self.parse_number('0.003'),
                    'taker': self.parse_number('0.003'),
                },
                'funding': {
                    'tierBased': False,
                    'percentage': True,
                    'withdraw': {},  # There is only 1% fee on withdrawals to your bank account.
                },
            },
            'exceptions': {
                '2002': InsufficientFunds,
                '2003': OrderNotFound,
            },
        })

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = await self.privateGetDepositAddress(self.extend(request, params))
        if 'success' in response:
            if response['success']:
                address = self.safe_string(response, 'address')
                tag = self.safe_string(response, 'addressTag')
                return {
                    'currency': code,
                    'address': self.check_address(address),
                    'tag': tag,
                    'info': response,
                }

    async def fetch_markets(self, params={}):
        response = await self.publicGetMarkets(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'id')
            symbol = self.safe_string(market, 'name')
            baseId, quoteId = symbol.split('/')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': None,
                'precision': self.precision,
                'limits': self.limits,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privateGetMembersMe(params)
        balances = self.safe_value(response, 'accounts')
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'balance')
            account['used'] = self.safe_string(balance, 'locked')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 300
        request['market'] = market['id']
        response = await self.publicGetDepth(self.extend(request, params))
        timestamp = self.safe_timestamp(response, 'timestamp')
        return self.parse_order_book(response, symbol, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'at')
        ticker = self.safe_value(ticker, 'ticker', {})
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_number(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'ask': self.safe_number(ticker, 'sell'),
            'bidVolume': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'change': None,
            'percentage': None,
            'previousClose': None,
            'average': None,
            'baseVolume': self.safe_number(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTickers(params)
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.safe_market(id)
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTickersMarket(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        id = self.safe_string(trade, 'id')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'volume')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.safe_number(trade, 'funds')
        if cost is None:
            cost = self.parse_number(Precise.string_mul(priceString, amountString))
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         1498530360,
        #         2700.0,
        #         2700.0,
        #         2700.0,
        #         2700.0,
        #         0.01
        #     ]
        #
        return [
            self.safe_timestamp(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
            self.safe_number(ohlcv, 5),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 30  # default is 30
        request = {
            'market': market['id'],
            'period': self.timeframes[timeframe],
            'limit': limit,
        }
        if since is not None:
            request['timestamp'] = int(since / 1000)
        else:
            request['timestamp'] = 1800000
        response = await self.publicGetK(self.extend(request, params))
        #
        #     [
        #         [1498530360,2700.0,2700.0,2700.0,2700.0,0.01],
        #         [1498530420,2700.0,2700.0,2700.0,2700.0,0],
        #         [1498530480,2700.0,2700.0,2700.0,2700.0,0],
        #     ]
        #
        if response == 'None':
            return []
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'done': 'closed',
            'wait': 'open',
            'cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "id": 7,                              # 唯一的 Order ID
        #         "side": "sell",                       # Buy/Sell 代表买单/卖单
        #         "price": "3100.0",                    # 出价
        #         "avg_price": "3101.2",                # 平均成交价
        #         "state": "wait",                      # 订单的当前状态 [wait,done,cancel]
        #                                               #   wait   表明订单正在市场上挂单
        #                                               #          是一个active order
        #                                               #          此时订单可能部分成交或者尚未成交
        #                                               #   done   代表订单已经完全成交
        #                                               #   cancel 代表订单已经被撤销
        #         "market": "btccny",                   # 订单参与的交易市场
        #         "created_at": "2014-04-18T02:02:33Z",  # 下单时间 ISO8601格式
        #         "volume": "100.0",                    # 购买/卖出数量
        #         "remaining_volume": "89.8",           # 还未成交的数量 remaining_volume 总是小于等于 volume
        #                                               #   在订单完全成交时变成 0
        #         "executed_volume": "10.2",            # 已成交的数量
        #                                               #   volume = remaining_volume + executed_volume
        #         "trades_count": 1,                    # 订单的成交数 整数值
        #                                               #   未成交的订单为 0 有一笔成交的订单为 1
        #                                               #   通过该字段可以判断订单是否处于部分成交状态
        #         "trades": [                          # 订单的详细成交记录 参见Trade
        #                                               #   注意: 只有某些返回详细订单数据的 API 才会包含 Trade 数据
        #             {
        #                 "id": 2,
        #                 "price": "3100.0",
        #                 "volume": "10.2",
        #                 "market": "btccny",
        #                 "created_at": "2014-04-18T02:04:49Z",
        #                 "side": "sell"
        #             }
        #         ]
        #     }
        #
        marketId = self.safe_string(order, 'market')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        status = self.parse_order_status(self.safe_string(order, 'state'))
        id = self.safe_string(order, 'id')
        type = self.safe_string(order, 'ord_type')
        side = self.safe_string(order, 'side')
        price = self.safe_number(order, 'price')
        amount = self.safe_number(order, 'volume')
        filled = self.safe_number(order, 'executed_volume')
        remaining = self.safe_number(order, 'remaining_volume')
        average = self.safe_number(order, 'avg_price')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'cost': None,
            'trades': None,
            'fee': None,
            'info': order,
            'average': average,
        })

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'side': side,
            'volume': str(amount),
            'ord_type': type,
        }
        if type == 'limit':
            request['price'] = str(price)
        response = await self.privatePostOrders(self.extend(request, params))
        return self.parse_order(response)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        result = await self.privatePostOrderDelete(self.extend(request, params))
        order = self.parse_order(result)
        status = self.safe_string(order, 'status')
        if status == 'closed' or status == 'canceled':
            raise OrderNotFound(self.id + ' ' + self.json(order))
        return order

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        id = self.safe_string(params, 'id')
        if id is None:
            raise ArgumentsRequired(self.id + ' withdraw() requires an extra `id` param(withdraw account id according to withdraws/bind_account_list endpoint')
        request = {
            'id': id,
            'currency_type': 'coin',  # or 'cash'
            'currency': currency['id'],
            'body': amount,
            # 'address': address,  # they don't allow withdrawing to direct addresses?
        }
        if tag is not None:
            request['memo'] = tag
        result = await self.privatePostWithdrawsApply(self.extend(request, params))
        return {
            'info': result,
            'id': None,
        }

    def nonce(self):
        return self.milliseconds()

    def encode_params(self, params):
        return self.urlencode(self.keysort(params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + 'api/' + self.version + '/' + self.implode_params(path, params) + '.json'
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + request
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            sortedByKey = self.keysort(self.extend({
                'access_key': self.apiKey,
                'tonce': nonce,
            }, params))
            query = self.urlencode(sortedByKey)
            payload = method + '|' + request + '|' + query
            signature = self.hmac(self.encode(payload), self.encode(self.secret))
            suffix = query + '&signature=' + signature
            if method == 'GET':
                url += '?' + suffix
            else:
                body = suffix
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if (code == 400) or (response is None):
            feedback = self.id + ' ' + body
            if response is None:
                raise ExchangeError(feedback)
            error = self.safe_value(response, 'error', {})
            errorCode = self.safe_string(error, 'code')
            self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
            # fallback to default error handler
