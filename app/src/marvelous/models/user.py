from dataclasses import dataclass
from typing import Optional
from .daily_bonus import DailyBonus


@dataclass()
class User:
    discord_id: int = None
    display_name: str = None
    marvelous_bonus: DailyBonus = None
    booing_penalty: DailyBonus = None
    super_marvelous_left: int = None
    survival_bonus_given: bool = None
    point: int = None
    github_id: Optional[str] = None
    sleeping: bool = None
