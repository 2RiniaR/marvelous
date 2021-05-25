import discord.ext.commands as commands
import marvelous.discord.presentation as presentation


@commands.command()
async def me(ctx: commands.Context):
    await presentation.show_status(ctx.author, ctx.channel)


@commands.command()
async def ranking(ctx: commands.Context):
    await presentation.show_ranking(ctx.channel)


@commands.group()
async def github(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send('このコマンドにはサブコマンドが必要です。')


@github.command(name="register")
async def register_github(ctx: commands.Context, github_id: str):
    await presentation.register_github(ctx.author, ctx.channel, github_id)


@github.command(name="unregister")
async def unregister_github(ctx: commands.Context):
    await presentation.unregister_github(ctx.author, ctx.channel)


def setup(bot: commands.Bot):
    bot.add_command(me)
    bot.add_command(ranking)
    bot.add_command(github)
