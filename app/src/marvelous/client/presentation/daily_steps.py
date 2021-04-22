from marvelous.models.daily_bonus import reset_daily_steps
from marvelous.settings import app_settings
from marvelous.helpers import is_now_time


def check_reset_daily_steps():
    reset_time = app_settings.marvelous.send_bonus.reset_time
    if is_now_time(reset_time):
        reset_daily_steps()
