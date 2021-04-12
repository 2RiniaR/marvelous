from marvelous.usecases.reset_survival_bonus import reset_survival_bonus
from discord.ext import tasks, commands
from marvelous.settings import app_settings
import datetime


@tasks.loop(seconds=60)
async def job():
    if datetime.datetime.now().time().strftime("%H:%M") == app_settings.survival.reset_time.strftime("%H:%M"):
        reset_survival_bonus()


def setup(bot: commands.Bot):
    job.start()
