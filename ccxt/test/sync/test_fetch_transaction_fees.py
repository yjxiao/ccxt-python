import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


def test_fetch_transaction_fees(exchange, skipped_properties):
    # const method = 'fetchTransactionFees';
    # const fees = await exchange.fetchTransactionFees ();
    # const withdrawKeys = Object.keys (fees['withdraw']);
    # todo : assert each entry
    return None
