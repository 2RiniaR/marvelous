import discord
import marvelous.discord.bot as bot


async def show_help_on_mention(message: discord.Message):
    if bot.client.user not in message.mentions:
        return
    await bot.show_help(message)
