from typing import List, Optional
from marvelous import models, db


def is_exist(discord_id: int) -> bool:
    return get_by_id(discord_id) is not None


def get_by_id(discord_id: int) -> Optional[models.User]:
    """ユーザー情報を取得する"""
    try:
        user: models.User = db.users.get_by_id(discord_id)
    except Exception as err:
        raise models.DataFetchError from err
    return user


def get_all() -> List[models.User]:
    try:
        users: List[models.User] = db.users.get_all()
    except Exception as err:
        raise models.DataFetchError from err
    return users


def update(user: models.User) -> None:
    try:
        db.users.update(user)
    except Exception as err:
        raise models.DataUpdateError from err


def register(user: models.User):
    """ユーザーを新規登録する"""
    if is_exist(user.discord_id):
        raise models.AlreadyExistError(user.discord_id)
    try:
        db.users.create(user)
    except Exception as err:
        raise models.DataUpdateError from err


def update_name(discord_id: int, name: str) -> None:
    """ユーザー名を更新する"""
    user: models.User = get_by_id(discord_id)
    if user is None:
        raise models.UserNotFoundError(discord_id)
    user.display_name = name
    update(user)
