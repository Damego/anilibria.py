from typing import Optional
from dataclasses import dataclass, field

from enum import Enum
from ..models import Player, Serie, Title


class EventType(Enum):
    TITLE_UPDATE = "title_update"
    PLAYLIST_UPDATE = "playlist_update"
    ENCODE_START = "encode_start"
    ENCODE_PROGRESS = "encode_progress"
    ENCODE_END = "encode_end"

    def __eq__(self, __o: object) -> bool:
        return self.value == __o


@dataclass(slots=True, frozen=True)
class EncodeEvent:
    id: str
    episode: str
    resolution: str
    quality: str
    encoded_percent: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class PlayListUpdateEvent:
    id: int
    player: Player
    updated_episode: Serie
    episode: str
    diff: dict
    reupload: bool


@dataclass(slots=True, frozen=True)
class TitleUpdateEvent:
    hash: str
    title: Title
    diff: dict
