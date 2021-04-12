import marvelous.data_store as data_store
from marvelous.usecases.get_user import is_user_exist
from marvelous.models.user import User


class AlreadyExistError(Exception):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"ユーザーID: {self.user_id} はすでに登録されています。"


def register_user(user: User):
    """ユーザーを新規登録する"""
    if is_user_exist(user.discord_id):
        raise AlreadyExistError(user.discord_id)
    data_store.users.create(user)
