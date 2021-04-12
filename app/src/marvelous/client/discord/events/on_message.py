import discord
from discord.ext import commands
import marvelous.settings
from marvelous.usecases.give_survival_bonus import give_survival_bonus
from marvelous.usecases.get_user import is_user_exist, UserNotFoundError
from marvelous.settings import app_settings
from marvelous.client.discord.actions.register_user_implicit import register_user_implicit


async def succeed(message: discord.Message):
    author: discord.User = message.author
    if app_settings.message:
        await message.channel.send(f"{author.name}、今日も生きててえらいね！  :clap: +1")


@commands.Cog.listener()
async def on_message(message: discord.Message):
    author: discord.User = message.author
    if author.bot:
        return
    if not is_user_exist(author.id):
        await register_user_implicit(author, message.channel)

    try:
        bonus_given = give_survival_bonus(author.id, app_settings.survival.point)
    except UserNotFoundError as e:
        return

    if bonus_given:
        await succeed(message)


def setup(bot: commands.Bot):
    bot.add_listener(on_message)
