import discord
from marvelous.usecases.send_reaction import cancel_reaction
from marvelous.models.reaction import MarvelousReaction, MarvelousSettings
from marvelous.settings import app_settings
from marvelous.client.discord.message_gateway import message_gateway


async def succeed(reaction: discord.Reaction, user: discord.User, marvelous: MarvelousReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    message = f":x: :clap: えらい！  {sender.name} --> {receiver.name}"
    await message_gateway.send(message, channel)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_marvelous_reaction_remove(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    marvelous = MarvelousReaction(settings=MarvelousSettings(
        daily_step_limit=app_settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=app_settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=app_settings.marvelous.send_bonus.point,
        receiver_point=app_settings.marvelous.receive_point
    ))

    try:
        cancel_reaction(sender.id, receiver.id, marvelous)
    except Exception as e:
        await failed(reaction, user, str(e))

    await succeed(reaction, user, marvelous)
