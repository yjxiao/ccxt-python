# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.okcoin import okcoin


class okcoinusd(okcoin):

    def describe(self):
        return self.deep_extend(super(okcoinusd, self).describe(), {
            # self is a stub file that will be removed before 2020 Q2
            # it is placed here for temporary backward compatibility
            'id': 'okcoinusd',
        })
