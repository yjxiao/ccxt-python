# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired


class therock (Exchange):

    def describe(self):
        return self.deep_extend(super(therock, self).describe(), {
            'id': 'therock',
            'name': 'TheRockTrading',
            'countries': ['MT'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchMyTrades': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766869-75057fa2-5ee9-11e7-9a6f-13e641fa4707.jpg',
                'api': 'https://api.therocktrading.com',
                'www': 'https://therocktrading.com',
                'doc': [
                    'https://api.therocktrading.com/doc/v1/index.html',
                    'https://api.therocktrading.com/doc/',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'funds',
                        'funds/{id}/orderbook',
                        'funds/{id}/ticker',
                        'funds/{id}/trades',
                        'funds/tickers',
                    ],
                },
                'private': {
                    'get': [
                        'balances',
                        'balances/{id}',
                        'discounts',
                        'discounts/{id}',
                        'funds',
                        'funds/{id}',
                        'funds/{id}/trades',
                        'funds/{fund_id}/orders',
                        'funds/{fund_id}/orders/{id}',
                        'funds/{fund_id}/position_balances',
                        'funds/{fund_id}/positions',
                        'funds/{fund_id}/positions/{id}',
                        'transactions',
                        'transactions/{id}',
                        'withdraw_limits/{id}',
                        'withdraw_limits',
                    ],
                    'post': [
                        'atms/withdraw',
                        'funds/{fund_id}/orders',
                    ],
                    'delete': [
                        'funds/{fund_id}/orders/{id}',
                        'funds/{fund_id}/orders/remove_all',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.0005,
                        'BCH': 0.0005,
                        'PPC': 0.02,
                        'ETH': 0.001,
                        'ZEC': 0.001,
                        'LTC': 0.002,
                        'EUR': 2.5,  # worst-case scenario: https://therocktrading.com/en/pages/fees
                    },
                    'deposit': {
                        'BTC': 0,
                        'BCH': 0,
                        'PPC': 0,
                        'ETH': 0,
                        'ZEC': 0,
                        'LTC': 0,
                        'EUR': 0,
                    },
                },
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetFunds()
        #
        #     {funds: [{                     id:   "BTCEUR",
        #                              description:   "Trade Bitcoin with Euro",
        #                                     type:   "currency",
        #                            base_currency:   "EUR",
        #                           trade_currency:   "BTC",
        #                                  buy_fee:    0.2,
        #                                 sell_fee:    0.2,
        #                      minimum_price_offer:    0.01,
        #                   minimum_quantity_offer:    0.0005,
        #                   base_currency_decimals:    2,
        #                  trade_currency_decimals:    4,
        #                                leverages: []                           },
        #                {                     id:   "LTCEUR",
        #                              description:   "Trade Litecoin with Euro",
        #                                     type:   "currency",
        #                            base_currency:   "EUR",
        #                           trade_currency:   "LTC",
        #                                  buy_fee:    0.2,
        #                                 sell_fee:    0.2,
        #                      minimum_price_offer:    0.01,
        #                   minimum_quantity_offer:    0.01,
        #                   base_currency_decimals:    2,
        #                  trade_currency_decimals:    2,
        #                                leverages: []                            }]}
        #
        markets = self.safe_value(response, 'funds')
        result = []
        if markets is None:
            raise ExchangeError(self.id + ' fetchMarkets got an unexpected response')
        else:
            for i in range(0, len(markets)):
                market = markets[i]
                id = self.safe_string(market, 'id')
                baseId = self.safe_string(market, 'trade_currency')
                quoteId = self.safe_string(market, 'base_currency')
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
                buy_fee = self.safe_float(market, 'buy_fee')
                sell_fee = self.safe_float(market, 'sell_fee')
                taker = max(buy_fee, sell_fee)
                taker = taker / 100
                maker = taker
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'info': market,
                    'active': True,
                    'maker': maker,
                    'taker': taker,
                    'precision': {
                        'amount': self.safe_integer(market, 'trade_currency_decimals'),
                        'price': self.safe_integer(market, 'base_currency_decimals'),
                    },
                    'limits': {
                        'amount': {
                            'min': self.safe_float(market, 'minimum_quantity_offer'),
                            'max': None,
                        },
                        'price': {
                            'min': self.safe_float(market, 'minimum_price_offer'),
                            'max': None,
                        },
                        'cost': {
                            'min': None,
                            'max': None,
                        },
                    },
                })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalances()
        balances = response['balances']
        result = {'info': response}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            free = balance['trading_balance']
            total = balance['balance']
            used = total - free
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetFundsIdOrderbook(self.extend({
            'id': self.market_id(symbol),
        }, params))
        timestamp = self.parse8601(orderbook['date'])
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'amount')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.parse8601(ticker['date'])
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(ticker, 'close'),  # previous day close, if any
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume_traded'),
            'quoteVolume': self.safe_float(ticker, 'volume'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetFundsTickers(params)
        tickers = self.index_by(response['tickers'], 'fund_id')
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetFundsIdTicker(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades
        #
        #     {     id:  4493548,
        #       fund_id: "ETHBTC",
        #        amount:  0.203,
        #         price:  0.02783576,
        #          side: "buy",
        #          dark:  False,
        #          date: "2018-11-30T08:19:18.236Z"}
        #
        # fetchMyTrades
        #
        #     {          id:    237338,
        #            fund_id:   "BTCEUR",
        #             amount:    0.348,
        #              price:    348,
        #               side:   "sell",
        #               dark:    False,
        #           order_id:    14920648,
        #               date:   "2015-06-03T00:49:49.000Z",
        #       transactions: [{      id:  2770768,
        #                             date: "2015-06-03T00:49:49.000Z",
        #                             type: "sold_currency_to_fund",
        #                            price:  121.1,
        #                         currency: "EUR"                       },
        #                       {      id:  2770769,
        #                             date: "2015-06-03T00:49:49.000Z",
        #                             type: "released_currency_to_fund",
        #                            price:  0.348,
        #                         currency: "BTC"                        },
        #                       {      id:  2770772,
        #                             date: "2015-06-03T00:49:49.000Z",
        #                             type: "paid_commission",
        #                            price:  0.06,
        #                         currency: "EUR",
        #                         trade_id:  440492                     }   ]}
        #
        if not market:
            market = self.markets_by_id[trade['fund_id']]
        timestamp = self.parse8601(self.safe_string(trade, 'date'))
        id = self.safe_string(trade, 'id')
        orderId = self.safe_string(trade, 'order_id')
        side = self.safe_string(trade, 'side')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        fee = None
        feeCost = None
        transactions = self.safe_value(trade, 'transactions', [])
        transactionsByType = self.group_by(transactions, 'type')
        feeTransactions = self.safe_value(transactionsByType, 'paid_commission', [])
        for i in range(0, len(feeTransactions)):
            if feeCost is None:
                feeCost = 0
            feeCost = self.sum(feeCost, self.safe_float(feeTransactions[i], 'price'))
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': market['quote'],
            }
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        if limit is not None:
            request['per_page'] = limit  # default 25 max 200
        if since is not None:
            request['after'] = self.iso8601(since)
        response = self.privateGetFundsIdTrades(self.extend(request, params))
        #
        #     {trades: [{          id:    237338,
        #                        fund_id:   "BTCEUR",
        #                         amount:    0.348,
        #                          price:    348,
        #                           side:   "sell",
        #                           dark:    False,
        #                       order_id:    14920648,
        #                           date:   "2015-06-03T00:49:49.000Z",
        #                   transactions: [{      id:  2770768,
        #                                         date: "2015-06-03T00:49:49.000Z",
        #                                         type: "sold_currency_to_fund",
        #                                        price:  121.1,
        #                                     currency: "EUR"                       },
        #                                   {      id:  2770769,
        #                                         date: "2015-06-03T00:49:49.000Z",
        #                                         type: "released_currency_to_fund",
        #                                        price:  0.348,
        #                                     currency: "BTC"                        },
        #                                   {      id:  2770772,
        #                                         date: "2015-06-03T00:49:49.000Z",
        #                                         type: "paid_commission",
        #                                        price:  0.06,
        #                                     currency: "EUR",
        #                                     trade_id:  440492                     }   ]}],
        #         meta: {total_count:    31,
        #                       first: {href: "https://api.therocktrading.com/v1/funds/BTCXRP/trades?page=1"},
        #                    previous:    null,
        #                     current: {href: "https://api.therocktrading.com/v1/funds/BTCXRP/trades?page=1"},
        #                        next: {href: "https://api.therocktrading.com/v1/funds/BTCXRP/trades?page=2"},
        #                        last: {href: "https://api.therocktrading.com/v1/funds/BTCXRP/trades?page=2"}  }}
        #
        return self.parse_trades(response['trades'], market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        if limit is not None:
            request['per_page'] = limit  # default 25 max 200
        if since is not None:
            request['after'] = self.iso8601(since)
        response = self.publicGetFundsIdTrades(self.extend(request, params))
        #
        #     {trades: [{     id:  4493548,
        #                   fund_id: "ETHBTC",
        #                    amount:  0.203,
        #                     price:  0.02783576,
        #                      side: "buy",
        #                      dark:  False,
        #                      date: "2018-11-30T08:19:18.236Z"},
        #                 {     id:  4492926,
        #                   fund_id: "ETHBTC",
        #                    amount:  0.04,
        #                     price:  0.02767034,
        #                      side: "buy",
        #                      dark:  False,
        #                      date: "2018-11-30T07:03:03.897Z"}  ],
        #         meta: {total_count:    null,
        #                       first: {page:  1,
        #                                href: "https://api.therocktrading.com/v1/funds/ETHBTC/trades?page=1"},
        #                    previous:    null,
        #                     current: {page:  1,
        #                                href: "https://api.therocktrading.com/v1/funds/ETHBTC/trades?page=1"},
        #                        next: {page:  2,
        #                                href: "https://api.therocktrading.com/v1/funds/ETHBTC/trades?page=2"},
        #                        last:    null                                                                   }}
        #
        return self.parse_trades(response['trades'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if type == 'market':
            price = 0
        response = self.privatePostFundsFundIdOrders(self.extend({
            'fund_id': self.market_id(symbol),
            'side': side,
            'amount': amount,
            'price': price,
        }, params))
        return {
            'info': response,
            'id': str(response['id']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privateDeleteFundsFundIdOrdersId(self.extend({
            'id': id,
            'fund_id': self.market_id(symbol),
        }, params))

    def parse_order_status(self, status):
        statuses = {
            'active': 'open',
            'executed': 'closed',
            'deleted': 'canceled',
            # don't know what self status means
            # 'conditional': '?',
        }
        return self.safe_string(statuses, status, status)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + url
            headers = {
                'X-TRT-KEY': self.apiKey,
                'X-TRT-NONCE': nonce,
                'X-TRT-SIGN': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512),
            }
            if query:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'
        elif api == 'public':
            if query:
                url += '?' + self.rawencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'errors' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
