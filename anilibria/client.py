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
            _name = "on_" + (name or coro.__name__)
            self._websocket._listener.add_event(coro, _name)

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
    ) -> Title:
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

    async def get_titles(
        self,
        id_list: Optional[List[int]] = None,
        code_list: Optional[List[str]] = None,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[Title]:
        data = await self._websocket._http.get_titles(
            id_list=id_list,
            code_list=code_list,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return [Title(**_) for _ in data]

    async def get_updates(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Title]:
        data = await self._websocket._http.get_updates(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return [Title(**_) for _ in data]

    async def get_changes(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        description_type: Optional[str] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Title]:
        data = await self._websocket._http.get_changes(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            after=after,
            limit=limit,
        )
        return [Title(**_) for _ in data]

    async def get_schedule(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        days: List[str] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[Schedule]:
        data = await self._websocket._http.get_schedule(
            filter=filter,
            remove=remove,
            include=include,
            days=days,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return [Schedule(**_) for _ in data]

    async def get_random_title(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> Title:
        data = await self._websocket._http.get_random_title(
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return Title(**data)

    async def get_youtube(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[YouTubeData]:
        data = await self._websocket._http.get_youtube(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
        )
        return [YouTubeData(**_) for _ in data]

    async def get_feed(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[
        Title
    ]:  # ? Can be here youtube videos? Docs says yes, but I didn't see any data about this
        data = await self._websocket._http.get_feed(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return [Title(**_) for _ in data]

    async def get_years(self) -> List[int]:
        return await self._websocket._http.get_years()

    async def get_genres(self, sorting_type: int = 0) -> List[str]:
        return await self._websocket._http.get_genres(sorting_type=sorting_type)

    async def get_caching_nodes(self) -> List[str]:
        return await self._websocket._http.get_caching_nodes()

    async def get_team(self) -> Team:
        data = await self._websocket._http.get_team()
        return Team(**data)

    async def get_seed_stats(
        self,
        users: List[str],
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
        after: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[SeedStats]:
        data = await self._websocket._http.get_seed_stats(
            users=users,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            sort_by=sort_by,
            order=order,
            limit=limit,
        )
        return [SeedStats(**_) for _ in data]

    async def get_rss(
        self,
        rss_type: str,
        since: Optional[int] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> str:  # ? str?
        data = await self._websocket._http.get_rss(
            rss_type=rss_type,
            session=self._websocket.session_id,
            since=since,
            after=after,
            limit=limit,
        )
        print(data)
        print(type(data))
        return data

    async def search_titles(
        self,
        search: Optional[List[str]] = None,
        year: Optional[List[str]] = None,
        season_code: Optional[List[str]] = None,
        genres: Optional[List[str]] = None,
        voice: Optional[List[str]] = None,
        translator: Optional[List[str]] = None,
        editing: Optional[List[str]] = None,
        decor: Optional[List[str]] = None,
        timing: Optional[List[str]] = None,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Title]:
        data = await self._websocket._http.search_titles(
            search=search,
            year=year,
            season_code=season_code,
            genres=genres,
            voice=voice,
            translator=translator,
            editing=editing,
            decor=decor,
            timing=timing,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return [Title(**_) for _ in data]

    async def advanced_search(
        self,
        query: str,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
        after: Optional[int] = None,
        order_by: str = None,
        limit: Optional[int] = None,
        sort_direction: Optional[int] = None,
    ) -> List[Title]:
        data = await self._websocket._http.advanced_search(
            query=query,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            order_by=order_by,
            limit=limit,
            sort_direction=sort_direction,
        )
        return [Title(**_) for _ in data]

    async def get_favourites(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[Title]:
        data = await self._websocket._http.get_favourites(
            session=self._websocket.session_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return [Title(**_) for _ in data]

    async def add_favourite(self, title_id: int) -> dict:
        await self._websocket._http.add_favourite(
            session=self._websocket.session_id, title_id=title_id
        )

    async def del_favourite(self, title_id: int) -> dict:
        await self._websocket._http.del_favourite(
            session=self._websocket.session_id, title_id=title_id
        )

    def start(self):
        self._loop.run_until_complete(self._start())
