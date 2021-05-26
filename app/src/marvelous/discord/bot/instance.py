import discord
from discord.ext import commands
from marvelous import settings


client: commands.Bot = commands.Bot(
    command_prefix="!erai ",
    intents=discord.Intents.all(),
    proxy=settings.network.proxy
)
