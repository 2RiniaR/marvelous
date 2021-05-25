import marvelous.settings as settings
import marvelous.helpers as helpers
from marvelous.domain import models, services
import logging


logger = logging.getLogger(__name__)


def check_reset_daily_steps():
    reset_time = settings.marvelous.send_bonus.reset_time
    if not helpers.is_now_time(reset_time):
        return
    run_reset_daily_steps()


def run_reset_daily_steps():
    try:
        services.reset_daily_bonus()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting daily bonus steps.")
        return
