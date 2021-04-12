import marvelous.data_store as data_store
from typing import Iterable
from marvelous.models.user import User


def get_ranking() -> Iterable[User]:
    """ユーザーランキングを取得する"""
    users: Iterable[User] = data_store.users.get_marvelous_point_ranking()
    return users
