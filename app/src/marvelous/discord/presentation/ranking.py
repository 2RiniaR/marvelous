import discord
from typing import Iterable
import logging
from marvelous import settings, services, models
from marvelous.discord import bot


logger = logging.getLogger(__name__)


def get_message(users: Iterable[models.User]) -> str:
    def get_user_column(index: int, user: models.User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    return "\n".join([
        "```",
        "👏👏👏 えらいポイント ランキング 👏👏👏",
        "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users))),
        "```"
    ])


def get_users() -> Iterable[models.User]:
    try:
        return services.marvelous_point.get_ranking()
    except models.ModelError:
        logger.exception("An unknown exception raised while getting marvelous point ranking.")


async def show(channel: discord.TextChannel):
    users = get_users()
    message = get_message(users[:settings.message.ranking_limit])
    await bot.message.sender.send(channel, content=message)
