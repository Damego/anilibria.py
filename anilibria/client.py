from asyncio import get_event_loop

from .api import WebSocketClient

# TODO: Добавить листенер для уведомлений и других ивентов.
# * Можно сделать через декоратор для клиента и через сторонний декоратор для каких-либо расширений, например: когов для discord.


class AniLibriaClient:
    def __init__(self, *, login: str, password: str, proxy: str = None) -> None:
        self.login = login
        self.password = password
        self.proxy = proxy

        self._loop = get_event_loop()
        self._websocket = WebSocketClient()

    async def _start(self):
        if not self._websocket.session_id:
            await self._websocket.login(self.login, self.password)

        while not self._websocket._closed:
            await self._websocket.run()

    async def subscibe(self):
        data = {
            "subscribe": {"season": {"year": 2022}}
        }
        await self._websocket.subscribe(data)

    def start(self):
        self._loop.run_until_complete(self._start())