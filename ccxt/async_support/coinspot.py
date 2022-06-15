# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.decimal_to_precision import TICK_SIZE


class coinspot(Exchange):

    def describe(self):
        return self.deep_extend(super(coinspot, self).describe(), {
            'id': 'coinspot',
            'name': 'CoinSpot',
            'countries': ['AU'],  # Australia
            'rateLimit': 1000,
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createMarketOrder': None,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
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
                'fetchMarkOHLCV': False,
                'fetchOpenInterestHistory': False,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28208429-3cacdf9a-6896-11e7-854e-4c79a772a30f.jpg',
                'api': {
                    'public': 'https://www.coinspot.com.au/pubapi',
                    'private': 'https://www.coinspot.com.au/api',
                },
                'www': 'https://www.coinspot.com.au',
                'doc': 'https://www.coinspot.com.au/api',
                'referral': 'https://www.coinspot.com.au/register?code=PJURCU',
            },
            'api': {
                'public': {
                    'get': [
                        'latest',
                    ],
                },
                'private': {
                    'post': [
                        'orders',
                        'orders/history',
                        'my/coin/deposit',
                        'my/coin/send',
                        'quote/buy',
                        'quote/sell',
                        'my/balances',
                        'my/orders',
                        'my/buy',
                        'my/sell',
                        'my/buy/cancel',
                        'my/sell/cancel',
                        'ro/my/balances',
                        'ro/my/balances/{cointype}',
                        'ro/my/deposits',
                        'ro/my/withdrawals',
                        'ro/my/transactions',
                        'ro/my/transactions/{cointype}',
                        'ro/my/transactions/open',
                        'ro/my/transactions/{cointype}/open',
                        'ro/my/sendreceive',
                        'ro/my/affiliatepayments',
                        'ro/my/referralpayments',
                    ],
                },
            },
            'markets': {
                'ADA/AUD': {'id': 'ada', 'symbol': 'ADA/AUD', 'base': 'ADA', 'quote': 'AUD', 'baseId': 'ada', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'BTC/AUD': {'id': 'btc', 'symbol': 'BTC/AUD', 'base': 'BTC', 'quote': 'AUD', 'baseId': 'btc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'BTC/USDT': {'id': 'btc', 'symbol': 'BTC/USDT', 'base': 'BTC', 'quote': 'USDT', 'baseId': 'btc', 'quoteId': 'usdt', 'type': 'spot', 'spot': True},
                'ETH/AUD': {'id': 'eth', 'symbol': 'ETH/AUD', 'base': 'ETH', 'quote': 'AUD', 'baseId': 'eth', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'XRP/AUD': {'id': 'xrp', 'symbol': 'XRP/AUD', 'base': 'XRP', 'quote': 'AUD', 'baseId': 'xrp', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'LTC/AUD': {'id': 'ltc', 'symbol': 'LTC/AUD', 'base': 'LTC', 'quote': 'AUD', 'baseId': 'ltc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'DOGE/AUD': {'id': 'doge', 'symbol': 'DOGE/AUD', 'base': 'DOGE', 'quote': 'AUD', 'baseId': 'doge', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'RFOX/AUD': {'id': 'rfox', 'symbol': 'RFOX/AUD', 'base': 'RFOX', 'quote': 'AUD', 'baseId': 'rfox', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'POWR/AUD': {'id': 'powr', 'symbol': 'POWR/AUD', 'base': 'POWR', 'quote': 'AUD', 'baseId': 'powr', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'NEO/AUD': {'id': 'neo', 'symbol': 'NEO/AUD', 'base': 'NEO', 'quote': 'AUD', 'baseId': 'neo', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'TRX/AUD': {'id': 'trx', 'symbol': 'TRX/AUD', 'base': 'TRX', 'quote': 'AUD', 'baseId': 'trx', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'EOS/AUD': {'id': 'eos', 'symbol': 'EOS/AUD', 'base': 'EOS', 'quote': 'AUD', 'baseId': 'eos', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'XLM/AUD': {'id': 'xlm', 'symbol': 'XLM/AUD', 'base': 'XLM', 'quote': 'AUD', 'baseId': 'xlm', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'RHOC/AUD': {'id': 'rhoc', 'symbol': 'RHOC/AUD', 'base': 'RHOC', 'quote': 'AUD', 'baseId': 'rhoc', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
                'GAS/AUD': {'id': 'gas', 'symbol': 'GAS/AUD', 'base': 'GAS', 'quote': 'AUD', 'baseId': 'gas', 'quoteId': 'aud', 'type': 'spot', 'spot': True},
            },
            'commonCurrencies': {
                'DRK': 'DASH',
            },
            'options': {
                'fetchBalance': 'private_post_my_balances',
            },
            'precisionMode': TICK_SIZE,
        })

    def parse_balance(self, response):
        result = {'info': response}
        balances = self.safe_value_2(response, 'balance', 'balances')
        if isinstance(balances, list):
            for i in range(0, len(balances)):
                currencies = balances[i]
                currencyIds = list(currencies.keys())
                for j in range(0, len(currencyIds)):
                    currencyId = currencyIds[j]
                    balance = currencies[currencyId]
                    code = self.safe_currency_code(currencyId)
                    account = self.account()
                    account['total'] = self.safe_string(balance, 'balance')
                    result[code] = account
        else:
            currencyIds = list(balances.keys())
            for i in range(0, len(currencyIds)):
                currencyId = currencyIds[i]
                code = self.safe_currency_code(currencyId)
                account = self.account()
                account['total'] = self.safe_string(balances, currencyId)
                result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        method = self.safe_string(self.options, 'fetchBalance', 'private_post_my_balances')
        response = await getattr(self, method)(params)
        #
        # read-write api keys
        #
        #     ...
        #
        # read-only api keys
        #
        #     {
        #         "status":"ok",
        #         "balances":[
        #             {
        #                 "LTC":{"balance":0.1,"audbalance":16.59,"rate":165.95}
        #             }
        #         ]
        #     }
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'cointype': market['id'],
        }
        orderbook = await self.privatePostOrders(self.extend(request, params))
        return self.parse_order_book(orderbook, symbol, None, 'buyorders', 'sellorders', 'rate', 'amount')

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         "btc":{
        #             "bid":"51970",
        #             "ask":"53000",
        #             "last":"52806.47"
        #         }
        #     }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.milliseconds()
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_string(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetLatest(params)
        id = market['id']
        id = id.lower()
        prices = self.safe_value(response, 'prices')
        #
        #     {
        #         "status":"ok",
        #         "prices":{
        #             "btc":{
        #                 "bid":"52732.47000022",
        #                 "ask":"53268.0699976",
        #                 "last":"53284.03"
        #             }
        #         }
        #     }
        #
        ticker = self.safe_value(prices, id)
        return self.parse_ticker(ticker, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'cointype': market['id'],
        }
        response = await self.privatePostOrdersHistory(self.extend(request, params))
        #
        #     {
        #         "status":"ok",
        #         "orders":[
        #             {"amount":0.00102091,"rate":21549.09999991,"total":21.99969168,"coin":"BTC","solddate":1604890646143,"market":"BTC/AUD"},
        #         ],
        #     }
        #
        trades = self.safe_value(response, 'orders', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # public fetchTrades
        #
        #     {
        #         "amount":0.00102091,
        #         "rate":21549.09999991,
        #         "total":21.99969168,
        #         "coin":"BTC",
        #         "solddate":1604890646143,
        #         "market":"BTC/AUD"
        #     }
        #
        priceString = self.safe_string(trade, 'rate')
        amountString = self.safe_string(trade, 'amount')
        costString = self.safe_number(trade, 'total')
        timestamp = self.safe_integer(trade, 'solddate')
        marketId = self.safe_string(trade, 'market')
        symbol = self.safe_symbol(marketId, market, '/')
        return self.safe_trade({
            'info': trade,
            'id': None,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': priceString,
            'amount': amountString,
            'cost': costString,
            'fee': None,
        }, market)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        method = 'privatePostMy' + self.capitalize(side)
        if type == 'market':
            raise ExchangeError(self.id + ' createOrder() allows limit orders only')
        request = {
            'cointype': self.market_id(symbol),
            'amount': amount,
            'rate': price,
        }
        return await getattr(self, method)(self.extend(request, params))

    async def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: not used by coinspot cancelOrder()
        :param dict params: extra parameters specific to the coinspot api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        side = self.safe_string(params, 'side')
        if side != 'buy' and side != 'sell':
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a side parameter, "buy" or "sell"')
        params = self.omit(params, 'side')
        method = 'privatePostMy' + self.capitalize(side) + 'Cancel'
        request = {
            'id': id,
        }
        return await getattr(self, method)(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.json(self.extend({'nonce': nonce}, params))
            headers = {
                'Content-Type': 'application/json',
                'key': self.apiKey,
                'sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
