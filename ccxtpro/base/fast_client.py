"""A faster version of aiohttp's websocket client that uses select and other optimizations"""

__author__ = 'Carlo Revelli'

import asyncio
import collections
from ccxt import NetworkError
from ccxt.async_support import Exchange
from ccxtpro.base.aiohttp_client import AiohttpClient

EVERY_MESSAGE = 0
NO_LAG = 1


class FastClient(AiohttpClient):
    change_context = False
    switcher = None
    mode = EVERY_MESSAGE
    max_pending = 256
    transport = None

    def __init__(self, url, on_message_callback, on_error_callback, on_close_callback, config={}):
        super(FastClient, self).__init__(url, on_message_callback, on_error_callback, on_close_callback, config)
        # instead of using the deque in aiohttp we implement our own for speed
        # https://github.com/aio-libs/aiohttp/blob/1d296d549050aa335ef542421b8b7dad788246d5/aiohttp/streams.py#L534
        self.stack = collections.deque()

    async def receive_loop(self):
        async def switcher():
            while self.stack:
                self.handle_message(self.stack.popleft())
                if self.mode == EVERY_MESSAGE and self.change_context:
                    await asyncio.sleep(0)
                    self.change_context = False
                if len(self.stack) > self.max_pending:
                    error_msg = 'You are taking too long to synchronously process each update on EVERY_MESSAGE mode, ' \
                                'as a result you are receiving old updates which is effectively lagging your connection. ' \
                                'Increase client.max_pending to increase the maximum allowed size of your buffer'
                    self.on_error(NetworkError(error_msg))
                    return

        def feed_data(data, size):
            self.stack.append(data)
            if self.switcher is None or self.switcher.done():
                self.switcher = asyncio.ensure_future(switcher())

        def network_error(exception):
            self.on_error(NetworkError(exception if exception else 1006))

        connection = self.connection._conn
        if connection.closed:
            # connection got terminated after the connection was made and before the receive loop ran
            self.on_close(1006)
            return
        self.transport = connection.transport
        protocol = connection.protocol
        queue = protocol._payload_parser.queue
        queue.feed_data = feed_data
        # queue.set_exception = network_error
        protocol.connection_lost = network_error

    def resolve(self, result, message_hash=None):
        super(FastClient, self).resolve(result, message_hash)
        self.change_context = True

    def reset(self, error):
        super(FastClient, self).reset(error)
        self.stack.clear()

    def on_error(self, error):
        if self.verbose:
            self.print(Exchange.iso8601(Exchange.milliseconds()), 'on_error', error)
        self.error = error
        self.reset(error)
        self.on_error_callback(self, error)
        self.transport.close()

    def on_close(self, code):
        if self.verbose:
            self.print(Exchange.iso8601(Exchange.milliseconds()), 'on_close', code)
        if not self.error:
            self.reset(NetworkError(code))
        self.on_close_callback(self, code)
        self.transport.close()
