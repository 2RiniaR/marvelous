import asyncio
import discord
from marvelous.settings import app_settings


class DiscordMessageGateway:
    strict: bool

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.strict = False

    async def send_force(self, text: str, channel: discord.TextChannel):
        await channel.send(text)

    async def send(self, text: str, channel: discord.TextChannel):
        asyncio.ensure_future(self.__send_with_strict_lock(text, channel), loop=self.loop)

    async def __send_with_strict_lock(self, text: str, channel: discord.TextChannel):
        if self.strict:
            return
        self.strict = True
        await channel.send(text)
        await asyncio.sleep(app_settings.message.strict_time)
        self.strict = False


message_gateway = DiscordMessageGateway()
