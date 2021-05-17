from discord.ext import commands
import discord
from marvelous.client.discord.help import MarvelousHelpCommand
from . import client
from marvelous.settings import env


INITIAL_EXTENSIONS = [
    "marvelous.client.discord.commands",
    "marvelous.client.discord.events",
    "marvelous.client.discord.tasks"
]
if env.run_environment == "development":
    INITIAL_EXTENSIONS += ["marvelous.client.discord.debug"]

COMMAND_PREFIX = "!erai "


async def runner(*args, **kwargs):
    try:
        await client.bot.start(*args, **kwargs)
    finally:
        if not client.bot.is_closed():
            await client.bot.close()


async def start(token: str):
    client.bot = commands.Bot(
        command_prefix=COMMAND_PREFIX,
        help_command=MarvelousHelpCommand(),
        intents=discord.Intents.all(),
        proxy=env.proxy
    )

    for extension in INITIAL_EXTENSIONS:
        client.bot.load_extension(extension)
    await runner(token)
