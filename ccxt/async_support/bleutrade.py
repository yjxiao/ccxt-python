# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder


class bleutrade(Exchange):

    def describe(self):
        return self.deep_extend(super(bleutrade, self).describe(), {
            'id': 'bleutrade',
            'name': 'Bleutrade',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'certified': False,
            'has': {
                'CORS': True,
                'cancelOrder': False,  # todo
                'createLimitOrder': False,  # todo
                'createMarketOrder': False,  # todo
                'createOrder': False,  # todo
                'editOrder': False,  # todo
                'withdraw': False,  # todo
                'fetchTrades': False,
                'fetchTickers': True,
                'fetchTicker': True,
                'fetchOrders': False,
                'fetchClosedOrders': True,
                'fetchWithdrawals': True,
                'fetchOrderTrades': False,
                'fetchLedger': True,
                'fetchDepositAddress': True,
            },
            'timeframes': {
                '15m': '15m',
                '20m': '20m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '3h': '3h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
            },
            'hostname': 'bleutrade.com',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30303000-b602dbe6-976d-11e7-956d-36c5049c01e7.jpg',
                'api': {
                    'v3Private': 'https://{hostname}/api/v3/private',
                    'v3Public': 'https://{hostname}/api/v3/public',
                },
                'www': ['https://bleutrade.com'],
                'doc': [
                    'https://app.swaggerhub.com/apis-docs/bleu/white-label/3.0.0',
                ],
                'fees': 'https://bleutrade.com/fees/',
            },
            'api': {
                'v3Public': {
                    'get': [
                        'getassets',
                        'getmarkets',
                        'getticker',
                        'getmarketsummary',
                        'getmarketsummaries',
                        'getorderbook',
                        'getmarkethistory',
                        'getcandles',
                    ],
                },
                'v3Private': {
                    'post': [
                        'getbalance',
                        'getbalances',
                        'buylimit',
                        'selllimit',
                        'buylimitami',
                        'selllimitami',
                        'buystoplimit',
                        'sellstoplimit',
                        'ordercancel',
                        'getopenorders',
                        'getcloseorders',
                        'getdeposithistory',
                        'getdepositaddress',
                        'getmytransactions',
                        'withdraw',
                        'directtransfer',
                        'getwithdrawhistory',
                        'getlimits',
                    ],
                },
            },
            'commonCurrencies': {
                'EPC': 'Epacoin',
            },
            'exceptions': {
                'exact': {
                    'ERR_INSUFICIENT_BALANCE': InsufficientFunds,
                    'ERR_LOW_VOLUME': BadRequest,
                },
                'broad': {
                    'Order is not open': InvalidOrder,
                    'Invalid Account / Api KEY / Api Secret': AuthenticationError,  # also happens when an invalid nonce is used
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.25 / 100,
                    'maker': 0.25 / 100,
                },
            },
            'options': {
                'parseOrderStatus': True,
                'symbolSeparator': '_',
            },
        })
        # undocumented api calls
        # https://bleutrade.com/api/v3/public/tradingview/symbols?symbol=ETH_BTC
        # https://bleutrade.com/api/v3/public/tradingview/config
        # https://bleutrade.com/api/v3/public/tradingview/time
        # https://bleutrade.com/api/v3/private/getcloseorders?market=ETH_BTC
        # https://bleutrade.com/config contains the fees

    async def fetch_currencies(self, params={}):
        response = await self.v3PublicGetGetassets(params)
        items = response['result']
        result = {}
        for i in range(0, len(items)):
            #   {Asset: 'USDT',
            #     AssetLong: 'Tether',
            #     MinConfirmation: 4,
            #     WithdrawTxFee: 1,
            #     WithdrawTxFeePercent: 0,
            #     SystemProtocol: 'ETHERC20',
            #     IsActive: True,
            #     InfoMessage: '',
            #     MaintenanceMode: False,
            #     MaintenanceMessage: '',
            #     FormatPrefix: '',
            #     FormatSufix: '',
            #     DecimalSeparator: '.',
            #     ThousandSeparator: ',',
            #     DecimalPlaces: 8,
            #     Currency: 'USDT',
            #     CurrencyLong: 'Tether',
            #     CoinType: 'ETHERC20'}
            item = items[i]
            id = self.safe_string(item, 'Asset')
            code = self.safe_currency_code(id)
            result[code] = {
                'id': id,
                'code': code,
                'name': self.safe_string(item, 'AssetLong'),
                'active': self.safe_value(item, 'IsActive') and not self.safe_value(item, 'MaintenanceMode'),
                'fee': self.safe_float(item, 'WithdrawTxFee'),
                'precision': self.safe_float(item, 'DecimalPlaces'),
                'info': item,
            }
        return result

    async def fetch_markets(self, params={}):
        # https://github.com/ccxt/ccxt/issues/5668
        response = await self.v3PublicGetGetmarkets(params)
        result = []
        markets = self.safe_value(response, 'result')
        for i in range(0, len(markets)):
            market = markets[i]
            #   {MarketName: 'LTC_USDT',
            #     MarketAsset: 'LTC',
            #     BaseAsset: 'USDT',
            #     MarketAssetLong: 'Litecoin',
            #     BaseAssetLong: 'Tether',
            #     IsActive: True,
            #     MinTradeSize: 0.0001,
            #     InfoMessage: '',
            #     MarketCurrency: 'LTC',
            #     BaseCurrency: 'USDT',
            #     MarketCurrencyLong: 'Litecoin',
            #     BaseCurrencyLong: 'Tether'}
            id = self.safe_string(market, 'MarketName')
            baseId = self.safe_string(market, 'MarketCurrency')
            quoteId = self.safe_string(market, 'BaseCurrency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': 8,
            }
            active = self.safe_value(market, 'IsActive', False)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'info': market,
                'precision': precision,
                'maker': self.fees['trading']['maker'],
                'taker': self.fees['trading']['taker'],
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'MinTradeSize'),
                        'max': None,
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': None,
                    },
                },
            })
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'type': 'ALL',
        }
        if limit is not None:
            request['depth'] = limit  # 50
        response = await self.v3PublicGetGetorderbook(self.extend(request, params))
        orderbook = self.safe_value(response, 'result')
        if not orderbook:
            raise ExchangeError(self.id + ' no orderbook data in ' + self.json(response))
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'Rate', 'Quantity')

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.v3PublicGetGetmarketsummary(self.extend(request, params))
        ticker = response['result'][0]
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.v3PublicGetGetmarketsummaries(params)
        result = self.safe_value(response, 'result')
        tickers = []
        for i in range(0, len(result)):
            ticker = self.parse_ticker(result[i])
            tickers.append(ticker)
        return self.filter_by_array(tickers, 'symbol', symbols)

    def parse_ticker(self, ticker, market=None):
        #   {TimeStamp: '2020-01-14 14:32:28',
        #     MarketName: 'LTC_USDT',
        #     MarketAsset: 'LTC',
        #     BaseAsset: 'USDT',
        #     MarketAssetName: 'Litecoin',
        #     BaseAssetName: 'Tether',
        #     PrevDay: 49.2867503,
        #     High: 56.78622664,
        #     Low: 49.27384025,
        #     Last: 53.94,
        #     Average: 51.37509368,
        #     Volume: 1.51282404,
        #     BaseVolume: 77.72147677,
        #     Bid: 53.62070218,
        #     Ask: 53.94,
        #     IsActive: 'true',
        #     InfoMessage: '',
        #     MarketCurrency: 'Litecoin',
        #     BaseCurrency: 'Tether'}
        timestamp = self.parse8601(self.safe_string(ticker, 'TimeStamp'))
        symbol = None
        marketId = self.safe_string(ticker, 'MarketName')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                symbol = self.parse_symbol(marketId)
        if (symbol is None) and (market is not None):
            symbol = market['symbol']
        previous = self.safe_float(ticker, 'PrevDay')
        last = self.safe_float(ticker, 'Last')
        change = None
        percentage = None
        if last is not None:
            if previous is not None:
                change = last - previous
                if previous > 0:
                    percentage = (change / previous) * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'High'),
            'low': self.safe_float(ticker, 'Low'),
            'bid': self.safe_float(ticker, 'Bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'Ask'),
            'askVolume': None,
            'vwap': None,
            'open': previous,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'Volume'),
            'quoteVolume': self.safe_float(ticker, 'BaseVolume'),
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['TimeStamp'] + '+00:00')
        return [
            timestamp,
            self.safe_float(ohlcv, 'Open'),
            self.safe_float(ohlcv, 'High'),
            self.safe_float(ohlcv, 'Low'),
            self.safe_float(ohlcv, 'Close'),
            self.safe_float(ohlcv, 'Volume'),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='15m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'period': self.timeframes[timeframe],
            'market': market['id'],
            'count': limit,
        }
        response = await self.v3PublicGetGetcandles(self.extend(request, params))
        return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            # todo: STOP-LIMIT and AMI order types are supported
            raise InvalidOrder(self.id + ' allows limit orders only')
        await self.load_markets()
        request = {
            'rate': self.price_to_precision(symbol, price),
            'quantity': self.amount_to_precision(symbol, amount),
            'tradeType': '1' if (side == 'buy') else '0',
            'market': self.market_id(symbol),
        }
        response = None
        if side == 'buy':
            response = await self.v3PrivatePostBuylimit(self.extend(request, params))
        else:
            response = await self.v3PrivatePostSelllimit(self.extend(request, params))
        #   {success:  True,
        #     message: "",
        #     result: "161105236"},
        return {
            'info': response,
            'id': self.safe_string(response, 'result'),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'orderid': id,
        }
        response = await self.v3PrivatePostOrdercancel(self.extend(request, params))
        # {success: True, message: '', result: ''}
        return response

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        response = await self.v3PrivatePostGetopenorders(self.extend(request, params))
        items = self.safe_value(response, 'result', [])
        return self.parse_orders(items, market, since, limit)

    def parse_symbol(self, id):
        base, quote = id.split(self.options['symbolSeparator'])
        base = self.safe_currency_code(base)
        quote = self.safe_currency_code(quote)
        return base + '/' + quote

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.v3PrivatePostGetbalances(params)
        result = {'info': response}
        items = response['result']
        for i in range(0, len(items)):
            item = items[i]
            currencyId = self.safe_string(item, 'Asset')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(item, 'Available')
            account['total'] = self.safe_float(item, 'Balance')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        response = await self.v3PrivatePostGetcloseorders(self.extend(request, params))
        orders = self.safe_value(response, 'result', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_transactions_with_method(self, method, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        response = await getattr(self, method)(params)
        transactions = self.safe_value(response, 'result', [])
        return self.parse_transactions(transactions, code, since, limit)

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('v3PrivatePostGetdeposithistory', code, since, limit, params)

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('v3PrivatePostGetwithdrawhistory', code, since, limit, params)

    async def fetch_deposit_address(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'asset': currency['id'],
        }
        response = await self.v3PrivatePostGetdepositaddress(self.extend(request, params))
        #   {success: True,
        #     message: '',
        #     result:
        #     {Asset: 'ETH',
        #         AssetName: 'Ethereum',
        #         DepositAddress: '0x748c5c8jhksjdfhd507d3aa9',
        #         Currency: 'ETH',
        #         CurrencyName: 'Ethereum'}}
        item = response['result']
        address = self.safe_string(item, 'DepositAddress')
        return {
            'currency': code,
            'address': self.check_address(address),
            # 'tag': tag,
            'info': item,
        }

    def parse_ledger_entry_type(self, type):
        # deposits don't seem to appear in here
        types = {
            'TRADE': 'trade',
            'WITHDRAW': 'transaction',
        }
        return self.safe_string(types, type, type)

    def parse_ledger_entry(self, item, currency=None):
        #
        # trade(both sides)
        #
        #     {
        #         ID: 109660527,
        #         TimeStamp: '2018-11-14 15:12:57.140776',
        #         Asset: 'ETH',
        #         AssetName: 'Ethereum',
        #         Amount: 0.01,
        #         Type: 'TRADE',
        #         Description: 'Trade +, order id 133111123',
        #         Comments: '',
        #         CoinSymbol: 'ETH',
        #         CoinName: 'Ethereum'
        #     }
        #
        #     {
        #         ID: 109660526,
        #         TimeStamp: '2018-11-14 15:12:57.140776',
        #         Asset: 'BTC',
        #         AssetName: 'Bitcoin',
        #         Amount: -0.00031776,
        #         Type: 'TRADE',
        #         Description: 'Trade -, order id 133111123, fee -0.00000079',
        #         Comments: '',
        #         CoinSymbol: 'BTC',
        #         CoinName: 'Bitcoin'
        #     }
        #
        # withdrawal
        #
        #     {
        #         ID: 104672316,
        #         TimeStamp: '2018-05-03 08:18:19.031831',
        #         Asset: 'DOGE',
        #         AssetName: 'Dogecoin',
        #         Amount: -61893.87864686,
        #         Type: 'WITHDRAW',
        #         Description: 'Withdraw: 61883.87864686 to address DD8tgehNNyYB2iqVazi2W1paaztgcWXtF6; fee 10.00000000',
        #         Comments: '',
        #         CoinSymbol: 'DOGE',
        #         CoinName: 'Dogecoin'
        #     }
        #
        code = self.safe_currency_code(self.safe_string(item, 'CoinSymbol'), currency)
        description = self.safe_string(item, 'Description')
        type = self.parse_ledger_entry_type(self.safe_string(item, 'Type'))
        referenceId = None
        fee = None
        delimiter = ', ' if (type == 'trade') else '; '
        parts = description.split(delimiter)
        for i in range(0, len(parts)):
            part = parts[i]
            if part.find('fee') == 0:
                part = part.replace('fee ', '')
                feeCost = float(part)
                if feeCost < 0:
                    feeCost = -feeCost
                fee = {
                    'cost': feeCost,
                    'currency': code,
                }
            elif part.find('order id') == 0:
                referenceId = part.replace('order id ', '')
            #
            # does not belong to Ledger, related to parseTransaction
            #
            #     if part.find('Withdraw') == 0:
            #         details = part.split(' to address ')
            #         if len(details) > 1:
            #             address = details[1]
            #     }
            #
        timestamp = self.parse8601(self.safe_string(item, 'TimeStamp'))
        amount = self.safe_float(item, 'Amount')
        direction = None
        if amount is not None:
            direction = 'in'
            if amount < 0:
                direction = 'out'
                amount = -amount
        id = self.safe_string(item, 'ID')
        return {
            'id': id,
            'info': item,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'direction': direction,
            'account': None,
            'referenceId': referenceId,
            'referenceAccount': None,
            'type': type,
            'currency': code,
            'amount': amount,
            'before': None,
            'after': None,
            'status': 'ok',
            'fee': fee,
        }

    async def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        # only seems to return 100 items and there is no documented way to change page size or offset
        request = {
        }
        response = await self.v3PrivatePostGetmytransactions(self.extend(request, params))
        items = response['result']
        return self.parse_ledger(items, code, since, limit)

    def parse_order(self, order, market=None):
        #
        # fetchClosedOrders
        #
        #   {OrderID: 89742658,
        #     Exchange: 'DOGE_BTC',
        #     Type: 'BUY',
        #     Quantity: 10000,
        #     QuantityRemaining: 0,
        #     QuantityBaseTraded: 0,
        #     Price: 6.6e-7,
        #     Status: 'OK',
        #     Created: '2018-02-16 08:55:36',
        #     Comments: ''}
        #
        #  fetchOpenOrders
        #
        #   {OrderID: 161105302,
        #     Exchange: 'ETH_BTC',
        #     Type: 'SELL',
        #     Quantity: 0.4,
        #     QuantityRemaining: 0.4,
        #     QuantityBaseTraded: 0,
        #     Price: 0.04,
        #     Status: 'OPEN',
        #     Created: '2020-01-22 09:21:27',
        #     Comments: {String: '', Valid: True}
        side = self.safe_string(order, 'Type').lower()
        status = self.parse_order_status(self.safe_string(order, 'Status'))
        symbol = None
        marketId = self.safe_string(order, 'Exchange')
        if marketId is None:
            if market is not None:
                symbol = market['symbol']
        else:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
                symbol = market['symbol']
            else:
                symbol = self.parse_symbol(marketId)
        timestamp = None
        if 'Created' in order:
            timestamp = self.parse8601(order['Created'] + '+00:00')
        price = self.safe_float(order, 'Price')
        cost = None
        amount = self.safe_float(order, 'Quantity')
        remaining = self.safe_float(order, 'QuantityRemaining')
        filled = None
        if amount is not None and remaining is not None:
            filled = amount - remaining
        if not cost:
            if price and filled:
                cost = price * filled
        if not price:
            if cost and filled:
                price = cost / filled
        average = self.safe_float(order, 'PricePerUnit')
        id = self.safe_string(order, 'OrderID')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': None,
        }

    def parse_order_status(self, status):
        statuses = {
            'OK': 'closed',
            'OPEN': 'open',
            'CANCELED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        #  deposit:
        #
        #   {ID: 118698752,
        #     Timestamp: '2020-01-21 11:16:09',
        #     Asset: 'ETH',
        #     Amount: 1,
        #     TransactionID: '',
        #     Status: 'CONFIRMED',
        #     Label: '0x748c5c8228d0c596f4d07f338blah',
        #     Symbol: 'ETH'}
        #
        # withdrawal:
        #
        #   {ID: 689281,
        #     Timestamp: '2019-07-05 13:14:43',
        #     Asset: 'BTC',
        #     Amount: -0.108959,
        #     TransactionID: 'da48d6901fslfjsdjflsdjfls852b87e362cad1',
        #     Status: 'CONFIRMED',
        #     Label: '0.1089590;35wztHPMgrebFvvblah;0.00100000',
        #     Symbol: 'BTC'}
        #
        id = self.safe_string(transaction, 'ID')
        amount = self.safe_float(transaction, 'Amount')
        type = 'deposit'
        if amount < 0:
            amount = abs(amount)
            type = 'withdrawal'
        currencyId = self.safe_string(transaction, 'Asset')
        code = self.safe_currency_code(currencyId, currency)
        label = self.safe_string(transaction, 'Label')
        timestamp = self.parse8601(self.safe_string(transaction, 'Timestamp'))
        txid = self.safe_string(transaction, 'TransactionID')
        address = None
        feeCost = None
        labelParts = label.split(';')
        if len(labelParts) == 3:
            amount = float(labelParts[0])
            address = labelParts[1]
            feeCost = float(labelParts[2])
        else:
            address = label
        fee = None
        if feeCost is not None:
            fee = {
                'currency': code,
                'cost': feeCost,
            }
        status = 'ok'
        if txid == 'CANCELED':
            txid = None
            status = 'canceled'
        return {
            'info': transaction,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'id': id,
            'currency': code,
            'amount': amount,
            'address': address,
            'tag': None,
            'status': status,
            'type': type,
            'updated': None,
            'txid': txid,
            'fee': fee,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.implode_params(self.urls['api'][api], {
            'hostname': self.hostname,
        }) + '/'
        if api == 'v3Private':
            self.check_required_credentials()
            request = {
                'apikey': self.apiKey,
                'nonce': self.nonce(),
            }
            url += path + '?' + self.urlencode(self.extend(request, params))
            signature = self.hmac(self.encode(url), self.encode(self.secret), hashlib.sha512)
            headers = {'apisign': signature}
        else:
            url += path + '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return  # fallback to default error handler
        #    examples...
        #    {"success":false,"message":"Erro: Order is not open.","result":""} <-- 'error' is spelt wrong
        #    {"success":false,"message":"Error: Very low volume.","result":"ERR_LOW_VOLUME"}
        #    {"success":false,"message":"Error: Insuficient Balance","result":"ERR_INSUFICIENT_BALANCE"}
        #
        if body[0] == '{':
            success = self.safe_value(response, 'success')
            if success is None:
                raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
            if not success:
                feedback = self.id + ' ' + body
                errorCode = self.safe_string(response, 'result')
                self.throw_broadly_matched_exception(self.exceptions['broad'], errorCode, feedback)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
                errorMessage = self.safe_string(response, 'message')
                self.throw_broadly_matched_exception(self.exceptions['broad'], errorMessage, feedback)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorMessage, feedback)
                raise ExchangeError(feedback)
