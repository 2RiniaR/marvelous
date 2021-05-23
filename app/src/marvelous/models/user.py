from __future__ import annotations
from dataclasses import dataclass
from .daily_bonus import DailyBonus
import marvelous.data_store as data_store
from marvelous.models.errors import UserNotFoundError, AlreadyExistError, DataFetchError, DataUpdateError
from typing import Iterable, Optional


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
    return get_user(discord_id) is not None


def get_user(discord_id: int) -> Optional[User]:
    """ユーザー情報を取得する"""
    try:
        user: User = data_store.users.get_by_id(discord_id)
    except Exception as err:
        raise DataFetchError from err
    return user


def register_user(user: User):
    """ユーザーを新規登録する"""
    if is_user_exist(user.discord_id):
        raise AlreadyExistError(user.discord_id)
    try:
        data_store.users.create(user)
    except Exception as err:
        raise DataUpdateError from err


def update_name(discord_id: int, name: str) -> None:
    """ユーザー名を更新する"""
    user: User = get_user(discord_id)
    if user is None:
        raise UserNotFoundError(discord_id)
    user.display_name = name
    try:
        data_store.users.update(user)
    except Exception as err:
        raise DataUpdateError from err


def get_ranking() -> Iterable[User]:
    """ユーザーランキングを取得する"""
    try:
        users: List[User] = data_store.users.get_all_sorted_by_marvelous_point()
    except Exception as err:
        raise DataFetchError from err
    return users


def reset_marvelous_point() -> None:
    """えらいポイントをリセットする"""
    try:
        data_store.users.reset_marvelous_point()
    except Exception as err:
        raise DataUpdateError from err
