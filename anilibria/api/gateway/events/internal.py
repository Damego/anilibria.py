from ...models import Title, Episode
from ...models.attrs_utils import define

__all__ = ("TitleEpisode", )


@define()
class TitleEpisode:
    """
    Модель для ивента `on_title_episode`.

    .. code-block:: python

      @client.event
      async def on_title_episode(event: TitleEpisode):
          ...
    """

    title: Title
    episode: Episode
