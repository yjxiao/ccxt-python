# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.abstract.independentreserve import ImplicitAPI
import hashlib
from ccxt.base.types import Balances, Currency, Int, Market, Num, Order, OrderBook, OrderSide, OrderType, Str, Ticker, Trade
from typing import List
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class independentreserve(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(independentreserve, self).describe(), {
            'id': 'independentreserve',
            'name': 'Independent Reserve',
            'countries': ['AU', 'NZ'],  # Australia, New Zealand
            'rateLimit': 1000,
            'pro': True,
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': False,
                'option': False,
                'addMargin': False,
                'cancelOrder': True,
                'closeAllPositions': False,
                'closePosition': False,
                'createOrder': True,
                'createReduceOnlyOrder': False,
                'createStopLimitOrder': False,
                'createStopMarketOrder': False,
                'createStopOrder': False,
                'fetchBalance': True,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchClosedOrders': True,
                'fetchCrossBorrowRate': False,
                'fetchCrossBorrowRates': False,
                'fetchDepositAddress': True,
                'fetchDepositAddresses': False,
                'fetchDepositAddressesByNetwork': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedBorrowRate': False,
                'fetchIsolatedBorrowRates': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarginMode': False,
                'fetchMarkets': True,
                'fetchMarkOHLCV': False,
                'fetchMyTrades': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchPosition': False,
                'fetchPositionMode': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': True,
                'reduceMargin': False,
                'setLeverage': False,
                'setMarginMode': False,
                'setPositionMode': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87182090-1e9e9080-c2ec-11ea-8e49-563db9a38f37.jpg',
                'api': {
                    'public': 'https://api.independentreserve.com/Public',
                    'private': 'https://api.independentreserve.com/Private',
                },
                'www': 'https://www.independentreserve.com',
                'doc': 'https://www.independentreserve.com/API',
            },
            'api': {
                'public': {
                    'get': [
                        'GetValidPrimaryCurrencyCodes',
                        'GetValidSecondaryCurrencyCodes',
                        'GetValidLimitOrderTypes',
                        'GetValidMarketOrderTypes',
                        'GetValidOrderTypes',
                        'GetValidTransactionTypes',
                        'GetMarketSummary',
                        'GetOrderBook',
                        'GetAllOrders',
                        'GetTradeHistorySummary',
                        'GetRecentTrades',
                        'GetFxRates',
                        'GetOrderMinimumVolumes',
                        'GetCryptoWithdrawalFees',
                    ],
                },
                'private': {
                    'post': [
                        'GetOpenOrders',
                        'GetClosedOrders',
                        'GetClosedFilledOrders',
                        'GetOrderDetails',
                        'GetAccounts',
                        'GetTransactions',
                        'GetFiatBankAccounts',
                        'GetDigitalCurrencyDepositAddress',
                        'GetDigitalCurrencyDepositAddresses',
                        'GetTrades',
                        'GetBrokerageFees',
                        'GetDigitalCurrencyWithdrawal',
                        'PlaceLimitOrder',
                        'PlaceMarketOrder',
                        'CancelOrder',
                        'SynchDigitalCurrencyDepositAddressWithBlockchain',
                        'RequestFiatWithdrawal',
                        'WithdrawFiatCurrency',
                        'WithdrawDigitalCurrency',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'taker': self.parse_number('0.005'),
                    'maker': self.parse_number('0.005'),
                    'percentage': True,
                    'tierBased': False,
                },
            },
            'commonCurrencies': {
                'PLA': 'PlayChip',
            },
            'precisionMode': TICK_SIZE,
        })

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for independentreserve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: an array of objects representing market data
        """
        baseCurrencies = await self.publicGetGetValidPrimaryCurrencyCodes(params)
        #     ['Xbt', 'Eth', 'Usdt', ...]
        quoteCurrencies = await self.publicGetGetValidSecondaryCurrencyCodes(params)
        #     ['Aud', 'Usd', 'Nzd', 'Sgd']
        limits = await self.publicGetGetOrderMinimumVolumes(params)
        #
        #     {
        #         "Xbt": 0.0001,
        #         "Eth": 0.001,
        #         "Ltc": 0.01,
        #         "Xrp": 1.0,
        #     }
        #
        result = []
        for i in range(0, len(baseCurrencies)):
            baseId = baseCurrencies[i]
            base = self.safe_currency_code(baseId)
            minAmount = self.safe_number(limits, baseId)
            for j in range(0, len(quoteCurrencies)):
                quoteId = quoteCurrencies[j]
                quote = self.safe_currency_code(quoteId)
                id = baseId + '/' + quoteId
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
                    'active': None,
                    'contract': False,
                    'linear': None,
                    'inverse': None,
                    'contractSize': None,
                    'expiry': None,
                    'expiryDatetime': None,
                    'strike': None,
                    'optionType': None,
                    'precision': {
                        'amount': None,
                        'price': None,
                    },
                    'limits': {
                        'leverage': {
                            'min': None,
                            'max': None,
                        },
                        'amount': {
                            'min': minAmount,
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
                    },
                    'created': None,
                    'info': id,
                })
        return result

    def parse_balance(self, response) -> Balances:
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'CurrencyCode')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'AvailableBalance')
            account['total'] = self.safe_string(balance, 'TotalBalance')
            result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}) -> Balances:
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/#/?id=balance-structure>`
        """
        await self.load_markets()
        response = await self.privatePostGetAccounts(params)
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'primaryCurrencyCode': market['baseId'],
            'secondaryCurrencyCode': market['quoteId'],
        }
        response = await self.publicGetGetOrderBook(self.extend(request, params))
        timestamp = self.parse8601(self.safe_string(response, 'CreatedTimestampUtc'))
        return self.parse_order_book(response, market['symbol'], timestamp, 'BuyOrders', 'SellOrders', 'Price', 'Volume')

    def parse_ticker(self, ticker, market: Market = None) -> Ticker:
        # {
        #     "DayHighestPrice":43489.49,
        #     "DayLowestPrice":41998.32,
        #     "DayAvgPrice":42743.9,
        #     "DayVolumeXbt":44.54515625000,
        #     "DayVolumeXbtInSecondaryCurrrency":0.12209818,
        #     "CurrentLowestOfferPrice":43619.64,
        #     "CurrentHighestBidPrice":43153.58,
        #     "LastPrice":43378.43,
        #     "PrimaryCurrencyCode":"Xbt",
        #     "SecondaryCurrencyCode":"Usd",
        #     "CreatedTimestampUtc":"2022-01-14T22:52:29.5029223Z"
        # }
        timestamp = self.parse8601(self.safe_string(ticker, 'CreatedTimestampUtc'))
        baseId = self.safe_string(ticker, 'PrimaryCurrencyCode')
        quoteId = self.safe_string(ticker, 'SecondaryCurrencyCode')
        defaultMarketId = None
        if (baseId is not None) and (quoteId is not None):
            defaultMarketId = baseId + '/' + quoteId
        market = self.safe_market(defaultMarketId, market, '/')
        symbol = market['symbol']
        last = self.safe_string(ticker, 'LastPrice')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'DayHighestPrice'),
            'low': self.safe_string(ticker, 'DayLowestPrice'),
            'bid': self.safe_string(ticker, 'CurrentHighestBidPrice'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'CurrentLowestOfferPrice'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': self.safe_string(ticker, 'DayAvgPrice'),
            'baseVolume': self.safe_string(ticker, 'DayVolumeXbtInSecondaryCurrrency'),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'primaryCurrencyCode': market['baseId'],
            'secondaryCurrencyCode': market['quoteId'],
        }
        response = await self.publicGetGetMarketSummary(self.extend(request, params))
        # {
        #     "DayHighestPrice":43489.49,
        #     "DayLowestPrice":41998.32,
        #     "DayAvgPrice":42743.9,
        #     "DayVolumeXbt":44.54515625000,
        #     "DayVolumeXbtInSecondaryCurrrency":0.12209818,
        #     "CurrentLowestOfferPrice":43619.64,
        #     "CurrentHighestBidPrice":43153.58,
        #     "LastPrice":43378.43,
        #     "PrimaryCurrencyCode":"Xbt",
        #     "SecondaryCurrencyCode":"Usd",
        #     "CreatedTimestampUtc":"2022-01-14T22:52:29.5029223Z"
        # }
        return self.parse_ticker(response, market)

    def parse_order(self, order, market: Market = None) -> Order:
        #
        # fetchOrder
        #
        #     {
        #         "OrderGuid": "c7347e4c-b865-4c94-8f74-d934d4b0b177",
        #         "CreatedTimestampUtc": "2014-09-23T12:39:34.3817763Z",
        #         "Type": "MarketBid",
        #         "VolumeOrdered": 5.0,
        #         "VolumeFilled": 5.0,
        #         "Price": null,
        #         "AvgPrice": 100.0,
        #         "ReservedAmount": 0.0,
        #         "Status": "Filled",
        #         "PrimaryCurrencyCode": "Xbt",
        #         "SecondaryCurrencyCode": "Usd"
        #     }
        #
        # fetchOpenOrders & fetchClosedOrders
        #
        #     {
        #         "OrderGuid": "b8f7ad89-e4e4-4dfe-9ea3-514d38b5edb3",
        #         "CreatedTimestampUtc": "2020-09-08T03:04:18.616367Z",
        #         "OrderType": "LimitOffer",
        #         "Volume": 0.0005,
        #         "Outstanding": 0.0005,
        #         "Price": 113885.83,
        #         "AvgPrice": 113885.83,
        #         "Value": 56.94,
        #         "Status": "Open",
        #         "PrimaryCurrencyCode": "Xbt",
        #         "SecondaryCurrencyCode": "Usd",
        #         "FeePercent": 0.005,
        #     }
        #
        symbol = None
        baseId = self.safe_string(order, 'PrimaryCurrencyCode')
        quoteId = self.safe_string(order, 'SecondaryCurrencyCode')
        base = None
        quote = None
        if (baseId is not None) and (quoteId is not None):
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
        elif market is not None:
            symbol = market['symbol']
            base = market['base']
            quote = market['quote']
        orderType = self.safe_string_2(order, 'Type', 'OrderType')
        side = None
        if orderType is not None:
            if orderType.find('Bid') >= 0:
                side = 'buy'
            elif orderType.find('Offer') >= 0:
                side = 'sell'
            if orderType.find('Market') >= 0:
                orderType = 'market'
            elif orderType.find('Limit') >= 0:
                orderType = 'limit'
        timestamp = self.parse8601(self.safe_string(order, 'CreatedTimestampUtc'))
        filled = self.safe_string(order, 'VolumeFilled')
        feeRate = self.safe_string(order, 'FeePercent')
        feeCost = None
        if feeRate is not None and filled is not None:
            feeCost = Precise.string_mul(feeRate, filled)
        return self.safe_order({
            'info': order,
            'id': self.safe_string(order, 'OrderGuid'),
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': orderType,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': self.safe_string(order, 'Price'),
            'stopPrice': None,
            'triggerPrice': None,
            'cost': self.safe_string(order, 'Value'),
            'average': self.safe_string(order, 'AvgPrice'),
            'amount': self.safe_string_2(order, 'VolumeOrdered', 'Volume'),
            'filled': filled,
            'remaining': self.safe_string(order, 'Outstanding'),
            'status': self.parse_order_status(self.safe_string(order, 'Status')),
            'fee': {
                'rate': feeRate,
                'cost': feeCost,
                'currency': base,
            },
            'trades': None,
        }, market)

    def parse_order_status(self, status):
        statuses = {
            'Open': 'open',
            'PartiallyFilled': 'open',
            'Filled': 'closed',
            'PartiallyFilledAndCancelled': 'canceled',
            'Cancelled': 'canceled',
            'PartiallyFilledAndExpired': 'canceled',
            'Expired': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    async def fetch_order(self, id: str, symbol: Str = None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        response = await self.privatePostGetOrderDetails(self.extend({
            'orderGuid': id,
        }, params))
        market = None
        if symbol is not None:
            market = self.market(symbol)
        return self.parse_order(response, market)

    async def fetch_open_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of  open orders structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        request = self.ordered({})
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['primaryCurrencyCode'] = market['baseId']
            request['secondaryCurrencyCode'] = market['quoteId']
        if limit is None:
            limit = 50
        request['pageIndex'] = 1
        request['pageSize'] = limit
        response = await self.privatePostGetOpenOrders(self.extend(request, params))
        data = self.safe_value(response, 'Data', [])
        return self.parse_orders(data, market, since, limit)

    async def fetch_closed_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetches information on multiple closed orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        request = self.ordered({})
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['primaryCurrencyCode'] = market['baseId']
            request['secondaryCurrencyCode'] = market['quoteId']
        if limit is None:
            limit = 50
        request['pageIndex'] = 1
        request['pageSize'] = limit
        response = await self.privatePostGetClosedOrders(self.extend(request, params))
        data = self.safe_value(response, 'Data', [])
        return self.parse_orders(data, market, since, limit)

    async def fetch_my_trades(self, symbol: Str = None, since: Int = None, limit: Int = 50, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Trade[]: a list of `trade structures <https://docs.ccxt.com/#/?id=trade-structure>`
        """
        await self.load_markets()
        pageIndex = self.safe_integer(params, 'pageIndex', 1)
        if limit is None:
            limit = 50
        request = self.ordered({
            'pageIndex': pageIndex,
            'pageSize': limit,
        })
        response = await self.privatePostGetTrades(self.extend(request, params))
        market = None
        if symbol is not None:
            market = self.market(symbol)
        return self.parse_trades(response['Data'], market, since, limit)

    def parse_trade(self, trade, market: Market = None) -> Trade:
        timestamp = self.parse8601(trade['TradeTimestampUtc'])
        id = self.safe_string(trade, 'TradeGuid')
        orderId = self.safe_string(trade, 'OrderGuid')
        priceString = self.safe_string_2(trade, 'Price', 'SecondaryCurrencyTradePrice')
        amountString = self.safe_string_2(trade, 'VolumeTraded', 'PrimaryCurrencyAmount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        cost = self.parse_number(Precise.string_mul(priceString, amountString))
        baseId = self.safe_string(trade, 'PrimaryCurrencyCode')
        quoteId = self.safe_string(trade, 'SecondaryCurrencyCode')
        marketId = None
        if (baseId is not None) and (quoteId is not None):
            marketId = baseId + '/' + quoteId
        symbol = self.safe_symbol(marketId, market, '/')
        side = self.safe_string(trade, 'OrderType')
        if side is not None:
            if side.find('Bid') >= 0:
                side = 'buy'
            elif side.find('Offer') >= 0:
                side = 'sell'
        return self.safe_trade({
            'id': id,
            'info': trade,
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
        }, market)

    async def fetch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Trade[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'primaryCurrencyCode': market['baseId'],
            'secondaryCurrencyCode': market['quoteId'],
            'numberOfRecentTradesToRetrieve': 50,  # max = 50
        }
        response = await self.publicGetGetRecentTrades(self.extend(request, params))
        return self.parse_trades(response['Trades'], market, since, limit)

    async def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/#/?id=fee-structure>` indexed by market symbols
        """
        await self.load_markets()
        response = await self.privatePostGetBrokerageFees(params)
        #
        #     [
        #         {
        #             "CurrencyCode": "Xbt",
        #             "Fee": 0.005
        #         }
        #         ...
        #     ]
        #
        fees = {}
        for i in range(0, len(response)):
            fee = response[i]
            currencyId = self.safe_string(fee, 'CurrencyCode')
            code = self.safe_currency_code(currencyId)
            tradingFee = self.safe_number(fee, 'Fee')
            fees[code] = {
                'info': fee,
                'fee': tradingFee,
            }
        result = {}
        for i in range(0, len(self.symbols)):
            symbol = self.symbols[i]
            market = self.market(symbol)
            fee = self.safe_value(fees, market['base'], {})
            result[symbol] = {
                'info': self.safe_value(fee, 'info'),
                'symbol': symbol,
                'maker': self.safe_number(fee, 'fee'),
                'taker': self.safe_number(fee, 'fee'),
                'percentage': True,
                'tierBased': True,
            }
        return result

    async def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float [price]: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        orderType = self.capitalize(type)
        orderType += 'Offer' if (side == 'sell') else 'Bid'
        request = self.ordered({
            'primaryCurrencyCode': market['baseId'],
            'secondaryCurrencyCode': market['quoteId'],
            'orderType': orderType,
        })
        response = None
        request['volume'] = amount
        if type == 'limit':
            request['price'] = price
            response = await self.privatePostPlaceLimitOrder(self.extend(request, params))
        else:
            response = await self.privatePostPlaceMarketOrder(self.extend(request, params))
        return self.safe_order({
            'info': response,
            'id': response['OrderGuid'],
        }, market)

    async def cancel_order(self, id: str, symbol: Str = None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        request = {
            'orderGuid': id,
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    async def fetch_deposit_address(self, code: str, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :see: https://www.independentreserve.com/features/api#GetDigitalCurrencyDepositAddress
        :param str code: unified currency code
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'primaryCurrencyCode': currency['id'],
        }
        response = await self.privatePostGetDigitalCurrencyDepositAddress(self.extend(request, params))
        #
        #    {
        #        Tag: '3307446684',
        #        DepositAddress: 'GCCQH4HACMRAD56EZZZ4TOIDQQRVNADMJ35QOFWF4B2VQGODMA2WVQ22',
        #        LastCheckedTimestampUtc: '2024-02-20T11:13:35.6912985Z',
        #        NextUpdateTimestampUtc: '2024-02-20T11:14:56.5112394Z'
        #    }
        #
        return self.parse_deposit_address(response)

    def parse_deposit_address(self, depositAddress, currency: Currency = None):
        #
        #    {
        #        Tag: '3307446684',
        #        DepositAddress: 'GCCQH4HACMRAD56EZZZ4TOIDQQRVNADMJ35QOFWF4B2VQGODMA2WVQ22',
        #        LastCheckedTimestampUtc: '2024-02-20T11:13:35.6912985Z',
        #        NextUpdateTimestampUtc: '2024-02-20T11:14:56.5112394Z'
        #    }
        #
        address = self.safe_string(depositAddress, 'DepositAddress')
        self.check_address(address)
        return {
            'info': depositAddress,
            'currency': self.safe_string(currency, 'code'),
            'address': address,
            'tag': self.safe_string(depositAddress, 'Tag'),
            'network': None,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            auth = [
                url,
                'apiKey=' + self.apiKey,
                'nonce=' + str(nonce),
            ]
            keys = list(params.keys())
            for i in range(0, len(keys)):
                key = keys[i]
                value = str(params[key])
                auth.append(key + '=' + value)
            message = ','.join(auth)
            signature = self.hmac(self.encode(message), self.encode(self.secret), hashlib.sha256)
            query = self.ordered({})
            query['apiKey'] = self.apiKey
            query['nonce'] = nonce
            query['signature'] = signature.upper()
            for i in range(0, len(keys)):
                key = keys[i]
                query[key] = params[key]
            body = self.json(query)
            headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
