"""
Совместное использование aiogram и anilibria.py.
"""


import logging

from aiogram import Bot, Dispatcher, types

from anilibria import AniLibriaClient, TitleSerieEvent

logging.basicConfig(level=logging.INFO)


bot = Bot("bot token")
dp = Dispatcher(bot)
ani_client = AniLibriaClient()


@ani_client.event()
async def on_connect():
    print("Anilibria connected")


@ani_client.event
async def on_title_serie(event: TitleSerieEvent):
    if event.title.code == "texhnolyze":
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
