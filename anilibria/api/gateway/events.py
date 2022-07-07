from typing import Optional

from attrs import define, field

from enum import Enum
from ..models import Player, Serie, Title, Torrents
from ..models.attrs_utils import convert


__all__ = [
    "EventType",
    "EncodeEvent",
    "PlayListUpdateEvent",
    "TitleUpdateEvent",
    "TorrentUpdateEvent",
    "TitleSerieEvent",
]


class EventType(str, Enum):
    """
    Обозначает ивенты, которые принимает Websocket
    """

    TITLE_UPDATE = "title_update"
    PLAYLIST_UPDATE = "playlist_update"
    ENCODE_START = "encode_start"
    ENCODE_PROGRESS = "encode_progress"
    ENCODE_END = "encode_end"
    ENCODE_FINISH = "encode_finish"
    TORRENT_UPDATE = "torrent_update"


@define
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


@define
class PlayListUpdateEvent:
    """
    Модель для ивента ``on_playlist_update``

    .. code-block:: python

      @client.event
      async def on_playlist_update(event: PlayListUpdateEvent):
          ...
    """

    id: Optional[int] = field(default=None)
    player: Optional[Player] = field(converter=convert(Player), default=None)
    updated_episode: Optional[Serie] = field(converter=convert(Serie), default=None)
    episode: Optional[str] = field(default=None)
    diff: Optional[dict] = field(default=None)
    reupload: Optional[bool] = field(default=None)


@define
class TitleUpdateEvent:
    """
    Модель для ивента ``on_title_update``

    .. code-block:: python

      @client.event
      async def on_title_update(event: TitleUpdateEvent):
          ...
    """

    hash: Optional[str] = field(default=None)
    title: Optional[Title] = field(converter=convert(Title), default=None)
    diff: Optional[dict] = field(default=None)


@define
class TorrentUpdateEvent:
    """
    Модель для ивента `on_torrent_update`

    .. code-block:: python

      @client.event
      async def on_torrent_update(event: TorrentUpdateEvent):
          ...
    """

    id: Optional[str] = field(default=None)
    torrents: Optional[Torrents] = field(converter=convert(Torrents), default=None)
    updated_torrent_id: Optional[int] = field(default=None)
    diff: Optional[dict] = field(default=None)
    hash: Optional[str] = field(default=None)


@define
class TitleSerieEvent:
    """
    Модель для ивента `on_title_serie` и подписок.

    .. code-block:: python

      @client.event
      async def on_title_serie(event: TitleSerieEvent):
          ...
    """

    title: Title = field(converter=convert(Title), default=None)
    episode: Serie = field(converter=convert(Serie), default=None)
