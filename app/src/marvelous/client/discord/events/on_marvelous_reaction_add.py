import discord
from marvelous.usecases.send_reaction import send_reaction
from marvelous.models.reaction import MarvelousReaction, MarvelousSettings
from marvelous.settings import app_settings
from marvelous.client.discord.message_gateway import message_gateway


async def succeed(reaction: discord.Reaction, user: discord.User, marvelous: MarvelousReaction):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    channel: discord.TextChannel = reaction.message.channel

    message = (
        f"**:clap: えらい！** が **{sender.name}** から **{receiver.name}** へ送られました！"
        f"{receiver.name} :clap:{'{:+}'.format(marvelous.result.receiver_point_diff)}"
    )
    if marvelous.result.sender_bonus_diff != 0:
        message += f"\n**ボーナス！**    {sender.name} :clap: {'{:+}'.format(marvelous.result.sender_point_diff)}"
    await message_gateway.send(message, channel)


async def failed(reaction: discord.Reaction, user: discord.User, message: str):
    pass


async def on_marvelous_reaction_add(reaction: discord.Reaction, user: discord.User):
    sender: discord.User = user
    receiver: discord.User = reaction.message.author
    marvelous = MarvelousReaction(settings=MarvelousSettings(
        daily_step_limit=app_settings.marvelous.send_bonus.daily_step_limit,
        steps_per_bonus=app_settings.marvelous.send_bonus.step_interval,
        sender_bonus_point=app_settings.marvelous.send_bonus.point,
        receiver_point=app_settings.marvelous.receive_point
    ))

    try:
        send_reaction(sender.id, receiver.id, marvelous)
    except Exception as e:
        await failed(reaction, user, str(e))

    await succeed(reaction, user, marvelous)
