import discord.ext.commands as commands
import marvelous.settings as settings
import discord


client: commands.Bot = commands.Bot(
    command_prefix="!erai ",
    intents=discord.Intents.all(),
    proxy=settings.network.proxy
)
