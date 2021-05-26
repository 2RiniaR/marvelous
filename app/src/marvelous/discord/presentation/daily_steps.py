from marvelous import settings, helpers, services, models
import logging


logger = logging.getLogger(__name__)


def check_reset_time():
    reset_time = settings.marvelous.send_bonus.reset_time
    if not helpers.time.is_now_time(reset_time):
        return
    reset()


def reset():
    try:
        services.daily_bonus.reset()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting daily bonus steps.")
        return
