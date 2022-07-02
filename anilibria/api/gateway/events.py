from typing import Optional
from dataclasses import dataclass, field

from enum import Enum
from ..models import Player, Serie, Title, Torrents


class EventType(Enum):
    """
    Обозначает ивенты, которые принимает вебсокет
    """
    TITLE_UPDATE = "title_update"
    PLAYLIST_UPDATE = "playlist_update"
    ENCODE_START = "encode_start"
    ENCODE_PROGRESS = "encode_progress"
    ENCODE_END = "encode_end"
    ENCODE_FINISH = "encode_finish"
    TORRENT_UPDATE = "torrent_update"

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
    id: Optional[str] = field(default=None)
    episode: Optional[str] = field(default=None)
    resolution: Optional[str] = field(default=None)
    quality: Optional[str] = field(default=None)
    encoded_percent: Optional[str] = field(default=None)


@dataclass(slots=True)
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

    def __post_init__(self):
        self.player = Player(**self.player)  # type: ignore
        self.updated_episode = Serie(**self.updated_episode)  # type: ignore


@dataclass(slots=True)
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

    def __post_init__(self):
        self.title = Title(**self.title)  # type: ignore


@dataclass(slots=True)
class TorrentUpdateEvent:
    id: str
    torrents: Torrents
    updated_torrent_id: int
    diff: dict
    hash: str

    def __post_init__(self):
        self.torrents = Torrents(**self.torrents)  # type: ignore
