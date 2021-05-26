import os
from dataclasses import dataclass


@dataclass()
class DBSettings:
    host: str
    port: str
    user: str
    password: str
    database: str
    pool_size: int


values = DBSettings(
    host=os.environ.get("MYSQL_HOST"),
    port=os.environ.get("MYSQL_PORT"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
    pool_size=int(os.environ.get("MYSQL_POOL_SIZE"))
)
