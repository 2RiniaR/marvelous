from discord.ext import tasks, commands
from ..presentation import (
    check_reset_survival_bonus, check_reset_daily_steps, check_reset_super_marvelous_left
)


@tasks.loop(seconds=60)
async def job():
    check_reset_daily_steps()
    check_reset_survival_bonus()
    check_reset_super_marvelous_left()


def setup(bot: commands.Bot):
    job.start()
