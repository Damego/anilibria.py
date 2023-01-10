from ...models import Title, Episode
from ...models.attrs_utils import define

__all__ = ("TitleSerie", )


@define()
class TitleSerie:
    """
    Модель для ивента `on_title_serie`.

    .. code-block:: python

      @client.event
      async def on_title_serie(event: TitleSerie):
          ...
    """

    title: Title
    episode: Episode
