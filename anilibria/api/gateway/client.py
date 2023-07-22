import asyncio
from logging import getLogger

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType
from orjson import dumps, loads

from ...const import __api_url__
from ..dispatch import Dispatch
from ..http import HTTPClient
from ..models.cattrs_utils import converter
from .events import Connect, EventType, Subscription

log = getLogger("anilibria.gateway")
URL = f"wss://{__api_url__}/ws/"
__all__ = ("GatewayClient",)


class GatewayClient:
    def __init__(self, http: HTTPClient):
        self._connection: ClientWebSocketResponse | None = None
        self._closed: bool = False
        self._stopped: bool = False

        self._http: HTTPClient = http
        self.dispatch: Dispatch = Dispatch()

        self._started_up: bool = False

    @property
    def loop(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        return loop

    async def start(self):
        await self.connect()

    async def close(self):
        if self._connection is not None:
            await self._connection.close()

    async def connect(self):

        if (session := self._http.session) is None or session.closed:
            session = await self._http.create_session()

        async with session.ws_connect(URL) as self._connection:
            self._closed = self._connection.closed

            if not self._started_up:
                self.dispatch.call("on_startup")
                self._started_up = True

            data = await self._receive_data()

            # Information about opened connection
            if data.get("connection") == "success":
                self.dispatch.call("on_connect", converter.structure(data, Connect))

            while not self._closed:
                data = await self._receive_data()

                # Possible only when connection was closed
                if isinstance(data, WSMessage):
                    return

                self._track_data(data)

    async def _receive_data(self) -> dict | WSMessage:
        response = await self._connection.receive()

        if response.type in {WSMsgType.CLOSING, WSMsgType.CLOSED}:
            self._closed = True
            return response

        return response.json(loads=loads)

    def _track_data(self, data: dict):
        log.debug(
            f"Received an event with data {data}",
        )

        type: str
        if not (type := data.get("type")):
            return self._track_unknown_event(data)

        event_model = EventType[type.upper()].value

        if event_model is None:
            return log.warning(f"Received a not excepted event `{type}`!")

        obj = converter.structure(data["data"], event_model)
        self.dispatch.call(f"on_{type}", obj)

    def _track_unknown_event(self, data: dict):
        if "subscribe" in data:
            self.dispatch.call("on_subscription", converter.structure(data, Subscription))

    async def _send_message(self, data: dict):
        await self._connection.send_bytes(dumps(data))

    async def subscribe(self, data: dict):
        await self._send_message(data)
