import discord
from . import ReactionEvent
from . import client
from marvelous.helpers import first_match
from typing import Optional


def get_reaction_from_message(emoji: discord.PartialEmoji, message: discord.Message) -> Optional[discord.Reaction]:
    # リアクションが取り消された結果、そのメッセージへのリアクションが消えた（個数が0になった）場合はNoneになる
    return first_match(
        message.reactions, pred=lambda r: str(r.emoji) == str(emoji), default=None
    )


async def fetch_reaction_event(payload: discord.RawReactionActionEvent) -> ReactionEvent:
    guild: discord.Guild = client.bot.get_guild(payload.guild_id)
    sender: discord.Member = guild.get_member(payload.user_id)
    channel: discord.TextChannel = guild.get_channel(payload.channel_id)
    message: discord.Message = await channel.fetch_message(payload.message_id)
    reaction: Optional[discord.Reaction] = get_reaction_from_message(payload.emoji, message)
    return ReactionEvent(sender, message.author, message.channel, payload.emoji, reaction)
