import discord
import logging
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional
from marvelous import services, models, settings, helpers
from marvelous.discord import presentation, cache, bot


logger = logging.getLogger(__name__)


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


def get_marvelous_model() -> models.MarvelousReaction:
    return models.MarvelousReaction(settings=models.MarvelousSettings(
        daily_step_limit=settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=settings.marvelous.send_bonus.point,
        receiver_point=settings.marvelous.receive_point
    ))


def get_super_marvelous_model() -> models.SuperMarvelousReaction:
    return models.SuperMarvelousReaction(settings=models.SuperMarvelousSettings(
        sender_point=settings.super_marvelous.send_point,
        receiver_point=settings.super_marvelous.receive_point
    ))


def get_booing_model() -> models.BooingReaction:
    return models.BooingReaction(settings=models.BooingSettings(
        daily_step_limit=settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=settings.booing.send_penalty.step_interval,
        sender_bonus_point=settings.booing.send_penalty.point,
        receiver_point=settings.booing.receive_point
    ))


def get_reaction_model(reaction_type: ReactionType) -> Optional[models.Reaction]:
    if reaction_type == ReactionType.Marvelous:
        return get_marvelous_model()
    elif reaction_type == ReactionType.SuperMarvelous:
        return get_super_marvelous_model()
    elif reaction_type == ReactionType.Booing:
        return get_booing_model()
    return None


def get_reaction_type(emoji: str) -> Optional[ReactionType]:
    if emoji == settings.marvelous.reaction:
        return ReactionType.Marvelous
    elif emoji == settings.super_marvelous.reaction:
        return ReactionType.SuperMarvelous
    elif emoji == settings.booing.reaction:
        return ReactionType.Booing
    return None


def is_event_available(event: ReactionEvent) -> bool:
    return (
            event.sender.id != event.receiver.id and
            not event.sender.bot and
            not event.receiver.bot
    )


def response_to_marvelous(event: ReactionEvent):
    if event.reaction is None:
        return
    if settings.marvelous.random_message_count == event.reaction.count:
        message = helpers.phrase.get_random_phrase(settings.message.phrases.on_receive_many_marvelous, event.receiver.display_name)
        bot.message.sender.send(event.channel, content=message)


def response_to_booing(event: ReactionEvent):
    if event.reaction is None:
        return
    if settings.marvelous.random_message_count == event.reaction.count:
        message = helpers.phrase.get_random_phrase(settings.message.phrases.on_receive_many_booing, event.receiver.display_name)
        bot.message.sender.send(event.channel, content=message)


def response_to_super_marvelous(event: ReactionEvent, reaction: models.SuperMarvelousReaction):
    if reaction.result.no_left_count:
        message = f":no_entry: {event.sender.display_name}    <<<    「めっちゃえらい！」の残り使用回数が0です"
    else:
        message = (
            f"{':raised_hands: '}**【{str(event.receiver.display_name)}】**{' :raised_hands:'}"
            f"    *by {event.sender.display_name}*"
            f"\n{helpers.phrase.get_random_phrase(settings.message.phrases.on_receive_super_marvelous, event.receiver.display_name)}"
        )
    bot.message.sender.send(event.channel, content=message)


def response_to_reaction(event: ReactionEvent, send: bool, reaction: models.Reaction):
    if send and isinstance(reaction, models.MarvelousReaction):
        response_to_marvelous(event)
    elif send and isinstance(reaction, models.BooingReaction):
        response_to_booing(event)
    elif send and isinstance(reaction, models.SuperMarvelousReaction):
        response_to_super_marvelous(event, reaction)


def run_event(event: ReactionEvent, send: bool):
    if not is_event_available(event):
        return

    presentation.user.register_if_not_exist(event.sender)
    presentation.user.register_if_not_exist(event.receiver)

    reaction_type = get_reaction_type(event.emoji)
    reaction = get_reaction_model(reaction_type)
    if reaction is None:
        return

    try:
        if send:
            services.reaction.send(event.sender.id, event.receiver.id, reaction)
        else:
            services.reaction.cancel(event.sender.id, event.receiver.id, reaction)
    except models.ModelError:
        logger.exception("An unknown exception raised while processing reaction.")
        return

    response_to_reaction(event, send, reaction)


def add(event: ReactionEvent):
    run_event(event, send=True)


def remove(event: ReactionEvent):
    run_event(event, send=False)


async def __fetch_event(ctx: cache.reaction.ReactionContext) -> Optional[ReactionEvent]:
    guild: discord.Guild = bot.instance.client.get_guild(ctx.guild_id)
    sender: discord.Member = guild.get_member(ctx.user_id)
    channel: discord.TextChannel = guild.get_channel(ctx.channel_id)
    if sender is None or channel is None:
        return None

    try:
        message: discord.Message = await channel.fetch_message(ctx.message_id)
    except discord.DiscordException as err:
        logger.warning(str(err))
        return None

    receiver: discord.Member = message.author
    if not isinstance(receiver, discord.Member):
        return None

    reaction: Optional[discord.Reaction] = helpers.iterable.first_match(
        message.reactions, pred=lambda r: str(r.emoji) == ctx.emoji_str, default=None)

    return ReactionEvent(
        sender=sender,
        channel=channel,
        receiver=receiver,
        reaction=reaction,
        emoji=ctx.emoji_str
    )


async def __reflect_state(state: cache.reaction.ReactionState):
    if state.initial_state == state.current_state:
        return

    event = await __fetch_event(state.context)
    if event is None:
        return

    if state.current_state:
        add(event)
    else:
        remove(event)


async def reflect_caches():
    states = cache.reaction.memory.get_all_states()
    cache.reaction.memory.reset()
    for state in states:
        await __reflect_state(state)


def __is_cache_target(emoji: discord.PartialEmoji) -> bool:
    str_emoji = str(emoji)
    return str_emoji in [
        settings.marvelous.reaction,
        settings.super_marvelous.reaction,
        settings.booing.reaction
    ]


def set_state(payload: discord.RawReactionActionEvent, is_added: bool):
    if not __is_cache_target(payload.emoji):
        return

    reaction_context = cache.reaction.ReactionContext(
        guild_id=payload.guild_id,
        user_id=payload.user_id,
        channel_id=payload.channel_id,
        message_id=payload.message_id,
        emoji_str=str(payload.emoji)
    )

    if not cache.reaction.memory.is_state_registered(reaction_context):
        cache.reaction.memory.register_state(reaction_context, not is_added)
    cache.reaction.memory.set_state(reaction_context, is_added)

