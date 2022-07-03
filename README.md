# anilibria.py
**Python async wrapper for anilibria.tv**

![Discord Shield](https://discordapp.com/api/guilds/992384114667823194/widget.png?style=shield)

## О библиотеке
anilibria.py - это REST API и Websocket обёртка API. <br>
Вы можете ей пользоваться для получение уведомлений о выходе новой серии, получение информации о тайтлах и других вещей.
 
## Установка

`pip install anilibria.py`

или

`pip install git+https://github.com/Damego/anilibria.py.git`

## Использование

Ниже представлено самое простое использование библиотеки. <br>
Функция `on_connect` будет вызвана после успешного подключения к API anilibria.
Функция `on_title_update` будет вызываться после того, как на сервер будет залита новая серия любого тайтла. <br>

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
@client.event
async def on_connect():
  print("Подключено")
  data = {"id": 8700}
  await client.subscribe(data)
  # Подпишется на тайтл с id 8700.
  # Теперь ивент `on_title_update` будет вызываться только тогда, 
  # когда обновится тайтл, на который вы подписались

```
Вы также можете использовать эту библиотеку вместе с другими:
- `discord.py` и его форках.
- `aiogram`

Примеры использования представлены в папке [examples](https://github.com/Damego/anilibria.py/tree/main/examples)

## Документация
[Оффициальная документация API](https://github.com/anilibria/docs/blob/master/api_v2.md) <br>
[Документация](https://anilibriapy.readthedocs.io/ru/latest/)
