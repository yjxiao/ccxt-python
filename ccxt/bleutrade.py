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
        return self.deep_extend(super(bleutrade, self).describe(), {
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
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30303000-b602dbe6-976d-11e7-956d-36c5049c01e7.jpg',
                'api': {
                    'public': 'https://bleutrade.com/api',
                    'account': 'https://bleutrade.com/api',
                    'market': 'https://bleutrade.com/api',
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

    def fetch_markets(self):
        markets = self.publicGetMarkets()
        result = []
        for p in range(0, len(markets['result'])):
            market = markets['result'][p]
            id = market['MarketName']
            baseId = market['MarketCurrency']
            quoteId = market['BaseCurrency']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': 8,
            }
            active = self.safe_string(market, 'IsActive')
            if active == 'true':
                active = True
            elif active == 'false':
                active = False
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
                'limits': {
                    'amount': {
                        'min': market['MinTradeSize'],
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
            })
        return result

    def parse_order_status(self, status):
        statuses = {
            'OK': 'closed',
            'OPEN': 'open',
            'CANCELED': 'canceled',
        }
        if status in statuses:
            return statuses[status]
        else:
            return status

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        # Possible params
        # orderstatus(ALL, OK, OPEN, CANCELED)
        # ordertype(ALL, BUY, SELL)
        # depth(optional, default is 500, max is 20000)
        self.load_markets()
        market = None
        if symbol is not None:
            self.load_markets()
            market = self.market(symbol)
        else:
            market = None
        response = self.accountGetOrders(self.extend({'market': 'ALL', 'orderstatus': 'ALL'}, params))
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
        response = self.accountGetOrderhistory({'orderid': id})
        trades = self.parse_trades(response['result'], None, since, limit)
        result = []
        for i in range(0, len(trades)):
            trade = self.extend(trades[i], {
                'order': id,
            })
            result.append(trade)
        return result

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
