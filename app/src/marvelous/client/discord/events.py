from logging import getLogger
from discord.ext import commands
import discord
from ..presentation import check_survival_bonus
from .reaction import set_reaction_state
from .help import show_help_on_mention


logger = getLogger(__name__)


@commands.Cog.listener()
async def on_ready():
    logger.info("Discord bot is ready.")


@commands.Cog.listener()
async def on_message(message: discord.Message):
    await show_help_on_mention(message)
    await check_survival_bonus(message.author, message.channel)


@commands.Cog.listener()
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    set_reaction_state(payload, True)


@commands.Cog.listener()
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    set_reaction_state(payload, False)


def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_message)
    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)
