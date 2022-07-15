from typing import Optional

from enum import Enum
from ..models import Player, Serie, Title, Torrents
from ..models.attrs_utils import convert, define, field, DictSerializer


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


@define()
class EncodeEvent(DictSerializer):
    """
    Модель для ивентов ``on_encode_start``, ``on_encode_progress``, ``on_encode_end`` и ``on_encode_finish``

    .. code-block:: python

      @client.event
      async def on_encode_start(event: EncodeEvent):
          ...
    """

    id: str = field()
    episode: str = field()
    resolution: Optional[str] = field(default=None)
    quality: Optional[str] = field(default=None)
    encoded_percent: Optional[str] = field(default=None)
    is_reupload: Optional[bool] = field(
        default=None, anilibria_name="isReupload"
    )  # idk this is optional or not


@define()
class PlayListUpdateEvent(DictSerializer):
    """
    Модель для ивента ``on_playlist_update``

    .. code-block:: python

      @client.event
      async def on_playlist_update(event: PlayListUpdateEvent):
          ...
    """

    id: int = field()
    player: Player = field(converter=convert(Player))
    updated_episode: Serie = field(converter=convert(Serie))
    episode: str = field()
    diff: dict = field()
    reupload: bool = field()


@define()
class TitleUpdateEvent(DictSerializer):
    """
    Модель для ивента ``on_title_update``

    .. code-block:: python

      @client.event
      async def on_title_update(event: TitleUpdateEvent):
          ...
    """

    hash: str = field()
    title: Title = field(converter=convert(Title))
    diff: dict = field()


@define()
class TorrentUpdateEvent(DictSerializer):
    """
    Модель для ивента `on_torrent_update`

    .. code-block:: python

      @client.event
      async def on_torrent_update(event: TorrentUpdateEvent):
          ...
    """

    id: str = field()
    torrents: Torrents = field(converter=convert(Torrents))
    updated_torrent_id: int = field()
    diff: dict = field()
    hash: str = field()


@define()
class TitleSerieEvent(DictSerializer):
    """
    Модель для ивента `on_title_serie` и подписок.

    .. code-block:: python

      @client.event
      async def on_title_serie(event: TitleSerieEvent):
          ...
    """

    title: Title = field(converter=convert(Title))
    episode: Serie = field()  # Нет конвертера, так как передаётся из другой модели
