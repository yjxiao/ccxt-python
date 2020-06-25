# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxtpro.huobipro import huobipro
from ccxt.base.errors import NotSupported


class huobijp(huobipro):

    def describe(self):
        return self.deep_extend(super(huobijp, self).describe(), {
            'id': 'huobijp',
            'name': 'Huobi Japan',
            'countries': ['JP'],
            'hostname': 'api-cloud.huobi.co.jp',
            'has': {
                'fetchDepositAddress': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/85734211-85755480-b705-11ea-8b35-0b7f1db33a2f.jpg',
                'api': {
                    'ws': {
                        'api': {
                            'public': 'wss://{hostname}/ws',
                            'private': 'wss://{hostname}/ws',
                        },
                    },
                    'market': 'https://{hostname}',
                    'public': 'https://{hostname}',
                    'private': 'https://{hostname}',
                },
                'www': 'https://www.huobi.co.jp',
                'referral': 'https://www.huobi.co.jp/register/?invite_code=znnq3',
                'doc': 'https://api-doc.huobi.co.jp',
                'fees': 'https://www.huobi.co.jp/support/fee',
            },
        })

    async def fetch_deposit_address(self, code, params={}):
        raise NotSupported(self.id + ' fetchDepositAddress not supported yet')
