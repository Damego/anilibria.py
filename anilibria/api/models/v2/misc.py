from typing import List, Optional

from attrs import define, field

from .title import Title
from ..attrs_utils import convert_list


__all__ = ["Schedule", "YouTubeData", "SeedStats"]


@define
class Schedule:
    day: Optional[int] = field(default=None)
    list: Optional[List[Title]] = field(converter=convert_list(Title), factory=list)


@define
class YouTubeData:
    id: Optional[int] = field(default=None)
    title: Optional[str] = field(default=None)
    image: Optional[str] = field(default=None)
    youtube_id: Optional[str] = field(default=None)
    timestamp: Optional[int] = field(default=None)
    comments: Optional[int] = field(default=None)
    views: Optional[int] = field(default=None)


@define
class SeedStats:
    downloaded: Optional[int] = field(default=None)
    uploaded: Optional[int] = field(default=None)
    user: Optional[str] = field(default=None)
