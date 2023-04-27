import asyncio
from logging import DEBUG, basicConfig, getLogger
from typing import Callable, Coroutine, Type

from aiohttp import WSServerHandshakeError

from ..api.error import NoArgumentsError
from ..api.gateway.client import GatewayClient
from ..api.gateway.events import BaseEvent, EventType, PlaylistUpdate, TitleEpisode
from ..api.http.client import HTTPClient
from ..api.models import (
    DescriptionType,
    Include,
    ListPagination,
    PlaylistType,
    RSSType,
    Schedule,
    SeedStats,
    Title,
    TitleFranchise,
    TitleTeam,
    User,
    YouTubeVideo,
)
from ..api.models.cattrs_utils import converter
from ..utils.serializer import dict_filter_missing
from ..utils.typings import MISSING, Absent

log = getLogger("anilibria.client")
__all__ = ("AniLibriaClient",)


class AniLibriaClient:
    """
    Основной клиент для взаимодействия с API anilibria.tv.
    """

    def __init__(self, *, proxy: str | None = None, logging: bool | int | None = None) -> None:
        self._http: HTTPClient = HTTPClient(proxy=proxy)
        self._websocket: GatewayClient = GatewayClient(http=self._http)

        if logging is not None:
            if logging is True:
                basicConfig(level=DEBUG)
            else:
                basicConfig(level=logging)

        self.event(self._on_playlist_update, name="on_playlist_update")

        self._loop = asyncio.get_event_loop()

    async def _on_playlist_update(self, event: PlaylistUpdate):
        # Убеждаемся, что ивент затрагивает обновление эпизода, а не другие данные
        if not event.updated_episode or not event.updated_episode.hls:
            return
        # Проверяем, что хотя бы одно из трёх качеств видео отсутствует, иначе это перезалив
        hls = event.updated_episode.hls
        if not hls.sd or not hls.hd or not hls.fhd:
            return
        # Смотрим предыдущие значения:
        # - списка эпизодов
        if (playlist := event.diff.get("list")) is None:
            return
        # - Конкретный эпизод
        if (episode := playlist.get(str(event.updated_episode.episode))) is None:
            return
        # - значения hls эпизода
        if (previous_hls := episode.get("hls")) is None:
            return
        # Если есть предыдущее значение, значит это перезалив
        if all(v is not None for v in previous_hls.values()):
            return

        title = await self.get_title(id=event.id)

        self._websocket.dispatch.call(
            "on_title_episode", TitleEpisode(title=title, episode=event.updated_episode)
        )

    def on_startup(self, coro: Callable[..., Coroutine] = MISSING):
        """
        Декоратор для прослушивания события ``on_startup``. Вызывается только один раз при запуске клиента.

        .. code-block:: python

           @client.on_startup()  # Можно без скобок
           async def start():  # Единственное событие, при котором функция ничего не должна принимать.
               ...

        :param Callable[..., Coroutine] coro: Функция, которая будет вызываться.
        """

        def wrapper(coro: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
            self._websocket.dispatch.register("on_startup", coro)

            return coro

        if coro is not MISSING:
            return wrapper(coro)

        return wrapper

    def on(self, event: Type[BaseEvent]):
        """
        Декоратор для прослушивания событий. Принимает класс события.

        .. code-block:: python

           @client.on(PlaylistUpdate)
           async def name_you_want(event: PlaylistUpdate):
               ...

        :param event: Класс ивента
        """

        def wrapper(coro: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
            event_name: str = "on_" + EventType(event).name.lower()
            self._websocket.dispatch.register(event_name, coro)

            return coro

        return wrapper

    def listen(self, coro: Callable[..., Coroutine] = MISSING, *, name: str = MISSING):
        """
        Декоратор для прослушивания событий. Принимает названия события.

        Примеры использования:

        .. code-block:: python

           @client.listen
           async def on_playlist_update(event: PlaylistUpdate):
               ...

           @client.listen()
           async def on_playlist_update(event: PlaylistUpdate):
               ...

           @client.listen(name="on_playlist_update")
           async def name_you_want(event: PlaylistUpdate):
               ...

        :param Callable[..., Coroutine] coro: Функция, которая будет вызываться.
        :param str name: Название ивента. Например: on_title_update.
        """

        def decorator(coro: Callable[..., Coroutine]):
            self._websocket.dispatch.register(name or coro.__name__, coro)
            return coro

        if coro is not MISSING:
            return decorator(coro)

        return decorator

    def event(self, coro: Callable[..., Coroutine] = MISSING, *, name: str = MISSING):
        """
        Декоратор для прослушивания событий. Принимает названия события.
        Алиас для :meth:`.listen`:

        Примеры использования:

        .. code-block:: python

           @client.listen
           async def on_playlist_update(event: PlaylistUpdate):
               ...

           @client.listen()
           async def on_playlist_update(event: PlaylistUpdate):
               ...

           @client.listen(name="on_playlist_update")
           async def name_you_want(event: PlaylistUpdate):
               ...

        :param Callable[..., Coroutine] coro: Функция, которая будет вызываться.
        :param str name: Название ивента. Например: on_title_update.
        """

        return self.listen(coro, name=name)

    async def subscribe(self, subscribe: dict, filter: str = MISSING, remove: str = MISSING):
        """
        По умолчанию клиент получает все возможные уведомления от API.
        Но можно подписаться на определённые ивенты, или ивенты с каким-то фильтром

        .. code-block:: python

           await client.subscribe(
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
        data = await self._http.login(mail, password)
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

        data = await self._http.get_title(**payload)
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
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
        """
        Возвращает список тайтлов с заданными параметрами.

        :param Absent[list[int]] id_list: Список с ID тайтлами
        :param Absent[list[str]] code_list: Список с кодами тайтлов.
        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
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
            page=page,
            items_per_page=items_per_page,
        )

        data = await self._http.get_titles(**payload)

        return converter.structure(data, ListPagination[Title])

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
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
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
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
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
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_updates(**payload)
        return converter.structure(data, ListPagination[Title])

    async def get_changes(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
        """
        payload = dict_filter_missing(
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
        data = await self._http.get_changes(**payload)
        return converter.structure(data, ListPagination[Title])

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
        data = await self._http.get_schedule(**payload)
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
        data = await self._http.get_random_title(**payload)
        return converter.structure(data, Title)

    async def get_youtube(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[YouTubeVideo]:
        """
        Возвращает список youtube видео в хронологическом порядке с заданными параметрами.

        :param Absent[list[str]] filter: То, что должно быть в ответе.
        :param Absent[list[str]] remove: То, чего не должно быть в ответе.
        :param Absent[list[Include]] include: Список типов файлов которые будут возвращены в виде base64 строки
        :param Absent[int] since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param Absent[int] after: Удаляет первые n записей из выдачи
        :param Absent[int] limit: Количество объектов в ответе. По умолчанию 5
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_youtube(**payload)
        return converter.structure(data, ListPagination[YouTubeVideo])

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
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title | YouTubeVideo]:
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
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
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
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_feed(**payload)

        data["list"]: list
        video: dict

        for index, video in enumerate(data["list"]):
            if title := video.get("title"):
                data["list"][index] = converter.structure(title, Title)
            else:
                data["list"][index] = converter.structure(data["youtube"], YouTubeVideo)

        return converter.structure(data, ListPagination[Title | YouTubeVideo])

    async def get_years(self) -> list[int]:
        """
        Возвращает список годов выхода доступных тайтлов отсортированный по возрастанию.
        """
        return await self._http.get_years()

    async def get_genres(self, sorting_type: int = 0) -> list[str]:
        """
        Возвращает список жанров доступных тайтлов отсортированный по алфавиту.

        :param int sorting_type: Тип сортировки элементов.
        """
        return await self._http.get_genres(sorting_type=sorting_type)

    async def get_team(self) -> TitleTeam:
        """
        Возвращает участников команды когда-либо существовавших на проекте.
        """
        data = await self._http.get_team()
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
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[SeedStats]:
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
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
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
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_seed_stats(**payload)
        return converter.structure(data, ListPagination[SeedStats])

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
            rss_type=rss_type, session_id=session_id, since=since, after=after, limit=limit
        )

        return await self._http.get_rss(**payload)

    async def search_titles(
        self,
        search: Absent[list[str]] = MISSING,
        year: Absent[list[str | int]] = MISSING,
        season_code: Absent[list[str]] = MISSING,
        genres: Absent[list[str]] = MISSING,
        team: Absent[list[str]] = MISSING,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
        """
        Возвращает список тайтлов, найденных по фильтрам.

        :param Absent[list[str]] search: Поиск по именам и описанию.
        :param Absent[list[str | int]] year: Список годов выхода.
        :param Absent[list[str]] season_code: Список сезонов.
        :param Absent[list[str]] genres: Список жанров.
        :param Absent[list[str]] team: Ники участников, работавшие над тайтлом.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[list[Include]] include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :param Absent[int] after: Удаляет первые n записей из выдачи.
        :param Absent[int] limit: Количество объектов в ответе.
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
        """
        payload = dict_filter_missing(
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
        data = await self._http.search_titles(**payload)
        return converter.structure(data, ListPagination[Title])

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
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
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
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
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
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.advanced_search(**payload)
        return converter.structure(data, ListPagination[Title])

    async def get_user(
        self,
        session_id: int,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
    ) -> User:
        """
        Возвращает объект пользователя по текущей сессии.

        :param session_id: Айди сессии.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        """
        payload = dict_filter_missing(session_id=session_id, filter=filter, remove=remove)
        data = await self._http.get_user(**payload)
        return converter.structure(data, User)

    async def get_user_favorites_titles(
        self,
        session_id: str,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlaylistType] = MISSING,
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[Title]:
        """
        Возвращает список избранных тайтлов пользователя

        :param str session_id: ID сессии.
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[list[Include]] include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param Absent[DescriptionType] description_type: Тип получаемого описания.
        :param Absent[PlaylistType] playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
        """
        payload = dict_filter_missing(
            session=session_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_user_favorites(**payload)
        return converter.structure(data, ListPagination[Title])

    async def add_user_favorite_title(self, session_id: str, title_id: int):
        """
        Добавляет тайтл в список избранных

        :param str session_id: ID сессии.
        :param int title_id: ID тайтла.
        """
        await self._http.add_user_favorite(session=session_id, title_id=title_id)

    async def remove_user_favorite_title(self, session_id: str, title_id: int):
        """
        Удаляет тайтл из списка избранных

        :param str session_id: ID сессии.
        :param int title_id: ID тайтла.
        """
        await self._http.remove_user_favorite(session=session_id, title_id=title_id)

    async def get_title_franchises(
        self,
        id: int,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
    ) -> TitleFranchise | None:
        """
        Получение франшизы тайтла

        :param id: ID тайтла
        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        """
        payload = dict_filter_missing(
            id=id,
            filter=filter,
            remove=remove,
        )
        data = await self._http.get_title_franchises(**payload)
        return converter.structure(data, TitleFranchise) if data else None

    async def get_franchises(
        self,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
        page: Absent[int] = MISSING,
        items_per_page: Absent[int] = MISSING,
    ) -> ListPagination[TitleFranchise]:
        """
        Возвращает список всех франшиз

        :param Absent[list[str]] filter: Список значений, которые будут в ответе.
        :param Absent[list[str]] remove: Список значений, которые будут удалены из ответа.
        :param Absent[int] after: Удаляет первые n записей из выдачи.
        :param Absent[int] limit: Количество объектов в ответе.
        :param Absent[int] page: Номер страницы. По умолчанию 1
        :param Absent[int] items_per_page: Количество элементов на одной странице.
        """
        payload = dict_filter_missing(
            filter=filter,
            remove=remove,
            after=after,
            limit=limit,
            page=page,
            items_per_page=items_per_page,
        )
        data = await self._http.get_franchises(**payload)
        return converter.structure(data, ListPagination[TitleFranchise])

    async def astart(self, *, auto_reconnect: bool = True):
        """
        Запускает клиент асинхронно
        """

        while True:
            try:
                await self._websocket.start()
            except WSServerHandshakeError as error:
                if auto_reconnect:
                    log.debug("Websocket disconnected. Reconnecting...")
                    continue
                raise error from error
            except (KeyboardInterrupt, asyncio.CancelledError):
                await self.close()
                break

    def start(self, *, auto_reconnect: bool = True):
        """
        Запускает клиент.
        """

        try:
            self._loop.run_until_complete(self.astart(auto_reconnect=auto_reconnect))
        except KeyboardInterrupt:
            self._loop.run_until_complete(self.close())

    def startwith(self, coro: Coroutine, *, auto_reconnect: bool = True):
        """
        Запускает основной клиент вместе с корутиной.

        :param coro: Корутина для запуска
        :param auto_reconnect: Нужно ли перезапускать клиент после ошибки сервера анилибрии?
        """
        gather = asyncio.gather(
            self._loop.create_task(self.astart(auto_reconnect=auto_reconnect)),
            self._loop.create_task(coro),
        )
        self._loop.run_until_complete(gather)

    async def close(self):
        """
        Закрывает клиент.
        """
        if self._http.session and not self._http.session.closed:
            await self._http.session.close()
            await self._websocket.close()
