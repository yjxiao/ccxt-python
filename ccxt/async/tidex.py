# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.liqui import liqui
import math


class tidex (liqui):

    def describe(self):
        return self.deep_extend(super(tidex, self).describe(), {
            'id': 'tidex',
            'name': 'Tidex',
            'countries': 'UK',
            'rateLimit': 2000,
            'version': '3',
            'has': {
                # 'CORS': False,
                # 'fetchTickers': True
                'fetchCurrencies': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/30781780-03149dc4-a12e-11e7-82bb-313b269d24d4.jpg',
                'api': {
                    'web': 'https://web.tidex.com/api',
                    'public': 'https://api.tidex.com/api/3',
                    'private': 'https://api.tidex.com/tapi',
                },
                'www': 'https://tidex.com',
                'doc': 'https://tidex.com/exchange/public-api',
                'fees': [
                    'https://tidex.com/exchange/assets-spec',
                    'https://tidex.com/exchange/pairs-spec',
                ],
            },
            'api': {
                'web': {
                    'get': [
                        'currency',
                        'pairs',
                        'tickers',
                        'orders',
                        'ordershistory',
                        'trade-data',
                        'trade-data/{id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.1 / 100,
                    'maker': 0.1 / 100,
                },
            },
            'commonCurrencies': {
                'MGO': 'WMGO',
                'EMGO': 'MGO',
            },
        })

    async def fetch_currencies(self, params={}):
        currencies = await self.webGetCurrency(params)
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['symbol']
            precision = currency['amountPoint']
            code = id.upper()
            code = self.common_currency_code(code)
            active = currency['visible'] is True
            status = 'ok'
            if not active:
                status = 'disabled'
            canWithdraw = currency['withdrawEnable'] is True
            canDeposit = currency['depositEnable'] is True
            if not canWithdraw or not canDeposit:
                active = False
            result[code] = {
                'id': id,
                'code': code,
                'name': currency['name'],
                'active': active,
                'status': status,
                'precision': precision,
                'funding': {
                    'withdraw': {
                        'active': canWithdraw,
                        'fee': currency['withdrawFee'],
                    },
                    'deposit': {
                        'active': canDeposit,
                        'fee': 0.0,
                    },
                },
                'limits': {
                    'amount': {
                        'min': None,
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['withdrawMinAmout'],
                        'max': None,
                    },
                    'deposit': {
                        'min': currency['depositMinAmount'],
                        'max': None,
                    },
                },
                'info': currency,
            }
        return result

    def get_version_string(self):
        return ''

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'nonce': nonce,
                'method': path,
            }, query))
            signature = self.sign_body_with_secret(body)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': signature,
            }
        elif api == 'public':
            url += self.get_version_string() + '/' + self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            url += '/' + self.implode_params(path, params)
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                if query:
                    body = self.urlencode(query)
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
