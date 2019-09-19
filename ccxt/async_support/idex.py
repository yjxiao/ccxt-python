# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder


class idex (Exchange):

    def describe(self):
        return self.deep_extend(super(idex, self).describe(), {
            'id': 'idex',
            'name': 'IDEX',
            'countries': ['US'],
            'rateLimit': 1500,
            'certified': True,
            'requiresWeb3': True,
            'has': {
                'fetchOrderBook': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchMarkets': True,
                'fetchBalance': True,
                'createOrder': True,
                'cancelOrder': True,
                'fetchTransactions': True,
                'fetchTrades': False,
                'fetchMyTrades': True,
                'withdraw': True,
                'fetchOHLCV': False,
            },
            'timeframes': {
                '1m': 'M1',
                '3m': 'M3',
                '5m': 'M5',
                '15m': 'M15',
                '30m': 'M30',  # default
                '1h': 'H1',
                '4h': 'H4',
                '1d': 'D1',
                '1w': 'D7',
                '1M': '1M',
            },
            'urls': {
                'test': 'https://api.idex.market',
                'logo': 'https://user-images.githubusercontent.com/1294454/63693236-3415e380-c81c-11e9-8600-ba1634f1407d.jpg',
                'api': 'https://api.idex.market',
                'www': 'https://idex.market',
                'doc': [
                    'https://github.com/AuroraDAO/idex-api-docs',
                ],
            },
            'api': {
                'public': {
                    'post': [
                        'returnTicker',
                        'returnCurrenciesWithPairs',  # undocumented
                        'returnCurrencies',
                        'return24Volume',
                        'returnBalances',
                        'returnCompleteBalances',  # shows amount in orders as well as total
                        'returnDepositsWithdrawals',
                        'returnOpenOrders',
                        'returnOrderBook',
                        'returnOrderStatus',
                        'returnOrderTrades',
                        'returnTradeHistory',
                        'returnTradeHistoryMeta',  # not documented
                        'returnContractAddress',
                        'returnNextNonce',
                    ],
                },
                'private': {
                    'post': [
                        'order',
                        'cancel',
                        'trade',
                        'withdraw',
                    ],
                },
            },
            'options': {
                'contractAddress': None,  # 0x2a0c0DBEcC7E4D658f48E01e3fA353F44050c208
                'orderNonce': None,
            },
            'exceptions': {
                'Invalid order signature. Please try again.': AuthenticationError,
                'You have insufficient funds to match self order. If you believe self is a mistake please refresh and try again.': InsufficientFunds,
                'Order no longer available.': InvalidOrder,
            },
            'requiredCredentials': {
                'walletAddress': True,
                'privateKey': True,
                'apiKey': False,
                'secret': False,
            },
        })

    async def fetch_markets(self, params={}):
        # idex does not have an endpoint for markets
        # instead we generate the markets from the endpoint for currencies
        request = {
            'includeDelisted': True,
        }
        markets = await self.publicPostReturnCurrenciesWithPairs(self.extend(request, params))
        currenciesById = {}
        currencies = markets['tokens']
        for i in range(0, len(currencies)):
            currency = currencies[i]
            currenciesById[currency['symbol']] = currency
        result = []
        limits = {
            'amount': {
                'min': None,
                'max': None,
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
        quotes = markets['pairs']
        keys = list(quotes.keys())
        for i in range(0, len(keys)):
            quoteId = keys[i]
            bases = quotes[quoteId]
            quote = self.safe_currency_code(quoteId)
            quoteCurrency = currenciesById[quoteId]
            for j in range(0, len(bases)):
                baseId = bases[j]
                id = quoteId + '_' + baseId
                base = self.safe_currency_code(baseId)
                symbol = base + '/' + quote
                baseCurrency = currenciesById[baseId]
                baseAddress = baseCurrency['address']
                quoteAddress = quoteCurrency['address']
                precision = {
                    'price': self.safe_integer(quoteCurrency, 'decimals'),
                    'amount': self.safe_integer(baseCurrency, 'decimals'),
                }
                result.append({
                    'symbol': symbol,
                    'precision': precision,
                    'base': base,
                    'quote': quote,
                    'baseId': baseAddress,
                    'quoteId': quoteAddress,
                    'limits': limits,
                    'id': id,
                    'info': baseCurrency,
                    'tierBased': False,
                })
        return result

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         last: '0.0016550916',
        #         high: 'N/A',
        #         low: 'N/A',
        #         lowestAsk: '0.0016743368',
        #         highestBid: '0.001163726270773897',
        #         percentChange: '0',
        #         baseVolume: '0',
        #         quoteVolume: '0'
        #     }
        #
        symbol = None
        if market:
            symbol = market['symbol']
        baseVolume = self.safe_float(ticker, 'baseVolume')
        quoteVolume = self.safe_float(ticker, 'quoteVolume')
        last = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'percentChange')
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': percentage,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicPostReturnTicker(params)
        #  {ETH_BOUNCY:
        #    {last: '0.000000004000088005',
        #      high: 'N/A',
        #      low: 'N/A',
        #      lowestAsk: '0.00000000599885995',
        #      highestBid: '0.000000001400500103',
        #      percentChange: '0',
        #      baseVolume: '0',
        #      quoteVolume: '0'},
        #   ETH_NBAI:
        #    {last: '0.0000032',
        #      high: 'N/A',
        #      low: 'N/A',
        #      lowestAsk: '0.000004000199999502',
        #      highestBid: '0.0000016002',
        #      percentChange: '0',
        #      baseVolume: '0',
        #      quoteVolume: '0'},}
        ids = list(response.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            symbol = None
            market = None
            if id in self.markets_by_id:
                market = self.markets_by_id[id]
                symbol = market['symbol']
            else:
                quoteId, baseId = id.split('_')
                base = self.safe_currency_code(baseId)
                quote = self.safe_currency_code(quoteId)
                symbol = base + '/' + quote
                market = {'symbol': symbol}
            ticker = response[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicPostReturnTicker(self.extend(request, params))
        # {last: '0.0016550916',
        #   high: 'N/A',
        #   low: 'N/A',
        #   lowestAsk: '0.0016743368',
        #   highestBid: '0.001163726270773897',
        #   percentChange: '0',
        #   baseVolume: '0',
        #   quoteVolume: '0'}
        return self.parse_ticker(response, market)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        id = market['quote'] + '_' + market['base']
        request = {
            'market': id,
            'count': 100,  # the default will only return one trade
        }
        if limit is not None:
            request['count'] = limit
        response = await self.publicPostReturnOrderBook(self.extend(request, params))
        #
        #     {
        #         "asks": [
        #             {
        #                 "price": "0.001675282799999",
        #                 "amount": "206.163978911921061732",
        #                 "total": "0.345382967850497906",
        #                 "orderHash": "0xfdf12c124a6a7fa4a8e1866b324da888c8e1b3ad209f5050d3a23df3397a5cb7",
        #                 "params": {
        #                     "tokenBuy": "0x0000000000000000000000000000000000000000",
        #                     "buySymbol": "ETH",
        #                     "buyPrecision": 18,
        #                     "amountBuy": "345382967850497906",
        #                     "tokenSell": "0xb98d4c97425d9908e66e53a6fdf673acca0be986",
        #                     "sellSymbol": "ABT",
        #                     "sellPrecision": 18,
        #                     "amountSell": "206163978911921061732",
        #                     "expires": 10000,
        #                     "nonce": 13489307413,
        #                     "user": "0x9e8ef79316a4a79bbf55a5f9c16b3e068fff65c6"
        #                 }
        #             }
        #         ],
        #         "bids": [
        #             {
        #                 "price": "0.001161865193232242",
        #                 "amount": "854.393661648355",
        #                 "total": "0.992690256787469029",
        #                 "orderHash": "0x2f2baaf982085e4096f9e23e376214885fa74b2939497968e92222716fc2c86d",
        #                 "params": {
        #                     "tokenBuy": "0xb98d4c97425d9908e66e53a6fdf673acca0be986",
        #                     "buySymbol": "ABT",
        #                     "buyPrecision": 18,
        #                     "amountBuy": "854393661648355000000",
        #                     "tokenSell": "0x0000000000000000000000000000000000000000",
        #                     "sellSymbol": "ETH",
        #                     "sellPrecision": 18,
        #                     "amountSell": "992690256787469029",
        #                     "expires": 10000,
        #                     "nonce": 18155189676,
        #                     "user": "0xb631284dd7b74a846af5b37766ceb1f85d53eca4"
        #                 }
        #             }
        #         ]
        #     }
        #
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'amount')

    def parse_bid_ask(self, bidAsk, priceKey=0, amountKey=1):
        price = self.safe_float(bidAsk, priceKey)
        amount = self.safe_float(bidAsk, amountKey)
        info = bidAsk
        return [price, amount, info]

    async def fetch_balance(self, params={}):
        request = {
            'address': self.walletAddress,
        }
        response = await self.publicPostReturnCompleteBalances(self.extend(request, params))
        #
        #     {
        #         ETH: {available: '0.0167', onOrders: '0.1533'}
        #     }
        #
        result = {
            'info': response,
        }
        keys = list(response.keys())
        for i in range(0, len(keys)):
            currency = keys[i]
            balance = response[currency]
            code = self.safe_currency_code(currency)
            result[code] = {
                'free': self.safe_float(balance, 'available'),
                'used': self.safe_float(balance, 'onOrders'),
            }
        return self.parse_balance(result)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.check_required_dependencies()
        await self.load_markets()
        market = self.market(symbol)
        if type == 'limit':
            expires = 100000
            contractAddress = await self.get_contract_address()
            tokenBuy = None
            tokenSell = None
            amountBuy = None
            amountSell = None
            quoteAmount = float(price) * float(amount)
            if side == 'buy':
                tokenBuy = market['baseId']
                tokenSell = market['quoteId']
                amountBuy = self.toWei(amount, 'ether', market['precision']['amount'])
                amountSell = self.toWei(quoteAmount, 'ether', 18)
            else:
                tokenBuy = market['quoteId']
                tokenSell = market['baseId']
                amountBuy = self.toWei(quoteAmount, 'ether', 18)
                amountSell = self.toWei(amount, 'ether', market['precision']['amount'])
            nonce = await self.get_nonce()
            orderToHash = {
                'contractAddress': contractAddress,
                'tokenBuy': tokenBuy,
                'amountBuy': amountBuy,
                'tokenSell': tokenSell,
                'amountSell': amountSell,
                'expires': expires,
                'nonce': nonce,
                'address': self.walletAddress,
            }
            orderHash = self.get_idex_create_order_hash(orderToHash)
            signature = self.signMessage(orderHash, self.privateKey)
            request = {
                'tokenBuy': tokenBuy,
                'amountBuy': amountBuy,
                'tokenSell': tokenSell,
                'amountSell': amountSell,
                'address': self.walletAddress,
                'nonce': nonce,
                'expires': expires,
            }
            response = await self.privatePostOrder(self.extend(request, signature))  # self.extend(request, params) will cause invalid signature
            # {orderNumber: 1562323021,
            #   orderHash:
            #    '0x31c42154a8421425a18d076df400d9ec1ef64d5251285384a71ba3c0ab31beb4',
            #   timestamp: 1564041428,
            #   price: '0.00073',
            #   amount: '210',
            #   total: '0.1533',
            #   type: 'buy',
            #   params:
            #    {tokenBuy: '0x763fa6806e1acf68130d2d0f0df754c93cc546b2',
            #      buyPrecision: 18,
            #      amountBuy: '210000000000000000000',
            #      tokenSell: '0x0000000000000000000000000000000000000000',
            #      sellPrecision: 18,
            #      amountSell: '153300000000000000',
            #      expires: 100000,
            #      nonce: 1,
            #      user: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1'} }
            return self.parse_order(response, market)
        elif type == 'market':
            if not('orderHash' in list(params.keys())):
                raise ArgumentsRequired(self.id + ' market order requires an order structure such as that in fetchOrderBook()[\'bids\'][0][2], fetchOrder()[\'info\'], or fetchOpenOrders()[0][\'info\']')
            # {price: '0.000132247803328924',
            #   amount: '19980',
            #   total: '2.6423111105119',
            #   orderHash:
            #    '0x5fb3452b3d13fc013585b51c91c43a0fbe4298c211243763c49437848c274749',
            #   params:
            #    {tokenBuy: '0x0000000000000000000000000000000000000000',
            #      buySymbol: 'ETH',
            #      buyPrecision: 18,
            #      amountBuy: '2642311110511900000',
            #      tokenSell: '0xb705268213d593b8fd88d3fdeff93aff5cbdcfae',
            #      sellSymbol: 'IDEX',
            #      sellPrecision: 18,
            #      amountSell: '19980000000000000000000',
            #      expires: 10000,
            #      nonce: 1564656561510,
            #      user: '0xc3f8304270e49b8e8197bfcfd8567b83d9e4479b'} }
            orderToSign = {
                'orderHash': params['orderHash'],
                'amount': params['params']['amountBuy'],
                'address': params['params']['user'],
                'nonce': params['params']['nonce'],
            }
            orderHash = self.get_idex_market_order_hash(orderToSign)
            signature = self.signMessage(orderHash, self.privateKey)
            signedOrder = self.extend(orderToSign, signature)
            signedOrder['address'] = self.walletAddress
            signedOrder['nonce'] = await self.get_nonce()
            #   [{
            #     "amount": "0.07",
            #     "date": "2017-10-13 16:25:36",
            #     "total": "0.49",
            #     "market": "ETH_DVIP",
            #     "type": "buy",
            #     "price": "7",
            #     "orderHash": "0xcfe4018c59e50e0e1964c979e6213ce5eb8c751cbc98a44251eb48a0985adc52",
            #     "uuid": "250d51a0-b033-11e7-9984-a9ab79bb8f35"
            #   }]
            response = await self.privatePostTrade(signedOrder)
            return self.parse_orders(response, market)

    async def get_nonce(self):
        if self.options['orderNonce'] is None:
            response = await self.publicPostReturnNextNonce({
                'address': self.walletAddress,
            })
            return self.safe_integer(response, 'nonce')
        else:
            result = self.options['orderNonce']
            self.options['orderNonce'] = self.sum(self.options['orderNonce'], 1)
            return result

    async def get_contract_address(self):
        if self.options['contractAddress'] is not None:
            return self.options['contractAddress']
        response = await self.publicPostReturnContractAddress()
        self.options['contractAddress'] = self.safe_string(response, 'address')
        return self.options['contractAddress']

    async def cancel_order(self, orderId, symbol=None, params={}):
        nonce = await self.get_nonce()
        orderToHash = {
            'orderHash': orderId,
            'nonce': nonce,
        }
        orderHash = self.get_idex_cancel_order_hash(orderToHash)
        signature = self.signMessage(orderHash, self.privateKey)
        request = {
            'orderHash': orderId,
            'address': self.walletAddress,
            'nonce': nonce,
        }
        response = await self.privatePostCancel(self.extend(request, signature))
        # {success: 1}
        if 'success' in response:
            return {
                'info': response,
            }
        else:
            raise ExchangeError(self.id + ' cancel order failed ' + self.json(response))

    async def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'address': self.walletAddress,
        }
        if since is not None:
            request['start'] = int(int(math.floor(since / 1000)))
        response = await self.publicPostReturnDepositsWithdrawals(self.extend(request, params))
        # {deposits:
        #    [{currency: 'ETH',
        #        amount: '0.05',
        #        timestamp: 1563953513,
        #        transactionHash:
        #         '0xd6eefd81c7efc9beeb35b924d6db3c93a78bf7eac082ba87e107ad4e94bccdcf',
        #        depositNumber: 1586430},
        #      {currency: 'ETH',
        #        amount: '0.12',
        #        timestamp: 1564040359,
        #        transactionHash:
        #         '0x2ecbb3ab72b6f79fc7a9058c39dce28f913152748c1507d13ab1759e965da3ca',
        #        depositNumber: 1587341}],
        #   withdrawals:
        #    [{currency: 'ETH',
        #        amount: '0.149',
        #        timestamp: 1564060001,
        #        transactionHash:
        #         '0xab555fc301779dd92fd41ccd143b1d72776ae7b5acfc59ca44a1d376f68fda15',
        #        withdrawalNumber: 1444070,
        #        status: 'COMPLETE'}]}
        deposits = self.parseTransactions(response['deposits'], currency, since, limit)
        withdrawals = self.parseTransactions(response['withdrawals'], currency, since, limit)
        return self.array_concat(deposits, withdrawals)

    def parse_transaction(self, item, currency=None):
        # {currency: 'ETH',
        #   amount: '0.05',
        #   timestamp: 1563953513,
        #   transactionHash:
        #    '0xd6eefd81c7efc9beeb35b924d6db3c93a78bf7eac082ba87e107ad4e94bccdcf',
        #   depositNumber: 1586430}
        amount = self.safe_float(item, 'amount')
        timestamp = self.safe_timestamp(item, 'timestamp')
        txhash = self.safe_string(item, 'transactionHash')
        id = None
        type = None
        status = None
        addressFrom = None
        addressTo = None
        if 'depositNumber' in item:
            id = self.safe_string(item, 'depositNumber')
            type = 'deposit'
            addressFrom = self.walletAddress
            addressTo = self.options['contractAddress']
        elif 'withdrawalNumber' in item:
            id = self.safe_string(item, 'withdrawalNumber')
            type = 'withdrawal'
            status = self.parse_transaction_status(self.safe_string(item, 'status'))
            addressFrom = self.options['contractAddress']
            addressTo = self.walletAddress
        code = self.safe_currency_code(self.safe_string(item, 'currency'))
        return {
            'info': item,
            'id': id,
            'txid': txhash,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'currency': code,
            'amount': amount,
            'status': status,
            'type': type,
            'updated': None,
            'comment': None,
            'addressFrom': addressFrom,
            'tagFrom': None,
            'addressTo': addressTo,
            'tagTo': None,
            'fee': {
                'currency': code,
                'cost': None,
                'rate': None,
            },
        }

    def parse_transaction_status(self, status):
        statuses = {
            'COMPLETE': 'ok',
        }
        return self.safe_string(statuses, status)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if self.walletAddress is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders requires a walletAddress')
        await self.load_markets()
        request = {
            'address': self.walletAddress,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        response = await self.publicPostReturnOpenOrders(self.extend(request, params))
        # [{timestamp: 1564041428,
        #     orderHash:
        #      '0x31c42154a8421425a18d076df400d9ec1ef64d5251285384a71ba3c0ab31beb4',
        #     orderNumber: 1562323021,
        #     market: 'ETH_LIT',
        #     type: 'buy',
        #     params:
        #      {tokenBuy: '0x763fa6806e1acf68130d2d0f0df754c93cc546b2',
        #        buySymbol: 'LIT',
        #        buyPrecision: 18,
        #        amountBuy: '210000000000000000000',
        #        tokenSell: '0x0000000000000000000000000000000000000000',
        #        sellSymbol: 'ETH',
        #        sellPrecision: 18,
        #        amountSell: '153300000000000000',
        #        expires: 100000,
        #        nonce: 1,
        #        user: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1'},
        #     price: '0.00073',
        #     amount: '210',
        #     status: 'open',
        #     total: '0.1533'}]
        return self.parse_orders(response, market, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {
            'orderHash': id,
        }
        response = await self.publicPostReturnOrderStatus(self.extend(request, params))
        # {filled: '0',
        #   initialAmount: '210',
        #   timestamp: 1564041428,
        #   orderHash:
        #    '0x31c42154a8421425a18d076df400d9ec1ef64d5251285384a71ba3c0ab31beb4',
        #   orderNumber: 1562323021,
        #   market: 'ETH_LIT',
        #   type: 'buy',
        #   params:
        #    {tokenBuy: '0x763fa6806e1acf68130d2d0f0df754c93cc546b2',
        #      buySymbol: 'LIT',
        #      buyPrecision: 18,
        #      amountBuy: '210000000000000000000',
        #      tokenSell: '0x0000000000000000000000000000000000000000',
        #      sellSymbol: 'ETH',
        #      sellPrecision: 18,
        #      amountSell: '153300000000000000',
        #      expires: 100000,
        #      nonce: 1,
        #      user: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1'},
        #   price: '0.00073',
        #   amount: '210',
        #   status: 'open',
        #   total: '0.1533'}
        return self.parse_order(response, market)

    def parse_order(self, order, market=None):
        # {filled: '0',
        #   initialAmount: '210',
        #   timestamp: 1564041428,
        #   orderHash:
        #    '0x31c42154a8421425a18d076df400d9ec1ef64d5251285384a71ba3c0ab31beb4',
        #   orderNumber: 1562323021,
        #   market: 'ETH_LIT',
        #   type: 'buy',
        #   params:
        #    {tokenBuy: '0x763fa6806e1acf68130d2d0f0df754c93cc546b2',
        #      buySymbol: 'LIT',
        #      buyPrecision: 18,
        #      amountBuy: '210000000000000000000',
        #      tokenSell: '0x0000000000000000000000000000000000000000',
        #      sellSymbol: 'ETH',
        #      sellPrecision: 18,
        #      amountSell: '153300000000000000',
        #      expires: 100000,
        #      nonce: 1,
        #      user: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1'},
        #   price: '0.00073',
        #   amount: '210',
        #   status: 'open',
        #   total: '0.1533'}
        timestamp = self.safe_timestamp(order, 'timestamp')
        side = self.safe_string(order, 'type')
        symbol = None
        amount = None
        remaining = None
        if 'initialAmount' in order:
            amount = self.safe_float(order, 'initialAmount')
            remaining = self.safe_float(order, 'amount')
        else:
            amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'filled')
        cost = self.safe_float(order, 'total')
        price = self.safe_float(order, 'price')
        if 'market' in order:
            marketId = order['market']
            symbol = self.markets_by_id[marketId]['symbol']
        elif (side is not None) and ('params' in list(order.keys())):
            params = order['params']
            buy = self.safe_currency_code(self.safe_string(params, 'tokenBuy'))
            sell = self.safe_currency_code(self.safe_string(params, 'tokenSell'))
            if buy is not None and sell is not None:
                symbol = (buy + '/' + sell) if (side == 'buy') else (sell + '/' + buy)
        if symbol is None and market is not None:
            symbol = market['symbol']
        id = self.safe_string(order, 'orderHash')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        return {
            'info': order,
            'id': id,
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'side': side,
            'amount': amount,
            'price': price,
            'type': 'limit',
            'filled': filled,
            'remaining': remaining,
            'cost': cost,
            'status': status,
        }

    def parse_order_status(self, status):
        statuses = {
            'open': 'open',
        }
        return self.safe_string(statuses, status, status)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if self.walletAddress is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders requires a walletAddress')
        await self.load_markets()
        request = {
            'address': self.walletAddress,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['market'] = market['id']
        if limit is not None:
            request['start'] = int(int(math.floor(limit)))
        response = await self.publicPostReturnTradeHistory(self.extend(request, params))
        # {ETH_IDEX:
        #    [{type: 'buy',
        #        date: '2019-07-25 11:24:41',
        #        amount: '347.833140025692348611',
        #        total: '0.050998794333719943',
        #        uuid: 'cbdff960-aece-11e9-b566-c5d69c3be671',
        #        tid: 4320867,
        #        timestamp: 1564053881,
        #        price: '0.000146618560640751',
        #        taker: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1',
        #        maker: '0x1a961bc2e0d619d101f5f92a6be752132d7606e6',
        #        orderHash:
        #         '0xbec6485613a15be619c04c1425e8e821ebae42b88fa95ac4dfe8ba2beb363ee4',
        #        transactionHash:
        #         '0xf094e07b329ac8046e8f34db358415863c41daa36765c05516f4cf4f5b403ad1',
        #        tokenBuy: '0x0000000000000000000000000000000000000000',
        #        buyerFee: '0.695666280051384697',
        #        gasFee: '28.986780264563232993',
        #        sellerFee: '0.00005099879433372',
        #        tokenSell: '0xb705268213d593b8fd88d3fdeff93aff5cbdcfae',
        #        usdValue: '11.336926687304238214'}]}
        #
        # if a symbol is specified in the request:
        #
        #    [{type: 'buy',
        #        date: '2019-07-25 11:24:41',
        #        amount: '347.833140025692348611',
        #        total: '0.050998794333719943',
        #        uuid: 'cbdff960-aece-11e9-b566-c5d69c3be671',
        #        tid: 4320867,
        #        timestamp: 1564053881,
        #        price: '0.000146618560640751',
        #        taker: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1',
        #        maker: '0x1a961bc2e0d619d101f5f92a6be752132d7606e6',
        #        orderHash:
        #         '0xbec6485613a15be619c04c1425e8e821ebae42b88fa95ac4dfe8ba2beb363ee4',
        #        transactionHash:
        #         '0xf094e07b329ac8046e8f34db358415863c41daa36765c05516f4cf4f5b403ad1',
        #        tokenBuy: '0x0000000000000000000000000000000000000000',
        #        buyerFee: '0.695666280051384697',
        #        gasFee: '28.986780264563232993',
        #        sellerFee: '0.00005099879433372',
        #        tokenSell: '0xb705268213d593b8fd88d3fdeff93aff5cbdcfae',
        #        usdValue: '11.336926687304238214'}]
        if isinstance(response, list):
            return self.parse_trades(response, market, since, limit)
        else:
            result = []
            marketIds = list(response.keys())
            for i in range(0, len(marketIds)):
                marketId = marketIds[i]
                trades = response[marketId]
                parsed = self.parse_trades(trades, market, since, limit)
                result = self.array_concat(result, parsed)
            return result

    def parse_trade(self, trade, market=None):
        # {type: 'buy',
        #   date: '2019-07-25 11:24:41',
        #   amount: '347.833140025692348611',
        #   total: '0.050998794333719943',
        #   uuid: 'cbdff960-aece-11e9-b566-c5d69c3be671',
        #   tid: 4320867,
        #   timestamp: 1564053881,
        #   price: '0.000146618560640751',
        #   taker: '0x0ab991497116f7f5532a4c2f4f7b1784488628e1',
        #   maker: '0x1a961bc2e0d619d101f5f92a6be752132d7606e6',
        #   orderHash:
        #    '0xbec6485613a15be619c04c1425e8e821ebae42b88fa95ac4dfe8ba2beb363ee4',
        #   transactionHash:
        #    '0xf094e07b329ac8046e8f34db358415863c41daa36765c05516f4cf4f5b403ad1',
        #   tokenBuy: '0x0000000000000000000000000000000000000000',
        #   buyerFee: '0.695666280051384697',
        #   gasFee: '28.986780264563232993',
        #   sellerFee: '0.00005099879433372',
        #   tokenSell: '0xb705268213d593b8fd88d3fdeff93aff5cbdcfae',
        #   usdValue: '11.336926687304238214'}
        side = self.safe_string(trade, 'type')
        feeCurrency = None
        symbol = None
        maker = self.safe_string(trade, 'maker')
        takerOrMaker = None
        if maker is not None:
            if maker.lower() == self.walletAddress.lower():
                takerOrMaker = 'maker'
            else:
                takerOrMaker = 'taker'
        buy = self.safe_currency_code(self.safe_string(trade, 'tokenBuy'))
        sell = self.safe_currency_code(self.safe_string(trade, 'tokenSell'))
        # get ready to be mind-boggled
        feeSide = None
        if buy is not None and sell is not None:
            if side == 'buy':
                feeSide = 'buyerFee'
                if takerOrMaker == 'maker':
                    symbol = buy + '/' + sell
                    feeCurrency = buy
                else:
                    symbol = sell + '/' + buy
                    feeCurrency = sell
            else:
                feeSide = 'sellerFee'
                if takerOrMaker == 'maker':
                    symbol = sell + '/' + buy
                    feeCurrency = buy
                else:
                    symbol = buy + '/' + sell
                    feeCurrency = sell
        if symbol is None and market is not None:
            symbol = market['symbol']
        timestamp = self.safe_timestamp(trade, 'timestamp')
        id = self.safe_string(trade, 'tid')
        amount = self.safe_float(trade, 'amount')
        price = self.safe_float(trade, 'price')
        cost = self.safe_float(trade, 'total')
        feeCost = self.safe_float(trade, feeSide)
        if feeCost < 0:
            gasFee = self.safe_float(trade, 'gasFee')
            feeCost = self.sum(gasFee, feeCost)
        fee = {
            'currency': feeCurrency,
            'cost': feeCost,
        }
        if feeCost is not None and amount is not None:
            feeCurrencyAmount = feeCurrency == cost if 'ETH' else amount
            fee['rate'] = feeCost / feeCurrencyAmount
        orderId = self.safe_string(trade, 'orderHash')
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'fee': fee,
            'price': price,
            'amount': amount,
            'cost': cost,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'order': orderId,
            'symbol': symbol,
            'type': 'limit',
        }

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_required_dependencies()
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        tokenAddress = currency['id']
        nonce = await self.get_nonce()
        amount = self.toWei(amount, 'ether', currency['precision'])
        requestToHash = {
            'contractAddress': await self.get_contract_address(),
            'token': tokenAddress,
            'amount': amount,
            'address': address,
            'nonce': nonce,
        }
        hash = self.get_idex_withdraw_hash(requestToHash)
        signature = self.signMessage(hash, self.privateKey)
        request = {
            'address': address,
            'amount': amount,
            'token': tokenAddress,
            'nonce': nonce,
        }
        response = await self.privatePostWithdraw(self.extend(request, signature))
        # {amount: '0'}
        return {
            'info': response,
            'id': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        body = self.json(params)  # all methods are POST
        url = self.urls['api'] + '/' + path
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if api == 'private':
            self.check_required_credentials()
            headers['API-Key'] = self.apiKey
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def get_idex_create_order_hash(self, order):
        return self.soliditySha3([
            order['contractAddress'],  # address
            order['tokenBuy'],  # address
            order['amountBuy'],  # uint256
            order['tokenSell'],  # address
            order['amountSell'],  # uint256
            order['expires'],  # uint256
            order['nonce'],  # uint256
            order['address'],  # address
        ])

    def get_idex_cancel_order_hash(self, order):
        return self.soliditySha3([
            order['orderHash'],  # address
            order['nonce'],  # uint256
        ])

    def get_idex_market_order_hash(self, order):
        return self.soliditySha3([
            order['orderHash'],  # address
            order['amount'],  # uint256
            order['address'],  # address
            order['nonce'],  # uint256
        ])

    def get_idex_withdraw_hash(self, request):
        return self.soliditySha3([
            request['contractAddress'],  # address
            request['token'],  # uint256
            request['amount'],  # uint256
            request['address'],  # address
            request['nonce'],  # uint256
        ])

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'error' in response:
            if response['error'] in self.exceptions:
                raise self.exceptions[response['error']](self.id + ' ' + response['error'])
            raise ExchangeError(self.id + ' ' + body)
