from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_public_currency = publicGetPublicCurrency = Entry('public/currency', 'public', 'GET', {'cost': 10})
    public_get_public_symbol = publicGetPublicSymbol = Entry('public/symbol', 'public', 'GET', {'cost': 10})
    public_get_public_ticker = publicGetPublicTicker = Entry('public/ticker', 'public', 'GET', {'cost': 10})
    public_get_public_price_rate = publicGetPublicPriceRate = Entry('public/price/rate', 'public', 'GET', {'cost': 10})
    public_get_public_trades = publicGetPublicTrades = Entry('public/trades', 'public', 'GET', {'cost': 10})
    public_get_public_orderbook = publicGetPublicOrderbook = Entry('public/orderbook', 'public', 'GET', {'cost': 10})
    public_get_public_candles = publicGetPublicCandles = Entry('public/candles', 'public', 'GET', {'cost': 10})
    public_get_public_futures_info = publicGetPublicFuturesInfo = Entry('public/futures/info', 'public', 'GET', {'cost': 10})
    public_get_public_futures_history_funding = publicGetPublicFuturesHistoryFunding = Entry('public/futures/history/funding', 'public', 'GET', {'cost': 10})
    public_get_public_futures_candles_index_price = publicGetPublicFuturesCandlesIndexPrice = Entry('public/futures/candles/index_price', 'public', 'GET', {'cost': 10})
    public_get_public_futures_candles_mark_price = publicGetPublicFuturesCandlesMarkPrice = Entry('public/futures/candles/mark_price', 'public', 'GET', {'cost': 10})
    public_get_public_futures_candles_premium_index = publicGetPublicFuturesCandlesPremiumIndex = Entry('public/futures/candles/premium_index', 'public', 'GET', {'cost': 10})
    public_get_public_futures_candles_open_interest = publicGetPublicFuturesCandlesOpenInterest = Entry('public/futures/candles/open_interest', 'public', 'GET', {'cost': 10})
    private_get_spot_balance = privateGetSpotBalance = Entry('spot/balance', 'private', 'GET', {'cost': 15})
    private_get_spot_order = privateGetSpotOrder = Entry('spot/order', 'private', 'GET', {'cost': 15})
    private_get_spot_order_client_order_id = privateGetSpotOrderClientOrderId = Entry('spot/order/{client_order_id}', 'private', 'GET', {'cost': 15})
    private_get_spot_fee = privateGetSpotFee = Entry('spot/fee', 'private', 'GET', {'cost': 15})
    private_get_spot_fee_symbol = privateGetSpotFeeSymbol = Entry('spot/fee/{symbol}', 'private', 'GET', {'cost': 15})
    private_get_spot_history_order = privateGetSpotHistoryOrder = Entry('spot/history/order', 'private', 'GET', {'cost': 15})
    private_get_spot_history_trade = privateGetSpotHistoryTrade = Entry('spot/history/trade', 'private', 'GET', {'cost': 15})
    private_get_margin_account = privateGetMarginAccount = Entry('margin/account', 'private', 'GET', {'cost': 15})
    private_get_margin_account_isolated_symbol = privateGetMarginAccountIsolatedSymbol = Entry('margin/account/isolated/{symbol}', 'private', 'GET', {'cost': 15})
    private_get_margin_order = privateGetMarginOrder = Entry('margin/order', 'private', 'GET', {'cost': 15})
    private_get_margin_order_client_order_id = privateGetMarginOrderClientOrderId = Entry('margin/order/{client_order_id}', 'private', 'GET', {'cost': 15})
    private_get_margin_history_clearing = privateGetMarginHistoryClearing = Entry('margin/history/clearing', 'private', 'GET', {'cost': 15})
    private_get_margin_history_order = privateGetMarginHistoryOrder = Entry('margin/history/order', 'private', 'GET', {'cost': 15})
    private_get_margin_history_positions = privateGetMarginHistoryPositions = Entry('margin/history/positions', 'private', 'GET', {'cost': 15})
    private_get_margin_history_trade = privateGetMarginHistoryTrade = Entry('margin/history/trade', 'private', 'GET', {'cost': 15})
    private_get_futures_balance = privateGetFuturesBalance = Entry('futures/balance', 'private', 'GET', {'cost': 15})
    private_get_futures_account = privateGetFuturesAccount = Entry('futures/account', 'private', 'GET', {'cost': 15})
    private_get_futures_account_isolated_symbol = privateGetFuturesAccountIsolatedSymbol = Entry('futures/account/isolated/{symbol}', 'private', 'GET', {'cost': 15})
    private_get_futures_order = privateGetFuturesOrder = Entry('futures/order', 'private', 'GET', {'cost': 15})
    private_get_futures_order_client_order_id = privateGetFuturesOrderClientOrderId = Entry('futures/order/{client_order_id}', 'private', 'GET', {'cost': 15})
    private_get_futures_fee = privateGetFuturesFee = Entry('futures/fee', 'private', 'GET', {'cost': 15})
    private_get_futures_fee_symbol = privateGetFuturesFeeSymbol = Entry('futures/fee/{symbol}', 'private', 'GET', {'cost': 15})
    private_get_futures_history_clearing = privateGetFuturesHistoryClearing = Entry('futures/history/clearing', 'private', 'GET', {'cost': 15})
    private_get_futures_history_order = privateGetFuturesHistoryOrder = Entry('futures/history/order', 'private', 'GET', {'cost': 15})
    private_get_futures_history_positions = privateGetFuturesHistoryPositions = Entry('futures/history/positions', 'private', 'GET', {'cost': 15})
    private_get_futures_history_trade = privateGetFuturesHistoryTrade = Entry('futures/history/trade', 'private', 'GET', {'cost': 15})
    private_get_wallet_balance = privateGetWalletBalance = Entry('wallet/balance', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_address = privateGetWalletCryptoAddress = Entry('wallet/crypto/address', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_address_recent_deposit = privateGetWalletCryptoAddressRecentDeposit = Entry('wallet/crypto/address/recent-deposit', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_address_recent_withdraw = privateGetWalletCryptoAddressRecentWithdraw = Entry('wallet/crypto/address/recent-withdraw', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_address_check_mine = privateGetWalletCryptoAddressCheckMine = Entry('wallet/crypto/address/check-mine', 'private', 'GET', {'cost': 15})
    private_get_wallet_transactions = privateGetWalletTransactions = Entry('wallet/transactions', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_check_offchain_available = privateGetWalletCryptoCheckOffchainAvailable = Entry('wallet/crypto/check-offchain-available', 'private', 'GET', {'cost': 15})
    private_get_wallet_crypto_fee_estimate = privateGetWalletCryptoFeeEstimate = Entry('wallet/crypto/fee/estimate', 'private', 'GET', {'cost': 15})
    private_get_sub_account = privateGetSubAccount = Entry('sub-account', 'private', 'GET', {'cost': 15})
    private_get_sub_account_acl = privateGetSubAccountAcl = Entry('sub-account/acl', 'private', 'GET', {'cost': 15})
    private_get_sub_account_balance_subaccid = privateGetSubAccountBalanceSubAccID = Entry('sub-account/balance/{subAccID}', 'private', 'GET', {'cost': 15})
    private_get_sub_account_crypto_address_subaccid_currency = privateGetSubAccountCryptoAddressSubAccIDCurrency = Entry('sub-account/crypto/address/{subAccID}/{currency}', 'private', 'GET', {'cost': 15})
    private_post_spot_order = privatePostSpotOrder = Entry('spot/order', 'private', 'POST', {'cost': 1})
    private_post_margin_order = privatePostMarginOrder = Entry('margin/order', 'private', 'POST', {'cost': 1})
    private_post_futures_order = privatePostFuturesOrder = Entry('futures/order', 'private', 'POST', {'cost': 1})
    private_post_wallet_convert = privatePostWalletConvert = Entry('wallet/convert', 'private', 'POST', {'cost': 15})
    private_post_wallet_crypto_address = privatePostWalletCryptoAddress = Entry('wallet/crypto/address', 'private', 'POST', {'cost': 15})
    private_post_wallet_crypto_withdraw = privatePostWalletCryptoWithdraw = Entry('wallet/crypto/withdraw', 'private', 'POST', {'cost': 15})
    private_post_wallet_transfer = privatePostWalletTransfer = Entry('wallet/transfer', 'private', 'POST', {'cost': 15})
    private_post_sub_account_freeze = privatePostSubAccountFreeze = Entry('sub-account/freeze', 'private', 'POST', {'cost': 15})
    private_post_sub_account_activate = privatePostSubAccountActivate = Entry('sub-account/activate', 'private', 'POST', {'cost': 15})
    private_post_sub_account_transfer = privatePostSubAccountTransfer = Entry('sub-account/transfer', 'private', 'POST', {'cost': 15})
    private_post_sub_account_acl = privatePostSubAccountAcl = Entry('sub-account/acl', 'private', 'POST', {'cost': 15})
    private_patch_spot_order_client_order_id = privatePatchSpotOrderClientOrderId = Entry('spot/order/{client_order_id}', 'private', 'PATCH', {'cost': 1})
    private_patch_margin_order_client_order_id = privatePatchMarginOrderClientOrderId = Entry('margin/order/{client_order_id}', 'private', 'PATCH', {'cost': 1})
    private_patch_futures_order_client_order_id = privatePatchFuturesOrderClientOrderId = Entry('futures/order/{client_order_id}', 'private', 'PATCH', {'cost': 1})
    private_delete_spot_order = privateDeleteSpotOrder = Entry('spot/order', 'private', 'DELETE', {'cost': 1})
    private_delete_spot_order_client_order_id = privateDeleteSpotOrderClientOrderId = Entry('spot/order/{client_order_id}', 'private', 'DELETE', {'cost': 1})
    private_delete_margin_position = privateDeleteMarginPosition = Entry('margin/position', 'private', 'DELETE', {'cost': 1})
    private_delete_margin_position_isolated_symbol = privateDeleteMarginPositionIsolatedSymbol = Entry('margin/position/isolated/{symbol}', 'private', 'DELETE', {'cost': 1})
    private_delete_margin_order = privateDeleteMarginOrder = Entry('margin/order', 'private', 'DELETE', {'cost': 1})
    private_delete_margin_order_client_order_id = privateDeleteMarginOrderClientOrderId = Entry('margin/order/{client_order_id}', 'private', 'DELETE', {'cost': 1})
    private_delete_futures_position = privateDeleteFuturesPosition = Entry('futures/position', 'private', 'DELETE', {'cost': 1})
    private_delete_futures_position_isolated_symbol = privateDeleteFuturesPositionIsolatedSymbol = Entry('futures/position/isolated/{symbol}', 'private', 'DELETE', {'cost': 1})
    private_delete_futures_order = privateDeleteFuturesOrder = Entry('futures/order', 'private', 'DELETE', {'cost': 1})
    private_delete_futures_order_client_order_id = privateDeleteFuturesOrderClientOrderId = Entry('futures/order/{client_order_id}', 'private', 'DELETE', {'cost': 1})
    private_delete_wallet_crypto_withdraw_id = privateDeleteWalletCryptoWithdrawId = Entry('wallet/crypto/withdraw/{id}', 'private', 'DELETE', {'cost': 1})
    private_put_margin_account_isolated_symbol = privatePutMarginAccountIsolatedSymbol = Entry('margin/account/isolated/{symbol}', 'private', 'PUT', {'cost': 1})
    private_put_futures_account_isolated_symbol = privatePutFuturesAccountIsolatedSymbol = Entry('futures/account/isolated/{symbol}', 'private', 'PUT', {'cost': 1})
    private_put_wallet_crypto_withdraw_id = privatePutWalletCryptoWithdrawId = Entry('wallet/crypto/withdraw/{id}', 'private', 'PUT', {'cost': 1})
