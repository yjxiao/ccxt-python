# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class blockchaincom(Exchange):

    def describe(self):
        return self.deep_extend(super(blockchaincom, self).describe(), {
            'id': 'blockchaincom',
            'secret': None,
            'name': 'Blockchain.com',
            'countries': ['LX'],
            'rateLimit': 10000,
            'version': 'v3',
            'has': {
                'CORS': False,
                'fetchTrades': False,
                'fetchOHLCV': False,
                'fetchLedger': False,
                'fetchMarkets': True,
                'fetchTickers': True,
                'fetchTicker': True,
                'fetchOrderBook': True,
                'fetchL2OrderBook': True,
                'fetchL3OrderBook': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchPartiallyFilledOrders': True,
                'fetchCanceledOrders': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'cancelOrders': True,
                'fetchWithdrawals': True,
                'fetchWithdrawal': True,
                'fetchDeposits': True,
                'fetchDeposit': True,
                'withdraw': True,
                'fetchTradingFees': True,
                'fetchWithdrawalWhitelist': True,  # fetches exchange specific benficiary-ids needed for withdrawals
                'fetchMyTrades': True,
            },
            'timeframes': None,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/147515585-1296e91b-7398-45e5-9d32-f6121538533f.jpeg',
                'test': {
                    'public': 'https://testnet-api.delta.exchange',
                    'private': 'https://testnet-api.delta.exchange',
                },
                'api': {
                    'public': 'https://api.blockchain.com/v3/exchange',
                    'private': 'https://api.blockchain.com/v3/exchange',
                },
                'www': 'https://blockchain.com',
                'doc': [
                    'https://api.blockchain.com/v3',
                ],
                'fees': 'https://exchange.blockchain.com/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'tickers',  # fetchTickers
                        'tickers/{symbol}',  # fetchTicker
                        'symbols',  # fetchMarkets
                        'symbols/{symbol}',  # fetchMarket
                        'l2/{symbol}',  # fetchL2OrderBook
                        'l3/{symbol}',  # fetchL3OrderBook
                    ],
                },
                'private': {
                    'get': [
                        'fees',  # fetchFees
                        'orders',  # fetchOpenOrders, fetchClosedOrders
                        'orders/{orderId}',  # fetchOrder(id)
                        'trades',
                        'fills',  # fetchMyTrades
                        'deposits',  # fetchDeposits
                        'deposits/{depositId}',  # fetchDeposit
                        'accounts',  # fetchBalance
                        'accounts/{account}/{currency}',
                        'whitelist',  # fetchWithdrawalWhitelist
                        'whitelist/{currency}',  # fetchWithdrawalWhitelistByCurrency
                        'withdrawals',  # fetchWithdrawalWhitelist
                        'withdrawals/{withdrawalId}',  # fetchWithdrawalById
                    ],
                    'post': [
                        'orders',  # createOrder
                        'deposits/{currency}',  # fetchDepositAddress by currency(only crypto supported)
                        'withdrawals',  # withdraw
                    ],
                    'delete': [
                        'orders',  # cancelOrders
                        'orders/{orderId}',  # cancelOrder
                    ],
                },
            },
            'fees': {
                'trading': {
                    'feeSide': 'get',
                    'tierBased': True,
                    'percentage': True,
                    'tiers': {
                        'taker': [
                            [self.parse_number('0'), self.parse_number('0.004')],
                            [self.parse_number('10000'), self.parse_number('0.0022')],
                            [self.parse_number('50000'), self.parse_number('0.002')],
                            [self.parse_number('100000'), self.parse_number('0.0018')],
                            [self.parse_number('500000'), self.parse_number('0.0018')],
                            [self.parse_number('1000000'), self.parse_number('0.0018')],
                            [self.parse_number('2500000'), self.parse_number('0.0018')],
                            [self.parse_number('5000000'), self.parse_number('0.0016')],
                            [self.parse_number('25000000'), self.parse_number('0.0014')],
                            [self.parse_number('100000000'), self.parse_number('0.0011')],
                            [self.parse_number('500000000'), self.parse_number('0.0008')],
                            [self.parse_number('1000000000'), self.parse_number('0.0006')],
                        ],
                        'maker': [
                            [self.parse_number('0'), self.parse_number('0.002')],
                            [self.parse_number('10000'), self.parse_number('0.0012')],
                            [self.parse_number('50000'), self.parse_number('0.001')],
                            [self.parse_number('100000'), self.parse_number('0.0008')],
                            [self.parse_number('500000'), self.parse_number('0.0007000000000000001')],
                            [self.parse_number('1000000'), self.parse_number('0.0006')],
                            [self.parse_number('2500000'), self.parse_number('0.0005')],
                            [self.parse_number('5000000'), self.parse_number('0.0004')],
                            [self.parse_number('25000000'), self.parse_number('0.0003')],
                            [self.parse_number('100000000'), self.parse_number('0.0002')],
                            [self.parse_number('500000000'), self.parse_number('0.0001')],
                            [self.parse_number('1000000000'), self.parse_number('0')],
                        ],
                    },
                },
            },
            'requiredCredentials': {
                'apiKey': False,
                'secret': True,
            },
            'precisionMode': TICK_SIZE,
            'exceptions': {
                'exact': {
                    '401': AuthenticationError,
                    '404': OrderNotFound,
                },
                'broad': {},
            },
        })

    def fetch_markets(self, params={}):
        #
        # },
        # "USDC-GBP": {
        # "base_currency": "USDC",
        # "base_currency_scale": 6,
        # "counter_currency": "GBP",
        # "counter_currency_scale": 2,
        # "min_price_increment": 10000,
        # "min_price_increment_scale": 8,
        # "min_order_size": 500000000,
        # "min_order_size_scale": 8,
        # "max_order_size": 0,
        # "max_order_size_scale": 8,
        # "lot_size": 10000,
        # "lot_size_scale": 8,
        # "status": "open",
        # "id": 68,
        # "auction_price": 0,
        # "auction_size": 0,
        # "auction_time": "",
        # "imbalance": 0
        # }, ...
        #
        markets = self.publicGetSymbols(params)
        marketIds = list(markets.keys())
        result = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.safe_value(markets, marketId)
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'counter_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            numericId = self.safe_number(market, 'id')
            active = None
            marketState = self.safe_string(market, 'status')
            if marketState == 'open':
                active = 'true'
            else:
                active = 'false'
            # price precision
            minPriceIncrementString = self.safe_string(market, 'min_price_increment')
            minPriceIncrementScaleString = self.safe_string(market, 'min_price_increment_scale')
            minPriceScalePrecisionString = self.parse_precision(minPriceIncrementScaleString)
            pricePrecisionString = Precise.string_mul(minPriceIncrementString, minPriceScalePrecisionString)
            pricePrecision = self.parse_number(pricePrecisionString)
            # amount precision
            lotSizeString = self.safe_string(market, 'lot_size')
            lotSizeScaleString = self.safe_string(market, 'lot_size_scale')
            lotSizeScalePrecisionString = self.parse_precision(lotSizeScaleString)
            amountPrecisionString = Precise.string_mul(lotSizeString, lotSizeScalePrecisionString)
            amountPrecision = self.parse_number(amountPrecisionString)
            # precision
            precision = {
                'price': pricePrecision,
                'amount': amountPrecision,
            }
            # minimum order size
            minOrderSizeString = self.safe_string(market, 'min_order_size')
            minOrderSizeScaleString = self.safe_string(market, 'min_order_size_scale')
            minOrderSizeScalePrecisionString = self.parse_precision(minOrderSizeScaleString)
            minOrderSizePreciseString = Precise.string_mul(minOrderSizeString, minOrderSizeScalePrecisionString)
            minOrderSize = self.parse_number(minOrderSizePreciseString)
            # maximum order size
            maxOrderSize = None
            maxOrderSize = self.safe_string(market, 'max_order_size')
            if maxOrderSize != '0':
                maxOrderSizeScaleString = self.safe_string(market, 'max_order_size_scale')
                maxOrderSizeScalePrecisionString = self.parse_precision(maxOrderSizeScaleString)
                maxOrderSizeString = Precise.string_mul(maxOrderSize, maxOrderSizeScalePrecisionString)
                maxOrderSize = self.parse_number(maxOrderSizeString)
            else:
                maxOrderSize = None
            limits = {
                'amount': {
                    'min': minOrderSize,
                    'max': maxOrderSize,
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': None,
                    'max': None,
                },
            }
            symbol = base + '/' + quote
            result.append({
                'id': marketId,
                'numericId': numericId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'limits': limits,
                'active': active,
                'info': market,
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        return self.fetch_l3_order_book(symbol, limit, params)

    def fetch_l3_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['depth'] = limit
        response = self.publicGetL3Symbol(self.extend(request, params))
        return self.parse_order_book(response, symbol, None, 'bids', 'asks', 'px', 'qty')

    def fetch_l2_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['depth'] = limit
        response = self.publicGetL2Symbol(self.extend(request, params))
        return self.parse_order_book(response, symbol, None, 'bids', 'asks', 'px', 'qty')

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #     "symbol": "BTC-USD",
        #     "price_24h": 47791.86,
        #     "volume_24h": 362.88635738,
        #     "last_trade_price": 47587.75
        #     }
        #
        marketId = self.safe_string(ticker, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        last = self.safe_number(ticker, 'last_trade_price')
        baseVolume = self.safe_number(ticker, 'volume_24h')
        open = self.safe_number(ticker, 'price_24h')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': None,
            'low': None,
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': None,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }, market)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetTickersSymbol(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTickers(params)
        return self.parse_tickers(tickers, symbols)

    def parse_order_state(self, state):
        states = {
            'OPEN': 'open',
            'REJECTED': 'rejected',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
            'PART_FILLED': 'open',
            'EXPIRED': 'expired',
        }
        return self.safe_string(states, state, state)

    def parse_order(self, order, market=None):
        #
        #     {
        #         clOrdId: '00001',
        #         ordType: 'MARKET',
        #         ordStatus: 'FILLED',
        #         side: 'BUY',
        #         symbol: 'USDC-USDT',
        #         exOrdId: '281775861306290',
        #         price: null,
        #         text: 'Fill',
        #         lastShares: '30.0',
        #         lastPx: '0.9999',
        #         leavesQty: '0.0',
        #         cumQty: '30.0',
        #         avgPx: '0.9999',
        #         timestamp: '1633940339619'
        #     }
        #
        clientOrderId = self.safe_string(order, 'clOrdId')
        type = self.safe_string_lower(order, 'ordType')
        statusId = self.safe_string(order, 'ordStatus')
        state = self.parse_order_state(statusId)
        side = self.safe_string_lower(order, 'side')
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        exchangeOrderId = self.safe_string(order, 'exOrdId')
        price = self.safe_string(order, 'price') if (type != 'market') else None
        average = self.safe_number(order, 'avgPx')
        timestamp = self.safe_integer(order, 'timestamp')
        datetime = self.iso8601(timestamp)
        filled = self.safe_string(order, 'cumQty')
        remaining = self.safe_string(order, 'leavesQty')
        result = self.safeOrder2({
            'id': exchangeOrderId,
            'clientOrderId': clientOrderId,
            'datetime': datetime,
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': state,
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'side': side,
            'price': price,
            'average': average,
            'amount': None,
            'filled': filled,
            'remaining': remaining,
            'cost': None,
            'trades': [],
            'fees': {},
            'info': order,
        })
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        clientOrderId = self.safe_string_2(params, 'clientOrderId', 'clOrdId', self.uuid16())
        self.load_markets()
        market = self.market(symbol)
        request = {
            # 'stopPx' : limit price
            # 'timeInForce' : "GTC" for Good Till Cancel, "IOC" for Immediate or Cancel, "FOK" for Fill or Kill, "GTD" Good Till Date
            # 'expireDate' : expiry date in the format YYYYMMDD
            # 'minQty' : The minimum quantity required for an IOC fill
            'symbol': market['id'],
            'side': side.upper(),
            'orderQty': self.amount_to_precision(symbol, amount),
            'ordType': type.upper(),  # LIMIT, MARKET, STOP, STOPLIMIT
            'clOrdId': clientOrderId,
        }
        params = self.omit(params, ['clientOrderId', 'clOrdId'])
        if request['ordType'] == 'LIMIT':
            request['price'] = self.price_to_precision(symbol, price)
        if request['ordType'] == 'STOPLIMIT':
            request['price'] = self.price_to_precision(symbol, price)
            request['stopPx'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrders(self.extend(request, params))
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        request = {
            'orderId': id,
        }
        response = self.privateDeleteOrdersOrderId(self.extend(request, params))
        return {
            'id': id,
            'info': response,
        }

    def cancel_orders(self, ids, symbol=None, params={}):
        # cancels all open orders if no symbol specified
        # cancels all open orders of specified symbol, if symbol is specified
        self.load_markets()
        request = {
            # 'symbol': marketId,
        }
        if symbol is not None:
            marketId = self.market_id(symbol)
            request['symbol'] = marketId
        response = self.privateDeleteOrders(self.extend(request, params))
        return {
            'symbol': symbol,
            'info': response,
        }

    def fetch_trading_fees(self, params={}):
        #
        #     {
        #         makerRate: "0.002",
        #         takerRate: "0.004",
        #         volumeInUSD: "0.0"
        #     }
        #
        self.load_markets()
        response = self.privateGetFees()
        return {
            'maker': self.safe_number(response, 'makerRate'),
            'taker': self.safe_number(response, 'takerRate'),
            'info': response,
        }

    def fetch_canceled_orders(self, symbol=None, since=None, limit=None, params={}):
        state = 'CANCELED'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        state = 'FILLED'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        state = 'OPEN'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_orders_by_state(self, state, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            # 'to': unix epoch ms
            # 'from': unix epoch ms
            'status': state,
            'limit': 100,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        #     {
        #         "exOrdId":281685751028507,
        #         "tradeId":281685434947633,
        #         "execId":8847494003,
        #         "side":"BUY",
        #         "symbol":"AAVE-USDT",
        #         "price":405.34,
        #         "qty":0.1,
        #         "fee":0.162136,
        #         "timestamp":1634559249687
        #     }
        #
        id = self.safe_string(trade, 'exOrdId')
        order = self.safe_string(trade, 'tradeId')
        side = self.safe_string(trade, 'side').lower()
        marketId = self.safe_string(trade, 'symbol')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'qty')
        costString = Precise.string_mul(priceString, amountString)
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(costString)
        timestamp = self.safe_integer(trade, 'timestamp')
        datetime = self.iso8601(timestamp)
        market = self.safe_market(marketId, market, '-')
        symbol = market['symbol']
        fee = None
        feeCost = self.safe_number(trade, 'fee')
        if feeCost is not None:
            feeCurrency = None
            if market is not None:
                if side == 'buy':
                    base = market['base']
                    feeCurrency = self.safe_currency_code(base)
                elif side == 'sell':
                    quote = market['quote']
                    feeCurrency = self.safe_currency_code(quote)
            fee = {'cost': feeCost, 'currency': feeCurrency}
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': datetime,
            'symbol': symbol,
            'order': order,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': order,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        market = None
        if symbol is not None:
            request['symbol'] = self.market_id(symbol)
            market = self.market(symbol)
        trades = self.privateGetFills(self.extend(request, params))
        return self.parse_trades(trades, market, since, limit, params)  # need to define

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privatePostDepositsCurrency(self.extend(request, params))
        rawAddress = self.safe_string(response, 'address')
        tag = None
        address = None
        if rawAddress is not None:
            # if a tag or memo is used it is separated by a colon in the 'address' value
            address, tag = rawAddress.split(':')
        result = {'info': response}
        result['currency'] = currency['code']
        result['address'] = address
        if tag is not None:
            result['tag'] = tag
        return result

    def parse_transaction_state(self, state):
        states = {
            'COMPLETED': 'ok',  #
            'REJECTED': 'failed',
            'PENDING': 'pending',
            'FAILED': 'failed',
            'REFUNDED': 'refunded',
        }
        return self.safe_string(states, state, state)

    def parse_transaction(self, transaction, currency=None):
        #
        # deposit
        #
        #     {
        #         "depositId":"748e9180-be0d-4a80-e175-0156150efc95",
        #         "amount":0.009,
        #         "currency":"ETH",
        #         "address":"0xEC6B5929D454C8D9546d4221ace969E1810Fa92c",
        #         "state":"COMPLETED",
        #         "txHash":"582114562140e51a80b481c2dfebaf62b4ab9769b8ff54820bb67e34d4a3ab0c",
        #         "timestamp":1633697196241
        #     }
        #
        # withdrawal
        #
        #     {
        #         "amount":30.0,
        #         "currency":"USDT",
        #         "beneficiary":"cab00d11-6e7f-46b7-b453-2e8ef6f101fa",  # blockchain specific id
        #         "withdrawalId":"99df5ef7-eab6-4033-be49-312930fbd1ea",
        #         "fee":34.005078,
        #         "state":"COMPLETED",
        #         "timestamp":1634218452549
        #     }
        #
        type = None
        id = None
        amount = self.safe_number(transaction, 'amount')
        timestamp = self.safe_integer(transaction, 'timestamp')
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        state = self.safe_string(transaction, 'state')
        if 'depositId' in transaction:
            type = 'deposit'
            id = self.safe_string(transaction, 'depositId')
        elif 'withdrawalId' in transaction:
            type = 'withdrawal'
            id = self.safe_string(transaction, 'withdrawalId')
        feeCost = self.safe_number(transaction, 'fee') if (type == 'withdrawal') else None
        fee = None
        if feeCost is not None:
            fee = {'currency': code, 'cost': feeCost}
        address = self.safe_string(transaction, 'address')
        txid = self.safe_string(transaction, 'txhash')
        result = {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'addressFrom': None,
            'address': address,
            'addressTo': address,
            'tagFrom': None,
            'tag': None,
            'tagTo': None,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': self.parse_transaction_state(state),  # 'status':   'pending',   # 'ok', 'failed', 'canceled', string
            'updated': None,
            'comment': None,
            'fee': fee,
        }
        return result

    def fetch_withdrawal_whitelist(self, params={}):
        self.load_markets()
        response = self.privateGetWhitelist()
        result = []
        for i in range(0, len(response)):
            entry = response[i]
            result.append({
                'beneficiaryId': self.safe_string(entry, 'whitelistId'),
                'name': self.safe_string(entry, 'name'),
                'currency': self.safe_string(entry, 'currency'),
                'info': entry,
            })
        return result

    def fetch_withdrawal_whitelist_by_currency(self, currency, params={}):
        self.load_markets()
        request = {
            'currency': self.currencyId(currency),
        }
        response = self.privateGetWhitelistCurrency(self.extend(request, params))
        result = []
        for i in range(0, len(response)):
            entry = response[i]
            result.append({
                'beneficiaryId': self.safe_string(entry, 'whitelistId'),
                'name': self.safe_string(entry, 'name'),
                'currency': self.safe_string(entry, 'currency'),
                'info': entry,
            })
        return result

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        currencyid = self.currencyId(code)
        request = {
            'amount': amount,
            'currency': currencyid,
            # 'beneficiary': address/id,
            'sendMax': False,
        }
        response = self.privatePostWithdrawals(self.extend(request, params))
        #
        #     {
        #         amount: "30.0",
        #         currency: "USDT",
        #         beneficiary: "adcd43fb-9ba6-41f7-8c0d-7013482cb88f",
        #         withdrawalId: "99df5ef7-eab6-4033-be49-312930fbd1ea",
        #         fee: "34.005078",
        #         state: "PENDING",
        #         timestamp: "1634218452595"
        #     },
        #
        withdrawalId = self.safe_string(response, 'withdrawalId')
        result = {
            'info': response,
            'id': withdrawalId,
        }
        return result

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            # 'from' : integer timestamp in ms
            # 'to' : integer timestamp in ms
        }
        if since is not None:
            request['from'] = since
        response = self.privateGetWithdrawals(self.extend(request, params))
        return self.parse_transactions(response, code, since, limit)

    def fetch_withdrawal(self, id, code=None, params={}):
        self.load_markets()
        request = {
            'withdrawalId': id,
        }
        response = self.privateGetWithdrawalsWithdrawalId(self.extend(request, params))
        return self.parse_transaction(response)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            # 'from' : integer timestamp in ms
            # 'to' : integer timestap in ms
        }
        if since is not None:
            request['from'] = since
        response = self.privateGetDeposits(self.extend(request, params))
        return self.parse_transactions(response, code, since, limit)

    def fetch_deposit(self, id, code=None, params={}):
        self.load_markets()
        depositId = self.safe_string(params, 'depositId', id)
        request = {
            'depositId': depositId,
        }
        deposit = self.privateGetDepositsDepositId(self.extend(request, params))
        return self.parse_transaction(deposit)

    def fetch_balance(self, params={}):
        self.load_markets()
        accountName = self.safe_string(params, 'account', 'primary')
        params = self.omit(params, 'account')
        request = {
            'account': accountName,
        }
        response = self.privateGetAccounts(self.extend(request, params))
        #
        #     {
        #         "primary": [
        #             {
        #                 "currency":"ETH",
        #                 "balance":0.009,
        #                 "available":0.009,
        #                 "balance_local":30.82869,
        #                 "available_local":30.82869,
        #                 "rate":3425.41
        #             },
        #             ...
        #         ]
        #     }
        #
        balances = self.safe_value(response, accountName)
        if balances is None:
            raise ExchangeError(self.id + ' fetchBalance() could not find the "' + accountName + '" account')
        result = {'info': response}
        for i in range(0, len(balances)):
            entry = balances[i]
            currencyId = self.safe_string(entry, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(entry, 'available')
            account['total'] = self.safe_string(entry, 'balance')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order(self, id, symbol=None, params={}):
        # note: only works with exchange-order-id
        # does not work with clientOrderId
        self.load_markets()
        request = {
            'orderId': id,
        }
        response = self.privateGetOrdersOrderId(self.extend(request, params))
        #
        #     {
        #         "exOrdId": 11111111,
        #         "clOrdId": "ABC",
        #         "ordType": "MARKET",
        #         "ordStatus": "FILLED",
        #         "side": "BUY",
        #         "price": 0.12345,
        #         "text": "string",
        #         "symbol": "BTC-USD",
        #         "lastShares": 0.5678,
        #         "lastPx": 3500.12,
        #         "leavesQty": 10,
        #         "cumQty": 0.123345,
        #         "avgPx": 345.33,
        #         "timestamp": 1592830770594
        #     }
        #
        return self.parse_order(response)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        requestPath = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + requestPath
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            headers = {
                'X-API-Token': self.secret,
            }
            if (method == 'GET'):
                if query:
                    url += '?' + self.urlencode(query)
            else:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        # {"timestamp":"2021-10-21T15:13:58.837+00:00","status":404,"error":"Not Found","message":"","path":"/orders/505050"
        if response is None:
            return
        text = self.safe_string(response, 'text')
        if text is not None:  # if trade currency account is empty returns 200 with rejected order
            if text == 'Insufficient Balance':
                raise InsufficientFunds(self.id + ' ' + body)
        errorCode = self.safe_string(response, 'status')
        errorMessage = self.safe_string(response, 'error')
        if code is not None:
            feedback = self.id + ' ' + self.json(response)
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], errorMessage, feedback)
