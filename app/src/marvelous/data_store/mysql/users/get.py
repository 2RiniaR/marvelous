from typing import Optional
import mysql.connector
from .. import connection
from logging import getLogger
from typing import Iterable
from typing import Tuple
from marvelous.models.daily_bonus import DailyBonus
from marvelous.models.user import User


logger = getLogger(__name__)


def get_user_by_id(discord_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE discord_id=%(discord_id)s"
    params = {"discord_id": discord_id}

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            data = cursor.fetchone()
        except mysql.connector.Error as e:
            client.connection.rollback()
            logger.error(str(e))
            raise e

    if data is None:
        return None
    user = convert_to_user(data)
    return user


def get_users_marvelous_point_ranking() -> Iterable[User]:
    query = "SELECT * FROM users ORDER BY marvelous_point DESC;"

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e

    if data is None:
        return []
    users: Iterable[User] = [convert_to_user(row) for row in data]
    return users


def convert_to_user(data: Tuple[str, str, str, str, str, str, str, str, str]) -> User:
    (discord_id, display_name, marvelous_point, super_marvelous_left, marvelous_bonus_step,
     marvelous_bonus_today_step, booing_penalty_step, booing_penalty_today_step, survival_bonus_given) = data
    return User(
        discord_id=int(discord_id),
        display_name=display_name,
        point=int(marvelous_point),
        super_marvelous_left=int(super_marvelous_left),
        marvelous_bonus=DailyBonus(step=int(marvelous_bonus_step), today=int(marvelous_bonus_today_step)),
        booing_penalty=DailyBonus(step=int(booing_penalty_step), today=int(booing_penalty_today_step)),
        survival_bonus_given=int(survival_bonus_given) == 1
    )
