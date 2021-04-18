from marvelous.models.usecases import reset_survival_bonus
import discord
from marvelous.models.usecases import give_survival_bonus, is_user_exist
from marvelous.models.errors import ModelError
from marvelous.settings import app_settings
from .user import register_user_implicit
from logging import getLogger
from marvelous.client.discord import message_gateway
from marvelous.settings.messages import get_message
from marvelous.helpers import is_now_time


logger = getLogger(__name__)


async def praise_survival(user: discord.Member, channel: discord.TextChannel):
    message = get_message("praise_survival", user.name)
    await message_gateway.send(message, channel)


def is_event_available(user: discord.Member) -> bool:
    return not user.bot


async def register_users_if_not_exist(user: discord.Member):
    if not is_user_exist(user.id):
        await register_user_implicit(user)


async def check_survival_bonus(user: discord.Member, channel: discord.TextChannel):
    if not is_event_available(user):
        return
    await register_users_if_not_exist(user)

    try:
        bonus_given = give_survival_bonus(user.id, app_settings.survival.point)
    except ModelError as err:
        logger.warning(str(err))
        return

    if bonus_given:
        await praise_survival(user, channel)


def check_reset_survival_bonus():
    reset_time = app_settings.survival.reset_time
    if is_now_time(reset_time):
        reset_survival_bonus()
