import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------
# -*- coding: utf-8 -*-


from ccxt.test.base import test_shared_methods  # noqa E402


async def test_all_proxies(exchange, skipped_properties):
    await test_proxy_url(exchange, skipped_properties)
    await test_http_proxy(exchange, skipped_properties)
    # 'httpsProxy', 'socksProxy'
    await test_proxy_for_exceptions(exchange, skipped_properties)


async def test_proxy_url(exchange, skipped_properties):
    method = 'proxyUrl'
    proxy_server_ip = '5.75.153.75'
    [proxy_url, http_proxy, https_proxy, socks_proxy] = test_shared_methods.remove_proxy_options(exchange, skipped_properties)
    exchange.proxy_url = 'http://' + proxy_server_ip + ':8090/proxy.php?url='
    encoded_colon = '%3A'
    encoded_slash = '%2F'
    ip_check_url = 'https' + encoded_colon + encoded_slash + encoded_slash + 'api.ipify.org'
    response = await exchange.fetch(ip_check_url)
    assert response == proxy_server_ip, exchange.id + ' ' + method + ' test failed. Returned response is ' + response + ' while it should be \"' + proxy_server_ip + '\"'
    # reset the instance property
    test_shared_methods.set_proxy_options(exchange, skipped_properties, proxy_url, http_proxy, https_proxy, socks_proxy)


async def test_http_proxy(exchange, skipped_properties):
    method = 'httpProxy'
    proxy_server_ip = '5.75.153.75'
    [proxy_url, http_proxy, https_proxy, socks_proxy] = test_shared_methods.remove_proxy_options(exchange, skipped_properties)
    exchange.http_proxy = 'http://' + proxy_server_ip + ':8002'
    ip_check_url = 'https://api.ipify.org/'
    response = await exchange.fetch(ip_check_url)
    assert response == proxy_server_ip, exchange.id + ' ' + method + ' test failed. Returned response is ' + response + ' while it should be \"' + proxy_server_ip + '\"'
    # reset the instance property
    test_shared_methods.set_proxy_options(exchange, skipped_properties, proxy_url, http_proxy, https_proxy, socks_proxy)


# with the below method we test out all variations of possible proxy options, so at least 2 of them should be set together, and such cases must throw exception
async def test_proxy_for_exceptions(exchange, skipped_properties):
    method = 'testProxyForExceptions'
    [proxy_url, http_proxy, https_proxy, socks_proxy] = test_shared_methods.remove_proxy_options(exchange, skipped_properties)
    possible_options_array = ['proxyUrl', 'proxyUrlCallback', 'proxy_url', 'proxy_url_callback', 'httpProxy', 'httpProxyCallback', 'http_proxy', 'http_proxy_callback', 'httpsProxy', 'httpsProxyCallback', 'https_proxy', 'https_proxy_callback', 'socksProxy', 'socksProxyCallback', 'socks_proxy', 'socks_proxy_callback']
    for i in range(0, len(possible_options_array)):
        for j in range(0, len(possible_options_array)):
            if j != i:
                proxy_first = possible_options_array[i]
                proxy_second = possible_options_array[j]
                exchange.set_property(exchange, proxy_first, '0.0.0.0')  # actual value does not matter
                exchange.set_property(exchange, proxy_second, '0.0.0.0')  # actual value does not matter
                exception_caught = False
                try:
                    await exchange.fetch('http://example.com')  # url does not matter, it will not be called
                except Exception as e:
                    exception_caught = True
                assert exception_caught, exchange.id + ' ' + method + ' test failed. No exception was thrown, while ' + proxy_first + ' and ' + proxy_second + ' were set together'
                # reset to undefined
                exchange.set_property(exchange, proxy_first, None)
                exchange.set_property(exchange, proxy_second, None)
    # reset the instance property
    test_shared_methods.set_proxy_options(exchange, skipped_properties, proxy_url, http_proxy, https_proxy, socks_proxy)
