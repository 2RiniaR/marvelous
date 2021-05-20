from discord.ext import commands
from .. import presentation


@commands.command()
async def me(ctx: commands.Context):
    await presentation.show_status(ctx.author, ctx.channel)


@commands.command()
async def ranking(ctx: commands.Context):
    await presentation.show_ranking(ctx.channel)


def setup(bot: commands.Bot):
    bot.add_command(me)
    bot.add_command(ranking)
