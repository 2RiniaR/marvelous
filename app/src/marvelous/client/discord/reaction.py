import discord
from . import client
from marvelous.helpers import first_match
from dataclasses import dataclass
from typing import Iterable, Optional, Dict
from ..presentation.reaction import ReactionType, ReactionEvent, add_reaction, remove_reaction
from marvelous.settings import app_settings
from logging import getLogger


logger = getLogger(__name__)


@dataclass()
class ReactionContext:
    user_id: int
    channel_id: int
    message_id: int
    reaction_type: ReactionType


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
        return (ctx.user_id << (64 * 0)) \
               | (ctx.channel_id << (64 * 1)) \
               | (ctx.message_id << (64 * 2)) \
               | (ctx.reaction_type << (64 * 3))

    def is_state_registered(self, ctx: ReactionContext) -> bool:
        event_hash = self.to_event_hash(ctx)
        return event_hash in self.states.keys()

    def register_state(self, ctx: ReactionContext, initial_state: bool) -> None:
        event_hash = self.to_event_hash(ctx)
        if len(self.states) > self.max_cache_count or event_hash in self.states.keys():
            return
        self.states[event_hash] = ReactionState(
            context=ReactionContext(
                user_id=ctx.user_id,
                message_id=ctx.message_id,
                channel_id=ctx.channel_id,
                reaction_type=ctx.reaction_type,
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


def get_reaction_type(emoji: discord.PartialEmoji) -> Optional[ReactionType]:
    str_emoji = str(emoji)
    if str_emoji == app_settings.marvelous.reaction:
        return ReactionType.Marvelous
    elif str_emoji == app_settings.super_marvelous.reaction:
        return ReactionType.SuperMarvelous
    elif str_emoji == app_settings.booing.reaction:
        return ReactionType.Booing
    return None


def get_reaction_from_message(emoji: discord.PartialEmoji, message: discord.Message) -> Optional[discord.Reaction]:
    # リアクションが取り消された結果、そのメッセージへのリアクションが消えた（個数が0になった）場合はNoneになる
    return first_match(message.reactions, pred=lambda r: str(r.emoji) == str(emoji), default=None)


async def fetch_reaction_event(ctx: ReactionContext) -> Optional[ReactionEvent]:
    sender: discord.User = client.bot.get_user(ctx.user_id)
    channel: discord.TextChannel = client.bot.get_channel(ctx.channel_id)
    if sender is None or channel is None:
        return None

    try:
        message: discord.Message = await channel.fetch_message(ctx.message_id)
    except discord.DiscordException as err:
        logger.warning(str(err))
        return None

    return ReactionEvent(
        sender=sender,
        channel=channel,
        receiver=message.author,
        reaction_type=ctx.reaction_type
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


def set_reaction_state(payload: discord.RawReactionActionEvent, is_added: bool):
    reaction_type = get_reaction_type(payload.emoji)
    if reaction_type is None:
        return

    reaction_context = ReactionContext(
        user_id=payload.user_id,
        channel_id=payload.channel_id,
        message_id=payload.message_id,
        reaction_type=reaction_type
    )

    if not reaction_cache.is_state_registered(reaction_context):
        reaction_cache.register_state(reaction_context, not is_added)
    reaction_cache.set_state(reaction_context, is_added)
