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

Ниже представлено самое простое использование библиотеки.

Функция ``on_connect`` будет вызвана после успешного подключения к API anilibria.

Функция ``on_title_update`` будет вызываться после того, как на сервер будет залита новая серия любого тайтла.

.. code-block:: python

  from anilibria import AniLibriaClient, TitleUpdateEvent

  client = AniLibriaClient(proxy="http://0.0.0.0:80")  # proxy - необязательный аргумент

  @client.event
  async def on_connect():
    print("Подключено")
  
  @client.event
  async def on_title_update(event: TitleUpdateEvent):
    print(event.title.names.ru)  # Выведет название тайтла на русском, который обновили.
  
  client.start()


Подписка на определённые тайтлы
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Если вы хотите получать уведомления об определённых тайтлах, то вы можете подписаться на них.

.. code-block:: python

   @client.event
   async def on_title_serie(event: TitleSerieEvent):
       if event.title.code == "texhnolyze":  # Ещё один способ: event.title.names.ru == "Технолайз"
           ...  # Если выйдет новая серия Технолайза, то вызовется эта функция и выполнится условие


Получение информации о тайтле
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
В библиотеке реализована поддержка http запросов. Список всех возможных методов вы можете увидеть [здесь](https://anilibriapy.readthedocs.io/ru/latest/client.html)

.. code-block:: python

   async def some_function():
       title = await client.get_title(code="kimetsu-no-yaiba-yuukaku-hen")
       print(title.description)  # Все атрибуты вы можете найти в документации моделей

Использование с другими библиотеками
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Вы также можете использовать эту библиотеку вместе с другими:

- ``discord.py`` и его форках
- ``aiogram``

Примеры использования представлены `здесь <https://github.com/Damego/anilibria.py/tree/main/examples>`__

.. toctree::
   :maxdepth: 4
   :caption: Страницы:

   api.rst

