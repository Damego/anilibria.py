from typing import List, Generic, TypeVar

from .title import Title
from .attrs_utils import define

T = TypeVar("T")

__all__ = ("Schedule", "YouTubeVideo", "SeedStats", "Pagination", "ListPagination", "User")


@define()
class Schedule:
    day: int
    list: list[Title]


@define()
class YouTubeVideo:
    id: int
    title: str
    image: str
    youtube_id: str
    timestamp: int
    comments: int
    views: int


@define()
class SeedStats:
    user: str
    downloaded: int
    uploaded: int


@define()
class Pagination:
    current_page: int
    pages: int
    items_per_page: int
    total_items: int


@define()
class ListPagination(Generic[T]):
    pagination: Pagination
    list: List[T]


@define()
class User:
    login: str = None
    nickname: str = None
    email: str = None
    avatar_original: str | None = None
    avatar_thumbnail: str | None = None
    vk_id: str | None = None
    patreon_id: str | None = None
