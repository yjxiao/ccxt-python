import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa F401
from ccxt.base.decimal_to_precision import TRUNCATE              # noqa F401
from ccxt.base.decimal_to_precision import ROUND                 # noqa F401
from ccxt.base.decimal_to_precision import DECIMAL_PLACES        # noqa F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO         # noqa F401
from ccxt.base.decimal_to_precision import NO_PADDING            # noqa F401

# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# number_to_string works, not supported in Python and PHP yet

# assert(number_to_string(-7.9e-7) == '-0.0000007899999999999999')
# assert(number_to_string( 7.9e-7) ==  '0.0000007899999999999999')
# assert(number_to_string(-12.345) == '-12.345')
# assert(number_to_string( 12.345) == '12.345')
# assert(number_to_string(0) == '0')

# ----------------------------------------------------------------------------
# testDecimalToPrecisionTruncationToNDigitsAfterDot

assert(decimal_to_precision('12.3456000', TRUNCATE, 100, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', TRUNCATE, 100, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', TRUNCATE, 4, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', TRUNCATE, 3, DECIMAL_PLACES) == '12.345')
assert(decimal_to_precision('12.3456', TRUNCATE, 2, DECIMAL_PLACES) == '12.34')
assert(decimal_to_precision('12.3456', TRUNCATE, 1, DECIMAL_PLACES) == '12.3')
assert(decimal_to_precision('12.3456', TRUNCATE, 0, DECIMAL_PLACES) == '12')

# assert(decimal_to_precision('12.3456', TRUNCATE, -1, DECIMAL_PLACES) == '10')  # not yet supported
# assert(decimal_to_precision('123.456', TRUNCATE, -2, DECIMAL_PLACES) == '120')  # not yet supported
# assert(decimal_to_precision('123.456', TRUNCATE, -3, DECIMAL_PLACES) == '100')  # not yet supported

assert(decimal_to_precision('0', TRUNCATE, 0, DECIMAL_PLACES) == '0')

# ----------------------------------------------------------------------------
# testDecimalToPrecisionTruncationToNSignificantDigits

assert(decimal_to_precision('0.000123456700', TRUNCATE, 100, SIGNIFICANT_DIGITS) == '0.0001234567')
assert(decimal_to_precision('0.0001234567', TRUNCATE, 100, SIGNIFICANT_DIGITS) == '0.0001234567')
assert(decimal_to_precision('0.0001234567', TRUNCATE, 7, SIGNIFICANT_DIGITS) == '0.0001234567')

assert(decimal_to_precision('0.000123456', TRUNCATE, 6, SIGNIFICANT_DIGITS) == '0.000123456')
assert(decimal_to_precision('0.000123456', TRUNCATE, 5, SIGNIFICANT_DIGITS) == '0.00012345')
assert(decimal_to_precision('0.000123456', TRUNCATE, 2, SIGNIFICANT_DIGITS) == '0.00012')
assert(decimal_to_precision('0.000123456', TRUNCATE, 1, SIGNIFICANT_DIGITS) == '0.0001')

assert(decimal_to_precision('123.0000987654', TRUNCATE, 10, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '123.0000987')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 8, SIGNIFICANT_DIGITS) == '123.00009')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 7, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '123.0000')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 6, SIGNIFICANT_DIGITS) == '123')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 5, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '123.00')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 4, SIGNIFICANT_DIGITS) == '123')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 4, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '123.0')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 3, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '123')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 2, SIGNIFICANT_DIGITS) == '120')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 1, SIGNIFICANT_DIGITS) == '100')
assert(decimal_to_precision('123.0000987654', TRUNCATE, 1, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '100')

assert(decimal_to_precision('1234.69', TRUNCATE, 0, SIGNIFICANT_DIGITS) == '0')
assert(decimal_to_precision('1234.69', TRUNCATE, 0, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '0')

# ----------------------------------------------------------------------------
# testDecimalToPrecisionRoundingToNDigitsAfterDot

assert(decimal_to_precision('12.3456000', ROUND, 100, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', ROUND, 100, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', ROUND, 4, DECIMAL_PLACES) == '12.3456')
assert(decimal_to_precision('12.3456', ROUND, 3, DECIMAL_PLACES) == '12.346')
assert(decimal_to_precision('12.3456', ROUND, 2, DECIMAL_PLACES) == '12.35')
assert(decimal_to_precision('12.3456', ROUND, 1, DECIMAL_PLACES) == '12.3')
assert(decimal_to_precision('12.3456', ROUND, 0, DECIMAL_PLACES) == '12')

# assert(decimal_to_precision('12.3456', ROUND, -1, DECIMAL_PLACES) == '10')   # not yet supported
# assert(decimal_to_precision('123.456', ROUND, -1, DECIMAL_PLACES) == '120')  # not yet supported
# assert(decimal_to_precision('123.456', ROUND, -2, DECIMAL_PLACES) == '100')  # not yet supported

assert(decimal_to_precision('9.999', ROUND, 3, DECIMAL_PLACES) == '9.999')
assert(decimal_to_precision('9.999', ROUND, 2, DECIMAL_PLACES) == '10')
assert(decimal_to_precision('9.999', ROUND, 2, DECIMAL_PLACES, PAD_WITH_ZERO) == '10.00')
assert(decimal_to_precision('99.999', ROUND, 2, DECIMAL_PLACES, PAD_WITH_ZERO) == '100.00')
assert(decimal_to_precision('-99.999', ROUND, 2, DECIMAL_PLACES, PAD_WITH_ZERO) == '-100.00')

# ----------------------------------------------------------------------------
# testDecimalToPrecisionRoundingToNSignificantDigits

assert(decimal_to_precision('0.000123456700', ROUND, 100, SIGNIFICANT_DIGITS) == '0.0001234567')
assert(decimal_to_precision('0.0001234567', ROUND, 100, SIGNIFICANT_DIGITS) == '0.0001234567')
assert(decimal_to_precision('0.0001234567', ROUND, 7, SIGNIFICANT_DIGITS) == '0.0001234567')

assert(decimal_to_precision('0.000123456', ROUND, 6, SIGNIFICANT_DIGITS) == '0.000123456')
assert(decimal_to_precision('0.000123456', ROUND, 5, SIGNIFICANT_DIGITS) == '0.00012346')
assert(decimal_to_precision('0.000123456', ROUND, 4, SIGNIFICANT_DIGITS) == '0.0001235')
assert(decimal_to_precision('0.00012', ROUND, 2, SIGNIFICANT_DIGITS) == '0.00012')
assert(decimal_to_precision('0.0001', ROUND, 1, SIGNIFICANT_DIGITS) == '0.0001')

assert(decimal_to_precision('123.0000987654', ROUND, 7, SIGNIFICANT_DIGITS) == '123.0001')
assert(decimal_to_precision('123.0000987654', ROUND, 6, SIGNIFICANT_DIGITS) == '123')

assert(decimal_to_precision('0.00098765', ROUND, 2, SIGNIFICANT_DIGITS) == '0.00099')
assert(decimal_to_precision('0.00098765', ROUND, 2, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '0.00099')

assert(decimal_to_precision('0.00098765', ROUND, 1, SIGNIFICANT_DIGITS) == '0.001')
assert(decimal_to_precision('0.00098765', ROUND, 10, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '0.0009876500000')

assert(decimal_to_precision('0.098765', ROUND, 1, SIGNIFICANT_DIGITS, PAD_WITH_ZERO) == '0.1')

assert(decimal_to_precision('0', ROUND, 0, SIGNIFICANT_DIGITS) == '0')

# ----------------------------------------------------------------------------
# testDecimalToPrecisionNegativeNumbers

assert(decimal_to_precision('-0.123456', TRUNCATE, 5, DECIMAL_PLACES) == '-0.12345')
assert(decimal_to_precision('-0.123456', ROUND, 5, DECIMAL_PLACES) == '-0.12346')

# ----------------------------------------------------------------------------
# decimal_to_precision: without dot / trailing dot

assert(decimal_to_precision('123', TRUNCATE, 0) == '123')

assert(decimal_to_precision('123', TRUNCATE, 5, DECIMAL_PLACES) == '123')
assert(decimal_to_precision('123', TRUNCATE, 5, DECIMAL_PLACES, PAD_WITH_ZERO) == '123.00000')

assert(decimal_to_precision('123.', TRUNCATE, 0, DECIMAL_PLACES) == '123')
assert(decimal_to_precision('123.', TRUNCATE, 5, DECIMAL_PLACES, PAD_WITH_ZERO) == '123.00000')

assert(decimal_to_precision('0.', TRUNCATE, 0) == '0')
assert(decimal_to_precision('0.', TRUNCATE, 5, DECIMAL_PLACES, PAD_WITH_ZERO) == '0.00000')

# ----------------------------------------------------------------------------
# decimal_to_precision: rounding for equidistant digits

assert(decimal_to_precision('1.44', ROUND, 1, DECIMAL_PLACES) == '1.4')
assert(decimal_to_precision('1.45', ROUND, 1, DECIMAL_PLACES) == '1.5')
assert(decimal_to_precision('1.45', ROUND, 0, DECIMAL_PLACES) == '1')  # not 2

# ----------------------------------------------------------------------------
# testDecimalToPrecisionErrorHandling(todo)
#
# throws(() =>
#     decimal_to_precision('123456.789', TRUNCATE, -2, DECIMAL_PLACES),
#         'negative precision is not yet supported')
#
# throws(() =>
#     decimal_to_precision('foo'),
#         "invalid number(contains an illegal character 'f')")
