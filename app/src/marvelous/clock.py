import datetime
from marvelous import settings
from typing import Optional


__manual_now: Optional[datetime.datetime] = None


def is_now_time(time: datetime.time):
    time_format: str = "%H:%M"
    return datetime.datetime.now().time().strftime(time_format) == time.strftime(time_format)


def is_now_weekday(num: int):
    if num < 0 or 6 < num:
        raise ValueError(f"num({num}) must be an integer in range 0 to 6.")
    return datetime.datetime.now().weekday() == num


def get_now() -> datetime.datetime:
    if settings.environment.is_development and __manual_now is not None:
        return __manual_now
    return datetime.datetime.now()


def set_now_manually(time: datetime.datetime):
    global __manual_now
    if not settings.environment.is_development:
        return
    __manual_now = time


def reset_now_manually():
    global __manual_now
    if not settings.environment.is_development:
        return
    __manual_now = None
