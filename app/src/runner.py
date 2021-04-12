from marvelous.settings.env import discord_token, app_settings_file_path
from marvelous.data_store.mysql import mysql_client
from marvelous.settings import app_settings
from marvelous.client.discord.client import bot
import logging
import asyncio


def main():
    print((
        "===============================\n"
        "||    Marvelous started!!    ||\n"
        "===============================\n"
    ))

    logging.basicConfig(level=logging.INFO)
    app_settings.load_from_file(app_settings_file_path)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(mysql_client.setup())

    bot.run(discord_token)


if __name__ == '__main__':
    main()
