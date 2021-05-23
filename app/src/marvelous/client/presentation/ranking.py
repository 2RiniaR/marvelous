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


def get_ranking() -> Iterable[models.User]:
    try:
        return models.get_ranking()
    except models.ModelError:
        logger.exception("An unknown exception raised while getting marvelous point ranking.")


async def show_ranking(channel: discord.TextChannel):
    users = get_ranking()
    message = get_ranking_message(users[:app_settings.message.ranking_limit])
    await message_gateway.send(channel, content=message)
