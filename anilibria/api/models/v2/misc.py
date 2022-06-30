from dataclasses import dataclass
from typing import List

from .title import Title


@dataclass(slots=True)
class Schedule:
    day: int
    list: List[Title]

    def __post_init__(self):
        self.list = [Title(**title) for title in self.list]


@dataclass(slots=True, frozen=True)
class YouTubeData:
    id: int
    title: str
    image: str
    youtube_id: str
    timestamp: int


@dataclass(slots=True, frozen=True)
class SeedStats:
    downloaded: int
    uploaded: int
    user: str
