# -*- coding: utf-8 -*-

from ccxt.async.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds


class hitbtc (Exchange):

    def describe(self):
        return self.deep_extend(super(hitbtc, self).describe(), {
            'id': 'hitbtc',
            'name': 'HitBTC',
            'countries': 'HK',  # Hong Kong
            'rateLimit': 1500,
            'version': '1',
            'hasCORS': False,
            'hasFetchTickers': True,
            'hasFetchOrder': True,
            'hasFetchOpenOrders': True,
            'hasFetchClosedOrders': True,
            'hasWithdraw': True,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766555-8eaec20e-5edc-11e7-9c5b-6dc69fc42f5e.jpg',
                'api': 'http://api.hitbtc.com',
                'www': 'https://hitbtc.com',
                'doc': 'https://github.com/hitbtc-com/hitbtc-api/blob/master/APIv1.md',
            },
            'api': {
                'public': {
                    'get': [
                        '{symbol}/orderbook',
                        '{symbol}/ticker',
                        '{symbol}/trades',
                        '{symbol}/trades/recent',
                        'symbols',
                        'ticker',
                        'time,'
                    ],
                },
                'trading': {
                    'get': [
                        'balance',
                        'orders/active',
                        'orders/recent',
                        'order',
                        'trades/by/order',
                        'trades',
                    ],
                    'post': [
                        'new_order',
                        'cancel_order',
                        'cancel_orders',
                    ],
                },
                'payment': {
                    'get': [
                        'balance',
                        'address/{currency}',
                        'transactions',
                        'transactions/{transaction}',
                    ],
                    'post': [
                        'transfer_to_trading',
                        'transfer_to_main',
                        'address/{currency}',
                        'payout',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': -0.01 / 100,
                    'taker': 0.1 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.0007,
                        'ETH': 0.00958,
                        'BCH': 0.0018,
                        'USDT': 5,
                        'BTG': 0.0005,
                        'LTC': 0.003,
                        'ZEC': 0.0001,
                        'XMR': 0.09,
                        '1ST': 0.84,
                        'ADX': 5.7,
                        'AE': 6.7,
                        'AEON': 0.01006,
                        'AIR': 565,
                        'AMP': 9,
                        'ANT': 6.7,
                        'ARDR': 2,
                        'ARN': 18.5,
                        'ART': 26,
                        'ATB': 0.0004,
                        'ATL': 27,
                        'ATM': 504,
                        'ATS': 860,
                        'AVT': 1.9,
                        'BAS': 113,
                        'BCN': 0.1,
                        'BET': 124,
                        'BKB': 46,
                        'BMC': 32,
                        'BMT': 100,
                        'BNT': 2.57,
                        'BQX': 4.7,
                        'BTM': 40,
                        'BTX': 0.04,
                        'BUS': 0.004,
                        'CCT': 115,
                        'CDT': 100,
                        'CDX': 30,
                        'CFI': 61,
                        'CLD': 0.88,
                        'CND': 574,
                        'CNX': 0.04,
                        'COSS': 65,
                        'CSNO': 16,
                        'CTR': 15,
                        'CTX': 146,
                        'CVC': 8.46,
                        'DBIX': 0.0168,
                        'DCN': 120000,
                        'DCT': 0.02,
                        'DDF': 342,
                        'DENT': 6240,
                        'DGB': 0.4,
                        'DGD': 0.01,
                        'DICE': 0.32,
                        'DLT': 0.26,
                        'DNT': 0.21,
                        'DOGE': 2,
                        'DOV': 34,
                        'DRPU': 24,
                        'DRT': 240,
                        'DSH': 0.017,
                        'EBET': 84,
                        'EBTC': 20,
                        'EBTCOLD': 6.6,
                        'ECAT': 14,
                        'EDG': 2,
                        'EDO': 2.9,
                        'ELE': 0.00172,
                        'ELM': 0.004,
                        'EMC': 0.03,
                        'EMGO': 14,
                        'ENJ': 163,
                        'EOS': 1.5,
                        'ERO': 34,
                        'ETBS': 15,
                        'ETC': 0.002,
                        'ETP': 0.004,
                        'EVX': 5.4,
                        'EXN': 456,
                        'FRD': 65,
                        'FUEL': 123.00105,
                        'FUN': 202.9598309,
                        'FYN': 1.849,
                        'FYP': 66.13,
                        'GNO': 0.0034,
                        'GUP': 4,
                        'GVT': 1.2,
                        'HAC': 144,
                        'HDG': 7,
                        'HGT': 1082,
                        'HPC': 0.4,
                        'HVN': 120,
                        'ICN': 0.55,
                        'ICO': 34,
                        'ICOS': 0.35,
                        'IND': 76,
                        'INDI': 5913,
                        'ITS': 15.0012,
                        'IXT': 11,
                        'KBR': 143,
                        'KICK': 112,
                        'LA': 41,
                        'LAT': 1.44,
                        'LIFE': 13000,
                        'LRC': 27,
                        'LSK': 0.3,
                        'LUN': 0.34,
                        'MAID': 5,
                        'MANA': 143,
                        'MCAP': 5.44,
                        'MIPS': 43,
                        'MNE': 1.33,
                        'MSP': 121,
                        'MTH': 92,
                        'MYB': 3.9,
                        'NDC': 165,
                        'NEBL': 0.04,
                        'NET': 3.96,
                        'NTO': 998,
                        'NXC': 13.39,
                        'NXT': 3,
                        'OAX': 15,
                        'ODN': 0.004,
                        'OMG': 2,
                        'OPT': 335,
                        'ORME': 2.8,
                        'OTN': 0.57,
                        'PAY': 3.1,
                        'PIX': 96,
                        'PLBT': 0.33,
                        'PLR': 114,
                        'PLU': 0.87,
                        'POE': 784,
                        'POLL': 3.5,
                        'PPT': 2,
                        'PRE': 32,
                        'PRG': 39,
                        'PRO': 41,
                        'PRS': 60,
                        'PTOY': 0.5,
                        'QAU': 63,
                        'QCN': 0.03,
                        'QTUM': 0.04,
                        'QVT': 64,
                        'REP': 0.02,
                        'RKC': 15,
                        'RVT': 14,
                        'SAN': 2.24,
                        'SBD': 0.03,
                        'SCL': 2.6,
                        'SISA': 1640,
                        'SKIN': 407,
                        'SMART': 0.4,
                        'SMS': 0.0375,
                        'SNC': 36,
                        'SNGLS': 4,
                        'SNM': 48,
                        'SNT': 233,
                        'STEEM': 0.01,
                        'STRAT': 0.01,
                        'STU': 14,
                        'STX': 11,
                        'SUB': 17,
                        'SUR': 3,
                        'SWT': 0.51,
                        'TAAS': 0.91,
                        'TBT': 2.37,
                        'TFL': 15,
                        'TIME': 0.03,
                        'TIX': 7.1,
                        'TKN': 1,
                        'TKR': 84,
                        'TNT': 90,
                        'TRST': 1.6,
                        'TRX': 1395,
                        'UET': 480,
                        'UGT': 15,
                        'VEN': 14,
                        'VERI': 0.037,
                        'VIB': 50,
                        'VIBE': 145,
                        'VOISE': 618,
                        'WEALTH': 0.0168,
                        'WINGS': 2.4,
                        'WTC': 0.75,
                        'XAUR': 3.23,
                        'XDN': 0.01,
                        'XEM': 15,
                        'XUC': 0.9,
                        'YOYOW': 140,
                        'ZAP': 24,
                        'ZRX': 23,
                        'ZSC': 191,
                    },
                    'deposit': {
                        'BTC': 0,
                        'ETH': 0,
                        'BCH': 0,
                        'USDT': 0,
                        'BTG': 0,
                        'LTC': 0,
                        'ZEC': 0,
                        'XMR': 0,
                        '1ST': 0,
                        'ADX': 0,
                        'AE': 0,
                        'AEON': 0,
                        'AIR': 0,
                        'AMP': 0,
                        'ANT': 0,
                        'ARDR': 0,
                        'ARN': 0,
                        'ART': 0,
                        'ATB': 0,
                        'ATL': 0,
                        'ATM': 0,
                        'ATS': 0,
                        'AVT': 0,
                        'BAS': 0,
                        'BCN': 0,
                        'BET': 0,
                        'BKB': 0,
                        'BMC': 0,
                        'BMT': 0,
                        'BNT': 0,
                        'BQX': 0,
                        'BTM': 0,
                        'BTX': 0,
                        'BUS': 0,
                        'CCT': 0,
                        'CDT': 0,
                        'CDX': 0,
                        'CFI': 0,
                        'CLD': 0,
                        'CND': 0,
                        'CNX': 0,
                        'COSS': 0,
                        'CSNO': 0,
                        'CTR': 0,
                        'CTX': 0,
                        'CVC': 0,
                        'DBIX': 0,
                        'DCN': 0,
                        'DCT': 0,
                        'DDF': 0,
                        'DENT': 0,
                        'DGB': 0,
                        'DGD': 0,
                        'DICE': 0,
                        'DLT': 0,
                        'DNT': 0,
                        'DOGE': 0,
                        'DOV': 0,
                        'DRPU': 0,
                        'DRT': 0,
                        'DSH': 0,
                        'EBET': 0,
                        'EBTC': 0,
                        'EBTCOLD': 0,
                        'ECAT': 0,
                        'EDG': 0,
                        'EDO': 0,
                        'ELE': 0,
                        'ELM': 0,
                        'EMC': 0,
                        'EMGO': 0,
                        'ENJ': 0,
                        'EOS': 0,
                        'ERO': 0,
                        'ETBS': 0,
                        'ETC': 0,
                        'ETP': 0,
                        'EVX': 0,
                        'EXN': 0,
                        'FRD': 0,
                        'FUEL': 0,
                        'FUN': 0,
                        'FYN': 0,
                        'FYP': 0,
                        'GNO': 0,
                        'GUP': 0,
                        'GVT': 0,
                        'HAC': 0,
                        'HDG': 0,
                        'HGT': 0,
                        'HPC': 0,
                        'HVN': 0,
                        'ICN': 0,
                        'ICO': 0,
                        'ICOS': 0,
                        'IND': 0,
                        'INDI': 0,
                        'ITS': 0,
                        'IXT': 0,
                        'KBR': 0,
                        'KICK': 0,
                        'LA': 0,
                        'LAT': 0,
                        'LIFE': 0,
                        'LRC': 0,
                        'LSK': 0,
                        'LUN': 0,
                        'MAID': 0,
                        'MANA': 0,
                        'MCAP': 0,
                        'MIPS': 0,
                        'MNE': 0,
                        'MSP': 0,
                        'MTH': 0,
                        'MYB': 0,
                        'NDC': 0,
                        'NEBL': 0,
                        'NET': 0,
                        'NTO': 0,
                        'NXC': 0,
                        'NXT': 0,
                        'OAX': 0,
                        'ODN': 0,
                        'OMG': 0,
                        'OPT': 0,
                        'ORME': 0,
                        'OTN': 0,
                        'PAY': 0,
                        'PIX': 0,
                        'PLBT': 0,
                        'PLR': 0,
                        'PLU': 0,
                        'POE': 0,
                        'POLL': 0,
                        'PPT': 0,
                        'PRE': 0,
                        'PRG': 0,
                        'PRO': 0,
                        'PRS': 0,
                        'PTOY': 0,
                        'QAU': 0,
                        'QCN': 0,
                        'QTUM': 0,
                        'QVT': 0,
                        'REP': 0,
                        'RKC': 0,
                        'RVT': 0,
                        'SAN': 0,
                        'SBD': 0,
                        'SCL': 0,
                        'SISA': 0,
                        'SKIN': 0,
                        'SMART': 0,
                        'SMS': 0,
                        'SNC': 0,
                        'SNGLS': 0,
                        'SNM': 0,
                        'SNT': 0,
                        'STEEM': 0,
                        'STRAT': 0,
                        'STU': 0,
                        'STX': 0,
                        'SUB': 0,
                        'SUR': 0,
                        'SWT': 0,
                        'TAAS': 0,
                        'TBT': 0,
                        'TFL': 0,
                        'TIME': 0,
                        'TIX': 0,
                        'TKN': 0,
                        'TKR': 0,
                        'TNT': 0,
                        'TRST': 0,
                        'TRX': 0,
                        'UET': 0,
                        'UGT': 0,
                        'VEN': 0,
                        'VERI': 0,
                        'VIB': 0,
                        'VIBE': 0,
                        'VOISE': 0,
                        'WEALTH': 0,
                        'WINGS': 0,
                        'WTC': 0,
                        'XAUR': 0,
                        'XDN': 0,
                        'XEM': 0,
                        'XUC': 0,
                        'YOYOW': 0,
                        'ZAP': 0,
                        'ZRX': 0,
                        'ZSC': 0,
                    },
                },
            },
        })

    def common_currency_code(self, currency):
        if currency == 'XBT':
            return 'BTC'
        if currency == 'DRK':
            return 'DASH'
        if currency == 'CAT':
            return 'BitClave'
        return currency

    async def fetch_markets(self):
        markets = await self.publicGetSymbols()
        result = []
        for p in range(0, len(markets['symbols'])):
            market = markets['symbols'][p]
            id = market['symbol']
            base = market['commodity']
            quote = market['currency']
            lot = float(market['lot'])
            step = float(market['step'])
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'lot': lot,
                'step': step,
                'info': market,
                'precision': {
                    'amount': self.precision_from_string(market['lot']),
                    'price': self.precision_from_string(market['step']),
                },
                'limits': {
                    'amount': {
                        'min': lot,
                        'max': None,
                    },
                    'price': {
                        'min': step,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        method = self.safe_string(params, 'type', 'trading')
        method += 'GetBalance'
        query = self.omit(params, 'type')
        response = await getattr(self, method)(query)
        balances = response['balance']
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            code = balance['currency_code']
            currency = self.common_currency_code(code)
            free = self.safe_float(balance, 'cash', 0.0)
            free = self.safe_float(balance, 'balance', free)
            used = self.safe_float(balance, 'reserved', 0.0)
            account = {
                'free': free,
                'used': used,
                'total': self.sum(free, used),
            }
            result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, params={}):
        await self.load_markets()
        orderbook = await self.publicGetSymbolOrderbook(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['timestamp']
        symbol = None
        if market:
            symbol = market['symbol']
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'ask': self.safe_float(ticker, 'ask'),
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': None,
            'first': None,
            'last': self.safe_float(ticker, 'last'),
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'volume_quote'),
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        tickers = await self.publicGetTicker(params)
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetSymbolTicker(self.extend({
            'symbol': market['id'],
        }, params))
        if 'message' in ticker:
            raise ExchangeError(self.id + ' ' + ticker['message'])
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        return {
            'info': trade,
            'id': trade[0],
            'timestamp': trade[3],
            'datetime': self.iso8601(trade[3]),
            'symbol': market['symbol'],
            'type': None,
            'side': trade[4],
            'price': float(trade[1]),
            'amount': float(trade[2]),
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        response = await self.publicGetSymbolTrades(self.extend({
            'symbol': market['id'],
            # 'from': 0,
            # 'till': 100,
            # 'by': 'ts',  # or by trade_id
            # 'sort': 'desc',  # or asc
            # 'start_index': 0,
            # 'max_results': 1000,
            # 'format_item': 'object',
            # 'format_price': 'number',
            # 'format_amount': 'number',
            # 'format_tid': 'string',
            # 'format_timestamp': 'millisecond',
            # 'format_wrap': False,
            'side': 'true',
        }, params))
        return self.parse_trades(response['trades'], market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        # check if amount can be evenly divided into lots
        # they want integer quantity in lot units
        quantity = float(amount) / market['lot']
        wholeLots = int(round(quantity))
        difference = quantity - wholeLots
        if abs(difference) > market['step']:
            raise ExchangeError(self.id + ' order amount should be evenly divisible by lot unit size of ' + str(market['lot']))
        clientOrderId = self.milliseconds()
        order = {
            'clientOrderId': str(clientOrderId),
            'symbol': market['id'],
            'side': side,
            'quantity': str(wholeLots),  # quantity in integer lot units
            'type': type,
        }
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        else:
            order['timeInForce'] = 'FOK'
        response = await self.tradingPostNewOrder(self.extend(order, params))
        return {
            'info': response,
            'id': response['ExecutionReport']['clientOrderId'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.tradingPostCancelOrder(self.extend({
            'clientOrderId': id,
        }, params))

    def get_order_status(self, status):
        statuses = {
            'new': 'open',
            'partiallyFilled': 'open',
            'filled': 'closed',
            'canceled': 'canceled',
            'rejected': 'rejected',
            'expired': 'expired',
        }
        return self.safe_string(statuses, status)

    def parse_order(self, order, market=None):
        timestamp = int(order['lastTimestamp'])
        symbol = None
        if not market:
            market = self.markets_by_id[order['symbol']]
        status = self.safe_string(order, 'orderStatus')
        if status:
            status = self.get_order_status(status)
        averagePrice = self.safe_float(order, 'avgPrice', 0.0)
        price = self.safe_float(order, 'orderPrice')
        amount = self.safe_float(order, 'orderQuantity')
        remaining = self.safe_float(order, 'quantityLeaves')
        filled = None
        cost = None
        if market:
            symbol = market['symbol']
            amount *= market['lot']
            remaining *= market['lot']
        if amount and remaining:
            filled = amount - remaining
            cost = averagePrice * filled
        return {
            'id': str(order['clientOrderId']),
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'status': status,
            'symbol': symbol,
            'type': order['type'],
            'side': order['side'],
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.tradingGetOrder(self.extend({
            'clientOrderId': id,
        }, params))
        return self.parse_order(response['orders'][0])

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        statuses = ['new', 'partiallyFiiled']
        market = None
        request = {
            'sort': 'desc',
            'statuses': ','.join(statuses),
        }
        if symbol:
            market = self.market(symbol)
            request['symbols'] = market['id']
        response = await self.tradingGetOrdersActive(self.extend(request, params))
        return self.parse_orders(response['orders'], market, since, limit)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        statuses = ['filled', 'canceled', 'rejected', 'expired']
        request = {
            'sort': 'desc',
            'statuses': ','.join(statuses),
            'max_results': 1000,
        }
        if symbol:
            market = self.market(symbol)
            request['symbols'] = market['id']
        response = await self.tradingGetOrdersRecent(self.extend(request, params))
        return self.parse_orders(response['orders'], market, since, limit)

    async def withdraw(self, currency, amount, address, params={}):
        await self.load_markets()
        response = await self.paymentPostPayout(self.extend({
            'currency_code': currency,
            'amount': amount,
            'address': address,
        }, params))
        return {
            'info': response,
            'id': response['transaction'],
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/' + 'api' + '/' + self.version + '/' + api + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            payload = {'nonce': nonce, 'apikey': self.apiKey}
            query = self.extend(payload, query)
            if method == 'GET':
                url += '?' + self.urlencode(query)
            else:
                url += '?' + self.urlencode(payload)
            auth = url
            if method == 'POST':
                if query:
                    body = self.urlencode(query)
                    auth += body
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Signature': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512).lower(),
            }
        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'code' in response:
            if 'ExecutionReport' in response:
                if response['ExecutionReport']['orderRejectReason'] == 'orderExceedsLimit':
                    raise InsufficientFunds(self.id + ' ' + self.json(response))
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
