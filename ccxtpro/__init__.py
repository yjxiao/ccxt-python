# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library (Async)"""

# -----------------------------------------------------------------------------

import ccxt.async_support as ccxt

# -----------------------------------------------------------------------------

__version__ = '0.0.25'

# -----------------------------------------------------------------------------

from ccxtpro.base.exchange import Exchange                   # noqa: F401
from ccxtpro.base.exchange import BaseExchange               # noqa: F401

# -----------------------------------------------------------------------------

from ccxt import decimal_to_precision  # noqa: F401
from ccxt import TRUNCATE              # noqa: F401
from ccxt import ROUND                 # noqa: F401
from ccxt import DECIMAL_PLACES        # noqa: F401
from ccxt import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt import NO_PADDING            # noqa: F401
from ccxt import PAD_WITH_ZERO         # noqa: F401

from ccxt.base import errors                        # noqa: F401
from ccxt import BaseError                          # noqa: F401
from ccxt import ExchangeError                      # noqa: F401
from ccxt import NotSupported                       # noqa: F401
from ccxt import AuthenticationError                # noqa: F401
from ccxt import PermissionDenied                   # noqa: F401
from ccxt import AccountSuspended                   # noqa: F401
from ccxt import InvalidNonce                       # noqa: F401
from ccxt import InsufficientFunds                  # noqa: F401
from ccxt import InvalidOrder                       # noqa: F401
from ccxt import OrderNotFound                      # noqa: F401
from ccxt import OrderNotCached                     # noqa: F401
from ccxt import DuplicateOrderId                   # noqa: F401
from ccxt import CancelPending                      # noqa: F401
from ccxt import NetworkError                       # noqa: F401
from ccxt import DDoSProtection                     # noqa: F401
from ccxt import RateLimitExceeded                  # noqa: F401
from ccxt import RequestTimeout                     # noqa: F401
from ccxt import ExchangeNotAvailable               # noqa: F401
from ccxt import OnMaintenance                      # noqa: F401
from ccxt import InvalidAddress                     # noqa: F401
from ccxt import AddressPending                     # noqa: F401
from ccxt import ArgumentsRequired                  # noqa: F401
from ccxt import BadRequest                         # noqa: F401
from ccxt import BadResponse                        # noqa: F401
from ccxt import NullResponse                       # noqa: F401
from ccxt import OrderImmediatelyFillable           # noqa: F401
from ccxt import OrderNotFillable                   # noqa: F401

# CCXT exchanges

from ccxt.async_support._1btcxe import _1btcxe                            # noqa: F401
from ccxt.async_support.acx import acx                                    # noqa: F401
from ccxt.async_support.adara import adara                                # noqa: F401
from ccxt.async_support.anxpro import anxpro                              # noqa: F401
from ccxt.async_support.bcex import bcex                                  # noqa: F401
from ccxt.async_support.bequant import bequant                            # noqa: F401
from ccxt.async_support.bibox import bibox                                # noqa: F401
from ccxt.async_support.bigone import bigone                              # noqa: F401
from ccxt.async_support.binanceje import binanceje                        # noqa: F401
from ccxt.async_support.binanceus import binanceus                        # noqa: F401
from ccxt.async_support.bit2c import bit2c                                # noqa: F401
from ccxt.async_support.bitbank import bitbank                            # noqa: F401
from ccxt.async_support.bitbay import bitbay                              # noqa: F401
from ccxt.async_support.bitfinex2 import bitfinex2                        # noqa: F401
from ccxt.async_support.bitflyer import bitflyer                          # noqa: F401
from ccxt.async_support.bitforex import bitforex                          # noqa: F401
from ccxt.async_support.bithumb import bithumb                            # noqa: F401
from ccxt.async_support.bitkk import bitkk                                # noqa: F401
from ccxt.async_support.bitlish import bitlish                            # noqa: F401
from ccxt.async_support.bitmart import bitmart                            # noqa: F401
from ccxt.async_support.bitmax import bitmax                              # noqa: F401
from ccxt.async_support.bitso import bitso                                # noqa: F401
from ccxt.async_support.bitstamp import bitstamp                          # noqa: F401
from ccxt.async_support.bitstamp1 import bitstamp1                        # noqa: F401
from ccxt.async_support.bitz import bitz                                  # noqa: F401
from ccxt.async_support.bl3p import bl3p                                  # noqa: F401
from ccxt.async_support.bleutrade import bleutrade                        # noqa: F401
from ccxt.async_support.braziliex import braziliex                        # noqa: F401
from ccxt.async_support.btcalpha import btcalpha                          # noqa: F401
from ccxt.async_support.btcbox import btcbox                              # noqa: F401
from ccxt.async_support.btcchina import btcchina                          # noqa: F401
from ccxt.async_support.btcmarkets import btcmarkets                      # noqa: F401
from ccxt.async_support.btctradeim import btctradeim                      # noqa: F401
from ccxt.async_support.btctradeua import btctradeua                      # noqa: F401
from ccxt.async_support.btcturk import btcturk                            # noqa: F401
from ccxt.async_support.buda import buda                                  # noqa: F401
from ccxt.async_support.bw import bw                                      # noqa: F401
from ccxt.async_support.bytetrade import bytetrade                        # noqa: F401
from ccxt.async_support.cex import cex                                    # noqa: F401
from ccxt.async_support.chilebit import chilebit                          # noqa: F401
from ccxt.async_support.cobinhood import cobinhood                        # noqa: F401
from ccxt.async_support.coinbase import coinbase                          # noqa: F401
from ccxt.async_support.coincheck import coincheck                        # noqa: F401
from ccxt.async_support.coinegg import coinegg                            # noqa: F401
from ccxt.async_support.coinex import coinex                              # noqa: F401
from ccxt.async_support.coinfalcon import coinfalcon                      # noqa: F401
from ccxt.async_support.coinfloor import coinfloor                        # noqa: F401
from ccxt.async_support.coingi import coingi                              # noqa: F401
from ccxt.async_support.coinmarketcap import coinmarketcap                # noqa: F401
from ccxt.async_support.coinmate import coinmate                          # noqa: F401
from ccxt.async_support.coinone import coinone                            # noqa: F401
from ccxt.async_support.coinspot import coinspot                          # noqa: F401
from ccxt.async_support.coolcoin import coolcoin                          # noqa: F401
from ccxt.async_support.coss import coss                                  # noqa: F401
from ccxt.async_support.crex24 import crex24                              # noqa: F401
from ccxt.async_support.deribit import deribit                            # noqa: F401
from ccxt.async_support.digifinex import digifinex                        # noqa: F401
from ccxt.async_support.dsx import dsx                                    # noqa: F401
from ccxt.async_support.exmo import exmo                                  # noqa: F401
from ccxt.async_support.exx import exx                                    # noqa: F401
from ccxt.async_support.fcoin import fcoin                                # noqa: F401
from ccxt.async_support.fcoinjp import fcoinjp                            # noqa: F401
from ccxt.async_support.flowbtc import flowbtc                            # noqa: F401
from ccxt.async_support.foxbit import foxbit                              # noqa: F401
from ccxt.async_support.ftx import ftx                                    # noqa: F401
from ccxt.async_support.fybse import fybse                                # noqa: F401
from ccxt.async_support.gemini import gemini                              # noqa: F401
from ccxt.async_support.hitbtc import hitbtc                              # noqa: F401
from ccxt.async_support.hitbtc2 import hitbtc2                            # noqa: F401
from ccxt.async_support.huobipro import huobipro                          # noqa: F401
from ccxt.async_support.huobiru import huobiru                            # noqa: F401
from ccxt.async_support.ice3x import ice3x                                # noqa: F401
from ccxt.async_support.idex import idex                                  # noqa: F401
from ccxt.async_support.independentreserve import independentreserve      # noqa: F401
from ccxt.async_support.indodax import indodax                            # noqa: F401
from ccxt.async_support.itbit import itbit                                # noqa: F401
from ccxt.async_support.kkex import kkex                                  # noqa: F401
from ccxt.async_support.kuna import kuna                                  # noqa: F401
from ccxt.async_support.lakebtc import lakebtc                            # noqa: F401
from ccxt.async_support.latoken import latoken                            # noqa: F401
from ccxt.async_support.lbank import lbank                                # noqa: F401
from ccxt.async_support.liquid import liquid                              # noqa: F401
from ccxt.async_support.livecoin import livecoin                          # noqa: F401
from ccxt.async_support.luno import luno                                  # noqa: F401
from ccxt.async_support.lykke import lykke                                # noqa: F401
from ccxt.async_support.mercado import mercado                            # noqa: F401
from ccxt.async_support.mixcoins import mixcoins                          # noqa: F401
from ccxt.async_support.oceanex import oceanex                            # noqa: F401
from ccxt.async_support.okcoincny import okcoincny                        # noqa: F401
from ccxt.async_support.okcoinusd import okcoinusd                        # noqa: F401
from ccxt.async_support.okex import okex                                  # noqa: F401
from ccxt.async_support.okex3 import okex3                                # noqa: F401
from ccxt.async_support.paymium import paymium                            # noqa: F401
from ccxt.async_support.rightbtc import rightbtc                          # noqa: F401
from ccxt.async_support.southxchange import southxchange                  # noqa: F401
from ccxt.async_support.stex import stex                                  # noqa: F401
from ccxt.async_support.stronghold import stronghold                      # noqa: F401
from ccxt.async_support.surbitcoin import surbitcoin                      # noqa: F401
from ccxt.async_support.theocean import theocean                          # noqa: F401
from ccxt.async_support.therock import therock                            # noqa: F401
from ccxt.async_support.tidebit import tidebit                            # noqa: F401
from ccxt.async_support.tidex import tidex                                # noqa: F401
from ccxt.async_support.timex import timex                                # noqa: F401
from ccxt.async_support.upbit import upbit                                # noqa: F401
from ccxt.async_support.vaultoro import vaultoro                          # noqa: F401
from ccxt.async_support.vbtc import vbtc                                  # noqa: F401
from ccxt.async_support.whitebit import whitebit                          # noqa: F401
from ccxt.async_support.xbtce import xbtce                                # noqa: F401
from ccxt.async_support.yobit import yobit                                # noqa: F401
from ccxt.async_support.zaif import zaif                                  # noqa: F401
from ccxt.async_support.zb import zb                                      # noqa: F401

# CCXT Pro exchanges

from ccxtpro.binance import binance                                       # noqa: F401
from ccxtpro.bitfinex import bitfinex                                     # noqa: F401
from ccxtpro.bitmex import bitmex                                         # noqa: F401
from ccxtpro.bittrex import bittrex                                       # noqa: F401
from ccxtpro.coinbaseprime import coinbaseprime                           # noqa: F401
from ccxtpro.coinbasepro import coinbasepro                               # noqa: F401
from ccxtpro.gateio import gateio                                         # noqa: F401
from ccxtpro.kraken import kraken                                         # noqa: F401
from ccxtpro.kucoin import kucoin                                         # noqa: F401
from ccxtpro.poloniex import poloniex                                     # noqa: F401

__all__ = ccxt.__all__
