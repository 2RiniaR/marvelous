import datetime
import discord
from marvelous import clock
from marvelous.discord import bot


def show_datetime(channel: discord.TextChannel):
    message = f"Current time: {clock.get_now().isoformat()}"
    bot.message.sender.send(channel, content=message, force=True)


def set_datetime(channel: discord.TextChannel, dt: str):
    clock.set_now_manually(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"))
    show_datetime(channel)


def reset_datetime(channel: discord.TextChannel):
    clock.reset_now_manually()
    show_datetime(channel)
