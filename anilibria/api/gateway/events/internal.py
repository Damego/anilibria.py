from ...models import Title, Episode
from ...models.attrs_utils import define
from .base import BaseEvent

__all__ = ("Connect", "TitleEpisode", )


@define()
class Connect(BaseEvent):
    api_version: str


@define()
class TitleEpisode(BaseEvent):
    """
    Модель для ивента `on_title_episode`.

    .. code-block:: python

      @client.event
      async def on_title_episode(event: TitleEpisode):
          ...
    """

    title: Title
    episode: Episode
