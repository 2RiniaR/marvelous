import mysql.connector
from .. import connection


def delete_user_by_id(discord_id: str) -> None:
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
