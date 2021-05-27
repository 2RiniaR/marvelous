import logging
from typing import List
import discord
from marvelous import models, settings
from marvelous.discord import bot, presentation


logger = logging.getLogger(__name__)


def get_message(users: List[models.User]) -> str:
    def get_user_column(index: int, user: models.User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    if len(users) == 0:
        return ""

    ranking_text = "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(users[:5])))

    return (
        f"👑今週、一番えらかったのは...  **{str(users[0].display_name)}**\n"
        "\n"
        "```\n"
        "【ランキング上位】\n"
        f"{ranking_text}"
        "```\n"
        "今週もよく頑張ったね。みんなえらい！\n"
        "\n"
        f"「{settings.super_marvelous.reaction} めっちゃえらい！」の使用回数をリセットしました。\n"
        f"えらいポイントをリセットしました。今週も頑張ろう！"
    )


def send_message():
    users = presentation.ranking.get_users()
    message = get_message(list(users))
    embed = discord.Embed(title="今週のえらい", description=message, color=0xe8b77b)
    bot.message.sender.send_to_default_channel(embed=embed, force=True)
