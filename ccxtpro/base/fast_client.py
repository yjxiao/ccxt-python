"""A faster version of aiohttp's websocket client that uses select and other optimizations"""

import asyncio
import collections
from ccxt import NetworkError
from ccxtpro.base.aiohttp_client import AiohttpClient


class FastClient(AiohttpClient):
    transport = None
    max_size = 1
    # equal to the maximum number of frames in a single call to data_received
    # this is done to avoid lag as much as possible

    def __init__(self, url, on_message_callback, on_error_callback, on_close_callback, config={}):
        super(FastClient, self).__init__(url, on_message_callback, on_error_callback, on_close_callback, config)
        # instead of using the deque in aiohttp we implement our own for speed
        # https://github.com/aio-libs/aiohttp/blob/1d296d549050aa335ef542421b8b7dad788246d5/aiohttp/streams.py#L534
        self.stack = collections.deque()

    def receive_loop(self):
        def handler():
            if self.stack:
                message = self.stack.popleft()
                self.handle_message(message)
                self.asyncio_loop.call_soon(handler)

        def feed_data(message, size):
            if not self.stack:
                self.asyncio_loop.call_soon(handler)
            if len(self.stack) > self.max_size:
                while self.stack:
                    self.handle_message(self.stack.popleft())
            self.stack.append(message)

        def feed_eof():
            self.on_error(NetworkError(1006))

        def wrapper(func):
            def parse_frame(buf):
                frames = func(buf)
                self.max_size = max(self.max_size, len(frames))
                return frames
            return parse_frame

        connection = self.connection._conn
        if connection.closed:
            # connection got terminated after the connection was made and before the receive loop ran
            self.on_close(1006)
            return
        self.transport = connection.transport
        ws_reader = connection.protocol._payload_parser
        ws_reader.parse_frame = wrapper(ws_reader.parse_frame)
        ws_reader.queue.feed_data = feed_data
        ws_reader.queue.feed_eof = feed_eof
        # return a future so super class won't complain
        return asyncio.sleep(0)

    def reset(self, error):
        super(FastClient, self).reset(error)
        self.stack.clear()
        if self.transport:
            self.transport.abort()
