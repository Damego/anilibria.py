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
    id: Optional[int] = field(default=None)
    player: Optional[Player] = field(default_factory=dict)
    updated_episode: Optional[Serie] = field(default_factory=dict)
    episode: Optional[str] = field(default=None)
    diff: Optional[dict] = field(default_factory=dict)
    reupload: Optional[bool] = field(default=None)

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
    hash: Optional[str] = field(default=None)
    title: Optional[Title] = field(default_factory=dict)
    diff: Optional[dict] = field(default_factory=dict)

    def __post_init__(self):
        self.title = Title(**self.title)  # type: ignore


@dataclass(slots=True)
class TorrentUpdateEvent:
    id: Optional[str] = field(default=None)
    torrents: Optional[Torrents] = field(default_factory=dict)
    updated_torrent_id: Optional[int] = field(default=None)
    diff: Optional[dict] = field(default_factory=dict)
    hash: Optional[str] = field(default=None)

    def __post_init__(self):
        self.torrents = Torrents(**self.torrents)  # type: ignore
