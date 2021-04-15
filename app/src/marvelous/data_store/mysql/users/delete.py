import mysql.connector
from marvelous.data_store.mysql.connection import connection


def delete(discord_id: str) -> None:
    query = "DELETE FROM users WHERE discord_id = %(discord_id)s"
    params = {"discord_id": discord_id}

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e
