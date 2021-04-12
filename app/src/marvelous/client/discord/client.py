from discord.ext import commands
import discord
from marvelous.client.discord.commands.help import MarvelousHelpCommand

INITIAL_EXTENSIONS = [
    "marvelous.client.discord.commands.ranking",
    "marvelous.client.discord.commands.me",
    "marvelous.client.discord.events.on_reaction_add",
    "marvelous.client.discord.events.on_reaction_remove",
    "marvelous.client.discord.events.on_message",
    "marvelous.client.discord.tasks.reset_survival_bonus",
    "marvelous.client.discord.tasks.reset_daily_steps",
    "marvelous.client.discord.tasks.reset_super_marvelous_left",
]
COMMAND_PREFIX = "!erai "


def init_bot() -> commands.Bot:
    _bot = commands.Bot(
        command_prefix=COMMAND_PREFIX,
        help_command=MarvelousHelpCommand(),
        intents=discord.Intents.all(),
    )

    for extension in INITIAL_EXTENSIONS:
        _bot.load_extension(extension)
    return _bot


bot: commands.Bot = init_bot()


@bot.event
async def on_ready():
    print("BOT READY")
