# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.ftx import ftx


class ftxus(ftx):

    def describe(self):
        return self.deep_extend(super(ftxus, self).describe(), {
            'id': 'ftxus',
            'name': 'FTX US',
            'countries': ['US'],
            'certified': False,
            'hostname': 'ftx.us',
            'has': {
                'future': False,
                'swap': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/141506670-12f6115f-f425-4cd8-b892-b51d157ca01f.jpg',
                'www': 'https://ftx.us/',
                'docs': 'https://docs.ftx.us/',
                'fees': 'https://help.ftx.us/hc/en-us/articles/360043579273-Fees',
            },
        })
