from .title import Title
from .attrs_utils import define


__all__ = ("Schedule", "YouTubeData", "SeedStats")


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
