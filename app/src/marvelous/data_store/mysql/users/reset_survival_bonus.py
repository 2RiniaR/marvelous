import mysql.connector
from marvelous.data_store.mysql.connection import connection


def reset_survival_bonus() -> None:
    query = "UPDATE users SET survival_bonus_given = 0"

    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            raise e
