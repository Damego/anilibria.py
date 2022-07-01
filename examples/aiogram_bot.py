"""
Совместное использование aiogram и anilibria.py.
"""


from aiogram import Bot, Dispatcher, types, executor
from anilibria import AniLibriaClient, TitleUpdateEvent

import logging


logging.basicConfig(level=logging.INFO)


bot = Bot("bot token")
dp = Dispatcher(bot)
ani_client = AniLibriaClient(proxy="your_proxy.com:80")


@ani_client.event()
async def on_connect():
    print("Anilibria connected")


@ani_client.on_title(id=8700)
async def on_anime(event: TitleUpdateEvent):
    print("Вышла новая серия технолайза! (хз что это)")


@dp.message_handler()
async def random(message: types.Message):
    if message.text != "!random":
        return
    title = await ani_client.get_random_title()
    name = title.names["ru"]
    await message.answer(name)

if __name__ == "__main__":
    ani_client.startwith(dp.start_polling())  # ! Not executor.start_polling(dp)
