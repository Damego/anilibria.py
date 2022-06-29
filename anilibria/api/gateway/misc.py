from typing import Optional
from dataclasses import dataclass, field

from enum import Enum
from ..models import Player, Serie


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


@dataclass(slots=True, frozen=True)
class TitleUpdateEvent:

    diff: dict  # Здесь может быть что угодно, а что именно - не сказано, так что пусть пока будет словарём.


print("playlist_update" == EventType.PLAYLIST_UPDATE)
