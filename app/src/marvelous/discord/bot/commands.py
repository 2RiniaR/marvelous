from discord.ext import commands
from marvelous.discord import presentation, bot


@commands.command()
async def me(ctx: commands.Context):
    presentation.user.show_status(ctx.author, ctx.channel)


@commands.command()
async def ranking(ctx: commands.Context):
    presentation.ranking.show(ctx.channel)


@commands.group()
async def github(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        bot.message.sender.send(ctx.channel, "このコマンドにはサブコマンドが必要です。", force=True)


@github.command(name="register")
async def register_github(ctx: commands.Context, github_id: str):
    presentation.user.register_github(ctx.author, ctx.channel, github_id)


@github.command(name="unregister")
async def unregister_github(ctx: commands.Context):
    presentation.user.unregister_github(ctx.author, ctx.channel)


def setup(bot: commands.Bot):
    bot.add_command(me)
    bot.add_command(ranking)
    bot.add_command(github)
