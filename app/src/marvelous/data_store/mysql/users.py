import marvelous.models as models
from typing import Dict, Tuple, List, Optional
from .execute import fetch_one, fetch_all, commit


def initialize_table() -> None:
    query = (
        'CREATE TABLE IF NOT EXISTS users ('
        '    discord_id bigint unsigned not null primary key,'
        '    display_name varchar(64) not null,'
        '    marvelous_point int signed,'
        '    super_marvelous_left int signed,'
        '    marvelous_bonus_step int unsigned,'
        '    marvelous_bonus_today_step int unsigned,'
        '    booing_penalty_step int unsigned,'
        '    booing_penalty_today_step int unsigned,'
        '    survival_bonus_given boolean,'
        '    github_id varchar(64)'
        ')'
    )
    commit(query)


def to_parameter(user: models.User) -> Dict[str, str]:
    return {
        "discord_id": str(user.discord_id),
        "display_name": str(user.display_name),
        "marvelous_point": str(user.point),
        "super_marvelous_left": str(user.super_marvelous_left),
        "marvelous_bonus_step": str(user.marvelous_bonus.step),
        "marvelous_bonus_today_step": str(user.marvelous_bonus.today),
        "booing_penalty_step": str(user.booing_penalty.step),
        "booing_penalty_today_step": str(user.booing_penalty.today),
        "survival_bonus_given": "1" if user.survival_bonus_given else "0",
        "github_id": str(user.github_id) if user.github_id is not None else None
    }


def to_user(data: Tuple[str, str, str, str, str, str, str, str, str, str]) -> models.User:
    (
        discord_id,
        display_name,
        marvelous_point,
        super_marvelous_left,
        marvelous_bonus_step,
        marvelous_bonus_today_step,
        booing_penalty_step,
        booing_penalty_today_step,
        survival_bonus_given,
        github_id
    ) = data
    return models.User(
        discord_id=int(discord_id),
        display_name=display_name,
        point=int(marvelous_point),
        super_marvelous_left=int(super_marvelous_left),
        marvelous_bonus=models.DailyBonus(step=int(marvelous_bonus_step), today=int(marvelous_bonus_today_step)),
        booing_penalty=models.DailyBonus(step=int(booing_penalty_step), today=int(booing_penalty_today_step)),
        survival_bonus_given=int(survival_bonus_given) == 1,
        github_id=github_id
    )


def create(user: models.User) -> None:
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


def delete_by_id(discord_id: str) -> None:
    query = "DELETE FROM users WHERE discord_id = %(discord_id)s"
    params = {"discord_id": discord_id}
    commit(query, params)


def get_by_id(discord_id: int) -> Optional[models.User]:
    query = "SELECT * FROM users WHERE discord_id=%(discord_id)s"
    params = {"discord_id": str(discord_id)}
    data = fetch_one(query, params)
    if data is None:
        return None
    user = to_user(data)
    return user


def get_all() -> List[models.User]:
    query = "SELECT * FROM users;"
    data = fetch_all(query)
    if data is None:
        return []
    users: List[models.User] = [to_user(row) for row in data]
    return users


def get_all_sorted_by_marvelous_point() -> List[models.User]:
    query = "SELECT * FROM users ORDER BY marvelous_point DESC;"
    data = fetch_all(query)
    if data is None:
        return []
    users: List[models.User] = [to_user(row) for row in data]
    return users


def update(user: models.User) -> None:
    query = (
        "UPDATE users SET "
        "display_name=%(display_name)s,"
        "marvelous_point=%(marvelous_point)s,"
        "super_marvelous_left=%(super_marvelous_left)s,"
        "marvelous_bonus_step=%(marvelous_bonus_step)s,"
        "marvelous_bonus_today_step=%(marvelous_bonus_today_step)s,"
        "booing_penalty_step=%(booing_penalty_step)s,"
        "booing_penalty_today_step=%(booing_penalty_today_step)s,"
        "survival_bonus_given=%(survival_bonus_given)s,"
        "github_id=%(github_id)s "
        "WHERE discord_id = %(discord_id)s"
    )
    params = to_parameter(user)
    commit(query, params)


def update_marvelous_point_all(users: List[models.User]) -> None:
    query_cases = "\n    ".join([f"WHEN %(discord_id_{i})s THEN %(marvelous_point_{i})s" for i, _ in enumerate(users)])
    query_where = ",".join([f"%(discord_id_{i})s" for i, _ in enumerate(users)])
    query = (
        "UPDATE users SET "
        "marvelous_point = CASE discord_id "
        f"{query_cases} "
        f"END WHERE discord_id IN ({query_where})"
    )
    discord_id_params = {f"discord_id_{i}": user.discord_id for i, user in enumerate(users)}
    marvelous_point_params = {f"marvelous_point_{i}": user.point for i, user in enumerate(users)}
    params = {**discord_id_params, **marvelous_point_params}
    commit(query, params)


def reset_survival_bonus() -> None:
    query = "UPDATE users SET survival_bonus_given = 0 where TRUE"
    commit(query)


def reset_super_marvelous_left(value: int) -> None:
    query = "UPDATE users SET super_marvelous_left = %(count)s where TRUE"
    params = {"count": str(value)}
    commit(query, params)


def reset_daily_steps() -> None:
    query = "UPDATE users SET marvelous_bonus_today_step = 0, booing_penalty_today_step = 0 where TRUE"
    commit(query)


def reset_marvelous_point() -> None:
    query = "UPDATE users SET marvelous_point = 0 where TRUE"
    commit(query)
