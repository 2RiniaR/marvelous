from typing import Iterable
from dataclasses import dataclass
import datetime
import json


@dataclass()
class BonusSettings:
    step_interval: int
    daily_step_limit: int
    point: int
    reset_time: datetime.time


@dataclass()
class MarvelousSettings:
    receive_point: int
    send_bonus: BonusSettings
    reactions: Iterable[str]


@dataclass()
class BooingSettings:
    receive_point: int
    send_penalty: BonusSettings
    reactions: Iterable[str]


@dataclass()
class SuperMarvelousSettings:
    receive_point: int
    send_point: int
    initial_left_count: int
    reactions: Iterable[str]
    reset_time: datetime.time
    reset_weekday: int


@dataclass()
class SurvivalSettings:
    point: int
    reset_time: datetime.time


@dataclass()
class MessageSettings:
    strict_time: float


class AppSettings:
    marvelous: MarvelousSettings
    super_marvelous: SuperMarvelousSettings
    booing: BooingSettings
    survival: SurvivalSettings
    message: MessageSettings

    def load_from_file(self, path: str) -> None:
        with open(path, "r") as f:
            settings = json.load(f)

        self.marvelous = MarvelousSettings(
            receive_point=int(settings["marvelous"]["receive_point"]),
            send_bonus=BonusSettings(
                step_interval=int(settings["marvelous"]["send_bonus"]["step_interval"]),
                daily_step_limit=int(settings["marvelous"]["send_bonus"]["daily_step_limit"]),
                point=int(settings["marvelous"]["send_bonus"]["point"]),
                reset_time=datetime.datetime.strptime(settings["marvelous"]["send_bonus"]["reset_time"], "%H:%M").time()
            ),
            reactions=settings["marvelous"]["reactions"]
        )

        self.booing = BooingSettings(
            receive_point=int(settings["booing"]["receive_point"]),
            send_penalty=BonusSettings(
                step_interval=int(settings["booing"]["send_penalty"]["step_interval"]),
                daily_step_limit=int(settings["booing"]["send_penalty"]["daily_step_limit"]),
                point=int(settings["booing"]["send_penalty"]["point"]),
                reset_time=datetime.datetime.strptime(settings["booing"]["send_penalty"]["reset_time"], "%H:%M").time()
            ),
            reactions=settings["booing"]["reactions"]
        )

        self.super_marvelous = SuperMarvelousSettings(
            receive_point=int(settings["super_marvelous"]["receive_point"]),
            send_point=int(settings["super_marvelous"]["send_point"]),
            reactions=settings["super_marvelous"]["reactions"],
            initial_left_count=int(settings["super_marvelous"]["initial_left_count"]),
            reset_time=datetime.datetime.strptime(settings["super_marvelous"]["reset_time"], "%H:%M").time(),
            reset_weekday=int(settings["super_marvelous"]["reset_weekday"])
        )

        self.survival = SurvivalSettings(
            point=int(settings["survival"]["point"]),
            reset_time=datetime.datetime.strptime(settings["survival"]["reset_time"], "%H:%M").time()
        )

        self.message = MessageSettings(
            strict_time=float(settings["message"]["strict_time"])
        )


app_settings = AppSettings()
