from dataclasses import dataclass
import datetime
from .bonus_interval import BonusIntervalSettings


@dataclass()
class BooingSettings:
    receive_point: int
    send_penalty: BonusIntervalSettings
    reaction: str
    random_message_count: int


values = BooingSettings(
    receive_point=-1,
    send_penalty=BonusIntervalSettings(
        step_interval=5,
        daily_step_limit=10,
        point=-1,
        reset_time=datetime.time(4, 0)
    ),
    reaction="💩",
    random_message_count=3
)
