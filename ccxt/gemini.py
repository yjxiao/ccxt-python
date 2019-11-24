# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import base64
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import OnMaintenance
from ccxt.base.errors import InvalidNonce


class gemini(Exchange):

    def describe(self):
        return self.deep_extend(super(gemini, self).describe(), {
            'id': 'gemini',
            'name': 'Gemini',
            'countries': ['US'],
            'rateLimit': 1500,  # 200 for private API
            'version': 'v1',
            'has': {
                'fetchDepositAddress': False,
                'createDepositAddress': True,
                'CORS': False,
                'fetchBidsAsks': False,
                'fetchTickers': False,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': False,
                'createMarketOrder': False,
                'withdraw': True,
                'fetchTransactions': True,
                'fetchWithdrawals': False,
                'fetchDeposits': False,
                'fetchOHLCV': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27816857-ce7be644-6096-11e7-82d6-3c257263229c.jpg',
                'api': {
                    'public': 'https://api.gemini.com',
                    'private': 'https://api.gemini.com',
                    'web': 'https://docs.gemini.com',
                },
                'www': 'https://gemini.com/',
                'doc': [
                    'https://docs.gemini.com/rest-api',
                    'https://docs.sandbox.gemini.com',
                ],
                'test': 'https://api.sandbox.gemini.com',
                'fees': [
                    'https://gemini.com/api-fee-schedule',
                    'https://gemini.com/trading-fees',
                    'https://gemini.com/transfer-fees',
                ],
            },
            'api': {
                'web': {
                    'get': [
                        'rest-api',
                    ],
                },
                'public': {
                    'get': [
                        'v1/symbols',
                        'v1/pubticker/{symbol}',
                        'v1/book/{symbol}',
                        'v1/trades/{symbol}',
                        'v1/auction/{symbol}',
                        'v1/auction/{symbol}/history',
                        'v2/candles/{symbol}/{timeframe}',
                        'v2/ticker/{symbol}',
                    ],
                },
                'private': {
                    'post': [
                        'v1/order/new',
                        'v1/order/cancel',
                        'v1/order/cancel/session',
                        'v1/order/cancel/all',
                        'v1/order/status',
                        'v1/orders',
                        'v1/mytrades',
                        'v1/tradevolume',
                        'v1/transfers',
                        'v1/balances',
                        'v1/deposit/{currency}/newAddress',
                        'v1/withdraw/{currency}',
                        'v1/heartbeat',
                        'v1/transfers',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'taker': 0.0035,
                    'maker': 0.001,
                },
            },
            'httpExceptions': {
                '400': BadRequest,  # Auction not open or paused, ineligible timing, market not open, or the request was malformed, in the case of a private API request, missing or malformed Gemini private API authentication headers
                '403': PermissionDenied,  # The API key is missing the role necessary to access self private API endpoint
                '404': OrderNotFound,  # Unknown API entry point or Order not found
                '406': InsufficientFunds,  # Insufficient Funds
                '429': DDoSProtection,  # Rate Limiting was applied
                '500': ExchangeError,  # The server encountered an error
                '502': ExchangeError,  # Technical issues are preventing the request from being satisfied
                '503': ExchangeNotAvailable,  # The exchange is down for maintenance
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1hr',
                '6h': '6hr',
                '1d': '1day',
            },
            'exceptions': {
                'exact': {
                    'AuctionNotOpen': BadRequest,  # Failed to place an auction-only order because there is no current auction open for self symbol
                    'ClientOrderIdTooLong': BadRequest,  # The Client Order ID must be under 100 characters
                    'ClientOrderIdMustBeString': BadRequest,  # The Client Order ID must be a string
                    'ConflictingOptions': BadRequest,  # New orders using a combination of order execution options are not supported
                    'EndpointMismatch': BadRequest,  # The request was submitted to an endpoint different than the one in the payload
                    'EndpointNotFound': BadRequest,  # No endpoint was specified
                    'IneligibleTiming': BadRequest,  # Failed to place an auction order for the current auction on self symbol because the timing is not eligible, new orders may only be placed before the auction begins.
                    'InsufficientFunds': InsufficientFunds,  # The order was rejected because of insufficient funds
                    'InvalidJson': BadRequest,  # The JSON provided is invalid
                    'InvalidNonce': InvalidNonce,  # The nonce was not greater than the previously used nonce, or was not present
                    'InvalidOrderType': InvalidOrder,  # An unknown order type was provided
                    'InvalidPrice': InvalidOrder,  # For new orders, the price was invalid
                    'InvalidQuantity': InvalidOrder,  # A negative or otherwise invalid quantity was specified
                    'InvalidSide': InvalidOrder,  # For new orders, and invalid side was specified
                    'InvalidSignature': AuthenticationError,  # The signature did not match the expected signature
                    'InvalidSymbol': BadRequest,  # An invalid symbol was specified
                    'InvalidTimestampInPayload': BadRequest,  # The JSON payload contained a timestamp parameter with an unsupported value.
                    'Maintenance': ExchangeNotAvailable,  # The system is down for maintenance
                    'MarketNotOpen': InvalidOrder,  # The order was rejected because the market is not accepting new orders
                    'MissingApikeyHeader': AuthenticationError,  # The X-GEMINI-APIKEY header was missing
                    'MissingOrderField': InvalidOrder,  # A required order_id field was not specified
                    'MissingRole': AuthenticationError,  # The API key used to access self endpoint does not have the required role assigned to it
                    'MissingPayloadHeader': AuthenticationError,  # The X-GEMINI-PAYLOAD header was missing
                    'MissingSignatureHeader': AuthenticationError,  # The X-GEMINI-SIGNATURE header was missing
                    'NoSSL': AuthenticationError,  # You must use HTTPS to access the API
                    'OptionsMustBeArray': BadRequest,  # The options parameter must be an array.
                    'OrderNotFound': OrderNotFound,  # The order specified was not found
                    'RateLimit': DDoSProtection,  # Requests were made too frequently. See Rate Limits below.
                    'System': ExchangeError,  # We are experiencing technical issues
                    'UnsupportedOption': BadRequest,  # This order execution option is not supported.
                },
                'broad': {
                    'The Gemini Exchange is currently undergoing maintenance.': OnMaintenance,  # The Gemini Exchange is currently undergoing maintenance. Please check https://status.gemini.com/ for more information.
                },
            },
            'options': {
                'fetchMarketsMethod': 'fetch_markets_from_web',
            },
        })

    def fetch_markets(self, params={}):
        method = self.safe_value(self.options, 'fetchMarketsMethod', 'fetch_markets_from_api')
        return getattr(self, method)(params)

    def fetch_markets_from_web(self, symbols=None, params={}):
        response = self.webGetRestApi(params)
        sections = response.split('<h1 id="symbols-and-minimums">Symbols and minimums</h1>')
        numSections = len(sections)
        error = self.id + ' the ' + self.name + ' API doc HTML markup has changed, breaking the parser of order limits and precision info for ' + self.name + ' markets.'
        if numSections != 2:
            raise NotSupported(error)
        tables = sections[1].split('tbody>')
        numTables = len(tables)
        if numTables < 2:
            raise NotSupported(error)
        # tables[1] = tables[1].replace("\n", '')  # eslint-disable-line quotes
        rows = tables[1].split("<tr>\n")  # eslint-disable-line quotes
        numRows = len(rows)
        if numRows < 2:
            raise NotSupported(error)
        result = []
        # skip the first element(empty string)
        for i in range(1, numRows):
            row = rows[i]
            cells = row.split("</td>\n")  # eslint-disable-line quotes
            numCells = len(cells)
            if numCells < 7:
                raise NotSupported(error)
            #
            #     [
            #         '<td><code class="prettyprint">btcusd</code>',
            #         '<td>USD',  # quote
            #         '<td>BTC',  # base
            #         '<td>0.00001 BTC(1e-5)',  # min amount
            #         '<td>0.00000001 BTC(1e-8)',  # amount min tick size
            #         '<td>0.01 USD',  # price min tick size
            #         '</tr>\n'
            #     ]
            #
            id = cells[0].replace('<td>', '')
            id = id.replace('<code class="prettyprint">', '')
            id = id.replace('</code>', '')
            baseId = cells[2].replace('<td>', '')
            quoteId = cells[1].replace('<td>', '')
            minAmountAsString = cells[3].replace('<td>', '')
            amountTickSizeAsString = cells[4].replace('<td>', '')
            priceTickSizeAsString = cells[5].replace('<td>', '')
            minAmount = minAmountAsString.split(' ')
            amountPrecision = amountTickSizeAsString.split(' ')
            pricePrecision = priceTickSizeAsString.split(' ')
            baseId = baseId.lower()
            quoteId = quoteId.lower()
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.precision_from_string(amountPrecision[0]),
                'price': self.precision_from_string(pricePrecision[0]),
            }
            active = None
            result.append({
                'id': id,
                'info': row,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': float(minAmount[0]),
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
            })
        return result

    def fetch_markets_from_api(self, params={}):
        response = self.publicGetV1Symbols(params)
        result = []
        for i in range(0, len(response)):
            id = response[i]
            market = id
            baseId = id[0:3]
            quoteId = id[3:6]
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': None,
                'price': None,
            }
            result.append({
                'id': id,
                'info': market,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'limits': {
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
                },
            })
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['limit_bids'] = limit
            request['limit_asks'] = limit
        response = self.publicGetV1BookSymbol(self.extend(request, params))
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'amount')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        ticker = self.publicGetV1PubtickerSymbol(self.extend(request, params))
        timestamp = self.safe_integer(ticker['volume'], 'timestamp')
        baseCurrency = market['base']  # unified structures are guaranteed to have unified fields
        quoteCurrency = market['quote']  # so we don't need safe-methods for unified structures
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': None,
            'low': None,
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker['volume'], baseCurrency),
            'quoteVolume': self.safe_float(ticker['volume'], quoteCurrency),
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'timestampms')
        id = self.safe_string(trade, 'tid')
        orderId = self.safe_string(trade, 'order_id')
        feeCurrencyId = self.safe_string(trade, 'fee_currency')
        feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
        fee = {
            'cost': self.safe_float(trade, 'fee_amount'),
            'currency': feeCurrencyCode,
        }
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        type = None
        side = self.safe_string_lower(trade, 'type')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': id,
            'order': orderId,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'cost': cost,
            'amount': amount,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetV1TradesSymbol(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostV1Balances(params)
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(balance, 'available')
            account['total'] = self.safe_float(balance, 'amount')
            result[code] = account
        return self.parse_balance(result)

    def parse_order(self, order, market=None):
        timestamp = self.safe_integer(order, 'timestampms')
        amount = self.safe_float(order, 'original_amount')
        remaining = self.safe_float(order, 'remaining_amount')
        filled = self.safe_float(order, 'executed_amount')
        status = 'closed'
        if order['is_live']:
            status = 'open'
        if order['is_cancelled']:
            status = 'canceled'
        price = self.safe_float(order, 'price')
        average = self.safe_float(order, 'avg_execution_price')
        cost = None
        if filled is not None:
            if average is not None:
                cost = filled * average
        type = self.safe_string(order, 'type')
        if type == 'exchange limit':
            type = 'limit'
        elif type == 'market buy' or type == 'market sell':
            type = 'market'
        else:
            type = order['type']
        fee = None
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'symbol')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(order, 'order_id')
        side = self.safe_string_lower(order, 'side')
        return {
            'id': id,
            'info': order,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'average': average,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': fee,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': id,
        }
        response = self.privatePostV1OrderStatus(self.extend(request, params))
        return self.parse_order(response)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.privatePostV1Orders(params)
        orders = self.parse_orders(response, None, since, limit)
        if symbol is not None:
            market = self.market(symbol)  # throws on non-existent symbol
            orders = self.filter_by_symbol(orders, market['symbol'])
        return orders

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        nonce = self.nonce()
        request = {
            'client_order_id': str(nonce),
            'symbol': self.market_id(symbol),
            'amount': str(amount),
            'price': str(price),
            'side': side,
            'type': 'exchange limit',  # gemini allows limit orders only
        }
        response = self.privatePostV1OrderNew(self.extend(request, params))
        return {
            'info': response,
            'id': response['order_id'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': id,
        }
        return self.privatePostV1OrderCancel(self.extend(request, params))

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit_trades'] = limit
        if since is not None:
            request['timestamp'] = int(since / 1000)
        response = self.privatePostV1Mytrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'amount': amount,
            'address': address,
        }
        response = self.privatePostV1WithdrawCurrency(self.extend(request, params))
        return {
            'info': response,
            'id': self.safe_string(response, 'txHash'),
        }

    def nonce(self):
        return self.milliseconds()

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit_transfers'] = limit
        if since is not None:
            request['timestamp'] = since
        response = self.privatePostV1Transfers(self.extend(request, params))
        return self.parse_transactions(response)

    def parse_transaction(self, transaction, currency=None):
        timestamp = self.safe_integer(transaction, 'timestampms')
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        address = self.safe_string(transaction, 'destination')
        type = self.safe_string_lower(transaction, 'type')
        status = 'pending'
        # When deposits show as Advanced or Complete they are available for trading.
        if transaction['status']:
            status = 'ok'
        fee = None
        feeAmount = self.safe_float(transaction, 'feeAmount')
        if feeAmount is not None:
            fee = {
                'cost': feeAmount,
                'currency': code,
            }
        return {
            'info': transaction,
            'id': self.safe_string(transaction, 'eid'),
            'txid': self.safe_string(transaction, 'txHash'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': None,  # or is it defined?
            'type': type,  # direction of the transaction,('deposit' | 'withdraw')
            'amount': self.safe_float(transaction, 'amount'),
            'currency': code,
            'status': status,
            'updated': None,
            'fee': fee,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            request = self.extend({
                'request': url,
                'nonce': nonce,
            }, query)
            payload = self.json(request)
            payload = base64.b64encode(self.encode(payload))
            signature = self.hmac(payload, self.encode(self.secret), hashlib.sha384)
            headers = {
                'Content-Type': 'text/plain',
                'X-GEMINI-APIKEY': self.apiKey,
                'X-GEMINI-PAYLOAD': self.decode(payload),
                'X-GEMINI-SIGNATURE': signature,
            }
        else:
            if query:
                url += '?' + self.urlencode(query)
        url = self.urls['api'][api] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            if isinstance(body, basestring):
                feedback = self.id + ' ' + body
                self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
            return  # fallback to default error handler
        #
        #     {
        #         "result": "error",
        #         "reason": "BadNonce",
        #         "message": "Out-of-sequence nonce <1234> precedes previously used nonce <2345>"
        #     }
        #
        result = self.safe_string(response, 'result')
        if result == 'error':
            reason = self.safe_string(response, 'reason')
            message = self.safe_string(response, 'message')
            feedback = self.id + ' ' + message
            exact = self.exceptions['exact']
            if reason in exact:
                raise exact[reason](feedback)
            elif message in exact:
                raise exact[message](feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
            raise ExchangeError(feedback)  # unknown message

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privatePostV1DepositCurrencyNewAddress(self.extend(request, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response,
        }

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'timeframe': self.timeframes[timeframe],
            'symbol': market['id'],
        }
        response = self.publicGetV2CandlesSymbolTimeframe(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)
