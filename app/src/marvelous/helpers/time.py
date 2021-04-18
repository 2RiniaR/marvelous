import datetime


def is_now_time(time: datetime.time):
    time_format: str = "%H:%M"
    return datetime.datetime.now().time().strftime(time_format) == time.strftime(time_format)


def is_now_weekday(num: int):
    return datetime.datetime.now().weekday() == num
