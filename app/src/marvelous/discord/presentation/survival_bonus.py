import discord
import logging
from typing import Optional
from marvelous.domain import models, services
import marvelous.settings as settings
import marvelous.discord.bot as bot
import marvelous.helpers as helpers
from .user import update_user_cache, register_user_implicit, clear_user_cache
from marvelous.discord.cahce import user_cache, UserContext


logger = logging.getLogger(__name__)


async def praise_survival(user: discord.Member, channel: discord.TextChannel):
    message = helpers.get_random_phrase(settings.message.phrases.praise_survival, user.display_name)
    await bot.message_gateway.send(channel, content=message, force=True)


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
        services.update_user_name(user.id, user.display_name)
    except models.ModelError:
        logger.exception("An unknown exception raised while updating user name.")

    try:
        bonus_given = services.give_survival_bonus(user.id, settings.survival_bonus.point)
        update_user_cache(user.id)
    except models.ModelError:
        logger.exception("An unknown exception raised while giving survival bonus.")
        return

    if bonus_given:
        await praise_survival(user, channel)


def check_reset_survival_bonus():
    reset_time = settings.survival_bonus.reset_time
    if not helpers.is_now_time(reset_time):
        return
    run_reset_survival_bonus()


def run_reset_survival_bonus():
    try:
        services.reset_survival_bonus()
        clear_user_cache()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting survival bonus.")
        return
