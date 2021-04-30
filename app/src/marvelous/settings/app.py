from dataclasses import dataclass
import datetime


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
    reaction: str


@dataclass()
class BooingSettings:
    receive_point: int
    send_penalty: BonusSettings
    reaction: str


@dataclass()
class SuperMarvelousSettings:
    receive_point: int
    send_point: int
    initial_left_count: int
    reaction: str
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

    def __init__(self):
        self.marvelous = MarvelousSettings(
            receive_point=1,
            send_bonus=BonusSettings(
                step_interval=5,
                daily_step_limit=10,
                point=1,
                reset_time=datetime.time(4, 0)
            ),
            reaction="👏"
        )

        self.booing = BooingSettings(
            receive_point=-1,
            send_penalty=BonusSettings(
                step_interval=5,
                daily_step_limit=10,
                point=-1,
                reset_time=datetime.time(4, 0)
            ),
            reaction="🖕"
        )

        self.super_marvelous = SuperMarvelousSettings(
            receive_point=10,
            send_point=1,
            reaction="🙌",
            initial_left_count=3,
            reset_time=datetime.time(4, 0),
            reset_weekday=0
        )

        self.survival = SurvivalSettings(
            point=1,
            reset_time=datetime.time(4, 0)
        )

        self.message = MessageSettings(
            strict_time=1.0
        )


app_settings = AppSettings()
