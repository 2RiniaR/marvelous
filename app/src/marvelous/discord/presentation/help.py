import discord
from marvelous.discord import bot


async def show_on_mention(message: discord.Message):
    if bot.instance.client.user not in message.mentions:
        return
    await bot.help.show(message)
