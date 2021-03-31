import marvelous.data_store as data_store
from marvelous.models.user import User
from marvelous.usecases.get_user import get_user


def apply(user: User, give_point: int):
    user.survival_bonus_given = True
    user.point += give_point


def give_survival_bonus(discord_id: int, give_point: int) -> bool:
    """「生きててえらいボーナス」を付与する"""
    user = get_user(discord_id)
    if user.survival_bonus_given:
        return False
    apply(user, give_point)
    data_store.users.update(user)
    return True
