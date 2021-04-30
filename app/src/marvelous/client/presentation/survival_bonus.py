import discord
from marvelous.models.survival_bonus import reset_survival_bonus, give_survival_bonus
from marvelous.models.user import is_user_exist, update_name
from marvelous.models.errors import ModelError
from marvelous.settings import app_settings
from .user import register_user_implicit
from logging import getLogger
from marvelous.client.discord import message_gateway
from marvelous.settings.messages import get_message
from marvelous.helpers import is_now_time


logger = getLogger(__name__)


async def praise_survival(user: discord.Member, channel: discord.TextChannel):
    message = get_message("praise_survival", user.display_name)
    await message_gateway.send(message, channel)


def is_event_available(user: discord.Member) -> bool:
    return not user.bot


async def register_users_if_not_exist(user: discord.Member):
    if is_user_exist(user.id):
        return

    try:
        await register_user_implicit(user)
    except ModelError as err:
        logger.error(str(err))
        return


async def check_survival_bonus(user: discord.Member, channel: discord.TextChannel):
    if not is_event_available(user):
        return
    await register_users_if_not_exist(user)

    try:
        update_name(user.id, user.display_name)
    except ModelError as err:
        logger.error(str(err))

    try:
        bonus_given = give_survival_bonus(user.id, app_settings.survival.point)
    except ModelError as err:
        logger.error(str(err))
        return

    if bonus_given:
        await praise_survival(user, channel)


def check_reset_survival_bonus():
    reset_time = app_settings.survival.reset_time
    if not is_now_time(reset_time):
        return

    try:
        reset_survival_bonus()
    except ModelError as err:
        logger.error(str(err))
        return
