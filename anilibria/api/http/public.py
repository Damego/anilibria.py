from ...utils import dict_filter_none
from .request import Request
from .route import Route

__all__ = ("PublicRequest",)


class PublicRequest(Request):
    def __init__(
        self,
        proxy: str | None = None,
    ) -> None:
        super().__init__(proxy)

    # v1
    """
    Представляет собой запросы на сайт "https://www.anilibria.tv/public"
    Здесь не будут реализованы методы для "/api", так как существует v2, в котором точно такие же методы,
    и к тому же документация к "/api" не обновлялась более двух лет.
    """

    async def login(self, mail: str, password: str) -> dict:
        payload: dict = {"mail": mail, "passwd": password}
        route = Route("POST", "/login.php", is_v1=True)

        return await self.request(route, data=payload)

    # v3

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
        return await self.request(Route("GET", "/title"), payload)

    async def get_titles(
        self,
        id_list: list[int] | None = None,
        code_list: list[str] | None = None,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            id_list=id_list,
            code_list=code_list,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/title/list"), payload)

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
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/title/updates"), payload)

    async def get_changes(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        description_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/title/changes"), payload)

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
        return await self.request(Route("GET", "/title/schedule"), payload)

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
        return await self.request(Route("GET", "/title/random"), payload)

    async def get_youtube(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        since: int | None = None,
        after: int | None = None,
        limit: int | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/youtube"), payload)

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
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/feed"), payload)

    async def get_years(self) -> list[int]:
        return await self.request(Route("GET", "/years"))

    async def get_genres(self, sorting_type: int = 0) -> list[str]:
        payload: dict = dict_filter_none(
            sorting_type=sorting_type,
        )
        return await self.request(Route("GET", "/genres"), payload)

    async def get_team(self) -> dict:
        return await self.request(Route("GET", "/team"))

    async def get_seed_stats(
        self,
        users: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        sort_by: str | None = None,
        order: int | None = None,
        limit: int | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
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
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/torrent/seed_stats"), payload)

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
        return await self.request(Route("GET", "/torrent/rss"), payload)

    async def search_titles(
        self,
        search: list[str] | None = None,
        year: list[str] | None = None,
        season_code: list[str] | None = None,
        genres: list[str] | None = None,
        team: list[str] | None = None,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        include: list[str] | None = None,
        description_type: str | None = None,
        playlist_type: str | None = None,
        after: int | None = None,
        limit: int | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(
            search=search,
            year=year,
            season_code=season_code,
            genres=genres,
            team=team,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/title/search"), payload)

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
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> dict:
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
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/title/search/advanced"), payload)

    async def get_user(
        self,
        session: str,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
    ) -> dict:
        payload = dict_filter_none(
            session=session,
            filter=filter,
            remove=remove,
        )

        return await self.request(Route("GET", "/user"), payload)

    async def get_user_favorites(
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
        return await self.request(Route("GET", "/user/favourites"), payload)

    async def add_user_favorite(self, session: str, title_id: int) -> dict:
        payload: dict = dict_filter_none(session=session, title_id=title_id)
        return await self.request(Route("PUT", "/user/favourites/add"), payload)

    async def remove_user_favorite(self, session: str, title_id: int) -> dict:
        payload: dict = dict_filter_none(session=session, title_id=title_id)
        return await self.request(Route("DELETE", "/user/favourites/remove"), payload)

    async def get_title_franchises(
        self,
        id: int,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
    ) -> dict:
        payload: dict = dict_filter_none(id=id, filter=filter, remove=remove)
        return await self.request(Route("GET", "/title/franchises"), payload)

    async def get_franchises(
        self,
        filter: list[str] | None = None,
        remove: list[str] | None = None,
        limit: int | None = None,
        after: int | None = None,
        page: int | None = None,
        items_per_page: int | None = None,
    ) -> list[dict]:
        payload: dict = dict_filter_none(
            filter=filter,
            remove=remove,
            limit=limit,
            after=after,
            page=page,
            items_per_page=items_per_page,
        )
        return await self.request(Route("GET", "/franchise/list"), payload)
