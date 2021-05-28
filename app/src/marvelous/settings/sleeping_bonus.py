import datetime
from dataclasses import dataclass
from typing import List


@dataclass()
class SleepingBonusSettings:
    point: int
    sleep_words: List[str]
    accept_sleep_start_time: datetime.timedelta
    accept_sleep_end_time: datetime.timedelta
    accept_wake_up_start_time: datetime.timedelta
    accept_wake_up_end_time: datetime.timedelta
    sleep_reaction: str


values = SleepingBonusSettings(
    accept_sleep_start_time=datetime.timedelta(days=0, hours=18, minutes=0),
    accept_sleep_end_time=datetime.timedelta(days=1, hours=1, minutes=0),
    accept_wake_up_start_time=datetime.timedelta(days=1, hours=5, minutes=0),
    accept_wake_up_end_time=datetime.timedelta(days=1, hours=12, minutes=0),
    point=5,
    sleep_words=["おやすみ"],
    sleep_reaction="😴"
)
