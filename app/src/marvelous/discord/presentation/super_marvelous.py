import marvelous.settings as settings
import marvelous.helpers as helpers
from marvelous.domain import models, services
import logging


logger = logging.getLogger(__name__)


def check_reset_super_marvelous_left():
    reset_time = settings.super_marvelous.reset_time
    reset_weekday = settings.super_marvelous.reset_weekday
    if not (helpers.is_now_time(reset_time) and helpers.is_now_weekday(reset_weekday)):
        return
    run_reset_super_marvelous_left()


def run_reset_super_marvelous_left():
    try:
        services.reset_super_marvelous_left_count(settings.super_marvelous.initial_left_count)
    except models.ModelError:
        logger.error("An unknown exception raised while resetting super marvelous left count.")
        return
