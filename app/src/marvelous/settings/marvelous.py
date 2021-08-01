from dataclasses import dataclass
import datetime
from .bonus_interval import BonusIntervalSettings


@dataclass()
class MarvelousSettings:
    receive_point: int
    send_bonus: BonusIntervalSettings
    reaction: str
    random_message_count: int


values = MarvelousSettings(
    receive_point=2,
    send_bonus=BonusIntervalSettings(
        step_interval=3,
        daily_step_limit=10,
        point=5,
        reset_time=datetime.time(4, 0)
    ),
    reaction="👏",
    random_message_count=3
)
