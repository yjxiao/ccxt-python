import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.test.base import test_trading_fee  # noqa E402


async def test_fetch_trading_fee(exchange, skipped_properties, symbol):
    method = 'fetchTradingFee'
    fee = await exchange.fetch_trading_fee(symbol)
    assert isinstance(fee, dict), exchange.id + ' ' + method + ' ' + symbol + ' must return an object. ' + exchange.json(fee)
    test_trading_fee(exchange, skipped_properties, method, symbol, fee)
