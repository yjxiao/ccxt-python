from ccxt.base.types import Entry


class ImplicitAPI:
    v1_pub_get_hist_kline = v1PubGetHistKline = Entry('hist/kline', ['v1', 'pub'], 'GET', {'cost': 10})
    v1_pub_get_hist_trades = v1PubGetHistTrades = Entry('hist/trades', ['v1', 'pub'], 'GET', {'cost': 1})
    v1_public_get_info = v1PublicGetInfo = Entry('info', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_info_symbol = v1PublicGetInfoSymbol = Entry('info/{symbol}', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_system_info = v1PublicGetSystemInfo = Entry('system_info', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_market_trades = v1PublicGetMarketTrades = Entry('market_trades', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_token = v1PublicGetToken = Entry('token', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_token_network = v1PublicGetTokenNetwork = Entry('token_network', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_funding_rates = v1PublicGetFundingRates = Entry('funding_rates', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_funding_rate_symbol = v1PublicGetFundingRateSymbol = Entry('funding_rate/{symbol}', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_funding_rate_history = v1PublicGetFundingRateHistory = Entry('funding_rate_history', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_futures = v1PublicGetFutures = Entry('futures', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_futures_symbol = v1PublicGetFuturesSymbol = Entry('futures/{symbol}', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_orderbook_symbol = v1PublicGetOrderbookSymbol = Entry('orderbook/{symbol}', ['v1', 'public'], 'GET', {'cost': 1})
    v1_public_get_kline = v1PublicGetKline = Entry('kline', ['v1', 'public'], 'GET', {'cost': 1})
    v1_private_get_client_token = v1PrivateGetClientToken = Entry('client/token', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_order_oid = v1PrivateGetOrderOid = Entry('order/{oid}', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_client_order_client_order_id = v1PrivateGetClientOrderClientOrderId = Entry('client/order/{client_order_id}', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_orders = v1PrivateGetOrders = Entry('orders', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_client_trade_tid = v1PrivateGetClientTradeTid = Entry('client/trade/{tid}', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_order_oid_trades = v1PrivateGetOrderOidTrades = Entry('order/{oid}/trades', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_client_trades = v1PrivateGetClientTrades = Entry('client/trades', ['v1', 'private'], 'GET', {'cost': 1})
    v1_private_get_client_info = v1PrivateGetClientInfo = Entry('client/info', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_asset_deposit = v1PrivateGetAssetDeposit = Entry('asset/deposit', ['v1', 'private'], 'GET', {'cost': 10})
    v1_private_get_asset_history = v1PrivateGetAssetHistory = Entry('asset/history', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_sub_account_all = v1PrivateGetSubAccountAll = Entry('sub_account/all', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_sub_account_assets = v1PrivateGetSubAccountAssets = Entry('sub_account/assets', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_token_interest = v1PrivateGetTokenInterest = Entry('token_interest', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_token_interest_token = v1PrivateGetTokenInterestToken = Entry('token_interest/{token}', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_interest_history = v1PrivateGetInterestHistory = Entry('interest/history', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_interest_repay = v1PrivateGetInterestRepay = Entry('interest/repay', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_get_funding_fee_history = v1PrivateGetFundingFeeHistory = Entry('funding_fee/history', ['v1', 'private'], 'GET', {'cost': 30})
    v1_private_get_positions = v1PrivateGetPositions = Entry('positions', ['v1', 'private'], 'GET', {'cost': 3.33})
    v1_private_get_position_symbol = v1PrivateGetPositionSymbol = Entry('position/{symbol}', ['v1', 'private'], 'GET', {'cost': 3.33})
    v1_private_get_client_transaction_history = v1PrivateGetClientTransactionHistory = Entry('client/transaction_history', ['v1', 'private'], 'GET', {'cost': 60})
    v1_private_post_order = v1PrivatePostOrder = Entry('order', ['v1', 'private'], 'POST', {'cost': 5})
    v1_private_post_asset_main_sub_transfer = v1PrivatePostAssetMainSubTransfer = Entry('asset/main_sub_transfer', ['v1', 'private'], 'POST', {'cost': 30})
    v1_private_post_asset_withdraw = v1PrivatePostAssetWithdraw = Entry('asset/withdraw', ['v1', 'private'], 'POST', {'cost': 30})
    v1_private_post_interest_repay = v1PrivatePostInterestRepay = Entry('interest/repay', ['v1', 'private'], 'POST', {'cost': 60})
    v1_private_post_client_account_mode = v1PrivatePostClientAccountMode = Entry('client/account_mode', ['v1', 'private'], 'POST', {'cost': 120})
    v1_private_post_client_leverage = v1PrivatePostClientLeverage = Entry('client/leverage', ['v1', 'private'], 'POST', {'cost': 120})
    v1_private_delete_order = v1PrivateDeleteOrder = Entry('order', ['v1', 'private'], 'DELETE', {'cost': 1})
    v1_private_delete_client_order = v1PrivateDeleteClientOrder = Entry('client/order', ['v1', 'private'], 'DELETE', {'cost': 1})
    v1_private_delete_orders = v1PrivateDeleteOrders = Entry('orders', ['v1', 'private'], 'DELETE', {'cost': 1})
    v1_private_delete_asset_withdraw = v1PrivateDeleteAssetWithdraw = Entry('asset/withdraw', ['v1', 'private'], 'DELETE', {'cost': 120})
    v2_private_get_client_holding = v2PrivateGetClientHolding = Entry('client/holding', ['v2', 'private'], 'GET', {'cost': 1})
    v3_private_get_algo_order_oid = v3PrivateGetAlgoOrderOid = Entry('algo/order/{oid}', ['v3', 'private'], 'GET', {'cost': 1})
    v3_private_get_algo_orders = v3PrivateGetAlgoOrders = Entry('algo/orders', ['v3', 'private'], 'GET', {'cost': 1})
    v3_private_get_balances = v3PrivateGetBalances = Entry('balances', ['v3', 'private'], 'GET', {'cost': 1})
    v3_private_get_accountinfo = v3PrivateGetAccountinfo = Entry('accountinfo', ['v3', 'private'], 'GET', {'cost': 60})
    v3_private_get_positions = v3PrivateGetPositions = Entry('positions', ['v3', 'private'], 'GET', {'cost': 3.33})
    v3_private_get_buypower = v3PrivateGetBuypower = Entry('buypower', ['v3', 'private'], 'GET', {'cost': 1})
    v3_private_post_algo_order = v3PrivatePostAlgoOrder = Entry('algo/order', ['v3', 'private'], 'POST', {'cost': 5})
    v3_private_put_order_oid = v3PrivatePutOrderOid = Entry('order/{oid}', ['v3', 'private'], 'PUT', {'cost': 2})
    v3_private_put_order_client_client_order_id = v3PrivatePutOrderClientClientOrderId = Entry('order/client/{client_order_id}', ['v3', 'private'], 'PUT', {'cost': 2})
    v3_private_put_algo_order_oid = v3PrivatePutAlgoOrderOid = Entry('algo/order/{oid}', ['v3', 'private'], 'PUT', {'cost': 2})
    v3_private_put_algo_order_client_client_order_id = v3PrivatePutAlgoOrderClientClientOrderId = Entry('algo/order/client/{client_order_id}', ['v3', 'private'], 'PUT', {'cost': 2})
    v3_private_delete_algo_order_order_id = v3PrivateDeleteAlgoOrderOrderId = Entry('algo/order/{order_id}', ['v3', 'private'], 'DELETE', {'cost': 1})
    v3_private_delete_algo_orders_pending = v3PrivateDeleteAlgoOrdersPending = Entry('algo/orders/pending', ['v3', 'private'], 'DELETE', {'cost': 1})
    v3_private_delete_algo_orders_pending_symbol = v3PrivateDeleteAlgoOrdersPendingSymbol = Entry('algo/orders/pending/{symbol}', ['v3', 'private'], 'DELETE', {'cost': 1})
    v3_private_delete_orders_pending = v3PrivateDeleteOrdersPending = Entry('orders/pending', ['v3', 'private'], 'DELETE', {'cost': 1})
