# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.binance import binance


class binanceus(binance):

    def describe(self):
        return self.deep_extend(super(binanceus, self).describe(), {
            'id': 'binanceus',
            'name': 'Binance US',
            'countries': ['US'],  # US
            'certified': False,
            'pro': True,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/65177307-217b7c80-da5f-11e9-876e-0b748ba0a358.jpg',
                'api': {
                    'web': 'https://www.binance.us',
                    'sapi': 'https://api.binance.us/sapi/v1',
                    'wapi': 'https://api.binance.us/wapi/v3',
                    'public': 'https://api.binance.us/api/v1',
                    'private': 'https://api.binance.us/api/v3',
                    'v3': 'https://api.binance.us/api/v3',
                    'v1': 'https://api.binance.us/api/v1',
                },
                'www': 'https://www.binance.us',
                'referral': 'https://www.binance.us/?ref=35005074',
                'doc': 'https://github.com/binance-us/binance-official-api-docs',
                'fees': 'https://www.binance.us/en/fee/schedule',
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.001,  # 0.1% trading fee, zero fees for all trading pairs before November 1
                    'maker': 0.001,  # 0.1% trading fee, zero fees for all trading pairs before November 1
                },
            },
            'options': {
                'quoteOrderQty': False,
            },
        })

    async def fetch_currencies(self, params={}):
        return None
