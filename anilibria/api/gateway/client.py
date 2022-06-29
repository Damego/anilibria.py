import asyncio

from aiohttp import WSMessage
from json import loads

from ..http import HTTPCLient
from ..listener import EventListener


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
        if data.get("title_update"):
            # title_data = data["title"]  # KeyError lol. Freak docs
            self._listener.dispatch("title_update", data)
        elif data.get("playlist_update"):
            self._listener.dispatch("playlist_update", data)
        elif data.get("start_encode"):
            self._listener.dispatch("start_encode", data)
        elif data.get("end_encode"):
            self._listener.dispatch("end_encode", data)
        elif data.get("encode_progress"):
            self._listener.dispatch("encode_progress", data)
        else:
            print(data)

        self._listener.dispatch("raw_ani_packet", data)
        # print("Packet dispatched", packet)  # TODO: Use logging

    async def login(self, login: str, password: str) -> str:
        data = await self._http.login(login, password)
        self.session_id = data["sessionId"]

    async def subscribe(self, data: dict):
        await self._client.send_json(data)
