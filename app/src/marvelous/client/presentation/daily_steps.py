from marvelous.models.daily_bonus import reset_daily_steps
from marvelous.settings import app_settings
from marvelous.helpers import is_now_time
from marvelous.models.errors import ModelError
from logging import getLogger


logger = getLogger(__name__)


def check_reset_daily_steps():
    reset_time = app_settings.marvelous.send_bonus.reset_time
    if not is_now_time(reset_time):
        return

    try:
        reset_daily_steps()
    except ModelError as err:
        logger.error(str(err))
        return
