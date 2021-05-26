from marvelous import db, settings
from . import connection


async def initialize():
    await db.connection.wait_ready()
    initialize_tables()


def initialize_tables():
    if settings.environment.is_development:
        db.users.drop_table()
    db.users.initialize_table()
