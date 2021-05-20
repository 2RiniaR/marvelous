import marvelous.settings.env as env
import marvelous.data_store as data_store
import marvelous.client.discord as discord
import logging
import asyncio


async def startup_async():
    print((
        "===============================\n"
        "||    Marvelous started!!    ||\n"
        "===============================\n"
    ))
    logging.basicConfig(level=logging.DEBUG if env.run_environment == "development" else logging.WARNING)
    await data_store.wait_ready()
    await discord.start(env.discord_token)


def startup():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup_async())
