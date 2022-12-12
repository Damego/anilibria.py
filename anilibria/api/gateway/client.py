import pprint

try:
    from orjson import loads, dumps
except ImportError:
    from json import loads, dumps

from asyncio import get_event_loop, get_running_loop, new_event_loop, AbstractEventLoop
from typing import List, Union, Optional
from logging import getLogger
from sys import version_info

from cattrs import structure
from aiohttp import WSMessage, ClientWebSocketResponse, WSMsgType
from aiohttp.http import WS_CLOSED_MESSAGE
from trio import open_nursery
from trio_websocket import open_websocket_url, WebSocketConnection


from .events import (
    TitleUpdate,
    PlayListUpdate,
    EncodeEvent,
    EventType,
    TorrentUpdate,
    TitleSerie,
)
from ..http import HTTPClient
from ..dispatch import EventDispatcher


log = getLogger("anilibria.gateway")
URL = "wss://api.anilibria.tv/v2.13/ws/"
__all__ = ["GatewayClient"]


class GatewayClient:
    def __init__(self, http: HTTPClient):
        self._connection: WebSocketConnection | None = None
        self._closed: bool = None  # noqa
        self._stopped: bool = None  # noqa

        self._http: HTTPClient = http

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
