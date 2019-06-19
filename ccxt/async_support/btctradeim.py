# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.coinegg import coinegg
from ccxt.base.errors import ExchangeError


class btctradeim (coinegg):

    def describe(self):
        result = self.deep_extend(super(btctradeim, self).describe(), {
            'id': 'btctradeim',
            'name': 'BtcTrade.im',
            'countries': ['HK'],
            'urls': {
                'referral': 'https://m.baobi.com/invite?inv=1765b2',
                'logo': 'https://user-images.githubusercontent.com/1294454/36770531-c2142444-1c5b-11e8-91e2-a4d90dc85fe8.jpg',
                'api': {
                    'web': 'https://api.btctrade.im/coin',
                    'rest': 'https://api.btctrade.im/api/v1',
                },
                'www': 'https://www.btctrade.im',
                'doc': 'https://www.btctrade.im/help.api.html',
                'fees': 'https://www.btctrade.im/spend.price.html',
            },
            'fees': {
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.001,
                    },
                },
            },
            # see the fix below
            #     'options': {
            #         'quoteIds': ['btc', 'eth', 'usc'],
            #     },
        })
        # a fix for PHP array_merge not overwriting "lists"(integer-indexed arrays)
        # https://github.com/ccxt/ccxt/issues/3343
        result['options']['quoteIds'] = ['btc', 'eth', 'usc']
        return result

    async def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = await self.fetch2(path, api, method, params, headers, body)
        if api == 'web':
            return response
        data = self.safe_value(response, 'data')
        if data:
            code = self.safe_string(response, 'code')
            if code != '0':
                message = self.safe_string(response, 'msg', 'Error')
                raise ExchangeError(message)
            return data
        return response
