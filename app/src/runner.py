from marvelous.settings.env import discord_token, app_settings_file_path
from marvelous.data_store.mysql.connection import wait_ready
from marvelous.settings import app_settings
from marvelous.client.discord.client import bot
import logging
import asyncio


def wait_db_ready():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_ready())


def main():
    print((
        "===============================\n"
        "||    Marvelous started!!    ||\n"
        "===============================\n"
    ))
    logging.basicConfig(level=logging.INFO)
    app_settings.load_from_file(app_settings_file_path)
    wait_db_ready()
    bot.run(discord_token)


if __name__ == '__main__':
    main()
