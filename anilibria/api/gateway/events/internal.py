from ...models import Episode, Title
from ...models.attrs_utils import define
from .base import BaseEvent

__all__ = (
    "Connect",
    "TitleEpisode",
)


@define()
class Connect(BaseEvent):
    """
    Модель для события ``on_connect``. Вызывается при подключении к АПИ анилибрии. Может вызываться несколько раз.

    .. code-block:: python

      @client.on(Connect)
      async def connected(event: Connect):
          ...
    """

    api_version: str
    "Версия АПИ анилибрии"


@define()
class TitleEpisode(BaseEvent):
    """
    Модель для ивента `on_title_episode`. Вызывается при полной загрузки эпизода на сервер.

    .. code-block:: python

      @client.on(TitleEpisode)
      async def on_title_episode(event: TitleEpisode):
          ...
    """

    title: Title
    "Объект тайтла"
    episode: Episode
    "Объект загруженного эпизода"
