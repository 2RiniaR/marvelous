from marvelous.models.user import User
from marvelous.data_store.mysql import mysql_client
import mysql.connector


def update(user: User) -> None:
    query = (
        "UPDATE users SET "
        "display_name=%s, marvelous_point=%s, super_marvelous_left=%s,"
        "marvelous_bonus_step=%s, marvelous_bonus_today_step=%s,"
        "booing_penalty_step=%s, booing_penalty_today_step=%s, survival_bonus_given=%s "
        "WHERE discord_id = %s"
    )
    cursor = mysql_client.connection.cursor()

    try:
        cursor.execute(query, [
            str(user.display_name),
            str(user.point),
            str(user.super_marvelous_left),
            str(user.marvelous_bonus.step),
            str(user.marvelous_bonus.today),
            str(user.booing_penalty.step),
            str(user.booing_penalty.today),
            "1" if user.survival_bonus_given else "0",
            str(user.discord_id)
        ])
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
