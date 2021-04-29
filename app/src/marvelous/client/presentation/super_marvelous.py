from marvelous.models.super_marvelous import reset_super_marvelous_left
from marvelous.settings import app_settings
from marvelous.helpers import is_now_time, is_now_weekday


def check_reset_super_marvelous_left():
    reset_time = app_settings.super_marvelous.reset_time
    reset_weekday = app_settings.super_marvelous.reset_weekday
    if is_now_time(reset_time) and is_now_weekday(reset_weekday):
        reset_super_marvelous_left(app_settings.super_marvelous.initial_left_count)
