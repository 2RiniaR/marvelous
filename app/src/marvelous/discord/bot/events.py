import logging
import discord
from discord.ext import commands
from marvelous.discord import presentation


logger = logging.getLogger(__name__)


@commands.Cog.listener()
async def on_ready():
    logger.info("Discord bot is ready.")


@commands.Cog.listener()
async def on_message(message: discord.Message):
    await presentation.help.show_on_mention(message)
    await presentation.survival_bonus.check_give(message.author, message.channel)


@commands.Cog.listener()
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    presentation.reaction.set_state(payload, True)


@commands.Cog.listener()
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    presentation.reaction.set_state(payload, False)


def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_message)
    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)
