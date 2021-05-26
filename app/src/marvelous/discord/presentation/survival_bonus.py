import discord
import logging
from typing import Optional
from marvelous import settings, helpers, services, models
from marvelous.discord import presentation, cache, bot


logger = logging.getLogger(__name__)


async def praise(user: discord.Member, channel: discord.TextChannel):
    message = helpers.phrase.get_random_phrase(settings.message.phrases.praise_survival, user.display_name)
    await bot.message.sender.send(channel, content=message, force=True)


def is_given(user_id: int) -> bool:
    state: Optional[cache.user.UserContext] = cache.user.memory.get_state(user_id)
    if state is not None:
        return state.survival_bonus_given
    state = presentation.user.update_cache(user_id)
    return state.survival_bonus_given


def is_event_available(user: discord.Member) -> bool:
    return not user.bot


async def check_give(user: discord.Member, channel: discord.TextChannel):
    if not is_event_available(user):
        return

    await presentation.user.register_if_not_exist(user)

    if is_given(user.id):
        return

    try:
        services.user.update_name(user.id, user.display_name)
    except models.ModelError:
        logger.exception("An unknown exception raised while updating user name.")

    try:
        bonus_given = services.survival_bonus.give(user.id, settings.survival_bonus.point)
        presentation.user.update_cache(user.id)
    except models.ModelError:
        logger.exception("An unknown exception raised while giving survival bonus.")
        return

    if bonus_given:
        await praise(user, channel)


def check_reset_time():
    reset_time = settings.survival_bonus.reset_time
    if not helpers.time.is_now_time(reset_time):
        return
    reset()


def reset():
    try:
        services.survival_bonus.reset()
        presentation.user.clear_cache()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting survival bonus.")
        return
