# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.zb import zb


class bitkk(zb):

    def describe(self):
        return self.deep_extend(super(bitkk, self).describe(), {
            'id': 'bitkk',
            'name': 'bitkk',
            'comment': 'a Chinese ZB clone',
            'urls': {
                'api': {
                    'public': 'http://api.bitkk.com/data',  # no https for public API
                    'private': 'https://trade.bitkk.com/api',
                },
                'www': 'https://www.bitkk.com',
                'doc': 'https://www.bitkk.com/i/developer',
                'fees': 'https://www.bitkk.com/i/rate',
            },
        })
