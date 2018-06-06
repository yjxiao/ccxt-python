# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import DDoSProtection


class coinbase (Exchange):

    def describe(self):
        return self.deep_extend(super(coinbase, self).describe(), {
            'id': 'coinbase',
            'name': 'coinbase',
            'countries': 'US',
            'rateLimit': 1000,
            'version': 'v2',
            'userAgent': self.userAgents['chrome'],
            'has': {
                'CORS': True,
                'cancelOrder': False,
                'createDepositAddress': False,
                'createOrder': False,
                'deposit': False,
                'fetchBalance': True,
                'fetchClosedOrders': False,
                'fetchCurrencies': False,
                'fetchDepositAddress': False,
                'fetchMarkets': False,
                'fetchMyTrades': False,
                'fetchOHLCV': False,
                'fetchOpenOrders': False,
                'fetchOrder': False,
                'fetchOrderBook': False,
                'fetchOrders': False,
                'fetchTicker': False,
                'fetchTickers': False,
                'fetchBidsAsks': False,
                'fetchTrades': False,
                'withdraw': False,
                'fetchTransactions': False,
                'fetchDeposits': False,
                'fetchWithdrawals': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/40811661-b6eceae2-653a-11e8-829e-10bfadb078cf.jpg',
                'api': 'https://api.coinbase.com',
                'www': 'https://www.coinbase.com',
                'doc': 'https://developers.coinbase.com/api/v2',
                'fees': 'https://support.coinbase.com/customer/portal/articles/2109597-buy-sell-bank-transfer-fees',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'time',
                        'exchange-rates',
                        'users/{user_id}',
                        'prices/{currency_pair}/buy',
                        'prices/{currency_pair}/sell',
                        'prices/{currency_pair}/spot',
                    ],
                },
                'private': {
                    'get': [
                        'accounts',
                        'accounts/{account_id}',
                        'accounts/{account_id}/addresses',
                        'accounts/{account_id}/addresses/{address_id}',
                        'accounts/{account_id}/addresses/{address_id}/transactions',
                        'accounts/{account_id}/transactions',
                        'accounts/{account_id}/transactions/{transaction_id}',
                        'accounts/{account_id}/buys',
                        'accounts/{account_id}/buys/{buy_id}',
                        'accounts/{account_id}/sells',
                        'accounts/{account_id}/sells/{sell_id}',
                        'accounts/{account_id}/deposits',
                        'accounts/{account_id}/deposits/{deposit_id}',
                        'accounts/{account_id}/withdrawals',
                        'accounts/{account_id}/withdrawals/{withdrawal_id}',
                        'payment-methods',
                        'payment-methods/{payment_method_id}',
                        'user',
                        'user/auth',
                    ],
                    'post': [
                        'accounts',
                        'accounts/{account_id}/primary',
                        'accounts/{account_id}/addresses',
                        'accounts/{account_id}/transactions',
                        'accounts/{account_id}/transactions/{transaction_id}/complete',
                        'accounts/{account_id}/transactions/{transaction_id}/resend',
                        'accounts/{account_id}/buys',
                        'accounts/{account_id}/buys/{buy_id}/commit',
                        'accounts/{account_id}/sells',
                        'accounts/{account_id}/sells/{sell_id}/commit',
                        'accounts/{account_id}/deposists',
                        'accounts/{account_id}/deposists/{deposit_id}/commit',
                        'accounts/{account_id}/withdrawals',
                        'accounts/{account_id}/withdrawals/{withdrawal_id}/commit',
                    ],
                    'put': [
                        'accounts/{account_id}',
                        'user',
                    ],
                    'delete': [
                        'accounts/{id}',
                        'accounts/{account_id}/transactions/{transaction_id}',
                    ],
                },
            },
            'exceptions': {
                'two_factor_required': AuthenticationError,  # 402 When sending money over 2fa limit
                'param_required': ExchangeError,  # 400 Missing parameter
                'validation_error': ExchangeError,  # 400 Unable to validate POST/PUT
                'invalid_request': ExchangeError,  # 400 Invalid request
                'personal_details_required': AuthenticationError,  # 400 User’s personal detail required to complete self request
                'identity_verification_required': AuthenticationError,  # 400 Identity verification is required to complete self request
                'jumio_verification_required': AuthenticationError,  # 400 Document verification is required to complete self request
                'jumio_face_match_verification_required': AuthenticationError,  # 400 Document verification including face match is required to complete self request
                'unverified_email': AuthenticationError,  # 400 User has not verified their email
                'authentication_error': AuthenticationError,  # 401 Invalid auth(generic)
                'invalid_token': AuthenticationError,  # 401 Invalid Oauth token
                'revoked_token': AuthenticationError,  # 401 Revoked Oauth token
                'expired_token': AuthenticationError,  # 401 Expired Oauth token
                'invalid_scope': AuthenticationError,  # 403 User hasn’t authenticated necessary scope
                'not_found': ExchangeError,  # 404 Resource not found
                'rate_limit_exceeded': DDoSProtection,  # 429 Rate limit exceeded
                'internal_server_error': ExchangeError,  # 500 Internal server error
            },
            'markets': {
                'BTC/USD': {'id': 'btc-usd', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD'},
                'LTC/USD': {'id': 'ltc-usd', 'symbol': 'LTC/USD', 'base': 'LTC', 'quote': 'USD'},
                'ETH/USD': {'id': 'eth-usd', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD'},
                'BCH/USD': {'id': 'bch-usd', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD'},
            },
        })

    def fetch_time(self):
        response = self.publicGetTime()
        return self.parse8601(response['data']['iso'])

    def fetch_balance(self, params={}):
        balances = self.privateGetAccounts()
        result = {'info': balances}
        for b in range(0, len(balances.data)):
            balance = balances.data[b]
            currency = balance['balance']['currency']
            account = {
                'free': self.safe_float(balance['balance'], 'amount'),
                'used': None,
                'total': self.safe_float(balance['balance'], 'amount'),
            }
            result[currency] = account
        return self.parse_balance(result)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if query:
                request += '?' + self.urlencode(query)
        url = self.urls['api'] + '/' + self.version + request
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            payload = ''
            if method != 'GET':
                if query:
                    body = self.json(query)
                    payload = body
            what = nonce + method + '/' + self.version + request + payload
            signature = self.hmac(self.encode(what), self.encode(self.secret))
            headers = {
                'CB-ACCESS-KEY': self.apiKey,
                'CB-ACCESS-SIGN': self.decode(signature),
                'CB-ACCESS-TIMESTAMP': nonce,
                'CB-VERSION': '2018-05-30',
                'Content-Type': 'application/json',
            }
        if not headers:
            headers = {
                'CB-VERSION': '2018-05-30',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            feedback = self.id + ' ' + body
            #
            #    {"error": "invalid_request", "error_description": "The request is missing a required parameter, includes an unsupported parameter value, or is otherwise malformed."}
            #
            # or
            #
            #    {
            #      "errors": [
            #        {
            #          "id": "not_found",
            #          "message": "Not found"
            #        }
            #      ]
            #    }
            #
            exceptions = self.exceptions
            errorCode = self.safe_string(response, 'error')
            if errorCode is not None:
                if errorCode in exceptions:
                    raise exceptions[errorCode](feedback)
                else:
                    raise ExchangeError(feedback)
            errors = self.safe_value(response, 'errors')
            if errors is not None:
                if isinstance(errors, list):
                    numErrors = len(errors)
                    if numErrors > 0:
                        errorCode = self.safe_string(errors[0], 'id')
                        if errorCode is not None:
                            if errorCode in exceptions:
                                raise exceptions[errorCode](feedback)
                            else:
                                raise ExchangeError(feedback)
