from discord.ext import commands
from ..presentation import show_status, show_ranking


@commands.command()
async def me(ctx: commands.Context):
    """👤自分のステータスを表示する"""
    await show_status(ctx.author, ctx.channel)


@commands.command()
async def ranking(ctx: commands.Context):
    """👑ランキングを表示する"""
    await show_ranking(ctx.channel)


def setup(bot: commands.Bot):
    bot.add_command(me)
    bot.add_command(ranking)
