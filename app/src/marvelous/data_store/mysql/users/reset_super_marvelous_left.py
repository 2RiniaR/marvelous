from marvelous.data_store.mysql import mysql_client
import mysql.connector


def reset_super_marvelous_left(value: int) -> None:
    query = "UPDATE users SET super_marvelous_left = %s"
    cursor = mysql_client.connection.cursor()

    try:
        cursor.execute(query, value)
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
