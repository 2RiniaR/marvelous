from typing import Iterable
from marvelous.data_store.mysql import mysql_client
from marvelous.data_store.mysql.users.convert_to_user import convert_to_user
from marvelous.models.user import User


def get_marvelous_point_ranking() -> Iterable[User]:
    query = "SELECT * FROM users ORDER BY marvelous_point DESC;"
    cursor = mysql_client.connection.cursor()
    cursor.execute(query)
    fetched_data = cursor.fetchall()

    if fetched_data is None:
        return []

    users: Iterable[User] = [convert_to_user(data) for data in fetched_data]
    return users
