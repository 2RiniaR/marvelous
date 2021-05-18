import discord
from typing import Iterable
from marvelous.client.discord import message_gateway
from logging import getLogger
import marvelous.models as models
from marvelous.settings import app_settings


logger = getLogger(__name__)


def get_ranking_message(users: Iterable[models.User]) -> str:
    def get_user_column(index: int, user: models.User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    return "\n".join([
        "```",
        "👏👏👏 えらいポイント ランキング 👏👏👏",
        "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users))),
        "```"
    ])


async def show_ranking(channel: discord.TextChannel):
    try:
        users = models.get_ranking()
    except models.ModelError as err:
        logger.error(str(err))
        return

    message = get_ranking_message(users[:app_settings.message.ranking_limit])
    await message_gateway.send(channel, content=message)
