"""
Совместное использование disnake и anilibria.py.
Вместо disnake может быть любой другой форк `discord.py` или сам `discord.py`
"""


import disnake
from disnake.ext import commands

from anilibria import AniLibriaClient, Connect, TitleEpisode

bot = commands.InteractionBot()
client = AniLibriaClient(proxy="your_proxy.com:80")


@bot.event
async def on_ready():
    print("Disnake bot ready!")


@client.on(Connect)
async def on_connect(event: Connect):
    print("connected")


@client.on(TitleEpisode)
async def new_episode(event: TitleEpisode):
    if event.title.code == "otonari-no-tenshi-sama-ni-itsunomanika-dame-ningen-ni-sareteita-ken":
        # Ангел по соседству
        guild = bot.get_guild(1234567890)
        channel = guild.get_channel(987654321)
        await channel.send(f"Вышла {event.episode.episode}-я серия {event.title.names.ru}")


@bot.slash_command(name="random")
async def random(interaction: disnake.CommandInteraction):
    title = await client.get_random_title()
    name = title.names.ru
    await interaction.send(f"Рандомное аниме: {name}.\nСсылка {title.url}")


if __name__ == "__main__":
    client.startwith(bot.start("bot token"))  # ! Not bot.run()
