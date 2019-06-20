# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.bittrex import bittrex
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder


class bleutrade (bittrex):

    def describe(self):
        timeframes = {
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
        }
        result = self.deep_extend(super(bleutrade, self).describe(), {
            'id': 'bleutrade',
            'name': 'Bleutrade',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'version': 'v2',
            'certified': False,
            'has': {
                'CORS': True,
                'fetchTickers': True,
                'fetchOrders': True,
                'fetchClosedOrders': True,
                'fetchOrderTrades': True,
            },
            'timeframes': timeframes,
            'hostname': 'bleutrade.com',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30303000-b602dbe6-976d-11e7-956d-36c5049c01e7.jpg',
                'api': {
                    'public': 'https://{hostname}/api',
                    'account': 'https://{hostname}/api',
                    'market': 'https://{hostname}/api',
                },
                'www': 'https://bleutrade.com',
                'doc': 'https://bleutrade.com/help/API',
                'fees': 'https://bleutrade.com/help/fees_and_deadlines',
            },
            'api': {
                'account': {
                    'get': [
                        'balance',
                        'balances',
                        'depositaddress',
                        'deposithistory',
                        'order',
                        'orders',
                        'orderhistory',
                        'withdrawhistory',
                        'withdraw',
                    ],
                },
                'public': {
                    'get': [
                        'candles',
                        'currencies',
                        'markethistory',
                        'markets',
                        'marketsummaries',
                        'marketsummary',
                        'orderbook',
                        'ticker',
                    ],
                },
            },
            'fees': {
                'funding': {
                    'withdraw': {
                        'ADC': 0.1,
                        'BTA': 0.1,
                        'BITB': 0.1,
                        'BTC': 0.001,
                        'BCC': 0.001,
                        'BTCD': 0.001,
                        'BTG': 0.001,
                        'BLK': 0.1,
                        'CDN': 0.1,
                        'CLAM': 0.01,
                        'DASH': 0.001,
                        'DCR': 0.05,
                        'DGC': 0.1,
                        'DP': 0.1,
                        'DPC': 0.1,
                        'DOGE': 10.0,
                        'EFL': 0.1,
                        'ETH': 0.01,
                        'EXP': 0.1,
                        'FJC': 0.1,
                        'BSTY': 0.001,
                        'GB': 0.1,
                        'NLG': 0.1,
                        'HTML': 1.0,
                        'LTC': 0.001,
                        'MONA': 0.01,
                        'MOON': 1.0,
                        'NMC': 0.015,
                        'NEOS': 0.1,
                        'NVC': 0.05,
                        'OK': 0.1,
                        'PPC': 0.1,
                        'POT': 0.1,
                        'XPM': 0.001,
                        'QTUM': 0.1,
                        'RDD': 0.1,
                        'SLR': 0.1,
                        'START': 0.1,
                        'SLG': 0.1,
                        'TROLL': 0.1,
                        'UNO': 0.01,
                        'VRC': 0.1,
                        'VTC': 0.1,
                        'XVP': 0.1,
                        'WDC': 0.001,
                        'ZET': 0.1,
                    },
                },
            },
            'commonCurrencies': {
                'EPC': 'Epacoin',
            },
            'exceptions': {
                'Insufficient fundsnot ': InsufficientFunds,
                'Invalid Order ID': InvalidOrder,
                'Invalid apikey or apisecret': AuthenticationError,
            },
            'options': {
                'parseOrderStatus': True,
                'disableNonce': False,
                'symbolSeparator': '_',
            },
        })
        # bittrex inheritance override
        result['timeframes'] = timeframes
        return result

    def parse_order_status(self, status):
        statuses = {
            'OK': 'closed',
            'OPEN': 'open',
            'CANCELED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        # Possible params
        # orderstatus(ALL, OK, OPEN, CANCELED)
        # ordertype(ALL, BUY, SELL)
        # depth(optional, default is 500, max is 20000)
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        else:
            market = None
        request = {
            'market': 'ALL',
            'orderstatus': 'ALL',
        }
        response = self.accountGetOrders(self.extend(request, params))
        return self.parse_orders(response['result'], market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        response = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(response, 'status', 'closed')

    def get_order_id_field(self):
        return 'orderid'

    def parse_symbol(self, id):
        base, quote = id.split(self.options['symbolSeparator'])
        base = self.common_currency_code(base)
        quote = self.common_currency_code(quote)
        return base + '/' + quote

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'market': self.market_id(symbol),
            'type': 'ALL',
        }
        if limit is not None:
            request['depth'] = limit  # 50
        response = self.publicGetOrderbook(self.extend(request, params))
        orderbook = self.safe_value(response, 'result')
        if not orderbook:
            raise ExchangeError(self.id + ' publicGetOrderbook() returneded no result ' + self.json(response))
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'Rate', 'Quantity')

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        # Currently we can't set the makerOrTaker field, but if the user knows the order side then it can be
        # determined(if the side of the trade is different to the side of the order, then the trade is maker).
        # Similarly, the correct 'side' for the trade is that of the order.
        # The trade fee can be set by the user, it is always 0.25% and is taken in the quote currency.
        self.load_markets()
        request = {
            'orderid': id,
        }
        response = self.accountGetOrderhistory(self.extend(request, params))
        return self.parse_trades(response['result'], None, since, limit, {
            'order': id,
        })

    def fetch_transactions_by_type(self, type, code=None, since=None, limit=None, params={}):
        self.load_markets()
        method = 'accountGetDeposithistory' if (type == 'deposit') else 'accountGetWithdrawhistory'
        response = getattr(self, method)(params)
        result = self.parseTransactions(response['result'])
        return self.filterByCurrencySinceLimit(result, code, since, limit)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('deposit', code, since, limit, params)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return self.fetch_transactions_by_type('withdrawal', code, since, limit, params)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['TimeStamp'] + '+00:00')
        return [
            timestamp,
            ohlcv['Open'],
            ohlcv['High'],
            ohlcv['Low'],
            ohlcv['Close'],
            ohlcv['Volume'],
        ]

    def fetch_ohlcv(self, symbol, timeframe='15m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'period': self.timeframes[timeframe],
            'market': market['id'],
            'count': limit,
        }
        response = self.publicGetCandles(self.extend(request, params))
        if 'result' in response:
            if response['result']:
                return self.parse_ohlcvs(response['result'], market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['TimeStamp'] + '+00:00')
        side = None
        if trade['OrderType'] == 'BUY':
            side = 'buy'
        elif trade['OrderType'] == 'SELL':
            side = 'sell'
        id = self.safe_string(trade, 'TradeID')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        cost = None
        price = self.safe_float(trade, 'Price')
        amount = self.safe_float(trade, 'Quantity')
        if amount is not None:
            if price is not None:
                cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def parse_order(self, order, market=None):
        side = self.safe_string_2(order, 'OrderType', 'Type')
        isBuyOrder = (side == 'LIMIT_BUY') or (side == 'BUY')
        isSellOrder = (side == 'LIMIT_SELL') or (side == 'SELL')
        if isBuyOrder:
            side = 'buy'
        if isSellOrder:
            side = 'sell'
        # We parse different fields in a very specific order.
        # Order might well be closed and then canceled.
        status = None
        if ('Opened' in list(order.keys())) and order['Opened']:
            status = 'open'
        if ('Closed' in list(order.keys())) and order['Closed']:
            status = 'closed'
        if ('CancelInitiated' in list(order.keys())) and order['CancelInitiated']:
            status = 'canceled'
        if ('Status' in list(order.keys())) and self.options['parseOrderStatus']:
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
        if 'Opened' in order:
            timestamp = self.parse8601(order['Opened'] + '+00:00')
        if 'Created' in order:
            timestamp = self.parse8601(order['Created'] + '+00:00')
        lastTradeTimestamp = None
        if ('TimeStamp' in list(order.keys())) and(order['TimeStamp'] is not None):
            lastTradeTimestamp = self.parse8601(order['TimeStamp'] + '+00:00')
        if ('Closed' in list(order.keys())) and(order['Closed'] is not None):
            lastTradeTimestamp = self.parse8601(order['Closed'] + '+00:00')
        if timestamp is None:
            timestamp = lastTradeTimestamp
        fee = None
        commission = None
        if 'Commission' in order:
            commission = 'Commission'
        elif 'CommissionPaid' in order:
            commission = 'CommissionPaid'
        if commission:
            fee = {
                'cost': self.safe_float(order, commission),
            }
            if market is not None:
                fee['currency'] = market['quote']
            elif symbol is not None:
                currencyIds = symbol.split('/')
                quoteCurrencyId = currencyIds[1]
                if quoteCurrencyId in self.currencies_by_id:
                    fee['currency'] = self.currencies_by_id[quoteCurrencyId]['code']
                else:
                    fee['currency'] = self.common_currency_code(quoteCurrencyId)
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
        id = self.safe_string_2(order, 'OrderUuid', 'OrderId')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
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
            'fee': fee,
        }

    def parse_transaction(self, transaction, currency=None):
        #
        #  deposit:
        #
        #     {
        #         Id: '96974373',
        #         Coin: 'DOGE',
        #         Amount: '12.05752192',
        #         TimeStamp: '2017-09-29 08:10:09',
        #         Label: 'DQqSjjhzCm3ozT4vAevMUHgv4vsi9LBkoE',
        #     }
        #
        # withdrawal:
        #
        #     {
        #         Id: '98009125',
        #         Coin: 'DOGE',
        #         Amount: '-483858.64312050',
        #         TimeStamp: '2017-11-22 22:29:05',
        #         Label: '483848.64312050DJVJZ58tJC8UeUv9Tqcdtn6uhWobouxFLT10.00000000',
        #         TransactionId: '8563105276cf798385fee7e5a563c620fea639ab132b089ea880d4d1f4309432',
        #     }
        #
        #     {
        #         "Id": "95820181",
        #         "Coin": "BTC",
        #         "Amount": "-0.71300000",
        #         "TimeStamp": "2017-07-19 17:14:24",
        #         "Label": "0.71200000PER9VM2txt4BTdfyWgvv3GziECRdVEPN630.00100000",
        #         "TransactionId": "CANCELED"
        #     }
        #
        id = self.safe_string(transaction, 'Id')
        amount = self.safe_float(transaction, 'Amount')
        type = 'deposit'
        if amount < 0:
            amount = abs(amount)
            type = 'withdrawal'
        currencyId = self.safe_string(transaction, 'Coin')
        code = None
        currency = self.safe_value(self.currencies_by_id, currencyId)
        if currency is not None:
            code = currency['code']
        else:
            code = self.common_currency_code(currencyId)
        label = self.safe_string(transaction, 'Label')
        timestamp = self.parse8601(self.safe_string(transaction, 'TimeStamp'))
        txid = self.safe_string(transaction, 'TransactionId')
        address = None
        feeCost = None
        labelParts = label.split('')
        if len(labelParts) == 3:
            amount = labelParts[0]
            address = labelParts[1]
            feeCost = labelParts[2]
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
