import mysql.connector
from marvelous.data_store.mysql.connection import connection


def reset_daily_steps() -> None:
    query = "UPDATE users SET marvelous_bonus_today_step = 0, booing_penalty_today_step = 0"

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e
