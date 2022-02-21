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
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidNonce


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
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedPositions': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
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
                        'Order/AddCoinFundsRequest',
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

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccountBalanceV2(params)
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

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        orderbook = self.publicGetExchangesPairOrderbook(self.extend(request, params))
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
        }, market, False)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetExchangesPairTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = self.options['fetchTradesMethod']
        request = {
            'pair': market['id'],
        }
        if since is not None:
            request['date'] = int(since)
        if limit is not None:
            request['limit'] = limit  # max 100000
        response = getattr(self, method)(self.extend(request, params))
        if isinstance(response, basestring):
            raise ExchangeError(response)
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
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
        response = getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': response['NewOrder']['id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        request = {
            'id': id,
        }
        return self.privatePostOrderCancelOrder(self.extend(request, params))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.privateGetOrderMyOrders(self.extend(request, params))
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

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
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
        response = self.privateGetOrderOrderHistory(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
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
            if market is None:
                marketId = self.safe_string(trade, 'pair')
                if marketId in self.markets_by_id[marketId]:
                    market = self.markets_by_id[marketId]
                elif reference_parts[0] in self.markets_by_id:
                    market = self.markets_by_id[reference_parts[0]]
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
