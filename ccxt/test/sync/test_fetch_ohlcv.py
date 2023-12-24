import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-

from ccxt.test.base import test_ohlcv  # noqa E402

def test_fetch_ohlcv(exchange, skipped_properties, symbol):
    method = 'fetchOHLCV'
    timeframe_keys = list(exchange.timeframes.keys())
    assert len(timeframe_keys), exchange.id + ' ' + method + ' - no timeframes found'
    # prefer 1m timeframe if available, otherwise return the first one
    chosen_timeframe_key = '1m'
    if not exchange.in_array(chosen_timeframe_key, timeframe_keys):
        chosen_timeframe_key = timeframe_keys[0]
    limit = 10
    duration = exchange.parse_timeframe(chosen_timeframe_key)
    since = exchange.milliseconds() - duration * limit * 1000 - 1000
    ohlcvs = exchange.fetch_ohlcv(symbol, chosen_timeframe_key, since, limit)
    assert isinstance(ohlcvs, list), exchange.id + ' ' + method + ' must return an array, returned ' + exchange.json(ohlcvs)
    now = exchange.milliseconds()
    for i in range(0, len(ohlcvs)):
        test_ohlcv(exchange, skipped_properties, method, ohlcvs[i], symbol, now)
