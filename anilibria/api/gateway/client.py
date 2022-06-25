import asyncio

from ..http import HTTPCLient


URL = "ws://api.anilibria.tv/v2/ws/"


class WebSocketClient:
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._http = HTTPCLient()
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
                print(packet)

    async def login(self, login: str, password: str) -> str:
        data = await self._http.login(login, password)
        self.session_id = data["sessionId"]

    async def subscribe(self, data: dict):
        await self._client.send_json(data)

