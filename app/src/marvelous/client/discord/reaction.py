from dataclasses import dataclass
import discord
from . import client
from marvelous.helpers import first_match
from typing import Optional, Dict


@dataclass()
class ReactionEvent:
    sender: discord.Member
    receiver: discord.Member
    channel: discord.TextChannel
    emoji: discord.PartialEmoji
    reaction: Optional[discord.Reaction]


class ReactionStateCache:
    states: Dict[int, bool]
    max_cache_count: int = 32768

    @staticmethod
    def to_event_hash(user_id: int, message_id: int, reaction_type: int) -> int:
        return user_id | (message_id << 32) | (reaction_type << 64)

    def set_state(self, user_id: int, message_id: int, reaction_type: int, is_added: bool) -> None:
        event_hash = self.to_event_hash(user_id, message_id, reaction_type)
        if len(self.states) > self.max_cache_count:
            return
        self.states[event_hash] = is_added

    def get_state(self, user_id: int, message_id: int, reaction_type: int) -> Optional[bool]:
        event_hash = self.to_event_hash(user_id, message_id, reaction_type)
        return self.states.get(event_hash)

    def reset(self):
        self.states.clear()


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
