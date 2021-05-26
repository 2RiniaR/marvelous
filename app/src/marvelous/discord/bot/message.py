import asyncio
import discord
import logging
from marvelous import settings
from marvelous.discord import bot


logger = logging.getLogger(__name__)


class DiscordMessageGateway:
    strict: bool

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.strict = False

    async def send_to_default_channel(
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
        await self.send(default_channel, content=content, embed=embed, force=force)

    async def send(
            self, channel: discord.TextChannel, content: str = None, embed: discord.Embed = None, force: bool = False
    ):
        asyncio.ensure_future(
            self.__send_with_strict_lock(channel, content=content, embed=embed, force=force), loop=self.loop)

    async def __send_with_strict_lock(
            self, channel: discord.TextChannel, content: str = None, embed: discord.Embed = None, force: bool = False
    ):
        if force:
            await channel.send(content, embed=embed)
            return

        if self.strict:
            return
        self.strict = True

        try:
            await channel.send(content, embed=embed)
            await asyncio.sleep(settings.message.strict_time)
        except Exception as err:
            logger.error(str(err))
        finally:
            self.strict = False


sender = DiscordMessageGateway()
