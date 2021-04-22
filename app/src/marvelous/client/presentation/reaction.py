from logging import getLogger
from marvelous.models.super_marvelous import SuperMarvelousReaction
from marvelous.models.reaction import send_reaction, cancel_reaction, Reaction
from marvelous.models.user import is_user_exist
from marvelous.models.errors import ModelError
from .user import register_user_implicit
from . import response_super_marvelous
from ..discord import ReactionEvent
from marvelous.helpers import get_reaction


logger = getLogger(__name__)


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


async def response(event: ReactionEvent, send: bool, reaction: Reaction):
    if send and isinstance(reaction, SuperMarvelousReaction):
        await response_super_marvelous(event, reaction)


async def run_reaction_event(event: ReactionEvent, send: bool):
    if not is_event_available(event):
        return
    await register_users_if_not_exist(event)

    reaction = get_reaction(event.emoji)
    try:
        if send:
            send_reaction(event.sender.id, event.receiver.id, reaction)
        else:
            cancel_reaction(event.sender.id, event.receiver.id, reaction)
    except ModelError as err:
        logger.warning(str(err))
        return

    await response(event, send, reaction)


async def add_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=True)


async def remove_reaction(event: ReactionEvent):
    await run_reaction_event(event, send=False)
