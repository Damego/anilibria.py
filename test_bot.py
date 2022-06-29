"""
Тестовый бот, для разработки вебсокета
"""

import asyncio
from os import getenv

from disnake import CommandInteraction
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv

from anilibria import AniLibriaClient


load_dotenv()

bot = InteractionBot()
client = AniLibriaClient(
    login=getenv("LOGIN"), password=getenv("PASSWORD"), proxy=getenv("PROXY")
)


@client.event(name="on_raw_packet")
async def test(data):
    print(data)


@client.event(name="on_title_update")
async def title_update(data):
    print(data)


@bot.slash_command(name="test")
async def command(interaction: CommandInteraction):
    data = await client.get_feed(limit=100)
    print(len(data))


@bot.event
async def on_ready():
    print("Bot ready")


loop = asyncio.get_event_loop()

task2 = loop.create_task(bot.start(getenv("BOT_TOKEN")))
task1 = loop.create_task(client._start())

gathered = asyncio.gather(task1, task2)
loop.run_until_complete(gathered)
