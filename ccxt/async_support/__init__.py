# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library (Async)"""

# -----------------------------------------------------------------------------

__version__ = '1.93.98'

# -----------------------------------------------------------------------------
from ccxt.rest.async_support.base.exchange import Exchange                   # noqa: F401

from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa: F401
from ccxt.base.decimal_to_precision import TRUNCATE              # noqa: F401
from ccxt.base.decimal_to_precision import ROUND                 # noqa: F401
from ccxt.base.decimal_to_precision import TICK_SIZE             # noqa: F401
from ccxt.base.decimal_to_precision import DECIMAL_PLACES        # noqa: F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt.base.decimal_to_precision import NO_PADDING            # noqa: F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO         # noqa: F401

from ccxt.base import errors                                # noqa: F401
from ccxt.base.errors import BaseError                                # noqa: F401
from ccxt.base.errors import ExchangeError                            # noqa: F401
from ccxt.base.errors import AuthenticationError                      # noqa: F401
from ccxt.base.errors import PermissionDenied                         # noqa: F401
from ccxt.base.errors import AccountNotEnabled                        # noqa: F401
from ccxt.base.errors import AccountSuspended                         # noqa: F401
from ccxt.base.errors import ArgumentsRequired                        # noqa: F401
from ccxt.base.errors import BadRequest                               # noqa: F401
from ccxt.base.errors import BadSymbol                                # noqa: F401
from ccxt.base.errors import MarginModeAlreadySet                     # noqa: F401
from ccxt.base.errors import BadResponse                              # noqa: F401
from ccxt.base.errors import NullResponse                             # noqa: F401
from ccxt.base.errors import InsufficientFunds                        # noqa: F401
from ccxt.base.errors import InvalidAddress                           # noqa: F401
from ccxt.base.errors import AddressPending                           # noqa: F401
from ccxt.base.errors import InvalidOrder                             # noqa: F401
from ccxt.base.errors import OrderNotFound                            # noqa: F401
from ccxt.base.errors import OrderNotCached                           # noqa: F401
from ccxt.base.errors import CancelPending                            # noqa: F401
from ccxt.base.errors import OrderImmediatelyFillable                 # noqa: F401
from ccxt.base.errors import OrderNotFillable                         # noqa: F401
from ccxt.base.errors import DuplicateOrderId                         # noqa: F401
from ccxt.base.errors import NotSupported                             # noqa: F401
from ccxt.base.errors import NetworkError                             # noqa: F401
from ccxt.base.errors import DDoSProtection                           # noqa: F401
from ccxt.base.errors import RateLimitExceeded                        # noqa: F401
from ccxt.base.errors import ExchangeNotAvailable                     # noqa: F401
from ccxt.base.errors import OnMaintenance                            # noqa: F401
from ccxt.base.errors import InvalidNonce                             # noqa: F401
from ccxt.base.errors import RequestTimeout                           # noqa: F401
from ccxt.base.errors import error_hierarchy                          # noqa: F401


from ccxt.ws.aax import aax                                                     # noqa: F401
from ccxt.ws.ascendex import ascendex                                           # noqa: F401
from ccxt.ws.bequant import bequant                                             # noqa: F401
from ccxt.rest.async_support.bibox import bibox                                 # noqa: F401
from ccxt.rest.async_support.bigone import bigone                               # noqa: F401
from ccxt.ws.binance import binance                                             # noqa: F401
from ccxt.ws.binancecoinm import binancecoinm                                   # noqa: F401
from ccxt.ws.binanceus import binanceus                                         # noqa: F401
from ccxt.ws.binanceusdm import binanceusdm                                     # noqa: F401
from ccxt.rest.async_support.bit2c import bit2c                                 # noqa: F401
from ccxt.rest.async_support.bitbank import bitbank                             # noqa: F401
from ccxt.rest.async_support.bitbay import bitbay                               # noqa: F401
from ccxt.rest.async_support.bitbns import bitbns                               # noqa: F401
from ccxt.ws.bitcoincom import bitcoincom                                       # noqa: F401
from ccxt.ws.bitfinex import bitfinex                                           # noqa: F401
from ccxt.ws.bitfinex2 import bitfinex2                                         # noqa: F401
from ccxt.rest.async_support.bitflyer import bitflyer                           # noqa: F401
from ccxt.rest.async_support.bitforex import bitforex                           # noqa: F401
from ccxt.rest.async_support.bitget import bitget                               # noqa: F401
from ccxt.rest.async_support.bithumb import bithumb                             # noqa: F401
from ccxt.ws.bitmart import bitmart                                             # noqa: F401
from ccxt.ws.bitmex import bitmex                                               # noqa: F401
from ccxt.ws.bitopro import bitopro                                             # noqa: F401
from ccxt.rest.async_support.bitpanda import bitpanda                           # noqa: F401
from ccxt.rest.async_support.bitrue import bitrue                               # noqa: F401
from ccxt.rest.async_support.bitso import bitso                                 # noqa: F401
from ccxt.ws.bitstamp import bitstamp                                           # noqa: F401
from ccxt.rest.async_support.bitstamp1 import bitstamp1                         # noqa: F401
from ccxt.ws.bittrex import bittrex                                             # noqa: F401
from ccxt.ws.bitvavo import bitvavo                                             # noqa: F401
from ccxt.rest.async_support.bkex import bkex                                   # noqa: F401
from ccxt.rest.async_support.bl3p import bl3p                                   # noqa: F401
from ccxt.rest.async_support.blockchaincom import blockchaincom                 # noqa: F401
from ccxt.rest.async_support.btcalpha import btcalpha                           # noqa: F401
from ccxt.rest.async_support.btcbox import btcbox                               # noqa: F401
from ccxt.rest.async_support.btcex import btcex                                 # noqa: F401
from ccxt.rest.async_support.btcmarkets import btcmarkets                       # noqa: F401
from ccxt.rest.async_support.btctradeua import btctradeua                       # noqa: F401
from ccxt.rest.async_support.btcturk import btcturk                             # noqa: F401
from ccxt.rest.async_support.buda import buda                                   # noqa: F401
from ccxt.rest.async_support.bw import bw                                       # noqa: F401
from ccxt.ws.bybit import bybit                                                 # noqa: F401
from ccxt.rest.async_support.bytetrade import bytetrade                         # noqa: F401
from ccxt.rest.async_support.cdax import cdax                                   # noqa: F401
from ccxt.rest.async_support.cex import cex                                     # noqa: F401
from ccxt.rest.async_support.coinbase import coinbase                           # noqa: F401
from ccxt.ws.coinbaseprime import coinbaseprime                                 # noqa: F401
from ccxt.ws.coinbasepro import coinbasepro                                     # noqa: F401
from ccxt.rest.async_support.coincheck import coincheck                         # noqa: F401
from ccxt.ws.coinex import coinex                                               # noqa: F401
from ccxt.rest.async_support.coinfalcon import coinfalcon                       # noqa: F401
from ccxt.rest.async_support.coinmate import coinmate                           # noqa: F401
from ccxt.rest.async_support.coinone import coinone                             # noqa: F401
from ccxt.rest.async_support.coinspot import coinspot                           # noqa: F401
from ccxt.rest.async_support.crex24 import crex24                               # noqa: F401
from ccxt.ws.cryptocom import cryptocom                                         # noqa: F401
from ccxt.ws.currencycom import currencycom                                     # noqa: F401
from ccxt.rest.async_support.delta import delta                                 # noqa: F401
from ccxt.rest.async_support.deribit import deribit                             # noqa: F401
from ccxt.rest.async_support.digifinex import digifinex                         # noqa: F401
from ccxt.rest.async_support.eqonex import eqonex                               # noqa: F401
from ccxt.ws.exmo import exmo                                                   # noqa: F401
from ccxt.rest.async_support.flowbtc import flowbtc                             # noqa: F401
from ccxt.rest.async_support.fmfwio import fmfwio                               # noqa: F401
from ccxt.ws.ftx import ftx                                                     # noqa: F401
from ccxt.ws.ftxus import ftxus                                                 # noqa: F401
from ccxt.ws.gate import gate                                                   # noqa: F401
from ccxt.ws.gateio import gateio                                               # noqa: F401
from ccxt.rest.async_support.gemini import gemini                               # noqa: F401
from ccxt.ws.hitbtc import hitbtc                                               # noqa: F401
from ccxt.rest.async_support.hitbtc3 import hitbtc3                             # noqa: F401
from ccxt.ws.hollaex import hollaex                                             # noqa: F401
from ccxt.ws.huobi import huobi                                                 # noqa: F401
from ccxt.ws.huobijp import huobijp                                             # noqa: F401
from ccxt.ws.huobipro import huobipro                                           # noqa: F401
from ccxt.ws.idex import idex                                                   # noqa: F401
from ccxt.rest.async_support.independentreserve import independentreserve       # noqa: F401
from ccxt.rest.async_support.indodax import indodax                             # noqa: F401
from ccxt.rest.async_support.itbit import itbit                                 # noqa: F401
from ccxt.ws.kraken import kraken                                               # noqa: F401
from ccxt.ws.kucoin import kucoin                                               # noqa: F401
from ccxt.rest.async_support.kucoinfutures import kucoinfutures                 # noqa: F401
from ccxt.rest.async_support.kuna import kuna                                   # noqa: F401
from ccxt.rest.async_support.latoken import latoken                             # noqa: F401
from ccxt.rest.async_support.lbank import lbank                                 # noqa: F401
from ccxt.rest.async_support.lbank2 import lbank2                               # noqa: F401
from ccxt.rest.async_support.liquid import liquid                               # noqa: F401
from ccxt.rest.async_support.luno import luno                                   # noqa: F401
from ccxt.rest.async_support.lykke import lykke                                 # noqa: F401
from ccxt.rest.async_support.mercado import mercado                             # noqa: F401
from ccxt.ws.mexc import mexc                                                   # noqa: F401
from ccxt.rest.async_support.mexc3 import mexc3                                 # noqa: F401
from ccxt.ws.ndax import ndax                                                   # noqa: F401
from ccxt.rest.async_support.novadax import novadax                             # noqa: F401
from ccxt.rest.async_support.oceanex import oceanex                             # noqa: F401
from ccxt.ws.okcoin import okcoin                                               # noqa: F401
from ccxt.ws.okex import okex                                                   # noqa: F401
from ccxt.rest.async_support.okex5 import okex5                                 # noqa: F401
from ccxt.ws.okx import okx                                                     # noqa: F401
from ccxt.rest.async_support.paymium import paymium                             # noqa: F401
from ccxt.ws.phemex import phemex                                               # noqa: F401
from ccxt.rest.async_support.poloniex import poloniex                           # noqa: F401
from ccxt.rest.async_support.probit import probit                               # noqa: F401
from ccxt.rest.async_support.qtrade import qtrade                               # noqa: F401
from ccxt.ws.ripio import ripio                                                 # noqa: F401
from ccxt.rest.async_support.stex import stex                                   # noqa: F401
from ccxt.rest.async_support.therock import therock                             # noqa: F401
from ccxt.rest.async_support.tidebit import tidebit                             # noqa: F401
from ccxt.rest.async_support.tidex import tidex                                 # noqa: F401
from ccxt.rest.async_support.timex import timex                                 # noqa: F401
from ccxt.ws.upbit import upbit                                                 # noqa: F401
from ccxt.rest.async_support.wavesexchange import wavesexchange                 # noqa: F401
from ccxt.rest.async_support.wazirx import wazirx                               # noqa: F401
from ccxt.ws.whitebit import whitebit                                           # noqa: F401
from ccxt.rest.async_support.woo import woo                                     # noqa: F401
from ccxt.rest.async_support.xena import xena                                   # noqa: F401
from ccxt.rest.async_support.yobit import yobit                                 # noqa: F401
from ccxt.rest.async_support.zaif import zaif                                   # noqa: F401
from ccxt.ws.zb import zb                                                       # noqa: F401
from ccxt.ws.zipmex import zipmex                                               # noqa: F401
from ccxt.rest.async_support.zonda import zonda                                 # noqa: F401

exchanges = [
    'aax',
    'alpaca',
    'ascendex',
    'bequant',
    'bibox',
    'bigone',
    'binance',
    'binancecoinm',
    'binanceus',
    'binanceusdm',
    'bit2c',
    'bitbank',
    'bitbay',
    'bitbns',
    'bitcoincom',
    'bitfinex',
    'bitfinex2',
    'bitflyer',
    'bitforex',
    'bitget',
    'bithumb',
    'bitmart',
    'bitmex',
    'bitopro',
    'bitpanda',
    'bitrue',
    'bitso',
    'bitstamp',
    'bitstamp1',
    'bittrex',
    'bitvavo',
    'bkex',
    'bl3p',
    'blockchaincom',
    'btcalpha',
    'btcbox',
    'btcex',
    'btcmarkets',
    'btctradeua',
    'btcturk',
    'buda',
    'bw',
    'bybit',
    'bytetrade',
    'cex',
    'coinbase',
    'coinbaseprime',
    'coinbasepro',
    'coincheck',
    'coinex',
    'coinfalcon',
    'coinmate',
    'coinone',
    'coinspot',
    'crex24',
    'cryptocom',
    'currencycom',
    'delta',
    'deribit',
    'digifinex',
    'eqonex',
    'exmo',
    'flowbtc',
    'fmfwio',
    'ftx',
    'ftxus',
    'gate',
    'gateio',
    'gemini',
    'hitbtc',
    'hitbtc3',
    'hollaex',
    'huobi',
    'huobijp',
    'huobipro',
    'idex',
    'independentreserve',
    'indodax',
    'itbit',
    'kraken',
    'kucoin',
    'kucoinfutures',
    'kuna',
    'latoken',
    'lbank',
    'lbank2',
    'liquid',
    'luno',
    'lykke',
    'mercado',
    'mexc',
    'mexc3',
    'ndax',
    'novadax',
    'oceanex',
    'okcoin',
    'okex',
    'okex5',
    'okx',
    'paymium',
    'phemex',
    'poloniex',
    'probit',
    'qtrade',
    'ripio',
    'stex',
    'therock',
    'tidebit',
    'tidex',
    'timex',
    'tokocrypto',
    'upbit',
    'wavesexchange',
    'wazirx',
    'whitebit',
    'woo',
    'yobit',
    'zaif',
    'zb',
    'zipmex',
    'zonda',
]

base = [
    'Exchange',
    'exchanges',
    'decimal_to_precision',
]

__all__ = base + errors.__all__ + exchanges
