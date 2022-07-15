from typing import List, Optional

from .request import Request


URL = "http://api.anilibria.tv/v2"
__all__ = ["V2Request"]


class V2Request:
    def __init__(self, request: Request) -> None:
        """
        :param request:
        """
        self.request = request

    def _to_dict(self, **kwargs) -> dict:
        """
        :param kwargs:
        :return:
        :rtype: str
        """
        return {key: value for key, value in kwargs.items() if value is not None}

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
    ) -> dict:
        """

        :param id:
        :param code:
        :param torrent_id:
        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :return:
        :rtype: dict
        """
        payload: dict = self._to_dict(
            id=id,
            code=code,
            torrent_id=torrent_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request.request("GET", f"{URL}/getTitle", payload)

    async def get_titles(
        self,
        id_list: Optional[List[int]] = None,
        code_list: Optional[List[str]] = None,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[dict]:
        """

        :param id_list:
        :param code_list:
        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            id_list=id_list,
            code_list=code_list,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request.request("GET", f"{URL}/getTitles", payload)

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
    ) -> List[dict]:
        """

        :param filter:
        :param remove:
        :param include:
        :param since:
        :param description_type:
        :param playlist_type:
        :param after:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return await self.request.request("GET", f"{URL}/getUpdates", payload)

    async def get_changes(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        description_type: Optional[str] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        """

        :param filter:
        :param remove:
        :param include:
        :param since:
        :param description_type:
        :param after:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            after=after,
            limit=limit,
        )
        return await self.request.request("GET", f"{URL}/getChanges", payload)

    async def get_schedule(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        days: List[str] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[dict]:
        """

        :param filter:
        :param remove:
        :param include:
        :param days:
        :param description_type:
        :param playlist_type:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            days=days,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request.request("GET", f"{URL}/getSchedule", payload)

    async def get_random_title(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> dict:
        """

        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :return:
        :rtype: dict
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request.request("GET", f"{URL}/getRandomTitle", payload)

    async def get_youtube(
        self,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        since: Optional[int] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        """

        :param filter:
        :param remove:
        :param include:
        :param since:
        :param after:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
        )
        return await self.request.request("GET", f"{URL}/getYouTube", payload)

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
    ) -> List[dict]:
        """

        :param filter:
        :param remove:
        :param include:
        :param since:
        :param description_type:
        :param playlist_type:
        :param after:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return await self.request.request("GET", f"{URL}/getFeed", payload)

    async def get_years(self) -> List[int]:
        """

        :return:
        :rtype: List[int]
        """
        return await self.request.request("GET", f"{URL}/getYears")

    async def get_genres(self, sorting_type: int = 0) -> List[str]:
        """

        :param sorting_type:
        :return:
        :rtype: List[str]
        """
        payload: dict = self._to_dict(
            sorting_type=sorting_type,
        )
        return await self.request.request("GET", f"{URL}/getGenres", payload)

    async def get_caching_nodes(self) -> List[str]:
        """

        :return:
        :rtype: List[str]
        """
        return await self.request.request("GET", f"{URL}/getCachingNodes")

    async def get_team(self) -> dict:
        """

        :return:
        :rtype: dict
        """
        return await self.request.request("GET", f"{URL}/getTeam")

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
    ) -> List[dict]:
        """

        :param users:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :param after:
        :param sort_by:
        :param order:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
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
        return await self.request.request("GET", f"{URL}/getSeedStats", payload)

    async def get_rss(
        self,
        rss_type: str,
        session: str,
        since: Optional[int] = None,
        after: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> str:
        """

        :param rss_type:
        :param session:
        :param since:
        :param after:
        :param limit:
        :return:
        :rtype: str
        """
        payload: dict = self._to_dict(
            rss_type=rss_type, session=session, since=since, after=after, limit=limit
        )
        return await self.request.request("GET", f"{URL}/getRSS", payload)

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
    ) -> List[dict]:
        """

        :param search:
        :param year:
        :param season_code:
        :param genres:
        :param voice:
        :param translator:
        :param editing:
        :param decor:
        :param timing:
        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :param after:
        :param limit:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
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
        return await self.request.request("GET", f"{URL}/searchTitles", payload)

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
    ) -> List[dict]:
        """

        :param query:
        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :param after:
        :param order_by:
        :param limit:
        :param sort_direction:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
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
        return await self.request.request("GET", f"{URL}/advancedSearch", payload)

    async def get_favorites(
        self,
        session: str,
        filter: Optional[List[str]] = None,
        remove: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        description_type: Optional[str] = None,
        playlist_type: Optional[str] = None,
    ) -> List[dict]:
        """

        :param session:
        :param filter:
        :param remove:
        :param include:
        :param description_type:
        :param playlist_type:
        :return:
        :rtype: List[dict]
        """
        payload: dict = self._to_dict(
            session=session,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return await self.request.request("GET", f"{URL}/getFavorites", payload)

    async def add_favorite(self, session: str, title_id: int) -> dict:
        """

        :param session:
        :param title_id:
        :return:
        :rtype: dict
        """
        payload: dict = self._to_dict(session=session, title_id=title_id)
        return await self.request.request("PUT", f"{URL}/addFavorite", payload)

    async def del_favorite(self, session: str, title_id: int) -> dict:
        """

        :param session:
        :param title_id:
        :return:
        :rtype: dict
        """
        payload: dict = self._to_dict(session=session, title_id=title_id)
        return await self.request.request("DELETE", f"{URL}/delFavorite", payload)
