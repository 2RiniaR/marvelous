import mysql.connector
import marvelous.settings
import asyncio


async def connect_to_server():
    while True:
        try:
            conn = mysql.connector.connect(
                host=marvelous.settings.env.mysql_host,
                port=marvelous.settings.env.mysql_port,
                user=marvelous.settings.env.mysql_user,
                password=marvelous.settings.env.mysql_password,
                database=marvelous.settings.env.mysql_database
            )
            if conn.is_connected():
                break
        except mysql.connector.DatabaseError as e:
            pass

        await asyncio.sleep(1)

    conn.ping(reconnect=True)
    return conn


class MySQLClient:
    def __init__(self):
        self.__connection = None

    async def setup(self):
        print("\n".join([
            "Connecting to MySQL server...",
            f"    host: {marvelous.settings.env.mysql_host}",
            f"    port: {marvelous.settings.env.mysql_port}",
            f"    user: {marvelous.settings.env.mysql_user}",
            f"    password: {marvelous.settings.env.mysql_password}",
            f"    database: {marvelous.settings.env.mysql_database}",
        ]))
        self.__connection = await connect_to_server()
        print("Connected to MySQL server.")

    @property
    def connection(self):
        return self.__connection


mysql_client = MySQLClient()
