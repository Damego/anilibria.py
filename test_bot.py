"""
Тестовый бот на disnake, проверки работоспособности библиотеки.
Библиотеку можно также использовть и с другими библиотеками, например: aiogram для телеграм ботов.
Позже я выложу папку с примерами исплользования с другими библиотеками.
"""

import asyncio
from os import getenv

from disnake import CommandInteraction
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv
import logging

#logging.basicConfig(level=logging.DEBUG)

from anilibria import AniLibriaClient, TitleUpdateEvent


# TODO на 30 июня
# * Документация
# * loop = asyncio.get_event_loop() -> DeprecationWarning: There is no current event loop

load_dotenv()

bot = InteractionBot()
client = AniLibriaClient(proxy=getenv("PROXY"))


@client.event(name="on_connect")
async def test():
    print("connected")


@client.on_title(id=8700)
async def on_anime(event: TitleUpdateEvent):
    print("aboba", event)


@client.event(name="on_title_update")
async def title_update(data):
    print(data)


@bot.slash_command(name="test")
async def command(interaction: CommandInteraction):
    ...


@bot.event
async def on_ready():
    print("Bot ready")


loop = asyncio.get_event_loop()

task2 = loop.create_task(bot.start(getenv("BOT_TOKEN")))
task1 = loop.create_task(client._start())

gathered = asyncio.gather(task1, task2)
loop.run_until_complete(gathered)
