from typing import Optional
from dataclasses import dataclass, field

from enum import Enum
from ..models import Player, Serie, Title


class EventType(Enum):
    """
    Обозначает все(нет) ивенты, которые принимает вебсокет
    """
    TITLE_UPDATE = "title_update"
    PLAYLIST_UPDATE = "playlist_update"
    ENCODE_START = "encode_start"
    ENCODE_PROGRESS = "encode_progress"
    ENCODE_END = "encode_end"

    def __eq__(self, __o: object) -> bool:
        return self.value == __o


@dataclass(slots=True, frozen=True)
class EncodeEvent:
    """
    Модель для ивентов ``on_encode_start``, ``on_encode_progress``, ``on_encode_end``

    .. code-block:: python

      @client.event
      async def on_encode_start(event: EncodeEvent):
          ...
    """
    id: str
    episode: str
    resolution: str
    quality: str
    encoded_percent: Optional[str] = field(default=None)


@dataclass(slots=True, frozen=True)
class PlayListUpdateEvent:
    """
    Модель для ивента ``on_playlist_update``

    .. code-block:: python

      @client.event
      async def on_playlist_update(event: PlayListUpdateEvent):
          ...
    """
    id: int
    player: Player
    updated_episode: Serie
    episode: str
    diff: dict
    reupload: bool


@dataclass(slots=True, frozen=True)
class TitleUpdateEvent:
    """
    Модель для ивента ``on_title_update``

    .. code-block:: python

      @client.event
      async def on_title_update(event: TitleUpdateEvent):
          ...
    """
    hash: str
    title: Title
    diff: dict
