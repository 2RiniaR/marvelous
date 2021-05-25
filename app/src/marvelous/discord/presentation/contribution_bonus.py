import marvelous.settings as settings
import marvelous.helpers as helpers
from marvelous.domain import models, services
import logging
import datetime


logger = logging.getLogger(__name__)


def check_github_bonus():
    reset_time = settings.contribution_bonus.given_time
    if not helpers.is_now_time(reset_time):
        return
    run_github_bonus()


def run_github_bonus():
    try:
        today: datetime.date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        point: int = settings.github.point
        services.give_contribution_bonus(point, today)
    except models.ModelError:
        logger.exception("An unknown exception raised while checking github bonus.")
        return
