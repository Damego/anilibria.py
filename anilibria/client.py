from asyncio import get_event_loop
from typing import Coroutine, Optional, List

from .api import WebSocketClient
from .api.models import *


class AniLibriaClient:
    def __init__(self, *, login: str, password: str, proxy: str = None) -> None:
        self.login = login
        self.password = password
        self.proxy = proxy

        self._loop = get_event_loop()
        self._websocket = WebSocketClient(proxy=self.proxy)

    async def _start(self):
        if not self._websocket.session_id:
            await self._websocket.login(self.login, self.password)

        while not self._websocket._closed:
            await self._websocket.run()

    async def subscribe(self):  # TODO: Оно что-то принимает, но что именно, не сказано
        data = {
            "subscribe": {"season": {"year": 2022}}
        }
        await self._websocket.subscribe(data)

    def event(self, name: str = None):
        def decorator(coro: Coroutine):
            self._websocket._listener.add_event(coro, name or coro.__name__)

            return coro
        return decorator

    async def get_title(
        self,
        id: Optional[int] = None,
        code: Optional[str] = None,
        torrent_id: Optional[int] = None,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,  # TODO: Тут значение по умолчанию какое-то
        playlist_type: Optional[str] = None,  # TODO: Тут значение по умолчанию какое-то
        ):
        data = await self._websocket._http.get_title(id=id, code=code, torrent_id=torrent_id, filter=filter, remove=remove, include=include, description_type=description_type, playlist_type=playlist_type)
        title = Title(**data)
        return title

    def start(self):
        self._loop.run_until_complete(self._start())