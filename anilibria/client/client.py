from typing import Coroutine, Callable
from logging import getLogger

from trio import run

from ..api import HTTPClient, GatewayClient
from ..api.models import (
    Title,
    Schedule,
    YouTubeData,
    TitleTeam,
    SeedStats,
    Include,
    DescriptionType,
    PlaylistType,
    RSSType,
)
from ..api.error import NoArgumentsError
from ..utils.typings import MISSING, Absent
from ..utils.serializer import dict_filter_missing
from ..api.models.cattrs_utils import converter

log = getLogger("anilibria.client")
__all__ = ("AniLibriaClient", )


class AniLibriaClient:
    """
    Основной клиент для взаимодействия с API anilibria.tv.
    """

    def __init__(self, *, proxy: str = None) -> None:
        self._http: HTTPClient = HTTPClient(proxy=proxy)
        self._websocket: GatewayClient = GatewayClient(http=self._http)

    def event(self, coro: Callable[..., Coroutine] = MISSING, *, name: str = MISSING):
        """
        Делает из функции ивент, который будет вызываться из вебсокета.

        :param Callable[..., Coroutine] coro: Функция, которая будет вызываться.
        :param str name: Название ивента. Например: on_title_update.
        """

        def decorator(coro: Callable[..., Coroutine]):
            self._websocket.dispatch.register(name or coro.__name__, coro)
            return coro

        if coro is not MISSING:
            return decorator(coro)

        return decorator

    async def subscribe(self, subscribe: dict, filter: str = MISSING, remove: str = MISSING):
        """
        По умолчанию клиент получает все возможные уведомления от API.
        Но можно подписаться на определённые ивенты, или ивенты с каким-то фильтром

        .. code-block:: python

           await subscribe(
               {
                   "title_update": {
                       "title": {
                           "season": {
                               "year": 2022
                           }
                       }
                   }
               }
           )

        :param dict subscribe: Данные о подписке. Здесь может быть всё то, что принимает веб сокет.
        :param str filter: То, что должно быть включено в подписку.
        :param str remove: То, что нужно удалить из подписки.
        """
        data = {"subscribe": subscribe}
        if filter is not MISSING:
            data["filter"] = filter
        if remove is not MISSING:
            data["remove"] = remove

        await self._websocket.subscribe(data)

    async def login(self, mail: str, password: str) -> str:
        """
        Входит в аккаунт.

        .. warning::
           Если запрос идёт из РФ, то для использования необходим VPN или proxy!

        :param str mail: Логин или эл.почта
        :param str password: Пароль
        :return: ID сессии
        """
        data = await self._http.public.login(mail, password)
        return data.get("sessionId")

    async def get_title(
        self,
        id: Absent[int] = MISSING,
        code: Absent[str] = MISSING,
        torrent_id: Absent[int] = MISSING,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
    ) -> Title:
        """
        Возвращает тайтл с заданными параметрами.

        :param Absent[int] id: ID тайтла.
        :param Absent[str] code: Код тайтла.
        :param Absent[int] torrent_id: ID торрента
        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        """
        if id is MISSING and code is MISSING:
            raise NoArgumentsError("id", "code")

        payload: dict = dict_filter_missing(
            id=id,
            code=code,
            torrent_id=torrent_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )

        data = await self._http.v2.get_title(**payload)
        return converter.structure(data, Title)

    async def get_titles(
        self,
        id_list: Absent[list[int]] = MISSING,
        code_list: Absent[list[str]] = MISSING,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов с заданными параметрами.

        :param Absent[list[int]] id_list: Список с ID тайтлами
        :param Absent[list[str]] code_list: Список с кодами тайтлов.
        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        """
        if id_list is MISSING and code_list is MISSING:
            raise NoArgumentsError("id_list", "code_list")

        payload: dict = dict_filter_missing(
            id_list=id_list,
            code_list=code_list,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )

        data = await self._http.v2.get_titles(**payload)

        return converter.structure(data, list[Title])

    async def get_updates(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        data = await self._http.v2.get_updates(**payload)
        return converter.structure(data, list[Title])

    async def get_changes(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            after=after,
            limit=limit,
        )
        data = await self._http.v2.get_changes(**payload)
        return converter.structure(data, list[Title])

    async def get_schedule(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        days: Absent[list[int]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
    ) -> list[Schedule]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами по дням.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[list[int]] days: Список дней недели, на которые нужно расписание
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            days=days,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        data = await self._http.v2.get_schedule(**payload)
        return converter.structure(data, list[Schedule])

    async def get_random_title(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
    ) -> Title:
        """
        Возвращает рандомный тайтл с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        data = await self._http.v2.get_random_title(**payload)
        return converter.structure(data, Title)

    async def get_youtube(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[YouTubeData]:
        """
        Возвращает список youtube видео в хронологическом порядке с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        :return: Список youtube видео
        :rtype: list[YouTubeData]
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
        )
        data = await self._http.v2.get_youtube(**payload)
        return converter.structure(data, list[YouTubeData])

    async def get_feed(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title | YouTubeData]:
        """
        Возвращает список тайтлов и youtube видео в хронологическом порядке с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        :return: Список тайтлов и youtube видео.
        :rtype: list[Union[Title, YouTubeData]]
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        data = await self._http.v2.get_feed(**payload)
        return [
            converter.structure(video.get("title") or video.get("youtube"), Title)
            for video in data
        ]

    async def get_years(self) -> list[int]:
        """
        Возвращает список годов выхода доступных тайтлов отсортированный по возрастанию.
        """
        return await self._http.v2.get_years()

    async def get_genres(self, sorting_type: int = 0) -> list[str]:
        """
        Возвращает список жанров доступных тайтлов отсортированный по алфавиту.

        :param int sorting_type: Тип сортировки элементов.
        """
        return await self._http.v2.get_genres(sorting_type=sorting_type)

    async def get_caching_nodes(self) -> list[str]:
        """
        Список кеш серверов с которых можно брать данные, отсортированные по нагрузке
        """
        return await self._http.v2.get_caching_nodes()

    async def get_team(self) -> TitleTeam:
        """
        Возвращает участников команды когда-либо существовавших на проекте.
        """
        data = await self._http.v2.get_team()
        return converter.structure(data, TitleTeam)

    async def get_seed_stats(
        self,
        users: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        sort_by: Absent[str] = MISSING,
        order: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[SeedStats]:
        """
        Возвращает топ пользователей по количеству загруженного и скачанно через торрент трекер anilibria.

        :param Absent[list[str]] users: Статистика по имени пользователя
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param Absent[int] after: Удаляет первые n записей из выдачи.
        :param Absent[str] sort_by: По какому полю производить сортировку, допустимые значения: downloaded, uploaded, user
        :param Absent[int] order: Направление сортировки 0 - DESC, 1 - ASC.
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        """
        payload = dict_filter_missing(
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
        data = await self._http.v2.get_seed_stats(**payload)
        return converter.structure(data, list[SeedStats])

    async def get_rss(
        self,
        rss_type: Absent[RSSType] = MISSING,
        session_id: Absent[str] = MISSING,
        since: Absent[int] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> str:
        """
        Возвращает список обновлений на сайте в одном из форматов RSS ленты.

        :param Absent[RSSType] rss_type: Предпочитаемый формат вывода
        :param Absent[str] session_id: Уникальный идентификатор сессии пользователя
        :param Absent[int] since: Список тайтлов у которых время обновления больше указанного timestamp
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе
        """
        payload: dict = dict_filter_missing(
            rss_type=rss_type,
            session_id=session_id,
            since=since,
            after=after,
            limit=limit
        )

        return await self._http.v2.get_rss(**payload)

    async def search_titles(
        self,
        search: Absent[list[str]] = MISSING,
        year: Absent[list[str | int]] = MISSING,
        season_code: Absent[list[str]] = MISSING,
        genres: Absent[list[str]] = MISSING,
        voice: Absent[list[str]] = MISSING,
        translator: Absent[list[str]] = MISSING,
        editing: Absent[list[str]] = MISSING,
        decor: Absent[list[str]] = MISSING,
        timing: Absent[list[str]] = MISSING,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов, найденных по фильтрам.

        :param Absent[list[str]] search: Поиск по именам и описанию.
        :param Absent[list[str | int]] year: Список годов выхода.
        :param Absent[list[str]] season_code: Список сезонов.
        :param Absent[list[str]] genres: Список жанров.
        :param Absent[list[str]] voice: Список войсеров.
        :param Absent[list[str]] translator: Список переводчиков.
        :param Absent[list[str]] editing: Список сабберов.
        :param Absent[list[str]] decor: Список оформителей.
        :param Absent[list[str]] timing: Список таймеров.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[list[Include]] include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :param Absent[int] after: Удаляет первые n записей из выдачи.
        :param Absent[int] limit: Количество объектов в ответе.
        """
        payload = dict_filter_missing(
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
        data = await self._http.v2.search_titles(**payload)
        return converter.structure(data, list[Title])

    async def advanced_search(
        self,
        query: str,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        order_by: Absent[str] = MISSING,
        limit: Absent[int] = MISSING,
        sort_direction: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов, найденных по фильтрам.

        :param str query: Запрос для поиска. Может быть название тайтла.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[list[Include]] include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий.
        :param Absent[int] after: Удаляет первые n записей из выдачи.
        :param Absent[str] order_by: Ключ по которому будет происходить сортировка результатов
        :param Absent[int] limit: Количество объектов в ответе.
        :param sort_direction: Направление сортировки. 0 - По возрастанию, 1 - По убыванию
        """
        payload = dict_filter_missing(
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
        data = await self._http.v2.advanced_search(**payload)
        return converter.structure(data, list[Title])

    async def get_favorites_titles(
        self,
        session_id: str,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список избранных тайтлов пользователя

        :param str session_id: ID сессии.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[list[Include]] include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        """
        payload = dict_filter_missing(
            session=session_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        data = await self._http.v2.get_favorites(**payload)
        return converter.structure(data, list[Title])

    async def add_favorite_title(self, session_id: str, title_id: int):
        """
        Добавляет тайтл в список избранных

        :param str session_id: ID сессии.
        :param int title_id: ID тайтла.
        """
        await self._http.v2.add_favorite(session=session_id, title_id=title_id)

    async def delete_favorite_title(self, session_id: str, title_id: int):
        """
        Добавляет тайтл в список избранных

        :param str session_id: ID сессии.
        :param int title_id: ID тайтла.
        """
        await self._http.v2.del_favorite(session=session_id, title_id=title_id)

    async def astart(self):
        """
        Асинхронно запускает вебсокет
        """
        try:
            await self._websocket.start()
        except KeyboardInterrupt:
            ...

    def start(self):
        """
        Запускает клиент.
        """
        run(self.astart)

    async def close(self):
        """
        Закрывает HTTP клиент.
        """
        await self._http.request.session.close()
