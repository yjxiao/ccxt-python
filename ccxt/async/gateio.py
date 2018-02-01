# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async.bter import bter


class gateio (bter):

    def describe(self):
        return self.deep_extend(super(gateio, self).describe(), {
            'id': 'gateio',
            'name': 'Gate.io',
            'countries': 'CN',
            'rateLimit': 1000,
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': True,
                'withdraw': True,
                'createDepositAddress': True,
                'fetchDepositAddress': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31784029-0313c702-b509-11e7-9ccc-bc0da6a0e435.jpg',
                'api': {
                    'public': 'https://data.gate.io/api',
                    'private': 'https://data.gate.io/api',
                },
                'www': 'https://gate.io/',
                'doc': 'https://gate.io/api2',
                'fees': 'https://gate.io/fee',
            },
        })

    async def query_deposit_address(self, method, currency, params={}):
        method = 'privatePost' + method + 'Address'
        response = await getattr(self, method)(self.extend({
            'currency': currency,
        }, params))
        address = None
        if 'addr' in response:
            address = self.safe_string(response['addr'], 0)
        return {
            'currency': currency,
            'address': address,
            'status': 'ok' if (address is not None) else 'none',
            'info': response,
        }

    async def create_deposit_address(self, currency, params={}):
        return await self.query_deposit_address('New', currency, params)

    async def fetch_deposit_address(self, currency, params={}):
        return await self.query_deposit_address('Deposit', currency, params)

    def parse_trade(self, trade, market):
        # exchange reports local time(UTC+8)
        timestamp = self.parse8601(trade['date']) - 8 * 60 * 60 * 1000
        return {
            'id': trade['tradeID'],
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': trade['rate'],
            'amount': self.safe_float(trade, 'amount'),
        }
