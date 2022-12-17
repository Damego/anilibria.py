try:
    from orjson import loads, dumps
except ImportError:
    from json import loads, dumps

from logging import getLogger

from trio import open_nursery, Nursery
from trio_websocket import open_websocket_url, WebSocketConnection

from . import events
from ..http import HTTPClient
from ..dispatch import Dispatch
from ...const import __api_url__
from ..models.cattrs_utils import converter


log = getLogger("anilibria.gateway")
URL = f"wss://{__api_url__}/ws/"
__all__ = ["GatewayClient"]


class GatewayClient:
    def __init__(self, http: HTTPClient):
        self._connection: WebSocketConnection | None = None
        self._closed: bool = None  # noqa
        self._stopped: bool = None  # noqa
        self.nursery: Nursery = None  # noqa

        self._http: HTTPClient = http
        self.dispatch: Dispatch = Dispatch()

        self._started_up: bool = False

    async def start(self):
        async with open_nursery() as self.nursery:
            self.nursery.start_soon(self.reconnect)

    async def reconnect(self):
        if self.dispatch.nursery is None:
            self.dispatch.nursery = self.nursery

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

            if not self._started_up:
                self.dispatch.call("on_startup")
                self._started_up = True

            data = await self._receive_data()
            if data.get("connection") == "success":
                # I don't think there are will be something other.
                self.dispatch.call("on_connect")

            while not self._closed:
                data = await self._receive_data()

                await self._track_data(data)

    async def _receive_data(self) -> dict:
        response = await self._connection.get_message()
        return loads(response)

    async def _track_data(self, data: dict):
        if not (type := data.get("type")):
            return await self._track_unknown_event(data)

        event_model = self._lookup_event(type)

        if event_model is None:
            log.warning(f"Received an not excepted event `{type}`!")

        obj = converter.structure(data, event_model)
        self.dispatch.call(f"on_{type}", obj)

        # TODO: Implement title_serie event

    @staticmethod
    def _lookup_event(type: str) -> type:
        return {
            "encode_start": events.EncodeStart,
            "encode_progress": events.EncodeProgress,
            "encode_end": events.EncodeEnd,
            "encode_finish": events.EncodeFinish,
            "title_update": events.TitleUpdate,
            "playlist_update": events.PlayListUpdate,
            "torrent_update": events.TorrentUpdate,
        }.get(type)


    async def _track_unknown_event(self, data: dict):
        ...
        # TODO: Subscription event

    async def _match_error(self):
        code: int = self._connection.closed.code

        print("ERROR", code)

    async def _send_message(self, data: dict):
        message = dumps(data)
        await self._connection.send_message(message)

    async def subscribe(self, data: dict):
        await self._send_message(data)
