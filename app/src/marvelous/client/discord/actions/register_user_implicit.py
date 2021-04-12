import discord
from marvelous.usecases.register_user import register_user, AlreadyExistError
from marvelous.client.discord.actions.get_initial_user import get_initial_user
from marvelous.models.user import User


async def register_user_implicit(author: discord.User, channel: discord.TextChannel):
    """暗黙的にユーザーを新規登録する"""
    try:
        user: User = get_initial_user(author)
        register_user(user)
    except AlreadyExistError as e:
        return

    message = f":white_check_mark: ユーザーを新規登録しました: {user.display_name}"
    await channel.send(message)
