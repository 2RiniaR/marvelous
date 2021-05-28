import discord
from marvelous import settings, models, helpers, clock
from marvelous.discord import bot, presentation, cache
from logging import getLogger
from typing import Optional


logger = getLogger(__name__)


def is_event_available(user: discord.Member) -> bool:
    return not user.bot


def is_sleeping(user_id: int) -> bool:
    state: Optional[cache.user.UserContext] = cache.user.memory.get_state(user_id)
    if state is not None:
        return state.sleeping
    state = presentation.user.update_cache(user_id)
    return state.sleeping


def set_sleep(user: discord.Member, message: discord.Message):
    if not is_event_available(user) or message.content not in settings.sleeping_bonus.sleep_words:
        return

    presentation.user.register_if_not_exist(user)

    if is_sleeping(user.id):
        return

    context = models.SleepContext(
        user_id=user.id,
        time=clock.get_now(),
        refresh_time=settings.sleeping_bonus.accept_wake_up_end_time,
        accept_start_time=settings.sleeping_bonus.accept_sleep_start_time,
        accept_end_time=settings.sleeping_bonus.accept_sleep_end_time
    )
    sleep: models.Sleep = models.Sleep(context)

    try:
        sleep.apply()
    except models.ModelError:
        logger.exception("An unknown exception raised while set the user slept.")
        return

    if sleep.result.status == models.SleepStatus.Accepted:
        presentation.user.update_cache(user.id)
        bot.reaction.sender.add(message, settings.sleeping_bonus.sleep_reaction)


def set_wake_up(user: discord.Member, channel: discord.TextChannel):
    if not is_event_available(user):
        return

    presentation.user.register_if_not_exist(user)

    if not is_sleeping(user.id):
        return

    context = models.WakeUpContext(
        user_id=user.id,
        time=clock.get_now(),
        point_on_accepted=settings.sleeping_bonus.point,
        accept_sleep_start_time=settings.sleeping_bonus.accept_sleep_start_time,
        accept_sleep_end_time=settings.sleeping_bonus.accept_sleep_end_time,
        accept_wake_up_start_time=settings.sleeping_bonus.accept_wake_up_start_time,
        accept_wake_up_end_time=settings.sleeping_bonus.accept_wake_up_end_time
    )
    wake_up: models.WakeUp = models.WakeUp(context)

    try:
        wake_up.apply()
    except models.ModelError:
        logger.exception("An unknown exception raised while set the user woke up.")
        return

    if wake_up.result.status == models.WakeUpStatus.Accepted:
        presentation.user.update_cache(user.id)
        message = helpers.phrase.get_random_phrase(settings.message.phrases.on_sleep_better, user.display_name)
        message += f"  `👏{'{:+}'.format(settings.sleeping_bonus.point)}`"
        bot.message.sender.send(channel, content=message)
    elif wake_up.result.status == models.WakeUpStatus.BeforeTerm:
        presentation.user.update_cache(user.id)
        message = helpers.phrase.get_random_phrase(settings.message.phrases.on_stay_up_late, user.display_name)
        bot.message.sender.send(channel, content=message)
    elif wake_up.result.status == models.WakeUpStatus.AfterTerm:
        presentation.user.update_cache(user.id)
        message = helpers.phrase.get_random_phrase(settings.message.phrases.on_wake_up_late, user.display_name)
        bot.message.sender.send(channel, content=message)
