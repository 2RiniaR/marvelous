from typing import Tuple
from marvelous.models.daily_bonus import DailyBonus
from marvelous.models.user import User


def convert_to_user(data: Tuple[str, str, str, str, str, str, str, str, str]) -> User:
    (discord_id, display_name, marvelous_point, super_marvelous_left, marvelous_bonus_step,
     marvelous_bonus_today_step, booing_penalty_step, booing_penalty_today_step, survival_bonus_given) = data
    return User(
        discord_id=int(discord_id),
        display_name=display_name,
        point=int(marvelous_point),
        super_marvelous_left=int(super_marvelous_left),
        marvelous_bonus=DailyBonus(step=int(marvelous_bonus_step), today=int(marvelous_bonus_today_step)),
        booing_penalty=DailyBonus(step=int(booing_penalty_step), today=int(booing_penalty_today_step)),
        survival_bonus_given=int(survival_bonus_given) == 1
    )
