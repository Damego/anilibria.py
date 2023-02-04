# anilibria.py
**Python async wrapper for anilibria.tv**

## О библиотеке
anilibria.py - это RestAPI и Websocket обёртка API.  
Вы можете ей пользоваться для получения уведомлений о выходе новой серии, получения информации о тайтлах.
 
## Установка

`pip install anilibria.py`  
или  
`poetry add anilibria.py`

## Использование методов клиента

В библиотеке реализована поддержка RESTful API.
Список всех возможных методов вы можете увидеть [здесь](https://anilibriapy.readthedocs.io/ru/latest/client.html)


```python
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
```

## Использование Websocket

АПИ Анилибрии имеет вебсокет, к которому можно подключиться.

```python
from anilibria import AniLibriaClient, Connect


client = AniLibriaClient()


@client.on(Connect)  # Или client.listen(name="on_connect")
async def connected(event: Connect):
   print("Подключено к АПИ")


client.start()

```

Все модели событий вы можете найти [здесь](https://anilibriapy.readthedocs.io/ru/latest/events.html)

### Использование с другими библиотеками
Вы также можете использовать эту библиотеку вместе с другими:
- `discord.py` и его форках.
- `aiogram`

Примеры использования представлены в папке [examples](https://github.com/Damego/anilibria.py/tree/main/examples)

## Документация
[Официальная документация API](https://github.com/anilibria/docs/blob/master/api_v3.md)  
[Документация библиотеки](https://anilibriapy.readthedocs.io/ru/latest/)
