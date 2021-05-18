from marvelous.settings import app_settings
from marvelous.helpers import is_now_time
import marvelous.models as models
from logging import getLogger


logger = getLogger(__name__)


def check_reset_daily_steps():
    reset_time = app_settings.marvelous.send_bonus.reset_time
    if not is_now_time(reset_time):
        return
    run_reset_daily_steps()


def run_reset_daily_steps():
    try:
        models.reset_daily_steps()
    except models.ModelError as err:
        logger.error(str(err))
        return
