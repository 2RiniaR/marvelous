from dataclasses import dataclass
import datetime


@dataclass()
class BonusIntervalSettings:
    step_interval: int
    daily_step_limit: int
    point: int
    reset_time: datetime.time
