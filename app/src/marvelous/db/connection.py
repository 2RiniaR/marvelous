import logging
import asyncio
from typing import Union, Optional
import mysql.connector
import mysql.connector.errorcode
from marvelous import settings


logger = logging.getLogger(__name__)


async def wait_ready():
    logger.debug("Waiting connect to MySQL server.")
    max_attempt = 30
    attempt = 0
    client = connection()

    while True:
        try:
            attempt += 1
            client.open_connection()
            if client.is_connected():
                client.close_connection()
                return
        except mysql.connector.Error as err:
            logger.debug(str(err))
            pass

        logger.debug(f"Attempt {attempt}...")
        if attempt >= max_attempt:
            logger.error(f"Failed to connect to MySQL server.")
            return

        await asyncio.sleep(1)


class MySQLClient:
    host: str
    port: str
    user: str
    password: str
    database: str
    pool_size: int
    pool_name: str = "mysql"
    connection: Optional[Union[mysql.connector.CMySQLConnection, mysql.connector.MySQLConnection]]

    def __init__(self, host: str, port: str, user: str, password: str, database: str, pool_size: int):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self.connection = None

    def __enter__(self):
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def open_connection(self):
        logger.debug(
            f"Connecting to MySQL server...  (host: {self.host}, port: {self.port}, user: {self.user}, "
            f"password: *HIDDEN*, database: {self.database})",
        )

        try:
            self.connection = mysql.connector.connect(
                host=self.host, port=self.port, user=self.user, password=self.password, database=self.database,
                # 現在のデプロイ環境では、コネクションプールがサポートされていないため設定をオフにしている
                # pool_size=self.pool_size, pool_name=self.pool_name, pool_reset_session=False
            )
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Something is wrong with your user name or password.")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist.")
            else:
                logger.error(err)
            raise err

        logger.info("Connected to MySQL server.")

    def close_connection(self):
        logger.debug("Closing MySQL server connection.")
        self.connection.close()
        logger.info("Closed MySQL server connection.")

    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()


def connection() -> MySQLClient:
    return MySQLClient(
        host=settings.db.host,
        port=settings.db.port,
        user=settings.db.user,
        password=settings.db.password,
        database=settings.db.database,
        pool_size=settings.db.pool_size
    )
