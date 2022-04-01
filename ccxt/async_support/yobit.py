# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.precise import Precise


class yobit(Exchange):

    def describe(self):
        return self.deep_extend(super(yobit, self).describe(), {
            'id': 'yobit',
            'name': 'YoBit',
            'countries': ['RU'],
            'rateLimit': 3000,  # responses are cached every 2 seconds
            'version': '3',
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'createDepositAddress': True,
                'createMarketOrder': None,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'fetchBalance': True,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchDepositAddress': True,
                'fetchDeposits': None,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': True,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': True,
                'fetchTransactions': None,
                'fetchWithdrawals': None,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766910-cdcbfdae-5eea-11e7-9859-03fea873272d.jpg',
                'api': {
                    'public': 'https://yobit.net/api',
                    'private': 'https://yobit.net/tapi',
                },
                'www': 'https://www.yobit.net',
                'doc': 'https://www.yobit.net/en/api/',
                'fees': 'https://www.yobit.net/en/fees/',
            },
            'api': {
                'public': {
                    'get': [
                        'depth/{pair}',
                        'info',
                        'ticker/{pair}',
                        'trades/{pair}',
                    ],
                },
                'private': {
                    'post': [
                        'ActiveOrders',
                        'CancelOrder',
                        'GetDepositAddress',
                        'getInfo',
                        'OrderInfo',
                        'Trade',
                        'TradeHistory',
                        'WithdrawCoinsToAddress',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.002,
                    'taker': 0.002,
                },
                'funding': {
                    'withdraw': {},
                },
            },
            'commonCurrencies': {
                'AIR': 'AirCoin',
                'ANI': 'ANICoin',
                'ANT': 'AntsCoin',  # what is self, a coin for ants?
                'ATMCHA': 'ATM',
                'ASN': 'Ascension',
                'AST': 'Astral',
                'ATM': 'Autumncoin',
                'AUR': 'AuroraCoin',
                'BAB': 'Babel',
                'BAN': 'BANcoin',
                'BCC': 'BCH',
                'BCS': 'BitcoinStake',
                'BITS': 'Bitstar',
                'BLN': 'Bulleon',
                'BNS': 'Benefit Bonus Coin',
                'BOT': 'BOTcoin',
                'BON': 'BONES',
                'BPC': 'BitcoinPremium',
                'BST': 'BitStone',
                'BTS': 'Bitshares2',
                'CAT': 'BitClave',
                'CBC': 'CryptoBossCoin',
                'CMT': 'CometCoin',
                'COIN': 'Coin.com',
                'COV': 'Coven Coin',
                'COVX': 'COV',
                'CPC': 'Capricoin',
                'CREDIT': 'Creditbit',
                'CS': 'CryptoSpots',
                'DCT': 'Discount',
                'DFT': 'DraftCoin',
                'DGD': 'DarkGoldCoin',
                'DIRT': 'DIRTY',
                'DROP': 'FaucetCoin',
                'DSH': 'DASH',
                'EGC': 'EverGreenCoin',
                'EGG': 'EggCoin',
                'EKO': 'EkoCoin',
                'ENTER': 'ENTRC',
                'EPC': 'ExperienceCoin',
                'ESC': 'EdwardSnowden',
                'EUROPE': 'EUROP',
                'EXT': 'LifeExtension',
                'FUND': 'FUNDChains',
                'FUNK': 'FUNKCoin',
                'FX': 'FCoin',
                'GCC': 'GlobalCryptocurrency',
                'GEN': 'Genstake',
                'GENE': 'Genesiscoin',
                'GMR': 'Gimmer',
                'GOLD': 'GoldMint',
                'GOT': 'Giotto Coin',
                'GSX': 'GlowShares',
                'GT': 'GTcoin',
                'HTML5': 'HTML',
                'HYPERX': 'HYPER',
                'ICN': 'iCoin',
                'INSANE': 'INSN',
                'JNT': 'JointCoin',
                'JPC': 'JupiterCoin',
                'JWL': 'Jewels',
                'KNC': 'KingN Coin',
                'LBTCX': 'LiteBitcoin',
                'LIZI': 'LiZi',
                'LOC': 'LocoCoin',
                'LOCX': 'LOC',
                'LUNYR': 'LUN',
                'LUN': 'LunarCoin',  # they just change the ticker if it is already taken
                'LUNA': 'Luna Coin',
                'MASK': 'Yobit MASK',
                'MDT': 'Midnight',
                'MEME': 'Memez Token',  # conflict with Meme Inu / Degenerator Meme
                'MIS': 'MIScoin',
                'MM': 'MasterMint',  # conflict with MilliMeter
                'NAV': 'NavajoCoin',
                'NBT': 'NiceBytes',
                'OMG': 'OMGame',
                'ONX': 'Onix',
                'PAC': '$PAC',
                'PLAY': 'PlayCoin',
                'PIVX': 'Darknet',
                'PRS': 'PRE',
                'PURE': 'PurePOS',
                'PUTIN': 'PutinCoin',
                'SPACE': 'Spacecoin',
                'STK': 'StakeCoin',
                'SUB': 'Subscriptio',
                'PAY': 'EPAY',
                'PLC': 'Platin Coin',
                'RAI': 'RaiderCoin',
                'RCN': 'RCoin',
                'REP': 'Republicoin',
                'RUR': 'RUB',
                'SBTC': 'Super Bitcoin',
                'SMC': 'SmartCoin',
                'SOLO': 'SoloCoin',
                'STAR': 'StarCoin',
                'SUPER': 'SuperCoin',
                'TNS': 'Transcodium',
                'TTC': 'TittieCoin',
                'UNI': 'Universe',
                'UST': 'Uservice',
                'VOL': 'VolumeCoin',
                'XIN': 'XINCoin',
                'XMT': 'SummitCoin',
                'XRA': 'Ratecoin',
            },
            'options': {
                # 'fetchTickersMaxLength': 2048,
                'fetchOrdersRequiresSymbol': True,
                'fetchTickersMaxLength': 512,
            },
            'exceptions': {
                'exact': {
                    '803': InvalidOrder,  # "Count could not be less than 0.001."(selling below minAmount)
                    '804': InvalidOrder,  # "Count could not be more than 10000."(buying above maxAmount)
                    '805': InvalidOrder,  # "price could not be less than X."(minPrice violation on buy & sell)
                    '806': InvalidOrder,  # "price could not be more than X."(maxPrice violation on buy & sell)
                    '807': InvalidOrder,  # "cost could not be less than X."(minCost violation on buy & sell)
                    '831': InsufficientFunds,  # "Not enougth X to create buy order."(buying with balance.quote < order.cost)
                    '832': InsufficientFunds,  # "Not enougth X to create sell order."(selling with balance.base < order.amount)
                    '833': OrderNotFound,  # "Order with id X was not found."(cancelling non-existent, closed and cancelled order)
                },
                'broad': {
                    'Invalid pair name': ExchangeError,  # {"success":0,"error":"Invalid pair name: btc_eth"}
                    'invalid api key': AuthenticationError,
                    'invalid sign': AuthenticationError,
                    'api key dont have trade permission': AuthenticationError,
                    'invalid parameter': InvalidOrder,
                    'invalid order': InvalidOrder,
                    'The given order has already been cancelled': InvalidOrder,
                    'Requests too often': DDoSProtection,
                    'not available': ExchangeNotAvailable,
                    'data unavailable': ExchangeNotAvailable,
                    'external service unavailable': ExchangeNotAvailable,
                    'Total transaction amount': InvalidOrder,  # {"success": 0, "error": "Total transaction amount is less than minimal total: 0.00010000"}
                    'The given order has already been closed and cannot be cancelled': InvalidOrder,
                    'Insufficient funds': InsufficientFunds,
                    'invalid key': AuthenticationError,
                    'invalid nonce': InvalidNonce,  # {"success":0,"error":"invalid nonce(has already been used)"}'
                    'Total order amount is less than minimal amount': InvalidOrder,
                    'Rate Limited': RateLimitExceeded,
                },
            },
            'orders': {},  # orders cache / emulation
        })

    def parse_balance(self, response):
        balances = self.safe_value(response, 'return', {})
        timestamp = self.safe_integer(balances, 'server_time')
        result = {
            'info': response,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        free = self.safe_value(balances, 'funds', {})
        total = self.safe_value(balances, 'funds_incl_orders', {})
        currencyIds = list(self.extend(free, total).keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(free, currencyId)
            account['total'] = self.safe_string(total, currencyId)
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetInfo(params)
        #
        #     {
        #         "success":1,
        #         "return":{
        #             "funds":{
        #                 "ltc":22,
        #                 "nvc":423.998,
        #                 "ppc":10,
        #             },
        #             "funds_incl_orders":{
        #                 "ltc":32,
        #                 "nvc":523.998,
        #                 "ppc":20,
        #             },
        #             "rights":{
        #                 "info":1,
        #                 "trade":0,
        #                 "withdraw":0
        #             },
        #             "transaction_count":0,
        #             "open_orders":1,
        #             "server_time":1418654530
        #         }
        #     }
        #
        return self.parse_balance(response)

    async def fetch_markets(self, params={}):
        response = await self.publicGetInfo(params)
        #
        #     {
        #         "server_time":1615856752,
        #         "pairs":{
        #             "ltc_btc":{
        #                 "decimal_places":8,
        #                 "min_price":0.00000001,
        #                 "max_price":10000,
        #                 "min_amount":0.0001,
        #                 "min_total":0.0001,
        #                 "hidden":0,
        #                 "fee":0.2,
        #                 "fee_buyer":0.2,
        #                 "fee_seller":0.2
        #             },
        #         },
        #     }
        #
        markets = self.safe_value(response, 'pairs')
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = baseId.upper()
            quote = quoteId.upper()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            hidden = self.safe_integer(market, 'hidden')
            feeString = self.safe_string(market, 'fee')
            feeString = Precise.string_div(feeString, '100')
            # yobit maker = taker
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
                'active': (hidden == 0),
                'contract': False,
                'linear': None,
                'inverse': None,
                'taker': self.parse_number(feeString),
                'maker': self.parse_number(feeString),
                'contractSize': None,
                'expiry': None,
                'expiryDatetime': None,
                'strike': None,
                'optionType': None,
                'precision': {
                    'amount': self.safe_integer(market, 'decimal_places'),
                    'price': self.safe_integer(market, 'decimal_places'),
                },
                'limits': {
                    'leverage': {
                        'min': None,
                        'max': None,
                    },
                    'amount': {
                        'min': self.safe_number(market, 'min_amount'),
                        'max': self.safe_number(market, 'max_amount'),
                    },
                    'price': {
                        'min': self.safe_number(market, 'min_price'),
                        'max': self.safe_number(market, 'max_price'),
                    },
                    'cost': {
                        'min': self.safe_number(market, 'min_total'),
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['limit'] = limit  # default = 150, max = 2000
        response = await self.publicGetDepthPair(self.extend(request, params))
        market_id_in_reponse = (market['id'] in response)
        if not market_id_in_reponse:
            raise ExchangeError(self.id + ' ' + market['symbol'] + ' order book is empty or not available')
        orderbook = response[market['id']]
        return self.parse_order_book(orderbook, symbol)

    async def fetch_order_books(self, symbols=None, limit=None, params={}):
        await self.load_markets()
        ids = None
        if symbols is None:
            ids = '-'.join(self.ids)
            # max URL length is 2083 symbols, including http schema, hostname, tld, etc...
            if len(ids) > 2048:
                numIds = len(self.ids)
                raise ExchangeError(self.id + ' has ' + str(numIds) + ' symbols exceeding max URL length, you are required to specify a list of symbols in the first argument to fetchOrderBooks')
        else:
            ids = self.market_ids(symbols)
            ids = '-'.join(ids)
        request = {
            'pair': ids,
            # 'ignore_invalid': True,
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.publicGetDepthPair(self.extend(request, params))
        result = {}
        ids = list(response.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = self.safe_symbol(id)
            result[symbol] = self.parse_order_book(response[id], symbol)
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         high: 0.03497582,
        #         low: 0.03248474,
        #         avg: 0.03373028,
        #         vol: 120.11485715062999,
        #         vol_cur: 3572.24914074,
        #         last: 0.0337611,
        #         buy: 0.0337442,
        #         sell: 0.03377798,
        #         updated: 1537522009
        #     }
        #
        timestamp = self.safe_timestamp(ticker, 'updated')
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({
            'symbol': self.safe_symbol(None, market),
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
            'average': self.safe_string(ticker, 'avg'),
            'baseVolume': self.safe_string(ticker, 'vol_cur'),
            'quoteVolume': self.safe_string(ticker, 'vol'),
            'info': ticker,
        }, market, False)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        ids = self.ids
        if symbols is None:
            numIds = len(ids)
            ids = '-'.join(ids)
            maxLength = self.safe_integer(self.options, 'fetchTickersMaxLength', 2048)
            # max URL length is 2048 symbols, including http schema, hostname, tld, etc...
            if len(ids) > self.options['fetchTickersMaxLength']:
                raise ArgumentsRequired(self.id + ' has ' + str(numIds) + ' markets exceeding max URL length for self endpoint(' + str(maxLength) + ' characters), please, specify a list of symbols of interest in the first argument to fetchTickers')
        else:
            ids = self.market_ids(symbols)
            ids = '-'.join(ids)
        request = {
            'pair': ids,
        }
        tickers = await self.publicGetTickerPair(self.extend(request, params))
        result = {}
        keys = list(tickers.keys())
        for k in range(0, len(keys)):
            id = keys[k]
            ticker = tickers[id]
            market = self.safe_market(id)
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_ticker(self, symbol, params={}):
        tickers = await self.fetch_tickers([symbol], params)
        return tickers[symbol]

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'timestamp')
        side = self.safe_string(trade, 'type')
        if side == 'ask':
            side = 'sell'
        elif side == 'bid':
            side = 'buy'
        priceString = self.safe_string_2(trade, 'rate', 'price')
        id = self.safe_string_2(trade, 'trade_id', 'tid')
        order = self.safe_string(trade, 'order_id')
        marketId = self.safe_string(trade, 'pair')
        symbol = self.safe_symbol(marketId, market)
        amountString = self.safe_string(trade, 'amount')
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        type = 'limit'  # all trades are still limit trades
        fee = None
        feeCost = self.safe_number(trade, 'commission')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'commissionCurrency')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            fee = {
                'cost': feeCost,
                'currency': feeCurrencyCode,
            }
        isYourOrder = self.safe_value(trade, 'is_your_order')
        if isYourOrder is not None:
            if fee is None:
                fee = self.calculate_fee(symbol, type, side, amount, price, 'taker')
        return {
            'id': id,
            'order': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = await self.publicGetTradesPair(self.extend(request, params))
        if isinstance(response, list):
            numElements = len(response)
            if numElements == 0:
                return []
        return self.parse_trades(response[market['id']], market, since, limit)

    async def fetch_trading_fees(self, params={}):
        await self.load_markets()
        response = await self.publicGetInfo(params)
        #
        #     {
        #         "server_time":1615856752,
        #         "pairs":{
        #             "ltc_btc":{
        #                 "decimal_places":8,
        #                 "min_price":0.00000001,
        #                 "max_price":10000,
        #                 "min_amount":0.0001,
        #                 "min_total":0.0001,
        #                 "hidden":0,
        #                 "fee":0.2,
        #                 "fee_buyer":0.2,
        #                 "fee_seller":0.2
        #             },
        #             ...
        #         },
        #     }
        #
        pairs = self.safe_value(response, 'pairs')
        marketIds = list(pairs.keys())
        result = {}
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            pair = self.safe_value(pairs, marketId, {})
            symbol = self.safe_symbol(marketId, None, '_')
            takerString = self.safe_string(pair, 'fee_buyer')
            makerString = self.safe_string(pair, 'fee_seller')
            taker = self.parse_number(Precise.string_div(takerString, '100'))
            maker = self.parse_number(Precise.string_div(makerString, '100'))
            result[symbol] = {
                'info': pair,
                'symbol': symbol,
                'taker': taker,
                'maker': maker,
                'percentage': True,
                'tierBased': False,
            }
        return result

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': side,
            'amount': self.amount_to_precision(symbol, amount),
            'rate': self.price_to_precision(symbol, price),
        }
        response = await self.privatePostTrade(self.extend(request, params))
        id = None
        status = 'open'
        filled = 0.0
        remaining = amount
        if 'return' in response:
            id = self.safe_string(response['return'], 'order_id')
            if id == '0':
                id = self.safe_string(response['return'], 'init_order_id')
                status = 'closed'
            filled = self.safe_number(response['return'], 'received', 0.0)
            remaining = self.safe_number(response['return'], 'remains', amount)
        timestamp = self.milliseconds()
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': price * filled,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'fee': None,
            # 'trades': self.parse_trades(order['trades'], market),
            'info': response,
            'clientOrderId': None,
            'average': None,
            'trades': None,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_id': int(id),
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'closed',
            '2': 'canceled',
            '3': 'open',  # or partially-filled and canceled? https://github.com/ccxt/ccxt/issues/1594
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        timestamp = self.safe_timestamp(order, 'timestamp_created')
        marketId = self.safe_string(order, 'pair')
        symbol = self.safe_symbol(marketId, market)
        remaining = self.safe_string(order, 'amount')
        amount = self.safe_string(order, 'start_amount')
        price = self.safe_string(order, 'rate')
        fee = None
        type = 'limit'
        side = self.safe_string(order, 'type')
        return self.safe_order({
            'info': order,
            'id': id,
            'clientOrderId': None,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': None,
            'amount': amount,
            'remaining': remaining,
            'filled': None,
            'status': status,
            'fee': fee,
            'average': None,
            'trades': None,
        }, market)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_id': int(id),
        }
        response = await self.privatePostOrderInfo(self.extend(request, params))
        id = str(id)
        orders = self.safe_value(response, 'return', {})
        return self.parse_order(self.extend({'id': id}, orders[id]))

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = await self.privatePostActiveOrders(self.extend(request, params))
        orders = self.safe_value(response, 'return', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a `symbol` argument')
        await self.load_markets()
        market = self.market(symbol)
        # some derived classes use camelcase notation for request fields
        request = {
            # 'from': 123456789,  # trade ID, from which the display starts numerical 0(test result: liqui ignores self field)
            # 'count': 1000,  # the number of trades for display numerical, default = 1000
            # 'from_id': trade ID, from which the display starts numerical 0
            # 'end_id': trade ID on which the display ends numerical ∞
            # 'order': 'ASC',  # sorting, default = DESC(test result: liqui ignores self field, most recent trade always goes last)
            # 'since': 1234567890,  # UTC start time, default = 0(test result: liqui ignores self field)
            # 'end': 1234567890,  # UTC end time, default = ∞(test result: liqui ignores self field)
            'pair': market['id'],
        }
        if limit is not None:
            request['count'] = int(limit)
        if since is not None:
            request['since'] = int(since / 1000)
        response = await self.privatePostTradeHistory(self.extend(request, params))
        trades = self.safe_value(response, 'return', {})
        ids = list(trades.keys())
        result = []
        for i in range(0, len(ids)):
            id = ids[i]
            trade = self.parse_trade(self.extend(trades[id], {
                'trade_id': id,
            }), market)
            result.append(trade)
        return self.filter_by_symbol_since_limit(result, market['symbol'], since, limit)

    async def create_deposit_address(self, code, params={}):
        request = {
            'need_new': 1,
        }
        response = await self.fetch_deposit_address(code, self.extend(request, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response['info'],
        }

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'coinName': currency['id'],
            'need_new': 0,
        }
        response = await self.privatePostGetDepositAddress(self.extend(request, params))
        address = self.safe_string(response['return'], 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'network': None,
            'info': response,
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'coinName': currency['id'],
            'amount': amount,
            'address': address,
        }
        # no docs on the tag, yet...
        if tag is not None:
            raise ExchangeError(self.id + ' withdraw() does not support the tag argument yet due to a lack of docs on withdrawing with tag/memo on behalf of the exchange.')
        response = await self.privatePostWithdrawCoinsToAddress(self.extend(request, params))
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'nonce': nonce,
                'method': path,
            }, query))
            signature = self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': signature,
            }
        elif api == 'public':
            url += '/' + self.version + '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            url += '/' + self.implode_params(path, params)
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                if query:
                    body = self.json(query)
                    headers = {
                        'Content-Type': 'application/json',
                    }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        if 'success' in response:
            #
            # 1 - Liqui only returns the integer 'success' key from their private API
            #
            #     {"success": 1, ...} httpCode == 200
            #     {"success": 0, ...} httpCode == 200
            #
            # 2 - However, exchanges derived from Liqui, can return non-integers
            #
            #     It can be a numeric string
            #     {"sucesss": "1", ...}
            #     {"sucesss": "0", ...}, httpCode >= 200(can be 403, 502, etc)
            #
            #     Or just a string
            #     {"success": "true", ...}
            #     {"success": "false", ...}, httpCode >= 200
            #
            #     Or a boolean
            #     {"success": True, ...}
            #     {"success": False, ...}, httpCode >= 200
            #
            # 3 - Oversimplified, Python PEP8 forbids comparison operator(==) of different types
            #
            # 4 - We do not want to copy-paste and duplicate the code of self handler to other exchanges derived from Liqui
            #
            # To cover points 1, 2, 3 and 4 combined self handler should work like self:
            #
            success = self.safe_value(response, 'success', False)
            if isinstance(success, str):
                if (success == 'true') or (success == '1'):
                    success = True
                else:
                    success = False
            if not success:
                code = self.safe_string(response, 'code')
                message = self.safe_string(response, 'error')
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
                raise ExchangeError(feedback)  # unknown message
