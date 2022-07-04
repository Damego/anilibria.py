# anilibria.py
**Python async wrapper for anilibria.tv**

![Discord Shield](https://discordapp.com/api/guilds/992384114667823194/widget.png?style=shield)

## О библиотеке
anilibria.py - это RestAPI и Websocket обёртка API.  
Вы можете ей пользоваться для получения уведомлений о выходе новой серии, получения информации о тайтлах.
 
## Установка

`pip install anilibria.py`  
или  
`pip install git+https://github.com/Damego/anilibria.py.git` - (Рекомендуется на текущий момент)

## Использование

Ниже представлено самое простое использование библиотеки.  
Функция `on_connect` будет вызвана после успешного подключения к API anilibria.  
Функция `on_title_update` будет вызываться после того, как на сервер будет залита новая серия любого тайтла.

```py
from anilibria import AniLibriaClient, TitleUpdateEvent

client = AniLibriaClient()

@client.event
async def on_connect():
  print("Подключено")

@client.event
async def on_title_update(event: TitleUpdateEvent):
  print(event.title.names.ru)  # Выведет название тайтла на русском, который обновили.
  
client.start()
```

### Подписка на определённые тайтлы.
Если вы хотите получать уведомления об определённых тайтлах, то вы можете подписаться на них. <br>

```py
@client.on_title_serie(code="texhnolyze")  # Код можно взять из ссылки тайтла
async def texhnolyze(event: PlayListUpdateEvent):  # Название функции может быть любое
    ...
  # Подпишется на тайтл `технолайз`.
  # Функция будет вызываться тогда, когда выйдет новая серия технолайза.

```

### Получение информации о тайтле
В библиотеке реализована поддержка http запросов. Список всех возможных методов вы можете увидеть [здесь](https://anilibriapy.readthedocs.io/ru/latest/client.html)

```py
async def some_function():
    title = await client.get_title(code="kimetsu-no-yaiba-yuukaku-hen")
    print(title.description)  # Все атрибуты вы можете найти в документации моделей
```

### Использование с другими библиотеками
Вы также можете использовать эту библиотеку вместе с другими:
- `discord.py` и его форках.
- `aiogram`

Примеры использования представлены в папке [examples](https://github.com/Damego/anilibria.py/tree/main/examples)

## Документация
[Официальная документация API](https://github.com/anilibria/docs/blob/master/api_v2.md)  
[Документация библиотеки](https://anilibriapy.readthedocs.io/ru/latest/)
