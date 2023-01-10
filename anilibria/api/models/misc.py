from typing import List

from .title import Title
from .attrs_utils import define


__all__ = ("Schedule", "YouTubeData", "SeedStats", "Pagination", "TitleResponse")


@define()
class Schedule:
    day: int
    list: list[Title]


@define()
class YouTubeData:
    id: int
    title: str
    image: str
    youtube_id: str
    timestamp: int
    comments: int
    views: int


@define()
class SeedStats:
    downloaded: int
    uploaded: int
    user: str


@define()
class Pagination:
    current_page: int
    pages: int
    items_per_page: int
    total_items: int


@define()
class TitleResponse:
    list: List[Title]
    pagination: Pagination
