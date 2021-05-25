import datetime
from dataclasses import dataclass


@dataclass()
class ContributionBonusSettings:
    given_time: datetime.time
    point: int


values = ContributionBonusSettings(
    given_time=datetime.time(0, 1),
    point=3
)
