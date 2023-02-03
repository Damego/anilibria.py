from typing import Optional
from enum import Enum

from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from ...models import Player, Episode, Title, Torrents
from ...models.attrs_utils import define
from ...models.cattrs_utils import converter
from .base import BaseEvent
from .internal import Connect, TitleEpisode


__all__ = (
    "EventType",
    "EncodeStart",
    "EncodeProgress",
    "EncodeEnd",
    "EncodeFinish",
    "PlaylistUpdate",
    "TitleUpdate",
    "TorrentUpdate",
)


@define()
class _BaseEncodeEvent(BaseEvent):
    """
    Базовый объект для события кодирования
    """

    id: str
    episode: str


@define()
class _EncodeEvent(_BaseEncodeEvent):
    resolution: str
    quality: str


@define()
class EncodeStart(_EncodeEvent):
    is_reupload: bool


@define()
class EncodeProgress(_EncodeEvent):
    encoded_percent: str


@define()
class EncodeEnd(_EncodeEvent):
    ...


@define()
class EncodeFinish(_BaseEncodeEvent):
    ...


@define()
class PlaylistUpdate(BaseEvent):
    """
    Модель для ивента ``on_playlist_update``

    .. code-block:: python

      @client.event
      async def on_playlist_update(event: PlaylistUpdate):
          ...
    """

    id: Optional[int] = None
    player: Player | None = None
    updated_episode: Episode | None = None
    episode: str | None = None
    diff: dict | None = None
    reupload: bool | None = None


@define()
class TitleUpdate(BaseEvent):
    """
    Модель для ивента ``on_title_update``

    .. code-block:: python

      @client.event
      async def on_title_update(event: TitleUpdate):
          ...
    """

    title: Title = None
    diff: dict = None


@define()
class TorrentUpdate(BaseEvent):
    """
    Модель для ивента `on_torrent_update`

    .. code-block:: python

      @client.event
      async def on_torrent_update(event: TorrentUpdate):
          ...
    """

    id: str = None
    torrents: Torrents = None
    updated_torrent_id: int = None
    diff: dict = None


class EventType(Enum):
    """
    Обозначает ивенты, которые принимает Websocket
    """

    # Anilibria events
    TITLE_UPDATE = TitleUpdate
    PLAYLIST_UPDATE = PlaylistUpdate
    ENCODE_START = EncodeStart
    ENCODE_PROGRESS = EncodeProgress
    ENCODE_END = EncodeEnd
    ENCODE_FINISH = EncodeFinish
    TORRENT_UPDATE = TorrentUpdate

    # Internal events
    TITLE_EPISODE = TitleEpisode
    CONNECT = Connect


# Hooks
# TODO: Find a better place
unstruct_hook = make_dict_unstructure_fn(EncodeStart, converter, is_reupload=override(rename="isReupload"))
struct_hook = make_dict_structure_fn(EncodeStart, converter, is_reupload=override(rename="isReupload"))

converter.register_unstructure_hook(EncodeStart, unstruct_hook)
converter.register_structure_hook(EncodeStart, struct_hook)