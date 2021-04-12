import discord
from marvelous.usecases.send_reaction import cancel_reaction
from marvelous.models.reaction import SuperMarvelousReaction, SuperMarvelousSettings
from marvelous.settings import app_settings
from marvelous.client.discord.actions.show_super_marvelous_count import show_super_marvelous_count


async def succeed(reaction: discord.Reaction, user: discord.User, super_marvelous: SuperMarvelousReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    if app_settings.message:
        message = f":x: :raised_hands: めっちゃえらい！  {sender.name} --> {receiver.name}"
        await channel.send(message)
        await show_super_marvelous_count(sender.id, channel)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_super_marvelous_reaction_remove(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    super_marvelous = SuperMarvelousReaction(settings=SuperMarvelousSettings(
        sender_point=app_settings.super_marvelous.send_point,
        receiver_point=app_settings.super_marvelous.receive_point
    ))

    try:
        cancel_reaction(sender.id, receiver.id, super_marvelous)
    except Exception as e:
        await failed(reaction, user, str(e))

    if super_marvelous.result.no_left_count:
        return

    await succeed(reaction, user, super_marvelous)

