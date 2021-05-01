from discord.ext import tasks, commands
from ..presentation import (
    check_reset_survival_bonus, check_reset_daily_steps, check_reset_super_marvelous_left, check_reset_marvelous_point
)
from .reaction import reflect_caches


@tasks.loop(seconds=1)
async def every_second():
    await reflect_caches()


@tasks.loop(seconds=60)
async def check_timer():
    check_reset_daily_steps()
    check_reset_survival_bonus()
    check_reset_super_marvelous_left()
    check_reset_marvelous_point()


def setup(_: commands.Bot):
    check_timer.start()
    every_second.start()
