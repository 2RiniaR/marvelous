from marvelous.data_store.mysql import mysql_client
import mysql.connector


def reset_daily_steps() -> None:
    query = "UPDATE users SET marvelous_bonus_today_step = 0, booing_penalty_today_step = 0"
    cursor = mysql_client.connection.cursor()

    try:
        cursor.execute(query)
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
