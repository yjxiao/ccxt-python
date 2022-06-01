# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import NotSupported
from ccxt.base.errors import InvalidNonce
from ccxt.base.precise import Precise


class bit2c(Exchange):

    def describe(self):
        return self.deep_extend(super(bit2c, self).describe(), {
            'id': 'bit2c',
            'name': 'Bit2C',
            'countries': ['IL'],  # Israel
            'rateLimit': 3000,
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
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchDepositAddress': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': True,
                'fetchTransfer': False,
                'fetchTransfers': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'transfer': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766119-3593220e-5ece-11e7-8b3a-5a041f6bcc3f.jpg',
                'api': 'https://bit2c.co.il',
                'www': 'https://www.bit2c.co.il',
                'referral': 'https://bit2c.co.il/Aff/63bfed10-e359-420c-ab5a-ad368dab0baf',
                'doc': [
                    'https://www.bit2c.co.il/home/api',
                    'https://github.com/OferE/bit2c',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'Exchanges/{pair}/Ticker',
                        'Exchanges/{pair}/orderbook',
                        'Exchanges/{pair}/trades',
                        'Exchanges/{pair}/lasttrades',
                    ],
                },
                'private': {
                    'post': [
                        'Merchant/CreateCheckout',
                        'Funds/AddCoinFundsRequest',
                        'Order/AddFund',
                        'Order/AddOrder',
                        'Order/AddOrderMarketPriceBuy',
                        'Order/AddOrderMarketPriceSell',
                        'Order/CancelOrder',
                        'Order/AddCoinFundsRequest',
                        'Order/AddStopOrder',
                        'Payment/GetMyId',
                        'Payment/Send',
                        'Payment/Pay',
                    ],
                    'get': [
                        'Account/Balance',
                        'Account/Balance/v2',
                        'Order/MyOrders',
                        'Order/GetById',
                        'Order/AccountHistory',
                        'Order/OrderHistory',
                    ],
                },
            },
            'markets': {
                'BTC/NIS': {'id': 'BtcNis', 'symbol': 'BTC/NIS', 'base': 'BTC', 'quote': 'NIS', 'baseId': 'Btc', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'ETH/NIS': {'id': 'EthNis', 'symbol': 'ETH/NIS', 'base': 'ETH', 'quote': 'NIS', 'baseId': 'Eth', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'BCH/NIS': {'id': 'BchabcNis', 'symbol': 'BCH/NIS', 'base': 'BCH', 'quote': 'NIS', 'baseId': 'Bchabc', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'LTC/NIS': {'id': 'LtcNis', 'symbol': 'LTC/NIS', 'base': 'LTC', 'quote': 'NIS', 'baseId': 'Ltc', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'ETC/NIS': {'id': 'EtcNis', 'symbol': 'ETC/NIS', 'base': 'ETC', 'quote': 'NIS', 'baseId': 'Etc', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'BTG/NIS': {'id': 'BtgNis', 'symbol': 'BTG/NIS', 'base': 'BTG', 'quote': 'NIS', 'baseId': 'Btg', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'BSV/NIS': {'id': 'BchsvNis', 'symbol': 'BSV/NIS', 'base': 'BSV', 'quote': 'NIS', 'baseId': 'Bchsv', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
                'GRIN/NIS': {'id': 'GrinNis', 'symbol': 'GRIN/NIS', 'base': 'GRIN', 'quote': 'NIS', 'baseId': 'Grin', 'quoteId': 'Nis', 'type': 'spot', 'spot': True},
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('0.005'),
                    'taker': self.parse_number('0.005'),
                },
            },
            'options': {
                'fetchTradesMethod': 'public_get_exchanges_pair_trades',
            },
            'exceptions': {
                'exact': {
                    'Please provide valid APIkey': AuthenticationError,  # {"error" : "Please provide valid APIkey"}
                },
                'broad': {
                    # {"error": "Please provide valid nonce in Request Nonce(1598218490) is not bigger than last nonce(1598218490)."}
                    # {"error": "Please provide valid nonce in Request UInt64.TryParse failed for nonce :"}
                    'Please provide valid nonce': InvalidNonce,
                    'please approve new terms of use on site': PermissionDenied,  # {"error" : "please approve new terms of use on site."}
                },
            },
        })

    def parse_balance(self, response):
        result = {
            'info': response,
            'timestamp': None,
            'datetime': None,
        }
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            account = self.account()
            currency = self.currency(code)
            uppercase = currency['id'].upper()
            if uppercase in response:
                account['free'] = self.safe_string(response, 'AVAILABLE_' + uppercase)
                account['total'] = self.safe_string(response, uppercase)
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bit2c api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privateGetAccountBalanceV2(params)
        #
        #     {
        #         "AVAILABLE_NIS": 0.0,
        #         "NIS": 0.0,
        #         "LOCKED_NIS": 0.0,
        #         "AVAILABLE_BTC": 0.0,
        #         "BTC": 0.0,
        #         "LOCKED_BTC": 0.0,
        #         "AVAILABLE_ETH": 0.0,
        #         "ETH": 0.0,
        #         "LOCKED_ETH": 0.0,
        #         "AVAILABLE_BCHSV": 0.0,
        #         "BCHSV": 0.0,
        #         "LOCKED_BCHSV": 0.0,
        #         "AVAILABLE_BCHABC": 0.0,
        #         "BCHABC": 0.0,
        #         "LOCKED_BCHABC": 0.0,
        #         "AVAILABLE_LTC": 0.0,
        #         "LTC": 0.0,
        #         "LOCKED_LTC": 0.0,
        #         "AVAILABLE_ETC": 0.0,
        #         "ETC": 0.0,
        #         "LOCKED_ETC": 0.0,
        #         "AVAILABLE_BTG": 0.0,
        #         "BTG": 0.0,
        #         "LOCKED_BTG": 0.0,
        #         "AVAILABLE_GRIN": 0.0,
        #         "GRIN": 0.0,
        #         "LOCKED_GRIN": 0.0,
        #         "Fees": {
        #             "BtcNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "EthNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "BchabcNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "LtcNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "EtcNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "BtgNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "LtcBtc": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "BchsvNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "GrinNis": {"FeeMaker": 1.0, "FeeTaker": 1.0}
        #         }
        #     }
        #
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the bit2c api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        orderbook = await self.publicGetExchangesPairOrderbook(self.extend(request, params))
        return self.parse_order_book(orderbook, symbol)

    def parse_ticker(self, ticker, market=None):
        symbol = self.safe_symbol(None, market)
        timestamp = self.milliseconds()
        averagePrice = self.safe_string(ticker, 'av')
        baseVolume = self.safe_string(ticker, 'a')
        last = self.safe_string(ticker, 'll')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_string(ticker, 'h'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'l'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': averagePrice,
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bit2c api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.publicGetExchangesPairTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the bit2c api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        method = self.options['fetchTradesMethod']  # public_get_exchanges_pair_trades or public_get_exchanges_pair_lasttrades
        request = {
            'pair': market['id'],
        }
        if since is not None:
            request['date'] = int(since)
        if limit is not None:
            request['limit'] = limit  # max 100000
        response = await getattr(self, method)(self.extend(request, params))
        #
        #     [
        #         {"date":1651785980,"price":127975.68,"amount":0.3750321,"isBid":true,"tid":1261018},
        #         {"date":1651785980,"price":127987.70,"amount":0.0389527820303982335802581029,"isBid":true,"tid":1261020},
        #         {"date":1651786701,"price":128084.03,"amount":0.0015614749161156156626239821,"isBid":true,"tid":1261022},
        #     ]
        #
        if isinstance(response, str):
            raise ExchangeError(response)
        return self.parse_trades(response, market, since, limit)

    async def fetch_trading_fees(self, params={}):
        await self.load_markets()
        response = await self.privateGetAccountBalance(params)
        #
        #     {
        #         "AVAILABLE_NIS": 0.0,
        #         "NIS": 0.0,
        #         "LOCKED_NIS": 0.0,
        #         "AVAILABLE_BTC": 0.0,
        #         "BTC": 0.0,
        #         "LOCKED_BTC": 0.0,
        #         ...
        #         "Fees": {
        #             "BtcNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             "EthNis": {"FeeMaker": 1.0, "FeeTaker": 1.0},
        #             ...
        #         }
        #     }
        #
        fees = self.safe_value(response, 'Fees', {})
        keys = list(fees.keys())
        result = {}
        for i in range(0, len(keys)):
            marketId = keys[i]
            symbol = self.safe_symbol(marketId)
            fee = self.safe_value(fees, marketId)
            makerString = self.safe_string(fee, 'FeeMaker')
            takerString = self.safe_string(fee, 'FeeTaker')
            maker = self.parse_number(Precise.string_div(makerString, '100'))
            taker = self.parse_number(Precise.string_div(takerString, '100'))
            result[symbol] = {
                'info': fee,
                'symbol': symbol,
                'taker': taker,
                'maker': maker,
                'percentage': True,
                'tierBased': False,
            }
        return result

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        method = 'privatePostOrderAddOrder'
        request = {
            'Amount': amount,
            'Pair': self.market_id(symbol),
        }
        if type == 'market':
            method += 'MarketPrice' + self.capitalize(side)
        else:
            request['Price'] = price
            request['Total'] = amount * price
            request['IsBid'] = (side == 'buy')
        response = await getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': response['NewOrder']['id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'id': id,
        }
        return await self.privatePostOrderCancelOrder(self.extend(request, params))

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = await self.privateGetOrderMyOrders(self.extend(request, params))
        orders = self.safe_value(response, market['id'], {})
        asks = self.safe_value(orders, 'ask', [])
        bids = self.safe_value(orders, 'bid', [])
        return self.parse_orders(self.array_concat(asks, bids), market, since, limit)

    def parse_order(self, order, market=None):
        timestamp = self.safe_integer(order, 'created')
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'amount')
        market = self.safe_market(None, market)
        side = self.safe_value(order, 'type')
        if side == 0:
            side = 'buy'
        elif side == 1:
            side = 'sell'
        id = self.safe_string(order, 'id')
        status = self.safe_string(order, 'status')
        return self.safe_order({
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': market['symbol'],
            'type': None,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': None,
            'trades': None,
            'fee': None,
            'info': order,
            'average': None,
        }, market)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {}
        if limit is not None:
            request['take'] = limit
        request['take'] = limit
        if since is not None:
            request['toTime'] = self.yyyymmdd(self.milliseconds(), '.')
            request['fromTime'] = self.yyyymmdd(since, '.')
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = await self.privateGetOrderOrderHistory(self.extend(request, params))
        #
        #     [
        #         {
        #             "ticks":1574767951,
        #             "created":"26/11/19 13:32",
        #             "action":1,
        #             "price":"1000",
        #             "pair":"EthNis",
        #             "reference":"EthNis|10867390|10867377",
        #             "fee":"0.5",
        #             "feeAmount":"0.08",
        #             "feeCoin":"₪",
        #             "firstAmount":"-0.015",
        #             "firstAmountBalance":"9",
        #             "secondAmount":"14.93",
        #             "secondAmountBalance":"130,233.28",
        #             "firstCoin":"ETH",
        #             "secondCoin":"₪"
        #         },
        #         {
        #             "ticks":1574767951,
        #             "created":"26/11/19 13:32",
        #             "action":0,
        #             "price":"1000",
        #             "pair":"EthNis",
        #             "reference":"EthNis|10867390|10867377",
        #             "fee":"0.5",
        #             "feeAmount":"0.08",
        #             "feeCoin":"₪",
        #             "firstAmount":"0.015",
        #             "firstAmountBalance":"9.015",
        #             "secondAmount":"-15.08",
        #             "secondAmountBalance":"130,218.35",
        #             "firstCoin":"ETH",
        #             "secondCoin":"₪"
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # public fetchTrades
        #
        #     {
        #         "date":1651785980,
        #         "price":127975.68,
        #         "amount":0.3750321,
        #         "isBid":true,
        #         "tid":1261018
        #     }
        #
        # private fetchMyTrades
        #
        #     {
        #         "ticks":1574767951,
        #         "created":"26/11/19 13:32",
        #         "action":1,
        #         "price":"1000",
        #         "pair":"EthNis",
        #         "reference":"EthNis|10867390|10867377",
        #         "fee":"0.5",
        #         "feeAmount":"0.08",
        #         "feeCoin":"₪",
        #         "firstAmount":"-0.015",
        #         "firstAmountBalance":"9",
        #         "secondAmount":"14.93",
        #         "secondAmountBalance":"130,233.28",
        #         "firstCoin":"ETH",
        #         "secondCoin":"₪"
        #     }
        #
        timestamp = None
        id = None
        price = None
        amount = None
        orderId = None
        fee = None
        side = None
        reference = self.safe_string(trade, 'reference')
        if reference is not None:
            timestamp = self.safe_timestamp(trade, 'ticks')
            price = self.safe_string(trade, 'price')
            amount = self.safe_string(trade, 'firstAmount')
            reference_parts = reference.split('|')  # reference contains 'pair|orderId|tradeId'
            marketId = self.safe_string(trade, 'pair')
            market = self.safe_market(marketId, market)
            market = self.safe_market(reference_parts[0], market)
            orderId = reference_parts[1]
            id = reference_parts[2]
            side = self.safe_integer(trade, 'action')
            if side == 0:
                side = 'buy'
            elif side == 1:
                side = 'sell'
            feeCost = self.safe_string(trade, 'feeAmount')
            if feeCost is not None:
                fee = {
                    'cost': feeCost,
                    'currency': 'NIS',
                }
        else:
            timestamp = self.safe_timestamp(trade, 'date')
            id = self.safe_string(trade, 'tid')
            price = self.safe_string(trade, 'price')
            amount = self.safe_string(trade, 'amount')
            side = self.safe_value(trade, 'isBid')
            if side is not None:
                if side:
                    side = 'buy'
                else:
                    side = 'sell'
        market = self.safe_market(None, market)
        return self.safe_trade({
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': fee,
        }, market)

    def is_fiat(self, code):
        return code == 'NIS'

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        if self.is_fiat(code):
            raise NotSupported(self.id + ' fetchDepositAddress() does not support fiat currencies')
        request = {
            'Coin': currency['id'],
        }
        response = await self.privatePostFundsAddCoinFundsRequest(self.extend(request, params))
        #
        #     {
        #         'address': '0xf14b94518d74aff2b1a6d3429471bcfcd3881d42',
        #         'hasTx': False
        #     }
        #
        return self.parse_deposit_address(response, currency)

    def parse_deposit_address(self, depositAddress, currency=None):
        #
        #     {
        #         'address': '0xf14b94518d74aff2b1a6d3429471bcfcd3881d42',
        #         'hasTx': False
        #     }
        #
        address = self.safe_string(depositAddress, 'address')
        self.check_address(address)
        code = self.safe_currency_code(None, currency)
        return {
            'currency': code,
            'network': None,
            'address': address,
            'tag': None,
            'info': depositAddress,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        if api == 'public':
            url += '.json'
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            query = self.extend({
                'nonce': nonce,
            }, params)
            auth = self.urlencode(query)
            if method == 'GET':
                if query:
                    url += '?' + auth
            else:
                body = auth
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512, 'base64')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'key': self.apiKey,
                'sign': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        #
        #     {"error" : "please approve new terms of use on site."}
        #     {"error": "Please provide valid nonce in Request Nonce(1598218490) is not bigger than last nonce(1598218490)."}
        #
        error = self.safe_string(response, 'error')
        if error is not None:
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions['exact'], error, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], error, feedback)
            raise ExchangeError(feedback)  # unknown message
