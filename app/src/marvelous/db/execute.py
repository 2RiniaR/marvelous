from . import connection
import mysql.connector
from .connection import connection
import logging


logger = logging.getLogger(__name__)


def commit(query: str, params=None):
    if params is None:
        params = {}
    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            client.connection.commit()
        except mysql.connector.Error as e:
            client.connection.rollback()
            logger.error(str(e))
            raise e


def fetch_one(query: str, params=None):
    if params is None:
        params = {}
    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            data = cursor.fetchone()
        except mysql.connector.Error as e:
            client.connection.rollback()
            logger.error(str(e))
            raise e
    return data


def fetch_all(query: str, params=None):
    if params is None:
        params = {}
    with connection() as client:
        cursor = client.connection.cursor()
        try:
            cursor.execute(query, params)
            data = cursor.fetchall()
        except mysql.connector.Error as e:
            client.connection.rollback()
            logger.error(str(e))
            raise e
    return data
