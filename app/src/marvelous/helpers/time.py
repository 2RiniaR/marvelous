import datetime


def is_now_time(time: datetime.time):
    time_format: str = "%H:%M"
    return datetime.datetime.now().time().strftime(time_format) == time.strftime(time_format)


def is_now_weekday(num: int):
    if num < 0 or 6 < num:
        raise ValueError(f"num({num}) must be an integer in range 0 to 6.")
    return datetime.datetime.now().weekday() == num
