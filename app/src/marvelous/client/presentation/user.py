import discord
from marvelous.models.user import register_user, get_user, is_user_exist, User, DailyBonus, reset_marvelous_point
from marvelous.models.errors import ModelError
from marvelous.settings import app_settings
from marvelous.client.discord import message_gateway
from logging import getLogger
from marvelous.helpers import is_now_time, is_now_weekday


logger = getLogger(__name__)


def get_initial_user(user: discord.Member):
    return User(
        discord_id=user.id,
        display_name=user.display_name,
        marvelous_bonus=DailyBonus(step=0, today=0),
        booing_penalty=DailyBonus(step=0, today=0),
        super_marvelous_left=app_settings.super_marvelous.initial_left_count,
        survival_bonus_given=False,
        point=0,
    )


def get_status_message(user: User) -> str:
    marvelous_bonus_left = app_settings.marvelous.send_bonus.step_interval - user.marvelous_bonus.step
    booing_penalty_left = app_settings.booing.send_penalty.step_interval - user.booing_penalty.step
    today_marvelous_count = min(app_settings.marvelous.send_bonus.daily_step_limit, user.marvelous_bonus.today)
    today_booing_count = min(app_settings.booing.send_penalty.daily_step_limit, user.booing_penalty.today)
    return "\n".join([
        "```",
        f"【{user.display_name}】",
        "累計 👏" + str(user.point),
        f"使用可能 {app_settings.super_marvelous.reaction}" + str(max(0, user.super_marvelous_left)),
        "",
        (
            f":   {app_settings.marvelous.reaction}ボーナスまであと {app_settings.marvelous.reaction}{marvelous_bonus_left}  "
            f"（本日分カウント {today_marvelous_count}/{app_settings.marvelous.send_bonus.daily_step_limit}）"
        ),
        (
            f":   {app_settings.booing.reaction}ペナルティまであと {app_settings.booing.reaction}{booing_penalty_left}  "
            f"（本日分カウント {today_booing_count}/{app_settings.booing.send_penalty.daily_step_limit}）"
        ),
        "```"
    ])


async def show_status(user: discord.Member, channel: discord.TextChannel):
    if not is_user_exist(user.id):
        await register_user_implicit(user)

    try:
        result_user = get_user(user.id)
    except ModelError as e:
        logger.error(str(e))
        return

    message = get_status_message(result_user)
    await message_gateway.send(message, channel)


async def register_user_implicit(author: discord.Member):
    try:
        user: User = get_initial_user(author)
        register_user(user)
    except ModelError as err:
        logger.error(str(err))


def check_reset_marvelous_point():
    reset_time = app_settings.user.reset_marvelous_point_time
    reset_weekday = app_settings.user.reset_marvelous_point_weekday
    if not (is_now_time(reset_time) and is_now_weekday(reset_weekday)):
        return
    run_reset_marvelous_point()


def run_reset_marvelous_point():
    try:
        reset_marvelous_point()
    except ModelError as err:
        logger.error(str(err))
        return
