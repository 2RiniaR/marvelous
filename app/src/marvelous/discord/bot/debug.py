from discord.ext import commands
from marvelous.discord import presentation, bot


@commands.command()
async def reset_survival_bonus(ctx: commands.Context):
    presentation.survival_bonus.reset()
    bot.message.sender.send(ctx.channel, "[DEBUG RUN] Reset survival bonus", force=True)


@commands.command()
async def reset_super_marvelous_left(ctx: commands.Context):
    presentation.super_marvelous.reset()
    bot.message.sender.send(ctx.channel, "[DEBUG RUN] Reset super marvelous left", force=True)


@commands.command()
async def reset_daily_steps(ctx: commands.Context):
    presentation.daily_steps.reset()
    bot.message.sender.send(ctx.channel, "[DEBUG RUN] Reset daily steps", force=True)


@commands.command()
async def reset_marvelous_point(ctx: commands.Context):
    presentation.marvelous_point.reset()
    bot.message.sender.send(ctx.channel, "[DEBUG RUN] Reset marvelous point", force=True)


@commands.command()
async def check_contribution_bonus(ctx: commands.Context):
    presentation.contribution_bonus.give()
    bot.message.sender.send(ctx.channel, "[DEBUG RUN] Check GitHub bonus", force=True)


def setup(bot: commands.Bot):
    bot.add_command(reset_survival_bonus)
    bot.add_command(reset_super_marvelous_left)
    bot.add_command(reset_daily_steps)
    bot.add_command(reset_marvelous_point)
    bot.add_command(check_contribution_bonus)
