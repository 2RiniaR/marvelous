import discord
from marvelous.usecases.send_reaction import send_reaction
from marvelous.models.reaction import SuperMarvelousReaction, SuperMarvelousSettings
from marvelous.settings import app_settings
from marvelous.client.discord.actions.show_super_marvelous_count import show_super_marvelous_count


async def succeed(reaction: discord.Reaction, user: discord.User, super_marvelous: SuperMarvelousReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    if app_settings.message:
        message = ":raised_hands:    " * 3 + "**" + str(receiver.name) + "**" + "    :raised_hands:" * 3
        message += (
            f"\n**:raised_hands: めっちゃえらい！** が **{sender.name}** から **{receiver.name}** へ送られました！    "
            f"{receiver.name} :clap:{'{:+}'.format(super_marvelous.result.receiver_point_diff)}\n"
            f"**ボーナス！**    {sender.name} :clap: {'{:+}'.format(super_marvelous.result.sender_point_diff)}"
        )
        await channel.send(message)
        await show_super_marvelous_count(sender.id, channel)


async def no_left_count(reaction: discord.Reaction, user: discord.User, super_marvelous: SuperMarvelousReaction):
    sender: discord.User = user
    channel: discord.TextChannel = reaction.message.channel

    message = f":no_entry: {sender.name} >>> 「めっちゃえらい！」の残り使用回数が0です"
    await channel.send(message)
    await show_super_marvelous_count(sender.id, channel)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_super_marvelous_reaction_add(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    super_marvelous = SuperMarvelousReaction(settings=SuperMarvelousSettings(
        sender_point=app_settings.super_marvelous.send_point,
        receiver_point=app_settings.super_marvelous.receive_point
    ))

    try:
        send_reaction(sender.id, receiver.id, super_marvelous)
    except Exception as e:
        await failed(reaction, user, str(e))

    if super_marvelous.result.no_left_count:
        await no_left_count(reaction, user, super_marvelous)
    else:
        await succeed(reaction, user, super_marvelous)
