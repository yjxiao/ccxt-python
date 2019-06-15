# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired


class bit2c (Exchange):

    def describe(self):
        return self.deep_extend(super(bit2c, self).describe(), {
            'id': 'bit2c',
            'name': 'Bit2C',
            'countries': ['IL'],  # Israel
            'rateLimit': 3000,
            'has': {
                'CORS': False,
                'fetchOpenOrders': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766119-3593220e-5ece-11e7-8b3a-5a041f6bcc3f.jpg',
                'api': 'https://bit2c.co.il',
                'www': 'https://www.bit2c.co.il',
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
                'BTC/NIS': {'id': 'BtcNis', 'symbol': 'BTC/NIS', 'base': 'BTC', 'quote': 'NIS', 'baseId': 'Btc', 'quoteId': 'Nis'},
                'ETH/NIS': {'id': 'EthNis', 'symbol': 'ETH/NIS', 'base': 'ETH', 'quote': 'NIS', 'baseId': 'Eth', 'quoteId': 'Nis'},
                'BCH/NIS': {'id': 'BchabcNis', 'symbol': 'BCH/NIS', 'base': 'BCH', 'quote': 'NIS', 'baseId': 'Bchabc', 'quoteId': 'Nis'},
                'LTC/NIS': {'id': 'LtcNis', 'symbol': 'LTC/NIS', 'base': 'LTC', 'quote': 'NIS', 'baseId': 'Ltc', 'quoteId': 'Nis'},
                'ETC/NIS': {'id': 'EtcNis', 'symbol': 'ETC/NIS', 'base': 'ETC', 'quote': 'NIS', 'baseId': 'Etc', 'quoteId': 'Nis'},
                'BTG/NIS': {'id': 'BtgNis', 'symbol': 'BTG/NIS', 'base': 'BTG', 'quote': 'NIS', 'baseId': 'Btg', 'quoteId': 'Nis'},
                'BSV/NIS': {'id': 'BchsvNis', 'symbol': 'BSV/NIS', 'base': 'BSV', 'quote': 'NIS', 'baseId': 'Bchsv', 'quoteId': 'Nis'},
                'GRIN/NIS': {'id': 'GrinNis', 'symbol': 'GRIN/NIS', 'base': 'GRIN', 'quote': 'NIS', 'baseId': 'Grin', 'quoteId': 'Nis'},
            },
            'fees': {
                'trading': {
                    'maker': 0.5 / 100,
                    'taker': 0.5 / 100,
                },
            },
            'options': {
                'fetchTradesMethod': 'public_get_exchanges_pair_lasttrades',
            },
            'exceptions': {
                # {"error" : "Please provide valid APIkey"}
                # {"error" : "Please provide valid nonce in Request UInt64.TryParse failed for nonce :"}
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balance = await self.privateGetAccountBalanceV2(params)
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
        result = {'info': balance}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            account = self.account()
            currency = self.currency(code)
            uppercase = currency['id'].upper()
            if uppercase in balance:
                account['free'] = self.safe_float(balance, 'AVAILABLE_' + uppercase)
                account['total'] = self.safe_float(balance, uppercase)
                account['used'] = account['total'] - account['free']
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        orderbook = await self.publicGetExchangesPairOrderbook(self.extend(request, params))
        return self.parse_order_book(orderbook)

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        ticker = await self.publicGetExchangesPairTicker(self.extend(request, params))
        timestamp = self.milliseconds()
        averagePrice = self.safe_float(ticker, 'av')
        baseVolume = self.safe_float(ticker, 'a')
        quoteVolume = None
        if baseVolume is not None and averagePrice is not None:
            quoteVolume = baseVolume * averagePrice
        last = self.safe_float(ticker, 'll')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'h'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'l'),
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
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        method = self.options['fetchTradesMethod']
        request = {
            'pair': market['id'],
        }
        response = await getattr(self, method)(self.extend(request, params))
        if isinstance(response, basestring):
            raise ExchangeError(response)
        return self.parse_trades(response, market, since, limit)

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
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        side = self.safe_value(order, 'type')
        if side == 0:
            side = 'buy'
        elif side == 1:
            side = 'sell'
        id = self.safe_string(order, 'id')
        status = self.safe_string(order, 'status')
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': cost,
            'trades': None,
            'fee': None,
            'info': order,
        }

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        method = 'privateGetOrderOrderhistory'
        request = {}
        if limit is not None:
            request['take'] = limit
        request['take'] = limit
        if since is not None:
            request['toTime'] = self.ymd(self.milliseconds(), '.')
            request['fromTime'] = self.ymd(since, '.')
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = None
        id = None
        price = None
        amount = None
        orderId = None
        feeCost = None
        side = None
        reference = self.safe_string(trade, 'reference')
        if reference is not None:
            timestamp = self.safe_integer(trade, 'ticks') * 1000
            price = self.safe_float(trade, 'price')
            amount = self.safe_float(trade, 'firstAmount')
            reference_parts = reference.split('|')  # reference contains: 'pair|orderId|tradeId'
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
            feeCost = self.safe_float(trade, 'feeAmount')
        else:
            timestamp = self.safe_integer(trade, 'date') * 1000
            id = self.safe_string(trade, 'tid')
            price = self.safe_float(trade, 'price')
            amount = self.safe_float(trade, 'amount')
            side = self.safe_value(trade, 'isBid')
            if side is not None:
                if side:
                    side = 'buy'
                else:
                    side = 'sell'
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': orderId,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': {
                'cost': feeCost,
                'currency': 'NIS',
                'rate': None,
            },
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        if api == 'public':
            # lasttrades is the only endpoint that doesn't require the .json extension/suffix
            if path.find('lasttrades') < 0:
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
                'sign': self.decode(signature),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
