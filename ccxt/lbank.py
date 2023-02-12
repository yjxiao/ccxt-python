# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import DDoSProtection
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class lbank(Exchange):

    def describe(self):
        return self.deep_extend(super(lbank, self).describe(), {
            'id': 'lbank',
            'name': 'LBank',
            'countries': ['CN'],
            'version': 'v1',
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'createStopLimitOrder': False,
                'createStopMarketOrder': False,
                'createStopOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchClosedOrders': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchOHLCV': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': False,  # status 0 API doesn't work
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'withdraw': True,
            },
            'timeframes': {
                '1m': 'minute1',
                '5m': 'minute5',
                '15m': 'minute15',
                '30m': 'minute30',
                '1h': 'hour1',
                '2h': 'hour2',
                '4h': 'hour4',
                '6h': 'hour6',
                '8h': 'hour8',
                '12h': 'hour12',
                '1d': 'day1',
                '1w': 'week1',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/38063602-9605e28a-3302-11e8-81be-64b1e53c4cfb.jpg',
                'api': {
                    'rest': 'https://api.lbank.info',
                },
                'www': 'https://www.lbank.info',
                'doc': 'https://github.com/LBank-exchange/lbank-official-api-docs',
                'fees': 'https://www.lbank.info/fees.html',
                'referral': 'https://www.lbank.info/invitevip?icode=7QCY',
            },
            'api': {
                'public': {
                    'get': [
                        'currencyPairs',
                        'ticker',
                        'depth',
                        'trades',
                        'kline',
                        'accuracy',
                    ],
                },
                'private': {
                    'post': [
                        'user_info',
                        'create_order',
                        'cancel_order',
                        'orders_info',
                        'orders_info_history',
                        'withdraw',
                        'withdrawCancel',
                        'withdraws',
                        'withdrawConfigs',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.001'),
                    'taker': self.parse_number('0.001'),
                },
                'funding': {
                    'withdraw': {},
                },
            },
            'commonCurrencies': {
                'GMT': 'GMT Token',
                'PNT': 'Penta',
                'SHINJA': 'SHINJA(1M)',
                'VET_ERC20': 'VEN',
            },
            'options': {
                'cacheSecretAsPem': True,
            },
            'precisionMode': TICK_SIZE,
        })

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for lbank
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetAccuracy(params)
        #
        #    [
        #        {
        #            "symbol": "btc_usdt",
        #            "quantityAccuracy": "4",
        #            "minTranQua": "0.0001",
        #            "priceAccuracy": "2"
        #        },
        #        ...
        #    ]
        #
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = market['symbol']
            parts = id.split('_')
            baseId = None
            quoteId = None
            numParts = len(parts)
            # lbank will return symbols like "vet_erc20_usdt"
            if numParts > 2:
                baseId = parts[0] + '_' + parts[1]
                quoteId = parts[2]
            else:
                baseId = parts[0]
                quoteId = parts[1]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            result.append({
                'id': id,
                'symbol': base + '/' + quote,
                'base': base,
                'quote': quote,
                'settle': None,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': 'spot',
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'active': True,
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'quantityAccuracy'))),
                    'price': self.parse_number(self.parse_precision(self.safe_string(market, 'priceAccuracy'))),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_float(market, 'minTranQua'),
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
                },
                'info': id,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "symbol":"btc_usdt",
        #         "ticker":{
        #             "high":43416.06,
        #             "vol":7031.7427,
        #             "low":41804.26,
        #             "change":1.33,
        #             "turnover":300302447.81,
        #             "latest":43220.4
        #         },
        #         "timestamp":1642201617747
        #     }
        #
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_market(marketId, market, '_')
        symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'timestamp')
        info = ticker
        ticker = info['ticker']
        last = self.safe_string(ticker, 'latest')
        percentage = self.safe_string(ticker, 'change')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'vol'),
            'quoteVolume': self.safe_string(ticker, 'turnover'),
            'info': info,
        }, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTicker(self.extend(request, params))
        # {
        #     "symbol":"btc_usdt",
        #     "ticker":{
        #         "high":43416.06,
        #         "vol":7031.7427,
        #         "low":41804.26,
        #         "change":1.33,
        #         "turnover":300302447.81,
        #         "latest":43220.4
        #         },
        #     "timestamp":1642201617747
        # }
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: a dictionary of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        request = {
            'symbol': 'all',
        }
        response = self.publicGetTicker(self.extend(request, params))
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_order_book(self, symbol, limit=60, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        size = 60
        if limit is not None:
            size = min(limit, size)
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'size': size,
        }
        response = self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'])

    def parse_trade(self, trade, market=None):
        market = self.safe_market(None, market)
        timestamp = self.safe_integer(trade, 'date_ms')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        id = self.safe_string(trade, 'tid')
        type = None
        side = self.safe_string(trade, 'type')
        # remove type additions from i.e. buy_maker, sell_maker, buy_ioc, sell_ioc, buy_fok, sell_fok
        splited = side.split('_')
        side = splited[0]
        return {
            'id': id,
            'info': self.safe_value(trade, 'info', trade),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'size': 100,
        }
        if since is not None:
            request['time'] = int(since)
        if limit is not None:
            request['size'] = limit
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         1590969600,
        #         0.02451657,
        #         0.02452675,
        #         0.02443701,
        #         0.02447814,
        #         238.38210000
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

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 100  # as it's defined in lbank2
        if since is None:
            duration = self.parse_timeframe(timeframe)
            since = self.milliseconds() - duration * 1000 * limit
        request = {
            'symbol': market['id'],
            'type': self.safe_string(self.timeframes, timeframe, timeframe),
            'size': limit,
            'time': int(since / 1000),
        }
        response = self.publicGetKline(self.extend(request, params))
        #
        #     [
        #         [1590969600,0.02451657,0.02452675,0.02443701,0.02447814,238.38210000],
        #         [1590969660,0.02447814,0.02449883,0.02443209,0.02445973,212.40270000],
        #         [1590969720,0.02445973,0.02452067,0.02445909,0.02446151,266.16920000],
        #     ]
        #
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_balance(self, response):
        result = {
            'info': response,
            'timestamp': None,
            'datetime': None,
        }
        info = self.safe_value(response, 'info', {})
        free = self.safe_value(info, 'free', {})
        freeze = self.safe_value(info, 'freeze', {})
        asset = self.safe_value(info, 'asset', {})
        currencyIds = list(free.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(free, currencyId)
            account['used'] = self.safe_string(freeze, currencyId)
            account['total'] = self.safe_string(asset, currencyId)
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privatePostUserInfo(params)
        #
        #     {
        #         "result":"true",
        #         "info":{
        #             "freeze":{
        #                 "iog":"0.00000000",
        #                 "ssc":"0.00000000",
        #                 "eon":"0.00000000",
        #             },
        #             "asset":{
        #                 "iog":"0.00000000",
        #                 "ssc":"0.00000000",
        #                 "eon":"0.00000000",
        #             },
        #             "free":{
        #                 "iog":"0.00000000",
        #                 "ssc":"0.00000000",
        #                 "eon":"0.00000000",
        #             },
        #         }
        #     }
        #
        return self.parse_balance(response)

    def parse_order_status(self, status):
        statuses = {
            '-1': 'cancelled',  # cancelled
            '0': 'open',  # not traded
            '1': 'open',  # partial deal
            '2': 'closed',  # complete deal
            '4': 'closed',  # disposal processing
        }
        return self.safe_string(statuses, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "symbol"："eth_btc",
        #         "amount"：10.000000,
        #         "create_time"：1484289832081,
        #         "price"：5000.000000,
        #         "avg_price"：5277.301200,
        #         "type"："sell",
        #         "order_id"："ab704110-af0d-48fd-a083-c218f19a4a55",
        #         "deal_amount"：10.000000,
        #         "status"：2
        #     }
        #
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market, '_')
        timestamp = self.safe_integer(order, 'create_time')
        # Limit Order Request Returns: Order Price
        # Market Order Returns: cny amount of market order
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'amount')
        filled = self.safe_string(order, 'deal_amount')
        average = self.safe_string(order, 'avg_price')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        id = self.safe_string(order, 'order_id')
        type = self.safe_string(order, 'order_type')
        side = self.safe_string(order, 'type')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'triggerPrice': None,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': None,
            'trades': None,
            'fee': None,
            'info': self.safe_value(order, 'info', order),
            'average': average,
        }, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        order = {
            'symbol': market['id'],
            'type': side,
            'amount': amount,
        }
        if type == 'market':
            order['type'] += '_market'
        else:
            order['price'] = price
        response = self.privatePostCreateOrder(self.extend(order, params))
        order = self.omit(order, 'type')
        order['order_id'] = response['order_id']
        order['type'] = side
        order['order_type'] = type
        order['create_time'] = self.milliseconds()
        order['info'] = response
        return self.parse_order(order, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = self.privatePostCancelOrder(self.extend(request, params))
        return response

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        # Id can be a list of ids delimited by a comma
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'order_id': id,
        }
        response = self.privatePostOrdersInfo(self.extend(request, params))
        data = self.safe_value(response, 'orders', [])
        orders = self.parse_orders(data, market)
        numOrders = len(orders)
        if numOrders == 1:
            return orders[0]
        else:
            return orders

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        if limit is None:
            limit = 100
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'current_page': 1,
            'page_length': limit,
        }
        response = self.privatePostOrdersInfoHistory(self.extend(request, params))
        data = self.safe_value(response, 'orders', [])
        return self.parse_orders(data, None, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        orders = self.fetch_orders(symbol, since, limit, params)
        closed = self.filter_by(orders, 'status', 'closed')
        canceled = self.filter_by(orders, 'status', 'cancelled')  # cancelled orders may be partially filled
        allOrders = self.array_concat(closed, canceled)
        return self.filter_by_symbol_since_limit(allOrders, symbol, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the lbank api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        # mark and fee are optional params, mark is a note and must be less than 255 characters
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'assetCode': currency['id'],
            'amount': amount,
            'account': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostWithdraw(self.extend(request, params))
        #
        #     {
        #         'result': 'true',
        #         'withdrawId': 90082,
        #         'fee':0.001
        #     }
        #
        return self.parse_transaction(response, currency)

    def parse_transaction(self, transaction, currency=None):
        #
        # withdraw
        #
        #     {
        #         'result': 'true',
        #         'withdrawId': 90082,
        #         'fee':0.001
        #     }
        #
        currency = self.safe_currency(None, currency)
        return {
            'id': self.safe_string_2(transaction, 'id', 'withdrawId'),
            'txid': None,
            'timestamp': None,
            'datetime': None,
            'network': None,
            'addressFrom': None,
            'address': None,
            'addressTo': None,
            'amount': None,
            'type': None,
            'currency': currency['code'],
            'status': None,
            'updated': None,
            'tagFrom': None,
            'tag': None,
            'tagTo': None,
            'comment': None,
            'fee': None,
            'info': transaction,
        }

    def convert_secret_to_pem(self, secret):
        lineLength = 64
        secretLength = len(secret) - 0
        numLines = int(secretLength / lineLength)
        numLines = self.sum(numLines, 1)
        pem = "-----BEGIN PRIVATE KEY-----\n"  # eslint-disable-line
        for i in range(0, numLines):
            start = i * lineLength
            end = self.sum(start, lineLength)
            pem += self.secret[start:end] + "\n"  # eslint-disable-line
        return pem + '-----END PRIVATE KEY-----'

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api']['rest'] + '/' + self.version + '/' + self.implode_params(path, params)
        # Every endpoint ends with ".do"
        url += '.do'
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            query = self.keysort(self.extend({
                'api_key': self.apiKey,
            }, params))
            queryString = self.rawencode(query)
            message = self.hash(self.encode(queryString)).upper()
            cacheSecretAsPem = self.safe_value(self.options, 'cacheSecretAsPem', True)
            pem = None
            if cacheSecretAsPem:
                pem = self.safe_value(self.options, 'pem')
                if pem is None:
                    pem = self.convert_secret_to_pem(self.secret)
                    self.options['pem'] = pem
            else:
                pem = self.convert_secret_to_pem(self.secret)
            query['sign'] = self.rsa(message, pem, 'RS256')
            body = self.urlencode(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        success = self.safe_string(response, 'result')
        if success == 'false':
            errorCode = self.safe_string(response, 'error_code')
            message = self.safe_string({
                '10000': 'Internal error',
                '10001': 'The required parameters can not be empty',
                '10002': 'verification failed',
                '10003': 'Illegal parameters',
                '10004': 'User requests are too frequent',
                '10005': 'Key does not exist',
                '10006': 'user does not exist',
                '10007': 'Invalid signature',
                '10008': 'This currency pair is not supported',
                '10009': 'Limit orders can not be missing orders and the number of orders',
                '10010': 'Order price or order quantity must be greater than 0',
                '10011': 'Market orders can not be missing the amount of the order',
                '10012': 'market sell orders can not be missing orders',
                '10013': 'is less than the minimum trading position 0.001',
                '10014': 'Account number is not enough',
                '10015': 'The order type is wrong',
                '10016': 'Account balance is not enough',
                '10017': 'Abnormal server',
                '10018': 'order inquiry can not be more than 50 less than one',
                '10019': 'withdrawal orders can not be more than 3 less than one',
                '10020': 'less than the minimum amount of the transaction limit of 0.001',
                '10022': 'Insufficient key authority',
            }, errorCode, self.json(response))
            ErrorClass = self.safe_value({
                '10002': AuthenticationError,
                '10004': DDoSProtection,
                '10005': AuthenticationError,
                '10006': AuthenticationError,
                '10007': AuthenticationError,
                '10009': InvalidOrder,
                '10010': InvalidOrder,
                '10011': InvalidOrder,
                '10012': InvalidOrder,
                '10013': InvalidOrder,
                '10014': InvalidOrder,
                '10015': InvalidOrder,
                '10016': InvalidOrder,
                '10022': AuthenticationError,
            }, errorCode, ExchangeError)
            raise ErrorClass(message)
