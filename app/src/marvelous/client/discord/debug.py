from discord.ext import commands
from .. import presentation


@commands.command()
async def reset_survival_bonus(ctx: commands.Context):
    presentation.run_reset_survival_bonus()
    await ctx.channel.send("[DEBUG RUN] Reset survival bonus")


@commands.command()
async def reset_super_marvelous_left(ctx: commands.Context):
    presentation.run_reset_super_marvelous_left()
    await ctx.channel.send("[DEBUG RUN] Reset super marvelous left")


@commands.command()
async def reset_daily_steps(ctx: commands.Context):
    presentation.run_reset_daily_steps()
    await ctx.channel.send("[DEBUG RUN] Reset daily steps")


@commands.command()
async def reset_marvelous_point(ctx: commands.Context):
    await presentation.run_reset_marvelous_point()
    await ctx.channel.send("[DEBUG RUN] Reset marvelous point")


@commands.command()
async def check_github_bonus(ctx: commands.Context):
    presentation.run_github_bonus()
    await ctx.channel.send("[DEBUG RUN] Check GitHub bonus")


def setup(bot: commands.Bot):
    bot.add_command(reset_survival_bonus)
    bot.add_command(reset_super_marvelous_left)
    bot.add_command(reset_daily_steps)
    bot.add_command(reset_marvelous_point)
    bot.add_command(check_github_bonus)
