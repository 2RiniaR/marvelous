from marvelous.models.user import User
from marvelous.data_store.mysql import mysql_client
import mysql.connector


def create(user: User) -> None:
    query = (
        'INSERT INTO users('
        'discord_id, display_name, marvelous_point, super_marvelous_left, marvelous_bonus_step,'
        'marvelous_bonus_today_step, booing_penalty_step, booing_penalty_today_step, survival_bonus_given)'
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    )
    cursor = mysql_client.connection.cursor()

    try:
        cursor.execute(query, [
            str(user.discord_id),
            str(user.display_name),
            str(user.point),
            str(user.super_marvelous_left),
            str(user.marvelous_bonus.step),
            str(user.marvelous_bonus.today),
            str(user.booing_penalty.step),
            str(user.booing_penalty.today),
            "1" if user.survival_bonus_given else "0"
        ])
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
