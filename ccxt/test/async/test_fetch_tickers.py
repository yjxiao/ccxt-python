import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-

from ccxt.test.base import test_ticker  # noqa E402

async def test_fetch_tickers(exchange, skipped_properties, symbol):
    method = 'fetchTickers'
    # log ('fetching all tickers at once...')
    tickers = None
    checked_symbol = None
    try:
        tickers = await exchange.fetch_tickers()
    except Exception as e:
        tickers = await exchange.fetch_tickers([symbol])
        checked_symbol = symbol
    assert isinstance(tickers, dict), exchange.id + ' ' + method + ' ' + checked_symbol + ' must return an object. ' + exchange.json(tickers)
    values = list(tickers.values())
    for i in range(0, len(values)):
        ticker = values[i]
        test_ticker(exchange, skipped_properties, method, ticker, checked_symbol)
