import discord
from marvelous.models.events import (
    MarvelousReaction, MarvelousSettings, BooingReaction, BooingSettings,
    SuperMarvelousReaction, SuperMarvelousSettings, Reaction
)
from marvelous.settings import app_settings


def get_marvelous() -> MarvelousReaction:
    return MarvelousReaction(settings=MarvelousSettings(
        daily_step_limit=app_settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=app_settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=app_settings.marvelous.send_bonus.point,
        receiver_point=app_settings.marvelous.receive_point
    ))


def get_booing() -> BooingReaction:
    return BooingReaction(settings=BooingSettings(
        daily_step_limit=app_settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=app_settings.booing.send_penalty.step_interval,
        sender_bonus_point=app_settings.booing.send_penalty.point,
        receiver_point=app_settings.booing.receive_point
    ))


def get_super_marvelous() -> SuperMarvelousReaction:
    return SuperMarvelousReaction(settings=SuperMarvelousSettings(
        sender_point=app_settings.super_marvelous.send_point,
        receiver_point=app_settings.super_marvelous.receive_point
    ))


def get_reaction(emoji: discord.PartialEmoji) -> Reaction:
    str_emoji = str(emoji)
    if str_emoji in app_settings.marvelous.reactions:
        return get_marvelous()
    elif str_emoji in app_settings.super_marvelous.reactions:
        return get_super_marvelous()
    elif str_emoji in app_settings.booing.reactions:
        return get_booing()
