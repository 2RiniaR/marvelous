from marvelous.models.user import User
from typing import Dict, Tuple
from marvelous.models.daily_bonus import DailyBonus


def to_parameter(user: User) -> Dict[str, str]:
    return {
        "discord_id": str(user.discord_id),
        "display_name": str(user.display_name),
        "marvelous_point": str(user.point),
        "super_marvelous_left": str(user.super_marvelous_left),
        "marvelous_bonus_step": str(user.marvelous_bonus.step),
        "marvelous_bonus_today_step": str(user.marvelous_bonus.today),
        "booing_penalty_step": str(user.booing_penalty.step),
        "booing_penalty_today_step": str(user.booing_penalty.today),
        "survival_bonus_given": "1" if user.survival_bonus_given else "0",
    }


def to_user(data: Tuple[str, str, str, str, str, str, str, str, str]) -> User:
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
