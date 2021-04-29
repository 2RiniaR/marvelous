from marvelous.models.user import User
import mysql.connector
from .. import connection


def create_user(user: User) -> None:
    query = (
        'INSERT INTO users('
        'discord_id, display_name, marvelous_point, super_marvelous_left, marvelous_bonus_step,'
        'marvelous_bonus_today_step, booing_penalty_step, booing_penalty_today_step, survival_bonus_given)'
        'VALUES (%(discord_id)s, %(display_name)s, %(marvelous_point)s, %(super_marvelous_left)s, '
        '%(marvelous_bonus_step)s, %(marvelous_bonus_today_step)s, %(booing_penalty_step)s, '
        '%(booing_penalty_today_step)s, %(survival_bonus_given)s)'
    )
    params = {
        "discord_id": str(user.discord_id),
        "display_name": str(user.display_name),
        "marvelous_point": str(user.point),
        "super_marvelous_left": str(user.super_marvelous_left),
        "marvelous_bonus_step": str(user.marvelous_bonus.step),
        "marvelous_bonus_today_step": str(user.marvelous_bonus.today),
        "booing_penalty_step": str(user.booing_penalty.step),
        "booing_penalty_today_step": str(user.booing_penalty.today),
        "survival_bonus_given": "1" if user.survival_bonus_given else "0",
    }

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e
