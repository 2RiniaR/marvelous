import logging
from typing import List
import discord
from marvelous import models, settings
from marvelous.discord import bot, presentation


logger = logging.getLogger(__name__)


def get_message(users: List[models.User]) -> str:
    def get_user_column(index: int, user: models.User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'๐{user.point}'.rjust(4)}  {user.display_name}"

    if len(users) == 0:
        return ""

    ranking_text = "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users[:5])))

    return (
        f"๐ไป้ฑใไธ็ชใใใใฃใใฎใฏ...  **{str(users[0].display_name)}**\n"
        "\n"
        "```\n"
        "ใใฉใณใญใณใฐไธไฝใ\n"
        f"{ranking_text}"
        "```\n"
        "ไป้ฑใใใ้ ๅผตใฃใใญใใฟใใชใใใ๏ผ\n"
        "\n"
        f"ใ{settings.super_marvelous.reaction} ใใฃใกใใใใ๏ผใใฎไฝฟ็จๅๆฐใใชใปใใใใพใใใ\n"
        f"ใใใใใคใณใใใชใปใใใใพใใใไป้ฑใ้ ๅผตใใ๏ผ"
    )


def send_message():
    users = presentation.ranking.get_users()
    message = get_message(list(users))
    embed = discord.Embed(title="ไป้ฑใฎใใใ", description=message, color=0xe8b77b)
    bot.message.sender.send_to_default_channel(embed=embed, force=True)
