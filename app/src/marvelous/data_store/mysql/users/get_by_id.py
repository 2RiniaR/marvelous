from typing import Optional
from marvelous.data_store.mysql import mysql_client
from marvelous.data_store.mysql.users.convert_to_user import convert_to_user
from marvelous.models.user import User


def get_by_id(discord_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE discord_id=%s"
    cursor = mysql_client.connection.cursor()
    cursor.execute(query, [discord_id])

    data = cursor.fetchone()
    if data is None:
        return None

    user = convert_to_user(data)
    return user
