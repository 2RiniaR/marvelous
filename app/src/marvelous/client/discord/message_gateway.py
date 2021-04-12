import asyncio
import discord
from marvelous.settings import app_settings


class DiscordMessageGateway:
    strict: bool

    async def send_message(self, text: str, channel: discord.TextChannel, mode: str):
        if mode == "all":
            await channel.send(text)
        elif mode == "strict":
            await self.send_message_strict(text, channel)

    async def send_message_strict(self, text: str, channel: discord.TextChannel):
        if self.strict:
            return
        self.strict = True
        await channel.send(text)
        await asyncio.sleep(app_settings.message.strict_time)
        self.strict = False


message_gateway = DiscordMessageGateway()
