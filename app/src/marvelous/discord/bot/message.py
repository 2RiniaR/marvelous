import asyncio
import discord
import logging
from marvelous import settings
from marvelous.discord import bot
from typing import Union


logger = logging.getLogger(__name__)


class DiscordMessageGateway:
    strict: bool

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.strict = False

    def send_to_default_channel(
            self, content: str = None, embed: discord.Embed = None, force: bool = False
    ):
        try:
            default_channel_id: int = settings.discord.default_channel_id
        except ValueError:
            logger.warning("Default channel id is invalid. Sending message to default will be canceled.")
            return

        default_channel = bot.instance.client.get_channel(default_channel_id)
        if default_channel is None:
            logger.warning("Default channel is None. Sending message to default was canceled.")
            return
        self.send(default_channel, content=content, embed=embed, force=force)

    def send(
            self, dest: Union[discord.TextChannel, discord.Member],
            content: str = None, embed: discord.Embed = None, force: bool = False
    ):
        asyncio.ensure_future(
            self.__send_with_strict_lock(dest, content=content, embed=embed, force=force), loop=self.loop)

    async def __send_with_strict_lock(
            self, dest: Union[discord.TextChannel, discord.Member],
            content: str = None, embed: discord.Embed = None, force: bool = False
    ):
        if force:
            await dest.send(content, embed=embed)
            return

        if self.strict:
            return
        self.strict = True

        try:
            await dest.send(content, embed=embed)
            await asyncio.sleep(settings.message.strict_time)
        except Exception as err:
            logger.error(str(err))
        finally:
            self.strict = False


sender = DiscordMessageGateway()
