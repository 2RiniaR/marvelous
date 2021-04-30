from typing import Optional
from typing import Iterable
from .convert import to_user
from marvelous.models.user import User
from .execute import fetch_one, fetch_all


def get_user_by_id(discord_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE discord_id=%(discord_id)s"
    params = {"discord_id": str(discord_id)}
    data = fetch_one(query, params)
    if data is None:
        return None
    user = to_user(data)
    return user


def get_users_marvelous_point_ranking() -> Iterable[User]:
    query = "SELECT * FROM users ORDER BY marvelous_point DESC;"
    data = fetch_all(query)
    if data is None:
        return []
    users: Iterable[User] = [to_user(row) for row in data]
    return users
