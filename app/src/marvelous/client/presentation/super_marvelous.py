from marvelous.settings import app_settings
from marvelous.helpers import is_now_time, is_now_weekday
import marvelous.models as models
from logging import getLogger


logger = getLogger(__name__)


def check_reset_super_marvelous_left():
    reset_time = app_settings.super_marvelous.reset_time
    reset_weekday = app_settings.super_marvelous.reset_weekday
    if not (is_now_time(reset_time) and is_now_weekday(reset_weekday)):
        return
    run_reset_super_marvelous_left()


def run_reset_super_marvelous_left():
    try:
        models.reset_super_marvelous_left(app_settings.super_marvelous.initial_left_count)
    except models.ModelError as err:
        logger.error(str(err))
        return
