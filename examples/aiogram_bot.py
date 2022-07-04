"""
Совместное использование aiogram и anilibria.py.
"""


from aiogram import Bot, Dispatcher, types
from anilibria import AniLibriaClient, PlayListUpdateEvent

import logging


logging.basicConfig(level=logging.INFO)


bot = Bot("bot token")
dp = Dispatcher(bot)
ani_client = AniLibriaClient()


@ani_client.event()
async def on_connect():
    print("Anilibria connected")


@ani_client.on_title_serie(code="texhnolyze")
async def texhnolyze(event: PlayListUpdateEvent):
    print("Вышла новая серия технолайза! (хз что это)")


@dp.message_handler()
async def random(message: types.Message):
    if message.text != "!random":
        return
    title = await ani_client.get_random_title()
    name = title.names.ru
    await message.answer(name)

if __name__ == "__main__":
    # В executor.start_polling() происходит много чего ещё, перед стартом бота,
    # если эти действия необходимы, откройте Issue об этом
    ani_client.startwith(dp.start_polling())  # ! Not executor.start_polling(dp)
