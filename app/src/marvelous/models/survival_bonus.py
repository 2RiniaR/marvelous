import marvelous.data_store as data_store
from .user import get_user, User
from .errors import DataFetchError, DataUpdateError, CalculateError, UserNotFoundError


def apply(user: User, give_point: int):
    user.survival_bonus_given = True
    user.point += give_point


def give_survival_bonus(discord_id: int, give_point: int) -> bool:
    """「生きててえらいボーナス」を付与する"""
    try:
        user = get_user(discord_id)
    except Exception as err:
        raise DataFetchError from err

    if user is None:
        raise UserNotFoundError(discord_id)

    if user.survival_bonus_given:
        return False

    try:
        apply(user, give_point)
    except Exception as err:
        raise CalculateError from err

    try:
        data_store.users.update(user)
    except Exception as err:
        raise DataUpdateError from err

    return True


def reset_survival_bonus() -> None:
    """「生きててえらいボーナス」をリセットする"""
    try:
        data_store.users.reset_survival_bonus()
    except Exception as err:
        raise DataUpdateError from err
