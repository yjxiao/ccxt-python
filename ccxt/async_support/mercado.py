# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired


class mercado (Exchange):

    def describe(self):
        return self.deep_extend(super(mercado, self).describe(), {
            'id': 'mercado',
            'name': 'Mercado Bitcoin',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'version': 'v3',
            'has': {
                'CORS': True,
                'createMarketOrder': True,
                'fetchOrder': True,
                'withdraw': True,
                'fetchOHLCV': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchTicker': True,
                'fetchTickers': True,
            },
            'timeframes': {
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '2w': '2w',
            },
            'timeframesMilliseconds': {
                '5m': 300,
                '15m': 900,
                '30m': 1800,
                '1h': 3600,
                '6h': 21600,
                '1d': 86400,
                '3d': 64800,
                '1w': 604800,
                '2w': 1209600,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27837060-e7c58714-60ea-11e7-9192-f05e86adb83f.jpg',
                'api': {
                    'public': 'https://www.mercadobitcoin.net/api',
                    'private': 'https://www.mercadobitcoin.net/tapi',
                    'v4Public': 'https://www.mercadobitcoin.com.br/v4',
                },
                'www': 'https://www.mercadobitcoin.com.br',
                'doc': [
                    'https://www.mercadobitcoin.com.br/api-doc',
                    'https://www.mercadobitcoin.com.br/trade-api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        '{coin}/orderbook/',  # last slash critical
                        '{coin}/ticker/',
                        '{coin}/trades/',
                        '{coin}/trades/{from}/',
                        '{coin}/trades/{from}/{to}',
                        '{coin}/day-summary/{year}/{month}/{day}/',
                    ],
                },
                'private': {
                    'post': [
                        'cancel_order',
                        'get_account_info',
                        'get_order',
                        'get_withdrawal',
                        'list_system_messages',
                        'list_orders',
                        'list_orderbook',
                        'place_buy_order',
                        'place_sell_order',
                        'place_market_buy_order',
                        'place_market_sell_order',
                        'withdraw_coin',
                    ],
                },
                'v4Public': {
                    'get': [
                        '{coin}/candle/',
                    ],
                },
            },
            'markets': {
                'BTC/BRL': {'id': 'BRLBTC', 'symbol': 'BTC/BRL', 'base': 'BTC', 'quote': 'BRL', 'suffix': 'Bitcoin'},
                'LTC/BRL': {'id': 'BRLLTC', 'symbol': 'LTC/BRL', 'base': 'LTC', 'quote': 'BRL', 'suffix': 'Litecoin'},
                'BCH/BRL': {'id': 'BRLBCH', 'symbol': 'BCH/BRL', 'base': 'BCH', 'quote': 'BRL', 'suffix': 'BCash'},
                'XRP/BRL': {'id': 'BRLXRP', 'symbol': 'XRP/BRL', 'base': 'XRP', 'quote': 'BRL', 'suffix': 'Ripple'},
                'ETH/BRL': {'id': 'BRLETH', 'symbol': 'ETH/BRL', 'base': 'ETH', 'quote': 'BRL', 'suffix': 'Ethereum'},
            },
            'tickers': [
                'BTC/BRL',
                'LTC/BRL',
                'BCH/BRL',
                'XRP/BRL',
                'ETH/BRL',
            ],
            'fees': {
                'trading': {
                    'maker': 0.3 / 100,
                    'taker': 0.7 / 100,
                },
            },
        })

    async def fetch_order_book(self, symbol, limit=None, params={}):
        market = self.market(symbol)
        orderbook = await self.publicGetCoinOrderbook(self.extend({
            'coin': market['base'],
        }, params))
        return self.parse_order_book(orderbook)

    async def fetch_ticker(self, symbol, params={}):
        market = self.market(symbol)
        response = await self.publicGetCoinTicker(self.extend({
            'coin': market['base'],
        }, params))
        ticker = response['ticker']
        timestamp = int(ticker['date']) * 1000
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = trade['date'] * 1000
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': str(trade['tid']),
            'order': None,
            'type': None,
            'side': trade['type'],
            'price': trade['price'],
            'amount': trade['amount'],
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        method = 'publicGetCoinTrades'
        request = {
            'coin': market['base'],
        }
        if since is not None:
            method += 'From'
            request['from'] = int(since / 1000)
        to = self.safe_integer(params, 'to')
        if to is not None:
            method += 'To'
        response = await getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_balance(self, params={}):
        response = await self.privatePostGetAccountInfo()
        balances = response['response_data']['balance']
        result = {'info': response}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            lowercase = currency.lower()
            account = self.account()
            if lowercase in balances:
                account['free'] = float(balances[lowercase]['available'])
                account['total'] = float(balances[lowercase]['total'])
                account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        order = {
            'coin_pair': self.market_id(symbol),
        }
        method = 'privatePostPlace' + self.capitalize(side) + 'Order'
        if type == 'limit':
            order['limit_price'] = price
            order['quantity'] = amount
        else:
            method = 'privatePostPlaceMarket' + self.capitalize(side) + 'Order'
            if side == 'buy':
                order['cost'] = (amount * '{:.5f}'.format(price))
            else:
                order['quantity'] = amount
        response = await getattr(self, method)(self.extend(order, params))
        return {
            'info': response,
            'id': str(response['response_data']['order']['order_id']),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = await self.privatePostCancelOrder(self.extend({
            'coin_pair': market['id'],
            'order_id': id,
        }, params))
        return self.parse_order(response['response_data']['order'], market)

    def parse_order_status(self, status):
        statuses = {
            '2': 'open',
            '3': 'canceled',
            '4': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'order_id')
        side = None
        if 'order_type' in order:
            side = 'buy' if (order['order_type'] == 1) else 'sell'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'coin_pair')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'created_timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
        fee = {
            'cost': self.safe_float(order, 'fee'),
            'currency': market['quote'],
        }
        price = self.safe_float(order, 'limit_price')
        # price = self.safe_float(order, 'executed_price_avg', price)
        average = self.safe_float(order, 'executed_price_avg')
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'executed_quantity')
        remaining = amount - filled
        cost = amount * average
        lastTradeTimestamp = self.safe_integer(order, 'updated_timestamp')
        if lastTradeTimestamp is not None:
            lastTradeTimestamp = lastTradeTimestamp * 1000
        result = {
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
            'trades': None,  # todo parse trades(operations)
        }
        return result

    async def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = None
        response = await self.privatePostGetOrder(self.extend({
            'coin_pair': market['id'],
            'order_id': int(id),
        }, params))
        return self.parse_order(response['response_data']['order'])

    async def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        await self.load_markets()
        currency = self.currency(code)
        request = {
            'coin': currency['id'],
            'quantity': '{:.10f}'.format(amount),
            'address': address,
        }
        if code == 'BRL':
            account_ref = ('account_ref' in list(params.keys()))
            if not account_ref:
                raise ExchangeError(self.id + ' requires account_ref parameter to withdraw ' + code)
        elif code != 'LTC':
            tx_fee = ('tx_fee' in list(params.keys()))
            if not tx_fee:
                raise ExchangeError(self.id + ' requires tx_fee parameter to withdraw ' + code)
            if code == 'XRP':
                if tag is None:
                    if not('destination_tag' in list(params.keys())):
                        raise ExchangeError(self.id + ' requires a tag argument or destination_tag parameter to withdraw ' + code)
                else:
                    request['destination_tag'] = tag
        response = await self.privatePostWithdrawCoin(self.extend(request, params))
        return {
            'info': response,
            'id': response['response_data']['withdrawal']['id'],
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv.timestamp * 1000,
            float(ohlcv.open),
            float(ohlcv.high),
            float(ohlcv.low),
            float(ohlcv.close),
            float(ohlcv.volume),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'precision': self.timeframes[timeframe],
            'coin': market.id.lower(),
        }
        if since is not None:
            request['from'] = int(since / 1000)
            if limit is not None:
                request['to'] = (self.sum(request['from'], limit * self.timeframesMilliseconds[timeframe]))
            else:
                request['to'] = self.sum(self.seconds(), 1)
        response = await self.v4PublicGetCoinCandle(self.extend(request, params))
        return self.parse_ohlcvs(response.candles, market, timeframe, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        response = None
        response = await self.privatePostListOrders(self.extend({
            'coin_pair': market['base']
        }, params))
        orders = response['response_data']['orders']
        for i in range(0, len(orders)):
            orders[i] = self.parse_order(orders[i])
        return orders

    async def fetch_tickers(self, symbols=None, params={}):
        tickers = {}
        for i in range(0, len(self.tickers)):
            ticker = self.tickers[i]
            tickers[ticker] = await self.fetch_ticker(ticker)
        return tickers

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or (api == 'v4Public'):
            url += self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/'
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'tapi_method': path,
                'tapi_nonce': nonce,
            }, params))
            auth = '/tapi/' + self.version + '/' + '?' + body
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'TAPI-ID': self.apiKey,
                'TAPI-MAC': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if 'error_message' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
