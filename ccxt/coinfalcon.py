# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class coinfalcon(Exchange):

    def describe(self):
        return self.deep_extend(super(coinfalcon, self).describe(), {
            'id': 'coinfalcon',
            'name': 'CoinFalcon',
            'countries': ['GB'],
            'rateLimit': 1000,
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
                'fetchDepositAddress': True,
                'fetchDepositAddresses': False,
                'fetchDeposits': True,
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
                'fetchMyTrades': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTradinFee': False,
                'fetchTradingFees': True,
                'fetchTransfer': False,
                'fetchTransfers': False,
                'fetchWithdrawals': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'transfer': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/41822275-ed982188-77f5-11e8-92bb-496bcd14ca52.jpg',
                'api': {
                    'rest': 'https://coinfalcon.com',
                },
                'www': 'https://coinfalcon.com',
                'doc': 'https://docs.coinfalcon.com',
                'fees': 'https://coinfalcon.com/fees',
                'referral': 'https://coinfalcon.com/?ref=CFJSVGTUPASB',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'markets/{market}',
                        'markets/{market}/orders',
                        'markets/{market}/trades',
                    ],
                },
                'private': {
                    'get': [
                        'user/accounts',
                        'user/orders',
                        'user/orders/{id}',
                        'user/orders/{id}/trades',
                        'user/trades',
                        'user/fees',
                        'account/withdrawals/{id}',
                        'account/withdrawals',
                        'account/deposit/{id}',
                        'account/deposits',
                        'account/deposit_address',
                    ],
                    'post': [
                        'user/orders',
                        'account/withdraw',
                    ],
                    'delete': [
                        'user/orders/{id}',
                        'account/withdrawals/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'maker': 0.0,
                    'taker': 0.002,  # tiered fee starts at 0.2%
                },
            },
            'precision': {
                'amount': self.parse_number('0.00000001'),
                'price': self.parse_number('0.00000001'),
            },
            'precisionMode': TICK_SIZE,
        })

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for coinfalcon
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetMarkets(params)
        #
        #    {
        #        "data": [
        #            {
        #                "name": "ETH-BTC",
        #                "precision": 6,
        #                "min_volume": "0.00000001",
        #                "min_price": "0.000001",
        #                "volume": "0.015713",
        #                "last_price": "0.069322",
        #                "highest_bid": "0.063892",
        #                "lowest_ask": "0.071437",
        #                "change_in_24h": "2.85",
        #                "size_precision": 8,
        #                "price_precision": 6
        #            },
        #            ...
        #        ]
        #    }
        #
        markets = self.safe_value(response, 'data', [])
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId, quoteId = market['name'].split('-')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            result.append({
                'id': market['name'],
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
                    'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'size_precision'))),
                    'price': self.parse_number(self.parse_precision(self.safe_string(market, 'price_precision'))),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(market, 'minPrice'),
                        'max': None,
                    },
                    'price': {
                        'min': self.safe_number(market, 'minVolume'),
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

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "name":"ETH-BTC",
        #         "precision":6,
        #         "min_volume":"0.00000001",
        #         "min_price":"0.000001",
        #         "volume":"0.000452",
        #         "last_price":"0.079059",
        #         "highest_bid":"0.073472",
        #         "lowest_ask":"0.079059",
        #         "change_in_24h":"8.9",
        #         "size_precision":8,
        #         "price_precision":6
        #     }
        #
        marketId = self.safe_string(ticker, 'name')
        market = self.safe_market(marketId, market, '-')
        timestamp = self.milliseconds()
        last = self.safe_string(ticker, 'last_price')
        return self.safe_ticker({
            'symbol': market['symbol'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_string(ticker, 'highest_bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'lowest_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_string(ticker, 'change_in_24h'),
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_string(ticker, 'volume'),
            'info': ticker,
        }, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        tickers = self.fetch_tickers([symbol], params)
        return tickers[symbol]

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        response = self.publicGetMarkets(params)
        #
        #     {
        #         "data":[
        #             {
        #                 "name":"ETH-BTC",
        #                 "precision":6,
        #                 "min_volume":"0.00000001",
        #                 "min_price":"0.000001",
        #                 "volume":"0.000452",
        #                 "last_price":"0.079059",
        #                 "highest_bid":"0.073472",
        #                 "lowest_ask":"0.079059",
        #                 "change_in_24h":"8.9",
        #                 "size_precision":8,
        #                 "price_precision":6
        #             }
        #         ]
        #     }
        #
        tickers = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|float|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'level': '3',
        }
        response = self.publicGetMarketsMarketOrders(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_order_book(data, market['symbol'], None, 'bids', 'asks', 'price', 'size')

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #      {
        #          "id":"5ec36295-5c8d-4874-8d66-2609d4938557",
        #          "price":"4050.06","size":"0.0044",
        #          "market_name":"ETH-USDT",
        #          "side":"sell",
        #          "created_at":"2021-12-07T17:47:36.811000Z"
        #      }
        #
        # fetchMyTrades(private)
        #
        #      {
        #              "id": "0718d520-c796-4061-a16b-915cd13f20c6",
        #              "price": "0.00000358",
        #              "size": "50.0",
        #              "market_name": "DOGE-BTC",
        #              "order_id": "ff2616d8-58d4-40fd-87ae-937c73eb6f1c",
        #              "side": "buy",
        #              "fee': "0.00000036",
        #              "fee_currency_code": "btc",
        #              "liquidity": "T",
        #              "created_at": "2021-12-08T18:26:33.840000Z"
        #      }
        #
        timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'size')
        symbol = market['symbol']
        tradeId = self.safe_string(trade, 'id')
        side = self.safe_string(trade, 'side')
        orderId = self.safe_string(trade, 'order_id')
        fee = None
        feeCostString = self.safe_string(trade, 'fee')
        if feeCostString is not None:
            feeCurrencyCode = self.safe_string(trade, 'fee_currency_code')
            fee = {
                'cost': feeCostString,
                'currency': self.safe_currency_code(feeCurrencyCode),
            }
        return self.safe_trade({
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': tradeId,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': None,
            'fee': fee,
        }, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int|float|None since: the earliest time in ms to fetch trades for
        :param int|float|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since is not None:
            request['start_time'] = self.iso8601(since)
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetUserTrades(self.extend(request, params))
        #
        #      {
        #          "data": [
        #              {
        #                  "id": "0718d520-c796-4061-a16b-915cd13f20c6",
        #                  "price": "0.00000358",
        #                  "size": "50.0",
        #                  "market_name": "DOGE-BTC",
        #                  "order_id": "ff2616d8-58d4-40fd-87ae-937c73eb6f1c",
        #                  "side": "buy",
        #                  "fee': "0.00000036",
        #                  "fee_currency_code": "btc",
        #                  "liquidity": "T",
        #                  "created_at": "2021-12-08T18:26:33.840000Z"
        #              },
        #          ]
        #      }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|float|None since: timestamp in ms of the earliest trade to fetch
        :param int|float|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if since is not None:
            request['since'] = self.iso8601(since)
        response = self.publicGetMarketsMarketTrades(self.extend(request, params))
        #
        #      {
        #          "data":[
        #              {
        #                  "id":"5ec36295-5c8d-4874-8d66-2609d4938557",
        #                  "price":"4050.06","size":"0.0044",
        #                  "market_name":"ETH-USDT",
        #                  "side":"sell",
        #                  "created_at":"2021-12-07T17:47:36.811000Z"
        #              },
        #          ]
        #      }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = self.privateGetUserFees(params)
        #
        #    {
        #        data: {
        #            maker_fee: '0.0',
        #            taker_fee: '0.2',
        #            btc_volume_30d: '0.0'
        #        }
        #    }
        #
        data = self.safe_value(response, 'data', {})
        makerString = self.safe_string(data, 'maker_fee')
        takerString = self.safe_string(data, 'taker_fee')
        maker = self.parse_number(Precise.string_div(makerString, '100'))
        taker = self.parse_number(Precise.string_div(takerString, '100'))
        result = {}
        for i in range(0, len(self.symbols)):
            symbol = self.symbols[i]
            result[symbol] = {
                'info': response,
                'symbol': symbol,
                'maker': maker,
                'taker': taker,
                'percentage': True,
                'tierBased': True,
            }
        return result

    def parse_balance(self, response):
        result = {'info': response}
        balances = self.safe_value(response, 'data', [])
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency_code')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'available_balance')
            account['used'] = self.safe_string(balance, 'hold_balance')
            account['total'] = self.safe_string(balance, 'balance')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privateGetUserAccounts(params)
        return self.parse_balance(response)

    def parse_deposit_address(self, depositAddress, currency=None):
        #
        #     {
        #         "address":"0x77b5051f97efa9cc52c9ad5b023a53fc15c200d3",
        #         "tag":"0"
        #     }
        #
        address = self.safe_string(depositAddress, 'address')
        tag = self.safe_string(depositAddress, 'tag')
        self.check_address(address)
        return {
            'currency': self.safe_currency_code(None, currency),
            'address': address,
            'tag': tag,
            'network': None,
            'info': depositAddress,
        }

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.safe_currency(code)
        request = {
            'currency': self.safe_string_lower(currency, 'id'),
        }
        response = self.privateGetAccountDepositAddress(self.extend(request, params))
        #
        #     {
        #         data: {
        #             address: '0x9918987bbe865a1a9301dc736cf6cf3205956694',
        #             tag:null
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_deposit_address(data, currency)

    def parse_order_status(self, status):
        statuses = {
            'fulfilled': 'closed',
            'canceled': 'canceled',
            'pending': 'open',
            'open': 'open',
            'partially_filled': 'open',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "id":"8bdd79f4-8414-40a2-90c3-e9f4d6d1eef4"
        #         "market":"IOT-BTC"
        #         "price":"0.0000003"
        #         "size":"4.0"
        #         "size_filled":"3.0"
        #         "fee":"0.0075"
        #         "fee_currency_code":"iot"
        #         "funds":"0.0"
        #         "status":"canceled"
        #         "order_type":"buy"
        #         "post_only":false
        #         "operation_type":"market_order"
        #         "created_at":"2018-01-12T21:14:06.747828Z"
        #     }
        #
        marketId = self.safe_string(order, 'market')
        symbol = self.safe_symbol(marketId, market, '-')
        timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        priceString = self.safe_string(order, 'price')
        amountString = self.safe_string(order, 'size')
        filledString = self.safe_string(order, 'size_filled')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        type = self.safe_string(order, 'operation_type')
        if type is not None:
            type = type.split('_')
            type = type[0]
        side = self.safe_string(order, 'order_type')
        postOnly = self.safe_value(order, 'post_only')
        return self.safe_order({
            'id': self.safe_string(order, 'id'),
            'clientOrderId': None,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'postOnly': postOnly,
            'side': side,
            'price': priceString,
            'stopPrice': None,
            'cost': None,
            'amount': amountString,
            'filled': filledString,
            'remaining': None,
            'trades': None,
            'fee': None,
            'info': order,
            'lastTradeTimestamp': None,
            'average': None,
        }, market)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param int|float amount: how much of currency you want to trade in units of base currency
        :param int|float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        # price/size must be string
        request = {
            'market': market['id'],
            'size': self.amount_to_precision(symbol, amount),
            'order_type': side,
        }
        if type == 'limit':
            price = self.price_to_precision(symbol, price)
            request['price'] = str(price)
        request['operation_type'] = type + '_order'
        response = self.privatePostUserOrders(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_order(data, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateDeleteUserOrdersId(self.extend(request, params))
        market = self.market(symbol)
        data = self.safe_value(response, 'data', {})
        return self.parse_order(data, market)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateGetUserOrdersId(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_order(data)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|float|None since: the earliest time in ms to fetch open orders for
        :param int|float|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        if since is not None:
            request['since_time'] = self.iso8601(since)
        # TODO: test status=all if it works for closed orders too
        response = self.privateGetUserOrders(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        orders = self.filter_by_array(data, 'status', ['pending', 'open', 'partially_filled'], False)
        return self.parse_orders(orders, market, since, limit)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|float|None since: the earliest time in ms to fetch deposits for
        :param int|float|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {
            # currency: 'xrp',  # optional: currency code in lowercase
            # status: 'completed',  # optional: withdrawal status
            # since_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
            # end_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
            # start_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
        }
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = self.safe_string_lower(currency, 'id')
        if since is not None:
            request['since_time'] = self.iso8601(since)
        response = self.privateGetAccountDeposits(self.extend(request, params))
        #
        #     data: [
        #         {
        #             id: '6e2f18b5-f80e-xxx-xxx-xxx',
        #             amount: '0.1',
        #             status: 'completed',
        #             currency_code: 'eth',
        #             txid: '0xxxx',
        #             address: '0xxxx',
        #             tag: null,
        #             type: 'deposit'
        #         },
        #     ]
        #
        transactions = self.safe_value(response, 'data', [])
        transactions.reverse()  # no timestamp but in reversed order
        return self.parse_transactions(transactions, currency, None, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|float|None since: the earliest time in ms to fetch withdrawals for
        :param int|float|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {
            # currency: 'xrp',  # optional: currency code in lowercase
            # status: 'completed',  # optional: withdrawal status
            # since_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
            # end_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
            # start_time  # datetime in ISO8601 format(2017-11-06T09:53:08.383210Z)
        }
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = self.safe_string_lower(currency, 'id')
        if since is not None:
            request['since_time'] = self.iso8601(since)
        response = self.privateGetAccountWithdrawals(self.extend(request, params))
        #
        #     data: [
        #         {
        #             id: '25f6f144-3666-xxx-xxx-xxx',
        #             amount: '0.01',
        #             status: 'completed',
        #             fee: '0.0005',
        #             currency_code: 'btc',
        #             txid: '4xxx',
        #             address: 'bc1xxx',
        #             tag: null,
        #             type: 'withdraw'
        #         },
        #     ]
        #
        transactions = self.safe_value(response, 'data', [])
        transactions.reverse()  # no timestamp but in reversed order
        return self.parse_transactions(transactions, currency, None, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param int|float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the coinfalcon api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': self.safe_string_lower(currency, 'id'),
            'address': address,
            'amount': amount,
            # 'tag': 'string',  # withdraw tag/memo
        }
        if tag is not None:
            request['tag'] = tag
        response = self.privatePostAccountWithdraw(self.extend(request, params))
        #
        #     data: [
        #         {
        #             id: '25f6f144-3666-xxx-xxx-xxx',
        #             amount: '0.01',
        #             status: 'approval_pending',
        #             fee: '0.0005',
        #             currency_code: 'btc',
        #             txid: null,
        #             address: 'bc1xxx',
        #             tag: null,
        #             type: 'withdraw'
        #         },
        #     ]
        #
        transaction = self.safe_value(response, 'data', [])
        return self.parse_transaction(transaction, currency)

    def parse_transaction_status(self, status):
        statuses = {
            'completed': 'ok',
            'denied': 'failed',
            'approval_pending': 'pending',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchWithdrawals, withdraw
        #
        #     {
        #         id: '25f6f144-3666-xxx-xxx-xxx',
        #         amount: '0.01',
        #         status: 'completed',
        #         fee: '0.0005',
        #         currency_code: 'btc',
        #         txid: '4xxx',
        #         address: 'bc1xxx',
        #         tag: null,
        #         type: 'withdraw'
        #     },
        #
        # fetchDeposits
        #
        #     {
        #         id: '6e2f18b5-f80e-xxx-xxx-xxx',
        #         amount: '0.1',
        #         status: 'completed',
        #         currency_code: 'eth',
        #         txid: '0xxxx',
        #         address: '0xxxx',
        #         tag: null,
        #         type: 'deposit'
        #     },
        #
        id = self.safe_string(transaction, 'id')
        address = self.safe_string(transaction, 'address')
        tag = self.safe_string(transaction, 'tag')
        txid = self.safe_string(transaction, 'txid')
        currencyId = self.safe_string(transaction, 'currency_code')
        code = self.safe_currency_code(currencyId, currency)
        type = self.safe_string(transaction, 'type')
        if type == 'withdraw':
            type = 'withdrawal'
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        amountString = self.safe_string(transaction, 'amount')
        amount = self.parse_number(amountString)
        feeCostString = self.safe_string(transaction, 'fee')
        feeCost = 0
        if feeCostString is not None:
            feeCost = self.parse_number(feeCostString)
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': None,
            'datetime': None,
            'network': None,
            'address': address,
            'addressTo': None,
            'addressFrom': None,
            'tag': tag,
            'tagTo': None,
            'tagFrom': None,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': None,
            'fee': {
                'currency': code,
                'cost': feeCost,
            },
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/api/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                request += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    request += '?' + self.urlencode(query)
            else:
                body = self.json(query)
            seconds = str(self.seconds())
            payload = '|'.join([seconds, method, request])
            if body:
                payload += '|' + body
            signature = self.hmac(self.encode(payload), self.encode(self.secret))
            headers = {
                'CF-API-KEY': self.apiKey,
                'CF-API-TIMESTAMP': seconds,
                'CF-API-SIGNATURE': signature,
                'Content-Type': 'application/json',
            }
        url = self.urls['api']['rest'] + request
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if code < 400:
            return
        ErrorClass = self.safe_value({
            '401': AuthenticationError,
            '429': RateLimitExceeded,
        }, code, ExchangeError)
        raise ErrorClass(body)
