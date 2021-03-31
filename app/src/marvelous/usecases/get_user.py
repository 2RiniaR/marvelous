import marvelous.data_store as data_store
from marvelous.models.user import User


class UserNotFoundError(Exception):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"ユーザーID: {self.user_id} が見つかりませんでした。"


def is_user_exist(discord_id: int) -> bool:
    return data_store.users.get_by_id(discord_id) is not None


def get_user(discord_id: int) -> User:
    """ユーザー情報を取得する"""
    user: User = data_store.users.get_by_id(discord_id)
    if user is None:
        raise UserNotFoundError(discord_id)
    return user
