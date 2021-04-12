import discord
from marvelous.usecases.send_reaction import send_reaction
from marvelous.models.reaction import BooingReaction, BooingSettings
from marvelous.settings import app_settings


async def succeed(reaction: discord.Reaction, user: discord.User, booing: BooingReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    if app_settings.message:
        message = (
            f"**:middle_finger: カス！** が **{sender.name}** から **{receiver.name}** へ送られました！    "
            f"{receiver.name} :clap:{'{:+}'.format(booing.result.receiver_point_diff)}"
        )
        if booing.result.sender_penalty_diff != 0:
            message += f"\n**ペナルティ！**    {sender.name} :clap: {'{:+}'.format(booing.result.sender_point_diff)}"
        await channel.send(message)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_booing_reaction_add(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    booing = BooingReaction(settings=BooingSettings(
        daily_step_limit=app_settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=app_settings.booing.send_penalty.step_interval,
        sender_bonus_point=app_settings.booing.send_penalty.point,
        receiver_point=app_settings.booing.receive_point
    ))

    try:
        send_reaction(sender.id, receiver.id, booing)
    except Exception as e:
        await failed(reaction, user, str(e))

    await succeed(reaction, user, booing)
