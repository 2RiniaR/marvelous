from logging import getLogger
from discord.ext import commands
import discord
from ..presentation import check_survival_bonus, add_reaction, remove_reaction
from .reaction import fetch_reaction_event


logger = getLogger(__name__)


@commands.Cog.listener()
async def on_ready():
    logger.info("Discord bot is ready.")


@commands.Cog.listener()
async def on_message(message: discord.Message):
    await check_survival_bonus(message.author, message.channel)


@commands.Cog.listener()
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    event = await fetch_reaction_event(payload)
    await add_reaction(event)


@commands.Cog.listener()
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    event = await fetch_reaction_event(payload)
    await remove_reaction(event)


def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_message)
    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)
