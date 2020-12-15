# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.huobipro import huobipro


class cdax(huobipro):

    def describe(self):
        return self.deep_extend(super(cdax, self).describe(), {
            'id': 'cdax',
            'name': 'CDAX',
            'countries': ['RU'],
            'hostname': 'cdax.io',
            'pro': False,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/102157692-fd406280-3e90-11eb-8d46-4511b617cd17.jpg',
                'www': 'https://cdax.io',
                'referral': 'https://cdax.io/invite?invite_code=esc74',
                'doc': 'https://github.com/cloudapidoc/API_Docs',
                'fees': 'https://cdax.io/about/fee',
            },
        })
