anilibria.py
============

О библиотеке
************
anilibria.py - это RESTful и Websocket обёртка для API anilibria.tv.

Вы можете ей пользоваться для получение уведомлений о выходе новой серии, получение информации о тайтлах и других вещей.

Установка
*********

``pip install --upgrade anilibria.py``

С использование poetry:
``poetry add anilibria.py``


Использование методов клиента
*****************************

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

Использование Websocket
***********************

АПИ Анилибрии имеет вебсокет, к которому можно подключиться.

.. code-block:: python

   from anilibria import AniLibriaClient, Connect


   client = AniLibriaClient()


   @client.on(Connect)  # Или client.listen(name="on_connect")
   async def connected(event: Connect):
       print("Подключено к АПИ")


   client.start()


Все модели события вы можете найти `здесь <https://anilibriapy.readthedocs.io/ru/latest/events.html>`_


Использование с другими библиотеками
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Вы также можете использовать эту библиотеку вместе с:

- ``discord.py`` и его форках
- ``aiogram``

и с другими.

Примеры использования представлены `здесь <https://github.com/Damego/anilibria.py/tree/main/examples>`__

Документация
^^^^^^^^^^^^
`Официальная документация API <https://github.com/anilibria/docs/blob/master/api_v3.md>`__

`Документация библиотеки <https://anilibriapy.readthedocs.io/ru/latest/>`__
