from marvelous.usecases.reset_daily_steps import reset_daily_steps
from marvelous.settings import app_settings
from discord.ext import tasks, commands
import datetime


@tasks.loop(seconds=60)
async def job():
    if datetime.datetime.now().time().strftime("%H:%M") == app_settings.marvelous.send_bonus.reset_time.strftime("%H:%M"):
        reset_daily_steps()


def setup(bot: commands.Bot):
    job.start()
