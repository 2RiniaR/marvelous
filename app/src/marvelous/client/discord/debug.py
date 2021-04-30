from discord.ext import commands
from ..presentation import run_reset_super_marvelous_left, run_reset_survival_bonus, run_reset_daily_steps


@commands.command()
async def reset_survival_bonus(ctx: commands.Context):
    """👤自分のステータスを表示する"""
    run_reset_survival_bonus()


@commands.command()
async def reset_super_marvelous_left(ctx: commands.Context):
    """👑ランキングを表示する"""
    run_reset_super_marvelous_left()


@commands.command()
async def reset_daily_steps(ctx: commands.Context):
    """👑ランキングを表示する"""
    run_reset_daily_steps()


def setup(bot: commands.Bot):
    bot.add_command(reset_survival_bonus)
    bot.add_command(reset_super_marvelous_left)
    bot.add_command(reset_daily_steps)
