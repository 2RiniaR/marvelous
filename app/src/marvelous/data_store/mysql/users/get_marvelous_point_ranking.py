from typing import Iterable
import mysql.connector
from marvelous.data_store.mysql.connection import connection
from marvelous.data_store.mysql.users.convert_to_user import convert_to_user
from marvelous.models.user import User


def get_marvelous_point_ranking() -> Iterable[User]:
    query = "SELECT * FROM users ORDER BY marvelous_point DESC;"

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e

    if data is None:
        return []
    users: Iterable[User] = [convert_to_user(row) for row in data]
    return users
