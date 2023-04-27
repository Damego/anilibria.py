from enum import Enum
from typing import Optional

from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from ...models import Episode, Player, Title, Torrents
from ...models.attrs_utils import define
from ...models.cattrs_utils import converter
from .base import BaseEvent
from .internal import Connect, TitleEpisode

__all__ = (
    "EncodeStart",
    "EncodeProgress",
    "EncodeEnd",
    "EncodeFinish",
    "PlaylistUpdate",
    "TitleUpdate",
    "TorrentUpdate",
    "Subscription",
    "EventType",
)


@define()
class _BaseEncodeEvent(BaseEvent):
    """
    Базовый объект для события кодирования
    """

    id: str
    "ID тайтла"
    episode: str
    "Номер эпизода"


@define()
class _EncodeEvent(_BaseEncodeEvent):
    resolution: str
    "Разрешение загружаемого эпизода"
    quality: str
    "Качество загружаемого эпизода"


@define()
class EncodeStart(_EncodeEvent):
    """
    Объект для события ``on_encode_start``.
    Вызывается, когда начинается загрузка эпизода на сервер.

    .. code-block:: python

       @client.on(EncodeStart)
       async def start_encode(event: EncodeStart):
           ...
    """

    is_reupload: bool
    "Является ли загрузка эпизода перезаливом"


@define()
class EncodeProgress(_EncodeEvent):
    """
    Объект для события ``on_encode_progress``.
    Вызывается на каждые 5% загрузки.

    .. code-block:: python

       @client.on(EncodeProgress)
       async def progress(event: EncodeProgress):
           ...
    """

    encoded_percent: str
    "Текущий процент загрузки"


@define()
class EncodeEnd(_EncodeEvent):
    """
    Объект для события ``on_encode_end``.
    Вызывается, когда было загружено одно качество эпизода на сервер.

    .. code-block:: python

       @client.on(EncodeEnd)
       async def encode_end(event: EncodeEnd):
           ...
    """

    ...


@define()
class EncodeFinish(_BaseEncodeEvent):
    """
    Объект для события ``on_encode_finish``.
    Вызывается, когда все возможные качества эпизода были загружены на сервер.

    .. code-block:: python

       @client.on(EncodeFinish)
       async def encode_finish(event: EncodeFinish):
           ...
    """

    ...


@define()
class PlaylistUpdate(BaseEvent):
    """
    Модель для ивента ``on_playlist_update``.
    Вызывается при обновлении данных плейлиста тайтла.

    .. code-block:: python

      @client.on(PlaylistUpdate)
      async def on_playlist_update(event: PlaylistUpdate):
          ...
    """

    id: Optional[int] = None
    "ID тайтла"
    player: Player | None = None
    "Обновлённый плейлист"
    updated_episode: Episode | None = None
    "Обновлённый/добавленный эпизод"
    episode: str | None = None
    "Номер эпизода"
    diff: dict | None = None
    "Словарь с предыдущими значениями"
    reupload: bool | None = None
    "Является ли это перезаливом"


@define()
class TitleUpdate(BaseEvent):
    """
    Модель для ивента ``on_title_update``.
    Вызывается при изменении информации о тайтле.

    .. code-block:: python

      @client.on(TitleUpdate)
      async def on_title_update(event: TitleUpdate):
          ...
    """

    title: Title = None
    "Объект тайтла"
    diff: dict = None
    "Предыдущие значения тайтла"


@define()
class TorrentUpdate(BaseEvent):
    """
    Модель для ивента `on_torrent_update`.
    Вызывается при изменении информации о торрент файлах.

    .. code-block:: python

      @client.on(TorrentUpdate)
      async def on_torrent_update(event: TorrentUpdate):
          ...
    """

    id: str = None
    "ID тайтла"
    torrents: Torrents = None
    "Информация о торренте"
    updated_torrent_id: int = None
    "ID обновлённого торрента"
    diff: dict = None
    "Предыдущие значения"


@define()
class Subscription(BaseEvent):
    """
    Модель для ивента `on_subscription`.
    Вызывается при подписке на события, приходящие с websocket.

    .. code-block:: python

      @client.on(Subscription)
      async def event_subscription(event: Subscription):
          ...
    """

    subscribe: str
    "Статус подписки"
    subscription_id: int
    "ID подписки"


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
    SUBSCRIPTION = Subscription

    # Internal events
    TITLE_EPISODE = TitleEpisode
    CONNECT = Connect


# Hooks
# TODO: Find a better place
unstruct_hook = make_dict_unstructure_fn(
    EncodeStart, converter, is_reupload=override(rename="isReupload")
)
struct_hook = make_dict_structure_fn(
    EncodeStart, converter, is_reupload=override(rename="isReupload")
)

converter.register_unstructure_hook(EncodeStart, unstruct_hook)
converter.register_structure_hook(EncodeStart, struct_hook)
