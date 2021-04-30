import discord
from logging import getLogger
from .user import register_user_implicit
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
from marvelous.settings import app_settings
from marvelous.models.reaction import send_reaction, cancel_reaction, Reaction
from marvelous.models.user import is_user_exist
from marvelous.models.errors import ModelError
from marvelous.models.super_marvelous import SuperMarvelousReaction, SuperMarvelousSettings
from marvelous.models.marvelous import MarvelousReaction, MarvelousSettings
from marvelous.models.booing import BooingReaction, BooingSettings
from ..discord import message_gateway


logger = getLogger(__name__)


class ReactionType(IntEnum):
    Marvelous = 0
    SuperMarvelous = 1
    Booing = 2


@dataclass()
class ReactionEvent:
    sender: discord.User
    receiver: discord.User
    channel: discord.TextChannel
    reaction_type: ReactionType


def get_marvelous() -> MarvelousReaction:
    return MarvelousReaction(settings=MarvelousSettings(
        daily_step_limit=app_settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=app_settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=app_settings.marvelous.send_bonus.point,
        receiver_point=app_settings.marvelous.receive_point
    ))


def get_super_marvelous() -> SuperMarvelousReaction:
    return SuperMarvelousReaction(settings=SuperMarvelousSettings(
        sender_point=app_settings.super_marvelous.send_point,
        receiver_point=app_settings.super_marvelous.receive_point
    ))


def get_booing() -> BooingReaction:
    return BooingReaction(settings=BooingSettings(
        daily_step_limit=app_settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=app_settings.booing.send_penalty.step_interval,
        sender_bonus_point=app_settings.booing.send_penalty.point,
        receiver_point=app_settings.booing.receive_point
    ))


def get_reaction(reaction_type: ReactionType) -> Optional[Reaction]:
    if reaction_type == ReactionType.Marvelous:
        return get_marvelous()
    elif reaction_type == ReactionType.SuperMarvelous:
        return get_super_marvelous()
    elif reaction_type == ReactionType.Booing:
        return get_booing()
    return None


def is_event_available(event: ReactionEvent) -> bool:
    return (
            event.sender.id != event.receiver.id and
            not event.sender.bot and
            not event.receiver.bot
    )


async def register_users_if_not_exist(event: ReactionEvent):
    if not is_user_exist(event.sender.id):
        await register_user_implicit(event.sender)
    if not is_user_exist(event.receiver.id):
        await register_user_implicit(event.receiver)


async def response_super_marvelous(event: ReactionEvent, reaction: SuperMarvelousReaction):
    if reaction.result.no_left_count:
        message = f":no_entry: {event.sender.name}    <<<    「めっちゃえらい！」の残り使用回数が0です"
    else:
        message = (
            f"{event.sender.display_name}    >>>    "
            f"{':raised_hands:    ' * 3}"
            f"**{str(event.receiver.name)}**"
            f"{'    :raised_hands:' * 3}"
        )
    await message_gateway.send(message, event.channel)


async def response(event: ReactionEvent, send: bool, reaction: Reaction):
    if send and isinstance(reaction, SuperMarvelousReaction):
        await response_super_marvelous(event, reaction)


async def run_reaction_event(event: ReactionEvent, send: bool):
    if not is_event_available(event):
        return
    await register_users_if_not_exist(event)

    reaction = get_reaction(event.reaction_type)
    if reaction is None:
        return

    try:
        if send:
            send_reaction(event.sender.id, event.receiver.id, reaction)
        else:
            cancel_reaction(event.sender.id, event.receiver.id, reaction)
    except ModelError as err:
        logger.error(str(err))
        return

    await response(event, send, reaction)


async def add_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=True)


async def remove_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=False)
