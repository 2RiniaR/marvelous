import mysql.connector
from marvelous.data_store.mysql.connection import connection


def reset_super_marvelous_left(value: int) -> None:
    query = "UPDATE users SET super_marvelous_left = %(count)s"
    params = {"count": value}

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e
