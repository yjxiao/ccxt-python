# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.ws import gate


class gateio(gate):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'alias': True,
            'id': 'gateio',
        })
