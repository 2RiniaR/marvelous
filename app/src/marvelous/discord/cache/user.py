from typing import Dict, Optional
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


@dataclass
class UserContext:
    registered: bool
    survival_bonus_given: bool = False
    sleeping: bool = False


@dataclass
class UserCacheState:
    context: UserContext


class UserCache:
    states: Dict[int, UserCacheState]
    max_cache_count: int = 32768

    def __init__(self):
        self.states = {}

    def is_state_registered(self, user_id: int) -> bool:
        return user_id in self.states.keys()

    def set_state(self, user_id: int, context: UserContext) -> None:
        if user_id not in self.states.keys() and len(self.states) > self.max_cache_count:
            return
        self.states[user_id] = UserCacheState(context=context)
        logger.debug(f"User cache (id = {user_id}) set.")

    def get_state(self, user_id: int) -> Optional[UserContext]:
        if not self.is_state_registered(user_id):
            return None
        return self.states[user_id].context

    def clear(self):
        self.states.clear()
        logger.debug("Cache cleared.")


memory = UserCache()
