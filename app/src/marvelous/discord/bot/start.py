import marvelous.settings as settings
from . import instance
from .help import MarvelousHelpCommand


INITIAL_EXTENSIONS = [
    "marvelous.discord.bot.commands",
    "marvelous.discord.bot.events",
    "marvelous.discord.bot.tasks"
]
if settings.environment.is_development:
    INITIAL_EXTENSIONS += ["marvelous.discord.bot.debug"]


async def runner(*args, **kwargs):
    try:
        await instance.client.start(*args, **kwargs)
    finally:
        if not instance.client.is_closed():
            await instance.client.close()


async def start(token: str):
    instance.client.help_command = MarvelousHelpCommand()
    for extension in INITIAL_EXTENSIONS:
        instance.client.load_extension(extension)
    await runner(token)
