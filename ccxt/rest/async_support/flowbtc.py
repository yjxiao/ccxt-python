# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.rest.async_support.ndax import ndax


class flowbtc(ndax):

    def describe(self):
        return self.deep_extend(super(flowbtc, self).describe(), {
            'id': 'flowbtc',
            'name': 'flowBTC',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87443317-01c0d080-c5fe-11ea-95c2-9ebe1a8fafd9.jpg',
                'api': {
                    'public': 'https://api.flowbtc.com.br:8443/ap/',
                    'private': 'https://api.flowbtc.com.br:8443/ap/',
                },
                'www': 'https://www.flowbtc.com.br',
                'doc': 'https://www.flowbtc.com.br/api.html',
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.0025,
                    'taker': 0.005,
                },
            },
        })
