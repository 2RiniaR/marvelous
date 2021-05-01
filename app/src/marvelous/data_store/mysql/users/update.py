from marvelous.models.user import User
from .convert import to_parameter
from .execute import commit


def update_user(user: User) -> None:
    query = (
        "UPDATE users SET "
        "display_name=%(display_name)s,"
        "marvelous_point=%(marvelous_point)s,"
        "super_marvelous_left=%(super_marvelous_left)s,"
        "marvelous_bonus_step=%(marvelous_bonus_step)s,"
        "marvelous_bonus_today_step=%(marvelous_bonus_today_step)s,"
        "booing_penalty_step=%(booing_penalty_step)s,"
        "booing_penalty_today_step=%(booing_penalty_today_step)s,"
        "survival_bonus_given=%(survival_bonus_given)s "
        "WHERE discord_id = %(discord_id)s"
    )
    params = to_parameter(user)
    commit(query, params)


def reset_survival_bonus() -> None:
    query = "UPDATE users SET survival_bonus_given = 0"
    commit(query)


def reset_super_marvelous_left(value: int) -> None:
    query = "UPDATE users SET super_marvelous_left = %(count)s"
    params = {"count": str(value)}
    commit(query, params)


def reset_daily_steps() -> None:
    query = "UPDATE users SET marvelous_bonus_today_step = 0, booing_penalty_today_step = 0"
    commit(query)


def reset_marvelous_point() -> None:
    query = "UPDATE users SET marvelous_point = 0"
    commit(query)
