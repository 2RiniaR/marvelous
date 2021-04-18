from __future__ import annotations
from dataclasses import dataclass
from ..parts import DailyBonus


@dataclass()
class User:
    discord_id: int = None
    display_name: str = None
    marvelous_bonus: DailyBonus = None
    booing_penalty: DailyBonus = None
    super_marvelous_left: int = None
    survival_bonus_given: bool = None
    point: int = None
