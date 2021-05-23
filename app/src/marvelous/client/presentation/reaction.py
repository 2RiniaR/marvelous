import discord
from logging import getLogger
from .user import register_user_implicit
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
from marvelous.settings import app_settings
import marvelous.models as models
from marvelous.settings.messages import get_message
from ..discord import message_gateway
from .user import is_user_exist


logger = getLogger(__name__)


class ReactionType(IntEnum):
    Marvelous = 0
    SuperMarvelous = 1
    Booing = 2


@dataclass()
class ReactionEvent:
    sender: discord.Member
    receiver: discord.Member
    channel: discord.TextChannel
    reaction: Optional[discord.Reaction]
    emoji: str


def get_marvelous() -> models.MarvelousReaction:
    return models.MarvelousReaction(settings=models.MarvelousSettings(
        daily_step_limit=app_settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=app_settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=app_settings.marvelous.send_bonus.point,
        receiver_point=app_settings.marvelous.receive_point
    ))


def get_super_marvelous() -> models.SuperMarvelousReaction:
    return models.SuperMarvelousReaction(settings=models.SuperMarvelousSettings(
        sender_point=app_settings.super_marvelous.send_point,
        receiver_point=app_settings.super_marvelous.receive_point
    ))


def get_booing() -> models.BooingReaction:
    return models.BooingReaction(settings=models.BooingSettings(
        daily_step_limit=app_settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=app_settings.booing.send_penalty.step_interval,
        sender_bonus_point=app_settings.booing.send_penalty.point,
        receiver_point=app_settings.booing.receive_point
    ))


def get_reaction(reaction_type: ReactionType) -> Optional[models.Reaction]:
    if reaction_type == ReactionType.Marvelous:
        return get_marvelous()
    elif reaction_type == ReactionType.SuperMarvelous:
        return get_super_marvelous()
    elif reaction_type == ReactionType.Booing:
        return get_booing()
    return None


def get_reaction_type(emoji: str) -> Optional[ReactionType]:
    if emoji == app_settings.marvelous.reaction:
        return ReactionType.Marvelous
    elif emoji == app_settings.super_marvelous.reaction:
        return ReactionType.SuperMarvelous
    elif emoji == app_settings.booing.reaction:
        return ReactionType.Booing
    return None


def is_event_available(event: ReactionEvent) -> bool:
    return (
            event.sender.id != event.receiver.id and
            not event.sender.bot and
            not event.receiver.bot
    )


async def response_marvelous(event: ReactionEvent):
    if event.reaction is None:
        return
    if app_settings.marvelous.random_message_count == event.reaction.count:
        message = get_message("praise_something", event.receiver.display_name)
        await message_gateway.send(event.channel, content=message)


async def response_booing(event: ReactionEvent):
    if event.reaction is None:
        return
    if app_settings.marvelous.random_message_count == event.reaction.count:
        message = get_message("comfort", event.receiver.display_name)
        await message_gateway.send(event.channel, content=message)


async def response_super_marvelous(event: ReactionEvent, reaction: models.SuperMarvelousReaction):
    if reaction.result.no_left_count:
        message = f":no_entry: {event.sender.display_name}    <<<    「めっちゃえらい！」の残り使用回数が0です"
    else:
        message = (
            f"{':raised_hands: '}**【{str(event.receiver.display_name)}】**{' :raised_hands:'}"
            f"    *by {event.sender.display_name}*"
            f"\n{get_message('praise_something', event.receiver.display_name)}"
        )
    await message_gateway.send(event.channel, content=message)


async def response(event: ReactionEvent, send: bool, reaction: models.Reaction):
    if send and isinstance(reaction, models.MarvelousReaction):
        await response_marvelous(event)
    elif send and isinstance(reaction, models.BooingReaction):
        await response_booing(event)
    elif send and isinstance(reaction, models.SuperMarvelousReaction):
        await response_super_marvelous(event, reaction)


async def run_reaction_event(event: ReactionEvent, send: bool):
    if not is_event_available(event):
        return

    await register_user_implicit(event.sender)
    await register_user_implicit(event.receiver)

    reaction_type = get_reaction_type(event.emoji)
    reaction = get_reaction(reaction_type)
    if reaction is None:
        return

    try:
        if send:
            models.send_reaction(event.sender.id, event.receiver.id, reaction)
        else:
            models.cancel_reaction(event.sender.id, event.receiver.id, reaction)
    except models.ModelError:
        logger.exception("An unknown exception raised while processing reaction.")
        return

    await response(event, send, reaction)


async def add_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=True)


async def remove_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=False)
