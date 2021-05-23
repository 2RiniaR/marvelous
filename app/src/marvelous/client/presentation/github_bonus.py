from marvelous.settings import app_settings
from marvelous.helpers import is_now_time
import marvelous.models as models
from logging import getLogger
import datetime


logger = getLogger(__name__)


def check_github_bonus():
    reset_time = app_settings.github.bonus_time
    if not is_now_time(reset_time):
        return
    run_github_bonus()


def run_github_bonus():
    try:
        today: datetime.date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        point: int = app_settings.github.bonus_point
        models.check_github_bonus(point, today)
    except models.ModelError:
        logger.exception("An unknown exception raised while checking github bonus.")
        return
