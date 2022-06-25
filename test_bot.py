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
client = AniLibriaClient(login=getenv("LOGIN"), password=getenv("PASSWORD"))


@bot.slash_command(name="test")
async def command(interaction: CommandInteraction):
    await client.subscibe()
    await interaction.send("вроде ок")


loop = asyncio.get_event_loop()

task2 = loop.create_task(bot.start(getenv("BOT_TOKEN")))
task1 = loop.create_task(client._start())

gathered = asyncio.gather(task1, task2)
loop.run_until_complete(gathered)