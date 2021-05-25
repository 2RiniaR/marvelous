import marvelous.domain.models as models
import marvelous.db as db
from .user import get_by_id as get_user_by_id


def apply(user: models.User, give_point: int):
    user.survival_bonus_given = True
    user.point += give_point


def give(discord_id: int, give_point: int) -> bool:
    """「生きててえらいボーナス」を付与する"""
    try:
        user = get_user_by_id(discord_id)
    except Exception as err:
        raise models.DataFetchError from err

    if user is None:
        raise models.UserNotFoundError(discord_id)

    if user.survival_bonus_given:
        return False

    try:
        apply(user, give_point)
    except Exception as err:
        raise models.CalculateError from err

    try:
        db.users.update(user)
    except Exception as err:
        raise models.DataUpdateError from err

    return True


def reset() -> None:
    """「生きててえらいボーナス」をリセットする"""
    try:
        db.users.reset_survival_bonus()
    except Exception as err:
        raise models.DataUpdateError from err
