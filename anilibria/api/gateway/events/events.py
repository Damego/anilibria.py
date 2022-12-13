

@define()
class TitleSerie:
    """
    Модель для ивента `on_title_serie` и подписок.

    .. code-block:: python

      @client.event
      async def on_title_serie(event: TitleSerie):
          ...
    """

    title: Title = field(converter=convert(Title))
    episode: Serie = field()  # Нет конвертера, так как передаётся из другой модели
