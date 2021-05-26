from marvelous import services, models, helpers, settings
import logging


logger = logging.getLogger(__name__)


def check_reset_time():
    reset_time = settings.super_marvelous.reset_time
    reset_weekday = settings.super_marvelous.reset_weekday
    if not (helpers.time.is_now_time(reset_time) and helpers.time.is_now_weekday(reset_weekday)):
        return
    reset()


def reset():
    try:
        services.super_marvelous.reset_left_count(settings.super_marvelous.initial_left_count)
    except models.ModelError:
        logger.error("An unknown exception raised while resetting super marvelous left count.")
        return
