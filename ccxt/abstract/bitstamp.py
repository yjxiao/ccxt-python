from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_ohlc_pair = publicGetOhlcPair = Entry('ohlc/{pair}/', 'public', 'GET', {'cost': 1})
    public_get_order_book_pair = publicGetOrderBookPair = Entry('order_book/{pair}/', 'public', 'GET', {'cost': 1})
    public_get_ticker = publicGetTicker = Entry('ticker/', 'public', 'GET', {'cost': 1})
    public_get_ticker_hour_pair = publicGetTickerHourPair = Entry('ticker_hour/{pair}/', 'public', 'GET', {'cost': 1})
    public_get_ticker_pair = publicGetTickerPair = Entry('ticker/{pair}/', 'public', 'GET', {'cost': 1})
    public_get_transactions_pair = publicGetTransactionsPair = Entry('transactions/{pair}/', 'public', 'GET', {'cost': 1})
    public_get_trading_pairs_info = publicGetTradingPairsInfo = Entry('trading-pairs-info/', 'public', 'GET', {'cost': 1})
    public_get_currencies = publicGetCurrencies = Entry('currencies/', 'public', 'GET', {'cost': 1})
    public_get_eur_usd = publicGetEurUsd = Entry('eur_usd/', 'public', 'GET', {'cost': 1})
    private_post_account_balances = privatePostAccountBalances = Entry('account_balances/', 'private', 'POST', {'cost': 1})
    private_post_account_balances_currency = privatePostAccountBalancesCurrency = Entry('account_balances/{currency}/', 'private', 'POST', {'cost': 1})
    private_post_balance = privatePostBalance = Entry('balance/', 'private', 'POST', {'cost': 1})
    private_post_balance_pair = privatePostBalancePair = Entry('balance/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_bch_withdrawal = privatePostBchWithdrawal = Entry('bch_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_bch_address = privatePostBchAddress = Entry('bch_address/', 'private', 'POST', {'cost': 1})
    private_post_user_transactions = privatePostUserTransactions = Entry('user_transactions/', 'private', 'POST', {'cost': 1})
    private_post_user_transactions_pair = privatePostUserTransactionsPair = Entry('user_transactions/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_crypto_transactions = privatePostCryptoTransactions = Entry('crypto-transactions/', 'private', 'POST', {'cost': 1})
    private_post_open_orders_all = privatePostOpenOrdersAll = Entry('open_orders/all/', 'private', 'POST', {'cost': 1})
    private_post_open_orders_pair = privatePostOpenOrdersPair = Entry('open_orders/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_order_status = privatePostOrderStatus = Entry('order_status/', 'private', 'POST', {'cost': 1})
    private_post_cancel_order = privatePostCancelOrder = Entry('cancel_order/', 'private', 'POST', {'cost': 1})
    private_post_cancel_all_orders = privatePostCancelAllOrders = Entry('cancel_all_orders/', 'private', 'POST', {'cost': 1})
    private_post_cancel_all_orders_pair = privatePostCancelAllOrdersPair = Entry('cancel_all_orders/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_buy_pair = privatePostBuyPair = Entry('buy/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_buy_market_pair = privatePostBuyMarketPair = Entry('buy/market/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_buy_instant_pair = privatePostBuyInstantPair = Entry('buy/instant/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_sell_pair = privatePostSellPair = Entry('sell/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_sell_market_pair = privatePostSellMarketPair = Entry('sell/market/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_sell_instant_pair = privatePostSellInstantPair = Entry('sell/instant/{pair}/', 'private', 'POST', {'cost': 1})
    private_post_transfer_to_main = privatePostTransferToMain = Entry('transfer-to-main/', 'private', 'POST', {'cost': 1})
    private_post_transfer_from_main = privatePostTransferFromMain = Entry('transfer-from-main/', 'private', 'POST', {'cost': 1})
    private_post_my_trading_pairs = privatePostMyTradingPairs = Entry('my_trading_pairs/', 'private', 'POST', {'cost': 1})
    private_post_fees_trading = privatePostFeesTrading = Entry('fees/trading/', 'private', 'POST', {'cost': 1})
    private_post_fees_withdrawal = privatePostFeesWithdrawal = Entry('fees/withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_fees_withdrawal_currency = privatePostFeesWithdrawalCurrency = Entry('fees/withdrawal/{currency}/', 'private', 'POST', {'cost': 1})
    private_post_withdrawal_requests = privatePostWithdrawalRequests = Entry('withdrawal-requests/', 'private', 'POST', {'cost': 1})
    private_post_withdrawal_open = privatePostWithdrawalOpen = Entry('withdrawal/open/', 'private', 'POST', {'cost': 1})
    private_post_withdrawal_status = privatePostWithdrawalStatus = Entry('withdrawal/status/', 'private', 'POST', {'cost': 1})
    private_post_withdrawal_cancel = privatePostWithdrawalCancel = Entry('withdrawal/cancel/', 'private', 'POST', {'cost': 1})
    private_post_liquidation_address_new = privatePostLiquidationAddressNew = Entry('liquidation_address/new/', 'private', 'POST', {'cost': 1})
    private_post_liquidation_address_info = privatePostLiquidationAddressInfo = Entry('liquidation_address/info/', 'private', 'POST', {'cost': 1})
    private_post_btc_unconfirmed = privatePostBtcUnconfirmed = Entry('btc_unconfirmed/', 'private', 'POST', {'cost': 1})
    private_post_websockets_token = privatePostWebsocketsToken = Entry('websockets_token/', 'private', 'POST', {'cost': 1})
    private_post_btc_withdrawal = privatePostBtcWithdrawal = Entry('btc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_btc_address = privatePostBtcAddress = Entry('btc_address/', 'private', 'POST', {'cost': 1})
    private_post_ripple_withdrawal = privatePostRippleWithdrawal = Entry('ripple_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ripple_address = privatePostRippleAddress = Entry('ripple_address/', 'private', 'POST', {'cost': 1})
    private_post_ltc_withdrawal = privatePostLtcWithdrawal = Entry('ltc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ltc_address = privatePostLtcAddress = Entry('ltc_address/', 'private', 'POST', {'cost': 1})
    private_post_eth_withdrawal = privatePostEthWithdrawal = Entry('eth_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_eth_address = privatePostEthAddress = Entry('eth_address/', 'private', 'POST', {'cost': 1})
    private_post_xrp_withdrawal = privatePostXrpWithdrawal = Entry('xrp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_xrp_address = privatePostXrpAddress = Entry('xrp_address/', 'private', 'POST', {'cost': 1})
    private_post_xlm_withdrawal = privatePostXlmWithdrawal = Entry('xlm_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_xlm_address = privatePostXlmAddress = Entry('xlm_address/', 'private', 'POST', {'cost': 1})
    private_post_pax_withdrawal = privatePostPaxWithdrawal = Entry('pax_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_pax_address = privatePostPaxAddress = Entry('pax_address/', 'private', 'POST', {'cost': 1})
    private_post_link_withdrawal = privatePostLinkWithdrawal = Entry('link_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_link_address = privatePostLinkAddress = Entry('link_address/', 'private', 'POST', {'cost': 1})
    private_post_usdc_withdrawal = privatePostUsdcWithdrawal = Entry('usdc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_usdc_address = privatePostUsdcAddress = Entry('usdc_address/', 'private', 'POST', {'cost': 1})
    private_post_omg_withdrawal = privatePostOmgWithdrawal = Entry('omg_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_omg_address = privatePostOmgAddress = Entry('omg_address/', 'private', 'POST', {'cost': 1})
    private_post_dai_withdrawal = privatePostDaiWithdrawal = Entry('dai_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_dai_address = privatePostDaiAddress = Entry('dai_address/', 'private', 'POST', {'cost': 1})
    private_post_knc_withdrawal = privatePostKncWithdrawal = Entry('knc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_knc_address = privatePostKncAddress = Entry('knc_address/', 'private', 'POST', {'cost': 1})
    private_post_mkr_withdrawal = privatePostMkrWithdrawal = Entry('mkr_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_mkr_address = privatePostMkrAddress = Entry('mkr_address/', 'private', 'POST', {'cost': 1})
    private_post_zrx_withdrawal = privatePostZrxWithdrawal = Entry('zrx_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_zrx_address = privatePostZrxAddress = Entry('zrx_address/', 'private', 'POST', {'cost': 1})
    private_post_gusd_withdrawal = privatePostGusdWithdrawal = Entry('gusd_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_gusd_address = privatePostGusdAddress = Entry('gusd_address/', 'private', 'POST', {'cost': 1})
    private_post_aave_withdrawal = privatePostAaveWithdrawal = Entry('aave_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_aave_address = privatePostAaveAddress = Entry('aave_address/', 'private', 'POST', {'cost': 1})
    private_post_bat_withdrawal = privatePostBatWithdrawal = Entry('bat_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_bat_address = privatePostBatAddress = Entry('bat_address/', 'private', 'POST', {'cost': 1})
    private_post_uma_withdrawal = privatePostUmaWithdrawal = Entry('uma_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_uma_address = privatePostUmaAddress = Entry('uma_address/', 'private', 'POST', {'cost': 1})
    private_post_snx_withdrawal = privatePostSnxWithdrawal = Entry('snx_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_snx_address = privatePostSnxAddress = Entry('snx_address/', 'private', 'POST', {'cost': 1})
    private_post_uni_withdrawal = privatePostUniWithdrawal = Entry('uni_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_uni_address = privatePostUniAddress = Entry('uni_address/', 'private', 'POST', {'cost': 1})
    private_post_yfi_withdrawal = privatePostYfiWithdrawal = Entry('yfi_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_yfi_address = privatePostYfiAddress = Entry('yfi_address', 'private', 'POST', {'cost': 1})
    private_post_audio_withdrawal = privatePostAudioWithdrawal = Entry('audio_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_audio_address = privatePostAudioAddress = Entry('audio_address/', 'private', 'POST', {'cost': 1})
    private_post_crv_withdrawal = privatePostCrvWithdrawal = Entry('crv_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_crv_address = privatePostCrvAddress = Entry('crv_address/', 'private', 'POST', {'cost': 1})
    private_post_algo_withdrawal = privatePostAlgoWithdrawal = Entry('algo_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_algo_address = privatePostAlgoAddress = Entry('algo_address/', 'private', 'POST', {'cost': 1})
    private_post_comp_withdrawal = privatePostCompWithdrawal = Entry('comp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_comp_address = privatePostCompAddress = Entry('comp_address/', 'private', 'POST', {'cost': 1})
    private_post_grt_withdrawal = privatePostGrtWithdrawal = Entry('grt_withdrawal', 'private', 'POST', {'cost': 1})
    private_post_grt_address = privatePostGrtAddress = Entry('grt_address/', 'private', 'POST', {'cost': 1})
    private_post_usdt_withdrawal = privatePostUsdtWithdrawal = Entry('usdt_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_usdt_address = privatePostUsdtAddress = Entry('usdt_address/', 'private', 'POST', {'cost': 1})
    private_post_eurt_withdrawal = privatePostEurtWithdrawal = Entry('eurt_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_eurt_address = privatePostEurtAddress = Entry('eurt_address/', 'private', 'POST', {'cost': 1})
    private_post_matic_withdrawal = privatePostMaticWithdrawal = Entry('matic_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_matic_address = privatePostMaticAddress = Entry('matic_address/', 'private', 'POST', {'cost': 1})
    private_post_sushi_withdrawal = privatePostSushiWithdrawal = Entry('sushi_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_sushi_address = privatePostSushiAddress = Entry('sushi_address/', 'private', 'POST', {'cost': 1})
    private_post_chz_withdrawal = privatePostChzWithdrawal = Entry('chz_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_chz_address = privatePostChzAddress = Entry('chz_address/', 'private', 'POST', {'cost': 1})
    private_post_enj_withdrawal = privatePostEnjWithdrawal = Entry('enj_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_enj_address = privatePostEnjAddress = Entry('enj_address/', 'private', 'POST', {'cost': 1})
    private_post_alpha_withdrawal = privatePostAlphaWithdrawal = Entry('alpha_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_alpha_address = privatePostAlphaAddress = Entry('alpha_address/', 'private', 'POST', {'cost': 1})
    private_post_ftt_withdrawal = privatePostFttWithdrawal = Entry('ftt_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ftt_address = privatePostFttAddress = Entry('ftt_address/', 'private', 'POST', {'cost': 1})
    private_post_storj_withdrawal = privatePostStorjWithdrawal = Entry('storj_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_storj_address = privatePostStorjAddress = Entry('storj_address/', 'private', 'POST', {'cost': 1})
    private_post_axs_withdrawal = privatePostAxsWithdrawal = Entry('axs_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_axs_address = privatePostAxsAddress = Entry('axs_address/', 'private', 'POST', {'cost': 1})
    private_post_sand_withdrawal = privatePostSandWithdrawal = Entry('sand_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_sand_address = privatePostSandAddress = Entry('sand_address/', 'private', 'POST', {'cost': 1})
    private_post_hbar_withdrawal = privatePostHbarWithdrawal = Entry('hbar_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_hbar_address = privatePostHbarAddress = Entry('hbar_address/', 'private', 'POST', {'cost': 1})
    private_post_rgt_withdrawal = privatePostRgtWithdrawal = Entry('rgt_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_rgt_address = privatePostRgtAddress = Entry('rgt_address/', 'private', 'POST', {'cost': 1})
    private_post_fet_withdrawal = privatePostFetWithdrawal = Entry('fet_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_fet_address = privatePostFetAddress = Entry('fet_address/', 'private', 'POST', {'cost': 1})
    private_post_skl_withdrawal = privatePostSklWithdrawal = Entry('skl_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_skl_address = privatePostSklAddress = Entry('skl_address/', 'private', 'POST', {'cost': 1})
    private_post_cel_withdrawal = privatePostCelWithdrawal = Entry('cel_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_cel_address = privatePostCelAddress = Entry('cel_address/', 'private', 'POST', {'cost': 1})
    private_post_sxp_withdrawal = privatePostSxpWithdrawal = Entry('sxp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_sxp_address = privatePostSxpAddress = Entry('sxp_address/', 'private', 'POST', {'cost': 1})
    private_post_ada_withdrawal = privatePostAdaWithdrawal = Entry('ada_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ada_address = privatePostAdaAddress = Entry('ada_address/', 'private', 'POST', {'cost': 1})
    private_post_slp_withdrawal = privatePostSlpWithdrawal = Entry('slp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_slp_address = privatePostSlpAddress = Entry('slp_address/', 'private', 'POST', {'cost': 1})
    private_post_ftm_withdrawal = privatePostFtmWithdrawal = Entry('ftm_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ftm_address = privatePostFtmAddress = Entry('ftm_address/', 'private', 'POST', {'cost': 1})
    private_post_perp_withdrawal = privatePostPerpWithdrawal = Entry('perp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_perp_address = privatePostPerpAddress = Entry('perp_address/', 'private', 'POST', {'cost': 1})
    private_post_dydx_withdrawal = privatePostDydxWithdrawal = Entry('dydx_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_dydx_address = privatePostDydxAddress = Entry('dydx_address/', 'private', 'POST', {'cost': 1})
    private_post_gala_withdrawal = privatePostGalaWithdrawal = Entry('gala_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_gala_address = privatePostGalaAddress = Entry('gala_address/', 'private', 'POST', {'cost': 1})
    private_post_shib_withdrawal = privatePostShibWithdrawal = Entry('shib_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_shib_address = privatePostShibAddress = Entry('shib_address/', 'private', 'POST', {'cost': 1})
    private_post_amp_withdrawal = privatePostAmpWithdrawal = Entry('amp_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_amp_address = privatePostAmpAddress = Entry('amp_address/', 'private', 'POST', {'cost': 1})
    private_post_sgb_withdrawal = privatePostSgbWithdrawal = Entry('sgb_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_sgb_address = privatePostSgbAddress = Entry('sgb_address/', 'private', 'POST', {'cost': 1})
    private_post_avax_withdrawal = privatePostAvaxWithdrawal = Entry('avax_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_avax_address = privatePostAvaxAddress = Entry('avax_address/', 'private', 'POST', {'cost': 1})
    private_post_wbtc_withdrawal = privatePostWbtcWithdrawal = Entry('wbtc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_wbtc_address = privatePostWbtcAddress = Entry('wbtc_address/', 'private', 'POST', {'cost': 1})
    private_post_ctsi_withdrawal = privatePostCtsiWithdrawal = Entry('ctsi_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ctsi_address = privatePostCtsiAddress = Entry('ctsi_address/', 'private', 'POST', {'cost': 1})
    private_post_cvx_withdrawal = privatePostCvxWithdrawal = Entry('cvx_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_cvx_address = privatePostCvxAddress = Entry('cvx_address/', 'private', 'POST', {'cost': 1})
    private_post_imx_withdrawal = privatePostImxWithdrawal = Entry('imx_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_imx_address = privatePostImxAddress = Entry('imx_address/', 'private', 'POST', {'cost': 1})
    private_post_nexo_withdrawal = privatePostNexoWithdrawal = Entry('nexo_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_nexo_address = privatePostNexoAddress = Entry('nexo_address/', 'private', 'POST', {'cost': 1})
    private_post_ust_withdrawal = privatePostUstWithdrawal = Entry('ust_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ust_address = privatePostUstAddress = Entry('ust_address/', 'private', 'POST', {'cost': 1})
    private_post_ant_withdrawal = privatePostAntWithdrawal = Entry('ant_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ant_address = privatePostAntAddress = Entry('ant_address/', 'private', 'POST', {'cost': 1})
    private_post_gods_withdrawal = privatePostGodsWithdrawal = Entry('gods_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_gods_address = privatePostGodsAddress = Entry('gods_address/', 'private', 'POST', {'cost': 1})
    private_post_rad_withdrawal = privatePostRadWithdrawal = Entry('rad_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_rad_address = privatePostRadAddress = Entry('rad_address/', 'private', 'POST', {'cost': 1})
    private_post_band_withdrawal = privatePostBandWithdrawal = Entry('band_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_band_address = privatePostBandAddress = Entry('band_address/', 'private', 'POST', {'cost': 1})
    private_post_inj_withdrawal = privatePostInjWithdrawal = Entry('inj_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_inj_address = privatePostInjAddress = Entry('inj_address/', 'private', 'POST', {'cost': 1})
    private_post_rly_withdrawal = privatePostRlyWithdrawal = Entry('rly_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_rly_address = privatePostRlyAddress = Entry('rly_address/', 'private', 'POST', {'cost': 1})
    private_post_rndr_withdrawal = privatePostRndrWithdrawal = Entry('rndr_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_rndr_address = privatePostRndrAddress = Entry('rndr_address/', 'private', 'POST', {'cost': 1})
    private_post_vega_withdrawal = privatePostVegaWithdrawal = Entry('vega_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_vega_address = privatePostVegaAddress = Entry('vega_address/', 'private', 'POST', {'cost': 1})
    private_post_1inch_withdrawal = privatePost1inchWithdrawal = Entry('1inch_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_1inch_address = privatePost1inchAddress = Entry('1inch_address/', 'private', 'POST', {'cost': 1})
    private_post_ens_withdrawal = privatePostEnsWithdrawal = Entry('ens_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ens_address = privatePostEnsAddress = Entry('ens_address/', 'private', 'POST', {'cost': 1})
    private_post_mana_withdrawal = privatePostManaWithdrawal = Entry('mana_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_mana_address = privatePostManaAddress = Entry('mana_address/', 'private', 'POST', {'cost': 1})
    private_post_lrc_withdrawal = privatePostLrcWithdrawal = Entry('lrc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_lrc_address = privatePostLrcAddress = Entry('lrc_address/', 'private', 'POST', {'cost': 1})
    private_post_ape_withdrawal = privatePostApeWithdrawal = Entry('ape_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ape_address = privatePostApeAddress = Entry('ape_address/', 'private', 'POST', {'cost': 1})
    private_post_mpl_withdrawal = privatePostMplWithdrawal = Entry('mpl_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_mpl_address = privatePostMplAddress = Entry('mpl_address/', 'private', 'POST', {'cost': 1})
    private_post_euroc_withdrawal = privatePostEurocWithdrawal = Entry('euroc_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_euroc_address = privatePostEurocAddress = Entry('euroc_address/', 'private', 'POST', {'cost': 1})
    private_post_sol_withdrawal = privatePostSolWithdrawal = Entry('sol_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_sol_address = privatePostSolAddress = Entry('sol_address/', 'private', 'POST', {'cost': 1})
    private_post_dot_withdrawal = privatePostDotWithdrawal = Entry('dot_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_dot_address = privatePostDotAddress = Entry('dot_address/', 'private', 'POST', {'cost': 1})
    private_post_near_withdrawal = privatePostNearWithdrawal = Entry('near_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_near_address = privatePostNearAddress = Entry('near_address/', 'private', 'POST', {'cost': 1})
    private_post_doge_withdrawal = privatePostDogeWithdrawal = Entry('doge_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_doge_address = privatePostDogeAddress = Entry('doge_address/', 'private', 'POST', {'cost': 1})
    private_post_flr_withdrawal = privatePostFlrWithdrawal = Entry('flr_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_flr_address = privatePostFlrAddress = Entry('flr_address/', 'private', 'POST', {'cost': 1})
    private_post_dgld_withdrawal = privatePostDgldWithdrawal = Entry('dgld_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_dgld_address = privatePostDgldAddress = Entry('dgld_address/', 'private', 'POST', {'cost': 1})
    private_post_ldo_withdrawal = privatePostLdoWithdrawal = Entry('ldo_withdrawal/', 'private', 'POST', {'cost': 1})
    private_post_ldo_address = privatePostLdoAddress = Entry('ldo_address/', 'private', 'POST', {'cost': 1})
