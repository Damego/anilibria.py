from asyncio import get_event_loop
from typing import Coroutine, Optional, List, Union, Any

from .api import WebSocketClient
from .api.models import *


class AniLibriaClient:
    def __init__(self, *, proxy: str = None) -> None:
        self.proxy = proxy
        self._loop = get_event_loop()
        self._websocket = WebSocketClient(proxy=self.proxy)
        self._subscribes: List[dict] = []

    async def _start(self):
        while not self._websocket._closed:
            await self._websocket.run(self._subscribes)

    async def subscribe(self, data: dict, filter: str, remove: str):
        payload = {"subscribe": data, "filter": filter, "remove": remove}
        await self._websocket.subscribe(payload)

    def event(self, coro: Coroutine = None, *, name: str = None, data: dict = None):
        if coro is not None:
            self._websocket._listener.add_event(
                name or coro.__name__, {"coro": coro, "data": data}
            )
            return coro

        def decorator(coro: Coroutine):
            self._websocket._listener.add_event(
                name or coro.__name__, {"coro": coro, "data": data}
            )
            return coro

        return decorator

    def on_title(
        self,
        id: int = None,
        code: str = None,
        names: Dict[str, Union[str, None]] = None,
        announce: str = None,
        status: Dict[str, Union[str, int]] = None,
        posters: Dict[str, str] = None,
        updated: int = None,
        last_change: int = None,
        type: Type = None,
        genres: List[str] = None,
        team: Dict[str, List[str]] = None,
        season: Dict[str, Union[str, int]] = None,
        description: str = None,
        in_favorites: int = None,
        blocked: Dict[str, bool] = None,
        player: Dict[str, Any] = None,
        torrents: Dict[str, Any] = None,
    ):
        """
        Подписывается на тайтл перед запуском клиента
        """

        def decorator(coro: Coroutine):
            return self.event(coro, name="on_title", data=data)

        data = self._to_dict(
            id=id,
            code=code,
            names=names,
            announce=announce,
            status=status,
            posters=posters,
            updated=updated,
            last_change=last_change,
            type=type,
            genres=genres,
            team=team,
            season=season,
            description=description,
            in_favorites=in_favorites,
            blocked=blocked,
            player=player,
            torrents=torrents,
        )
        self._subscribes.append({"subscribe": data})

        return decorator

    def _to_dict(self, **kwargs):
        return {key: value for key, value in kwargs.items() if value is not None}

    async def login(self, mail: str, password: str) -> str:
        data = await self._websocket._http.public.login(mail, password)
        return data.get("sessionId")

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
        data = await self._websocket._http.v2.get_title(
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
        data = await self._websocket._http.v2.get_titles(
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
        data = await self._websocket._http.v2.get_updates(
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
        data = await self._websocket._http.v2.get_changes(
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
        data = await self._websocket._http.v2.get_schedule(
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
        data = await self._websocket._http.v2.get_random_title(
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
        data = await self._websocket._http.v2.get_youtube(
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
        data = await self._websocket._http.v2.get_feed(
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
        return await self._websocket._http.v2.get_years()

    async def get_genres(self, sorting_type: int = 0) -> List[str]:
        return await self._websocket._http.v2.get_genres(sorting_type=sorting_type)

    async def get_caching_nodes(self) -> List[str]:
        return await self._websocket._http.v2.get_caching_nodes()

    async def get_team(self) -> Team:
        data = await self._websocket._http.v2.get_team()
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
        data = await self._websocket._http.v2.get_seed_stats(
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
        data = await self._websocket._http.v2.get_rss(
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
        data = await self._websocket._http.v2.search_titles(
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
        data = await self._websocket._http.v2.advanced_search(
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

    async def get_favorites(
        self,
        session_id: str,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[Title]:
        data = await self._websocket._http.v2.get_favorites(
            session=session_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return [Title(**_) for _ in data]

    async def add_favorite(self, session_id: str, title_id: int) -> dict:
        await self._websocket._http.v2.add_favorite(
            session=session_id, title_id=title_id
        )

    async def del_favorite(self, session_id: str, title_id: int) -> dict:
        await self._websocket._http.v2.del_favorite(
            session=session_id, title_id=title_id
        )

    def start(self):
        self._loop.run_until_complete(self._start())
