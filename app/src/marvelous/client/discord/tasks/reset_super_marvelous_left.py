from marvelous.usecases.reset_super_marvelous_left import reset_super_marvelous_left
from marvelous.settings import app_settings
from discord.ext import tasks, commands
import datetime


@tasks.loop(seconds=60)
async def job():
    if datetime.datetime.now().time().strftime("%H:%M") == app_settings.super_marvelous.reset_time.strftime("%H:%M"):
        reset_super_marvelous_left(app_settings.super_marvelous.initial_left_count)


def setup(bot: commands.Bot):
    job.start()
