import discord
import marvelous.models as models
from marvelous.settings import app_settings
from logging import getLogger
from marvelous.client.discord import message_gateway
from marvelous.settings.messages import get_message
from marvelous.helpers import is_now_time
from typing import Optional
from .user import update_user_cache, register_user_implicit, clear_user_cache
from ..discord.user import user_cache, UserContext


logger = getLogger(__name__)


async def praise_survival(user: discord.Member, channel: discord.TextChannel):
    message = get_message("praise_survival", user.display_name)
    await message_gateway.send(channel, content=message, force=True)


def is_survival_bonus_given(user_id: int) -> bool:
    state: Optional[UserContext] = user_cache.get_state(user_id)
    if state is not None:
        return state.survival_bonus_given
    state = update_user_cache(user_id)
    return state.survival_bonus_given


def is_event_available(user: discord.Member) -> bool:
    return not user.bot


async def check_survival_bonus(user: discord.Member, channel: discord.TextChannel):
    if not is_event_available(user):
        return

    await register_user_implicit(user)

    if is_survival_bonus_given(user.id):
        return

    try:
        models.update_name(user.id, user.display_name)
    except models.ModelError:
        logger.exception("An unknown exception raised while updating user name.")

    try:
        bonus_given = models.give_survival_bonus(user.id, app_settings.survival.point)
        update_user_cache(user.id)
    except models.ModelError:
        logger.exception("An unknown exception raised while giving survival bonus.")
        return

    if bonus_given:
        await praise_survival(user, channel)


def check_reset_survival_bonus():
    reset_time = app_settings.survival.reset_time
    if not is_now_time(reset_time):
        return
    run_reset_survival_bonus()


def run_reset_survival_bonus():
    try:
        models.reset_survival_bonus()
        clear_user_cache()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting survival bonus.")
        return
