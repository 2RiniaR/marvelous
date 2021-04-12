from discord.ext import commands
import discord
from marvelous.usecases.get_user import get_user, is_user_exist, UserNotFoundError
from marvelous.models.user import User
from marvelous.settings import app_settings
from marvelous.client.discord.actions.register_user_implicit import register_user_implicit
from marvelous.client.discord.message_gateway import message_gateway


def get_user_status_message(user: User) -> str:
    marvelous_bonus_left = app_settings.marvelous.send_bonus.step_interval - user.marvelous_bonus.step
    booing_penalty_left = app_settings.booing.send_penalty.step_interval - user.booing_penalty.step
    today_marvelous_count = min(app_settings.marvelous.send_bonus.daily_step_limit, user.marvelous_bonus.today)
    today_booing_count = min(app_settings.booing.send_penalty.daily_step_limit, user.booing_penalty.today)
    return "\n".join([
        "```",
        f"【{user.display_name}】",
        "累計 👏" + str(user.point),
        "使用可能 🙌" + str(max(0, user.super_marvelous_left)),
        "",
        (
            f":   👏ボーナスまであと 👏{marvelous_bonus_left}  "
            f"（本日分カウント {today_marvelous_count}/{app_settings.marvelous.send_bonus.daily_step_limit}）"
        ),
        (
            f":   🖕ペナルティまであと 🖕{booing_penalty_left}  "
            f"（本日分カウント {today_booing_count}/{app_settings.booing.send_penalty.daily_step_limit}）"
        ),
        "```"
    ])


@commands.command()
async def me(ctx: commands.Context):
    """👤自分のステータスを表示する"""
    author: discord.User = ctx.message.author
    channel: discord.TextChannel = ctx.channel

    if is_user_exist(author.id):
        await register_user_implicit(author, channel)

    try:
        user = get_user(author.id)
    except UserNotFoundError as e:
        return

    message = get_user_status_message(user)
    await message_gateway.send(message, channel)


def setup(bot: commands.Bot):
    bot.add_command(me)
