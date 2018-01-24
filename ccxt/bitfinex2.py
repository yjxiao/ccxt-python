# -*- coding: utf-8 -*-

from ccxt.bitfinex import bitfinex
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported
from ccxt.base.errors import InsufficientFunds


class bitfinex2 (bitfinex):

    def describe(self):
        return self.deep_extend(super(bitfinex2, self).describe(), {
            'id': 'bitfinex2',
            'name': 'Bitfinex v2',
            'countries': 'VG',
            'version': 'v2',
            # new metainfo interface
            'has': {
                'CORS': True,
                'createOrder': False,
                'fetchMyTrades': False,
                'fetchOHLCV': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOpenOrders': False,
                'fetchClosedOrders': False,
                'withdraw': True,
                'deposit': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '3h': '3h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1D',
                '1w': '7D',
                '2w': '14D',
                '1M': '1M',
            },
            'rateLimit': 1500,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766244-e328a50c-5ed2-11e7-947b-041416579bb3.jpg',
                'api': 'https://api.bitfinex.com',
                'www': 'https://www.bitfinex.com',
                'doc': [
                    'https://bitfinex.readme.io/v2/docs',
                    'https://github.com/bitfinexcom/bitfinex-api-node',
                ],
                'fees': 'https://www.bitfinex.com/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'platform/status',
                        'tickers',
                        'ticker/{symbol}',
                        'trades/{symbol}/hist',
                        'book/{symbol}/{precision}',
                        'book/{symbol}/P0',
                        'book/{symbol}/P1',
                        'book/{symbol}/P2',
                        'book/{symbol}/P3',
                        'book/{symbol}/R0',
                        'stats1/{key}:{size}:{symbol}/{side}/{section}',
                        'stats1/{key}:{size}:{symbol}/long/last',
                        'stats1/{key}:{size}:{symbol}/long/hist',
                        'stats1/{key}:{size}:{symbol}/short/last',
                        'stats1/{key}:{size}:{symbol}/short/hist',
                        'candles/trade:{timeframe}:{symbol}/{section}',
                        'candles/trade:{timeframe}:{symbol}/last',
                        'candles/trade:{timeframe}:{symbol}/hist',
                    ],
                    'post': [
                        'calc/trade/avg',
                    ],
                },
                'private': {
                    'post': [
                        'auth/r/wallets',
                        'auth/r/orders/{symbol}',
                        'auth/r/orders/{symbol}/new',
                        'auth/r/orders/{symbol}/hist',
                        'auth/r/order/{symbol}:{id}/trades',
                        'auth/r/trades/{symbol}/hist',
                        'auth/r/positions',
                        'auth/r/funding/offers/{symbol}',
                        'auth/r/funding/offers/{symbol}/hist',
                        'auth/r/funding/loans/{symbol}',
                        'auth/r/funding/loans/{symbol}/hist',
                        'auth/r/funding/credits/{symbol}',
                        'auth/r/funding/credits/{symbol}/hist',
                        'auth/r/funding/trades/{symbol}/hist',
                        'auth/r/info/margin/{key}',
                        'auth/r/info/funding/{key}',
                        'auth/r/movements/{currency}/hist',
                        'auth/r/stats/perf:{timeframe}/hist',
                        'auth/r/alerts',
                        'auth/w/alert/set',
                        'auth/w/alert/{type}:{symbol}:{price}/del',
                        'auth/calc/order/avail',
                    ],
                },
            },
            'markets': {
                'AVT/BTC': {'id': 'tAVTBTC', 'symbol': 'AVT/BTC', 'base': 'AVT', 'quote': 'BTC', 'baseId': 'tAVT', 'quoteId': 'tBTC'},
                'AVT/ETH': {'id': 'tAVTETH', 'symbol': 'AVT/ETH', 'base': 'AVT', 'quote': 'ETH', 'baseId': 'tAVT', 'quoteId': 'tETH'},
                'AVT/USD': {'id': 'tAVTUSD', 'symbol': 'AVT/USD', 'base': 'AVT', 'quote': 'USD', 'baseId': 'tAVT', 'quoteId': 'zUSD'},
                'CST_BCC/BTC': {'id': 'tBCCBTC', 'symbol': 'CST_BCC/BTC', 'base': 'CST_BCC', 'quote': 'BTC', 'baseId': 'tBCC', 'quoteId': 'tBTC'},
                'CST_BCC/USD': {'id': 'tBCCUSD', 'symbol': 'CST_BCC/USD', 'base': 'CST_BCC', 'quote': 'USD', 'baseId': 'tBCC', 'quoteId': 'zUSD'},
                'BCH/BTC': {'id': 'tBCHBTC', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'tBCH', 'quoteId': 'tBTC'},
                'BCH/ETH': {'id': 'tBCHETH', 'symbol': 'BCH/ETH', 'base': 'BCH', 'quote': 'ETH', 'baseId': 'tBCH', 'quoteId': 'tETH'},
                'BCH/USD': {'id': 'tBCHUSD', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD', 'baseId': 'tBCH', 'quoteId': 'zUSD'},
                'CST_BCU/BTC': {'id': 'tBCUBTC', 'symbol': 'CST_BCU/BTC', 'base': 'CST_BCU', 'quote': 'BTC', 'baseId': 'tBCU', 'quoteId': 'tBTC'},
                'CST_BCU/USD': {'id': 'tBCUUSD', 'symbol': 'CST_BCU/USD', 'base': 'CST_BCU', 'quote': 'USD', 'baseId': 'tBCU', 'quoteId': 'zUSD'},
                'BT1/BTC': {'id': 'tBT1BTC', 'symbol': 'BT1/BTC', 'base': 'BT1', 'quote': 'BTC', 'baseId': 'tBT1', 'quoteId': 'tBTC'},
                'BT1/USD': {'id': 'tBT1USD', 'symbol': 'BT1/USD', 'base': 'BT1', 'quote': 'USD', 'baseId': 'tBT1', 'quoteId': 'zUSD'},
                'BT2/BTC': {'id': 'tBT2BTC', 'symbol': 'BT2/BTC', 'base': 'BT2', 'quote': 'BTC', 'baseId': 'tBT2', 'quoteId': 'tBTC'},
                'BT2/USD': {'id': 'tBT2USD', 'symbol': 'BT2/USD', 'base': 'BT2', 'quote': 'USD', 'baseId': 'tBT2', 'quoteId': 'zUSD'},
                'BTC/USD': {'id': 'tBTCUSD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'tBTC', 'quoteId': 'zUSD'},
                'BTC/EUR': {'id': 'tBTCEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'tBTC', 'quoteId': 'zEUR'},
                'BTG/BTC': {'id': 'tBTGBTC', 'symbol': 'BTG/BTC', 'base': 'BTG', 'quote': 'BTC', 'baseId': 'tBTG', 'quoteId': 'tBTC'},
                'BTG/USD': {'id': 'tBTGUSD', 'symbol': 'BTG/USD', 'base': 'BTG', 'quote': 'USD', 'baseId': 'tBTG', 'quoteId': 'zUSD'},
                'DASH/BTC': {'id': 'tDSHBTC', 'symbol': 'DASH/BTC', 'base': 'DASH', 'quote': 'BTC', 'baseId': 'tDASH', 'quoteId': 'tBTC'},
                'DASH/USD': {'id': 'tDSHUSD', 'symbol': 'DASH/USD', 'base': 'DASH', 'quote': 'USD', 'baseId': 'tDASH', 'quoteId': 'zUSD'},
                'DAT/BTC': {'id': 'tDATBTC', 'symbol': 'DAT/BTC', 'base': 'DAT', 'quote': 'BTC', 'baseId': 'tDAT', 'quoteId': 'tBTC'},
                'DAT/ETH': {'id': 'tDATETH', 'symbol': 'DAT/ETH', 'base': 'DAT', 'quote': 'ETH', 'baseId': 'tDAT', 'quoteId': 'tETH'},
                'DAT/USD': {'id': 'tDATUSD', 'symbol': 'DAT/USD', 'base': 'DAT', 'quote': 'USD', 'baseId': 'tDAT', 'quoteId': 'zUSD'},
                'EDO/BTC': {'id': 'tEDOBTC', 'symbol': 'EDO/BTC', 'base': 'EDO', 'quote': 'BTC', 'baseId': 'tEDO', 'quoteId': 'tBTC'},
                'EDO/ETH': {'id': 'tEDOETH', 'symbol': 'EDO/ETH', 'base': 'EDO', 'quote': 'ETH', 'baseId': 'tEDO', 'quoteId': 'tETH'},
                'EDO/USD': {'id': 'tEDOUSD', 'symbol': 'EDO/USD', 'base': 'EDO', 'quote': 'USD', 'baseId': 'tEDO', 'quoteId': 'zUSD'},
                'EOS/BTC': {'id': 'tEOSBTC', 'symbol': 'EOS/BTC', 'base': 'EOS', 'quote': 'BTC', 'baseId': 'tEOS', 'quoteId': 'tBTC'},
                'EOS/ETH': {'id': 'tEOSETH', 'symbol': 'EOS/ETH', 'base': 'EOS', 'quote': 'ETH', 'baseId': 'tEOS', 'quoteId': 'tETH'},
                'EOS/USD': {'id': 'tEOSUSD', 'symbol': 'EOS/USD', 'base': 'EOS', 'quote': 'USD', 'baseId': 'tEOS', 'quoteId': 'zUSD'},
                'ETC/BTC': {'id': 'tETCBTC', 'symbol': 'ETC/BTC', 'base': 'ETC', 'quote': 'BTC', 'baseId': 'tETC', 'quoteId': 'tBTC'},
                'ETC/USD': {'id': 'tETCUSD', 'symbol': 'ETC/USD', 'base': 'ETC', 'quote': 'USD', 'baseId': 'tETC', 'quoteId': 'zUSD'},
                'ETH/BTC': {'id': 'tETHBTC', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'tETH', 'quoteId': 'tBTC'},
                'ETH/USD': {'id': 'tETHUSD', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD', 'baseId': 'tETH', 'quoteId': 'zUSD'},
                'ETP/BTC': {'id': 'tETPBTC', 'symbol': 'ETP/BTC', 'base': 'ETP', 'quote': 'BTC', 'baseId': 'tETP', 'quoteId': 'tBTC'},
                'ETP/ETH': {'id': 'tETPETH', 'symbol': 'ETP/ETH', 'base': 'ETP', 'quote': 'ETH', 'baseId': 'tETP', 'quoteId': 'tETH'},
                'ETP/USD': {'id': 'tETPUSD', 'symbol': 'ETP/USD', 'base': 'ETP', 'quote': 'USD', 'baseId': 'tETP', 'quoteId': 'zUSD'},
                'IOTA/BTC': {'id': 'tIOTBTC', 'symbol': 'IOTA/BTC', 'base': 'IOTA', 'quote': 'BTC', 'baseId': 'tIOTA', 'quoteId': 'tBTC'},
                'IOTA/ETH': {'id': 'tIOTETH', 'symbol': 'IOTA/ETH', 'base': 'IOTA', 'quote': 'ETH', 'baseId': 'tIOTA', 'quoteId': 'tETH'},
                'IOTA/USD': {'id': 'tIOTUSD', 'symbol': 'IOTA/USD', 'base': 'IOTA', 'quote': 'USD', 'baseId': 'tIOTA', 'quoteId': 'zUSD'},
                'LTC/BTC': {'id': 'tLTCBTC', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC', 'baseId': 'tLTC', 'quoteId': 'tBTC'},
                'LTC/USD': {'id': 'tLTCUSD', 'symbol': 'LTC/USD', 'base': 'LTC', 'quote': 'USD', 'baseId': 'tLTC', 'quoteId': 'zUSD'},
                'NEO/BTC': {'id': 'tNEOBTC', 'symbol': 'NEO/BTC', 'base': 'NEO', 'quote': 'BTC', 'baseId': 'tNEO', 'quoteId': 'tBTC'},
                'NEO/ETH': {'id': 'tNEOETH', 'symbol': 'NEO/ETH', 'base': 'NEO', 'quote': 'ETH', 'baseId': 'tNEO', 'quoteId': 'tETH'},
                'NEO/USD': {'id': 'tNEOUSD', 'symbol': 'NEO/USD', 'base': 'NEO', 'quote': 'USD', 'baseId': 'tNEO', 'quoteId': 'zUSD'},
                'OMG/BTC': {'id': 'tOMGBTC', 'symbol': 'OMG/BTC', 'base': 'OMG', 'quote': 'BTC', 'baseId': 'tOMG', 'quoteId': 'tBTC'},
                'OMG/ETH': {'id': 'tOMGETH', 'symbol': 'OMG/ETH', 'base': 'OMG', 'quote': 'ETH', 'baseId': 'tOMG', 'quoteId': 'tETH'},
                'OMG/USD': {'id': 'tOMGUSD', 'symbol': 'OMG/USD', 'base': 'OMG', 'quote': 'USD', 'baseId': 'tOMG', 'quoteId': 'zUSD'},
                'QTUM/BTC': {'id': 'tQTMBTC', 'symbol': 'QTUM/BTC', 'base': 'QTUM', 'quote': 'BTC', 'baseId': 'tQTUM', 'quoteId': 'tBTC'},
                'QTUM/ETH': {'id': 'tQTMETH', 'symbol': 'QTUM/ETH', 'base': 'QTUM', 'quote': 'ETH', 'baseId': 'tQTUM', 'quoteId': 'tETH'},
                'QTUM/USD': {'id': 'tQTMUSD', 'symbol': 'QTUM/USD', 'base': 'QTUM', 'quote': 'USD', 'baseId': 'tQTUM', 'quoteId': 'zUSD'},
                'RRT/BTC': {'id': 'tRRTBTC', 'symbol': 'RRT/BTC', 'base': 'RRT', 'quote': 'BTC', 'baseId': 'tRRT', 'quoteId': 'tBTC'},
                'RRT/USD': {'id': 'tRRTUSD', 'symbol': 'RRT/USD', 'base': 'RRT', 'quote': 'USD', 'baseId': 'tRRT', 'quoteId': 'zUSD'},
                'SAN/BTC': {'id': 'tSANBTC', 'symbol': 'SAN/BTC', 'base': 'SAN', 'quote': 'BTC', 'baseId': 'tSAN', 'quoteId': 'tBTC'},
                'SAN/ETH': {'id': 'tSANETH', 'symbol': 'SAN/ETH', 'base': 'SAN', 'quote': 'ETH', 'baseId': 'tSAN', 'quoteId': 'tETH'},
                'SAN/USD': {'id': 'tSANUSD', 'symbol': 'SAN/USD', 'base': 'SAN', 'quote': 'USD', 'baseId': 'tSAN', 'quoteId': 'zUSD'},
                'XMR/BTC': {'id': 'tXMRBTC', 'symbol': 'XMR/BTC', 'base': 'XMR', 'quote': 'BTC', 'baseId': 'tXMR', 'quoteId': 'tBTC'},
                'XMR/USD': {'id': 'tXMRUSD', 'symbol': 'XMR/USD', 'base': 'XMR', 'quote': 'USD', 'baseId': 'tXMR', 'quoteId': 'zUSD'},
                'XRP/BTC': {'id': 'tXRPBTC', 'symbol': 'XRP/BTC', 'base': 'XRP', 'quote': 'BTC', 'baseId': 'tXRP', 'quoteId': 'tBTC'},
                'XRP/USD': {'id': 'tXRPUSD', 'symbol': 'XRP/USD', 'base': 'XRP', 'quote': 'USD', 'baseId': 'tXRP', 'quoteId': 'zUSD'},
                'ZEC/BTC': {'id': 'tZECBTC', 'symbol': 'ZEC/BTC', 'base': 'ZEC', 'quote': 'BTC', 'baseId': 'tZEC', 'quoteId': 'tBTC'},
                'ZEC/USD': {'id': 'tZECUSD', 'symbol': 'ZEC/USD', 'base': 'ZEC', 'quote': 'USD', 'baseId': 'tZEC', 'quoteId': 'zUSD'},
                'YYW/USD': {'id': 'tYYWUSD', 'symbol': 'YYW/USD', 'base': 'YYW', 'quote': 'USD', 'baseId': 'tYYW', 'quoteId': 'zUSD'},
                'YYW/BTC': {'id': 'tYYWBTC', 'symbol': 'YYW/BTC', 'base': 'YYW', 'quote': 'BTC', 'baseId': 'tYYW', 'quoteId': 'zBTC'},
                'YYW/ETH': {'id': 'tYYWETH', 'symbol': 'YYW/ETH', 'base': 'YYW', 'quote': 'ETH', 'baseId': 'tYYW', 'quoteId': 'zETH'},
                'SNT/USD': {'id': 'tSNTUSD', 'symbol': 'SNT/USD', 'base': 'SNT', 'quote': 'USD', 'baseId': 'tSNT', 'quoteId': 'zUSD'},
                'SNT/BTC': {'id': 'tSNTBTC', 'symbol': 'SNT/BTC', 'base': 'SNT', 'quote': 'BTC', 'baseId': 'tSNT', 'quoteId': 'zBTC'},
                'SNT/ETH': {'id': 'tSNTETH', 'symbol': 'SNT/ETH', 'base': 'SNT', 'quote': 'ETH', 'baseId': 'tSNT', 'quoteId': 'zETH'},
                'QASH/USD': {'id': 'tQASHUSD', 'symbol': 'QASH/USD', 'base': 'QASH', 'quote': 'USD', 'baseId': 'tQASH', 'quoteId': 'zUSD'},
                'QASH/BTC': {'id': 'tQASHBTC', 'symbol': 'QASH/BTC', 'base': 'QASH', 'quote': 'BTC', 'baseId': 'tQASH', 'quoteId': 'zBTC'},
                'QASH/ETH': {'id': 'tQASHETH', 'symbol': 'QASH/ETH', 'base': 'QASH', 'quote': 'ETH', 'baseId': 'tQASH', 'quoteId': 'zETH'},
                'GNT/USD': {'id': 'tGNTUSD', 'symbol': 'GNT/USD', 'base': 'GNT', 'quote': 'USD', 'baseId': 'tGNT', 'quoteId': 'zUSD'},
                'GNT/BTC': {'id': 'tGNTBTC', 'symbol': 'GNT/BTC', 'base': 'GNT', 'quote': 'BTC', 'baseId': 'tGNT', 'quoteId': 'zBTC'},
                'GNT/ETH': {'id': 'tGNTETH', 'symbol': 'GNT/ETH', 'base': 'GNT', 'quote': 'ETH', 'baseId': 'tGNT', 'quoteId': 'zETH'},
                'BAT/USD': {'id': 'tBATUSD', 'symbol': 'BAT/USD', 'base': 'BAT', 'quote': 'USD', 'baseId': 'tBAT', 'quoteId': 'zUSD'},
                'BAT/BTC': {'id': 'tBATBTC', 'symbol': 'BAT/BTC', 'base': 'BAT', 'quote': 'BTC', 'baseId': 'tBAT', 'quoteId': 'zBTC'},
                'BAT/ETH': {'id': 'tBATETH', 'symbol': 'BAT/ETH', 'base': 'BAT', 'quote': 'ETH', 'baseId': 'tBAT', 'quoteId': 'zETH'},
                'SPK/USD': {'id': 'tSPKUSD', 'symbol': 'SPK/USD', 'base': 'SPK', 'quote': 'USD', 'baseId': 'tSPK', 'quoteId': 'zUSD'},
                'SPK/BTC': {'id': 'tSPKBTC', 'symbol': 'SPK/BTC', 'base': 'SPK', 'quote': 'BTC', 'baseId': 'tSPK', 'quoteId': 'zBTC'},
                'SPK/ETH': {'id': 'tSPKETH', 'symbol': 'SPK/ETH', 'base': 'SPK', 'quote': 'ETH', 'baseId': 'tSPK', 'quoteId': 'zETH'},
            },
            'fees': {
                'trading': {
                    'maker': 0.1 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'withdraw': {
                        'BTC': 0.0005,
                        'BCH': 0.0005,
                        'ETH': 0.01,
                        'EOS': 0.1,
                        'LTC': 0.001,
                        'OMG': 0.1,
                        'IOT': 0.0,
                        'NEO': 0.0,
                        'ETC': 0.01,
                        'XRP': 0.02,
                        'ETP': 0.01,
                        'ZEC': 0.001,
                        'BTG': 0.0,
                        'DASH': 0.01,
                        'XMR': 0.04,
                        'QTM': 0.01,
                        'EDO': 0.5,
                        'DAT': 1.0,
                        'AVT': 0.5,
                        'SAN': 0.1,
                        'USDT': 5.0,
                        'SPK': 9.2784,
                        'BAT': 9.0883,
                        'GNT': 8.2881,
                        'SNT': 14.303,
                        'QASH': 3.2428,
                        'YYW': 18.055,
                    },
                },
            },
        })

    def common_currency_code(self, currency):
        currencies = {
            'DSH': 'DASH',  # Bitfinex names Dash as DSH, instead of DASH
            'QTM': 'QTUM',
            'BCC': 'CST_BCC',
            'BCU': 'CST_BCU',
            'IOT': 'IOTA',
            'DAT': 'DATA',
        }
        return currencies[currency] if (currency in list(currencies.keys())) else currency

    def fetch_balance(self, params={}):
        response = self.privatePostAuthRWallets()
        balanceType = self.safe_string(params, 'type', 'exchange')
        result = {'info': response}
        for b in range(0, len(response)):
            balance = response[b]
            accountType, currency, total, interest, available = balance
            if accountType == balanceType:
                if currency[0] == 't':
                    currency = currency[1:]
                uppercase = currency.upper()
                uppercase = self.common_currency_code(uppercase)
                account = self.account()
                account['free'] = available
                account['total'] = total
                if account['free']:
                    account['used'] = account['total'] - account['free']
                result[uppercase] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, params={}):
        orderbook = self.publicGetBookSymbolPrecision(self.extend({
            'symbol': self.market_id(symbol),
            'precision': 'R0',
        }, params))
        timestamp = self.milliseconds()
        result = {
            'bids': [],
            'asks': [],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        for i in range(0, len(orderbook)):
            order = orderbook[i]
            price = order[1]
            amount = order[2]
            side = 'bids' if (amount > 0) else 'asks'
            amount = abs(amount)
            result[side].append([price, amount])
        result['bids'] = self.sort_by(result['bids'], 0, True)
        result['asks'] = self.sort_by(result['asks'], 0)
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        length = len(ticker)
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': ticker[length - 2],
            'low': ticker[length - 1],
            'bid': ticker[length - 10],
            'ask': ticker[length - 8],
            'vwap': None,
            'open': None,
            'close': None,
            'first': None,
            'last': ticker[length - 4],
            'change': ticker[length - 6],
            'percentage': ticker[length - 5],
            'average': None,
            'baseVolume': ticker[length - 3],
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        tickers = self.publicGetTickers(self.extend({
            'symbols': ','.join(self.ids),
        }, params))
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            id = ticker[0]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        market = self.markets[symbol]
        ticker = self.publicGetTickerSymbol(self.extend({
            'symbol': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        id, timestamp, amount, price = trade
        side = 'sell' if (amount < 0) else 'buy'
        if amount < 0:
            amount = -amount
        return {
            'id': str(id),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['start'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTradesSymbolHist(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'timeframe': self.timeframes[timeframe],
            'sort': 1,
        }
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            request['start'] = since
        request = self.extend(request, params)
        response = self.publicGetCandlesTradeTimeframeSymbolHist(request)
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        raise NotSupported(self.id + ' createOrder not implemented yet')

    def cancel_order(self, id, symbol=None, params={}):
        raise NotSupported(self.id + ' cancelOrder not implemented yet')

    def fetch_order(self, id, symbol=None, params={}):
        raise NotSupported(self.id + ' fetchOrder not implemented yet')

    def withdraw(self, currency, amount, address, tag=None, params={}):
        raise NotSupported(self.id + ' withdraw not implemented yet')

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        url = self.urls['api'] + '/' + request
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            body = self.json(query)
            auth = '/api' + '/' + request + nonce + body
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha384)
            headers = {
                'bfx-nonce': nonce,
                'bfx-apikey': self.apiKey,
                'bfx-signature': signature,
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if response:
            if 'message' in response:
                if response['message'].find('not enough exchange balance') >= 0:
                    raise InsufficientFunds(self.id + ' ' + self.json(response))
                raise ExchangeError(self.id + ' ' + self.json(response))
            return response
        elif response == '':
            raise ExchangeError(self.id + ' returned empty response')
        return response
