from marvelous import settings, db, discord
import logging
import asyncio


async def startup_async():
    print((
        "===============================\n"
        "||    Marvelous started!!    ||\n"
        "===============================\n"
    ))
    logging.basicConfig(level=logging.DEBUG if settings.environment.is_development else logging.WARNING)
    await db.initialize()
    await discord.start(settings.discord.token)


def startup():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup_async())
