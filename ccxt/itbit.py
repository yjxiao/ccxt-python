# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired


class itbit(Exchange):

    def describe(self):
        return self.deep_extend(super(itbit, self).describe(), {
            'id': 'itbit',
            'name': 'itBit',
            'countries': ['US'],
            'rateLimit': 2000,
            'version': 'v1',
            'has': {
                'cancelOrder': True,
                'CORS': True,
                'createMarketOrder': False,
                'createOrder': True,
                'fetchBalance': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrders': True,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTransactions': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27822159-66153620-60ad-11e7-89e7-005f6d7f3de0.jpg',
                'api': 'https://api.itbit.com',
                'www': 'https://www.itbit.com',
                'doc': [
                    'https://api.itbit.com/docs',
                    'https://www.itbit.com/api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'markets/{symbol}/ticker',
                        'markets/{symbol}/order_book',
                        'markets/{symbol}/trades',
                    ],
                },
                'private': {
                    'get': [
                        'wallets',
                        'wallets/{walletId}',
                        'wallets/{walletId}/balances/{currencyCode}',
                        'wallets/{walletId}/funding_history',
                        'wallets/{walletId}/trades',
                        'wallets/{walletId}/orders',
                        'wallets/{walletId}/orders/{id}',
                    ],
                    'post': [
                        'wallet_transfers',
                        'wallets',
                        'wallets/{walletId}/cryptocurrency_deposits',
                        'wallets/{walletId}/cryptocurrency_withdrawals',
                        'wallets/{walletId}/orders',
                        'wire_withdrawal',
                    ],
                    'delete': [
                        'wallets/{walletId}/orders/{id}',
                    ],
                },
            },
            'markets': {
                'BTC/USD': {'id': 'XBTUSD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'XBT', 'quoteId': 'USD'},
                'BTC/SGD': {'id': 'XBTSGD', 'symbol': 'BTC/SGD', 'base': 'BTC', 'quote': 'SGD', 'baseId': 'XBT', 'quoteId': 'SGD'},
                'BTC/EUR': {'id': 'XBTEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'XBT', 'quoteId': 'EUR'},
                'ETH/USD': {'id': 'ETHUSD', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD', 'baseId': 'ETH', 'quoteId': 'USD'},
                'ETH/EUR': {'id': 'ETHEUR', 'symbol': 'ETH/EUR', 'base': 'ETH', 'quote': 'EUR', 'baseId': 'ETH', 'quoteId': 'EUR'},
                'ETH/SGD': {'id': 'ETHSGD', 'symbol': 'ETH/SGD', 'base': 'ETH', 'quote': 'SGD', 'baseId': 'ETH', 'quoteId': 'SGD'},
                'PAXGUSD': {'id': 'PAXGUSD', 'symbol': 'PAXG/USD', 'base': 'PAXG', 'quote': 'USD', 'baseId': 'PAXG', 'quoteId': 'USD'},
                'BCHUSD': {'id': 'BCHUSD', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD', 'baseId': 'BCH', 'quoteId': 'USD'},
                'LTCUSD': {'id': 'LTCUSD', 'symbol': 'LTC/USD', 'base': 'LTC', 'quote': 'USD', 'baseId': 'LTC', 'quoteId': 'USD'},
            },
            'fees': {
                'trading': {
                    'maker': -0.03 / 100,
                    'taker': 0.35 / 100,
                },
            },
            'commonCurrencies': {
                'XBT': 'BTC',
            },
        })

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        orderbook = self.publicGetMarketsSymbolOrderBook(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        ticker = self.publicGetMarketsSymbolTicker(self.extend(request, params))
        serverTimeUTC = self.safe_string(ticker, 'serverTimeUTC')
        if not serverTimeUTC:
            raise ExchangeError(self.id + ' fetchTicker returned a bad response: ' + self.json(ticker))
        timestamp = self.parse8601(serverTimeUTC)
        vwap = self.safe_float(ticker, 'vwap24h')
        baseVolume = self.safe_float(ticker, 'volume24h')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24h'),
            'low': self.safe_float(ticker, 'low24h'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_float(ticker, 'openToday'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         timestamp: "2015-05-22T17:45:34.7570000Z",
        #         matchNumber: "5CR1JEUBBM8J",
        #         price: "351.45000000",
        #         amount: "0.00010000"
        #     }
        #
        # fetchMyTrades(private)
        #
        #     {
        #         "orderId": "248ffda4-83a0-4033-a5bb-8929d523f59f",
        #         "timestamp": "2015-05-11T14:48:01.9870000Z",
        #         "instrument": "XBTUSD",
        #         "direction": "buy",                      # buy or sell
        #         "currency1": "XBT",                      # base currency
        #         "currency1Amount": "0.00010000",         # order amount in base currency
        #         "currency2": "USD",                      # quote currency
        #         "currency2Amount": "0.0250530000000000",  # order cost in quote currency
        #         "rate": "250.53000000",
        #         "commissionPaid": "0.00000000",   # net trade fee paid after using any available rebate balance
        #         "commissionCurrency": "USD",
        #         "rebatesApplied": "-0.000125265",  # negative values represent amount of rebate balance used for trades removing liquidity from order book; positive values represent amount of rebate balance earned from trades adding liquidity to order book
        #         "rebateCurrency": "USD",
        #         "executionId": "23132"
        #     }
        #
        id = self.safe_string_2(trade, 'executionId', 'matchNumber')
        timestamp = self.parse8601(self.safe_string(trade, 'timestamp'))
        side = self.safe_string(trade, 'direction')
        orderId = self.safe_string(trade, 'orderId')
        feeCost = self.safe_float(trade, 'commissionPaid')
        feeCurrencyId = self.safe_string(trade, 'commissionCurrency')
        feeCurrency = self.safe_currency_code(feeCurrencyId)
        rebatesApplied = self.safe_float(trade, 'rebatesApplied')
        if rebatesApplied is not None:
            rebatesApplied = -rebatesApplied
        rebateCurrencyId = self.safe_string(trade, 'rebateCurrency')
        rebateCurrency = self.safe_currency_code(rebateCurrencyId)
        price = self.safe_float_2(trade, 'price', 'rate')
        amount = self.safe_float_2(trade, 'currency1Amount', 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        marketId = self.safe_string(trade, 'instrument')
        if marketId is not None:
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId = self.safe_string(trade, 'currency1')
                quoteId = self.safe_string(trade, 'currency2')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
        if symbol is None:
            if market is not None:
                symbol = market['symbol']
        result = {
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
            'cost': cost,
            'fee': None,
        }
        if feeCost is not None:
            if rebatesApplied is not None:
                if feeCurrency == rebateCurrency:
                    feeCost = self.sum(feeCost, rebatesApplied)
                    result['fee'] = {
                        'cost': feeCost,
                        'currency': feeCurrency,
                    }
                else:
                    result['fees'] = [
                        {
                            'cost': feeCost,
                            'currency': feeCurrency,
                        },
                        {
                            'cost': rebatesApplied,
                            'currency': rebateCurrency,
                        },
                    ]
            else:
                result['fee'] = {
                    'cost': feeCost,
                    'currency': feeCurrency,
                }
        if not ('fee' in result):
            if not ('fees' in result):
                result['fee'] = None
        return result

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        walletId = self.safe_string(params, 'walletId')
        if walletId is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a walletId parameter')
        request = {
            'walletId': walletId,
        }
        if limit is not None:
            request['perPage'] = limit  # default 50, max 50
        response = self.privateGetWalletsWalletIdFundingHistory(self.extend(request, params))
        #     {bankName: 'USBC(usd)',
        #         withdrawalId: 94740,
        #         holdingPeriodCompletionDate: '2018-04-16T07:57:05.9606869',
        #         time: '2018-04-16T07:57:05.9600000',
        #         currency: 'USD',
        #         transactionType: 'Withdrawal',
        #         amount: '2186.72000000',
        #         walletName: 'Wallet',
        #         status: 'completed'},
        #
        #     {"time": "2018-01-02T19:52:22.4176503",
        #     "amount": "0.50000000",
        #     "status": "completed",
        #     "txnHash": "1b6fff67ed83cb9e9a38ca4976981fc047322bc088430508fe764a127d3ace95",
        #     "currency": "XBT",
        #     "walletName": "Wallet",
        #     "transactionType": "Deposit",
        #     "destinationAddress": "3AAWTH9et4e8o51YKp9qPpmujrNXKwHWNX"}
        items = response['fundingHistory']
        result = []
        for i in range(0, len(items)):
            item = items[i]
            time = self.safe_string(item, 'time')
            timestamp = self.parse8601(time)
            currency = self.safe_string(item, 'currency')
            destinationAddress = self.safe_string(item, 'destinationAddress')
            txnHash = self.safe_string(item, 'txnHash')
            transactionType = self.safe_string_lower(item, 'transactionType')
            transactionStatus = self.safe_string(item, 'status')
            status = self.parse_transfer_status(transactionStatus)
            result.append({
                'id': self.safe_string(item, 'withdrawalId'),
                'timestamp': timestamp,
                'datetime': self.iso8601(timestamp),
                'currency': self.safe_currency_code(currency),
                'address': destinationAddress,
                'tag': None,
                'txid': txnHash,
                'type': transactionType,
                'status': status,
                'amount': self.safe_float(item, 'amount'),
                'fee': None,
                'info': item,
            })
        return result

    def parse_transfer_status(self, status):
        options = {
            'cancelled': 'canceled',
            'completed': 'ok',
        }
        return self.safe_string(options, status, 'pending')

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        walletId = self.safe_string(params, 'walletId')
        if walletId is None:
            raise ExchangeError(self.id + ' fetchMyTrades requires a walletId parameter')
        request = {
            'walletId': walletId,
        }
        if since is not None:
            request['rangeStart'] = self.ymdhms(since, 'T')
        if limit is not None:
            request['perPage'] = limit  # default 50, max 50
        response = self.privateGetWalletsWalletIdTrades(self.extend(request, params))
        #
        #     {
        #         "totalNumberOfRecords": "2",
        #         "currentPageNumber": "1",
        #         "latestExecutionId": "332",  # most recent execution at time of response
        #         "recordsPerPage": "50",
        #         "tradingHistory": [
        #             {
        #                 "orderId": "248ffda4-83a0-4033-a5bb-8929d523f59f",
        #                 "timestamp": "2015-05-11T14:48:01.9870000Z",
        #                 "instrument": "XBTUSD",
        #                 "direction": "buy",                      # buy or sell
        #                 "currency1": "XBT",                      # base currency
        #                 "currency1Amount": "0.00010000",         # order amount in base currency
        #                 "currency2": "USD",                      # quote currency
        #                 "currency2Amount": "0.0250530000000000",  # order cost in quote currency
        #                 "rate": "250.53000000",
        #                 "commissionPaid": "0.00000000",   # net trade fee paid after using any available rebate balance
        #                 "commissionCurrency": "USD",
        #                 "rebatesApplied": "-0.000125265",  # negative values represent amount of rebate balance used for trades removing liquidity from order book; positive values represent amount of rebate balance earned from trades adding liquidity to order book
        #                 "rebateCurrency": "USD",
        #                 "executionId": "23132"
        #             },
        #         ],
        #     }
        #
        trades = self.safe_value(response, 'tradingHistory', [])
        market = None
        if symbol is not None:
            market = self.market(symbol)
        return self.parse_trades(trades, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetMarketsSymbolTrades(self.extend(request, params))
        #
        #     {
        #         count: 3,
        #         recentTrades: [
        #             {
        #                 timestamp: "2015-05-22T17:45:34.7570000Z",
        #                 matchNumber: "5CR1JEUBBM8J",
        #                 price: "351.45000000",
        #                 amount: "0.00010000"
        #             },
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'recentTrades', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.fetch_wallets(params)
        balances = response[0]['balances']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'availableBalance')
            account['total'] = self.safe_float(balance, 'totalBalance')
            result[code] = account
        return self.parse_balance(result)

    def fetch_wallets(self, params={}):
        self.load_markets()
        if not self.uid:
            raise AuthenticationError(self.id + ' fetchWallets requires uid API credential')
        request = {
            'userId': self.uid,
        }
        return self.privateGetWallets(self.extend(request, params))

    def fetch_wallet(self, walletId, params={}):
        self.load_markets()
        request = {
            'walletId': walletId,
        }
        return self.privateGetWalletsWalletId(self.extend(request, params))

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'open',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 'filled',
        }
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        walletIdInParams = ('walletId' in params)
        if not walletIdInParams:
            raise ExchangeError(self.id + ' fetchOrders requires a walletId parameter')
        walletId = params['walletId']
        request = {
            'walletId': walletId,
        }
        response = self.privateGetWalletsWalletIdOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'submitted': 'open',  # order pending book entry
            'open': 'open',
            'filled': 'closed',
            'cancelled': 'canceled',
            'rejected': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "id": "13d6af57-8b0b-41e5-af30-becf0bcc574d",
        #         "walletId": "7e037345-1288-4c39-12fe-d0f99a475a98",
        #         "side": "buy",
        #         "instrument": "XBTUSD",
        #         "type": "limit",
        #         "currency": "XBT",
        #         "amount": "2.50000000",
        #         "displayAmount": "2.50000000",
        #         "price": "650.00000000",
        #         "volumeWeightedAveragePrice": "0.00000000",
        #         "amountFilled": "0.00000000",
        #         "createdTime": "2014-02-11T17:05:15Z",
        #         "status": "submitted",
        #         "funds": null,
        #         "metadata": {},
        #         "clientOrderIdentifier": null,
        #         "postOnly": "False"
        #     }
        #
        side = self.safe_string(order, 'side')
        type = self.safe_string(order, 'type')
        symbol = self.markets_by_id[order['instrument']]['symbol']
        timestamp = self.parse8601(order['createdTime'])
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'amountFilled')
        remaining = None
        cost = None
        fee = None
        price = self.safe_float(order, 'price')
        average = self.safe_float(order, 'volumeWeightedAveragePrice')
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
            if average is not None:
                cost = filled * average
        clientOrderId = self.safe_string(order, 'clientOrderIdentifier')
        id = self.safe_string(order, 'id')
        return {
            'id': id,
            'clientOrderId': clientOrderId,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': self.parse_order_status(self.safe_string(order, 'status')),
            'symbol': symbol,
            'type': type,
            'timeInForce': None,
            'side': side,
            'price': price,
            'stopPrice': None,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
            # 'trades': self.parse_trades(order['trades'], market),
            'trades': None,
        }

    def nonce(self):
        return self.milliseconds()

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        walletIdInParams = ('walletId' in params)
        if not walletIdInParams:
            raise ExchangeError(self.id + ' createOrder requires a walletId parameter')
        amount = str(amount)
        price = str(price)
        market = self.market(symbol)
        request = {
            'side': side,
            'type': type,
            'currency': market['id'].replace(market['quote'], ''),
            'amount': amount,
            'display': amount,
            'price': price,
            'instrument': market['id'],
        }
        response = self.privatePostWalletsWalletIdOrders(self.extend(request, params))
        return {
            'info': response,
            'id': response['id'],
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        walletIdInParams = ('walletId' in params)
        if not walletIdInParams:
            raise ExchangeError(self.id + ' fetchOrder requires a walletId parameter')
        request = {
            'id': id,
        }
        response = self.privateGetWalletsWalletIdOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def cancel_order(self, id, symbol=None, params={}):
        walletIdInParams = ('walletId' in params)
        if not walletIdInParams:
            raise ExchangeError(self.id + ' cancelOrder requires a walletId parameter')
        request = {
            'id': id,
        }
        return self.privateDeleteWalletsWalletIdOrdersId(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET' and query:
            url += '?' + self.urlencode(query)
        if method == 'POST' and query:
            body = self.json(query)
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            timestamp = nonce
            authBody = body if (method == 'POST') else ''
            auth = [method, url, authBody, nonce, timestamp]
            message = nonce + self.json(auth).replace('\\/', '/')
            hash = self.hash(self.encode(message), 'sha256', 'binary')
            binaryUrl = self.encode(url)
            binhash = self.binary_concat(binaryUrl, hash)
            signature = self.hmac(binhash, self.encode(self.secret), hashlib.sha512, 'base64')
            headers = {
                'Authorization': self.apiKey + ':' + signature,
                'Content-Type': 'application/json',
                'X-Auth-Timestamp': timestamp,
                'X-Auth-Nonce': nonce,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'code' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
