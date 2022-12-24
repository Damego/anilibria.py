from .request import Request
from .route import Route
from ...utils import dict_filter_none


__all__ = ("PublicRequest", )


class PublicRequest(Request):
    def __init__(self, proxy: str | None = None, ) -> None:
        super().__init__(proxy)

    # v1
    """
    Представляет собой запросы на сайт "https://www.anilibria.tv/public"
    Здесь не будут реализованы методы для "/api", так как существует v2, в котором точно такие же запросы,
    и к тому же документация к "/api" не обновлялась более двух лет.
    """
    async def login(self, mail: str, password: str) -> dict:
        payload: dict = {"mail": mail, "passwd": password}
        route = Route("POST", "/login.php", is_v1=True)

        return await self.request(route, data=payload)

    # v2

    async def get_title(
        self,
        id: int | None = None,
        code: str | None = None,
        torrent_id: int | None = None,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            id=id,
            code=code,
            torrent_id=torrent_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request(Route("GET", "/getTitle"), payload)

    async def get_titles(
        self,
        id_list: list[int] | None = None,
        code_list: list[str] | None = None,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            id_list=id_list,
            code_list=code_list,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request(Route("GET", "/getTitles"), payload)

    async def get_updates(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return await self.request(Route("GET", "/getUpdates"), payload)

    async def get_changes(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        description_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            after=after,
            limit=limit,
        )
        return await self.request(Route("GET", "/getChanges"), payload)

    async def get_schedule(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        days: list[str] = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            days=days,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request(Route("GET", "/getSchedule"), payload)

    async def get_random_title(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request(Route("GET", "/getRandomTitle"), payload)

    async def get_youtube(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
        )
        return await self.request(Route("GET", "/getYouTube"), payload)

    async def get_feed(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return await self.request(Route("GET", "/getFeed"), payload)

    async def get_years(self) -> list[int]:
        return await self.request(Route("GET", "/getYears"))

    async def get_genres(self, sorting_type: int = 0) -> list[str]:
        payload: dict = dict_filter_none(
            sorting_type=sorting_type,
        )
        return await self.request(Route("GET", "/getGenres"), payload)

    async def get_caching_nodes(self) -> list[str]:
        return await self.request(Route("GET", "/getCachingNodes"))

    async def get_team(self) -> dict:
        return await self.request(Route("GET", "/getTeam"))

    async def get_seed_stats(
        self,
        users: list[str],
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        sort_by: str | None = None,
        order: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
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
        return await self.request(Route("GET", "/getSeedStats"), payload)

    async def get_rss(
        self,
        rss_type: str,
        session: str,
        since: int | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> str:
        payload: dict = dict_filter_none(
            rss_type=rss_type, session=session, since=since, after=after, limit=limit
        )
        return await self.request(Route("GET", "/getRSS"), payload)

    async def search_titles(
        self,
        search: list[str] | None = None,
        year: list[str] | None = None,
        season_code: list[str] | None = None,
        genres: list[str] | None = None,
        voice: list[str] | None = None,
        translator: list[str] | None = None,
        editing: list[str] | None = None,
        decor: list[str] | None = None,
        timing: list[str] | None = None,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
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
        return await self.request(Route("GET", "/searchTitles"), payload)

    async def advanced_search(
        self,
        query: str,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        sort_direction: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
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
        return await self.request(Route("GET", "/advancedSearch"), payload)

    async def get_favorites(
        self,
        session: str,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            session=session,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request(Route("GET", "/getFavorites"), payload)

    async def add_favorite(self, session: str, title_id: int) -> dict:
        payload: dict = dict_filter_none(session=session, title_id=title_id)
        return await self.request(Route("PUT", "/addFavorite"), payload)

    async def del_favorite(self, session: str, title_id: int) -> dict:
        payload: dict = dict_filter_none(session=session, title_id=title_id)
        return await self.request(Route("DELETE", "/delFavorite"), payload)
