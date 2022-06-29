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

    async def subscribe(self, data: dict, filter: str, remove: str):
        """
        Оно что-то принимает, но что именно, не сказано. \n
        Принимает filter: str и remove: str. Насчёт первого вопросов нет, но что делать со вторым?
        """
        payload = {"subscribe": data, "filter": filter, "remove": remove}
        await self._websocket.subscribe(payload)

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
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ):
        data = await self._websocket._http.get_title(
            id=id,
            code=code,
            torrent_id=torrent_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return Title(**data)

    def start(self):
        self._loop.run_until_complete(self._start())
