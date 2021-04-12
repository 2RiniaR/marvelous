from marvelous.models.user import User
from marvelous.models.daily_bonus import DailyBonus
from marvelous.settings import app_settings
import discord


def get_initial_user(user: discord.User):
    return User(
        discord_id=user.id,
        display_name=user.display_name,
        marvelous_bonus=DailyBonus(step=0, today=0),
        booing_penalty=DailyBonus(step=0, today=0),
        super_marvelous_left=app_settings.super_marvelous.initial_left_count,
        survival_bonus_given=False,
        point=0,
    )
