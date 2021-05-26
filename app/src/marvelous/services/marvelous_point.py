from typing import List
from marvelous import db, models


def reset() -> None:
    """えらいポイントをリセットする"""
    try:
        db.users.reset_marvelous_point()
    except Exception as err:
        raise models.DataUpdateError from err


def get_ranking() -> List[models.User]:
    """ユーザーランキングを取得する"""
    try:
        users: List[models.User] = db.users.get_all_sorted_by_marvelous_point()
    except Exception as err:
        raise models.DataFetchError from err
    return users
