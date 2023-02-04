"""
Совместное использование aiogram v2 и anilibria.py.
"""


import logging

from aiogram import Bot, Dispatcher, types

from anilibria import AniLibriaClient, TitleEpisode

logging.basicConfig(level=logging.INFO)


bot = Bot("bot token")
dp = Dispatcher(bot)
ani_client = AniLibriaClient()


@ani_client.event()
async def on_connect():
    print("Anilibria connected")


@ani_client.on(TitleEpisode)
async def new_episode(event: TitleEpisode):
    if event.title.code == "otonari-no-tenshi-sama-ni-itsunomanika-dame-ningen-ni-sareteita-ken":
        # Ангел по соседству
        await bot.send_message(
            123456789, f"Вышла {event.episode.episode}-я серия {event.title.names.ru}"
        )


@dp.message_handler()
async def random(message: types.Message):
    if message.text != "!random":
        return
    title = await ani_client.get_random_title()
    name = title.names.ru
    await message.answer(name)


if __name__ == "__main__":
    # Обратите внимание, здесь используется dp.start_polling(), а не executor.start_polling()

    # В executor.start_polling() происходит много чего ещё, перед стартом бота,
    # если эти действия необходимы, откройте Issue об этом
    ani_client.startwith(dp.start_polling())
