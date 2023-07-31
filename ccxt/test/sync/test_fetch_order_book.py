import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.test.base import test_order_book  # noqa E402


def test_fetch_order_book(exchange, skipped_properties, symbol):
    method = 'fetchOrderBook'
    orderbook = exchange.fetch_order_book(symbol)
    test_order_book(exchange, skipped_properties, method, orderbook, symbol)
