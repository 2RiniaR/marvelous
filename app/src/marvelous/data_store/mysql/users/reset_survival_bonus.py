from marvelous.data_store.mysql import mysql_client
import mysql.connector


def reset_survival_bonus() -> None:
    query = "UPDATE users SET survival_bonus_given = 0"
    cursor = mysql_client.connection.cursor()

    try:
        cursor.execute(query)
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
