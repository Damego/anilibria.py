from typing import Coroutine
from logging import getLogger

from trio import run
from cattrs import structure

from ..api import HTTPClient, GatewayClient
from ..api.models import (
    Title,
    Schedule,
    YouTubeData,
    TitleTeam,
    SeedStats,
    Include,
    DescriptionType,
    PlayListType,
    RSSType,
)
from ..api.dispatch import Event
from ..api.error import NoArgumentsError
from ..utils.typings import MISSING, Absent

log = getLogger("anilibria.client")
__all__ = ["AniLibriaClient"]


class AniLibriaClient:
    """
    Основной клиент для взаимодействия с API anilibria.tv.
    """

    def __init__(self, *, proxy: str = None) -> None:
        self._http: HTTPClient = HTTPClient(proxy=proxy)
        self._websocket: GatewayClient = GatewayClient(http=self._http)

    async def astart(self):
        """
        Запускает websocket.
        """
        await self._websocket.start()

    def event(self, coro: Coroutine = MISSING, *, name: str = MISSING, data: dict = MISSING):
        """
        Делает из функции ивент, который будет вызываться из вебсокета.

        :param coro: Функция, которая будет вызываться.
        :param name: Название ивента. Например: on_title_update.
        :param data: Дополнительные данные.
        """
        if coro is not None:
            self._websocket.dispatcher.add_event(name or coro.__name__, Event(coro=coro, data=data))
            return coro

        def decorator(coro: Coroutine):
            self._websocket.dispatcher.add_event(name or coro.__name__, Event(coro=coro, data=data))
            return coro

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

        :param subscribe: Данные о подписке. Здесь может быть всё то, что принимает веб сокет.
        :param filter: То, что должно быть включено в подписку.
        :param remove: То, что нужно удалить из подписки.
        """
        data = {"subscribe": subscribe}
        if filter is not MISSING:
            data["filter"] = filter
        if remove is not MISSING:
            data["remove"] = remove

        await self._websocket.subscribe(data)

    async def login(self, mail: str, password: str) -> str:
        """
        Входит в аккаунт и возвращает айди сессии.

        .. warning::
           Если запрос идёт из РФ, то для использования необходим VPN или proxy!

        :param mail: Логин или эл.почта
        :param password: Пароль
        :return: ID сессии
        :rtype: str
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
        playlist_type: Absent[PlayListType] = MISSING,
    ) -> Title:
        """
        Возвращает объект тайтла с заданными параметрами.

        :param id: ID тайтла.
        :param code: Код тайтла.
        :param torrent_id: ID торрента
        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :return: Объект тайтла
        :rtype: Title
        """
        if id is MISSING and code is MISSING:
            raise NoArgumentsError("id", "code")

        data = await self._http.v2.get_title(
            id=id,
            code=code,
            torrent_id=torrent_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return structure(data, Title)  # Title(**data)

    async def get_titles(
        self,
        id_list: Absent[list[int]] = MISSING,
        code_list: Absent[list[str]] = MISSING,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов с заданными параметрами.

        :param id_list: Список с айди тайтлами
        :param code_list: Список с кодами тайтлов.
        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :return: Список тайтлов
        :rtype: list[Title]
        """
        if id_list is MISSING and code_list is MISSING:
            raise NoArgumentsError("id_list", "code_list")

        data = await self._http.v2.get_titles(
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
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами.

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param after: Удаляет первые n записей из выдачи
        :param limit: Количество объектов в ответе. По умолчанию 5
        :return: Список тайтлов
        :rtype: list[Title]
        """
        data = await self._http.v2.get_updates(
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

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param description_type: Тип получаемого описания.
        :param after: Удаляет первые n записей из выдачи
        :param limit: Количество объектов в ответе. По умолчанию 5
        :return: Список тайтлов
        :rtype: list[Title]
        """
        data = await self._http.v2.get_changes(
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
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        days: list[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
    ) -> list[Schedule]:
        """
        Возвращает список последних обновлений тайтлов с заданными параметрами по дням.

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param days: Список дней недели, на которые нужно расписание
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :return: Список расписаний
        :rtype: list[Schedule]
        """
        data = await self._http.v2.get_schedule(
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
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
    ) -> Title:
        """
        Возвращает рандомный тайтл с заданными параметрами.

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :return: Объект тайтла
        :rtype: Title
        """
        data = await self._http.v2.get_random_title(
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return Title(**data)

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

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param after: Удаляет первые n записей из выдачи
        :param limit: Количество объектов в ответе. По умолчанию 5
        :return: Список youtube видео
        :rtype: list[YouTubeData]
        """
        data = await self._http.v2.get_youtube(
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
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        since: Absent[int] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title | YouTubeData]:
        """
        Возвращает список тайтлов и youtube видео в хронологическом порядке с заданными параметрами.

        :param filter: То, что должно быть в ответе.
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param since: Список тайтлов, у которых время обновления больше указанного timestamp
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param after: Удаляет первые n записей из выдачи
        :param limit: Количество объектов в ответе. По умолчанию 5
        :return: Список тайтлов и youtube видео.
        :rtype: list[Union[Title, YouTubeData]]
        """
        data = await self._http.v2.get_feed(
            filter=filter,
            remove=remove,
            include=include,
            since=since,
            description_type=description_type,
            playlist_type=playlist_type,
            after=after,
            limit=limit,
        )
        return [
            Title(**_["title"]) if _.get("title") else YouTubeData(**_["youtube"]) for _ in data
        ]

    async def get_years(self) -> list[int]:
        """
        Возвращает список годов выхода доступных тайтлов отсортированный по возрастанию.

        :return: Список с годами.
        """
        return await self._http.v2.get_years()

    async def get_genres(self, sorting_type: int = 0) -> list[str]:
        """
        Возвращает список жанров доступных тайтлов отсортированный по алфавиту.

        :param sorting_type: Тип сортировки элементов.
        :return: Список с жанрами.
        """
        return await self._http.v2.get_genres(sorting_type=sorting_type)

    async def get_caching_nodes(self) -> list[str]:
        """
        Список кеш серверов с которых можно брать данные отсортированные по нагрузке

        :return: Список серверов.
        :rtype: list[str]
        """
        return await self._http.v2.get_caching_nodes()

    async def get_team(self) -> TitleTeam:
        """
        Возвращает список участников команды когда-либо существовавших на проекте.

        :return: Объект команды
        :rtype: Team
        """
        data = await self._http.v2.get_team()
        return TitleTeam(**data)

    async def get_seed_stats(
        self,
        users: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
        after: Absent[int] = MISSING,
        sort_by: Absent[str] = MISSING,
        order: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[SeedStats]:
        """
        Возвращает топ пользователей по количеству загруженного и скачанно через торрент трекер anilibria.

        :param users: Статистика по имени пользователя
        :param remove: То, чего не должно быть в ответе.
        :param include: Список типов файлов которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list)
        :param after: Удаляет первые n записей из выдачи.
        :param sort_by: По какому полю производить сортировку, допустимые значения: downloaded, uploaded, user
        :param order: Направление сортировки 0 - DESC, 1 - ASC.
        :param limit: Количество объектов в ответе. По умолчанию 5
        :return: Список с пользователями
        :rtype: list[SeedStats]
        """
        data = await self._http.v2.get_seed_stats(
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
        rss_type: Absent[RSSType] = MISSING,
        session_id: Absent[str] = MISSING,
        since: Absent[int] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> str:
        """
        Возвращает список обновлений на сайте в одном из форматов RSS ленты.

        :param rss_type: Предпочитаемый формат вывода
        :param session_id: Уникальный идентификатор сессии пользователя
        :param since: Список тайтлов у которых время обновления больше указанного timestamp
        :param after: Удаляет первые n записей из выдачи
        :param limit: Количество объектов в ответе
        :return: RSS
        :rtype: str
        """
        data = await self._http.v2.get_rss(
            rss_type=rss_type,
            session=session_id,
            since=since,
            after=after,
            limit=limit,
        )
        return data

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
        playlist_type: Absent[PlayListType] = MISSING,
        after: Absent[int] = MISSING,
        limit: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов, найденных по фильтрам.

        :param search: Поиск по именам и описанию.
        :param year: Список годов выхода.
        :param season_code: Список сезонов.
        :param genres: Список жанров.
        :param voice: Список войсеров.
        :param translator: Список переводчиков.
        :param editing: Список сабберов.
        :param decor: Список оформителей.
        :param timing: Список таймеров.
        :param filter: Список значений, которые будут в ответе.
        :param remove: Список значений, которые будут удалены из ответа.
        :param include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :param after: Удаляет первые n записей из выдачи.
        :param limit: Количество объектов в ответе.
        :return: Список тайтлов
        :rtype: list[Title]
        """
        data = await self._http.v2.search_titles(
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
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
        after: Absent[int] = MISSING,
        order_by: str = MISSING,
        limit: Absent[int] = MISSING,
        sort_direction: Absent[int] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список тайтлов, найденных по фильтрам.

        :param query:
        :param filter: Список значений, которые будут в ответе.
        :param remove: Список значений, которые будут удалены из ответа.
        :param include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :param after: Удаляет первые n записей из выдачи.
        :param order_by: Ключ по которому будет происходить сортировка результатов
        :param limit: Количество объектов в ответе.
        :param sort_direction: Направление сортировки. 0 - По возрастанию, 1 - По убыванию
        :return: Список тайтлов
        :rtype: list[Title]
        """
        data = await self._http.v2.advanced_search(
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

    async def get_favorites_titles(
        self,
        session_id: str,
        filter: Absent[list[str]] = MISSING,
        remove: Absent[list[str]] = MISSING,
        include: Absent[list[Include]] = MISSING,
        description_type: Absent[DescriptionType] = MISSING,
        playlist_type: Absent[PlayListType] = MISSING,
    ) -> list[Title]:
        """
        Возвращает список избранных тайтлов пользователя

        :param session_id: ID сессии.
        :param filter: Список значений, которые будут в ответе.
        :param remove: Список значений, которые будут удалены из ответа.
        :param include: Список типов файлов, которые будут возвращены в виде base64 строки
        :param description_type: Тип получаемого описания.
        :param playlist_type: Формат получаемого списка серий. Словарь(object) или список(list).
        :return: Список тайтлов
        :rtype: list[Title]
        """
        data = await self._http.v2.get_favorites(
            session=session_id,
            filter=filter,
            remove=remove,
            include=include,
            description_type=description_type,
            playlist_type=playlist_type,
        )
        return [Title(**_) for _ in data]

    async def add_favorite_title(self, session_id: str, title_id: int):
        """
        Добавляет тайтл в список избранных

        :param session_id: ID сессии.
        :param title_id: айди тайтла.
        """
        await self._http.v2.add_favorite(session=session_id, title_id=title_id)

    async def delete_favorite_title(self, session_id: str, title_id: int):
        """
        Добавляет тайтл в список избранных

        :param session_id: ID сессии.
        :param title_id: айди тайтла.
        """
        await self._http.v2.del_favorite(session=session_id, title_id=title_id)

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
