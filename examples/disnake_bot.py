"""
Совместное использование disnake и anilibria.py.
Вместо disnake может быть любой другой форк `discord.py` и сам `discord.py`
"""


from anilibria import AniLibriaClient, TitleUpdateEvent
import disnake
from disnake.ext import commands


bot = commands.InteractionBot()
client = AniLibriaClient(proxy="your_proxy.com:80")


@bot.event
async def on_ready():
    print("Disnake bot ready!")


@client.event()
async def on_connect():
    print("connected")


@client.on_title(id=8700)
async def on_anime(event: TitleUpdateEvent):
    print("Вышла новая серия технолайза! (хз что это)")


@bot.slash_command(name="random")
async def random(interaction: disnake.CommandInteraction):
    title = await client.get_random_title()
    name = title.names["ru"]
    await interaction.send(name)


if __name__ == "__main__":
    client.startwith(bot.start("bot token"))  # ! Not bot.run()
