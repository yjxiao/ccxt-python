import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-

from ccxt.test.base import test_leverage_tier  # noqa E402

def test_fetch_market_leverage_tiers(exchange, skipped_properties, symbol):
    method = 'fetchMarketLeverageTiers'
    tiers = exchange.fetch_market_leverage_tiers(symbol)
    assert isinstance(tiers, list), exchange.id + ' ' + method + ' ' + symbol + ' must return an array. ' + exchange.json(tiers)
    array_length = len(tiers)
    assert array_length >= 1, exchange.id + ' ' + method + ' ' + symbol + ' must return an array with at least one entry. ' + exchange.json(tiers)
    for j in range(0, len(tiers)):
        test_leverage_tier(exchange, skipped_properties, method, tiers[j])
