from typing import Generic, List, TypeVar

from .attrs_utils import define
from .title import Title

T = TypeVar("T")

__all__ = ("Schedule", "YouTubeVideo", "SeedStats", "Pagination", "ListPagination", "User")


@define()
class Schedule:
    day: int
    "День недели"
    list: list[Title]
    "Список тайтлов"


@define()
class YouTubeVideo:
    id: int
    """Айди записи в базе"""
    title: str
    "Название youtube видео"
    image: str
    "Ссылка на превью к видео"
    youtube_id: str
    "Айди видео в youtube"
    timestamp: int
    "Время создания в формате UNIX timestamp"
    comments: int
    "Количество комментариев у видео"
    views: int
    "Количество просмотров у видео"

    @property
    def url(self) -> str:
        """Возвращает полную youtube ссылку на видео"""
        return f"https://youtu.be/{self.youtube_id}"


@define()
class SeedStats:
    user: str
    "Имя пользователя"
    downloaded: int
    "Сколько байт было скачано"
    uploaded: int
    "Сколько байт было загружено"


@define()
class Pagination:
    current_page: int
    "Текущая страница"
    pages: int
    "Всего страниц"
    items_per_page: int
    "Количество элементов на странице"
    total_items: int
    "Всего элементов"


@define()
class ListPagination(Generic[T]):
    pagination: Pagination
    "Объект пагинации"
    list: List[T]
    "Список объектов определённого типа"


@define()
class User:
    login: str | None = None
    "Логин пользователя"
    nickname: str | None = None
    "Ник пользователя"
    email: str | None = None
    "Электронная почта пользователя"
    avatar_original: str | None = None
    "Путь к аватару пользователя"
    avatar_thumbnail: str | None = None
    "Путь к превью аватара пользователя"
    vk_id: str | None = None
    "Айди аккаунта Вконтакте"
    patreon_id: str | None = None
    "Айди аккаунта в Patreon"
