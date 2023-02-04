"""
Совместное использование aiogram v2 и anilibria.py.
"""

import logging

from aiogram import Bot, Dispatcher, types, filters

from anilibria import AniLibriaClient, TitleEpisode

logging.basicConfig(level=logging.INFO)

bot = Bot("bot token", parse_mode="HTML")
ani_client = AniLibriaClient()


@ani_client.event()
async def on_connect():
    print("Anilibria connected")


@ani_client.on(TitleEpisode)
async def new_episode(event: TitleEpisode):
    if event.title.code == "otonari-no-tenshi-sama-ni-itsunomanika-dame-ningen-ni-sareteita-ken":
        # Ангел по соседству
        await bot.send_message(123456789, f"Вышла {event.episode.episode}-я серия {event.title.names.ru}")


@dp.message(filters.Command(commands=["random"]))
async def random(message: types.Message):
    title = await ani_client.get_random_title()
    name = title.names.ru
    await message.answer(name)


if __name__ == "__main__":
    # Обратите внимание, здесь используется dp.start_polling(), а не dp.run_polling()

    dp = Dispatcher()
    ani_client.startwith(dp.start_polling(bot))
