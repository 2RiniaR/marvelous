from dataclasses import dataclass
import datetime


@dataclass()
class SuperMarvelousSettings:
    receive_point: int
    send_point: int
    initial_left_count: int
    reaction: str
    reset_time: datetime.time
    reset_weekday: int


values = SuperMarvelousSettings(
    receive_point=3,
    send_point=1,
    reaction="🙌",
    initial_left_count=3,
    reset_time=datetime.time(4, 0),
    reset_weekday=0
)
