import discord
from discord.ext import commands
from marvelous.settings import app_settings
from marvelous.client.discord.events.on_marvelous_reaction_remove import on_marvelous_reaction_remove
from marvelous.client.discord.events.on_super_marvelous_reaction_remove import on_super_marvelous_reaction_remove
from marvelous.client.discord.events.on_booing_reaction_remove import on_booing_reaction_remove
from marvelous.client.discord.actions.register_user_implicit import register_user_implicit
from marvelous.usecases.get_user import is_user_exist


@commands.Cog.listener()
async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    reaction_name = str(reaction)
    sender: discord.User = user
    receiver: discord.User = reaction.message.author

    if sender.id == receiver.id or sender.bot or receiver.bot:
        return

    if not is_user_exist(sender.id):
        await register_user_implicit(sender, reaction.message.channel)
    if not is_user_exist(receiver.id):
        await register_user_implicit(receiver, reaction.message.channel)

    if reaction_name in app_settings.marvelous.reactions:
        await on_marvelous_reaction_remove(reaction, user)
    elif reaction_name in app_settings.super_marvelous.reactions:
        await on_super_marvelous_reaction_remove(reaction, user)
    elif reaction_name in app_settings.booing.reactions:
        await on_booing_reaction_remove(reaction, user)


def setup(bot: commands.Bot):
    bot.add_listener(on_reaction_remove)
