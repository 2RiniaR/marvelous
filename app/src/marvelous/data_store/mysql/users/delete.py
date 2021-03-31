from marvelous.data_store.mysql import mysql_client
import mysql.connector


def delete(discord_id: str) -> None:
    query = "DELETE FROM users WHERE discord_id = %s"
    cursor = mysql_client.connection.cursor()
    try:
        cursor.execute(query, discord_id)
        mysql_client.connection.commit()
    except mysql.connector.Error as e:
        mysql_client.connection.rollback()
        raise e
