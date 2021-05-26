from marvelous import settings, helpers, services, models
import logging
import datetime


logger = logging.getLogger(__name__)


def check_give_time():
    reset_time = settings.contribution_bonus.given_time
    if not helpers.time.is_now_time(reset_time):
        return
    give()


def give():
    try:
        today: datetime.date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        point: int = settings.contribution_bonus.point
        services.contribution_bonus.give(point, today)
    except models.ModelError:
        logger.exception("An unknown exception raised while checking github bonus.")
        return
