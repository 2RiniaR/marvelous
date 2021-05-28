from __future__ import annotations
import datetime
from enum import Enum, auto


class Timing(Enum):
    TooEarly = auto()
    InTerm = auto()
    TooLate = auto()

    @staticmethod
    def from_time(time: datetime.datetime, start: datetime.datetime, end: datetime.datetime) -> Timing:
        if time < start:
            return Timing.TooEarly
        elif time < end:
            return Timing.InTerm
        else:
            return Timing.TooLate
