from ccxt.base.types import Entry


class ImplicitAPI:
    v1_public_get_public_auth = v1PublicGetPublicAuth = Entry('public/auth', ['v1', 'public'], 'GET', {'cost': 3.3333333333333335})
    v1_public_get_public_get_instruments = v1PublicGetPublicGetInstruments = Entry('public/get-instruments', ['v1', 'public'], 'GET', {'cost': 3.3333333333333335})
    v1_public_get_public_get_book = v1PublicGetPublicGetBook = Entry('public/get-book', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_public_get_candlestick = v1PublicGetPublicGetCandlestick = Entry('public/get-candlestick', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_public_get_trades = v1PublicGetPublicGetTrades = Entry('public/get-trades', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_public_get_tickers = v1PublicGetPublicGetTickers = Entry('public/get-tickers', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_public_get_valuations = v1PublicGetPublicGetValuations = Entry('public/get-valuations', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_public_get_expired_settlement_price = v1PublicGetPublicGetExpiredSettlementPrice = Entry('public/get-expired-settlement-price', ['v1', 'public'], 'GET', {'cost': 3.3333333333333335})
    v1_public_get_public_get_insurance = v1PublicGetPublicGetInsurance = Entry('public/get-insurance', ['v1', 'public'], 'GET', {'cost': 1})
    v1_private_post_private_set_cancel_on_disconnect = v1PrivatePostPrivateSetCancelOnDisconnect = Entry('private/set-cancel-on-disconnect', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_cancel_on_disconnect = v1PrivatePostPrivateGetCancelOnDisconnect = Entry('private/get-cancel-on-disconnect', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_user_balance = v1PrivatePostPrivateUserBalance = Entry('private/user-balance', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_user_balance_history = v1PrivatePostPrivateUserBalanceHistory = Entry('private/user-balance-history', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_positions = v1PrivatePostPrivateGetPositions = Entry('private/get-positions', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_create_order = v1PrivatePostPrivateCreateOrder = Entry('private/create-order', ['v1', 'private'], 'POST', {'cost': 0.6666666666666666})
    v1_private_post_private_create_order_list = v1PrivatePostPrivateCreateOrderList = Entry('private/create-order-list', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_cancel_order = v1PrivatePostPrivateCancelOrder = Entry('private/cancel-order', ['v1', 'private'], 'POST', {'cost': 0.6666666666666666})
    v1_private_post_private_cancel_order_list = v1PrivatePostPrivateCancelOrderList = Entry('private/cancel-order-list', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_cancel_all_orders = v1PrivatePostPrivateCancelAllOrders = Entry('private/cancel-all-orders', ['v1', 'private'], 'POST', {'cost': 0.6666666666666666})
    v1_private_post_private_close_position = v1PrivatePostPrivateClosePosition = Entry('private/close-position', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_order_history = v1PrivatePostPrivateGetOrderHistory = Entry('private/get-order-history', ['v1', 'private'], 'POST', {'cost': 100})
    v1_private_post_private_get_open_orders = v1PrivatePostPrivateGetOpenOrders = Entry('private/get-open-orders', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_order_detail = v1PrivatePostPrivateGetOrderDetail = Entry('private/get-order-detail', ['v1', 'private'], 'POST', {'cost': 0.3333333333333333})
    v1_private_post_private_get_trades = v1PrivatePostPrivateGetTrades = Entry('private/get-trades', ['v1', 'private'], 'POST', {'cost': 100})
    v1_private_post_private_change_account_leverage = v1PrivatePostPrivateChangeAccountLeverage = Entry('private/change-account-leverage', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_transactions = v1PrivatePostPrivateGetTransactions = Entry('private/get-transactions', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_create_subaccount_transfer = v1PrivatePostPrivateCreateSubaccountTransfer = Entry('private/create-subaccount-transfer', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_subaccount_balances = v1PrivatePostPrivateGetSubaccountBalances = Entry('private/get-subaccount-balances', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_order_list = v1PrivatePostPrivateGetOrderList = Entry('private/get-order-list', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_create_withdrawal = v1PrivatePostPrivateCreateWithdrawal = Entry('private/create-withdrawal', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_currency_networks = v1PrivatePostPrivateGetCurrencyNetworks = Entry('private/get-currency-networks', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_deposit_address = v1PrivatePostPrivateGetDepositAddress = Entry('private/get-deposit-address', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_accounts = v1PrivatePostPrivateGetAccounts = Entry('private/get-accounts', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_withdrawal_history = v1PrivatePostPrivateGetWithdrawalHistory = Entry('private/get-withdrawal-history', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v1_private_post_private_get_deposit_history = v1PrivatePostPrivateGetDepositHistory = Entry('private/get-deposit-history', ['v1', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_public_get_public_auth = v2PublicGetPublicAuth = Entry('public/auth', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_get_instruments = v2PublicGetPublicGetInstruments = Entry('public/get-instruments', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_get_book = v2PublicGetPublicGetBook = Entry('public/get-book', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_get_candlestick = v2PublicGetPublicGetCandlestick = Entry('public/get-candlestick', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_get_ticker = v2PublicGetPublicGetTicker = Entry('public/get-ticker', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_get_trades = v2PublicGetPublicGetTrades = Entry('public/get-trades', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_margin_get_transfer_currencies = v2PublicGetPublicMarginGetTransferCurrencies = Entry('public/margin/get-transfer-currencies', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_margin_get_load_currenices = v2PublicGetPublicMarginGetLoadCurrenices = Entry('public/margin/get-load-currenices', ['v2', 'public'], 'GET', {'cost': 1})
    v2_public_get_public_respond_heartbeat = v2PublicGetPublicRespondHeartbeat = Entry('public/respond-heartbeat', ['v2', 'public'], 'GET', {'cost': 1})
    v2_private_post_private_set_cancel_on_disconnect = v2PrivatePostPrivateSetCancelOnDisconnect = Entry('private/set-cancel-on-disconnect', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_cancel_on_disconnect = v2PrivatePostPrivateGetCancelOnDisconnect = Entry('private/get-cancel-on-disconnect', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_create_withdrawal = v2PrivatePostPrivateCreateWithdrawal = Entry('private/create-withdrawal', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_withdrawal_history = v2PrivatePostPrivateGetWithdrawalHistory = Entry('private/get-withdrawal-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_currency_networks = v2PrivatePostPrivateGetCurrencyNetworks = Entry('private/get-currency-networks', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_deposit_history = v2PrivatePostPrivateGetDepositHistory = Entry('private/get-deposit-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_deposit_address = v2PrivatePostPrivateGetDepositAddress = Entry('private/get-deposit-address', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_account_summary = v2PrivatePostPrivateGetAccountSummary = Entry('private/get-account-summary', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_create_order = v2PrivatePostPrivateCreateOrder = Entry('private/create-order', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_cancel_order = v2PrivatePostPrivateCancelOrder = Entry('private/cancel-order', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_cancel_all_orders = v2PrivatePostPrivateCancelAllOrders = Entry('private/cancel-all-orders', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_create_order_list = v2PrivatePostPrivateCreateOrderList = Entry('private/create-order-list', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_order_history = v2PrivatePostPrivateGetOrderHistory = Entry('private/get-order-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_open_orders = v2PrivatePostPrivateGetOpenOrders = Entry('private/get-open-orders', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_order_detail = v2PrivatePostPrivateGetOrderDetail = Entry('private/get-order-detail', ['v2', 'private'], 'POST', {'cost': 0.3333333333333333})
    v2_private_post_private_get_trades = v2PrivatePostPrivateGetTrades = Entry('private/get-trades', ['v2', 'private'], 'POST', {'cost': 100})
    v2_private_post_private_margin_get_user_config = v2PrivatePostPrivateMarginGetUserConfig = Entry('private/margin/get-user-config', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_account_summary = v2PrivatePostPrivateMarginGetAccountSummary = Entry('private/margin/get-account-summary', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_transfer = v2PrivatePostPrivateMarginTransfer = Entry('private/margin/transfer', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_borrow = v2PrivatePostPrivateMarginBorrow = Entry('private/margin/borrow', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_repay = v2PrivatePostPrivateMarginRepay = Entry('private/margin/repay', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_transfer_history = v2PrivatePostPrivateMarginGetTransferHistory = Entry('private/margin/get-transfer-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_borrow_history = v2PrivatePostPrivateMarginGetBorrowHistory = Entry('private/margin/get-borrow-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_interest_history = v2PrivatePostPrivateMarginGetInterestHistory = Entry('private/margin/get-interest-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_repay_history = v2PrivatePostPrivateMarginGetRepayHistory = Entry('private/margin/get-repay-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_liquidation_history = v2PrivatePostPrivateMarginGetLiquidationHistory = Entry('private/margin/get-liquidation-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_liquidation_orders = v2PrivatePostPrivateMarginGetLiquidationOrders = Entry('private/margin/get-liquidation-orders', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_create_order = v2PrivatePostPrivateMarginCreateOrder = Entry('private/margin/create-order', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_margin_cancel_order = v2PrivatePostPrivateMarginCancelOrder = Entry('private/margin/cancel-order', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_margin_cancel_all_orders = v2PrivatePostPrivateMarginCancelAllOrders = Entry('private/margin/cancel-all-orders', ['v2', 'private'], 'POST', {'cost': 0.6666666666666666})
    v2_private_post_private_margin_get_order_history = v2PrivatePostPrivateMarginGetOrderHistory = Entry('private/margin/get-order-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_open_orders = v2PrivatePostPrivateMarginGetOpenOrders = Entry('private/margin/get-open-orders', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_margin_get_order_detail = v2PrivatePostPrivateMarginGetOrderDetail = Entry('private/margin/get-order-detail', ['v2', 'private'], 'POST', {'cost': 0.3333333333333333})
    v2_private_post_private_margin_get_trades = v2PrivatePostPrivateMarginGetTrades = Entry('private/margin/get-trades', ['v2', 'private'], 'POST', {'cost': 100})
    v2_private_post_private_deriv_transfer = v2PrivatePostPrivateDerivTransfer = Entry('private/deriv/transfer', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_deriv_get_transfer_history = v2PrivatePostPrivateDerivGetTransferHistory = Entry('private/deriv/get-transfer-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_accounts = v2PrivatePostPrivateGetAccounts = Entry('private/get-accounts', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_get_subaccount_balances = v2PrivatePostPrivateGetSubaccountBalances = Entry('private/get-subaccount-balances', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_create_subaccount_transfer = v2PrivatePostPrivateCreateSubaccountTransfer = Entry('private/create-subaccount-transfer', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_otc_get_otc_user = v2PrivatePostPrivateOtcGetOtcUser = Entry('private/otc/get-otc-user', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_otc_get_instruments = v2PrivatePostPrivateOtcGetInstruments = Entry('private/otc/get-instruments', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_otc_request_quote = v2PrivatePostPrivateOtcRequestQuote = Entry('private/otc/request-quote', ['v2', 'private'], 'POST', {'cost': 100})
    v2_private_post_private_otc_accept_quote = v2PrivatePostPrivateOtcAcceptQuote = Entry('private/otc/accept-quote', ['v2', 'private'], 'POST', {'cost': 100})
    v2_private_post_private_otc_get_quote_history = v2PrivatePostPrivateOtcGetQuoteHistory = Entry('private/otc/get-quote-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    v2_private_post_private_otc_get_trade_history = v2PrivatePostPrivateOtcGetTradeHistory = Entry('private/otc/get-trade-history', ['v2', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_public_get_public_auth = derivativesPublicGetPublicAuth = Entry('public/auth', ['derivatives', 'public'], 'GET', {'cost': 3.3333333333333335})
    derivatives_public_get_public_get_instruments = derivativesPublicGetPublicGetInstruments = Entry('public/get-instruments', ['derivatives', 'public'], 'GET', {'cost': 3.3333333333333335})
    derivatives_public_get_public_get_book = derivativesPublicGetPublicGetBook = Entry('public/get-book', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_public_get_public_get_candlestick = derivativesPublicGetPublicGetCandlestick = Entry('public/get-candlestick', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_public_get_public_get_trades = derivativesPublicGetPublicGetTrades = Entry('public/get-trades', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_public_get_public_get_tickers = derivativesPublicGetPublicGetTickers = Entry('public/get-tickers', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_public_get_public_get_valuations = derivativesPublicGetPublicGetValuations = Entry('public/get-valuations', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_public_get_public_get_expired_settlement_price = derivativesPublicGetPublicGetExpiredSettlementPrice = Entry('public/get-expired-settlement-price', ['derivatives', 'public'], 'GET', {'cost': 3.3333333333333335})
    derivatives_public_get_public_get_insurance = derivativesPublicGetPublicGetInsurance = Entry('public/get-insurance', ['derivatives', 'public'], 'GET', {'cost': 1})
    derivatives_private_post_private_set_cancel_on_disconnect = derivativesPrivatePostPrivateSetCancelOnDisconnect = Entry('private/set-cancel-on-disconnect', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_cancel_on_disconnect = derivativesPrivatePostPrivateGetCancelOnDisconnect = Entry('private/get-cancel-on-disconnect', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_user_balance = derivativesPrivatePostPrivateUserBalance = Entry('private/user-balance', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_user_balance_history = derivativesPrivatePostPrivateUserBalanceHistory = Entry('private/user-balance-history', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_positions = derivativesPrivatePostPrivateGetPositions = Entry('private/get-positions', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_create_order = derivativesPrivatePostPrivateCreateOrder = Entry('private/create-order', ['derivatives', 'private'], 'POST', {'cost': 0.6666666666666666})
    derivatives_private_post_private_create_order_list = derivativesPrivatePostPrivateCreateOrderList = Entry('private/create-order-list', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_cancel_order = derivativesPrivatePostPrivateCancelOrder = Entry('private/cancel-order', ['derivatives', 'private'], 'POST', {'cost': 0.6666666666666666})
    derivatives_private_post_private_cancel_order_list = derivativesPrivatePostPrivateCancelOrderList = Entry('private/cancel-order-list', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_cancel_all_orders = derivativesPrivatePostPrivateCancelAllOrders = Entry('private/cancel-all-orders', ['derivatives', 'private'], 'POST', {'cost': 0.6666666666666666})
    derivatives_private_post_private_close_position = derivativesPrivatePostPrivateClosePosition = Entry('private/close-position', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_convert_collateral = derivativesPrivatePostPrivateConvertCollateral = Entry('private/convert-collateral', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_order_history = derivativesPrivatePostPrivateGetOrderHistory = Entry('private/get-order-history', ['derivatives', 'private'], 'POST', {'cost': 100})
    derivatives_private_post_private_get_open_orders = derivativesPrivatePostPrivateGetOpenOrders = Entry('private/get-open-orders', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_order_detail = derivativesPrivatePostPrivateGetOrderDetail = Entry('private/get-order-detail', ['derivatives', 'private'], 'POST', {'cost': 0.3333333333333333})
    derivatives_private_post_private_get_trades = derivativesPrivatePostPrivateGetTrades = Entry('private/get-trades', ['derivatives', 'private'], 'POST', {'cost': 100})
    derivatives_private_post_private_change_account_leverage = derivativesPrivatePostPrivateChangeAccountLeverage = Entry('private/change-account-leverage', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_transactions = derivativesPrivatePostPrivateGetTransactions = Entry('private/get-transactions', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_create_subaccount_transfer = derivativesPrivatePostPrivateCreateSubaccountTransfer = Entry('private/create-subaccount-transfer', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_subaccount_balances = derivativesPrivatePostPrivateGetSubaccountBalances = Entry('private/get-subaccount-balances', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
    derivatives_private_post_private_get_order_list = derivativesPrivatePostPrivateGetOrderList = Entry('private/get-order-list', ['derivatives', 'private'], 'POST', {'cost': 3.3333333333333335})
