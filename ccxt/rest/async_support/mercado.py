# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.rest.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder
from ccxt.base.decimal_to_precision import TICK_SIZE


class mercado(Exchange):

    def describe(self):
        return self.deep_extend(super(mercado, self).describe(), {
            'id': 'mercado',
            'name': 'Mercado Bitcoin',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'version': 'v3',
            'has': {
                'CORS': True,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createMarketOrder': True,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'createStopLimitOrder': False,
                'createStopMarketOrder': False,
                'createStopOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
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
                'fetchMyTrades': 'emulated',
                'fetchOHLCV': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': None,
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
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '2w': '2w',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27837060-e7c58714-60ea-11e7-9192-f05e86adb83f.jpg',
                'api': {
                    'public': 'https://www.mercadobitcoin.net/api',
                    'private': 'https://www.mercadobitcoin.net/tapi',
                    'v4Public': 'https://www.mercadobitcoin.com.br/v4',
                },
                'www': 'https://www.mercadobitcoin.com.br',
                'doc': [
                    'https://www.mercadobitcoin.com.br/api-doc',
                    'https://www.mercadobitcoin.com.br/trade-api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'coins',
                        '{coin}/orderbook/',  # last slash critical
                        '{coin}/ticker/',
                        '{coin}/trades/',
                        '{coin}/trades/{from}/',
                        '{coin}/trades/{from}/{to}',
                        '{coin}/day-summary/{year}/{month}/{day}/',
                    ],
                },
                'private': {
                    'post': [
                        'cancel_order',
                        'get_account_info',
                        'get_order',
                        'get_withdrawal',
                        'list_system_messages',
                        'list_orders',
                        'list_orderbook',
                        'place_buy_order',
                        'place_sell_order',
                        'place_market_buy_order',
                        'place_market_sell_order',
                        'withdraw_coin',
                    ],
                },
                'v4Public': {
                    'get': [
                        '{coin}/candle/',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.003,
                    'taker': 0.007,
                },
            },
            'options': {
                'limits': {
                    'BTC': 0.001,
                    'BCH': 0.001,
                    'ETH': 0.01,
                    'LTC': 0.01,
                    'XRP': 0.1,
                },
            },
            'precisionMode': TICK_SIZE,
        })

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for mercado
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = await self.publicGetCoins(params)
        #
        #     [
        #         "BCH",
        #         "BTC",
        #         "ETH",
        #         "LTC",
        #         "XRP",
        #         "MBPRK01",
        #         "MBPRK02",
        #         "MBPRK03",
        #         "MBPRK04",
        #         "MBCONS01",
        #         "USDC",
        #         "WBX",
        #         "CHZ",
        #         "MBCONS02",
        #         "PAXG",
        #         "MBVASCO01",
        #         "LINK"
        #     ]
        #
        result = []
        amountLimits = self.safe_value(self.options, 'limits', {})
        for i in range(0, len(response)):
            coin = response[i]
            baseId = coin
            quoteId = 'BRL'
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            id = quote + base
            priceLimit = '1e-5'
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
                'active': None,
                'contract': False,
                'linear': None,
                'inverse': None,
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.parse_number('0.00000001'),
                    'price': self.parse_number('0.00001'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(amountLimits, baseId),
                        'max': None,
                    },
                    'price': {
                        'min': self.parse_number(priceLimit),
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': coin,
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['base'],
        }
        response = await self.publicGetCoinOrderbook(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'])

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "high":"103.96000000",
        #         "low":"95.00000000",
        #         "vol":"2227.67806598",
        #         "last":"97.91591000",
        #         "buy":"95.52760000",
        #         "sell":"97.91475000",
        #         "open":"99.79955000",
        #         "date":1643382606
        #     }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.safe_timestamp(ticker, 'date')
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['base'],
        }
        response = await self.publicGetCoinTicker(self.extend(request, params))
        ticker = self.safe_value(response, 'ticker', {})
        #
        #     {
        #         "ticker": {
        #             "high":"1549.82293000",
        #             "low":"1503.00011000",
        #             "vol":"81.82827101",
        #             "last":"1533.15000000",
        #             "buy":"1533.21018000",
        #             "sell":"1540.09000000",
        #             "open":"1524.71089000",
        #             "date":1643691671
        #         }
        #     }
        #
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp_2(trade, 'date', 'executed_timestamp')
        market = self.safe_market(None, market)
        id = self.safe_string_2(trade, 'tid', 'operation_id')
        type = None
        side = self.safe_string(trade, 'type')
        price = self.safe_string(trade, 'price')
        amount = self.safe_string_2(trade, 'amount', 'quantity')
        feeCost = self.safe_string(trade, 'fee_rate')
        fee = None
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
            }
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': fee,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        method = 'publicGetCoinTrades'
        request = {
            'coin': market['base'],
        }
        if since is not None:
            method += 'From'
            request['from'] = int(since / 1000)
        to = self.safe_integer(params, 'to')
        if to is not None:
            method += 'To'
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_balance(self, response):
        data = self.safe_value(response, 'response_data', {})
        balances = self.safe_value(data, 'balance', {})
        result = {'info': response}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            if currencyId in balances:
                balance = self.safe_value(balances, currencyId, {})
                account = self.account()
                account['free'] = self.safe_string(balance, 'available')
                account['total'] = self.safe_string(balance, 'total')
                result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privatePostGetAccountInfo(params)
        return self.parse_balance(response)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
        }
        method = self.capitalize(side) + 'Order'
        if type == 'limit':
            method = 'privatePostPlace' + method
            request['limit_price'] = self.price_to_precision(market['symbol'], price)
            request['quantity'] = self.amount_to_precision(market['symbol'], amount)
        else:
            method = 'privatePostPlaceMarket' + method
            if side == 'buy':
                if price is None:
                    raise InvalidOrder(self.id + ' createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount')
                request['cost'] = self.price_to_precision(market['symbol'], amount * price)
            else:
                request['quantity'] = self.amount_to_precision(market['symbol'], amount)
        response = await getattr(self, method)(self.extend(request, params))
        # TODO: replace self with a call to parseOrder for unification
        return {
            'info': response,
            'id': str(response['response_data']['order']['order_id']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'order_id': id,
        }
        response = await self.privatePostCancelOrder(self.extend(request, params))
        #
        #     {
        #         response_data: {
        #             order: {
        #                 order_id: 2176769,
        #                 coin_pair: 'BRLBCH',
        #                 order_type: 2,
        #                 status: 3,
        #                 has_fills: False,
        #                 quantity: '0.10000000',
        #                 limit_price: '1996.15999',
        #                 executed_quantity: '0.00000000',
        #                 executed_price_avg: '0.00000',
        #                 fee: '0.00000000',
        #                 created_timestamp: '1536956488',
        #                 updated_timestamp: '1536956499',
        #                 operations: []
        #             }
        #         },
        #         status_code: 100,
        #         server_unix_timestamp: '1536956499'
        #     }
        #
        responseData = self.safe_value(response, 'response_data', {})
        order = self.safe_value(responseData, 'order', {})
        return self.parse_order(order, market)

    def parse_order_status(self, status):
        statuses = {
            '2': 'open',
            '3': 'canceled',
            '4': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "order_id": 4,
        #         "coin_pair": "BRLBTC",
        #         "order_type": 1,
        #         "status": 2,
        #         "has_fills": True,
        #         "quantity": "2.00000000",
        #         "limit_price": "900.00000",
        #         "executed_quantity": "1.00000000",
        #         "executed_price_avg": "900.00000",
        #         "fee": "0.00300000",
        #         "created_timestamp": "1453838494",
        #         "updated_timestamp": "1453838494",
        #         "operations": [
        #             {
        #                 "operation_id": 1,
        #                 "quantity": "1.00000000",
        #                 "price": "900.00000",
        #                 "fee_rate": "0.30",
        #                 "executed_timestamp": "1453838494",
        #             },
        #         ],
        #     }
        #
        id = self.safe_string(order, 'order_id')
        order_type = self.safe_string(order, 'order_type')
        side = None
        if 'order_type' in order:
            side = 'buy' if (order_type == '1') else 'sell'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        marketId = self.safe_string(order, 'coin_pair')
        market = self.safe_market(marketId, market)
        timestamp = self.safe_timestamp(order, 'created_timestamp')
        fee = {
            'cost': self.safe_string(order, 'fee'),
            'currency': market['quote'],
        }
        price = self.safe_string(order, 'limit_price')
        # price = self.safe_number(order, 'executed_price_avg', price)
        average = self.safe_string(order, 'executed_price_avg')
        amount = self.safe_string(order, 'quantity')
        filled = self.safe_string(order, 'executed_quantity')
        lastTradeTimestamp = self.safe_timestamp(order, 'updated_timestamp')
        rawTrades = self.safe_value(order, 'operations', [])
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': market['symbol'],
            'type': 'limit',
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
            'trades': rawTrades,
        }, market)

    async def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'order_id': int(id),
        }
        response = await self.privatePostGetOrder(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        order = self.safe_value(responseData, 'order')
        return self.parse_order(order, market)

    async def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'coin': currency['id'],
            'quantity': format(amount, '.10f'),
            'address': address,
        }
        if code == 'BRL':
            account_ref = ('account_ref' in params)
            if not account_ref:
                raise ArgumentsRequired(self.id + ' withdraw() requires account_ref parameter to withdraw ' + code)
        elif code != 'LTC':
            tx_fee = ('tx_fee' in params)
            if not tx_fee:
                raise ArgumentsRequired(self.id + ' withdraw() requires tx_fee parameter to withdraw ' + code)
            if code == 'XRP':
                if tag is None:
                    if not ('destination_tag' in params):
                        raise ArgumentsRequired(self.id + ' withdraw() requires a tag argument or destination_tag parameter to withdraw ' + code)
                else:
                    request['destination_tag'] = tag
        response = await self.privatePostWithdrawCoin(self.extend(request, params))
        #
        #     {
        #         "response_data": {
        #             "withdrawal": {
        #                 "id": 1,
        #                 "coin": "BRL",
        #                 "quantity": "300.56",
        #                 "net_quantity": "291.68",
        #                 "fee": "8.88",
        #                 "account": "bco: 341, ag: 1111, cta: 23456-X",
        #                 "status": 1,
        #                 "created_timestamp": "1453912088",
        #                 "updated_timestamp": "1453912088"
        #             }
        #         },
        #         "status_code": 100,
        #         "server_unix_timestamp": "1453912088"
        #     }
        #
        responseData = self.safe_value(response, 'response_data', {})
        withdrawal = self.safe_value(responseData, 'withdrawal')
        return self.parse_transaction(withdrawal, currency)

    def parse_transaction(self, transaction, currency=None):
        #
        #     {
        #         "id": 1,
        #         "coin": "BRL",
        #         "quantity": "300.56",
        #         "net_quantity": "291.68",
        #         "fee": "8.88",
        #         "account": "bco: 341, ag: 1111, cta: 23456-X",
        #         "status": 1,
        #         "created_timestamp": "1453912088",
        #         "updated_timestamp": "1453912088"
        #     }
        #
        currency = self.safe_currency(None, currency)
        return {
            'id': self.safe_string(transaction, 'id'),
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

    def parse_ohlcv(self, ohlcv, market=None):
        return [
            self.safe_timestamp(ohlcv, 'timestamp'),
            self.safe_number(ohlcv, 'open'),
            self.safe_number(ohlcv, 'high'),
            self.safe_number(ohlcv, 'low'),
            self.safe_number(ohlcv, 'close'),
            self.safe_number(ohlcv, 'volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'precision': self.timeframes[timeframe],
            'coin': market['id'].lower(),
        }
        if limit is not None and since is not None:
            request['from'] = int(since / 1000)
            request['to'] = self.sum(request['from'], limit * self.parse_timeframe(timeframe))
        elif since is not None:
            request['from'] = int(since / 1000)
            request['to'] = self.sum(self.seconds(), 1)
        elif limit is not None:
            request['to'] = self.seconds()
            request['from'] = request['to'] - (limit * self.parse_timeframe(timeframe))
        response = await self.v4PublicGetCoinCandle(self.extend(request, params))
        candles = self.safe_value(response, 'candles', [])
        return self.parse_ohlcvs(candles, market, timeframe, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
        }
        response = await self.privatePostListOrders(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        orders = self.safe_value(responseData, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'status_list': '[2]',  # open only
        }
        response = await self.privatePostListOrders(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        orders = self.safe_value(responseData, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the mercado api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'has_fills': True,
        }
        response = await self.privatePostListOrders(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        ordersRaw = self.safe_value(responseData, 'orders', [])
        orders = self.parse_orders(ordersRaw, market, since, limit)
        trades = self.orders_to_trades(orders)
        return self.filter_by_symbol_since_limit(trades, market['symbol'], since, limit)

    def orders_to_trades(self, orders):
        result = []
        for i in range(0, len(orders)):
            trades = self.safe_value(orders[i], 'trades', [])
            for y in range(0, len(trades)):
                result.append(trades[y])
        return result

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or (api == 'v4Public'):
            url += self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/'
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'tapi_method': path,
                'tapi_nonce': nonce,
            }, params))
            auth = '/tapi/' + self.version + '/' + '?' + body
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'TAPI-ID': self.apiKey,
                'TAPI-MAC': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        #
        # todo add a unified standard handleErrors with self.exceptions in describe()
        #
        #     {"status":503,"message":"Maintenancing, try again later","result":null}
        #
        errorMessage = self.safe_value(response, 'error_message')
        if errorMessage is not None:
            raise ExchangeError(self.id + ' ' + self.json(response))
