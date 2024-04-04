import ccxt

exchange = ccxt.binance()
data = exchange.fetch_premium_index_ohlcv("ETHUSDT")
print(data[0])