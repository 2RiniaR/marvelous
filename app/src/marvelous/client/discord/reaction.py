import discord
from . import client
from marvelous.helpers import first_match
from dataclasses import dataclass
from typing import Iterable, Optional, Dict
from ..presentation.reaction import ReactionEvent, add_reaction, remove_reaction
from marvelous.settings import app_settings
from logging import getLogger


logger = getLogger(__name__)


@dataclass()
class ReactionContext:
    guild_id: int
    user_id: int
    channel_id: int
    message_id: int
    emoji_str: str


@dataclass()
class ReactionState:
    context: ReactionContext
    initial_state: bool
    current_state: bool


class ReactionStateCache:
    states: Dict[int, ReactionState]
    max_cache_count: int = 32768

    def __init__(self):
        self.states = {}

    @staticmethod
    def to_event_hash(ctx: ReactionContext) -> int:
        # return hash((
        #     ctx.guild_id, ctx.user_id, ctx.channel_id, ctx.message_id, ctx.hashed_emoji
        # ))
        return (ctx.guild_id << (64 * 0)) \
               | (ctx.user_id << (64 * 1)) \
               | (ctx.channel_id << (64 * 2)) \
               | (ctx.message_id << (64 * 3)) \
               | (hash(ctx.emoji_str) << (64 * 4))

    def is_state_registered(self, ctx: ReactionContext) -> bool:
        event_hash = self.to_event_hash(ctx)
        return event_hash in self.states.keys()

    def register_state(self, ctx: ReactionContext, initial_state: bool) -> None:
        event_hash = self.to_event_hash(ctx)
        if len(self.states) > self.max_cache_count or event_hash in self.states.keys():
            return
        self.states[event_hash] = ReactionState(
            context=ReactionContext(
                guild_id=ctx.guild_id,
                user_id=ctx.user_id,
                message_id=ctx.message_id,
                channel_id=ctx.channel_id,
                emoji_str=ctx.emoji_str,
            ),
            initial_state=initial_state,
            current_state=initial_state
        )

    def set_state(self, ctx: ReactionContext, state: bool) -> None:
        event_hash = self.to_event_hash(ctx)
        if event_hash not in self.states.keys():
            raise AttributeError
        self.states[event_hash].current_state = state

    def get_all_states(self) -> Iterable[ReactionState]:
        return self.states.copy().values()

    def reset(self) -> None:
        self.states.clear()


reaction_cache = ReactionStateCache()


def get_reaction_from_message(emoji: discord.PartialEmoji, message: discord.Message) -> Optional[discord.Reaction]:
    # リアクションが取り消された結果、そのメッセージへのリアクションが消えた（個数が0になった）場合はNoneになる
    return first_match(message.reactions, pred=lambda r: str(r.emoji) == str(emoji), default=None)


async def fetch_reaction_event(ctx: ReactionContext) -> Optional[ReactionEvent]:
    guild: discord.Guild = client.bot.get_guild(ctx.guild_id)
    sender: discord.Member = guild.get_member(ctx.user_id)
    channel: discord.TextChannel = guild.get_channel(ctx.channel_id)
    if sender is None or channel is None:
        return None

    try:
        message: discord.Message = await channel.fetch_message(ctx.message_id)
    except discord.DiscordException as err:
        logger.warning(str(err))
        return None

    receiver: discord.Member = message.author
    if not isinstance(receiver, discord.Member):
        return None

    reaction = first_match(message.reactions, pred=lambda r: str(r.emoji) == ctx.emoji_str, default=None)
    if reaction is None:
        return None

    return ReactionEvent(
        sender=sender,
        channel=channel,
        receiver=receiver,
        reaction=reaction
    )


async def reflect_state(state: ReactionState):
    if state.initial_state == state.current_state:
        return

    event = await fetch_reaction_event(state.context)
    if event is None:
        return

    if state.current_state:
        await add_reaction(event)
    else:
        await remove_reaction(event)


async def reflect_caches():
    states = reaction_cache.get_all_states()
    reaction_cache.reset()
    for state in states:
        await reflect_state(state)


def is_cache_target(emoji: discord.PartialEmoji) -> bool:
    str_emoji = str(emoji)
    return str_emoji in [
        app_settings.marvelous.reaction,
        app_settings.super_marvelous.reaction,
        app_settings.booing.reaction
    ]


def set_reaction_state(payload: discord.RawReactionActionEvent, is_added: bool):
    if not is_cache_target(payload.emoji):
        return

    reaction_context = ReactionContext(
        guild_id=payload.guild_id,
        user_id=payload.user_id,
        channel_id=payload.channel_id,
        message_id=payload.message_id,
        emoji_str=str(payload.emoji)
    )

    if not reaction_cache.is_state_registered(reaction_context):
        reaction_cache.register_state(reaction_context, not is_added)
    reaction_cache.set_state(reaction_context, is_added)
