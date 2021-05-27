import discord
from marvelous.discord import bot


def show_on_mention(message: discord.Message):
    if bot.instance.client.user not in message.mentions:
        return
    bot.help.show(message)
