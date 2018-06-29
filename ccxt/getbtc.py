# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt._1btcxe import _1btcxe


class getbtc (_1btcxe):

    def describe(self):
        return self.deep_extend(super(getbtc, self).describe(), {
            'id': 'getbtc',
            'name': 'GetBTC',
            'countries': ['VC', 'RU'],  # Saint Vincent and the Grenadines, Russia, CIS
            'rateLimit': 1000,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/33801902-03c43462-dd7b-11e7-992e-077e4cd015b9.jpg',
                'api': 'https://getbtc.org/api',
                'www': 'https://getbtc.org',
                'doc': 'https://getbtc.org/api-docs.php',
            },
            'has': {
                'fetchTrades': False,
                'fetchOHLCV': False,
            },
            'fees': {
                'trading': {
                    'taker': 0.20 / 100,
                    'maker': 0.20 / 100,
                },
            },
            'markets': {
                'BTC/USD': {'lot': 1e-08, 'symbol': 'BTC/USD', 'quote': 'USD', 'base': 'BTC', 'precision': {'amount': 8, 'price': 8}, 'id': 'USD', 'limits': {'amount': {'max': None, 'min': 1e-08}, 'price': {'max': 'None', 'min': 1e-08}}},
                'BTC/EUR': {'lot': 1e-08, 'symbol': 'BTC/EUR', 'quote': 'EUR', 'base': 'BTC', 'precision': {'amount': 8, 'price': 8}, 'id': 'EUR', 'limits': {'amount': {'max': None, 'min': 1e-08}, 'price': {'max': 'None', 'min': 1e-08}}},
                'BTC/RUB': {'lot': 1e-08, 'symbol': 'BTC/RUB', 'quote': 'RUB', 'base': 'BTC', 'precision': {'amount': 8, 'price': 8}, 'id': 'RUB', 'limits': {'amount': {'max': None, 'min': 1e-08}, 'price': {'max': 'None', 'min': 1e-08}}},
            },
        })
