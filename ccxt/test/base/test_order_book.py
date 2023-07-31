import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.base.precise import Precise  # noqa E402
from ccxt.test.base import test_shared_methods  # noqa E402


def test_order_book(exchange, skipped_properties, method, entry, symbol):
    format = {
        'symbol': 'ETH/BTC',
        'asks': [[exchange.parse_number('1.24'), exchange.parse_number('0.453')], [exchange.parse_number('1.25'), exchange.parse_number('0.157')]],
        'bids': [[exchange.parse_number('1.23'), exchange.parse_number('0.123')], [exchange.parse_number('1.22'), exchange.parse_number('0.543')]],
        'timestamp': 1504224000000,
        'datetime': '2017-09-01T00:00:00',
        'nonce': 134234234,
    }
    empty_allowed_for = ['symbol', 'nonce', 'datetime', 'timestamp']  # todo: make timestamp required
    test_shared_methods.assert_structure(exchange, skipped_properties, method, entry, format, empty_allowed_for)
    test_shared_methods.assert_timestamp(exchange, skipped_properties, method, entry)
    test_shared_methods.assert_symbol(exchange, skipped_properties, method, entry, 'symbol', symbol)
    log_text = test_shared_methods.log_template(exchange, method, entry)
    #
    bids = entry['bids']
    bids_length = len(bids)
    for i in range(0, bids_length):
        current_bid_string = exchange.safe_string(bids[i], 0)
        next_i = i + 1
        if bids_length > next_i:
            next_bid_string = exchange.safe_string(bids[next_i], 0)
            assert Precise.string_gt(current_bid_string, next_bid_string), 'current bid should be > than the next one: ' + current_bid_string + '>' + next_bid_string + log_text
        test_shared_methods.assert_greater(exchange, skipped_properties, method, bids[i], 0, '0')
        test_shared_methods.assert_greater(exchange, skipped_properties, method, bids[i], 1, '0')
    asks = entry['asks']
    asks_length = len(asks)
    for i in range(0, asks_length):
        current_ask_string = exchange.safe_string(asks[i], 0)
        next_i = i + 1
        if asks_length > next_i:
            next_ask_string = exchange.safe_string(asks[next_i], 0)
            assert Precise.string_lt(current_ask_string, next_ask_string), 'current ask should be < than the next one: ' + current_ask_string + '<' + next_ask_string + log_text
        test_shared_methods.assert_greater(exchange, skipped_properties, method, asks[i], 0, '0')
        test_shared_methods.assert_greater(exchange, skipped_properties, method, asks[i], 1, '0')
    if bids_length and asks_length:
        first_bid = exchange.safe_string(bids[0], 0)
        first_ask = exchange.safe_string(asks[0], 0)
        # check bid-ask spread
        assert Precise.string_lt(first_bid, first_ask), 'bids[0][0] (' + first_ask + ') should be < than asks[0][0] (' + first_ask + ')' + log_text
