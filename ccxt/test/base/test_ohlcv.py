import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.test.base import test_shared_methods  # noqa E402


def test_ohlcv(exchange, skipped_properties, method, entry, symbol, now):
    format = [1638230400000, exchange.parse_number('0.123'), exchange.parse_number('0.125'), exchange.parse_number('0.121'), exchange.parse_number('0.122'), exchange.parse_number('123.456')]
    empty_not_allowed_for = [0, 1, 2, 3, 4, 5]
    test_shared_methods.assert_structure(exchange, skipped_properties, method, entry, format, empty_not_allowed_for)
    test_shared_methods.assert_timestamp(exchange, skipped_properties, method, entry, now, 0)
    log_text = test_shared_methods.log_template(exchange, method, entry)
    #
    length = len(entry)
    assert length >= 6, 'ohlcv array length should be >= 6;' + log_text
    high = exchange.safe_string(entry, 2)
    low = exchange.safe_string(entry, 3)
    test_shared_methods.assert_less_or_equal(exchange, skipped_properties, method, entry, '1', high)
    test_shared_methods.assert_greater_or_equal(exchange, skipped_properties, method, entry, '1', low)
    test_shared_methods.assert_less_or_equal(exchange, skipped_properties, method, entry, '4', high)
    test_shared_methods.assert_greater_or_equal(exchange, skipped_properties, method, entry, '4', low)
    assert (symbol is None) or (isinstance(symbol, str)), 'symbol ' + symbol + ' is incorrect' + log_text  # todo: check with standard symbol check
