from typing import Optional

from enum import Enum
from ...models import Player, Serie, Title, Torrents
from ...models.attrs_utils import convert, define, field
from ...models.enums import StrEnum


__all__ = [
    "EventType",
    "EncodeStart",
    "EncodeProgress",
    "EncodeEnd",
    "EncodeFinish",
    "PlayListUpdate",
    "TitleUpdate",
    "TorrentUpdate",
]


class EventType(StrEnum):
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
class EncodeEvent:
    """
    Базовый объект для события кодирования
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
class EncodeStart(EncodeEvent):
    ...


@define()
class EncodeProgress(EncodeEvent):
    ...


@define()
class EncodeEnd(EncodeEvent):
    ...


@define()
class EncodeFinish(EncodeEvent):
    ...


@define()
class PlayListUpdate:
    """
    Модель для ивента ``on_playlist_update``

    .. code-block:: python

      @client.event
      async def on_playlist_update(event: PlayListUpdate):
          ...
    """

    id: int = field()
    player: Player = field(converter=convert(Player))
    updated_episode: Serie = field(converter=convert(Serie))
    episode: str = field()
    diff: dict = field()
    reupload: bool = field()


@define()
class TitleUpdate:
    """
    Модель для ивента ``on_title_update``

    .. code-block:: python

      @client.event
      async def on_title_update(event: TitleUpdate):
          ...
    """

    hash: str
    title: Title
    diff: dict


@define()
class TorrentUpdate:
    """
    Модель для ивента `on_torrent_update`

    .. code-block:: python

      @client.event
      async def on_torrent_update(event: TorrentUpdate):
          ...
    """

    id: str = field()
    torrents: Torrents = field(converter=convert(Torrents))
    updated_torrent_id: int = field()
    diff: dict = field()
    hash: str = field()
