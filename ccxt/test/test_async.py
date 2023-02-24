# -*- coding: utf-8 -*-

import argparse
import asyncio
import json
# import logging
import os
import sys
import time  # noqa: F401
from traceback import format_tb

# ------------------------------------------------------------------------------
# logging.basicConfig(level=logging.INFO)
# ------------------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root)

import ccxt.async_support as ccxt  # noqa: E402

# ------------------------------------------------------------------------------

class Argv(object):
    token_bucket = False
    sandbox = False
    privateOnly = False
    private = False
    verbose = False
    nonce = None
    exchange = None
    symbol = None
    pass

argv = Argv()
parser = argparse.ArgumentParser()
parser.add_argument('--token_bucket', action='store_true', help='enable token bucket experimental test')
parser.add_argument('--sandbox', action='store_true', help='enable sandbox mode')
parser.add_argument('--privateOnly', action='store_true', help='run private tests only')
parser.add_argument('--private', action='store_true', help='run private tests')
parser.add_argument('--verbose', action='store_true', help='enable verbose output')
parser.add_argument('--nonce', type=int, help='integer')
parser.add_argument('exchange', type=str, help='exchange id in lowercase', nargs='?')
parser.add_argument('symbol', type=str, help='symbol in uppercase', nargs='?')
parser.parse_args(namespace=argv)

token_bucket = argv.token_bucket
sandbox = argv.sandbox
privateOnly = argv.privateOnly
privateTest = argv.private
verbose = argv.verbose
nonce = argv.nonce
exchangeName = argv.exchange
exchangeSymbol = argv.symbol


exchange = getattr(ccxt, exchangeName) ({'verbose': verbose})

# ------------------------------------------------------------------------------

path = os.path.dirname(ccxt.__file__)
print(os.getcwd(), path)
print(sys.argv)
if 'site-packages' in os.path.dirname(ccxt.__file__):
    raise Exception("You are running test_async.py/test.py against a globally-installed version of the library! It was previously installed into your site-packages folder by pip or pip3. To ensure testing against the local folder uninstall it first with pip uninstall ccxt or pip3 uninstall ccxt")

# ------------------------------------------------------------------------------

# trick transpiler
is_sync = ('token'+'_'+'bucket') not in locals()

import importlib  # noqa: E402
import glob  # noqa: E402
testFiles = {}
for file_path in glob.glob(current_dir + '/test_*.py'):
    name = os.path.basename(file_path)[:-3]
    if (name != 'test_async') and (name != 'test_sync'):
        if not is_sync and '_async' in name:
            testFiles[name.replace('_async','')] = importlib.import_module(name)
        elif is_sync and '_async' not in name:
            testFiles[name] = importlib.import_module(name.replace('test_async', 'test_sync'))

# print a colored string
def dump(*args):
    print(' '.join([str(arg) for arg in args]))


# print an error string
def dump_error(*args):
    string = ' '.join([str(arg) for arg in args])
    print(string)
    sys.stderr.write(string + "\n")
    sys.stderr.flush()

Error = Exception
# ------------------------------------------------------------------------------


def handle_all_unhandled_exceptions(type, value, traceback):
    dump_error((type), (value), '\n\n' + ('\n'.join(format_tb(traceback))))
    exit(1)  # unrecoverable crash


sys.excepthook = handle_all_unhandled_exceptions

# ------------------------------------------------------------------------------

# non-transpiled commons
import re
def methodNamerInTest(methodName):
    snake_cased = re.sub(r'(?<!^)(?=[A-Z])', '_', methodName).lower()
    snake_cased = snake_cased.replace('o_h_l_c_v', 'ohlcv')
    full_name = 'test_' + snake_cased
    return full_name

targetDir = current_dir + '/../../'
envVars = {}
class emptyClass():
    pass

def io_file_exists(path):
    return os.path.isfile(path)

def io_file_read(path, decode = True):
    fs = open(path, "r")
    content = fs.read()
    if decode:
        return json.loads(content)
    else:
        return content

def exception_message (exc):
    return '[' + type(exc).__name__ + '] ' + str(exc)[0:200]

async def call_method(methodName, exchange, args):
    return await getattr(testFiles[methodName], methodName)(exchange, *args)

def add_proxy_agent (exchange, settings):
    pass

def exit_script():
    exit()

def get_exchange_prop (exchange, prop, defaultValue = None):
    return getattr(exchange,prop) if hasattr(exchange,prop) else defaultValue

def set_exchange_prop (exchange, prop, value):
    setattr(exchange, prop, value)


### AUTO-TRANSPILER-START ###
# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code


import asyncio


class testMainClass(emptyClass):

    async def init(self, exchange, symbol):
        self.expand_settings(exchange, symbol)
        await self.start_test(exchange, symbol)

    def expand_settings(self, exchange, symbol):
        exchangeId = exchange.id
        keysGlobal = targetDir + 'keys.json'
        keysLocal = targetDir + 'keys.local.json'
        fileExists = io_file_exists(keysLocal)
        keysFile = keysLocal if fileExists else keysGlobal
        allSettings = io_file_read(keysFile)
        exchangeSettings = exchange.safe_value(allSettings, exchangeId, {})
        if exchangeSettings:
            settingKeys = list(exchangeSettings.keys())
            for i in range(0, len(settingKeys)):
                key = settingKeys[i]
                if exchangeSettings[key]:
                    existing = get_exchange_prop(exchange, key, {})
                    set_exchange_prop(exchange, key, exchange.deep_extend(existing, exchangeSettings[key]))
        # credentials
        reqCreds = get_exchange_prop(exchange, 're' + 'quiredCredentials')  # dont glue the r-e-q-u-i-r-e phrase, because leads to messed up transpilation
        objkeys = list(reqCreds.keys())
        for i in range(0, len(objkeys)):
            credential = objkeys[i]
            isRequired = reqCreds[credential]
            if isRequired and get_exchange_prop(exchange, credential) is None:
                fullKey = exchangeId + '_' + credential
                credentialEnvName = fullKey.upper()  # example: KRAKEN_APIKEY
                credentialValue = envVars[credentialEnvName]
                if credentialValue:
                    set_exchange_prop(exchange, credential, credentialValue)
        # others
        if exchangeSettings and exchange.safe_value(exchangeSettings, 'skip'):
            dump('[Skipped]', 'exchange', exchangeId, 'symbol', symbol)
            exit_script()
        if exchange.alias:
            dump('[Skipped] Alias exchange. ', 'exchange', exchangeId, 'symbol', symbol)
            exit_script()
        add_proxy_agent(exchange, exchangeSettings)

    async def test_method(self, methodName, exchange, args):
        methodNameInTest = methodNamerInTest(methodName)
        skipMessage = None
        if (methodName != 'loadMarkets') and (not(methodName in exchange.has) or not exchange.has[methodName]):
            skipMessage = 'not supported'
        elif not (methodNameInTest in testFiles):
            skipMessage = 'test not available'
        if skipMessage:
            dump('[Skipping]', exchange.id, methodNameInTest, ' - ' + skipMessage)
            return
        argsStringified = '(' + ','.join(args) + ')'
        dump('[Testing]', exchange.id, methodNameInTest, argsStringified)
        try:
            return await call_method(methodNameInTest, exchange, args)
        except Exception as e:
            dump(exception_message(e), ' | Exception from: ', exchange.id, methodNameInTest, argsStringified)
            raise e

    async def test_safe(self, methodName, exchange, args):
        try:
            await self.test_method(methodName, exchange, args)
            return True
        except Exception as e:
            return False

    async def run_public_tests(self, exchange, symbol):
        tests = {
            'loadMarkets': [],
            'fetchCurrencies': [],
            'fetchTicker': [symbol],
            'fetchTickers': [symbol],
            'fetchOHLCV': [symbol],
            'fetchTrades': [symbol],
            'fetchOrderBook': [symbol],
            'fetchL2OrderBook': [symbol],
            'fetchOrderBooks': [],
            'fetchBidsAsks': [],
            'fetchStatus': [],
            'fetchTime': [],
        }
        market = exchange.market(symbol)
        isSpot = market['spot']
        if isSpot:
            tests['fetchCurrencies'] = []
        else:
            tests['fetchFundingRates'] = [symbol]
            tests['fetchFundingRate'] = [symbol]
            tests['fetchFundingRateHistory'] = [symbol]
            tests['fetchIndexOHLCV'] = [symbol]
            tests['fetchMarkOHLCV'] = [symbol]
            tests['fetchPremiumIndexOHLCV'] = [symbol]
        testNames = list(tests.keys())
        promises = []
        for i in range(0, len(testNames)):
            testName = testNames[i]
            testArgs = tests[testName]
            promises.append(self.test_safe(testName, exchange, testArgs))
        await asyncio.gather(*promises)

    async def load_exchange(self, exchange):
        markets = await exchange.load_markets()
        assert isinstance(exchange.markets, dict), '.markets is not an object'
        assert isinstance(exchange.symbols, list), '.symbols is not an array'
        symbolsLength = len(exchange.symbols)
        marketKeys = list(exchange.markets.keys())
        marketKeysLength = len(marketKeys)
        assert symbolsLength > 0, '.symbols count <= 0(less than or equal to zero)'
        assert marketKeysLength > 0, '.markets objects keys length <= 0(less than or equal to zero)'
        assert symbolsLength == marketKeysLength, 'number of .symbols is not equal to the number of .markets'
        symbols = [
            'BTC/CNY',
            'BTC/USD',
            'BTC/USDT',
            'BTC/EUR',
            'BTC/ETH',
            'ETH/BTC',
            'BTC/JPY',
            'ETH/EUR',
            'ETH/JPY',
            'ETH/CNY',
            'ETH/USD',
            'LTC/CNY',
            'DASH/BTC',
            'DOGE/BTC',
            'BTC/AUD',
            'BTC/PLN',
            'USD/SLL',
            'BTC/RUB',
            'BTC/UAH',
            'LTC/BTC',
            'EUR/USD',
        ]
        resultSymbols = []
        exchangeSpecificSymbols = exchange.symbols
        for i in range(0, len(exchangeSpecificSymbols)):
            symbol = exchangeSpecificSymbols[i]
            if exchange.inArray(symbol, symbols):
                resultSymbols.append(symbol)
        resultMsg = ''
        resultLength = len(resultSymbols)
        exchangeSymbolsLength = len(exchange.symbols)
        if resultLength > 0:
            if exchangeSymbolsLength > resultLength:
                resultMsg = ', '.join(resultSymbols) + ' + more...'
            else:
                resultMsg = ', '.join(resultSymbols)
        dump('Exchange loaded', exchangeSymbolsLength, 'symbols', resultMsg)

    def get_test_symbol(self, exchange, symbols):
        symbol = None
        for i in range(0, len(symbols)):
            s = symbols[i]
            market = exchange.safe_value(exchange.markets, s)
            if market is not None:
                active = exchange.safe_value(market, 'active')
                if active or (active is None):
                    symbol = s
                    break
        return symbol

    def get_exchange_code(self, exchange, codes=None):
        if codes is None:
            codes = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'EOS', 'BNB', 'BSV', 'USDT']
        code = codes[0]
        for i in range(0, len(codes)):
            if codes[i] in exchange.currencies:
                return codes[i]
        return code

    def get_symbols_from_exchange(self, exchange, spot=True):
        res = []
        markets = exchange.markets
        keys = list(markets.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            market = markets[key]
            if spot and market['spot']:
                res.append(key)
            elif not spot and not market['spot']:
                res.append(key)
        return res

    def get_valid_symbol(self, exchange, spot=True):
        codes = [
            'BTC',
            'ETH',
            'XRP',
            'LTC',
            'BCH',
            'EOS',
            'BNB',
            'BSV',
            'USDT',
            'ATOM',
            'BAT',
            'BTG',
            'DASH',
            'DOGE',
            'ETC',
            'IOTA',
            'LSK',
            'MKR',
            'NEO',
            'PAX',
            'QTUM',
            'TRX',
            'TUSD',
            'USD',
            'USDC',
            'WAVES',
            'XEM',
            'XMR',
            'ZEC',
            'ZRX',
        ]
        spotSymbols = [
            'BTC/USD',
            'BTC/USDT',
            'BTC/CNY',
            'BTC/EUR',
            'BTC/ETH',
            'ETH/BTC',
            'ETH/USD',
            'ETH/USDT',
            'BTC/JPY',
            'LTC/BTC',
            'ZRX/WETH',
            'EUR/USD',
        ]
        swapSymbols = [
            'BTC/USDT:USDT',
            'BTC/USD:USD',
            'ETH/USDT:USDT',
            'ETH/USD:USD',
            'LTC/USDT:USDT',
            'DOGE/USDT:USDT',
            'ADA/USDT:USDT',
            'BTC/USD:BTC',
            'ETH/USD:ETH',
        ]
        targetSymbols = spotSymbols if spot else swapSymbols
        symbol = self.get_test_symbol(exchange, targetSymbols)
        exchangeMarkets = self.get_symbols_from_exchange(exchange, spot)
        # if symbols wasn't found from above hardcoded list, then try to locate any symbol which has our target hardcoded 'base' code
        if symbol is None:
            for i in range(0, len(codes)):
                currentCode = codes[i]
                marketsForCurrentCode = exchange.filter_by(exchangeMarkets, 'base', currentCode)
                symbolsForCurrentCode = list(marketsForCurrentCode.keys())
                if len(symbolsForCurrentCode):
                    symbol = self.get_test_symbol(exchange, symbolsForCurrentCode)
                    break
        # if there wasn't found any symbol with our hardcoded 'base' code, then just try to find symbols that are 'active'
        if symbol is None:
            activeMarkets = exchange.filter_by(exchangeMarkets, 'active', True)
            activeSymbols = list(activeMarkets.keys())
            symbol = self.get_test_symbol(exchange, activeSymbols)
        if symbol is None:
            first = exchangeMarkets[0]
            if first is not None:
                symbol = first['symbol']
        return symbol

    async def test_exchange(self, exchange, providedSymbol=None):
        spotSymbol = None
        swapSymbol = None
        if providedSymbol is not None:
            market = exchange.market(providedSymbol)
            if market['spot']:
                spotSymbol = providedSymbol
            else:
                swapSymbol = providedSymbol
        else:
            spotSymbol = self.get_valid_symbol(exchange, True)
            swapSymbol = self.get_valid_symbol(exchange, False)
        if spotSymbol is not None:
            dump('Selected SPOT SYMBOL:', spotSymbol)
        if swapSymbol is not None:
            dump('Selected SWAP SYMBOL:', swapSymbol)
        if not privateOnly:
            if exchange.has['spot'] and spotSymbol is not None:
                exchange.options['type'] = 'spot'
                await self.run_public_tests(exchange, spotSymbol)
            if exchange.has['swap'] and swapSymbol is not None:
                exchange.options['type'] = 'swap'
                await self.run_public_tests(exchange, swapSymbol)
        if privateTest or privateOnly:
            if exchange.has['spot'] and spotSymbol is not None:
                exchange.options['defaultType'] = 'spot'
                await self.run_private_tests(exchange, spotSymbol)
            if exchange.has['swap'] and swapSymbol is not None:
                exchange.options['defaultType'] = 'swap'
                await self.run_private_tests(exchange, swapSymbol)

    async def run_private_tests(self, exchange, symbol):
        if not exchange.check_required_credentials(False):
            dump('[Skipped]', 'Keys not found, skipping private tests')
            return
        code = self.get_exchange_code(exchange)
        # if exchange.extendedTest:
        #     await test('InvalidNonce', exchange, symbol)
        #     await test('OrderNotFound', exchange, symbol)
        #     await test('InvalidOrder', exchange, symbol)
        #     await test('InsufficientFunds', exchange, symbol, balance)  # danger zone - won't execute with non-empty balance
        # }
        tests = {
            'signIn': [exchange],
            'fetchBalance': [exchange],
            'fetchAccounts': [exchange],
            'fetchTransactionFees': [exchange],
            'fetchTradingFees': [exchange],
            'fetchStatus': [exchange],
            'fetchOrders': [exchange, symbol],
            'fetchOpenOrders': [exchange, symbol],
            'fetchClosedOrders': [exchange, symbol],
            'fetchMyTrades': [exchange, symbol],
            'fetchLeverageTiers': [exchange, symbol],
            'fetchLedger': [exchange, code],
            'fetchTransactions': [exchange, code],
            'fetchDeposits': [exchange, code],
            'fetchWithdrawals': [exchange, code],
            'fetchBorrowRates': [exchange, code],
            'fetchBorrowRate': [exchange, code],
            'fetchBorrowInterest': [exchange, code, symbol],
            'addMargin': [exchange, symbol],
            'reduceMargin': [exchange, symbol],
            'setMargin': [exchange, symbol],
            'setMarginMode': [exchange, symbol],
            'setLeverage': [exchange, symbol],
            'cancelAllOrders': [exchange, symbol],
            'cancelOrder': [exchange, symbol],
            'cancelOrders': [exchange, symbol],
            'fetchCanceledOrders': [exchange, symbol],
            'fetchClosedOrder': [exchange, symbol],
            'fetchOpenOrder': [exchange, symbol],
            'fetchOrder': [exchange, symbol],
            'fetchOrderTrades': [exchange, symbol],
            'fetchPosition': [exchange, symbol],
            'fetchDeposit': [exchange, code],
            'createDepositAddress': [exchange, code],
            'fetchDepositAddress': [exchange, code],
            'fetchDepositAddresses': [exchange, code],
            'fetchDepositAddressesByNetwork': [exchange, code],
            'editOrder': [exchange, symbol],
            'fetchBorrowRateHistory': [exchange, symbol],
            'fetchBorrowRatesPerSymbol': [exchange, symbol],
            'fetchLedgerEntry': [exchange, code],
            'fetchWithdrawal': [exchange, code],
            'transfer': [exchange, code],
            'withdraw': [exchange, code],
        }
        market = exchange.market(symbol)
        isSpot = market['spot']
        if isSpot:
            tests['fetchCurrencies'] = [exchange, symbol]
        else:
            # derivatives only
            tests['fetchPositions'] = [exchange, [symbol]]
            tests['fetchPosition'] = [exchange, symbol]
            tests['fetchPositionRisk'] = [exchange, symbol]
            tests['setPositionMode'] = [exchange, symbol]
            tests['setMarginMode'] = [exchange, symbol]
            tests['fetchOpenInterestHistory'] = [exchange, symbol]
            tests['fetchFundingRateHistory'] = [exchange, symbol]
            tests['fetchFundingHistory'] = [exchange, symbol]
        testNames = list(tests.keys())
        promises = []
        for i in range(0, len(testNames)):
            testName = testNames[i]
            testArgs = tests[testName]
            promises.append(self.test_safe(testName, exchange, testArgs))
        results = await asyncio.gather(*promises)
        errors = []
        for i in range(0, len(testNames)):
            testName = testNames[i]
            success = results[i]
            if not success:
                errors.append(testName)
        if len(errors) > 0:
            raise Error('Failed private tests [' + market['type'] + ']: ' + ', '.join(errors))

    async def start_test(self, exchange, symbol):
        # we don't need to test aliases
        if exchange.alias:
            return
        if sandbox or get_exchange_prop(exchange, 'sandbox'):
            exchange.set_sandbox_mode(True)
        await self.load_exchange(exchange)
        await self.test_exchange(exchange, symbol)

### AUTO-TRANSPILER-END ###

if __name__ == '__main__':
    asyncio.run(testMainClass().init(exchange, exchangeSymbol))
