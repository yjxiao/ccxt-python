# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError


class anxpro (Exchange):

    def describe(self):
        return self.deep_extend(super(anxpro, self).describe(), {
            'id': 'anxpro',
            'name': 'ANXPro',
            'countries': ['JP', 'SG', 'HK', 'NZ'],
            'rateLimit': 1500,
            'has': {
                'CORS': False,
                'fetchCurrencies': True,
                'fetchOHLCV': False,
                'fetchTrades': False,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27765983-fd8595da-5ec9-11e7-82e3-adb3ab8c2612.jpg',
                'api': {
                    'public': 'https://anxpro.com/api/2',
                    'private': 'https://anxpro.com/api/2',
                    'v3public': 'https://anxpro.com/api/3',
                },
                'www': 'https://anxpro.com',
                'doc': [
                    'https://anxv2.docs.apiary.io',
                    'https://anxv3.docs.apiary.io',
                    'https://anxpro.com/pages/api',
                ],
            },
            'api': {
                'v3public': {
                    'get': [
                        'currencyStatic',
                    ],
                },
                'public': {
                    'get': [
                        '{currency_pair}/money/ticker',
                        '{currency_pair}/money/depth/full',
                        '{currency_pair}/money/trade/fetch',  # disabled by ANXPro
                    ],
                },
                'private': {
                    'post': [
                        '{currency_pair}/money/order/add',
                        '{currency_pair}/money/order/cancel',
                        '{currency_pair}/money/order/quote',
                        '{currency_pair}/money/order/result',
                        '{currency_pair}/money/orders',
                        'money/{currency}/address',
                        'money/{currency}/send_simple',
                        'money/info',
                        'money/trade/list',
                        'money/wallet/history',
                    ],
                },
            },
            'httpExceptions': {
                '403': AuthenticationError,
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.3 / 100,
                    'taker': 0.6 / 100,
                },
            },
        })

    def fetch_currencies(self, params={}):
        response = self.v3publicGetCurrencyStatic(params)
        result = {}
        currencies = response['currencyStatic']['currencies']
        #       "currencies": {
        #         "HKD": {
        #           "decimals": 2,
        #           "minOrderSize": 1.00000000,
        #           "maxOrderSize": 10000000000.00000000,
        #           "displayDenominator": 1,
        #           "summaryDecimals": 0,
        #           "displayUnit": "HKD",
        #           "symbol": "$",
        #           "type": "FIAT",
        #           "engineSettings": {
        #             "depositsEnabled": False,
        #             "withdrawalsEnabled": True,
        #             "displayEnabled": True,
        #             "mobileAccessEnabled": True
        #           },
        #           "minOrderValue": 1.00000000,
        #           "maxOrderValue": 10000000000.00000000,
        #           "maxMarketOrderValue": 36000.00000000,
        #           "maxMarketOrderSize": 36000.00000000,
        #           "assetDivisibility": 0
        #         },
        #         "ETH": {
        #           "decimals": 8,
        #           "minOrderSize": 0.00010000,
        #           "maxOrderSize": 1000000000.00000000,
        #           "type": "CRYPTO",
        #           "confirmationThresholds": [
        #             {"confosRequired": 30, "threshold": 0.50000000},
        #             {"confosRequired": 45, "threshold": 10.00000000},
        #             {"confosRequired": 70}
        #           ],
        #           "networkFee": 0.00500000,
        #           "engineSettings": {
        #             "depositsEnabled": True,
        #             "withdrawalsEnabled": True,
        #             "displayEnabled": True,
        #             "mobileAccessEnabled": True
        #           },
        #           "minOrderValue": 0.00010000,
        #           "maxOrderValue": 10000000000.00000000,
        #           "maxMarketOrderValue": 10000000000.00000000,
        #           "maxMarketOrderSize": 1000000000.00000000,
        #           "digitalCurrencyType": "ETHEREUM",
        #           "assetDivisibility": 0,
        #           "assetIcon": "/images/currencies/crypto/ETH.svg"
        #         },
        #       },
        ids = list(currencies.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            currency = currencies[id]
            code = self.common_currency_code(id)
            engineSettings = self.safe_value(currency, 'engineSettings')
            depositsEnabled = self.safe_value(engineSettings, 'depositsEnabled')
            withdrawalsEnabled = self.safe_value(engineSettings, 'withdrawalsEnabled')
            displayEnabled = self.safe_value(engineSettings, 'displayEnabled')
            active = depositsEnabled and withdrawalsEnabled and displayEnabled
            precision = self.safe_integer(currency, 'decimals')
            fee = self.safe_float(currency, 'networkFee')
            type = self.safe_string(currency, 'type')
            if type != 'None':
                type = type.lower()
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': code,
                'type': type,
                'active': active,
                'precision': precision,
                'fee': fee,
                'limits': {
                    'amount': {
                        'min': self.safe_float(currency, 'minOrderSize'),
                        'max': self.safe_float(currency, 'maxOrderSize'),
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': self.safe_float(currency, 'minOrderValue'),
                        'max': self.safe_float(currency, 'maxOrderValue'),
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                },
            }
        return result

    def fetch_markets(self, params={}):
        response = self.v3publicGetCurrencyStatic(params)
        #
        #   {
        #     "currencyStatic": {
        #       "currencies": {
        #         "HKD": {
        #           "decimals": 2,
        #           "minOrderSize": 1.00000000,
        #           "maxOrderSize": 10000000000.00000000,
        #           "displayDenominator": 1,
        #           "summaryDecimals": 0,
        #           "displayUnit": "HKD",
        #           "symbol": "$",
        #           "type": "FIAT",
        #           "engineSettings": {
        #             "depositsEnabled": False,
        #             "withdrawalsEnabled": True,
        #             "displayEnabled": True,
        #             "mobileAccessEnabled": True
        #           },
        #           "minOrderValue": 1.00000000,
        #           "maxOrderValue": 10000000000.00000000,
        #           "maxMarketOrderValue": 36000.00000000,
        #           "maxMarketOrderSize": 36000.00000000,
        #           "assetDivisibility": 0
        #         },
        #         "ETH": {
        #           "decimals": 8,
        #           "minOrderSize": 0.00010000,
        #           "maxOrderSize": 1000000000.00000000,
        #           "type": "CRYPTO",
        #           "confirmationThresholds": [
        #             {"confosRequired": 30, "threshold": 0.50000000},
        #             {"confosRequired": 45, "threshold": 10.00000000},
        #             {"confosRequired": 70}
        #           ],
        #           "networkFee": 0.00500000,
        #           "engineSettings": {
        #             "depositsEnabled": True,
        #             "withdrawalsEnabled": True,
        #             "displayEnabled": True,
        #             "mobileAccessEnabled": True
        #           },
        #           "minOrderValue": 0.00010000,
        #           "maxOrderValue": 10000000000.00000000,
        #           "maxMarketOrderValue": 10000000000.00000000,
        #           "maxMarketOrderSize": 1000000000.00000000,
        #           "digitalCurrencyType": "ETHEREUM",
        #           "assetDivisibility": 0,
        #           "assetIcon": "/images/currencies/crypto/ETH.svg"
        #         },
        #       },
        #       "currencyPairs": {
        #         "ETHUSD": {
        #           "priceDecimals": 5,
        #           "engineSettings": {
        #             "tradingEnabled": True,
        #             "displayEnabled": True,
        #             "cancelOnly": True,
        #             "verifyRequired": False,
        #             "restrictedBuy": False,
        #             "restrictedSell": False
        #           },
        #           "minOrderRate": 10.00000000,
        #           "maxOrderRate": 10000.00000000,
        #           "displayPriceDecimals": 5,
        #           "tradedCcy": "ETH",
        #           "settlementCcy": "USD",
        #           "preferredMarket": "ANX",
        #           "chartEnabled": True,
        #           "simpleTradeEnabled": False
        #         },
        #       },
        #     },
        #     "timestamp": "1549840691039",
        #     "resultCode": "OK"
        #   }
        #
        currencyStatic = self.safe_value(response, 'currencyStatic', {})
        currencies = self.safe_value(currencyStatic, 'currencies', {})
        currencyPairs = self.safe_value(currencyStatic, 'currencyPairs', {})
        result = []
        ids = list(currencyPairs.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            market = currencyPairs[id]
            #
            #     "ETHUSD": {
            #       "priceDecimals": 5,
            #       "engineSettings": {
            #         "tradingEnabled": True,
            #         "displayEnabled": True,
            #         "cancelOnly": True,
            #         "verifyRequired": False,
            #         "restrictedBuy": False,
            #         "restrictedSell": False
            #       },
            #       "minOrderRate": 10.00000000,
            #       "maxOrderRate": 10000.00000000,
            #       "displayPriceDecimals": 5,
            #       "tradedCcy": "ETH",
            #       "settlementCcy": "USD",
            #       "preferredMarket": "ANX",
            #       "chartEnabled": True,
            #       "simpleTradeEnabled": False
            #     },
            #
            baseId = self.safe_string(market, 'tradedCcy')
            quoteId = self.safe_string(market, 'settlementCcy')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            baseCurrency = self.safe_value(currencies, baseId, {})
            quoteCurrency = self.safe_value(currencies, quoteId, {})
            precision = {
                'price': self.safe_integer(market, 'priceDecimals'),
                'amount': self.safe_integer(baseCurrency, 'decimals'),
            }
            engineSettings = self.safe_value(market, 'engineSettings')
            displayEnabled = self.safe_value(engineSettings, 'displayEnabled')
            tradingEnabled = self.safe_value(engineSettings, 'tradingEnabled')
            active = displayEnabled and tradingEnabled
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'precision': precision,
                'active': active,
                'limits': {
                    'price': {
                        'min': self.safe_float(market, 'minOrderRate'),
                        'max': self.safe_float(market, 'maxOrderRate'),
                    },
                    'amount': {
                        'min': self.safe_float(baseCurrency, 'minOrderSize'),
                        'max': self.safe_float(baseCurrency, 'maxOrderSize'),
                    },
                    'cost': {
                        'min': self.safe_float(quoteCurrency, 'minOrderValue'),
                        'max': self.safe_float(quoteCurrency, 'maxOrderValue'),
                    },
                },
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        response = self.privatePostMoneyInfo()
        balance = response['data']
        currencies = list(balance['Wallets'].keys())
        result = {'info': balance}
        for c in range(0, len(currencies)):
            currency = currencies[c]
            account = self.account()
            if currency in balance['Wallets']:
                wallet = balance['Wallets'][currency]
                account['free'] = float(wallet['Available_Balance']['value'])
                account['total'] = float(wallet['Balance']['value'])
                account['used'] = account['total'] - account['free']
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        response = self.publicGetCurrencyPairMoneyDepthFull(self.extend({
            'currency_pair': self.market_id(symbol),
        }, params))
        orderbook = response['data']
        t = int(orderbook['dataUpdateTime'])
        timestamp = int(t / 1000)
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'amount')

    def fetch_ticker(self, symbol, params={}):
        response = self.publicGetCurrencyPairMoneyTicker(self.extend({
            'currency_pair': self.market_id(symbol),
        }, params))
        ticker = response['data']
        t = int(ticker['dataUpdateTime'])
        timestamp = int(t / 1000)
        bid = self.safe_float(ticker['buy'], 'value')
        ask = self.safe_float(ticker['sell'], 'value')
        baseVolume = float(ticker['vol']['value'])
        last = float(ticker['last']['value'])
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': float(ticker['high']['value']),
            'low': float(ticker['low']['value']),
            'bid': bid,
            'bidVolume': None,
            'ask': ask,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': float(ticker['avg']['value']),
            'baseVolume': baseVolume,
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        raise ExchangeError(self.id + ' switched off the trades endpoint, see their docs at https://docs.anxv2.apiary.io')

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        market = self.market(symbol)
        order = {
            'currency_pair': market['id'],
            'amount_int': int(amount * 100000000),  # 10^8
        }
        if type == 'limit':
            order['price_int'] = int(price * market['multiplier'])  # 10^5 or 10^8
        order['type'] = 'bid' if (side == 'buy') else 'ask'
        result = self.privatePostCurrencyPairMoneyOrderAdd(self.extend(order, params))
        return {
            'info': result,
            'id': result['data'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostCurrencyPairMoneyOrderCancel({'oid': id})

    def get_amount_multiplier(self, code):
        multipliers = {
            'BTC': 100000000,
            'LTC': 100000000,
            'STR': 100000000,
            'XRP': 100000000,
            'DOGE': 100000000,
        }
        defaultValue = 100
        return self.safe_integer(multipliers, code, defaultValue)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        multiplier = self.get_amount_multiplier(code)
        request = {
            'currency': currency,
            'amount_int': int(amount * multiplier),
            'address': address,
        }
        if tag is not None:
            request['destinationTag'] = tag
        response = self.privatePostMoneyCurrencySendSimple(self.extend(request, params))
        return {
            'info': response,
            'id': response['data']['transactionId'],
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'][api] + '/' + request
        if api == 'public' or api == 'v3public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({'nonce': nonce}, query))
            secret = base64.b64decode(self.secret)
            # eslint-disable-next-line quotes
            auth = request + "\0" + body
            signature = self.hmac(self.encode(auth), secret, hashlib.sha512, 'base64')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Rest-Key': self.apiKey,
                'Rest-Sign': self.decode(signature),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response):
        if response is None or response == '':
            return
        result = self.safe_string(response, 'result')
        if (result is not None) and(result != 'success'):
            raise ExchangeError(self.id + ' ' + body)
        else:
            resultCode = self.safe_string(response, 'resultCode')
            if (resultCode is not None) and(resultCode != 'OK'):
                raise ExchangeError(self.id + ' ' + body)
