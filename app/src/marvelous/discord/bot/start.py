from marvelous import settings
from marvelous.discord import bot


INITIAL_EXTENSIONS = [
    "marvelous.discord.bot.commands",
    "marvelous.discord.bot.events",
    "marvelous.discord.bot.tasks"
]
if settings.environment.is_development:
    INITIAL_EXTENSIONS += ["marvelous.discord.bot.debug"]


async def runner(*args, **kwargs):
    try:
        await bot.instance.client.start(*args, **kwargs)
    finally:
        if not bot.instance.client.is_closed():
            await bot.instance.client.close()


async def start(token: str):
    bot.instance.client.help_command = bot.help.MarvelousHelpCommand()
    for extension in INITIAL_EXTENSIONS:
        bot.instance.client.load_extension(extension)
    await runner(token)
