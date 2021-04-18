from marvelous.settings.env import discord_token, app_settings_file_path
from marvelous.data_store.mysql.connection import wait_ready
from marvelous.settings import app_settings
from marvelous.client import start
import logging
import asyncio


async def wait_db_ready():
    await wait_ready()


async def startup_async():
    print((
        "===============================\n"
        "||    Marvelous started!!    ||\n"
        "===============================\n"
    ))
    logging.basicConfig(level=logging.INFO)
    app_settings.load_from_file(app_settings_file_path)
    await wait_db_ready()
    await start(discord_token)


def startup():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup_async())
