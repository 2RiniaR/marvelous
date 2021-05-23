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
    random_message_count: int


@dataclass()
class BooingSettings:
    receive_point: int
    send_penalty: BonusSettings
    reaction: str
    random_message_count: int


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
    ranking_limit: int


@dataclass()
class UserSettings:
    update_name_time: datetime.time
    reset_marvelous_point_time: datetime.time
    reset_marvelous_point_weekday: int


@dataclass()
class GitHubSettings:
    bonus_time: datetime.time
    bonus_point: int


@dataclass()
class AppSettings:
    marvelous: MarvelousSettings
    super_marvelous: SuperMarvelousSettings
    booing: BooingSettings
    survival: SurvivalSettings
    message: MessageSettings
    user: UserSettings
    github: GitHubSettings


app_settings = AppSettings(
    marvelous=MarvelousSettings(
        receive_point=1,
        send_bonus=BonusSettings(
            step_interval=5,
            daily_step_limit=10,
            point=1,
            reset_time=datetime.time(4, 0)
        ),
        reaction="👏",
        random_message_count=3
    ),
    booing=BooingSettings(
        receive_point=-1,
        send_penalty=BonusSettings(
            step_interval=5,
            daily_step_limit=10,
            point=-1,
            reset_time=datetime.time(4, 0)
        ),
        reaction="💩",
        random_message_count=3
    ),
    super_marvelous=SuperMarvelousSettings(
        receive_point=3,
        send_point=1,
        reaction="🙌",
        initial_left_count=3,
        reset_time=datetime.time(4, 0),
        reset_weekday=0
    ),
    survival=SurvivalSettings(
        point=1,
        reset_time=datetime.time(4, 0)
    ),
    message=MessageSettings(
        strict_time=1.0,
        ranking_limit=8
    ),
    user=UserSettings(
        update_name_time=datetime.time(4, 0),
        reset_marvelous_point_time=datetime.time(4, 0),
        reset_marvelous_point_weekday=0
    ),
    github=GitHubSettings(
        bonus_time=datetime.time(0, 1),
        bonus_point=3
    )
)
