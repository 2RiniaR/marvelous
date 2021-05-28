from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import datetime
from marvelous import services, models
from marvelous.helpers.time import Timing
from typing import Optional


@dataclass
class SleepContext:
    user_id: int
    time: datetime.datetime
    refresh_time: datetime.timedelta
    accept_start_time: datetime.timedelta
    accept_end_time: datetime.timedelta


class SleepStatus(Enum):
    Rejected = auto()
    Accepted = auto()


@dataclass
class SleepResult:
    status: SleepStatus


class Sleep:
    context: SleepContext
    user: Optional[models.User] = None
    result: Optional[SleepResult] = None

    def __init__(self, context: SleepContext):
        self.context = context

    def __get_base_datetime(self) -> datetime.datetime:
        time = self.context.time
        refresh = self.context.refresh_time
        today_refresh = datetime.timedelta(seconds=refresh.seconds)
        diff = time - today_refresh
        zero_time = datetime.datetime(year=diff.year, month=diff.month, day=diff.day, hour=0, minute=0, second=0,
                                      microsecond=0)
        return zero_time

    def apply(self):
        # モデルに渡される時間を表す引数は、全て「ある日の00:00」からの相対時刻を用いている。
        # そのため、どの日を基準にしているのかを引数から逆算する必要がある。
        base_datetime = self.__get_base_datetime()

        # 起床イベントの発行された時間が受付時間内であるかどうかのチェックを行う
        timing = Timing.from_time(self.context.time, base_datetime+self.context.accept_start_time,
                                  base_datetime+self.context.accept_end_time)
        if timing != Timing.InTerm:
            self.result = SleepResult(status=SleepStatus.Rejected)
            return

        self.user: models.User = services.user.get_by_id(self.context.user_id)
        if self.user is None:
            raise models.UserNotFoundError(self.context.user_id)

        self.user.slept_at = self.context.time
        services.user.update(self.user)
        self.result = SleepResult(status=SleepStatus.Accepted)


@dataclass
class WakeUpContext:
    user_id: int
    time: datetime.datetime
    point_on_accepted: int
    accept_sleep_start_time: datetime.timedelta
    accept_sleep_end_time: datetime.timedelta
    accept_wake_up_start_time: datetime.timedelta
    accept_wake_up_end_time: datetime.timedelta


class WakeUpStatus(Enum):
    NotSleeping = auto()
    Ignored = auto()
    BeforeTerm = auto()
    Accepted = auto()
    AfterTerm = auto()


@dataclass
class WakeUpResult:
    status: WakeUpStatus
    point_diff: int


class WakeUp:
    context: WakeUpContext
    user: Optional[models.User] = None
    result: Optional[WakeUpResult] = None

    def __init__(self, context: WakeUpContext):
        self.context = context

    def give_bonus(self):
        self.user.point += self.context.point_on_accepted

    def __get_base_datetime(self) -> datetime.datetime:
        time = self.user.slept_at
        diff = time - self.context.accept_sleep_start_time
        zero_time = datetime.datetime(year=diff.year, month=diff.month, day=diff.day, hour=0, minute=0, second=0,
                                      microsecond=0)
        return zero_time

    def apply(self):
        self.user: models.User = services.user.get_by_id(self.context.user_id)
        if self.user is None:
            raise models.UserNotFoundError(self.context.user_id)

        if self.user.slept_at is None:
            self.result = WakeUpResult(status=WakeUpStatus.NotSleeping, point_diff=0)
            return

        # モデルに渡される時間を表す引数は、全て「ある日の00:00」からの相対時刻を用いている。
        # そのため、どの日を基準にしているのかを引数から逆算する必要がある。
        base_datetime = self.__get_base_datetime()

        # 睡眠イベントの適用と同時に起床イベントが適用されないように、睡眠イベントの受付時間中は Ignored を返すようにする
        refresh_timing = Timing.from_time(self.context.time, base_datetime + self.context.accept_sleep_start_time,
                                          base_datetime + self.context.accept_sleep_end_time)
        if refresh_timing == Timing.InTerm:
            self.result = WakeUpResult(status=WakeUpStatus.Ignored, point_diff=0)
            return

        # 起床イベントの発行された時間が適切であるかどうかのチェックを行う
        wake_up_timing = Timing.from_time(self.context.time, base_datetime + self.context.accept_wake_up_start_time,
                                          base_datetime + self.context.accept_wake_up_end_time)
        if wake_up_timing == Timing.TooEarly:
            self.result = WakeUpResult(status=WakeUpStatus.BeforeTerm, point_diff=0)
        elif wake_up_timing == Timing.TooLate:
            self.result = WakeUpResult(status=WakeUpStatus.AfterTerm, point_diff=0)
        else:
            self.result = WakeUpResult(status=WakeUpStatus.Accepted, point_diff=self.context.point_on_accepted)
            self.give_bonus()

        self.user.slept_at = None
        services.user.update(self.user)
