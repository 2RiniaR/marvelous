from __future__ import annotations
from dataclasses import dataclass
from .daily_bonus import DailyBonus
import marvelous.data_store as data_store
from marvelous.models.errors import UserNotFoundError, AlreadyExistError
from logging import getLogger
from typing import Iterable


logger = getLogger(__name__)


@dataclass()
class User:
    discord_id: int = None
    display_name: str = None
    marvelous_bonus: DailyBonus = None
    booing_penalty: DailyBonus = None
    super_marvelous_left: int = None
    survival_bonus_given: bool = None
    point: int = None


def is_user_exist(discord_id: int) -> bool:
    user: User = data_store.users.get_user_by_id(discord_id)
    return user is not None


def get_user(discord_id: int) -> User:
    """ユーザー情報を取得する"""
    user: User = data_store.users.get_user_by_id(discord_id)
    if user is None:
        raise UserNotFoundError(discord_id)
    return user


def register_user(user: User):
    """ユーザーを新規登録する"""
    if is_user_exist(user.discord_id):
        raise AlreadyExistError(user.discord_id)
    data_store.users.create_user(user)


def update_name(discord_id: int, name: str) -> None:
    """ユーザー名を更新する"""
    user: User = get_user(discord_id)
    user.display_name = name
    data_store.users.update_user(user)


def get_ranking() -> Iterable[User]:
    """ユーザーランキングを取得する"""
    users: Iterable[User] = data_store.users.get_users_marvelous_point_ranking()
    return users
