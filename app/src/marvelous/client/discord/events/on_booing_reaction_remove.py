import discord
from marvelous.usecases.send_reaction import cancel_reaction
from marvelous.models.reaction import BooingReaction, BooingSettings
from marvelous.settings import app_settings
from marvelous.client.discord.message_gateway import message_gateway


async def succeed(reaction: discord.Reaction, user: discord.User, booing: BooingReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    message = f":x: :middle_finger: カス！  {sender.name} --> {receiver.name}"
    await message_gateway.send(message, channel)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_booing_reaction_remove(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    booing = BooingReaction(settings=BooingSettings(
        daily_step_limit=app_settings.booing.send_penalty.daily_step_limit,
        steps_per_bonus=app_settings.booing.send_penalty.step_interval,
        sender_bonus_point=app_settings.booing.send_penalty.point,
        receiver_point=app_settings.booing.receive_point
    ))

    try:
        cancel_reaction(sender.id, receiver.id, booing)
    except Exception as e:
        await failed(reaction, user, str(e))

    await succeed(reaction, user, booing)
