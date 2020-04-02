# -*- coding: utf-8 -*-

from exchange.test_order_book import test_order_book


async def test_watch_order_book(exchange, symbol):
    # log (symbol.green, 'watching order book...')
    method = 'watchOrderBook'
    if (method in exchange.has) and exchange.has[method]:
        response = None
        now = exchange.milliseconds()
        end = now + 30000
        while now < end:
            response = await getattr(exchange, method)(symbol)
            now = exchange.milliseconds()
            test_order_book(exchange, response, method, symbol)
        return response
    else:
        print(method, 'not supported')


__all__ = ['test_watch_order_book']
