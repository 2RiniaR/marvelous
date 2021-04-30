import discord
from marvelous.models.user import get_ranking, User
from typing import Iterable
from marvelous.client.discord import message_gateway
from logging import getLogger
from marvelous.models.errors import ModelError


logger = getLogger(__name__)


def get_ranking_message(users: Iterable[User]) -> str:
    def get_user_column(index: int, user: User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    return "\n".join([
        "```",
        "👏👏👏 えらいポイント ランキング 👏👏👏",
        "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users))),
        "```"
    ])


async def show_ranking(channel: discord.TextChannel):
    try:
        users = get_ranking()
    except ModelError as err:
        logger.error(str(err))
        return

    message = get_ranking_message(users)
    await message_gateway.send(message, channel)
