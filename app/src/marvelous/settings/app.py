from dataclasses import dataclass
import datetime
from typing import Optional


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
    default_channel_id: Optional[int]


@dataclass()
class UserSettings:
    update_name_time: datetime.time
    reset_marvelous_point_time: datetime.time
    reset_marvelous_point_weekday: int


@dataclass()
class AppSettings:
    marvelous: MarvelousSettings
    super_marvelous: SuperMarvelousSettings
    booing: BooingSettings
    survival: SurvivalSettings
    message: MessageSettings
    user: UserSettings


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
        # ファイルサーバー上のファイルに設定を保存できるようにする
        #     -> 理想だが、デプロイ先がHerokuの場合はAmazon S3などの外部サービスを利用する必要がある
        # メモリ上に設定を保持する
        #     -> Herokuの稼働サーバーは1日1回再起動されるため、メモリ上には設定を保持できない
        # 特定のサーバーでのみの運用となるので、コストを考慮してあえてハードコーディングをしています
        # default_channel_id=690909527461199922
        default_channel_id=829402921010987049
    ),
    user=UserSettings(
        update_name_time=datetime.time(4, 0),
        reset_marvelous_point_time=datetime.time(4, 0),
        reset_marvelous_point_weekday=0
    )
)
