from discord.ext import commands
import discord
from marvelous.usecases.get_ranking import get_ranking
from marvelous.models.user import User
from typing import Iterable


def get_ranking_message(users: Iterable[User]) -> str:
    def get_user_column(index: int, user: User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    return "\n".join([
        "```",
        "👏👏👏 えらいポイント ランキング 👏👏👏",
        "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users))),
        "```"
    ])


@commands.command()
async def ranking(ctx: commands.Context):
    """👑ランキングを表示する"""
    channel: discord.TextChannel = ctx.channel

    users = get_ranking()
    message = get_ranking_message(users)
    await channel.send(message)


def setup(bot: commands.Bot):
    bot.add_command(ranking)
