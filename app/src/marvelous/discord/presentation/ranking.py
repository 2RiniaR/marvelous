import discord
from typing import Iterable
import logging
from marvelous.domain import models, services
import marvelous.discord.bot as bot
import marvelous.settings as settings


logger = logging.getLogger(__name__)


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
        return services.get_marvelous_point_ranking()
    except models.ModelError:
        logger.exception("An unknown exception raised while getting marvelous point ranking.")


async def show_ranking(channel: discord.TextChannel):
    users = get_ranking()
    message = get_ranking_message(users[:settings.message.ranking_limit])
    await bot.message_gateway.send(channel, content=message)
