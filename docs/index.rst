anilibria.py
============

О библиотеке
************
anilibria.py - это REST API и Websocket обёртка API.

Вы можете ей пользоваться для получение уведомлений о выходе новой серии, получение информации о тайтлах и других вещей.

Установка
*********

``pip install anilibria.py``

или

``pip install git+https://github.com/Damego/anilibria.py.git`` - (Рекомендуется на текущий момент)

Использование
*************

В библиотеке реализована поддержка RESTful API.
Список всех возможных методов вы можете увидеть `здесь <https://anilibriapy.readthedocs.io/ru/latest/client.html>`__

.. code-block:: python

  import asyncio

  from anilibria import AniLibriaClient


  async def main():
      # Создание клиента
      client = AniLibriaClient(proxy="http://0.0.0.0:80")  # proxy - необязательный аргумент

      # Получение тайтла по его коду
      title = await client.get_title(code="kimetsu-no-yaiba-yuukaku-hen")
      # Вывод описание тайтла
      print(title.description)  # Все атрибуты вы можете найти в документации моделей

  asyncio.run(main())


Использование с другими библиотеками
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Вы также можете использовать эту библиотеку вместе с:

- ``discord.py`` и его форках
- ``aiogram``

и с другими.

Примеры использования представлены `здесь <https://github.com/Damego/anilibria.py/tree/main/examples>`__

.. toctree::
   :maxdepth: 4
   :caption: Страницы:

   api.rst
   events.rst
