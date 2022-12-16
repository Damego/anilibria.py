import pprint

try:
    from orjson import loads, dumps
except ImportError:
    from json import loads, dumps

from logging import getLogger

from cattrs import structure
from trio import open_nursery
from trio_websocket import open_websocket_url, WebSocketConnection


from ..http import HTTPClient
from ..dispatch import Dispatch
from ...const import __api_url__


log = getLogger("anilibria.gateway")
URL = f"wss://{__api_url__}/ws/"
__all__ = ["GatewayClient"]


class GatewayClient:
    def __init__(self, http: HTTPClient):
        self._connection: WebSocketConnection | None = None
        self._closed: bool = None  # noqa
        self._stopped: bool = None  # noqa

        self._http: HTTPClient = http
        self.dispatch: Dispatch = Dispatch()

    async def start(self):
        async with open_nursery() as nursery:
            nursery.start_soon(self.reconnect)

    async def reconnect(self):
        self._closed = True

        if self._closed:
            await self.connect()

    async def connect(self):
        self._stopped = False

        async with open_websocket_url(URL) as self._connection:
            self._closed = self._connection.closed

            if self._stopped:
                await self._connection.aclose()
            if self._closed:
                await self._match_error()

            data = await self._receive_data()
            print(data)

            while not self._closed:
                data = await self._receive_data()

                await self._track_data(data)

    async def _receive_data(self) -> dict:
        response = await self._connection.get_message()
        return loads(response)

    async def _track_data(self, data: dict):
        payload = data  # TODO: structure cattrs
        pprint.pprint(payload)

        if not (type := data.get("type")):
            return await self._track_unknown_event(data)

    async def _track_unknown_event(self, data: dict):
        ...

    async def _match_error(self):
        code: int = self._connection.closed.code

        print("ERROR", code)

    async def _send_message(self, data: dict):
        message = dumps(data)
        await self._connection.send_message(message)

    async def subscribe(self, data: dict):
        await self._send_message(data)
