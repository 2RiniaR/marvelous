from dataclasses import dataclass
import datetime


@dataclass()
class UserSettings:
    update_name_time: datetime.time
    reset_marvelous_point_time: datetime.time
    reset_marvelous_point_weekday: int


values = UserSettings(
    update_name_time=datetime.time(4, 0),
    reset_marvelous_point_time=datetime.time(4, 0),
    reset_marvelous_point_weekday=0
)
