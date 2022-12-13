from ...models import Title, Serie
from ...models.attrs_utils import define


@define()
class TitleSerie:
    """
    Модель для ивента `on_title_serie` и подписок.

    .. code-block:: python

      @client.event
      async def on_title_serie(event: TitleSerie):
          ...
    """

    title: Title
    episode: Serie
