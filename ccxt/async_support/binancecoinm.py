# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.binance import binance


class binancecoinm(binance):

    def describe(self):
        return self.deep_extend(super(binancecoinm, self).describe(), {
            'id': 'binancecoinm',
            'name': 'Binance COIN-M',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/117738721-668c8d80-b205-11eb-8c49-3fad84c4a07f.jpg',
                'doc': [
                    'https://binance-docs.github.io/apidocs/delivery/en/',
                    'https://binance-docs.github.io/apidocs/spot/en',
                ],
            },
            'has': {
                'CORS': None,
                'spot': False,
                'margin': False,
                'swap': True,
                'future': True,
                'option': None,
                'createStopMarketOrder': True,
            },
            'options': {
                'fetchMarkets': ['inverse'],
                'defaultSubType': 'inverse',
                'leverageBrackets': None,
            },
        })

    async def transfer_in(self, code: str, amount, params={}):
        # transfer from spot wallet to coinm futures wallet
        return await self.futuresTransfer(code, amount, 3, params)

    async def transfer_out(self, code: str, amount, params={}):
        # transfer from coinm futures wallet to spot wallet
        return await self.futuresTransfer(code, amount, 4, params)
