# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.binance import binance


class binanceje (binance):

    def describe(self):
        return self.deep_extend(super(binanceje, self).describe(), {
            'id': 'binanceje',
            'name': 'Binance Jersey',
            'countries': ['JE'],  # Jersey
            'certified': False,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/54874009-d526eb00-4df3-11e9-928c-ce6a2b914cd1.jpg',
                'api': {
                    'web': 'https://www.binance.je',
                    'wapi': 'https://api.binance.je/wapi/v3',
                    'public': 'https://api.binance.je/api/v1',
                    'private': 'https://api.binance.je/api/v3',
                    'v3': 'https://api.binance.je/api/v3',
                    'v1': 'https://api.binance.je/api/v1',
                },
                'www': 'https://www.binance.je',
                'referral': 'https://www.binance.je/?ref=35047921',
                'doc': 'https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md',
                'fees': 'https://www.binance.je/fees.html',
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.0005,
                    'maker': 0.0005,
                },
                # should be deleted, these are outdated and inaccurate
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.0005,
                        'ETH': 0.01,
                    },
                    'deposit': {},
                },
            },
        })
