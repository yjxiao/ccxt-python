# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported


class kuna(Exchange):

    def describe(self):
        return self.deep_extend(super(kuna, self).describe(), {
            'id': 'kuna',
            'name': 'Kuna',
            'countries': ['UA'],
            'rateLimit': 1000,
            'version': 'v2',
            'has': {
                'CORS': None,
                'spot': True,
                'margin': None,
                'swap': False,
                'future': False,
                'option': False,
                'cancelOrder': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchL3OrderBook': True,
                'fetchLeverage': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOHLCV': 'emulated',
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setPositionMode': False,
                'withdraw': None,
            },
            'timeframes': None,
            'urls': {
                'extension': '.json',
                'referral': 'https://kuna.io?r=kunaid-gvfihe8az7o4',
                'logo': 'https://user-images.githubusercontent.com/51840849/87153927-f0578b80-c2c0-11ea-84b6-74612568e9e1.jpg',
                'api': {
                    'xreserve': 'https://api.xreserve.fund',
                    'v3': 'https://api.kuna.io',
                    'public': 'https://kuna.io',  # v2
                    'private': 'https://kuna.io',  # v2
                },
                'www': 'https://kuna.io',
                'doc': 'https://kuna.io/documents/api',
                'fees': 'https://kuna.io/documents/api',
            },
            'api': {
                'xreserve': {
                    'get': {
                        'nonce': 1,
                        'fee': 1,
                        'delegated-transactions': 1,
                    },
                    'post': {
                        'delegate-transfer': 1,
                    },
                },
                'v3': {
                    'public': {
                        'get': {
                            'timestamp': 1,
                            'currencies': 1,
                            'markets': 1,
                            'tickers': 1,
                            'k': 1,
                            'trades_history': 1,
                            'fees': 1,
                            'exchange-rates': 1,
                            'exchange-rates/currency': 1,
                            'book/market': 1,
                            'kuna_codes/code/check': 1,
                            'landing_page_statistic': 1,
                            'translations/locale': 1,
                            'trades/market/hist': 1,
                        },
                        'post': {
                            'http_test': 1,
                            'deposit_channels': 1,
                            'withdraw_channels': 1,
                            'subscription_plans': 1,
                            'send_to': 1,
                            'confirm_token': 1,
                            'kunaid': 1,
                            'withdraw/prerequest': 1,
                            'deposit/prerequest': 1,
                            'deposit/exchange-rates': 1,
                        },
                    },
                    'sign': {
                        'get': {
                            'reset_password/token': 1,
                        },
                        'post': {
                            'signup/google': 1,
                            'signup/resend_confirmation': 1,
                            'signup': 1,
                            'signin': 1,
                            'signin/two_factor': 1,
                            'signin/resend_confirm_device': 1,
                            'signin/confirm_device': 1,
                            'reset_password': 1,
                            'cool-signin': 1,
                        },
                        'put': {
                            'reset_password/token': 1,
                            'signup/code/confirm': 1,
                        },
                    },
                    'private': {
                        'post': {
                            'auth/w/order/submit': 1,
                            'auth/r/orders': 1,
                            'auth/r/orders/market': 1,
                            'auth/r/orders/markets': 1,
                            'auth/api_tokens/delete': 1,
                            'auth/api_tokens/create': 1,
                            'auth/api_tokens': 1,
                            'auth/signin_history/uniq': 1,
                            'auth/signin_history': 1,
                            'auth/disable_withdraw_confirmation': 1,
                            'auth/change_password': 1,
                            'auth/deposit_address': 1,
                            'auth/announcements/accept': 1,
                            'auth/announcements/unaccepted': 1,
                            'auth/otp/deactivate': 1,
                            'auth/otp/activate': 1,
                            'auth/otp/secret': 1,
                            'auth/r/order/market/:order_id/trades': 1,
                            'auth/r/orders/market/hist': 1,
                            'auth/r/orders/hist': 1,
                            'auth/r/orders/hist/markets': 1,
                            'auth/r/orders/details': 1,
                            'auth/assets-history': 1,
                            'auth/assets-history/withdraws': 1,
                            'auth/assets-history/deposits': 1,
                            'auth/r/wallets': 1,
                            'auth/markets/favorites': 1,
                            'auth/markets/favorites/list': 1,
                            'auth/me/update': 1,
                            'auth/me': 1,
                            'auth/fund_sources': 1,
                            'auth/fund_sources/list': 1,
                            'auth/withdraw/resend_confirmation': 1,
                            'auth/withdraw': 1,
                            'auth/withdraw/details': 1,
                            'auth/withdraw/info': 1,
                            'auth/payment_addresses': 1,
                            'auth/deposit/prerequest': 1,
                            'auth/deposit/exchange-rates': 1,
                            'auth/deposit': 1,
                            'auth/deposit/details': 1,
                            'auth/deposit/info': 1,
                            'auth/kuna_codes/count': 1,
                            'auth/kuna_codes/details': 1,
                            'auth/kuna_codes/edit': 1,
                            'auth/kuna_codes/send-pdf': 1,
                            'auth/kuna_codes': 1,
                            'auth/kuna_codes/redeemed-by-me': 1,
                            'auth/kuna_codes/issued-by-me': 1,
                            'auth/payment_requests/invoice': 1,
                            'auth/payment_requests/type': 1,
                            'auth/referral_program/weekly_earnings': 1,
                            'auth/referral_program/stats': 1,
                            'auth/merchant/payout_services': 1,
                            'auth/merchant/withdraw': 1,
                            'auth/merchant/payment_services': 1,
                            'auth/merchant/deposit': 1,
                            'auth/verification/auth_token': 1,
                            'auth/kunaid_purchase/create': 1,
                            'auth/devices/list': 1,
                            'auth/sessions/list': 1,
                            'auth/subscriptions/reactivate': 1,
                            'auth/subscriptions/cancel': 1,
                            'auth/subscriptions/prolong': 1,
                            'auth/subscriptions/create': 1,
                            'auth/subscriptions/list': 1,
                            'auth/kuna_ids/list': 1,
                            'order/cancel/multi': 1,
                            'order/cancel': 1,
                        },
                        'put': {
                            'auth/fund_sources/id': 1,
                            'auth/kuna_codes/redeem': 1,
                        },
                        'delete': {
                            'auth/markets/favorites': 1,
                            'auth/fund_sources': 1,
                            'auth/devices': 1,
                            'auth/devices/list': 1,
                            'auth/sessions/list': 1,
                            'auth/sessions': 1,
                        },
                    },
                },
                'public': {
                    'get': [
                        'depth',  # Get depth or specified market Both asks and bids are sorted from highest price to lowest.
                        'k_with_pending_trades',  # Get K data with pending trades, which are the trades not included in K data yet, because there's delay between trade generated and processed by K data generator
                        'k',  # Get OHLC(k line) of specific market
                        'markets',  # Get all available markets
                        'order_book',  # Get the order book of specified market
                        'order_book/{market}',
                        'tickers',  # Get ticker of all markets
                        'tickers/{market}',  # Get ticker of specific market
                        'timestamp',  # Get server current time, in seconds since Unix epoch
                        'trades',  # Get recent trades on market, each trade is included only once Trades are sorted in reverse creation order.
                        'trades/{market}',
                    ],
                },
                'private': {
                    'get': [
                        'members/me',  # Get your profile and accounts info
                        'deposits',  # Get your deposits history
                        'deposit',  # Get details of specific deposit
                        'deposit_address',  # Where to deposit The address field could be empty when a new address is generating(e.g. for bitcoin), you should try again later in that case.
                        'orders',  # Get your orders, results is paginated
                        'order',  # Get information of specified order
                        'trades/my',  # Get your executed trades Trades are sorted in reverse creation order.
                        'withdraws',  # Get your cryptocurrency withdraws
                        'withdraw',  # Get your cryptocurrency withdraw
                    ],
                    'post': [
                        'orders',  # Create a Sell/Buy order
                        'orders/multi',  # Create multiple sell/buy orders
                        'orders/clear',  # Cancel all my orders
                        'order/delete',  # Cancel an order
                        'withdraw',  # Create a withdraw
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': self.parse_number('0.0025'),
                    'maker': self.parse_number('0.0025'),
                },
                'funding': {
                    'withdraw': {
                        'UAH': '1%',
                        'BTC': 0.001,
                        'BCH': 0.001,
                        'ETH': 0.01,
                        'WAVES': 0.01,
                        'GOL': 0.0,
                        'GBG': 0.0,
                        # 'RMC': 0.001 BTC
                        # 'ARN': 0.01 ETH
                        # 'R': 0.01 ETH
                        # 'EVR': 0.01 ETH
                    },
                    'deposit': {
                        # 'UAH': (amount) => amount * 0.001 + 5
                    },
                },
            },
            'commonCurrencies': {
                'PLA': 'Plair',
            },
            'exceptions': {
                '2002': InsufficientFunds,
                '2003': OrderNotFound,
            },
        })

    async def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = await self.publicGetTimestamp(params)
        #
        #     1594911427
        #
        return response * 1000

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for kuna
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        quotes = ['btc', 'rub', 'uah', 'usd', 'usdt', 'usdc']
        markets = []
        response = await self.publicGetTickers(params)
        #
        #    {
        #        shibuah: {
        #            at: '1644463685',
        #            ticker: {
        #                buy: '0.000911',
        #                sell: '0.00092',
        #                low: '0.000872',
        #                high: '0.000963',
        #                last: '0.000911',
        #                vol: '1539278096.0',
        #                price: '1434244.211249'
        #            }
        #        }
        #    }
        #
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            for j in range(0, len(quotes)):
                quoteId = quotes[j]
                # usd gets matched before usdt in usdtusd USDT/USD
                # https://github.com/ccxt/ccxt/issues/9868
                slicedId = id[1:]
                index = slicedId.find(quoteId)
                slice = slicedId[index:]
                if (index > 0) and (slice == quoteId):
                    # usd gets matched before usdt in usdtusd USDT/USD
                    # https://github.com/ccxt/ccxt/issues/9868
                    baseId = id[0] + slicedId.replace(quoteId, '')
                    base = self.safe_currency_code(baseId)
                    quote = self.safe_currency_code(quoteId)
                    markets.append({
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
                        'info': None,
                    })
        return markets

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 300
        orderbook = await self.publicGetDepth(self.extend(request, params))
        timestamp = self.safe_timestamp(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, symbol, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'at')
        ticker = ticker['ticker']
        symbol = self.safe_symbol(None, market)
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
            'open': self.safe_string(ticker, 'open'),
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

    async def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        response = await self.publicGetTickers(params)
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = None
            symbol = id
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                base = id[0:3]
                quote = id[3:6]
                base = base.upper()
                quote = quote.upper()
                base = self.safe_currency_code(base)
                quote = self.safe_currency_code(quote)
                symbol = base + '/' + quote
            result[symbol] = self.parse_ticker(response[id], market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTickersMarket(self.extend(request, params))
        return self.parse_ticker(response, market)

    async def fetch_l3_order_book(self, symbol, limit=None, params={}):
        return await self.fetch_order_book(symbol, limit, params)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        #
        #      [
        #          {
        #              "id":11353466,
        #              "price":"3000.16",
        #              "volume":"0.000397",
        #              "funds":"1.19106352",
        #              "market":"ethusdt",
        #              "created_at":"2022-04-12T18:32:36Z",
        #              "side":null,
        #              "trend":"sell"
        #          },
        #      ]
        #
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #      {
        #          "id":11353466,
        #          "price":"3000.16",
        #          "volume":"0.000397",
        #          "funds":"1.19106352",
        #          "market":"ethusdt",
        #          "created_at":"2022-04-12T18:32:36Z",
        #          "side":null,
        #          "trend":"sell"
        #      }
        #
        # fetchMyTrades(private)
        #
        #      {
        #          "id":11353719,
        #          "price":"0.13566",
        #          "volume":"99.0",
        #          "funds":"13.43034",
        #          "market":"dogeusdt",
        #          "created_at":"2022-04-12T18:58:44Z",
        #          "side":"ask",
        #          "order_id":1665670371,
        #          "trend":"buy"
        #      }
        #
        timestamp = self.parse8601(self.safe_string(trade, 'created_at'))
        symbol = None
        if market:
            symbol = market['symbol']
        side = self.safe_string_2(trade, 'side', 'trend')
        if side is not None:
            sideMap = {
                'ask': 'sell',
                'bid': 'buy',
            }
            side = self.safe_string(sideMap, side, side)
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'volume')
        costString = self.safe_number(trade, 'funds')
        orderId = self.safe_string(trade, 'order_id')
        id = self.safe_string(trade, 'id')
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'order': orderId,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': costString,
            'fee': None,
        }, market)

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        await self.load_markets()
        trades = await self.fetch_trades(symbol, since, limit, params)
        ohlcvc = self.build_ohlcvc(trades, timeframe, since, limit)
        result = []
        for i in range(0, len(ohlcvc)):
            ohlcv = ohlcvc[i]
            result.append([
                ohlcv[0],
                ohlcv[1],
                ohlcv[2],
                ohlcv[3],
                ohlcv[4],
                ohlcv[5],
            ])
        return result

    def parse_balance(self, response):
        balances = self.safe_value(response, 'accounts', [])
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'balance')
            account['used'] = self.safe_string(balance, 'locked')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privateGetMembersMe(params)
        return self.parse_balance(response)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the kuna api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
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
        marketId = self.safe_value(response, 'market')
        market = self.safe_value(self.markets_by_id, marketId)
        return self.parse_order(response, market)

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': id,
        }
        response = await self.privatePostOrderDelete(self.extend(request, params))
        order = self.parse_order(response)
        status = order['status']
        if status == 'closed' or status == 'canceled':
            raise OrderNotFound(self.id + ' ' + self.json(order))
        return order

    def parse_order_status(self, status):
        statuses = {
            'done': 'closed',
            'wait': 'open',
            'cancel': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        marketId = self.safe_string(order, 'market')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.parse8601(self.safe_string(order, 'created_at'))
        status = self.parse_order_status(self.safe_string(order, 'state'))
        type = self.safe_string(order, 'type')
        side = self.safe_string(order, 'side')
        id = self.safe_string(order, 'id')
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
            'price': self.safe_string(order, 'price'),
            'stopPrice': None,
            'amount': self.safe_string(order, 'volume'),
            'filled': self.safe_string(order, 'executed_volume'),
            'remaining': self.safe_string(order, 'remaining_volume'),
            'trades': None,
            'fee': None,
            'info': order,
            'cost': None,
            'average': None,
        }, market)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'id': int(id),
        }
        response = await self.privateGetOrder(self.extend(request, params))
        return self.parse_order(response)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.privateGetOrders(self.extend(request, params))
        # todo emulation of fetchClosedOrders, fetchOrders, fetchOrder
        # with order cache + fetchOpenOrders
        # as in BTC-e, Liqui, Yobit, DSX, Tidex, WEX
        return self.parse_orders(response, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        #
        #      [
        #          {
        #              "id":11353719,
        #              "price":"0.13566",
        #              "volume":"99.0",
        #              "funds":"13.43034",
        #              "market":"dogeusdt",
        #              "created_at":"2022-04-12T18:58:44Z",
        #              "side":"ask",
        #              "order_id":1665670371,
        #              "trend":"buy"
        #          },
        #      ]
        #
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.privateGetTradesMy(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def nonce(self):
        return self.milliseconds()

    def encode_params(self, params):
        if 'orders' in params:
            orders = params['orders']
            query = self.urlencode(self.keysort(self.omit(params, 'orders')))
            for i in range(0, len(orders)):
                order = orders[i]
                keys = list(order.keys())
                for k in range(0, len(keys)):
                    key = keys[k]
                    value = order[key]
                    query += '&orders%5B%5D%5B' + key + '%5D=' + str(value)
            return query
        return self.urlencode(self.keysort(params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = None
        if isinstance(api, list):
            version, access = api
            url = self.urls['api'][version] + '/' + version + '/' + self.implode_params(path, params)
            if access == 'public':
                if method == 'GET':
                    if params:
                        url += '?' + self.urlencode(params)
                elif (method == 'POST') or (method == 'PUT'):
                    headers = {'Content-Type': 'application/json'}
                    body = self.json(params)
            elif access == 'private':
                raise NotSupported(self.id + ' private v3 API is not supported yet')
        else:
            request = '/api/' + self.version + '/' + self.implode_params(path, params)
            if 'extension' in self.urls:
                request += self.urls['extension']
            query = self.omit(params, self.extract_params(path))
            url = self.urls['api'][api] + request
            if api == 'public':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                self.check_required_credentials()
                nonce = str(self.nonce())
                query = self.encode_params(self.extend({
                    'access_key': self.apiKey,
                    'tonce': nonce,
                }, params))
                auth = method + '|' + request + '|' + query
                signed = self.hmac(self.encode(auth), self.encode(self.secret))
                suffix = query + '&signature=' + signed
                if method == 'GET':
                    url += '?' + suffix
                else:
                    body = suffix
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if code == 400:
            error = self.safe_value(response, 'error')
            errorCode = self.safe_string(error, 'code')
            feedback = self.id + ' ' + self.json(response)
            self.throw_exactly_matched_exception(self.exceptions, errorCode, feedback)
            # fallback to default error handler
