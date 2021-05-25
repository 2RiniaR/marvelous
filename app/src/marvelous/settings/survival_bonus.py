from dataclasses import dataclass
import datetime


@dataclass()
class SurvivalBonusSettings:
    point: int
    reset_time: datetime.time


values = SurvivalBonusSettings(
    point=1,
    reset_time=datetime.time(4, 0)
)
