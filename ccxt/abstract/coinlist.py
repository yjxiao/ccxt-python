from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_v1_symbols = publicGetV1Symbols = Entry('v1/symbols', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_summary = publicGetV1SymbolsSummary = Entry('v1/symbols/summary', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol = publicGetV1SymbolsSymbol = Entry('v1/symbols/{symbol}', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_summary = publicGetV1SymbolsSymbolSummary = Entry('v1/symbols/{symbol}/summary', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_book = publicGetV1SymbolsSymbolBook = Entry('v1/symbols/{symbol}/book', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_quote = publicGetV1SymbolsSymbolQuote = Entry('v1/symbols/{symbol}/quote', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_candles = publicGetV1SymbolsSymbolCandles = Entry('v1/symbols/{symbol}/candles', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_auctions = publicGetV1SymbolsSymbolAuctions = Entry('v1/symbols/{symbol}/auctions', 'public', 'GET', {'cost': 1})
    public_get_v1_symbols_symbol_auctions_auction_code = publicGetV1SymbolsSymbolAuctionsAuctionCode = Entry('v1/symbols/{symbol}/auctions/{auction_code}', 'public', 'GET', {'cost': 1})
    public_get_v1_time = publicGetV1Time = Entry('v1/time', 'public', 'GET', {'cost': 1})
    public_get_v1_assets = publicGetV1Assets = Entry('v1/assets', 'public', 'GET', {'cost': 1})
    private_get_v1_fees = privateGetV1Fees = Entry('v1/fees', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts = privateGetV1Accounts = Entry('v1/accounts', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts_trader_id = privateGetV1AccountsTraderId = Entry('v1/accounts/{trader_id}', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts_trader_id_ledger = privateGetV1AccountsTraderIdLedger = Entry('v1/accounts/{trader_id}/ledger', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts_trader_id_wallets = privateGetV1AccountsTraderIdWallets = Entry('v1/accounts/{trader_id}/wallets', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts_trader_id_wallet_ledger = privateGetV1AccountsTraderIdWalletLedger = Entry('v1/accounts/{trader_id}/wallet-ledger', 'private', 'GET', {'cost': 1})
    private_get_v1_accounts_trader_id_ledger_summary = privateGetV1AccountsTraderIdLedgerSummary = Entry('v1/accounts/{trader_id}/ledger-summary', 'private', 'GET', {'cost': 1})
    private_get_v1_keys = privateGetV1Keys = Entry('v1/keys', 'private', 'GET', {'cost': 1})
    private_get_v1_fills = privateGetV1Fills = Entry('v1/fills', 'private', 'GET', {'cost': 1})
    private_get_v1_orders = privateGetV1Orders = Entry('v1/orders', 'private', 'GET', {'cost': 1})
    private_get_v1_orders_order_id = privateGetV1OrdersOrderId = Entry('v1/orders/{order_id}', 'private', 'GET', {'cost': 1})
    private_get_v1_reports = privateGetV1Reports = Entry('v1/reports', 'private', 'GET', {'cost': 1})
    private_get_v1_balances = privateGetV1Balances = Entry('v1/balances', 'private', 'GET', {'cost': 1})
    private_get_v1_transfers = privateGetV1Transfers = Entry('v1/transfers', 'private', 'GET', {'cost': 1})
    private_get_v1_user = privateGetV1User = Entry('v1/user', 'private', 'GET', {'cost': 1})
    private_get_v1_credits = privateGetV1Credits = Entry('v1/credits', 'private', 'GET', {'cost': 1})
    private_post_v1_keys = privatePostV1Keys = Entry('v1/keys', 'private', 'POST', {'cost': 1})
    private_post_v1_orders = privatePostV1Orders = Entry('v1/orders', 'private', 'POST', {'cost': 1})
    private_post_v1_orders_cancel_all_after = privatePostV1OrdersCancelAllAfter = Entry('v1/orders/cancel-all-after', 'private', 'POST', {'cost': 1})
    private_post_v1_reports = privatePostV1Reports = Entry('v1/reports', 'private', 'POST', {'cost': 1})
    private_post_v1_transfers_to_wallet = privatePostV1TransfersToWallet = Entry('v1/transfers/to-wallet', 'private', 'POST', {'cost': 1})
    private_post_v1_transfers_from_wallet = privatePostV1TransfersFromWallet = Entry('v1/transfers/from-wallet', 'private', 'POST', {'cost': 1})
    private_post_v1_transfers_internal_transfer = privatePostV1TransfersInternalTransfer = Entry('v1/transfers/internal-transfer', 'private', 'POST', {'cost': 1})
    private_post_v1_transfers_withdrawal_request = privatePostV1TransfersWithdrawalRequest = Entry('v1/transfers/withdrawal-request', 'private', 'POST', {'cost': 1})
    private_post_v1_orders_bulk = privatePostV1OrdersBulk = Entry('v1/orders/bulk', 'private', 'POST', {'cost': 1})
    private_patch_v1_orders_order_id = privatePatchV1OrdersOrderId = Entry('v1/orders/{order_id}', 'private', 'PATCH', {'cost': 1})
    private_patch_v1_orders_bulk = privatePatchV1OrdersBulk = Entry('v1/orders/bulk', 'private', 'PATCH', {'cost': 1})
    private_delete_v1_keys_key = privateDeleteV1KeysKey = Entry('v1/keys/{key}', 'private', 'DELETE', {'cost': 1})
    private_delete_v1_orders = privateDeleteV1Orders = Entry('v1/orders', 'private', 'DELETE', {'cost': 1})
    private_delete_v1_orders_order_id = privateDeleteV1OrdersOrderId = Entry('v1/orders/{order_id}', 'private', 'DELETE', {'cost': 1})
    private_delete_v1_orders_bulk = privateDeleteV1OrdersBulk = Entry('v1/orders/bulk', 'private', 'DELETE', {'cost': 1})
