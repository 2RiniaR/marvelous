from discord.ext import tasks, commands
from marvelous.discord import presentation


@tasks.loop(seconds=1)
async def every_second():
    await presentation.reaction.reflect_caches()


@tasks.loop(seconds=60)
async def check_timer():
    presentation.daily_steps.check_reset_time()
    presentation.survival_bonus.check_reset_time()
    presentation.super_marvelous.check_reset_time()
    presentation.contribution_bonus.check_give_time()
    await presentation.marvelous_point.check_reset_time()


def setup(_: commands.Bot):
    check_timer.start()
    every_second.start()
