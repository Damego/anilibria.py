import asyncio

from aiohttp import WSMessage
from json import loads

from ..http import HTTPCLient
from ..listener import EventListener
from .events import *


URL = "ws://api.anilibria.tv/v2/ws/"


class WebSocketClient:
    def __init__(self, proxy: str = None):
        self._loop = asyncio.get_event_loop()
        self._http = HTTPCLient(proxy)
        self._listener = EventListener()
        self.proxy = proxy

        self._client = None
        self._closed = False
        self.session_id = None

    async def run(self):
        await self.__run()

    async def __run(self):
        async with self._http.request.session.ws_connect(URL) as self._client:
            self._closed = self._client._closed

            if self._closed:
                await self.__run()

            while not self._closed:
                packet = await self._client.receive()
                await self.process_packet(packet)

    async def process_packet(self, packet: WSMessage):
        data = loads(packet.data)
        type = data.get("type")
        if type is None:
            await self._other(data)
        event_name = f"on_{type}"
        if type == EventType.TITLE_UPDATE:
            event = TitleUpdateEvent(**data[type])
            self._listener.dispatch(event_name, event)
        elif type == EventType.PLAYLIST_UPDATE:
            event = PlayListUpdateEvent(**data[type])
            self._listener.dispatch(event_name, event)
        elif type in [
            EventType.ENCODE_START,
            EventType.ENCODE_END,
            EventType.ENCODE_PROGRESS,
        ]:
            event = EncodeEvent(**data[type])
            self._listener.dispatch(event_name, data)
        else:
            print("ANOTHER EVENT", data)

        self._listener.dispatch("on_raw_packet", data)
        # print("Packet dispatched", packet)  # TODO: Use logging

    async def _other(self, data):
        print(data)

    async def login(self, login: str, password: str) -> str:
        data = await self._http.login(login, password)
        self.session_id = data["sessionId"]

    async def subscribe(self, data: dict):
        await self._client.send_json(data)
