# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.liqui import liqui
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import DDoSProtection


class yobit (liqui):

    def describe(self):
        return self.deep_extend(super(yobit, self).describe(), {
            'id': 'yobit',
            'name': 'YoBit',
            'countries': ['RU'],
            'rateLimit': 3000,  # responses are cached every 2 seconds
            'version': '3',
            'has': {
                'createDepositAddress': True,
                'fetchDepositAddress': True,
                'CORS': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766910-cdcbfdae-5eea-11e7-9859-03fea873272d.jpg',
                'api': {
                    'public': 'https://yobit.net/api',
                    'private': 'https://yobit.net/tapi',
                },
                'www': 'https://www.yobit.net',
                'doc': 'https://www.yobit.net/en/api/',
                'fees': 'https://www.yobit.net/en/fees/',
            },
            'api': {
                'public': {
                    'get': [
                        'depth/{pair}',
                        'info',
                        'ticker/{pair}',
                        'trades/{pair}',
                    ],
                },
                'private': {
                    'post': [
                        'ActiveOrders',
                        'CancelOrder',
                        'GetDepositAddress',
                        'getInfo',
                        'OrderInfo',
                        'Trade',
                        'TradeHistory',
                        'WithdrawCoinsToAddress',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.002,
                    'taker': 0.002,
                },
                'funding': {
                    'withdraw': {},
                },
            },
            'commonCurrencies': {
                'AIR': 'AirCoin',
                'ANI': 'ANICoin',
                'ANT': 'AntsCoin',  # what is self, a coin for ants?
                'ATMCHA': 'ATM',
                'ASN': 'Ascension',
                'AST': 'Astral',
                'ATM': 'Autumncoin',
                'BCC': 'BCH',
                'BCS': 'BitcoinStake',
                'BLN': 'Bulleon',
                'BOT': 'BOTcoin',
                'BON': 'BONES',
                'BPC': 'BitcoinPremium',
                'BTS': 'Bitshares2',
                'CAT': 'BitClave',
                'CMT': 'CometCoin',
                'COV': 'Coven Coin',
                'COVX': 'COV',
                'CPC': 'Capricoin',
                'CRC': 'CryCash',
                'CS': 'CryptoSpots',
                'DCT': 'Discount',
                'DGD': 'DarkGoldCoin',
                'DIRT': 'DIRTY',
                'DROP': 'FaucetCoin',
                'EKO': 'EkoCoin',
                'ENTER': 'ENTRC',
                'EPC': 'ExperienceCoin',
                'ERT': 'Eristica Token',
                'ESC': 'EdwardSnowden',
                'EUROPE': 'EUROP',
                'EXT': 'LifeExtension',
                'FUNK': 'FUNKCoin',
                'GCC': 'GlobalCryptocurrency',
                'GEN': 'Genstake',
                'GENE': 'Genesiscoin',
                'GOLD': 'GoldMint',
                'HTML5': 'HTML',
                'HYPERX': 'HYPER',
                'ICN': 'iCoin',
                'INSANE': 'INSN',
                'JNT': 'JointCoin',
                'JPC': 'JupiterCoin',
                'KNC': 'KingN Coin',
                'LBTCX': 'LiteBitcoin',
                'LIZI': 'LiZi',
                'LOC': 'LocoCoin',
                'LOCX': 'LOC',
                'LUNYR': 'LUN',
                'LUN': 'LunarCoin',  # they just change the ticker if it is already taken
                'MDT': 'Midnight',
                'NAV': 'NavajoCoin',
                'NBT': 'NiceBytes',
                'OMG': 'OMGame',
                'PAC': '$PAC',
                'PLAY': 'PlayCoin',
                'PIVX': 'Darknet',
                'PRS': 'PRE',
                'PUTIN': 'PUT',
                'STK': 'StakeCoin',
                'SUB': 'Subscriptio',
                'PAY': 'EPAY',
                'PLC': 'Platin Coin',
                'RCN': 'RCoin',
                'REP': 'Republicoin',
                'RUR': 'RUB',
                'XIN': 'XINCoin',
            },
            'options': {
                'fetchOrdersRequiresSymbol': True,
            },
        })

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'closed',
            '2': 'canceled',
            '3': 'open',  # or partially-filled and closed? https://github.com/ccxt/ccxt/issues/1594
        }
        if status in statuses:
            return statuses[status]
        return status

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo()
        balances = response['return']
        result = {'info': balances}
        sides = {'free': 'funds', 'total': 'funds_incl_orders'}
        keys = list(sides.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            side = sides[key]
            if side in balances:
                currencies = list(balances[side].keys())
                for j in range(0, len(currencies)):
                    lowercase = currencies[j]
                    uppercase = lowercase.upper()
                    currency = self.common_currency_code(uppercase)
                    account = None
                    if currency in result:
                        account = result[currency]
                    else:
                        account = self.account()
                    account[key] = balances[side][lowercase]
                    if (account['total'] is not None) and(account['free'] is not None):
                        account['used'] = account['total'] - account['free']
                    result[currency] = account
        return self.parse_balance(result)

    def create_deposit_address(self, code, params={}):
        response = self.fetch_deposit_address(code, self.extend({
            'need_new': 1,
        }, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response['info'],
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'coinName': currency['id'],
            'need_new': 0,
        }
        response = self.privatePostGetDepositAddress(self.extend(request, params))
        address = self.safe_string(response['return'], 'address')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        response = self.privatePostWithdrawCoinsToAddress(self.extend({
            'coinName': currency['id'],
            'amount': amount,
            'address': address,
        }, params))
        return {
            'info': response,
            'id': None,
        }

    def handle_errors(self, code, reason, url, method, headers, body):
        if body[0] == '{':
            response = json.loads(body)
            if 'success' in response:
                if not response['success']:
                    if 'error_log' in response:
                        if response['error_log'].find('Insufficient funds') >= 0:  # not enougTh is a typo inside Liqui's own API...
                            raise InsufficientFunds(self.id + ' ' + self.json(response))
                        elif response['error_log'] == 'Requests too often':
                            raise DDoSProtection(self.id + ' ' + self.json(response))
                        elif (response['error_log'] == 'not available') or (response['error_log'] == 'external service unavailable'):
                            raise DDoSProtection(self.id + ' ' + self.json(response))
                        elif response['error_log'] == 'Total transaction amount':
                            # eg {"success":0,"error":"Total transaction amount is less than minimal total: 0.00010000"}
                            raise InvalidOrder(self.id + ' ' + self.json(response))
                    raise ExchangeError(self.id + ' ' + self.json(response))
