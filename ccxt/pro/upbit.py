# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache
from ccxt.async_support.base.ws.client import Client
from typing import Optional


class upbit(ccxt.async_support.upbit):

    def describe(self):
        return self.deep_extend(super(upbit, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api.upbit.com/websocket/v1',
                },
            },
            'options': {
                'tradesLimit': 1000,
            },
        })

    async def watch_public(self, symbol: str, channel, params={}):
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        marketId = market['id']
        url = self.urls['api']['ws']
        self.options[channel] = self.safe_value(self.options, channel, {})
        self.options[channel][symbol] = True
        symbols = list(self.options[channel].keys())
        marketIds = self.market_ids(symbols)
        request = [
            {
                'ticket': self.uuid(),
            },
            {
                'type': channel,
                'codes': marketIds,
                # 'isOnlySnapshot': False,
                # 'isOnlyRealtime': False,
            },
        ]
        messageHash = channel + ':' + marketId
        return await self.watch(url, messageHash, request, messageHash)

    async def watch_ticker(self, symbol: str, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the upbit api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        return await self.watch_public(symbol, 'ticker')

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the upbit api endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        symbol = self.symbol(symbol)
        trades = await self.watch_public(symbol, 'trade')
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the upbit api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        orderbook = await self.watch_public(symbol, 'orderbook')
        return orderbook.limit()

    def handle_ticker(self, client: Client, message):
        # 2020-03-17T23:07:36.511Z 'onMessage' <Buffer 7b 22 74 79 70 65 22 3a 22 74 69 63 6b 65 72 22 2c 22 63 6f 64 65 22 3a 22 42 54 43 2d 45 54 48 22 2c 22 6f 70 65 6e 69 6e 67 5f 70 72 69 63 65 22 3a ... >
        # {type: 'ticker',
        #   code: 'BTC-ETH',
        #   opening_price: 0.02295092,
        #   high_price: 0.02295092,
        #   low_price: 0.02161249,
        #   trade_price: 0.02161249,
        #   prev_closing_price: 0.02185802,
        #   acc_trade_price: 2.32732482,
        #   change: 'FALL',
        #   change_price: 0.00024553,
        #   signed_change_price: -0.00024553,
        #   change_rate: 0.0112329479,
        #   signed_change_rate: -0.0112329479,
        #   ask_bid: 'ASK',
        #   trade_volume: 2.12,
        #   acc_trade_volume: 106.11798418,
        #   trade_date: '20200317',
        #   trade_time: '215843',
        #   trade_timestamp: 1584482323000,
        #   acc_ask_volume: 90.16935908,
        #   acc_bid_volume: 15.9486251,
        #   highest_52_week_price: 0.03537414,
        #   highest_52_week_date: '2019-04-08',
        #   lowest_52_week_price: 0.01614901,
        #   lowest_52_week_date: '2019-09-06',
        #   trade_status: null,
        #   market_state: 'ACTIVE',
        #   market_state_for_ios: null,
        #   is_trading_suspended: False,
        #   delisting_date: null,
        #   market_warning: 'NONE',
        #   timestamp: 1584482323378,
        #   acc_trade_price_24h: 2.5955306323568927,
        #   acc_trade_volume_24h: 118.38798416,
        #   stream_type: 'SNAPSHOT'}
        marketId = self.safe_string(message, 'code')
        messageHash = 'ticker:' + marketId
        ticker = self.parse_ticker(message)
        symbol = ticker['symbol']
        self.tickers[symbol] = ticker
        client.resolve(ticker, messageHash)

    def handle_order_book(self, client: Client, message):
        # {type: 'orderbook',
        #   code: 'BTC-ETH',
        #   timestamp: 1584486737444,
        #   total_ask_size: 16.76384456,
        #   total_bid_size: 168.9020623,
        #   orderbook_units:
        #    [{ask_price: 0.02295077,
        #        bid_price: 0.02161249,
        #        ask_size: 3.57100696,
        #        bid_size: 22.5303265},
        #      {ask_price: 0.02295078,
        #        bid_price: 0.02152658,
        #        ask_size: 0.52451651,
        #        bid_size: 2.30355128},
        #      {ask_price: 0.02295086,
        #        bid_price: 0.02150802,
        #        ask_size: 1.585,
        #        bid_size: 5}, ...],
        #   stream_type: 'SNAPSHOT'}
        marketId = self.safe_string(message, 'code')
        symbol = self.safe_symbol(marketId, None, '-')
        type = self.safe_string(message, 'stream_type')
        options = self.safe_value(self.options, 'watchOrderBook', {})
        limit = self.safe_integer(options, 'limit', 15)
        if type == 'SNAPSHOT':
            self.orderbooks[symbol] = self.order_book({}, limit)
        orderBook = self.orderbooks[symbol]
        # upbit always returns a snapshot of 15 topmost entries
        # the "REALTIME" deltas are not incremental
        # therefore we reset the orderbook on each update
        # and reinitialize it again with new bidasks
        orderBook.reset({})
        orderBook['symbol'] = symbol
        bids = orderBook['bids']
        asks = orderBook['asks']
        data = self.safe_value(message, 'orderbook_units', [])
        for i in range(0, len(data)):
            entry = data[i]
            ask_price = self.safe_float(entry, 'ask_price')
            ask_size = self.safe_float(entry, 'ask_size')
            bid_price = self.safe_float(entry, 'bid_price')
            bid_size = self.safe_float(entry, 'bid_size')
            asks.store(ask_price, ask_size)
            bids.store(bid_price, bid_size)
        timestamp = self.safe_integer(message, 'timestamp')
        datetime = self.iso8601(timestamp)
        orderBook['timestamp'] = timestamp
        orderBook['datetime'] = datetime
        messageHash = 'orderbook:' + marketId
        client.resolve(orderBook, messageHash)

    def handle_trades(self, client: Client, message):
        # {type: 'trade',
        #   code: 'KRW-BTC',
        #   timestamp: 1584508285812,
        #   trade_date: '2020-03-18',
        #   trade_time: '05:11:25',
        #   trade_timestamp: 1584508285000,
        #   trade_price: 6747000,
        #   trade_volume: 0.06499468,
        #   ask_bid: 'ASK',
        #   prev_closing_price: 6774000,
        #   change: 'FALL',
        #   change_price: 27000,
        #   sequential_id: 1584508285000002,
        #   stream_type: 'REALTIME'}
        trade = self.parse_trade(message)
        symbol = trade['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        stored.append(trade)
        marketId = self.safe_string(message, 'code')
        messageHash = 'trade:' + marketId
        client.resolve(stored, messageHash)

    def handle_message(self, client: Client, message):
        methods = {
            'ticker': self.handle_ticker,
            'orderbook': self.handle_order_book,
            'trade': self.handle_trades,
        }
        methodName = self.safe_string(message, 'type')
        method = self.safe_value(methods, methodName)
        if method:
            method(client, message)
