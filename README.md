# anilibria.py
**Python async wrapper for anilibria.tv**

<hr>

## О библиотеке
anilibria.py - это REST API и Websocket обёртка API. <br>
Вы можете ей пользоваться для получение уведомлений о выходе новой серии, получение информации о тайтлах и других вещей.

## Предупреждение
На данный момент https://anilibria.tv/ заблокирован на территории РФ. <br>
Для того, чтобы воспользоваться библиотекой, вам необходимо использовать VPN или прокси. <br>
Если вы не из России, то можете спокойно ей пользоваться.

## Установка

`pip install anilibria.py` - Пока не работает

## Использование

Ниже представлено самое простое использование библиотеки. <br>
Функция `on_connect` будет вызвана после успешного подключения к API anilibria.
Функция `on_title_update` будет вызываться после того, как на сервер будет залита новая серия любого тайтла. <br>

```py
from anilibria import AniLibriaClient, TitleUpdateEvent

client = AniLibriaClient(proxy="http://0.0.0.0:80")  # proxy - не обязательный аргумент

@client.event
async def on_connect():
  print("Подключено")
  
@client.event
async def on_title_update(event: TitleUpdateEvent):
  print(event.title.names["ru"])  # Выведет название тайтла на русском, который обновили.
  
client.start()
```

### Подписка на определённые тайтлы.

Если вы хотите получать уведомления об определённых тайтлах, то вы можете подписаться на них. <br>

```py
#  Первый способ
@client.event
async def on_connect():
  print("Подключено")
  data = {"id": 8700}
  await client.subscribe(data)
  # Подпишется на тайтл с id 8700.
  # Теперь ивент `on_title_update` будет вызываться только тогда, 
  # когда обновится тайтл, на который вы подписались

#  Второй способ
@client.on_title(id=8700)
async def texhnolyze(event: TitleUpdateEvent):  # Название функции может быть любое
  print("Вышла новая серия технолайза! (хз что это)")

# Оба способа работают даже вместе.

```
Вы также можете использовать эту библиотеку вместе с другими:
- `discord.py` и его форках.
- `aiogram`

Примеры использования представлены в папке [examples](https://github.com/Damego/anilibria.py/tree/main/examples)

## Документация
[Оффициальная документация API](https://github.com/anilibria/docs/blob/master/api_v2.md)
[Документация](https://anilibriapy.readthedocs.io/en/latest/)
