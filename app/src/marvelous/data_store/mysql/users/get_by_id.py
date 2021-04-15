from typing import Optional
import mysql.connector
from marvelous.data_store.mysql.connection import connection
from marvelous.data_store.mysql.users.convert_to_user import convert_to_user
from marvelous.models.user import User


def get_by_id(discord_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE discord_id=%(discord_id)s"
    params = {"discord_id": discord_id}

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            data = cursor.fetchone()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e

    if data is None:
        return None
    user = convert_to_user(data)
    return user
