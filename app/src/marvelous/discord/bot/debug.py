from discord.ext import commands
from marvelous.discord import presentation


@commands.command()
async def reset_survival_bonus(ctx: commands.Context):
    presentation.survival_bonus.reset()
    await ctx.channel.send("[DEBUG RUN] Reset survival bonus")


@commands.command()
async def reset_super_marvelous_left(ctx: commands.Context):
    presentation.super_marvelous.reset()
    await ctx.channel.send("[DEBUG RUN] Reset super marvelous left")


@commands.command()
async def reset_daily_steps(ctx: commands.Context):
    presentation.daily_steps.reset()
    await ctx.channel.send("[DEBUG RUN] Reset daily steps")


@commands.command()
async def reset_marvelous_point(ctx: commands.Context):
    await presentation.marvelous_point.reset()
    await ctx.channel.send("[DEBUG RUN] Reset marvelous point")


@commands.command()
async def check_contribution_bonus(ctx: commands.Context):
    presentation.contribution_bonus.give()
    await ctx.channel.send("[DEBUG RUN] Check GitHub bonus")


def setup(bot: commands.Bot):
    bot.add_command(reset_survival_bonus)
    bot.add_command(reset_super_marvelous_left)
    bot.add_command(reset_daily_steps)
    bot.add_command(reset_marvelous_point)
    bot.add_command(check_contribution_bonus)
