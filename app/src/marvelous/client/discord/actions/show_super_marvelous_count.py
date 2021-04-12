import discord
from marvelous.usecases.get_user import get_user, UserNotFoundError
from marvelous.client.discord.message_gateway import message_gateway


async def show_super_marvelous_count(discord_id: int, channel: discord.TextChannel):
    try:
        user = get_user(discord_id)
    except UserNotFoundError as e:
        return

    message = f"残り使用可能 :raised_hands: {user.super_marvelous_left}"
    await message_gateway.send(message, channel)
