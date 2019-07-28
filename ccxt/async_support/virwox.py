# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class virwox (Exchange):

    def describe(self):
        return self.deep_extend(super(virwox, self).describe(), {
            'id': 'virwox',
            'name': 'VirWoX',
            'countries': ['AT', 'EU'],
            'rateLimit': 1000,
            'has': {
                'CORS': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766894-6da9d360-5eea-11e7-90aa-41f2711b7405.jpg',
                'api': {
                    'public': 'https://api.virwox.com/api/json.php',
                    'private': 'https://www.virwox.com/api/trading.php',
                },
                'www': 'https://www.virwox.com',
                'doc': 'https://www.virwox.com/developers.php',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
                'login': True,
                'password': True,
            },
            'api': {
                'public': {
                    'get': [
                        'getInstruments',
                        'getBestPrices',
                        'getMarketDepth',
                        'estimateMarketOrder',
                        'getTradedPriceVolume',
                        'getRawTradeData',
                        'getStatistics',
                        'getTerminalList',
                        'getGridList',
                        'getGridStatistics',
                    ],
                    'post': [
                        'getInstruments',
                        'getBestPrices',
                        'getMarketDepth',
                        'estimateMarketOrder',
                        'getTradedPriceVolume',
                        'getRawTradeData',
                        'getStatistics',
                        'getTerminalList',
                        'getGridList',
                        'getGridStatistics',
                    ],
                },
                'private': {
                    'get': [
                        'cancelOrder',
                        'getBalances',
                        'getCommissionDiscount',
                        'getOrders',
                        'getTransactions',
                        'placeOrder',
                    ],
                    'post': [
                        'cancelOrder',
                        'getBalances',
                        'getCommissionDiscount',
                        'getOrders',
                        'getTransactions',
                        'placeOrder',
                    ],
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetGetInstruments(params)
        markets = self.safe_value(response, 'result')
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            key = keys[i]
            market = self.safe_value(markets, key, {})
            id = self.safe_string(market, 'instrumentID')
            baseId = self.safe_string(market, 'longCurrency')
            quoteId = self.safe_string(market, 'shortCurrency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostGetBalances(params)
        balances = self.safe_value(response['result'], 'accountList')
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_float(balance, 'balance')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_market_price(self, symbol, params={}):
        await self.load_markets()
        request = {
            'symbols': [symbol],
        }
        response = await self.publicPostGetBestPrices(self.extend(request, params))
        result = self.safe_value(response, 'result')
        return {
            'bid': self.safe_float(result[0], 'bestBuyPrice'),
            'ask': self.safe_float(result[0], 'bestSellPrice'),
        }

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbols': [symbol],
        }
        if limit is not None:
            request['buyDepth'] = limit  # 100
            request['sellDepth'] = limit  # 100
        response = await self.publicPostGetMarketDepth(self.extend(request, params))
        orderbook = response['result'][0]
        return self.parse_order_book(orderbook, None, 'buy', 'sell', 'price', 'volume')

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        end = self.milliseconds()
        start = end - 86400000
        request = {
            'instrument': symbol,
            'endDate': self.ymdhms(end),
            'startDate': self.ymdhms(start),
            'HLOC': 1,
        }
        response = await self.publicGetGetTradedPriceVolume(self.extend(request, params))
        tickers = self.safe_value(response['result'], 'priceVolumeList')
        keys = list(tickers.keys())
        length = len(keys)
        lastKey = keys[length - 1]
        ticker = self.safe_value(tickers, lastKey)
        timestamp = self.milliseconds()
        close = self.safe_float(ticker, 'close')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': close,
            'last': close,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'longVolume'),
            'quoteVolume': self.safe_float(ticker, 'shortVolume'),
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'time')
        if timestamp is not None:
            timestamp *= 1000
        id = self.safe_string(trade, 'tid')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'vol')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'order': None,
            'symbol': symbol,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
            'info': trade,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'instrument': symbol,
            'timespan': 3600,
        }
        response = await self.publicGetGetRawTradeData(self.extend(request, params))
        result = self.safe_value(response, 'result', {})
        trades = self.safe_value(result, 'data', [])
        return self.parse_trades(trades, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'instrument': market['symbol'],
            'orderType': side.upper(),
            'amount': amount,
        }
        if type == 'limit':
            request['price'] = price
        response = await self.privatePostPlaceOrder(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response['result'], 'orderID'),
        }

    async def cancel_order(self, id, symbol=None, params={}):
        request = {
            'orderID': id,
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        auth = {}
        if api == 'private':
            self.check_required_credentials()
            auth['key'] = self.apiKey
            auth['user'] = self.login
            auth['pass'] = self.password
        nonce = self.nonce()
        if method == 'GET':
            url += '?' + self.urlencode(self.extend({
                'method': path,
                'id': nonce,
            }, auth, params))
        else:
            headers = {'Content-Type': 'application/json'}
            body = self.json({
                'method': path,
                'params': self.extend(auth, params),
                'id': nonce,
            })
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if code == 200:
            if (body[0] == '{') or (body[0] == '['):
                if 'result' in response:
                    result = response['result']
                    if 'errorCode' in result:
                        errorCode = result['errorCode']
                        if errorCode != 'OK':
                            raise ExchangeError(self.id + ' error returned: ' + body)
                else:
                    raise ExchangeError(self.id + ' malformed response: no result in response: ' + body)
            else:
                # if not a JSON response
                raise ExchangeError(self.id + ' returned a non-JSON reply: ' + body)
