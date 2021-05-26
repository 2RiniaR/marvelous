import dataclasses
import logging
from typing import Iterable, Dict


logger = logging.getLogger(__name__)


@dataclasses.dataclass()
class ReactionContext:
    guild_id: int
    user_id: int
    channel_id: int
    message_id: int
    emoji_str: str


@dataclasses.dataclass()
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


memory = ReactionStateCache()
