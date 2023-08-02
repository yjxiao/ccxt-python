from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_instruments = publicGetInstruments = Entry('instruments', 'public', 'GET', {})
    public_get_orderbook = publicGetOrderbook = Entry('orderbook', 'public', 'GET', {})
    public_get_tickers = publicGetTickers = Entry('tickers', 'public', 'GET', {})
    public_get_history = publicGetHistory = Entry('history', 'public', 'GET', {})
    public_get_historicalfundingrates = publicGetHistoricalfundingrates = Entry('historicalfundingrates', 'public', 'GET', {})
    private_get_openpositions = privateGetOpenpositions = Entry('openpositions', 'private', 'GET', {})
    private_get_notifications = privateGetNotifications = Entry('notifications', 'private', 'GET', {})
    private_get_accounts = privateGetAccounts = Entry('accounts', 'private', 'GET', {})
    private_get_openorders = privateGetOpenorders = Entry('openorders', 'private', 'GET', {})
    private_get_recentorders = privateGetRecentorders = Entry('recentorders', 'private', 'GET', {})
    private_get_fills = privateGetFills = Entry('fills', 'private', 'GET', {})
    private_get_transfers = privateGetTransfers = Entry('transfers', 'private', 'GET', {})
    private_get_leveragepreferences = privateGetLeveragepreferences = Entry('leveragepreferences', 'private', 'GET', {})
    private_get_pnlpreferences = privateGetPnlpreferences = Entry('pnlpreferences', 'private', 'GET', {})
    private_post_sendorder = privatePostSendorder = Entry('sendorder', 'private', 'POST', {})
    private_post_editorder = privatePostEditorder = Entry('editorder', 'private', 'POST', {})
    private_post_cancelorder = privatePostCancelorder = Entry('cancelorder', 'private', 'POST', {})
    private_post_transfer = privatePostTransfer = Entry('transfer', 'private', 'POST', {})
    private_post_batchorder = privatePostBatchorder = Entry('batchorder', 'private', 'POST', {})
    private_post_cancelallorders = privatePostCancelallorders = Entry('cancelallorders', 'private', 'POST', {})
    private_post_cancelallordersafter = privatePostCancelallordersafter = Entry('cancelallordersafter', 'private', 'POST', {})
    private_post_withdrawal = privatePostWithdrawal = Entry('withdrawal', 'private', 'POST', {})
    private_put_leveragepreferences = privatePutLeveragepreferences = Entry('leveragepreferences', 'private', 'PUT', {})
    private_put_pnlpreferences = privatePutPnlpreferences = Entry('pnlpreferences', 'private', 'PUT', {})
    charts_get_price_type_symbol_interval = chartsGetPriceTypeSymbolInterval = Entry('{price_type}/{symbol}/{interval}', 'charts', 'GET', {})
    history_get_orders = historyGetOrders = Entry('orders', 'history', 'GET', {})
    history_get_executions = historyGetExecutions = Entry('executions', 'history', 'GET', {})
    history_get_triggers = historyGetTriggers = Entry('triggers', 'history', 'GET', {})
    history_get_accountlogcsv = historyGetAccountlogcsv = Entry('accountlogcsv', 'history', 'GET', {})
    history_get_market_symbol_orders = historyGetMarketSymbolOrders = Entry('market/{symbol}/orders', 'history', 'GET', {})
    history_get_market_symbol_executions = historyGetMarketSymbolExecutions = Entry('market/{symbol}/executions', 'history', 'GET', {})
    feeschedules_get_volumes = feeschedulesGetVolumes = Entry('volumes', 'feeschedules', 'GET', {})
