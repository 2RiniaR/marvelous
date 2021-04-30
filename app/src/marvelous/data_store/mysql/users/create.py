from marvelous.models.user import User
from .execute import commit
from .convert import to_parameter


def create_user(user: User) -> None:
    query = (
        'INSERT INTO users('
        'discord_id, display_name, marvelous_point, super_marvelous_left, marvelous_bonus_step,'
        'marvelous_bonus_today_step, booing_penalty_step, booing_penalty_today_step, survival_bonus_given)'
        'VALUES (%(discord_id)s, %(display_name)s, %(marvelous_point)s, %(super_marvelous_left)s, '
        '%(marvelous_bonus_step)s, %(marvelous_bonus_today_step)s, %(booing_penalty_step)s, '
        '%(booing_penalty_today_step)s, %(survival_bonus_given)s)'
    )
    params = to_parameter(user)
    commit(query, params)
