import asyncio
import discord
import logging
from typing import Union


logger = logging.getLogger(__name__)


class ReactionGateway:

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def add(self, message: discord.Message, emoji: Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]):
        asyncio.ensure_future(message.add_reaction(emoji), loop=self.loop)


sender = ReactionGateway()
