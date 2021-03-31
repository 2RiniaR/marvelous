import marvelous.data_store as data_store
from marvelous.usecases.get_user import get_user
from marvelous.models.user import User


def update_name(discord_id: int, name: str) -> None:
    """ユーザー名を更新する"""
    user: User = get_user(discord_id)
    user.display_name = name
    data_store.users.update(user)
