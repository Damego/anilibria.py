from dataclasses import dataclass, field
from typing import List, Optional

from .title import Title


@dataclass(slots=True)
class Schedule:
    day: Optional[int] = field(default=None)
    list: Optional[List[Title]] = field(default_factory=list)

    def __post_init__(self):
        self.list = [Title(**title) for title in self.list]


@dataclass(slots=True, frozen=True)
class YouTubeData:
    id: Optional[int] = field(default=None)
    title: Optional[str] = field(default=None)
    image: Optional[str] = field(default=None)
    youtube_id: Optional[str] = field(default=None)
    timestamp: Optional[int] = field(default=None)


@dataclass(slots=True, frozen=True)
class SeedStats:
    downloaded: Optional[int] = field(default=None)
    uploaded: Optional[int] = field(default=None)
    user: Optional[str] = field(default=None)
