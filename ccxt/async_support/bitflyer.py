# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.abstract.bitflyer import ImplicitAPI
import hashlib
from ccxt.base.types import OrderSide
from typing import Optional
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import TICK_SIZE


class bitflyer(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(bitflyer, self).describe(), {
            'id': 'bitflyer',
            'name': 'bitFlyer',
            'countries': ['JP'],
            'version': 'v1',
            'rateLimit': 1000,  # their nonce-timestamp is in seconds...
            'hostname': 'bitflyer.com',  # or bitflyer.com
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': None,  # has but not fully implemented
                'future': None,  # has but not fully implemented
                'option': False,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': 'emulated',
                'fetchDeposits': True,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': 'emulated',
                'fetchOrder': 'emulated',
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchPositionMode': False,
                'fetchPositions': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': True,
                'fetchTradingFees': False,
                'fetchTransfer': False,
                'fetchTransfers': False,
                'fetchWithdrawals': True,
                'transfer': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28051642-56154182-660e-11e7-9b0d-6042d1e6edd8.jpg',
                'api': {
                    'rest': 'https://api.{hostname}',
                },
                'www': 'https://bitflyer.com',
                'doc': 'https://lightning.bitflyer.com/docs?lang=en',
            },
            'api': {
                'public': {
                    'get': [
                        'getmarkets/usa',  # new(wip)
                        'getmarkets/eu',  # new(wip)
                        'getmarkets',     # or 'markets'
                        'getboard',       # ...
                        'getticker',
                        'getexecutions',
                        'gethealth',
                        'getboardstate',
                        'getchats',
                    ],
                },
                'private': {
                    'get': [
                        'getpermissions',
                        'getbalance',
                        'getbalancehistory',
                        'getcollateral',
                        'getcollateralhistory',
                        'getcollateralaccounts',
                        'getaddresses',
                        'getcoinins',
                        'getcoinouts',
                        'getbankaccounts',
                        'getdeposits',
                        'getwithdrawals',
                        'getchildorders',
                        'getparentorders',
                        'getparentorder',
                        'getexecutions',
                        'getpositions',
                        'gettradingcommission',
                    ],
                    'post': [
                        'sendcoin',
                        'withdraw',
                        'sendchildorder',
                        'cancelchildorder',
                        'sendparentorder',
                        'cancelparentorder',
                        'cancelallchildorders',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.002'),
                    'taker': self.parse_number('0.002'),
                },
            },
            'precisionMode': TICK_SIZE,
        })

    def parse_expiry_date(self, expiry):
        day = expiry[0:2]
        monthName = expiry[2:5]
        year = expiry[5:9]
        months = {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12',
        }
        month = self.safe_string(months, monthName)
        return self.parse8601(year + '-' + month + '-' + day + 'T00:00:00Z')

    def safe_market(self, marketId=None, market=None, delimiter=None, marketType=None):
        # Bitflyer has a different type of conflict in markets, because
        # some of their ids(ETH/BTC and BTC/JPY) are duplicated in US, EU and JP.
        # Since they're the same we just need to return one
        return super(bitflyer, self).safe_market(marketId, market, delimiter, 'spot')

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bitflyer
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        jp_markets = await self.publicGetGetmarkets(params)
        #
        #     [
        #         # spot
        #         {"product_code": "BTC_JPY", "market_type": "Spot"},
        #         {"product_code": "BCH_BTC", "market_type": "Spot"},
        #         # forex swap
        #         {"product_code": "FX_BTC_JPY", "market_type": "FX"},
        #         # future
        #         {
        #             "product_code": "BTCJPY11FEB2022",
        #             "alias": "BTCJPY_MAT1WK",
        #             "market_type": "Futures",
        #         },
        #     ]
        #
        us_markets = await self.publicGetGetmarketsUsa(params)
        #
        #     [
        #         {"product_code": "BTC_USD", "market_type": "Spot"},
        #         {"product_code": "BTC_JPY", "market_type": "Spot"},
        #     ]
        #
        eu_markets = await self.publicGetGetmarketsEu(params)
        #
        #     [
        #         {"product_code": "BTC_EUR", "market_type": "Spot"},
        #         {"product_code": "BTC_JPY", "market_type": "Spot"},
        #     ]
        #
        markets = self.array_concat(jp_markets, us_markets)
        markets = self.array_concat(markets, eu_markets)
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'product_code')
            currencies = id.split('_')
            marketType = self.safe_string(market, 'market_type')
            swap = (marketType == 'FX')
            future = (marketType == 'Futures')
            spot = not swap and not future
            type = 'spot'
            settle = None
            baseId = None
            quoteId = None
            expiry = None
            if spot:
                baseId = self.safe_string(currencies, 0)
                quoteId = self.safe_string(currencies, 1)
            elif swap:
                type = 'swap'
                baseId = self.safe_string(currencies, 1)
                quoteId = self.safe_string(currencies, 2)
            elif future:
                alias = self.safe_string(market, 'alias')
                if alias is None:
                    # no alias:
                    # {product_code: 'BTCJPY11MAR2022', market_type: 'Futures'}
                    # TODO self will break if there are products with 4 chars
                    baseId = id[0:3]
                    quoteId = id[3:6]
                    # last 9 chars are expiry date
                    expiryDate = id[-9:]
                    expiry = self.parse_expiry_date(expiryDate)
                else:
                    splitAlias = alias.split('_')
                    currencyIds = self.safe_string(splitAlias, 0)
                    baseId = currencyIds[0:-3]
                    quoteId = currencyIds[-3:]
                    splitId = id.split(currencyIds)
                    expiryDate = self.safe_string(splitId, 1)
                    expiry = self.parse_expiry_date(expiryDate)
                type = 'future'
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            taker = self.fees['trading']['taker']
            maker = self.fees['trading']['maker']
            contract = swap or future
            if contract:
                maker = 0.0
                taker = 0.0
                settle = 'JPY'
                symbol = symbol + ':' + settle
                if future:
                    symbol = symbol + '-' + self.yymmdd(expiry)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'settle': settle,
                'baseId': baseId,
                'quoteId': quoteId,
                'settleId': None,
                'type': type,
                'spot': spot,
                'margin': False,
                'swap': swap,
                'future': future,
                'option': False,
                'active': True,
                'contract': contract,
                'linear': None if spot else True,
                'inverse': None if spot else False,
                'taker': taker,
                'maker': maker,
                'contractSize': None,
                'expiry': expiry,
                'expiryDatetime': self.iso8601(expiry),
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': None,
                    'price': None,
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': None,
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
                'info': market,
            })
        return result

    def parse_balance(self, response):
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_string(balance, 'amount')
            account['free'] = self.safe_string(balance, 'available')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privateGetGetbalance(params)
        #
        #     [
        #         {
        #             "currency_code": "JPY",
        #             "amount": 1024078,
        #             "available": 508000
        #         },
        #         {
        #             "currency_code": "BTC",
        #             "amount": 10.24,
        #             "available": 4.12
        #         },
        #         {
        #             "currency_code": "ETH",
        #             "amount": 20.48,
        #             "available": 16.38
        #         }
        #     ]
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        orderbook = await self.publicGetGetboard(self.extend(request, params))
        return self.parse_order_book(orderbook, market['symbol'], None, 'bids', 'asks', 'price', 'size')

    def parse_ticker(self, ticker, market=None):
        symbol = self.safe_symbol(None, market)
        timestamp = self.parse8601(self.safe_string(ticker, 'timestamp'))
        last = self.safe_string(ticker, 'ltp')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_string(ticker, 'best_bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'best_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume_by_product'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol: str, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        response = await self.publicGetGetticker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public) v1
        #
        #     {
        #          "id":2278466664,
        #          "side":"SELL",
        #          "price":56810.7,
        #          "size":0.08798,
        #          "exec_date":"2021-11-19T11:46:39.323",
        #          "buy_child_order_acceptance_id":"JRF20211119-114209-236525",
        #          "sell_child_order_acceptance_id":"JRF20211119-114639-236919"
        #      }
        #
        #      {
        #          "id":2278463423,
        #          "side":"BUY",
        #          "price":56757.83,
        #          "size":0.6003,"exec_date":"2021-11-19T11:28:00.523",
        #          "buy_child_order_acceptance_id":"JRF20211119-112800-236526",
        #          "sell_child_order_acceptance_id":"JRF20211119-112734-062017"
        #      }
        #
        #
        #
        side = self.safe_string_lower(trade, 'side')
        if side is not None:
            if len(side) < 1:
                side = None
        order = None
        if side is not None:
            idInner = side + '_child_order_acceptance_id'
            if idInner in trade:
                order = trade[idInner]
        if order is None:
            order = self.safe_string(trade, 'child_order_acceptance_id')
        timestamp = self.parse8601(self.safe_string(trade, 'exec_date'))
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'size')
        id = self.safe_string(trade, 'id')
        market = self.safe_market(None, market)
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': order,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': None,
        }, market)

    async def fetch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        response = await self.publicGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_trading_fee(self, symbol: str, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/#/?id=fee-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        response = await self.privateGetGettradingcommission(self.extend(request, params))
        #
        #   {
        #       commission_rate: '0.0020'
        #   }
        #
        fee = self.safe_number(response, 'commission_rate')
        return {
            'info': response,
            'symbol': market['symbol'],
            'maker': fee,
            'taker': fee,
        }

    async def create_order(self, symbol: str, type, side: OrderSide, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_type': type.upper(),
            'side': side.upper(),
            'price': price,
            'size': amount,
        }
        result = await self.privatePostSendchildorder(self.extend(request, params))
        # {"status": - 200, "error_message": "Insufficient funds", "data": null}
        id = self.safe_string(result, 'child_order_acceptance_id')
        return self.safe_order({
            'id': id,
            'info': result,
        })

    async def cancel_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a `symbol` argument')
        await self.load_markets()
        request = {
            'product_code': self.market_id(symbol),
            'child_order_acceptance_id': id,
        }
        return await self.privatePostCancelchildorder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'ACTIVE': 'open',
            'COMPLETED': 'closed',
            'CANCELED': 'canceled',
            'EXPIRED': 'canceled',
            'REJECTED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(self.safe_string(order, 'child_order_date'))
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'size')
        filled = self.safe_string(order, 'executed_size')
        remaining = self.safe_string(order, 'outstanding_size')
        status = self.parse_order_status(self.safe_string(order, 'child_order_state'))
        type = self.safe_string_lower(order, 'child_order_type')
        side = self.safe_string_lower(order, 'side')
        marketId = self.safe_string(order, 'product_code')
        symbol = self.safe_symbol(marketId, market)
        fee = None
        feeCost = self.safe_number(order, 'total_commission')
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': None,
                'rate': None,
            }
        id = self.safe_string(order, 'child_order_acceptance_id')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'info': order,
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
            'triggerPrice': None,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
            'average': None,
            'trades': None,
        }, market)

    async def fetch_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit=100, params={}):
        """
        fetches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
            'count': limit,
        }
        response = await self.privateGetGetchildorders(self.extend(request, params))
        orders = self.parse_orders(response, market, since, limit)
        if symbol is not None:
            orders = self.filter_by(orders, 'symbol', symbol)
        return orders

    async def fetch_open_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit=100, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'child_order_state': 'ACTIVE',
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol: Optional[str] = None, since: Optional[int] = None, limit=100, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'child_order_state': 'COMPLETED',
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_order(self, id: str, symbol: Optional[str] = None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a `symbol` argument')
        orders = await self.fetch_orders(symbol)
        ordersById = self.index_by(orders, 'id')
        if id in ordersById:
            return ordersById[id]
        raise OrderNotFound(self.id + ' No order found with id ' + id)

    async def fetch_my_trades(self, symbol: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/#/?id=trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'product_code': market['id'],
        }
        if limit is not None:
            request['count'] = limit
        response = await self.privateGetGetexecutions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_positions(self, symbols: Optional[List[str]] = None, params={}):
        """
        fetch all open positions
        :param [str] symbols: list of unified market symbols
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `position structure <https://docs.ccxt.com/#/?id=position-structure>`
        """
        if symbols is None:
            raise ArgumentsRequired(self.id + ' fetchPositions() requires a `symbols` argument, exactly one symbol in an array')
        await self.load_markets()
        request = {
            'product_code': self.market_ids(symbols),
        }
        response = await self.privateGetGetpositions(self.extend(request, params))
        #
        #     [
        #         {
        #             "product_code": "FX_BTC_JPY",
        #             "side": "BUY",
        #             "price": 36000,
        #             "size": 10,
        #             "commission": 0,
        #             "swap_point_accumulate": -35,
        #             "require_collateral": 120000,
        #             "open_date": "2015-11-03T10:04:45.011",
        #             "leverage": 3,
        #             "pnl": 965,
        #             "sfd": -0.5
        #         }
        #     ]
        #
        # todo unify parsePosition/parsePositions
        return response

    async def withdraw(self, code: str, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        self.check_address(address)
        await self.load_markets()
        if code != 'JPY' and code != 'USD' and code != 'EUR':
            raise ExchangeError(self.id + ' allows withdrawing JPY, USD, EUR only, ' + code + ' is not supported')
        currency = self.currency(code)
        request = {
            'currency_code': currency['id'],
            'amount': amount,
            # 'bank_account_id': 1234,
        }
        response = await self.privatePostWithdraw(self.extend(request, params))
        #
        #     {
        #         "message_id": "69476620-5056-4003-bcbe-42658a2b041b"
        #     }
        #
        return self.parse_transaction(response, currency)

    async def fetch_deposits(self, code: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        await self.load_markets()
        currency = None
        request = {}
        if code is not None:
            currency = self.currency(code)
        if limit is not None:
            request['count'] = limit  # default 100
        response = await self.privateGetGetcoinins(self.extend(request, params))
        #
        #     [
        #         {
        #             "id": 100,
        #             "order_id": "CDP20151227-024141-055555",
        #             "currency_code": "BTC",
        #             "amount": 0.00002,
        #             "address": "1WriteySQufKZ2pVuM1oMhPrTtTVFq35j",
        #             "tx_hash": "9f92ee65a176bb9545f7becb8706c50d07d4cee5ffca34d8be3ef11d411405ae",
        #             "status": "COMPLETED",
        #             "event_date": "2015-11-27T08:59:20.301"
        #         }
        #     ]
        #
        return self.parse_transactions(response, currency, since, limit)

    async def fetch_withdrawals(self, code: Optional[str] = None, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bitflyer api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        await self.load_markets()
        currency = None
        request = {}
        if code is not None:
            currency = self.currency(code)
        if limit is not None:
            request['count'] = limit  # default 100
        response = await self.privateGetGetcoinouts(self.extend(request, params))
        #
        #     [
        #         {
        #             "id": 500,
        #             "order_id": "CWD20151224-014040-077777",
        #             "currency_code": "BTC",
        #             "amount": 0.1234,
        #             "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        #             "tx_hash": "724c07dfd4044abcb390b0412c3e707dd5c4f373f0a52b3bd295ce32b478c60a",
        #             "fee": 0.0005,
        #             "additional_fee": 0.0001,
        #             "status": "COMPLETED",
        #             "event_date": "2015-12-24T01:40:40.397"
        #         }
        #     ]
        #
        return self.parse_transactions(response, currency, since, limit)

    def parse_deposit_status(self, status):
        statuses = {
            'PENDING': 'pending',
            'COMPLETED': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_withdrawal_status(self, status):
        statuses = {
            'PENDING': 'pending',
            'COMPLETED': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #     {
        #         "id": 100,
        #         "order_id": "CDP20151227-024141-055555",
        #         "currency_code": "BTC",
        #         "amount": 0.00002,
        #         "address": "1WriteySQufKZ2pVuM1oMhPrTtTVFq35j",
        #         "tx_hash": "9f92ee65a176bb9545f7becb8706c50d07d4cee5ffca34d8be3ef11d411405ae",
        #         "status": "COMPLETED",
        #         "event_date": "2015-11-27T08:59:20.301"
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         "id": 500,
        #         "order_id": "CWD20151224-014040-077777",
        #         "currency_code": "BTC",
        #         "amount": 0.1234,
        #         "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        #         "tx_hash": "724c07dfd4044abcb390b0412c3e707dd5c4f373f0a52b3bd295ce32b478c60a",
        #         "fee": 0.0005,
        #         "additional_fee": 0.0001,
        #         "status": "COMPLETED",
        #         "event_date": "2015-12-24T01:40:40.397"
        #     }
        #
        # withdraw
        #
        #     {
        #         "message_id": "69476620-5056-4003-bcbe-42658a2b041b"
        #     }
        #
        id = self.safe_string_2(transaction, 'id', 'message_id')
        address = self.safe_string(transaction, 'address')
        currencyId = self.safe_string(transaction, 'currency_code')
        code = self.safe_currency_code(currencyId, currency)
        timestamp = self.parse8601(self.safe_string(transaction, 'event_date'))
        amount = self.safe_number(transaction, 'amount')
        txId = self.safe_string(transaction, 'tx_hash')
        rawStatus = self.safe_string(transaction, 'status')
        type = None
        status = None
        fee = None
        if 'fee' in transaction:
            type = 'withdrawal'
            status = self.parse_withdrawal_status(rawStatus)
            feeCost = self.safe_number(transaction, 'fee')
            additionalFee = self.safe_number(transaction, 'additional_fee')
            fee = {'currency': code, 'cost': feeCost + additionalFee}
        else:
            type = 'deposit'
            status = self.parse_deposit_status(rawStatus)
        return {
            'info': transaction,
            'id': id,
            'txid': txId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'network': None,
            'address': address,
            'addressTo': address,
            'addressFrom': None,
            'tag': None,
            'tagTo': None,
            'tagFrom': None,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'internal': None,
            'fee': fee,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.version + '/'
        if api == 'private':
            request += 'me/'
        request += path
        if method == 'GET':
            if params:
                request += '?' + self.urlencode(params)
        baseUrl = self.implode_hostname(self.urls['api']['rest'])
        url = baseUrl + request
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = ''.join([nonce, method, request])
            if params:
                if method != 'GET':
                    body = self.json(params)
                    auth += body
            headers = {
                'ACCESS-KEY': self.apiKey,
                'ACCESS-TIMESTAMP': nonce,
                'ACCESS-SIGN': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256),
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
