import logging
from marvelous import helpers, settings, services, models
from marvelous.discord import presentation


logger = logging.getLogger(__name__)


def check_reset_time():
    reset_time = settings.user.reset_marvelous_point_time
    reset_weekday = settings.user.reset_marvelous_point_weekday
    if not (helpers.time.is_now_time(reset_time) and helpers.time.is_now_weekday(reset_weekday)):
        return
    reset()


def reset():
    presentation.weekly_news.send_message()
    try:
        services.marvelous_point.reset()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting marvelous point.")
        return
